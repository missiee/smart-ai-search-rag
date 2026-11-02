from ticketbot import handle_ticket
from testticket import TICKETS

cat_ok = 0
esc_ok = 0
src_ok = 0
src_total = 0
auto = 0
wrong_auto = 0

for t in TICKETS:
    r = handle_ticket(t['ticket'])
    escalated = r['status'] == 'escalated'

    if r['category'] == t['category']:
        cat_ok += 1
    if escalated == t['escalate']:
        esc_ok += 1
    if r['status'] == 'auto_sent':
        auto += 1
        if t['escalate']:
            wrong_auto += 1
    if not t['escalate']:
        src_total += 1
        if t['source'] in r['sources']:
            src_ok += 1

    print(r['status'], r['confidence'], '|', t['ticket'][:60])

n = len(TICKETS)
print('---')
print('Category accuracy:', round(100 * cat_ok / n), '%')
print('Escalation accuracy:', round(100 * esc_ok / n), '%')
print('Right source retrieved:', round(100 * src_ok / max(src_total, 1)), '%')
print('Auto-sent:', round(100 * auto / n), '%')
print('Wrongly auto-sent (danger):', wrong_auto)