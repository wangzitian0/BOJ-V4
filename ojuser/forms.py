from django import forms
import account.forms
from .models import UserProfile, GroupProfile
from bojv4.conf import CONST
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget


class UserProfileForm(account.forms.SignupForm):
    nickname = forms.CharField(
        label=_("Your Nickname"),
        max_length=30
    )
    gender = forms.ChoiceField(
        label=_("Your Gender"),
        choices=CONST.GENDER,
        initial=CONST.GENDER[0][0],
    )
    prefer_lang = forms.ChoiceField(
        label=_("Your Perfer Language"),
        choices=CONST.LANGUAGE,
        initial=CONST.LANGUAGE[0],
    )


class UserSettingsForm(account.forms.SettingsForm):
    nickname = forms.CharField(
        label=_("Your Nickname"),
        max_length=30
    )


class UserProfilesForm(forms.ModelForm):
    gender = forms.ChoiceField(
        label=_("Your Gender"),
        choices=CONST.GENDER,
        initial=CONST.GENDER[0][0],
    )
    prefer_lang = forms.ChoiceField(
        label=_("Your Perfer Language"),
        choices=CONST.LANGUAGE,
        initial=CONST.LANGUAGE[0],
    )

    class Meta:
        model = UserProfile
        fields = ['gender', 'prefer_lang', ]


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        #  fields = '__all__'
        fields = ['name', ]


class GroupProfileForm(forms.ModelForm):
    class Meta:
        model = GroupProfile
        fields = ['nickname', 'admins', 'parent', ]
        widgets = {
            'admins': ModelSelect2MultipleWidget(
                search_fields=['username__icontains', ]
            ),
            'parent': ModelSelect2Widget(
                search_fields=['group__name__icontains', ]
            ),
        }
"""
    parents = forms.ModelMultipleChoiceField("self")

    def __init__(self, *args, **kwargs):
        super(GroupProfileForm, self).__init__(*args, **kwargs)
        group_profile_qs = GroupProfile.objects.all()
        self.fields['parents'].widget = ModelSelect2MultipleWidget(
            queryset=group_profile_qs,
            search_fields=['group__name__icontains', ]
        )
        self.fields['parents'].initial = self.instance.get_parents()
        self.fields['parents'].queryset = group_profile_qs

    def save(self, *args, **kwargs):
        instance = super(GroupProfileForm, self).save(*args, **kwargs)
        Consisting.objects.filter(child=instance).delete()
        #  need add some exception about circle
        for pr in self.cleaned_data['parents']:
            instance.add_parent(pr)

    class Meta:
        model = GroupProfile
        fields = ['nickname', 'admins', 'parents', ]
        widgets = {
            'admins': ModelSelect2MultipleWidget(
                search_fields=['username__icontains', ]
            ),
        }
"""
