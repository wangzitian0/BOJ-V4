from django import forms
import account.forms
from django.forms import ModelForm


class UserProfileForm(account.forms.SignupForm):
    nickname = forms.CharField(max_length=30)
    gender = forms.CharField(max_length=6)
    prefer_lang = forms.CharField(max_length=6)


class UserSettingsForm(account.forms.SettingsForm):
    nickname = forms.CharField(max_length=30)
    gender = forms.CharField(max_length=6)
    prefer_lang = forms.CharField(max_length=6)
