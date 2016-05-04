from django import forms
from .models import Submission
from django_select2.forms import ModelSelect2Widget


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('code', 'language')
        widgets = {
            'language': ModelSelect2Widget(
                search_fields=[
                    'key__icontains',
                    'name__icontains',
                    'desc__icontains',
                ]
            ),
        }

    def __init__(self, qs=None, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['language'].queryset = qs
