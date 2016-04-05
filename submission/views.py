from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Submission
from .serializers import SubmissionSerializer

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
#  from guardian.shortcuts import get_objects_for_user


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated,)


class SubmissionListView(ListView):

    model = Submission
    paginate_by = 10

    #  def get_queryset(self):
    #  return get_objects_for_user(self.request.user, 'problem.view_problem')


class SubmissionDetailView(DetailView):

    model = Submission

    def get_context_data(self, **kwargs):
        context = super(SubmissionDetailView, self).get_context_data(**kwargs)
        return context


class SubmissionCreateView(CreateView):
    model = Submission
    fields = '__all__'
    template_name_suffix = '_create_form'
