from django import forms
from .models import Submission
from bojv4.conf import LANGUAGE
from django_select2.forms import ModelSelect2Widget


class SubmissionForm(forms.ModelForm):

    language = forms.ChoiceField(label='language', choices=LANGUAGE.choice(), widget=forms.Select())

    class Meta:
        model = Submission
        fields = ('code', 'language')

    def __init__(self, qs=None, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
