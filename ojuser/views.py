from account.views import SignupView, SettingsView
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django_tables2 import RequestConfig

from .forms import UserProfileForm, UserSettingsForm, UserProfilesForm
from .forms import GroupProfileForm, GroupForm, GroupSearchForm
from .serializers import UserSerializer, UserProfileSerializer
from .serializers import GroupProfileSerializer, UserSlugSerializer, GroupSerializer
from .tables import GroupUserTable, GroupTable
from .models import GroupProfile
from .filters import GroupFilter

from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403


class GroupListView(ListView):

    model = GroupProfile
    template_name = 'ojuser/group_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(GroupListView, self).get_queryset()
        self.filter = GroupFilter(self.request.GET, queryset=qs, user=self.request.user)
        profiles_can_change = get_objects_for_user(
            self.request.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        )
        self.group_can_change_qs = profiles_can_change
        profiles_can_delete = get_objects_for_user(
            self.request.user,
            'ojuser.delete_groupprofile',
            with_superuser=True
        )
        self.group_can_delete_qs = profiles_can_delete
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        groups_table = GroupTable(self.get_queryset())
        RequestConfig(self.request).configure(groups_table)
        #  add filter here
        group_search_form = GroupSearchForm()
        context["group_search_form"] = group_search_form
        context['groups_table'] = groups_table
        context['filter'] = self.filter
        context['group_can_change'] = self.group_can_change_qs
        context['group_can_delete'] = self.group_can_delete_qs
        return context


class GroupCreateView(TemplateView):
    template_name = 'ojuser/group_create_form.html'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.group_profile_form.is_valid() and self.group_admins_form.is_valid():
            gg = GroupProfile(**self.group_profile_form.cleaned_data)
            gg.superadmin = self.request.user
            gg.save()
            GroupForm(request.POST, instance=gg.admin_group).save()
            return HttpResponseRedirect(reverse('mygroup-detail', args=[gg.pk, ]))
        return super(GroupCreateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        self.group_profile_form = GroupProfileForm(self.request.POST or None)
        self.group_admins_form = GroupForm(self.request.POST or None)
        context["group_profile_form"] = self.group_profile_form
        context["group_admins_form"] = self.group_admins_form
        return context


class GroupUpdateView(TemplateView):
    template_name = 'ojuser/group_update_form.html'

    @method_decorator(permission_required_or_403(
        'change_groupprofile',
        (GroupProfile, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(GroupUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.group_profile_form = GroupProfileForm(self.request.POST, instance=self.object)
        self.group_admins_form = GroupForm(self.request.POST, instance=self.object.admin_group)
        if self.group_profile_form.is_valid() and self.group_admins_form.is_valid():
            self.group_profile_form.save()
            self.group_admins_form.save()
            return HttpResponseRedirect(reverse('mygroup-detail', args=[context['pk'], ]))
        return super(GroupUpdateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        self.pk = self.kwargs['pk']
        qs = GroupProfile.objects.all()
        self.object = get_object_or_404(qs, pk=self.pk)
        self.group_profile_form = GroupProfileForm(instance=self.object)
        self.group_admins_form = GroupForm(instance=self.object.admin_group,)
        context["group_profile_form"] = self.group_profile_form
        context["group_admins_form"] = self.group_admins_form
        context['pk'] = self.pk
        return context


class GroupDeleteView(DeleteView):
    model = GroupProfile
    template_name = 'ojuser/group_confirm_delete.html'
    success_url = reverse_lazy('mygroup-list')

    @method_decorator(permission_required_or_403(
        'delete_groupprofile',
        (GroupProfile, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(GroupDeleteView, self).dispatch(request, *args, **kwargs)


class GroupDetailView(DetailView):

    model = GroupProfile
    template_name = 'ojuser/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        group = context['object']
        context['admins'] = group.admin_group.user_set.all()
        context['children'] = group.get_children()

        group_users = group.user_group.user_set.all()
        group_users_table = GroupUserTable(group_users)
        RequestConfig(self.request).configure(group_users_table)
        #  add filter here
        context['group_users_table'] = group_users_table
        return context


class GroupMemberView(TemplateView):
    template_name = 'ojuser/group_members.html'

    @method_decorator(permission_required_or_403(
        'change_groupprofile',
        (GroupProfile, 'pk', 'pk')
    ))
    def dispatch(self, request, *args, **kwargs):
        return super(GroupMemberView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, pk=None, **kwargs):
        context = super(GroupMemberView, self).get_context_data(**kwargs)
        context['pk'] = pk
        return context


class UserAddView(TemplateView):
    template_name = 'ojuser/user_add.html'

    def get_context_data(self, **kwargs):
        context = super(UserAddView, self).get_context_data(**kwargs)
        return context


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    @list_route(methods=['post'], url_path='bulk_create')
    def create_users(self, request):
        serializer = UserProfileSerializer(
            data=request.data, many=True, context={'request': request}
        )
        #  print request.data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupProfileViewSet(viewsets.ModelViewSet):
    queryset = GroupProfile.objects.all()
    serializer_class = GroupProfileSerializer
    permission_classes = [IsAuthenticated, ]

    @detail_route(methods=['post', 'get', 'put', ], url_path='members')
    def manage_member(self, request, pk=None):
        qs = self.get_queryset()
        group = get_object_or_404(qs, pk=pk)
        print group.user_group.user_set
        if request.method == "POST" or request.method == "PUT":
            users = []
            errors = []
            valid = 1
            for x in request.data:
                try:
                    user = User.objects.get(username=x['username'])
                    users.append(user)
                    errors.append({})
                except User.DoesNotExist:
                    errors.append({"username": "user do not exsit"})
                    valid = 0
            if not valid:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            group.user_group.user_set.clear()
            group.user_group.user_set.add(*users)
        serializer = UserSlugSerializer(group.user_group.user_set, many=True)
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
