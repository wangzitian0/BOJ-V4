from django import forms
import account.forms
from .models import UserProfile, GroupProfile, Consisting
from bojv4.conf import CONST
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django_select2.forms import ModelSelect2MultipleWidget


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
    parents = forms.ModelMultipleChoiceField("self")

    def __init__(self, *args, **kwargs):
        super(GroupProfileForm, self).__init__(*args, **kwargs)
        #  change it to groups which i can manager
        #  self.fields['parents'].queryset = self.instance._parents
        self.fields['parents'].queryset = GroupProfile.objects.all()
        self.fields['parents'].initial = self.instance.parents()
        self.fields['parents'].widget = ModelSelect2MultipleWidget(
            queryset=GroupProfile.objects.all(),
            search_fields=['group__name__icontains', ]
        )

    def save(self, *args, **kwargs):
        instance = super(GroupProfileForm, self).save(*args, **kwargs)
        Consisting.objects.filter(child=instance).delete()
        parents = []
        for pr in self.cleaned_data['parents']:
            gg = Consisting(parent=pr, child=instance)
            parents.append(gg)
        Consisting.objects.bulk_create(parents)

    class Meta:
        model = GroupProfile
        fields = ['nickname', 'admins', 'parents', ]
        widgets = {
            'admins': ModelSelect2MultipleWidget(
                search_fields=['username__icontains', ]
            ),
        }
