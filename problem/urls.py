from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^$", views.ProblemListView.as_view(), name="problem-list"),
    url(r'^add/$', views.ProblemCreateView.as_view(), name='problem-add'),
    url(r'^(?P<pk>[0-9]+)/$', views.ProblemDetailView.as_view(), name='problem-detail'),
    url(r'^(?P<pk>[0-9]+)/data/$', views.ProblemDataView.as_view(), name='problem-data'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.ProblemUpdateView.as_view(), name='problem-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.ProblemDeleteView.as_view(), name='problem-delete'),
    url(r'^(?P<pid>[0-9]+)/files/$', views.FileCreateView.as_view(), name='upload-new'),
    url(r'^(?P<pid>[0-9]+)/view/$', views.FileListView.as_view(), name='file-list'),
    url(r'^delete/(?P<pk>\d+)$', views.FileDeleteView.as_view(), name='upload-delete'),
]

