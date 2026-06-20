import allure





@allure.epic("Mobile Testing Platform")

@allure.feature("Login Module")

class TestMetaReporting:



    @allure.story("Valid user login")

    def test_login_success(self):

        with allure.step("Start test: valid login flow"):

            allure.attach(

                "User enters correct credentials",

                name="Input data",

                attachment_type=allure.attachment_type.TEXT

            )

            assert True



    @allure.story("Invalid user login")

    def test_login_failure(self):

        with allure.step("Start test: invalid login flow"):

            allure.attach(

                "User enters wrong password",

                name="Input data",

                attachment_type=allure.attachment_type.TEXT

            )

            assert True