from account.views import SignupView, SettingsView
from .forms import UserProfileForm, UserSettingsForm, UserProfilesForm
from .forms import GroupProfileForm, GroupForm
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, GroupUsersSerializer
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import detail_route


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @detail_route(methods=['get', 'patch', 'post'], url_path='users')
    def get_problem_datas(self, request, pk=None):
        qs = self.get_queryset()
        group = get_object_or_404(qs, pk=pk)
        serializer = GroupUsersSerializer(group, context={'request': request})
        return Response(serializer.data)


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


class GroupListView(ListView):

    model = Group
    template_name = 'ojuser/group_list.html'

    def get_queryset(self):
        return self.request.user.groups.all()


class GroupDetailView(DetailView):

    model = Group
    template_name = 'ojuser/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        ob = context['object']
        context['admins'] = ob.profile.admins.all()
        context['parents'] = ob.profile.parents()
        context['children'] = ob.profile.children.all()
        return context


class GroupCreateView(TemplateView):
    template_name = 'ojuser/group_create_form.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        group_form = context["group_form"]
        group_profile_form = context["group_profile_form"]
        if group_form.is_valid() and group_profile_form.is_valid():
            group = group_form.save()
            group_profile_form = GroupProfileForm(request.POST, instance=group.profile)
            group_profile_form.superadmin = self.request.user
            group_profile_form.save()
            return HttpResponseRedirect(reverse('mygroup-detail', args=[group.pk, ]))
        return super(GroupCreateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)

        group_form = GroupForm(self.request.POST or None)
        group_profile_form = GroupProfileForm(self.request.POST or None)
        context["group_form"] = group_form
        context["group_profile_form"] = group_profile_form

        return context


class GroupMemberView(TemplateView):
    template_name = 'ojuser/group_member.html'
