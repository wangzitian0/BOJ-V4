from account.views import SignupView, SettingsView
from django.views.generic.edit import FormView
from .forms import UserProfileForm, UserSettingsForm, UserProfilesForm
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        profile.nickname = form.cleaned_data["nickname"]
        profile.save()
        super(OjUserSettingsView, self).update_account(form)

    def get_initial(self):
        initial = super(OjUserSettingsView, self).get_initial()
        profile = self.request.user.profile
        initial["nickname"] = profile.nickname
        return initial


class OjUserProfilesView(FormView):
    template_name = 'account/profiles.html'
    form_class = UserProfilesForm
    #  success_url = reverse_lazy('account')
    success_url = '.'
    messages = {
        "profiles_updated": {
            "level": messages.SUCCESS,
            "text": _("Account profiles updated.")
        },
    }

    def get_initial(self):
        initial = super(OjUserProfilesView, self).get_initial()
        profile = self.request.user.profile
        initial["gender"] = profile.gender
        initial["prefer_lang"] = profile.prefer_lang
        return initial

    def form_valid(self, form):
        profile = self.request.user.profile
        profile.gender = form.cleaned_data["gender"]
        profile.prefer_lang = form.cleaned_data["prefer_lang"]
        profile.save()
        if self.messages.get("profiles_updated"):
            messages.add_message(
                self.request,
                self.messages["profiles_updated"]["level"],
                self.messages["profiles_updated"]["text"]
            )
        return redirect(self.get_success_url())
