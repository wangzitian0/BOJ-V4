from django.shortcuts import render
from account.views import SignupView, SettingsView

from  .forms import UserProfileForm, UserSettingsForm

# Create your views here.
class OjUserSignupView(SignupView):

    form_class = UserProfileForm
    def after_signup(self, form):
        self.create_profile(form)
        super(OjUserSignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.profile
        profile.nickname = form.cleaned_data["nickname"]
        profile.gender = form.cleaned_data["gender"]
        profile.prefer_lang = form.cleaned_data["prefer_lang"]
        profile.save()

class OjUserSettingsView(SettingsView):
    form_class = UserSettingsForm

    def update_account(self, form):
        profile = self.request.user.profile
        profile.update(
            nickname = form.cleaned_data["nickname"],
            gender = form.cleaned_data["gender"],
            prefer_lang = form.cleaned_data["prefer_lang"],
        )
        profile.save()
        super(OjUserSettingsView, self).update_account(form)


    def get_initial(self):
        initial = super(OjUserSettingsView, self).get_initial()
        profile = self.request.user.profile
        initial["nickname"] = profile.nickname
        initial["gender"] = profile.gender
        initial["prefer_lang"] = profile.prefer_lang
        return initial

