from django import forms
import account.forms
from bojv4.conf import GENDER
from .models import UserProfile, GroupProfile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget


class UserProfileForm(account.forms.SignupForm):
    nickname = forms.CharField(
        label=_("Your Nickname"),
        max_length=30
    )
    gender = forms.ChoiceField(
        label=_("Your Gender"),
        choices=GENDER.choice(),
        initial=GENDER.choice()[0][0],
    )


class UserProfilesForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ['user', ]

"""
class GroupSearchWidget(ModelSelect2Widget):
    model = GroupProfile,
    search_fields = [
        'name__icontains',
        'nickname__icontains',
    ]

    #  def label_from_instance(self, group):
    #  return group.name + " - " + group.profile.nickname
"""


class GroupSearchForm(forms.Form):

    keyword = forms.ModelChoiceField(
        queryset=GroupProfile.objects.all(),
        #  widget=GroupSearchWidget()
        widget=ModelSelect2Widget(
            search_fields=[
                'name__icontains',
                'nickname__icontains',
            ]
        )
    )

    class Meta:
        fields = ['keyword', ]


class GroupForm(forms.ModelForm):
    admins = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=ModelSelect2MultipleWidget(
            queryset=User.objects.all(),
            search_fields=[
                'username__icontains',
            ]
        ),
    )

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            print "instance user_set============="
            print self.instance.user_set.all()
            self.fields['admins'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        instance = super(GroupForm, self).save(commit=False)
        instance.user_set.clear()
        for admin in self.cleaned_data['admins']:
            instance.user_set.add(admin)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Group
        #  fields = '__all__'
        fields = ['admins', ]


class GroupProfileForm(forms.ModelForm):
    class Meta:
        model = GroupProfile
        fields = ['name', 'nickname', 'parent', 'superadmin']
        widgets = {
            'parent': ModelSelect2Widget(
                search_fields=['name__icontains', ]
            ),
            'superadmin': ModelSelect2Widget(
                search_fields=['username__icontains',]
            )
        }

    def __init__(self, *args, **kwargs):
        print '=============kwargs========'
        print kwargs
        super(GroupProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            my_children = self.instance.get_descendants(include_self=True)
            self.fields['parent'].queryset = GroupProfile.objects.all().exclude(pk__in=my_children)

