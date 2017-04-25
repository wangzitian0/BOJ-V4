from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^$", views.ContestListView.as_view(), name="contest-list"),
    url(r'^add/(?P<gid>[0-9]+)/$', views.ContestCreateView.as_view(), name='add-contest'),
    url(r'^(?P<pk>[0-9]+)/$', views.ContestDetailView.as_view(), name='contest-detail'),
    url(r'^(?P<pk>[0-9]+)/problem/(?P<index>[A-Z]+)$', views.ProblemDetailView.as_view(), name='problem-detail'),
    url(r'^(?P<pk>[0-9]+)/submission/$', views.SubmissionListView.as_view(), name='submission-list'),
    url(r'^(?P<pk>[0-9]+)/clarification/$', views.ClarificationListView.as_view(), name='clarification-list'),
    url(r'^(?P<pk>[0-9]+)/board/$', views.BoardView.as_view(), name='board'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.ContestUpdateView.as_view(), name='contest-update'),
    url(r'^(?P<pk>[0-9]+)/submit/$', views.SubmissionCreateView.as_view(),
        name='submission-add'),
    url(r'^(?P<cpk>[0-9]+)/submission/(?P<pk>[0-9]+)$', views.SubmissionDetailView.as_view(), name='submission-detail'),
    #url(r'^(?P<pid>[0-9]+)/view/$', views.FileListView.as_view(), name='file-list'),
    #url(r'^delete/(?P<pk>\d+)$', views.FileDeleteView.as_view(), name='upload-delete'),
]



