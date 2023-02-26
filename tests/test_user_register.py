import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    # def setup_method(self):
    #     base_part = "learnqa"
    #     domain = "example.com"
    #     random_part = datetime.now().strftime("%m%d%Y%H%M%S")
    #     self.email = f"{base_part}{random_part}@{domain}"
    exclude_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email"),
    ]

    def test_user_create_successfully(self):
        # data = {
        #     "password": 123,
        #     "username": "learnqa",
        #     "firstName": "learnqa",
        #     "lastName": "learnqa",
        #     "email": self.email,
        # }

        data = self.prepare_registration_data()

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        # email = "vinkotov@example.com"
        #
        # data = {
        #     "password": 123,
        #     "username": "learnqa",
        #     "firstName": "learnqa",
        #     "lastName": "learnqa",
        #     "email": email,
        # }

        data = self.prepare_registration_data(email="vinkotov@example.com")

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{data['email']}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_wrong_email(self):
        data = self.prepare_registration_data(email="vinkotovexample.com")

        response = MyRequests.post('/user/', data=data)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"The user with wrong email '{data['email']}' has been created"

    @pytest.mark.parametrize('exclude_param', exclude_params)
    def test_create_user_without_one_parameter(self, exclude_param):
        data = self.prepare_registration_data()
        data[exclude_param] = None

        response = MyRequests.post('/user/', data=data)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_param}", \
            f"The user has been created with missed parameter '{exclude_param}'"

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = data['username'][1]
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_content(response,
                                  f"The value of 'username' field is too short",
                                  "The user has been created with short 'username'")

    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = data['username']*250
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_content(response,
                                  "The value of 'username' field is too long",
                                  "The user was created with name more than 250 characters")



