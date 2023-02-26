import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")

        # assert "user_id" in response1.json(), "There is no user id in the response"
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("This test successfully authorize user by email and password")
    def test_auth_user(self):
        response2 = MyRequests.get(
            '/user/auth',
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        # assert "user_id" in response2.json(), "There is no user id in the second response"
        # user_id_from_check_method = response2.json()["user_id"]
        #
        # assert self.user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

        Assertions.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method,
                                             "User id from auth method is not equal to user id from check method")

    @allure.description("Thes test checks authorization status w/o sending auth cookie and password")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == 'no_cookie':
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token}
            )
        else:
            response2 = MyRequests.get(
                "/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )

        # assert "user_id" in response2.json()
        #
        # user_id_from_check_method = response2.json()["user_id"]
        #
        # assert user_id_from_check_method == 0, "There is no user id in the second response"

        Assertions.assert_json_value_by_name(response2, "user_id", 0,
                                             "There is no user id in the second response")
