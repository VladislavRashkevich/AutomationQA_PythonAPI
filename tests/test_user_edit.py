from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        #REGISTER
        register_data = self.prepare_registration_data()
        response_reg = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response_reg, "id")

        #LOGING
        loging_data = {
            "email": email,
            "password": password
        }

        response_loging = MyRequests.post("/user/login", data=loging_data)
        auth_sid = self.get_cookie(response_loging, "auth_sid")
        token = self.get_header(response_loging, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"
        new_last_name = "Changed Last"

        cookie = {"auth_sid": auth_sid}
        header = {"x-csrf-token": token}

        data_edit = {"firstName": new_name,
                     "lastName": new_last_name}

        response_edit = MyRequests.put(
            f"/user/{user_id}",
            data=data_edit,
            headers=header,
            cookies=cookie
        )
        Assertions.assert_code_status(response_edit, 200)

        #USER INFO
        response_get_info = MyRequests.get(
            f"/user/{user_id}",
            headers=header,
            cookies=cookie
        )

        Assertions.assert_code_status(response_get_info, 200)
        Assertions.assert_json_value_by_name(response_get_info, "firstName", new_name,
                                             "Wrong name of the user after edit")
        Assertions.assert_json_value_by_name(response_get_info, "lastName", new_last_name,
                                             "Wrong last name of the user after edit")
