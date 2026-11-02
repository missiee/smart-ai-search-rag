import os

os.makedirs('docs', exist_ok=True)

FILES = {}

FILES['refund_policy.txt'] = '''
ShopEasy Refund and Return Policy

1. Order cancellation
You can cancel an order before it ships. Go to My Orders, select the order and click Cancel Order. Cancelled orders are refunded in full to the original payment method within 5 to 7 working days.

2. Returns after delivery
You can return most items within 7 days of delivery. The item must be unused, in its original packaging, with all tags and accessories. To start a return, go to My Orders and click Return Item. We arrange a free pickup within 3 working days.

3. Refund timeline
After we receive and inspect the returned item, your refund is credited to the original payment method within 5 to 7 working days. For cash on delivery orders, the refund is sent to your bank account or to your ShopEasy Wallet, whichever you choose in the return request.

4. Items that cannot be returned
Gift cards, digital products, innerwear and items marked Final Sale cannot be returned or refunded.

5. Damaged or wrong items
If you received a damaged, defective or wrong item, report it within 48 hours of delivery. Go to My Orders, click Report a Problem and upload a photo. We will send a replacement or a full refund including shipping charges.

6. Checking refund status
You can check your refund status under My Orders, then Refund Details. If a refund has not arrived after 10 working days, contact support with your order number.
'''

FILES['shipping_policy.txt'] = '''
ShopEasy Shipping and Delivery Policy

1. Delivery options
Standard delivery takes 4 to 7 working days. Express delivery takes 1 to 2 working days and costs an extra 99 rupees. Orders above 499 rupees get free standard shipping. For orders below 499 rupees, the shipping fee is 49 rupees.

2. Dispatch time
Most orders are dispatched within 24 hours on working days. Once your order is dispatched, you receive an email and an SMS with a tracking link.

3. Tracking your order
Go to My Orders and click Track Order to see the live status of your package.

4. Delayed or missing packages
If your package has not arrived within 10 working days of dispatch, contact support with your order number. We will investigate with the courier partner and send a replacement or a full refund.

5. Changing the delivery address
You can change the address only before the order is dispatched. Go to My Orders and click Edit Address. After dispatch, the address cannot be changed.

6. Delivery attempts
Our courier partner makes 3 delivery attempts. If all attempts fail, the package returns to our warehouse and the order is refunded.

7. Cash on delivery
Cash on delivery is available for orders up to 5000 rupees. International shipping is not available at this time.
'''

FILES['account_help.txt'] = '''
ShopEasy Account Help

1. Resetting your password
On the login page, click Forgot Password and enter your registered email or mobile number. We send an OTP or a reset link that is valid for 15 minutes. Set a new password with at least 8 characters and one number.

2. Did not receive the reset email or OTP
Check your spam folder and wait 2 minutes. Then request a new link. Make sure you typed the same email or mobile number that you used to register.

3. Account locked
After 5 wrong password attempts, your account is locked for 30 minutes. After that time you can try again or reset your password.

4. Changing your email or mobile number
Go to Account Settings, then Profile. You must verify the new email or number with an OTP.

5. Login with Google
If you registered with Google, use the Continue with Google button and the same Google account.

6. Two step verification
You can turn on two step verification in Account Settings, then Security.

7. Deleting your account
Go to Account Settings and click Delete Account. Pending orders must be completed first. Your data is removed within 30 days.
'''

FILES['billing_faq.txt'] = '''
ShopEasy Billing and Payments FAQ

1. Downloading your invoice
Go to My Orders, select the order and click Download Invoice. The invoice is available after the order is dispatched.

2. GST invoice
To get a GST invoice, enter your GST number at checkout. It cannot be added after the order is placed.

3. Payment methods
We accept UPI, credit and debit cards, net banking, ShopEasy Wallet and cash on delivery.

4. Payment failed but money was deducted
If money was deducted but no order was created, the bank automatically returns the amount within 5 to 7 working days. If it does not arrive, contact support with your transaction ID.

5. Charged twice
If you were charged twice for one order, send us the transaction ID and a screenshot. After verification, the extra amount is refunded within 7 working days.

6. Coupons
Only one coupon can be used per order. Coupons cannot be combined and cannot be used after the expiry date.

7. EMI
EMI is available on orders above 3000 rupees with selected credit cards for 3, 6 or 9 months.
'''

FILES['product_faq.txt'] = '''
ShopEasy Product FAQ

1. Warranty
Electronics come with a 1 year manufacturer warranty. To make a claim, go to My Orders and click Warranty Claim. Keep your invoice ready.

2. Size exchange
Clothing and shoes can be exchanged once within 7 days of delivery for a different size, subject to stock availability.

3. Product authenticity
All sellers on ShopEasy are verified and all products are 100 percent genuine.

4. Out of stock items
Click Notify Me on the product page. We send you an email when the item is back in stock.

5. Product reviews
Only verified buyers can write reviews. You can write a review from My Orders after delivery.

6. Bulk orders
For orders of more than 10 units of one product, write to bulk@shopeasy.example for special pricing.
'''

for name, text in FILES.items():
    with open(os.path.join('docs', name), 'w', encoding='utf-8') as f:
        f.write(text.strip() + '\n')
    print('Created', name)