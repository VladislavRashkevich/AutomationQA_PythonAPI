from requests import Response
from json.decoder import JSONDecodeError
from datetime import datetime

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in last response"
        return response.cookies.get(cookie_name)

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header with name {header_name}  in last response"
        return response.headers.get(header_name)

    def get_json_value(self, response: Response, name):
        try:
            response_json_as_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text '{response.text}'"
        assert name in response_json_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_json_as_dict[name]

    def prepare_registration_data(self, email=None):
        if not email:
            email = f"{datetime.now().strftime('%m%d%Y%H%M%S')}@example.com"

        data = {
            "password": 1234,
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email,
        }

        return data


