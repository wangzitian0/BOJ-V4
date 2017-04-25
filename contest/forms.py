# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime, timedelta, date, time
from bojv4.conf import LANGUAGE_MASK, LANGUAGE
from .models import Contest, ContestSubmission

'''
class ContestForm(forms.ModelForm):

    class Meta:
        model = Contest
        exclude = ["author", 'start_time']
        widgets = {
           'group': ModelSelect2Widget(
                search_fields=[
                    'name__icontains',
                    'nickname__icontains',
                ]
            ),
        }
'''


class ContestForm(forms.Form):

    title = forms.CharField(max_length=64, min_length=1,
            label=u'测验标题', widget=forms.TextInput(attrs={
                'class':'input-block-level',
                'placeholder':'Contest Title'}))
    desc = forms.CharField(required=False, label=u'测验描述',
            widget=forms.Textarea(attrs={
                'class':'input-block-level',
                'placeholder':'Contest Description'}))
    start_date = forms.DateField(initial=date.today()+timedelta(days=1), label=u'开始日期',
            widget=forms.DateInput(format='%Y-%m-%d', attrs={
                'class':'input-small',
                'placeholder':'YYYY-MM-DD'}))
    start_time = forms.TimeField(initial=time(9, 0, 0),label=u'开始时间',
            widget=forms.TimeInput(format='%H:%M:%S',attrs={
                'class':'input-small',
                'placeholder':'hh:mm:ss'}))
    length = forms.IntegerField(min_value=1, initial=300, label=u'测验时长',
            widget=forms.TextInput(attrs={
                'class':'input-small',
                'placeholder':'Contest Duration'}), )
    board_stop = forms.IntegerField(min_value=1, initial=300, label=u'排行榜时长',
            widget=forms.TextInput(attrs={
                'class':'input-small',
                'placeholder':'Board Duration'}), )
    lang_limit = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_MASK.choice(),
                                           initial=[4, 1, 2], label=u'语言限制')

    started = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super(ContestForm, self).clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        length = cleaned_data.get('length')
        started = cleaned_data.get('started')

        if start_date and start_time and length:
            if started == 'True':
                if datetime.combine(start_date, start_time) + timedelta(minutes=length) < datetime.now():
                    raise forms.ValidationError("Error end time")
            elif datetime.combine(start_date, start_time) < datetime.now():
                raise forms.ValidationError("Error start time")

        return cleaned_data


class SubmissionForm(forms.Form):

    index = forms.ChoiceField(choices=(), widget=forms.Select())
    language = forms.ChoiceField(choices=LANGUAGE.choice(), widget=forms.Select())

