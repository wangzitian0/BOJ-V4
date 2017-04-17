from .models import Contest
from .filters import ContestFilter
from .tables import ContestTable
from .form import ContestForm

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig

from guardian.shortcuts import get_objects_for_user
# Create your views here.


class ContestListView(ListView):

    model = Contest
    paginate_by = 10

    def get_queryset(self):
        group_can_view_qs = get_objects_for_user(
            self.request.user,
            'ojuser.view_groupprofile',
            with_superuser=True
        ).distinct()
        self.contest_can_view_qs = self.request.user.contests.all()
        for g in group_can_view_qs.all():
            self.contest_can_view_qs |= g.contests.all()
        self.filter = ContestFilter(
            self.request.GET,
            queryset=self.contest_can_view_qs,
            user=self.request.user
        )
        return self.filter.qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        print self.template_name
        return super(ContestListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestListView, self).get_context_data(**kwargs)
        print "template_name: ", self.get_template_names()
        contests_table = ContestTable(self.get_queryset())
        RequestConfig(self.request).configure(contests_table)
        #  add filter here
        context['contests_table'] = contests_table
        context['filter'] = self.filter
        context['contests_can_view'] = self.contest_can_view_qs

        # context['contests_can_delete'] = self.contest_can_delete_qs
        # context['contests_can_change'] = self.contest_can_change_qs
        return context


class ContestCreateView(CreateView):
    model = Contest
    form_class = ContestForm
    template_name_suffix = '_create_form'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ContestCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(ContestCreateView, self).post(request, *args, **kwargs)


    def form_valid(self, form):
        print '=========form valid==============='
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(ContestCreateView, self).form_valid(form)

    def get_form(self):
        groups = get_objects_for_user(
                self.request.user,
                'ojuser.change_groupprofile',
                with_superuser=True
            )
        form = ContestForm(**self.get_form_kwargs())
        form.fields['groups'].widget.queryset = groups
        return form

    def get_success_url(self):
        return reverse('problem:upload-new', args=[self.object.pk])
