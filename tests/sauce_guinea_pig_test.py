from .base_test import *
from .sauceutils import *
import uuid


@on_platforms(devices)
class TestGuineaPig(BaseTest):
    @classmethod
    def setup_class(cls):
        BaseTest.setup_class()
        if cls.upload and cls.sim_app_path is not None:
            upload_app(cls.sim_app_path, cls.username, cls.access_key)
        if cls.upload and cls.dev_app_path is not None:
            upload_app(cls.dev_app_path, cls.username, cls.access_key)

    def test_email_input(self):
        email = "hello@world.com"
        # populate text fields with values
        email_box = self.driver.find_element_by_id("fbemail")
        email_box.click()
        email_box.send_keys(email)

        # hide keyboard by clicking away
        self.driver.find_element_by_id("h1Text").click()

        read_back = email_box.text
        # .value_of_css_property("value")
        assert (read_back == email, "Input: %s , does not match read back: %s" % (email, read_back))

    def test_comment_input(self):
        comments = str(uuid.uuid4())
        # populate text fields with values
        comment_box = self.driver.find_element_by_id("comments")
        comment_box.click()
        comment_box.send_keys(comments)

        # hide keyboard by clicking away
        self.driver.find_element_by_id("h1Text").click()
        # click submit
        self.driver.find_element_by_id("submit").click()

        submitted_comments = self.driver.find_element_by_id("submittedComments").text
        # .value_of_css_property("value")
        assert (submitted_comments == comments,
                "Input: %s , does not match read back: %s" % (comments, submitted_comments))


if __name__ == '__main__':
    unittest.main()
