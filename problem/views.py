import json
import mimetypes
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required_or_403

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
#  from django.contrib.auth.decorators import login_required

from filer.models.filemodels import File
from .models import Problem, ProblemDataInfo, Language

from .serializers import ProblemSerializer, ProblemDataInfoSerializer
from .serializers import LanguageSerializer, FileSerializer, ProblemDataSerializer

from .forms import ProblemForm
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import detail_route


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


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (IsAuthenticated,)


class ProblemListView(ListView):

    model = Problem
    paginate_by = 10

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'problem.view_problem')


class ProblemDetailView(DetailView):

    model = Problem

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'problem.view_problem')

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        return context


class ProblemCreateView(CreateView):
    model = Problem
    #  fields = '__all__'
    form_class = ProblemForm
    template_name_suffix = '_create_form'

    #  @staff_member_required
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(ProblemCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('problem:upload-new', args=[self.object.pk])


class ProblemUpdateView(UpdateView):
    model = Problem
    #  fields = '__all__'
    form_class = ProblemForm
    template_name_suffix = '_update_form'

    @method_decorator(permission_required_or_403('change_problem', (Problem, 'pk', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('problem:upload-new', args=[self.object.pk])


class ProblemDeleteView(DeleteView):
    model = Problem
    success_url = reverse_lazy('problem:problem-list')

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
