import json
import ollama
from retrieval import search_with_score

MODEL = 'llama3.2:3b'
CATEGORIES = ['billing', 'refund', 'login', 'shipping', 'product_info', 'other']
SENSITIVE_WORDS = ['lawyer', 'legal', 'court', 'consumer forum', 'fraud', 'scam', 'chargeback', 'sue']


def classify(ticket):
    prompt = (
        'Classify this customer support ticket. '
        'Return JSON with two keys: category (one of ' + ', '.join(CATEGORIES) + ') '
        'and angry (true if the customer is very angry or threatens legal action, otherwise false).'
        '\n\nTicket: ' + ticket
    )
    resp = ollama.chat(
        model=MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        format='json',
    )
    try:
        data = json.loads(resp['message']['content'])
    except Exception:
        data = {}
    category = data.get('category', 'other')
    if category not in CATEGORIES:
        category = 'other'
    return category, bool(data.get('angry', False))


def draft_reply(ticket, hits):
    context = '\n\n'.join('[{}] {}'.format(h['source'], h['text']) for h in hits)
    system = (
        'You are a polite customer support agent. Answer ONLY using the context. '
        'Keep the reply short, clear and friendly. '
        'If the context does not contain the answer, reply with exactly: NOT_FOUND'
    )
    user_msg = 'Context:\n' + context + '\n\nCustomer ticket: ' + ticket
    resp = ollama.chat(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user_msg},
        ],
    )
    return resp['message']['content'].strip()


def handle_ticket(ticket, auto_t=0.55, review_t=0.40):
    category, angry = classify(ticket)
    sensitive = angry or any(w in ticket.lower() for w in SENSITIVE_WORDS)
    hits, top_sim = search_with_score(ticket, k=4)
    sources = sorted(set(h['source'] for h in hits))

    result = {
        'category': category,
        'angry': angry,
        'confidence': round(top_sim, 2),
        'sources': sources,
        'reply': '',
        'status': '',
        'reason': '',
    }

    # Raasta 1: seedha insaan ko bhejo
    if sensitive:
        result['status'] = 'escalated'
        result['reason'] = 'Sensitive ya gussa wala ticket'
        return result
    if category == 'other':
        result['status'] = 'escalated'
        result['reason'] = 'Category samajh nahi aayi'
        return result
    if top_sim < review_t:
        result['status'] = 'escalated'
        result['reason'] = 'Docs mein relevant jaankari nahi mili'
        return result

    # Jawab banao
    reply = draft_reply(ticket, hits)
    if 'NOT_FOUND' in reply:
        result['status'] = 'escalated'
        result['reason'] = 'Model ko docs mein jawab nahi mila'
        return result

    result['reply'] = reply
    if top_sim >= auto_t:
        result['status'] = 'auto_sent'
        result['reason'] = 'High confidence'
    else:
        result['status'] = 'needs_review'
        result['reason'] = 'Medium confidence, insaan check karein'
    return result