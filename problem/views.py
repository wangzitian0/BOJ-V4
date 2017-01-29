
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q

import json
import mimetypes
from django_tables2 import RequestConfig
from filer.models.filemodels import File
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403

from .models import Problem, ProblemDataInfo
from .filters import ProblemFilter
from .tables import ProblemTable
from .serializers import ProblemSerializer, ProblemDataInfoSerializer
from .serializers import FileSerializer, ProblemDataSerializer
from .forms import ProblemForm


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated,)


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['get'], url_path='datas')
    def get_problem_datas(self, request, pk=None):
        qs = self.get_queryset()
        problem = get_object_or_404(qs, pk=pk)
        serializer = ProblemDataSerializer(problem, context={'request': request})
        return Response(serializer.data)


class ProblemDataInfoViewSet(viewsets.ModelViewSet):
    queryset = ProblemDataInfo.objects.all()
    serializer_class = ProblemDataInfoSerializer
    permission_classes = (IsAuthenticated,)


class ProblemListView(ListView):

    model = Problem
    paginate_by = 10

    def get_queryset(self):
        gp_can_view = get_objects_for_user(
            self.request.user,
            'ojuser.view_groupprofile',
            with_superuser=True
        )
        self.problem_can_view_qs = Problem.objects.filter(groups__in=gp_can_view).distinct()

        gp_can_change = get_objects_for_user(
            self.request.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        )
        self.problem_can_change_qs = Problem.objects.filter(groups__in=gp_can_change).distinct()

        groups_can_delete = get_objects_for_user(
            self.request.user,
            'problem.delete_problem',
            with_superuser=True
        )
        self.problem_can_delete_qs = Problem.objects.filter(pk__in=groups_can_delete).distinct()

        self.problem_can_change_qs |= self.problem_can_delete_qs
        self.problem_can_view_qs |= self.problem_can_change_qs
        self.filter = ProblemFilter(
            self.request.GET,
            queryset=self.problem_can_view_qs,
            user=self.request.user
        )
        return self.filter.qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProblemListView, self).get_context_data(**kwargs)
        problems_table = ProblemTable(self.get_queryset())
        RequestConfig(self.request).configure(problems_table)
        #  add filter here
        context['problems_table'] = problems_table
        context['filter'] = self.filter
        context['problem_can_view'] = self.problem_can_view_qs
        context['problem_can_delete'] = self.problem_can_delete_qs
        context['problem_can_change'] = self.problem_can_change_qs
        return context


class ProblemDetailView(DetailView):

    model = Problem
#    template_name = 'problem/problem_detail.html'

    def get_queryset(self):
        gp_can_view = get_objects_for_user(
            self.request.user,
            'ojuser.view_groupprofile',
            with_superuser=True
        )
        gp_can_change = get_objects_for_user(
            self.request.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        )
        groups_can_delete = get_objects_for_user(
            self.request.user,
            'problem.delete_problem',
            with_superuser=True
        )
        self.qs = Problem.objects.filter(
            Q(groups__in=gp_can_view) |
            Q(groups__in=gp_can_change) |
            Q(pk__in=groups_can_delete)
        ).distinct()
        return self.qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        print "===================dispatch=========="
        return super(ProblemDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        if self.request.user.has_perm('problem.change_problem', self.object): 
            print "----------------ACCESS!--------------------"
            context['has_change_perm'] = 1
        print context
        return context


class ProblemCreateView(CreateView):
    model = Problem
    form_class = ProblemForm
    template_name_suffix = '_create_form'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.superadmin = self.request.user
        self.object.save()
        return super(ProblemCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('problem:upload-new', args=[self.object.pk])


class ProblemUpdateView(UpdateView):
    model = Problem
    #  fields = '__all__'
    form_class = ProblemForm
    template_name_suffix = '_update_form'

    def get_queryset(self):
        gp_can_change = get_objects_for_user(
            self.request.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        )
        groups_can_delete = get_objects_for_user(
            self.request.user,
            'problem.delete_problem',
            with_superuser=True
        )
        self.qs = Problem.objects.filter(
            Q(groups__in=gp_can_change) |
            Q(pk__in=groups_can_delete)
        ).distinct()
        return self.qs

    def get_success_url(self):
        return reverse('problem:upload-new', args=[self.object.pk])


class ProblemDeleteView(DeleteView):
    model = Problem
    success_url = reverse_lazy('problem:problem-list')

    def get_queryset(self):
        groups_can_delete = get_objects_for_user(
            self.request.user,
            'problem.delete_problem',
            with_superuser=True
        )
        self.qs = Problem.objects.filter(
            Q(pk__in=groups_can_delete)
        ).distinct()
        return self.qs

    @method_decorator(permission_required_or_403('delete_problem', (Problem, 'pk', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemDeleteView, self).dispatch(request, *args, **kwargs)

#  =======================  problem datas  ===========================


def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.
    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField
    """
    obj = getattr(instance, file_attr)
    return {
        'url': obj.url,
        'name': obj.name,
        'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': obj.url,
        'size': obj.size,
        'deleteUrl': reverse('problem:upload-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
    }

MIMEANY = '*/*'
MIMEJSON = 'application/json'
MIMETEXT = 'text/plain'


def response_mimetype(request):
    can_json = MIMEJSON in request.META['HTTP_ACCEPT']
    can_json |= MIMEANY in request.META['HTTP_ACCEPT']
    return MIMEJSON if can_json else MIMETEXT


class JSONResponse(HttpResponse):
    def __init__(self, obj='', json_opts=None, mimetype=MIMEJSON, *args, **kwargs):
        json_opts = json_opts if isinstance(json_opts, dict) else {}
        content = json.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


class FileCreateView(CreateView):
    model = File
    fields = "__all__"
    template_name = 'problem/problemdata_form.html'

    def get_context_data(self, **kwargs):
        context = super(FileCreateView, self).get_context_data(**kwargs)
        context['pid'] = self.kwargs['pid']
        return context

    def form_valid(self, form):
        pid = self.kwargs['pid']
        _problem = Problem.objects.get(pk=pid)
        self.object = form.save()
        #  print _problem, self.object
        ProblemDataInfo.objects.create(data=self.object, problem=_problem)
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class FileDeleteView(DeleteView):
    model = File

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class FileListView(ListView):
    model = File

    def get_queryset(self):
        _problem = Problem.objects.get(pk=self.kwargs['pid'])
        qs = super(FileListView, self).get_queryset()
        return qs.filter(datainfo__problem=_problem)

    def render_to_response(self, context, **response_kwargs):
        files = [serialize(p) for p in self.get_queryset()]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
