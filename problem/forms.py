from django import forms
from django_select2.forms import ModelSelect2MultipleWidget
#  from django.contrib.auth.models import Group
from .models import Problem
from ojuser.models import GroupProfile


class ProblemForm(forms.ModelForm):


    class Meta:
        model = Problem
        exclude = ["superadmin", "is_checked"]
        widgets = {
            'allowed_lang': ModelSelect2MultipleWidget(
                search_fields=[
                    'key__icontains',
                    'name__icontains',
                ]
            ),
            'groups': ModelSelect2MultipleWidget(
                search_fields=[
                    'name__icontains',
                    'nickname__icontains',
                ]
            ),
        }


