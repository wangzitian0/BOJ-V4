#  -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from rest_framework import status
from rest_framework.test import APITestCase

from django.core import mail
from .models import Language, GroupProfile
from django.contrib.auth.models import User

from account.models import EmailConfirmation


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


class LoginViewTestCase(TestCase):

    def signup(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "goo",
            "gender": "S",
        }
        self.client.post(reverse("account_signup"), data)
        self.client.logout()

    def test_get(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["account/login.html"])

    def test_post_wrong_password(self):
        self.signup()
        data = {
            "username": "foo",
            "password": "1234",
        }
        response = self.client.post(reverse("account_login"), data)
        self.assertEqual(response.status_code, 200)


    def test_post_empty(self):
        data = {}
        response = self.client.post(reverse("account_login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())

    @override_settings(
        AUTHENTICATION_BACKENDS=[
            "account.auth_backends.UsernameAuthenticationBackend",
        ]
    )
    def test_post_success(self):
        self.signup()
        data = {
            "username": "foo",
            "password": "bar",
        }
        response = self.client.post(reverse("account_login"), data)
        self.assertRedirects(
            response,
            settings.ACCOUNT_LOGIN_REDIRECT_URL,
            fetch_redirect_response=False
        )


class LogoutViewTestCase(TestCase):

    def signup(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "goo",
            "gender": "S",
        }
        self.client.post(reverse("account_signup"), data)

    def test_get_anonymous(self):
        response = self.client.get(reverse("account_logout"))
        self.assertRedirects(
            response,
            settings.ACCOUNT_LOGOUT_REDIRECT_URL,
            fetch_redirect_response=False
        )

    def test_get_authenticated(self):
        self.signup()
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["account/logout.html"])

    def test_post_anonymous(self):
        response = self.client.post(reverse("account_logout"), {})
        self.assertRedirects(
            response,
            settings.ACCOUNT_LOGOUT_REDIRECT_URL,
            fetch_redirect_response=False
        )

    def test_post_authenticated(self):
        self.signup()
        response = self.client.post(reverse("account_logout"), {})
        self.assertRedirects(
            response,
            settings.ACCOUNT_LOGOUT_REDIRECT_URL,
            fetch_redirect_response=False
        )


class ConfirmEmailViewTestCase(TestCase):

    def signup(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "goo",
            "gender": "S",
        }
        self.client.post(reverse("account_signup"), data)
        return EmailConfirmation.objects.get()

    def test_get_good_key(self):
        email_confirmation = self.signup()
        response = self.client.get(
            reverse("account_confirm_email", kwargs={"key": email_confirmation.key})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["account/email_confirm.html"])

    def test_get_bad_key(self):
        response = self.client.get(reverse("account_confirm_email", kwargs={"key": "badkey"}))
        self.assertEqual(response.status_code, 404)

    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_REQUIRED=True)
    def test_post_required(self):
        email_confirmation = self.signup()
        response = self.client.post(
            reverse("account_confirm_email", kwargs={"key": email_confirmation.key}), {}
        )
        self.assertRedirects(
            response,
            reverse(settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL),
            fetch_redirect_response=False
        )

    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_REQUIRED=False)
    def test_post_not_required(self):
        email_confirmation = self.signup()
        response = self.client.post(
            reverse("account_confirm_email", kwargs={"key": email_confirmation.key}), {}
        )
        self.assertRedirects(
            response,
            settings.ACCOUNT_LOGIN_REDIRECT_URL,
            fetch_redirect_response=False
        )


class ChangePasswordViewTestCase(TestCase):

    def signup(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "goo",
            "gender": "S",
        }
        self.client.post(reverse("account_signup"), data)
        mail.outbox = []
        return User.objects.get(username="foo")

    def test_get_anonymous(self):
        response = self.client.get(reverse("account_password"))
        self.assertRedirects(
            response,
            reverse("account_password_reset"),
            fetch_redirect_response=False
        )

    def test_get_authenticated(self):
        self.signup()
        response = self.client.get(reverse("account_password"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["account/password_change.html"])

    def test_post_anonymous(self):
        data = {
            "password_current": "password",
            "password_new": "new-password",
            "password_new_confirm": "new-password",
        }
        response = self.client.post(reverse("account_password"), data)
        self.assertEqual(response.status_code, 403)

    def test_post_authenticated_success(self):
        user = self.signup()
        data = {
            "password_current": "bar",
            "password_new": "new-bar",
            "password_new_confirm": "new-bar",
        }
        response = self.client.post(reverse("account_password"), data)
        self.assertRedirects(
            response,
            reverse(settings.ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL),
            fetch_redirect_response=False
        )
        updated_user = User.objects.get(username=user.username)
        self.assertNotEqual(user.password, updated_user.password)
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE=False)
    def test_post_authenticated_success_no_mail(self):
        self.signup()
        data = {
            "password_current": "bar",
            "password_new": "new-bar",
            "password_new_confirm": "new-bar",
        }
        response = self.client.post(reverse("account_password"), data)
        self.assertRedirects(
            response,
            reverse(settings.ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL),
            fetch_redirect_response=False
        )
        self.assertEqual(len(mail.outbox), 0)


class ProfilesTestCase(TestCase):

    def setUp(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
            "nickname": "foobar",
            "gender": "M",
        }
        self.client.post(reverse("account_signup"), data)
        Language.objects.create(key="gcc", name='GUN C', desc='gcc 11')
        self.client.login(username='foo', password='bar')

    def test_get(self):
        response = self.client.get(reverse("account_profiles"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["account/profiles.html"])
        self.assertContains(response, 'foo')
        self.assertContains(
            response,
            '''name="nickname" type="text" value="foobar"'''
        )
        self.assertContains(
            response,
            '''<option value="M" selected="selected">Male</option>'''
        )
        self.assertContains(
            response,
            '''<option value="1" selected="selected">GUN C</option>'''
        )

    def test_post_success(self):
        data = {
            "nickname": "google",
            "gender": "F",
            "prefer_lang": 1,
        }
        response = self.client.post(reverse("account_profiles"), data)
        self.assertRedirects(
            response,
            reverse("account_profiles"),
            fetch_redirect_response=False
        )


class MyGroupsCreateTestCase(TestCase):

    def setUp(self):
        xx = 'admin_A0'
        user = User.objects.create_user(xx, xx, xx)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        for ch in range(ord('a'), ord('b') + 1):
            xx = 'admin_' + chr(ch) + '0'
            user = User.objects.create_user(xx, xx, xx)
            user.is_staff = True
            user.save()

            gp = 0

            xx = 'group_' + chr(ch)
            if ch == ord('a'):
                gp = GroupProfile.objects.create(name=xx, nickname=xx, superadmin=user)
            else:
                pr = (ch - ord('a') + 1) / 2
                pr = GroupProfile.objects.get(pk=pr)
                gp = GroupProfile.objects.create(name=xx, nickname=xx, superadmin=user, parent=pr)

            xx = 'admin_' + chr(ch) + '1'
            user = User.objects.create_user(xx, xx, xx)
            user.is_staff = True
            user.save()
            gp.admin_group.user_set.add(user)

            xx = 'admin_' + chr(ch) + '2'
            user = User.objects.create_user(xx, xx, xx)
            gp.admin_group.user_set.add(user)

            xx = 'user_' + chr(ch) + '0'
            user = User.objects.create_user(xx, xx, xx)
            gp.admin_group.user_set.add(user)

            xx = 'user_' + chr(ch) + '1'
            user = User.objects.create_user(xx, xx, xx)
            gp.admin_group.user_set.add(user)

    def test_admin_create_group(self):
        self.client.login(username='admin_A0', password='admin_A0')
        response = self.client.get(reverse("mygroup-create"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["ojuser/group_create_form.html"])

    def test_staff_create_group(self):
        self.client.login(username='admin_a0', password='admin_a0')
        response = self.client.get(reverse("mygroup-create"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["ojuser/group_create_form.html"])

    def test_user_create_group(self):
        self.client.login(username='user_a0', password='user_a0')
        response = self.client.get(reverse("mygroup-create"))
        self.assertEqual(response.status_code, 302)

    def test_post_success(self):
        self.client.login(username='admin_a0', password='admin_a0')
        data = {
            "name": "gc1",
            "nickname": "gc2",
            "parent": 1,
            "admins": 2,
        }
        response = self.client.post(reverse("mygroup-create"), data)
        self.assertRedirects(
            response,
            reverse("mygroup-detail", kwargs={"pk": GroupProfile.objects.count()}),
            fetch_redirect_response=False
        )


class MyGroupsListTestCase(TestCase):

    def setUp(self):
        xx = 'admin_A0'
        user = User.objects.create_user(xx, xx, xx)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        for ch in range(ord('a'), ord('g') + 1):
            xx = 'admin_' + chr(ch) + '0'
            user = User.objects.create_user(xx, xx, xx)
            user.is_staff = True
            user.save()

            gp = 0

            xx = 'group_' + chr(ch)
            if ch == ord('a'):
                gp = GroupProfile.objects.create(name=xx, nickname=xx, superadmin=user)
            else:
                pr = (ch - ord('a') + 1) / 2
                pr = GroupProfile.objects.get(pk=pr)
                gp = GroupProfile.objects.create(name=xx, nickname=xx, superadmin=user, parent=pr)

            xx = 'admin_' + chr(ch) + '1'
            user = User.objects.create_user(xx, xx, xx)
            user.is_staff = True
            user.save()
            gp.admin_group.user_set.add(user)

            xx = 'admin_' + chr(ch) + '2'
            user = User.objects.create_user(xx, xx, xx)
            gp.admin_group.user_set.add(user)

            xx = 'user_' + chr(ch) + '0'
            user = User.objects.create_user(xx, xx, xx)
            gp.user_group.user_set.add(user)

            xx = 'user_' + chr(ch) + '1'
            user = User.objects.create_user(xx, xx, xx)
            gp.user_group.user_set.add(user)

        Language.objects.create(key="gcc", name='GUN C', desc='gcc 11')

    def test_get(self):
        self.client.login(username='admin_c0', password='admin_c0')
        response = self.client.get(reverse("mygroup-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ["ojuser/group_list.html", "ojuser/groupprofile_list.html"]
        )

    def test_superadmin_group(self):
        self.client.login(username='admin_A0', password='admin_A0')
        response = self.client.get(reverse("mygroup-list"))
        self.assertSequenceEqual(
            list(response.context['group_can_view']),
            list(GroupProfile.objects.filter(pk__in=[1, 2, 3, 4, 5, 6, 7, ])),
        )
        self.assertSequenceEqual(
            list(response.context['group_can_change']),
            list(GroupProfile.objects.filter(pk__in=[1, 2, 3, 4, 5, 6, 7, ])),
        )
        self.assertSequenceEqual(
            list(response.context['group_can_delete']),
            list(GroupProfile.objects.filter(pk__in=[1, 2, 3, 4, 5, 6, 7, ])),
        )
        self.assertContains(
            response,
            '''<a href="/accounts/mygroups/add" class="btn btn-large btn-primary">New </a>'''
        )

    def test_creater_group(self):
        self.client.login(username='admin_c0', password='admin_c0')
        response = self.client.get(reverse("mygroup-list"))
        self.assertSequenceEqual(
            list(response.context['group_can_view']),
            list(GroupProfile.objects.filter(pk__in=[1, 3, 6, 7, ])),
        )
        self.assertSequenceEqual(
            list(response.context['group_can_change']),
            list(GroupProfile.objects.filter(pk__in=[3, 6, 7, ])),
        )
        self.assertSequenceEqual(
            list(response.context['group_can_delete']),
            list(GroupProfile.objects.filter(pk__in=[3, ])),
        )
        self.assertContains(
            response,
            '''<a href="/accounts/mygroups/add" class="btn btn-large btn-primary">New </a>'''
        )

    def test_staff_group(self):
        self.client.login(username='admin_c1', password='admin_c1')
        response = self.client.get(reverse("mygroup-list"))
        self.assertContains(
            response,
            '''<a href="/accounts/mygroups/add" class="btn btn-large btn-primary">New </a>'''
        )

    def test_admin_group(self):
        self.client.login(username='admin_c2', password='admin_c2')
        response = self.client.get(reverse("mygroup-list"))
        self.assertSequenceEqual(
            list(response.context['group_can_view']),
            list(GroupProfile.objects.filter(pk__in=[1, 3, 6, 7, ])),
        )
        self.assertSequenceEqual(
            list(response.context['group_can_change']),
            list(GroupProfile.objects.filter(pk__in=[3, 6, 7, ])),
        )
        self.assertSequenceEqual(
            list(response.context['group_can_delete']),
            list(GroupProfile.objects.filter(pk__in=[])),
        )

    def test_user_group(self):
        self.client.login(username='user_c0', password='user_c0')
        response = self.client.get(reverse("mygroup-list"))
        self.assertSequenceEqual(
            list(response.context['group_can_view']),
            list(GroupProfile.objects.filter(pk__in=[1, 3, ])),
        )
        self.assertSequenceEqual(
            list(response.context['group_can_change']),
            list(GroupProfile.objects.filter(pk__in=[])),
        )
        self.assertSequenceEqual(
            list(response.context['group_can_delete']),
            list(GroupProfile.objects.filter(pk__in=[])),
        )

    def test_group_link(self):
        self.client.login(username='admin_c0', password='admin_c0')
        response = self.client.get(reverse("mygroup-list"))
        self.assertContains(
            response,
            '''<a href="/accounts/mygroups/3/" title="查看组资源">'''
        )
        self.assertContains(
            response,
            '''<a href="/accounts/mygroups/3/members/" title="成员管理">'''
        )
        self.assertContains(
            response,
            '''<a href="/accounts/mygroups/3/update/" title="修改组信息">'''
        )
        self.assertContains(
            response,
            '''<a href="/accounts/mygroups/3/delete/" title="删除组">'''
        )


class AccountTests(APITestCase):

    def setUp(self):
        xx = 'admin_A0'
        user = User.objects.create_user(xx, xx, xx)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        xx = 'admin_a0'
        user = User.objects.create_user(xx, xx, xx)
        user.is_staff = True
        user.save()

        xx = 'user_a0'
        user = User.objects.create_user(xx, xx, xx)

    def test_admin_create_account(self):
        url = reverse('language-list')
        data = {
            "key": "gcc",
            "name": "GUN C",
            "desc": "gcc -o a a.c"
        }
        self.client.login(username='admin_a0', password='admin_a0')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(Language.objects.get().key, 'gcc')

    def test_user_create_account(self):
        url = reverse('language-list')
        data = {
            "key": "gcc",
            "name": "GUN C",
            "desc": "gcc -o a a.c"
        }
        self.client.login(username='user_a0', password='user_a0')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
