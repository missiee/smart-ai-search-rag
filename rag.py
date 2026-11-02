import ollama
from retrieval import search

MODEL = 'llama3.2:3b'

SYSTEM = (
    'Tum ek helpful assistant ho. Sirf diye gaye context se jawab do. '
    'Agar jawab context mein nahi hai to bolo: mujhe documents mein ye nahi mila. '
    'Jawab ke end mein source file ke naam likho.'
)


def answer(question, k=4):
    hits = search(question, k)
    context = '\n\n'.join('[{}] {}'.format(h['source'], h['text']) for h in hits)
    user_msg = 'Context:\n' + context + '\n\nSawal: ' + question
    resp = ollama.chat(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': user_msg},
        ],
    )
    return resp['message']['content'], hits