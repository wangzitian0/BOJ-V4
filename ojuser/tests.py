#  from django.conf import settings
#  from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
#  from django.test import TestCase, override_settings

from django.contrib.auth.models import User

#  from account.models import SignupCode, EmailConfirmation


class SignupViewTestCase(TestCase):

    def test_get(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "goo",
            "gender": "S",
        }
        response = self.client.post(reverse("account_signup"), data)
        self.assertEqual(response.status_code, 302)

    def test_get_authenticated(self):
        User.objects.create_user("foo", password="bar")
        self.client.login(username="foo", password="bar")

        with self.settings(ACCOUNT_LOGIN_REDIRECT_URL="/logged-in/"):
            response = self.client.get(reverse("account_signup"))
            self.assertRedirects(response, "/logged-in/", fetch_redirect_response=False)

    def test_post_authenticated(self):
        User.objects.create_user("foo", password="bar")
        self.client.login(username="foo", password="bar")

        with self.settings(ACCOUNT_LOGIN_REDIRECT_URL="/logged-in/"):
            data = {
                "username": "foo",
                "password": "bar",
                "password_confirm": "bar",
                "email": "foobar@example.com",
                "nickname": "goo",
                "gender": "S",
                "code": "abc123",
            }
            response = self.client.post(reverse("account_signup"), data)
            self.assertEqual(response.status_code, 404)

    def test_get_next_url(self):
        next_url = "/next-url/"
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "goo",
            "gender": "S",
        }
        response = self.client.post("{}?next={}".format(reverse("account_signup"), next_url), data)
        self.assertRedirects(response, next_url, fetch_redirect_response=False)

    def test_post_next_url(self):
        next_url = "/next-url/"
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "goo",
            "gender": "S",
            "next": next_url,
        }
        response = self.client.post(reverse("account_signup"), data)
        self.assertRedirects(response, next_url, fetch_redirect_response=False)

    def test_session_next_url(self):
        next_url = "/next-url/"
        session = self.client.session
        session["redirect_to"] = next_url
        session.save()
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "goo",
            "gender": "S",
        }
        response = self.client.post(reverse("account_signup"), data)
        self.assertRedirects(response, next_url, fetch_redirect_response=False)
