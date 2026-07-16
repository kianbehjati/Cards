from django.test import TestCase
from .views import pass_validate
from django.urls import reverse
from django.contrib.auth import get_user_model
class AuthTestCase(TestCase):
    def setUp(self):
        myUser = get_user_model()
        user = myUser.objects.create(username="test",phone_number="+989998887766",email="test@test.com")
        user.set_password("test1234@")
        user.save()
    def test_pass_validate(self):
        # str return means something failed
        self.assertIsInstance(pass_validate("test1234","test1234"),str)
        self.assertIsInstance(pass_validate("test1234","test1235"),str)

        self.assertIsInstance(pass_validate("Test1234","Test1234"),str)
        
        self.assertIsInstance(pass_validate("test1234@","test1234@"),str)
        self.assertIsInstance(pass_validate("Test1234@","Test1234!"),str)

        self.assertIsInstance(pass_validate("Test1234@ª","Test1234@ª"),str)

        self.assertIsInstance(pass_validate("Test14@","Test14@"),str)

        # only bool return of pass_validate is True
        self.assertIsInstance(pass_validate("Test1234@","Test1234@"),bool)

    def test_login(self):
        url = reverse("auth:login")
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

        # wrong username currect pass
        fail_post_response = self.client.post(url,data={"user_name":"tst","password":"test1234@"},follow=True)
        self.assertContains(fail_post_response,"*wrong credintials")
        self.assertEqual(fail_post_response.status_code, 200)

        # correct username wrong pass
        fail_post_response = self.client.post(url,data={"user_name":"test","password":"test1234"},follow=True)
        self.assertContains(fail_post_response,"*wrong credintials")
        self.assertEqual(fail_post_response.status_code, 200)

        # both wrong
        fail_post_response = self.client.post(url,data={"user_name":"tst","password":"test1234"},follow=True)
        self.assertContains(fail_post_response,"*wrong credintials")
        self.assertEqual(fail_post_response.status_code, 200)

        # both correct(success)
        success_post_response = self.client.post(url,data={"user_name":"test","password":"test1234@"},follow=True)
        self.assertContains(success_post_response,"Create Card")
        self.assertEqual(success_post_response.status_code, 200)

        # check already login redirect 
        response =  self.client.post(url,data={"user_name":"test","password":"test1234@"})
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        login_url = reverse("auth:login")
        login = self.client.post(login_url,data={"user_name":"test","password":"test1234@"})

        # logout to home ('/')
        logout_url = reverse("auth:logout")
        logout = self.client.get(logout_url,follow=True)
        self.assertRedirects(logout, "/")

        # logout to "next"(contactus for example)
        login = self.client.post(login_url,data={"user_name":"test","password":"test1234@"})
        logout = self.client.get(logout_url,{"next":reverse("contactus")},follow=True)
        self.assertRedirects(logout, reverse("contactus"))
        
    def test_signup(self):
        signup_url = reverse("auth:signup")

        data = {
            "user_name":"testuser",
            "email":"test@test1.com",
            "phone_input":"+989998887777",
            "password":"Test1234@",
            "confirm_password":"Test1234@"
        }

        # no phone
        no_phone = data.copy()
        no_phone["phone_input"] = ""
        user_create = self.client.post(signup_url,data=no_phone)
        self.assertContains(user_create,"*you should enter a valid phone number")

        # unvalid phone
        unvalid_phone = data.copy()
        unvalid_phone["phone_input"] = "+98999888777" # one digit short
        user_create = self.client.post(signup_url,data=unvalid_phone)
        self.assertContains(user_create,"*you should enter a valid phone number")

        unvalid_phone["phone_input"] = "+9899988877777" # one digit extra
        user_create = self.client.post(signup_url,data=unvalid_phone)
        self.assertContains(user_create,"*you should enter a valid phone number")

        # same username 
        same_username = data.copy()
        same_username["user_name"] = "test" # in set up
        user_create = self.client.post(signup_url,data=same_username)
        self.assertContains(user_create,"*an other user uses same username")

        # same phone
        same_phone = data.copy()
        same_phone["phone_input"] = "+989998887766" # in set up
        user_create = self.client.post(signup_url,data=same_phone)
        self.assertContains(user_create,"*an other user use same phone number")
        
        # same email
        same_email = data.copy()
        same_email["email"] = "test@test.com" # in set up
        user_create = self.client.post(signup_url,data=same_email)
        self.assertContains(user_create,"*an other user use same email")

        # optional email allowed
        no_email = data.copy()
        no_email["email"] = ""
        user_create = self.client.post(signup_url,data=no_email,follow=True)
        self.assertRedirects(user_create,reverse("auth:userpanel"))

    def test_forget_password(self):
        url = reverse("auth:forgetpass")
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

        # Wrong credentials (wrong username and/or wrong phone number)
        fail_post_response = self.client.post(url, data={"username": "wronguser", "phone_number": "+989998887766"}, follow=True)
        self.assertContains(fail_post_response, "*wrong credintials")

        fail_post_response2 = self.client.post(url, data={"username": "test", "phone_number": "+989123456789"}, follow=True)
        self.assertContains(fail_post_response2, "*wrong credintials")

        # Correct credentials (success)
        success_post_response = self.client.post(url, data={"username": "test", "phone_number": "+989998887766"})
        # Should redirect to password-change page with token
        self.assertEqual(success_post_response.status_code, 302)
        self.assertTrue(success_post_response.url.startswith("/auth/password-change/"))

    def test_user_edit(self):
        url = reverse("auth:useredit")
        
        # When logged out, it should redirect to login page
        logout_response = self.client.get(url)
        self.assertEqual(logout_response.status_code, 302)
        self.assertTrue(logout_response.url.startswith(reverse("auth:login")))

        # Log in first
        login_url = reverse("auth:login")
        self.client.post(login_url, data={"user_name": "test", "password": "test1234@"})

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

        # No Change
        same_data_response = self.client.post(url, data={
            "user_name": "test",
            "email": "test@test.com",
            "phone_input": "+989998887766"
        })
        self.assertEqual(same_data_response.status_code, 302)
        self.assertRedirects(same_data_response, reverse("auth:userpanel"))

        # Create another user to test unique fields constraints
        myUser = get_user_model()
        another_user = myUser.objects.create(username="other", phone_number="+989111111111", email="other@other.com")
        another_user.set_password("test1234@")
        another_user.save()


        fail_username_response = self.client.post(url, data={
            "user_name": "other",
            "email": "test@test.com",
            "phone_input": "+989998887766"
        })
        self.assertContains(fail_username_response, "an other user use same User name")

        fail_email_response = self.client.post(url, data={
            "user_name": "test",
            "email": "other@other.com",
            "phone_input": "+989998887766"
        })
        self.assertContains(fail_email_response, "an other user use same Email")

        fail_phone_response = self.client.post(url, data={
            "user_name": "test",
            "email": "test@test.com",
            "phone_input": "+989111111111"
        })
        self.assertContains(fail_phone_response, "an other user use same Phone Number")

        # Try an invalid phone number
        fail_invalid_phone = self.client.post(url, data={
            "user_name": "test",
            "email": "test@test.com",
            "phone_input": "+123"
        })
        self.assertContains(fail_invalid_phone, "Phone number is not valid")

        # Success
        success_edit = self.client.post(url, data={
            "user_name": "testnew",
            "email": "newtest@test.com",
            "phone_input": "+989222222222"
        })
        self.assertEqual(success_edit.status_code, 302)
        self.assertRedirects(success_edit, reverse("auth:userpanel"))

        # Verify database update
        user = myUser.objects.get(id=self.client.session['_auth_user_id'])
        self.assertEqual(user.username, "testnew")
        self.assertEqual(user.email, "newtest@test.com")
        self.assertEqual(user.phone_number, "+989222222222")
