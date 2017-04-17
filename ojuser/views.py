import json
import copy
from itertools import chain
from account.views import SignupView
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_tables2 import RequestConfig

from .forms import UserProfileForm, UserProfilesForm
from .forms import GroupProfileForm, GroupForm, GroupSearchForm
from .serializers import UserSerializer, UserProfileSerializer, \
        get_rand_password, GroupProfileSerializer, UserSlugSerializer, GroupSerializer, \
        UserResetSerializer
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
        profiles_can_view = get_objects_for_user(
            self.request.user,
            'ojuser.view_groupprofile',
            with_superuser=True
        )
        self.group_can_view_qs = profiles_can_view
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
        # self.filter = GroupFilter(self.request.GET, queryset=qs, user=self.request.user)
        self.filter = GroupFilter(self.request.GET, queryset=profiles_can_view, user=self.request.user)
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
        context['group_can_view'] = self.group_can_view_qs
        context['group_can_change'] = self.group_can_change_qs
        context['group_can_delete'] = self.group_can_delete_qs
        tree_list = []
        for u in self.get_queryset():
            p_name = '#'
            if u.parent:
                p_name = str(u.parent.pk)
            url = reverse('mygroup-detail', args=[u.pk, ])
            tree_list.append({
                'id': str(u.pk),
                'parent': p_name,
                'text': u.nickname,
                'state': {
                    'opened': True,
                },
            })
        context['tree_list'] = json.dumps(tree_list)
        print context['tree_list']

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
            # gg.superadmin = self.request.user
            gg.save()
            GroupForm(request.POST, instance=gg.admin_group).save()
            return HttpResponseRedirect(reverse('mygroup-detail', args=[gg.pk, ]))
        return super(GroupCreateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        self.group_profile_form = GroupProfileForm(self.request.POST or None)
        self.group_admins_form = GroupForm(self.request.POST or None)
        group = GroupProfile.objects.filter(name='root').first()
        groups = get_objects_for_user(
            user=self.request.user,
            perms='ojuser.delete_groupprofile',
            with_superuser=True)
        queryset = User.objects.filter(pk=self.request.user.pk)
        superadmin_queryset = copy.copy(queryset)
        if group:
            superadmin_queryset |= group.user_group.user_set.all()
        self.group_profile_form.fields['superadmin'].queryset = superadmin_queryset

        for g in groups.all():
            queryset |= g.user_group.user_set.all()

        self.group_admins_form.fields["admins"].widget.queryset = queryset

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
        my_children = self.object.get_descendants(include_self=True)
        profiles_can_change = get_objects_for_user(
            self.request.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        ).exclude(pk__in=my_children)
        self.group_profile_form = GroupProfileForm(instance=self.object)
        self.group_profile_form.fields['parent'].queryset = profiles_can_change
        self.group_profile_form.fields['parent'].widget.queryset = profiles_can_change
        user_queryset = User.objects.filter(pk__in=self.object.user_group.user_set.all())
        self.group_admins_form = GroupForm(instance=self.object.admin_group)
        self.group_admins_form.fields['admins'].widget.queryset = user_queryset
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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GroupDetailView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(GroupDetailView, self).get_queryset()
        profiles_can_view = get_objects_for_user(
            self.request.user,
            'ojuser.view_groupprofile',
            with_superuser=True
        )
        self.group_can_view_qs = profiles_can_view
        profiles_can_change = get_objects_for_user(
            self.request.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        )
        self.group_can_change_qs = profiles_can_change
        # self.filter = GroupFilter(self.request.GET, queryset=qs, user=self.request.user)
        self.filter = GroupFilter(self.request.GET, queryset=profiles_can_view, user=self.request.user)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['group_pk'] = context['object'].pk
        group = context['object']
        print group.get_ancestors()
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


class GroupResetView(DetailView):
    template_name = 'ojuser/reset_members.html'
    model = GroupProfile

    def get_context_data(self, **kwargs):
        context = super(GroupResetView, self).get_context_data(**kwargs)
        group = context['object']
        group_users = group.user_group.user_set.all()
        context['users'] = group_users
        return context

class UserAddView(TemplateView):
    template_name = 'ojuser/user_add.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserAddView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        profiles_can_change = get_objects_for_user(
            self.request.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        )
        context = super(UserAddView, self).get_context_data(**kwargs)
        context['group_can_change'] = profiles_can_change.all()
        if self.request.GET.has_key('group_pk'):
            context['select_group'] = int(self.request.GET['group_pk'])
            # print "================select_group"
            # print context['select_group']
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
        mp = {}
        for m in request.data['users']:
            if not m.has_key('password'):
                m['password'] = get_rand_password()
            mp[m['username']] = m['password']
        serializer = UserProfileSerializer(
            data=request.data['users'], many=True, context={'request': request}
        )
        if serializer.is_valid():
            users = serializer.save()
            for r in serializer.data:
                r['password'] = mp[r['username']]
            if request.data.has_key('group_pk'):
                try:
                    group = GroupProfile.objects.get(pk=int(request.data['group_pk']))
                    group.user_group.user_set.add(*users)
                    group.save()
                except Exception, ex:
                    print ex
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

    @detail_route(methods=['post', 'get', 'put', ], url_path='reset')
    def reset_member(self, request, pk=None):
        qs = self.get_queryset()
        group = get_object_or_404(qs, pk=pk)
        if request.method == "POST":
            users = []
            errors = []
            valid = 1
            for x in request.data:
                try:
                    user = User.objects.get(pk=int(x))
                    users.append(user)
                    errors.append({})
                except User.DoesNotExist:
                    errors.append({"pk": "user do not exsit"})
                    valid = 0
            if not valid:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            resp = []
            for u in users:
                pwd = get_rand_password()
                u.set_password(pwd)
                u.save()
                resp.append({
                    'pk': u.pk,
                    'password': pwd,
                    })
            serializer = UserResetSerializer(resp, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OjUserSignupView(SignupView):

    form_class = UserProfileForm

    def after_signup(self, form):
        self.create_profile(form)
        super(OjUserSignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.profile
        profile.nickname = form.cleaned_data["nickname"]
        profile.gender = form.cleaned_data["gender"]
        profile.save()
        group = GroupProfile.objects.filter(name='public').first()
        if group:
            group.user_group.user_set.add(self.created_user)


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
        initial["nickname"] = profile.nickname
        initial["gender"] = profile.gender
        return initial

    def form_valid(self, form):
        profile = self.request.user.profile
        profile.gender = form.cleaned_data["gender"]
        profile.nickname = form.cleaned_data["nickname"]
        profile.save()
        if self.messages.get("profiles_updated"):
            messages.add_message(
                self.request,
                self.messages["profiles_updated"]["level"],
                self.messages["profiles_updated"]["text"]
            )
        return redirect(self.get_success_url())


