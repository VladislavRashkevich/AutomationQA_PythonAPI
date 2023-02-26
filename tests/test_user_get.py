import random

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        cookie_auth = self.get_cookie(response1, "auth_sid")
        x_csrf_token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            cookies={"auth_sid": cookie_auth},
            headers={"x-csrf-token": x_csrf_token}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

        # Assertions.assert_code_status(response2, 200)
        # Assertions.assert_json_has_key(response2, "username")
        # Assertions.assert_json_has_key(response2, "email")
        # Assertions.assert_json_has_key(response2, "firstName")
        # Assertions.assert_json_has_key(response2, "lastName")

    def test_get_only_username_not_auth_auth(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post('/user/login', data=data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")
        user_id = self.get_json_value(response_login, "user_id")

        cookies = {"auth_sid": auth_sid}
        headers = {"x-csrf-token": token}

        response_get_details = MyRequests.get(f"/user/1000", headers=headers, cookies=cookies)

        expected_fields = ["email", "firstName", "lastName"]

        Assertions.assert_code_status(response_get_details, 200)
        Assertions.assert_json_has_key(response_get_details, 'username')
        Assertions.assert_json_has_not_keys(response_get_details, expected_fields)
