# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime, timedelta, date, time
from bojv4.conf import LANGUAGE_MASK, LANGUAGE
from submission.models import Submission
from .models import Contest, ContestSubmission, Notification, Clarification, ContestProblem
from ojuser.models import GroupProfile
from django_select2.forms import ModelSelect2Widget


class ContestForm(forms.ModelForm):

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

    lang_limited = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_MASK.choice(),
                                           initial=[4, 1, 2], label=u'语言限制')

    started = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Contest
        fields = ['title', 'desc', 'start_time', 'start_date', 'contest_type' ,'length', 'board_stop', 'lang_limited']
        
    def clean(self):
        cleaned_data = super(ContestForm, self).clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        length = cleaned_data.get('length')

        if start_date and start_time and length:
            if datetime.combine(start_date, start_time) + timedelta(minutes=length) < datetime.now():
                raise forms.ValidationError("Error end time")
            elif datetime.combine(start_date, start_time) < datetime.now():
                raise forms.ValidationError("Error start time")
            cleaned_data['start_time'] = datetime.combine(start_date, start_time)

        return cleaned_data


class SubmissionForm(forms.ModelForm):

    problem = forms.ModelChoiceField(queryset=ContestProblem.objects.all(), widget=forms.Select(), label='problem')
    language = forms.ChoiceField(choices=LANGUAGE.choice(), widget=forms.Select(), label='language')
    code = forms.CharField(label='code', widget=forms.Textarea, max_length=65536)

    class Meta:
        model = ContestSubmission
        fields = ['problem', 'language', 'code']

    def set_choice(self, contest):
        lang_limit = []
        for x in LANGUAGE_MASK.choice():
            if contest.lang_limit & x[0]:
                lang_limit.append((x[1], LANGUAGE.get_display_name(x[1])))
        self.fields['language'].choices = lang_limit
        self.fields['problem'].queryset = contest.problems.all()


class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification
        fields = ['title', 'content']


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Clarification
        fields = ['question']


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Clarification
        fields = ['answer']

