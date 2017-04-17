from django import forms
from django_select2.forms import ModelSelect2Widget
#  from django.contrib.auth.models import Group
from .models import Contest
from ojuser.models import GroupProfile


class ContestForm(forms.ModelForm):

    class Meta:
        model = Contest
        exclude = ["author", ]
        widgets = {
           'group': ModelSelect2Widget(
                search_fields=[
                    'name__icontains',
                    'nickname__icontains',
                ]
            ),
        }


