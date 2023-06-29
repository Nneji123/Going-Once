import os
import random
import time

import requests
from dotenv import load_dotenv

load_dotenv()


PAYSTACK_API_KEY = os.environ.get("PAYSTACK_API_KEY")


def generate_reference_id() -> str:
    timestamp = str(int(time.time() * 1000))
    random_number = str(random.randint(1000, 9999))
    reference_id = timestamp + random_number
    return reference_id


class PaystackAPI:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.base_url = "https://api.paystack.co/"

    def _make_request(self, url, method="GET", json=None):
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}{url}"
        response = requests.request(method, url, headers=headers, json=json)
        response.raise_for_status()
        return response.json()

    def create_transfer_recipient(
        self,
        recipient_type,
        name,
        account_number,
        bank_code,
        currency,
        email=None,
        authorization_code=None,
    ):
        """Create a transfer recipient for a bank account, mobile money, or authorization code."""
        url = "transferrecipient"
        data = {
            "type": recipient_type,
            "name": name,
            "account_number": account_number,
            "bank_code": bank_code,
            "currency": currency,
        }
        if email:
            data["email"] = email
        if authorization_code:
            data["authorization_code"] = authorization_code

        return self._make_request(url, method="POST", json=data)

    def transfer_money(self, recipient_code, amount, reason=None):
        """Transfer money to a recipient."""
        url = "transfer"
        data = {
            "source": "balance",
            "amount": amount * 100,
            "recipient": recipient_code,
        }
        if reason:
            data["reason"] = reason

        return self._make_request(url, method="POST", json=data)

    def collect_payment(self, reference, amount, email):
        """Collect payments from a customer"""
        url = "transaction/initialize"
        data = {"reference": reference, "amount": amount * 100, "email": email}
        return self._make_request(url, method="POST", json=data)


paystack = PaystackAPI(secret_key="sk_test_d06b8c83ca756582a55428f9ef39c0dfb4ff0978")
# Example usage of collect_payment method
# reference = generate_reference_id()
# amount = 10000  # Replace with actual amount
# email = "ifeanyinneji777@gmail.com"  # Replace with actual email
# response = paystack.collect_payment(reference, amount, email)
# authorization_url = response['data']['authorization_url']
# print("Authorization URL: ", authorization_url)

# # Example of accessing access_code and reference from the response
# access_code = response['data']['access_code']
# transaction_reference = response['data']['reference']
# print("Access Code: ", access_code)
# print("Transaction Reference: ", transaction_reference)


# Create a transfer recipient
recipient_type = (
    "nuban"  # Can be "nuban" for bank account or "mobile_money" for mobile money
)
name = "John Doe"
account_number = "0123456789"
bank_code = "057"  # Bank code for the bank where the recipient's account is located
currency = "NGN"  # Currency for the transfer (e.g. "NGN" for Nigerian Naira)
email = "test@gmail.com"  # Optional, only required for mobile money recipients
authorization_code = (
    None  # Optional, only required for recipients with authorization codes
)

recipient_response = paystack.create_transfer_recipient(
    recipient_type, name, account_number, bank_code, currency, email, authorization_code
)

# Extract recipient code from the response
recipient_code = recipient_response["data"]["recipient_code"]

# Transfer money to the recipient
amount = 5000  # Amount to transfer in Naira
reason = "Payment for services"  # Optional, reason for the transfer
transfer_response = paystack.transfer_money(recipient_code, amount, reason)

# Handle the response as needed
print(transfer_response)
