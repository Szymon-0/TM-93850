import allure

import pytest





@allure.feature("Attachments & Failure Handling")

class TestAttachments:



    @allure.story("Failure with screenshots and API logs")

    def test_failure_with_attachments(self):



        try:

            with allure.step("Start test and simulate API response"):

                api_response = '{"status": "ERROR", "code": 500}'



                allure.attach(

                    api_response,

                    name="API_Response",

                    attachment_type=allure.attachment_type.JSON

                )



                assert 1 == 2  # wymuszony FAIL



        except Exception as e:



            allure.attach(

                "Fake screenshot binary content",

                name="Screenshot_Error_01",

                attachment_type=allure.attachment_type.PNG

            )



            raise e