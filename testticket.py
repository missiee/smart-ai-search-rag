TICKETS = [
    {'ticket': 'I cancelled my order yesterday. When will I get my refund?',
     'category': 'refund', 'escalate': False, 'source': 'refund_policy.txt'},
    {'ticket': 'How do I reset my password? I cannot log in.',
     'category': 'login', 'escalate': False, 'source': 'account_help.txt'},
    {'ticket': 'My package has not arrived after 10 days.',
     'category': 'shipping', 'escalate': False, 'source': 'shipping_policy.txt'},
    {'ticket': 'Where can I download my invoice?',
     'category': 'billing', 'escalate': False, 'source': 'billing_faq.txt'},
    {'ticket': 'This is a scam. I will contact my lawyer if I do not get my money back today.',
     'category': 'refund', 'escalate': True, 'source': ''},
    {'ticket': 'Can you recommend a good restaurant nearby?',
     'category': 'other', 'escalate': True, 'source': ''},
]