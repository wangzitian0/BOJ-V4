# -*- coding: utf-8 -*-

from datetime import datetime, date, time, timedelta
from django import forms
from kari.const import Const
from django.forms.extras.widgets import SelectDateWidget
from Contest.widgets import SelectTimeWidget


class contestForm(forms.Form):
    LANG_CHOICE = (
        ('gcc', u'允许提交C代码'), 
        ('g++', u'允许提交C++代码'), 
        ('java', u'允许提交JAVA代码'), 
    )
    CONTEST_CHOICE = (
        ('0', u'公开'),
        ('1', u'私有'),
    )
    BOARD_CHOICE = (
        ('0', u'ACM式'), 
        ('1', u'分组计分式'), 
        ('2', u'仅提交，不判题式')
    )
    STAT_CHOICE = (
        ('0', u'全部信息可见'),
        ('1', u'仅自己的信息可见'),
    )
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
    contest_type = forms.ChoiceField(choices=STAT_CHOICE, label=u'统计信息查看限制')
    board_type = forms.ChoiceField(choices=BOARD_CHOICE, label=u'计分形式')
    lang_limit = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANG_CHOICE,
                                           initial=['gcc', 'g++', 'java'], label=u'语言限制')

    started = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    def clean(self):
        cleaned_data = super(contestForm, self).clean()        
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        length = cleaned_data.get('length')
        started = cleaned_data.get('started')
                
        if start_date and start_time and length:
            if started == 'True':
                if datetime.combine(start_date, start_time) + timedelta(minutes=length) < datetime.now():
                    raise forms.ValidationError(Const.CONTEST_END_TIME_ERR)
            elif datetime.combine(start_date, start_time) < datetime.now():
                raise forms.ValidationError(Const.CONTEST_TIME_ERR)
        
        return cleaned_data
    
class contestNoticeForm(forms.Form):
    title = forms.CharField(max_length=128, min_length=1, label=u'公告标题')
    content = forms.CharField(widget=forms.Textarea, required=False, label=u'公告内容')

class ClarificationForm(forms.Form):
    question = forms.CharField(max_length = 2048)

class AnswerClarificationForm(forms.Form):
    answer = forms.CharField(max_length = 2048)
