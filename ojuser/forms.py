from django import forms
import account.forms
from .models import UserProfile
from bojv4.conf import CONST
from django.utils.translation import ugettext_lazy as _

class UserProfileForm(account.forms.SignupForm):
    nickname = forms.CharField(
        label = _("Your Nickname"),
        max_length = 30
    )
    gender = forms.ChoiceField(
        label = _("Your Gender"),
        choices = CONST.GENDER,
        initial = CONST.GENDER[0][0],
    )
    prefer_lang = forms.ChoiceField(
        label = _("Your Perfer Language"),
        choices = CONST.LANGUAGE,
        initial = CONST.LANGUAGE[0],
    )


class UserSettingsForm(account.forms.SettingsForm):
    nickname = forms.CharField(
        label = _("Your Nickname"),
        max_length = 30
    )


class UserProfilesForm(forms.ModelForm):
    gender = forms.ChoiceField(
        label = _("Your Gender"),
        choices = CONST.GENDER,
        initial = CONST.GENDER[0][0],
    )
    prefer_lang = forms.ChoiceField(
        label = _("Your Perfer Language"),
        choices = CONST.LANGUAGE,
        initial = CONST.LANGUAGE[0],
    )
    class Meta:
        model = UserProfile
        fields = ['gender', 'prefer_lang',]

