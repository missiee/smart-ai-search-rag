from ticketbot import handle_ticket

ticket = input('Ticket likho: ')
r = handle_ticket(ticket)
for key, value in r.items():
    print(key, ':', value)