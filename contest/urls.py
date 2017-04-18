from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^$", views.ContestListView.as_view(), name="contest-list"),
    url(r'^add/(?P<gid>[0-9]+)/$', views.ContestCreateView.as_view(), name='add-contest'),
    url(r'^(?P<pk>[0-9]+)/$', views.ContestDetailView.as_view(), name='contest-detail'),
    #url(r'^(?P<pk>[0-9]+)/data/$', views.ProblemDataView.as_view(), name='problem-data'),
    #url(r'^(?P<pk>[0-9]+)/update/$', views.ProblemUpdateView.as_view(), name='problem-update'),
    #url(r'^(?P<pk>[0-9]+)/delete/$', views.ProblemDeleteView.as_view(), name='problem-delete'),
    #url(r'^(?P<pid>[0-9]+)/files/$', views.FileCreateView.as_view(), name='upload-new'),
    #url(r'^(?P<pid>[0-9]+)/view/$', views.FileListView.as_view(), name='file-list'),
    #url(r'^delete/(?P<pk>\d+)$', views.FileDeleteView.as_view(), name='upload-delete'),
]



