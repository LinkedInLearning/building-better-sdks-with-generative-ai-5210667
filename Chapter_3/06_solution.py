import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class TwilioAPI:
    def __init__(self, account_sid=None, auth_token=None, base_url="https://api.twilio.com/2010-04-01"):
        """
        Initialize the TwilioAPI class.

        :param account_sid: Twilio Account SID
        :param auth_token: Twilio Auth Token
        :param base_url: Base URL for the Twilio API
        """
        self.account_sid = account_sid or os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = auth_token or os.getenv("TWILIO_AUTH_TOKEN")
        self.base_url = f"{base_url}/Accounts/{self.account_sid}"
        self.headers = {
            "Authorization": f"Basic {self._encode_credentials()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _encode_credentials(self):
        """
        Encode the account SID and auth token for basic authentication.

        :return: Encoded credentials
        """
        credentials = f"{self.account_sid}:{self.auth_token}"
        return base64.b64encode(credentials.encode()).decode()

    def _request(self, method, url, data=None):
        """
        Make an HTTP request.

        :param method: HTTP method (GET, POST, etc.)
        :param url: URL for the request
        :param data: Data to send with the request
        :return: JSON response
        """
        response = self.session.request(method, url, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()


class TwilioMessagingAPI(TwilioAPI):
    def send_message(self, to, from_, body):
        """
        Send an SMS message.

        :param to: The destination phone number
        :param from_: The phone number to send the message from
        :param body: The body of the message
        :return: The response from the API
        """
        url = f"{self.base_url}/Messages.json"
        data = {
            'To': to,
            'From': from_,
            'Body': body
        }
        return self._request("POST", url, data)

    def fetch_message(self, message_sid):
        """
        Fetch a message.

        :param message_sid: The SID of the message to fetch
        :return: The response from the API
        """
        url = f"{self.base_url}/Messages/{message_sid}.json"
        return self._request("GET", url)

    def list_messages(self, params=None):
        """
        List messages.

        :param params: Optional parameters for filtering the list
        :return: The response from the API
        """
        url = f"{self.base_url}/Messages.json"
        if params:
            url += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
        return self._request("GET", url)


# Example usage:
if __name__ == "__main__":
    account_sid = "your_account_sid"
    auth_token = "your_auth_token"
    twilio = TwilioMessagingAPI(account_sid, auth_token)

    try:
        # Send an SMS message
        response = twilio.send_message("+1234567890", "+0987654321", "Hello, World!")
        print(response)

        # Fetch a message
        message = twilio.fetch_message("SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print(message)

        # List messages
        messages = twilio.list_messages({'PageSize': 20})
        print(messages)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")