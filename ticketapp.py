import html
import time

import pandas as pd
import streamlit as st

from ticketbot import handle_ticket

st.set_page_config(page_title='Ticket Bot', page_icon=':rocket:', layout='wide')

CSS = '''
@keyframes shift { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
@keyframes drop { from {opacity: 0; transform: translateY(-30px);} to {opacity: 1; transform: translateY(0);} }
@keyframes pulse { 0% {box-shadow: 0 0 0 0 rgba(255,255,255,0.7);} 70% {box-shadow: 0 0 0 16px rgba(255,255,255,0);} 100% {box-shadow: 0 0 0 0 rgba(255,255,255,0);} }
.hero { background: linear-gradient(120deg, #6366f1, #8b5cf6, #ec4899, #f59e0b, #06b6d4); background-size: 300% 300%; animation: drop 0.7s ease, shift 10s ease infinite; padding: 28px; border-radius: 18px; color: white; margin-bottom: 18px; }
.hero h1 { margin: 0; font-size: 2.1rem; color: white; }
.hero p { margin: 6px 0 0 0; opacity: 0.95; font-size: 1.05rem; }
.badge { display: inline-block; padding: 10px 24px; border-radius: 999px; color: white; font-weight: 700; font-size: 1.1rem; margin: 6px 0 14px 0; animation: pulse 1.6s ease 3; }
.card { border-radius: 16px; padding: 16px 18px; color: white; box-shadow: 0 8px 22px rgba(0,0,0,0.22); }
.card-title { opacity: 0.85; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; }
.card-value { font-size: 1.5rem; font-weight: 700; margin-top: 4px; }
.bar { height: 16px; border-radius: 999px; background: rgba(128,128,128,0.25); overflow: hidden; margin: 14px 0 6px 0; }
.fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #22c55e, #3b82f6, #a855f7); }
.slide { border-radius: 18px; padding: 28px; margin: 12px 0; color: white; min-height: 170px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }
.slide h3 { margin-top: 0; color: white; }
.dots { margin-top: 18px; }
.dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: rgba(255,255,255,0.4); margin-right: 8px; }
.dot.on { background: white; transform: scale(1.4); }
section[data-testid='stSidebar'] { background: linear-gradient(180deg, rgba(99,102,241,0.18), rgba(236,72,153,0.14)); }
div.stButton > button { border-radius: 999px; font-weight: 600; transition: transform 0.15s ease, box-shadow 0.15s ease; }
div.stButton > button:hover { transform: translateY(-2px) scale(1.03); box-shadow: 0 6px 18px rgba(99,102,241,0.45); }
button[kind='primary'], button[data-testid='stBaseButton-primary'] { background: linear-gradient(90deg, #6366f1, #ec4899); border: none; color: white; }
'''

VARIANT_CSS = '''
@keyframes popVARIANT { 0% {transform: scale(0.5); opacity: 0;} 70% {transform: scale(1.08); opacity: 1;} 100% {transform: scale(1); opacity: 1;} }
@keyframes growVARIANT { from {width: 0;} }
@keyframes rightVARIANT { from {opacity: 0; transform: translateX(90px);} to {opacity: 1; transform: translateX(0);} }
@keyframes leftVARIANT { from {opacity: 0; transform: translateX(-90px);} to {opacity: 1; transform: translateX(0);} }
.pop-VARIANT { animation: popVARIANT 0.6s ease both; }
.fill-VARIANT { animation: growVARIANT 1.1s ease both; }
.right-VARIANT { animation: rightVARIANT 0.55s ease both; }
.left-VARIANT { animation: leftVARIANT 0.55s ease both; }
'''
for v in ['a', 'b']:
    CSS += VARIANT_CSS.replace('VARIANT', v)

st.markdown('<style>' + CSS + '</style>', unsafe_allow_html=True)

st.markdown('''
<div class='hero'>
<h1>Customer Ticket Auto-Reply Bot</h1>
<p>Reads a ticket, searches the docs, drafts a reply and decides what to do next.</p>
</div>
''', unsafe_allow_html=True)

BADGES = {
    'auto_sent': ('AUTO SENT', '#16a34a, #22d3ee'),
    'needs_review': ('NEEDS REVIEW', '#f59e0b, #f97316'),
    'escalated': ('ESCALATED TO HUMAN', '#ef4444, #db2777'),
}

REASONS = {
    'Sensitive ya gussa wala ticket': 'Sensitive or angry ticket, sent to a human.',
    'Category samajh nahi aayi': 'Could not match the ticket to a store topic.',
    'Docs mein relevant jaankari nahi mili': 'No relevant information found in the documents.',
    'Model ko docs mein jawab nahi mila': 'The model could not find the answer in the documents.',
    'High confidence': 'High confidence, the reply can be sent automatically.',
    'Medium confidence, insaan check karein': 'Medium confidence, a human should review the reply.',
}

SLIDE_COLORS = [
    '#06b6d4, #3b82f6',
    '#8b5cf6, #ec4899',
    '#f59e0b, #ef4444',
    '#10b981, #06b6d4',
    '#6366f1, #a855f7',
]

SAMPLES = [
    'I cancelled my order yesterday. When will I get my refund?',
    'How do I reset my password? I cannot log in.',
    'My order has not arrived for 5 days. When will I get it?',
    'Where can I download my invoice?',
    'I am going to sue you, this is a scam!',
    'What is the capital of France?',
]

for key, default in [('ticket_text', ''), ('result', None), ('last_ticket', ''),
                     ('history', []), ('slide', 0), ('animate', False),
                     ('count', 0), ('dir', 'right')]:
    if key not in st.session_state:
        st.session_state[key] = default


def set_sample(text):
    st.session_state['ticket_text'] = text


def go(delta):
    st.session_state['slide'] = max(0, min(4, st.session_state['slide'] + delta))
    st.session_state['dir'] = 'right' if delta > 0 else 'left'


def start_play():
    st.session_state['playing'] = True


def type_words(text):
    for word in text.split(' '):
        yield word + ' '
        time.sleep(0.04)


def reason_en(r):
    return REASONS.get(r['reason'], r['reason'])


def card(title, value, colors, v, delay):
    return '''<div class='card pop-{}' style='background: linear-gradient(135deg, {}); animation-delay: {}s;'><div class='card-title'>{}</div><div class='card-value'>{}</div></div>'''.format(v, colors, delay, title, value)


def badge_html(r, v):
    label, colors = BADGES[r['status']]
    return '''<span class='badge pop-{}' style='background: linear-gradient(135deg, {});'>{}</span>'''.format(v, colors, label)


def build_slides(r, ticket):
    esc = html.escape
    nl = chr(10)
    if r['reply']:
        reply = esc(r['reply']).replace(nl, '<br>')
    else:
        reply = 'No reply was drafted. This ticket goes to a human.'
    angry = 'yes' if r.get('angry', False) else 'no'
    return [
        ('Ticket received', '<i>' + esc(ticket).replace(nl, '<br>') + '</i>'),
        ('Category detected', 'Category: <b>' + esc(r['category']) + '</b><br>Angry or legal threat: <b>' + angry + '</b>'),
        ('Searching documents', 'Closest documents: <b>' + esc(', '.join(r['sources'])) + '</b><br>Confidence: <b>' + str(r['confidence']) + '</b>'),
        ('Reply drafted', reply),
        ('Final decision', 'Status: <b>' + BADGES[r['status']][0] + '</b><br>Reason: ' + esc(reason_en(r))),
    ]


def slide_html(slide, i, n, direction):
    title, body = slide
    v = 'a' if i % 2 == 0 else 'b'
    dots = ''.join('''<span class='dot {}'></span>'''.format('on' if k == i else '') for k in range(n))
    return '''<div class='slide {}-{}' style='background: linear-gradient(135deg, {});'><h3>{}</h3><div>{}</div><div class='dots'>{}</div></div>'''.format(direction, v, SLIDE_COLORS[i], title, body, dots)


HAS_DIALOG = hasattr(st, 'dialog')

if HAS_DIALOG:
    @st.dialog('Ticket result')
    def show_popup(r, v):
        st.markdown(badge_html(r, v), unsafe_allow_html=True)
        st.write('Category: ' + r['category'])
        st.write('Confidence: ' + str(r['confidence']))
        st.write(reason_en(r))
        if r['reply']:
            st.info(r['reply'])


st.sidebar.header('Settings')
auto_t = st.sidebar.slider('Auto-send threshold', 0.0, 1.0, 0.45)
review_t = st.sidebar.slider('Review threshold', 0.0, 1.0, 0.25)
typing = st.sidebar.toggle('Typing animation', value=True)
celebrate = st.sidebar.toggle('Balloons on auto-send', value=True)
popup_on = st.sidebar.toggle('Pop-up result window', value=True)

st.sidebar.header('Sample tickets')
for i, s in enumerate(SAMPLES):
    st.sidebar.button(s[:38] + '...', key='sample' + str(i), on_click=set_sample, args=(s,))

tab1, tab2, tab3 = st.tabs(['Process ticket', 'How the bot decided', 'History'])

with tab1:
    ticket = st.text_area('Customer ticket', key='ticket_text', height=130,
                          placeholder='Type the customer message here, or pick a sample from the sidebar...')

    if st.button('Process ticket', type='primary') and ticket.strip():
        with st.spinner('The bot is reading the ticket, searching the docs and drafting a reply...'):
            result = handle_ticket(ticket, auto_t, review_t)
        st.session_state['result'] = result
        st.session_state['last_ticket'] = ticket
        st.session_state['slide'] = 0
        st.session_state['dir'] = 'right'
        st.session_state['animate'] = True
        st.session_state['count'] += 1
        st.session_state['history'].append({
            'ticket': ticket[:60],
            'category': result['category'],
            'status': result['status'],
            'confidence': result['confidence'],
        })
        if result['status'] == 'auto_sent' and celebrate:
            st.balloons()
        if result['status'] == 'escalated':
            st.toast('This ticket was sent to a human')
        if popup_on and HAS_DIALOG:
            show_popup(result, 'a' if st.session_state['count'] % 2 == 0 else 'b')

    r = st.session_state['result']
    if r:
        v = 'a' if st.session_state['count'] % 2 == 0 else 'b'
        st.markdown(badge_html(r, v), unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.markdown(card('Category', html.escape(r['category']), '#3b82f6, #06b6d4', v, 0.0), unsafe_allow_html=True)
        c2.markdown(card('Confidence', str(r['confidence']), '#8b5cf6, #ec4899', v, 0.12), unsafe_allow_html=True)
        c3.markdown(card('Docs matched', str(len(r['sources'])), '#f59e0b, #ef4444', v, 0.24), unsafe_allow_html=True)

        pct = int(min(max(float(r['confidence']), 0.0), 1.0) * 100)
        st.markdown('''<div class='bar'><div class='fill fill-{}' style='width: {}%;'></div></div>'''.format(v, pct), unsafe_allow_html=True)
        st.caption('Reason: ' + reason_en(r))

        animate = st.session_state['animate']
        st.session_state['animate'] = False
        if r['reply']:
            st.subheader('Reply')
            if typing and animate:
                st.write_stream(type_words(r['reply']))
            else:
                st.write(r['reply'])
        with st.expander('Sources'):
            for src in r['sources']:
                st.write('- ' + src)

with tab2:
    r = st.session_state['result']
    if not r:
        st.info('Process a ticket first, then come back here to replay how the bot decided.')
    else:
        slides = build_slides(r, st.session_state['last_ticket'])
        n = len(slides)
        box = st.empty()

        b1, b2, b3 = st.columns(3)
        b1.button('Previous', on_click=go, args=(-1,))
        b2.button('Next', on_click=go, args=(1,))
        b3.button('Play slideshow', on_click=start_play)

        if st.session_state.pop('playing', False):
            for i in range(n):
                box.markdown(slide_html(slides[i], i, n, 'right'), unsafe_allow_html=True)
                time.sleep(1.6)
            st.session_state['slide'] = n - 1
        else:
            idx = st.session_state['slide']
            box.markdown(slide_html(slides[idx], idx, n, st.session_state['dir']), unsafe_allow_html=True)

with tab3:
    history = st.session_state['history']
    if not history:
        st.info('No tickets processed yet.')
    else:
        df = pd.DataFrame(history)
        st.metric('Tickets processed (this session)', len(df))
        st.bar_chart(df['status'].value_counts())
        st.dataframe(df.iloc[::-1])