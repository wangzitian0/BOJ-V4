from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r"^mygroups/$", views.GroupListView.as_view(), name="mygroup-list"),
    url(r"^mygroups/add$", views.GroupCreateView.as_view(), name="mygroup-create"),
    url(r'^mygroups/(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(), name='mygroup-detail'),
    url(r'^mygroups/(?P<pk>[0-9]+)/update/$', views.GroupUpdateView.as_view(),
        name='mygroup-update'),
    url(r'^mygroups/(?P<pk>[0-9]+)/delete/$', views.GroupDeleteView.as_view(),
        name='mygroup-delete'),
    url(r'^mygroups/(?P<pk>[0-9]+)/members/$', views.GroupMemberView.as_view(),
        name='mygroup-add-member'),
    url(r'^myusers/add/$', views.UserAddView.as_view(), name='user-add'),
    url(r"^signup/$", views.OjUserSignupView.as_view(), name="account_signup"),
    url(r"^profiles/$", views.OjUserProfilesView.as_view(), name="account_profiles"),
    url(r"^", include("account.urls")),
]
