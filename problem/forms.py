from django import forms
from django_select2.forms import ModelSelect2MultipleWidget
#  from django.contrib.auth.models import Group
from .models import Problem


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = '__all__'
        widgets = {
            'groups': ModelSelect2MultipleWidget(
                search_fields=['name__icontains', ]
            ),
        }
