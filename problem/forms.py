from django import forms
from django_select2.forms import ModelSelect2MultipleWidget
#  from django.contrib.auth.models import Group
from .models import Problem, ProblemTag
from ojuser.models import GroupProfile


class ProblemForm(forms.ModelForm):

    is_spj = forms.NullBooleanField(widget=forms.CheckboxInput(), initial=False)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=ProblemTag.objects.all(),
        widget=ModelSelect2MultipleWidget(
                 search_fields=[
                    'name__icontains',
                    'nickname__icontains',
                ]))

    class Meta:
        model = Problem
        exclude = ["superadmin", "is_checked", "created_time", "last_updated_time", "desc"]
        widgets = {
            'groups': ModelSelect2MultipleWidget(
                search_fields=[
                    'name__icontains',
                    'nickname__icontains',
                ]
            ),
            'tags': ModelSelect2MultipleWidget(
                search_fields=[
                    'name__icontains'
                ]
            )
        }


