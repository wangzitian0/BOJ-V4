from django.shortcuts import render

# Create your views here.
import account.views
import myuser.forms
from .models import UserProfile

class SignupView(account.views.SignupView):
    form_class = myuser.forms.SignupForm

    def update_profile(self, form):
        UserProfile.objects.create(
            user=self.created_user,
            birthdate = form.cleaned_data["birthdate"],
        )
    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)



class SettingsView(account.views.SettingsView):
    form_class = myuser.forms.SettingsForm
    
    def update_profile(self, form):
        UserProfile.objects.update(
            birthdate = form.cleaned_data["birthdate"]
        )
    def update_account(self, form):
        self.update_profile(form)
        super(SettingsView, self).update_account(form)