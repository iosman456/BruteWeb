import json
import requests

class UtilityTools:
    @staticmethod
    def save_to_json(domain, domain_info, server_info):
        data = {
            'domain': domain,
            'domain_info': domain_info,
            'server_info': server_info
        }
        with open('protecth.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def sms_bomber(phone_number, message, count):
        for i in range(count):
            try:
                response = requests.post(
                    "https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID/Messages.json",
                    auth=("YOUR_ACCOUNT_SID", "YOUR_AUTH_TOKEN"),
                    data={"From": "YOUR_TWILIO_NUMBER",
                          "To": phone_number,
                          "Body": message})
                print(f"Sent SMS {i+1} to {phone_number} - Status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error: {e}")
