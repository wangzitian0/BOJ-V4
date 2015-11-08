from django.shortcuts import render

# Create your views here.
import account.views
import myuser.forms
from .models import BojUser

class BojSettingsView(account.views.SettingsView):
    form_class = myuser.forms.BojSettingsForm
    
    def update_profile(self, form):
        BojUser.objects.update(
            nickname = form.cleaned_data["nickname"],
            gender = form.cleaned_data["gender"],
            default_lang = form.cleaned_data["default_lang"],
        )
    def update_account(self, form):
        self.update_profile(form)
        super(BojSettingsView, self).update_account(form)

    def get_initial(self):
        initial = super(BojSettingsView, self).get_initial()
        if self.primary_email_address:
            initial["email"] = self.primary_email_address.email 
        initial["nickname"] = BojUser.objects.get(user=self.request.user).nickname 
        initial["gender"] = BojUser.objects.get(user=self.request.user).gender 
        initial["default_lang"] = BojUser.objects.get(user=self.request.user).default_lang 
        return initial


class BojUserView(account.views.SignupView):
    form_class = myuser.forms.BojUserForm

    def update_profile(self, form):
        BojUser.objects.create(
            user=self.created_user,
            nickname = form.cleaned_data["nickname"],
            gender = form.cleaned_data["gender"],
            default_lang = form.cleaned_data["default_lang"],
        )
    def after_signup(self, form):
        self.update_profile(form)
        super(BojUserView, self).after_signup(form)
