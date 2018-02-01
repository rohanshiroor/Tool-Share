"""ToolShare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from toolsharesite import views
import notifications.urls
from django.conf import settings

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^registration/$', views.registration, name='registration'),
        url(r'^$', views.Index, name='index'),
        url(r'^RegisterUser/', views.RegisterUser,name='RegisterUser'),
        url(r'^Login/',views.Login,name='Login'),
        url(r'^Logout/',views.Logout,name='Logout'),
        url(r'^Dashboard/',views.Dashboard,name='Dashboard'),
        url(r'^UpdateProfile/$',views.UpdateProfile,name='UpdateProfile'),
        url(r'^Shed/',views.Shed,name='Shed'),
        url(r'^CreateShed/',views.CreateShed,name='CreateShed'),
        url(r'^CreateCommunityShed/(?P<id>\d+)',views.CreateCommunityShed,name='CreateCommunityShed'),
        url(r'^ToolRegistration/', views.ToolRegistration,name='ToolRegistration'),
        url(r'^ToolManagement/', views.ToolManagement,name='ToolManagement'),
        url(r'^DeactivateTool/(?P<id>\d+)', views.DeactivateTool, name='DeactivateTool'),
        url(r'^DeleteTool/(?P<id>\d+)', views.DeleteTool, name='DeleteTool'),
        url(r'^RequestTool/(?P<id>\d+)', views.RequestTool, name='RequestTool'),
        url(r'^ManageRequest/', views.ManageRequest, name='ManageRequest'),
        url(r'^AcceptRequest/(?P<id>\d+)', views.AcceptRequest, name='AcceptRequest'),
        url(r'^RejectRequest/(?P<id>\d+)', views.RejectRequest, name='RejectRequest'),
        url(r'^ViewToolDetails/(?P<id>\d+)', views.ViewToolDetails, name='ViewToolDetails'),
        url(r'^ReturnTool/(?P<id>\d+)',views.ReturnTool, name='ReturnTool'),
        url(r'^ToolReturnAccept/(?P<id>\d+)', views.ToolReturnAccept, name='ToolReturnAccept'),
        url(r'^ViewComment/(?P<id>\d+)', views.ViewComment, name='ViewComment'),
        url(r'^CreateShedHome/',views.CreateShedHome,name='CreateShedHome'),
        url(r'^CreateCommunityShedHome/',views.CreateCommunityShedHome,name='CreateCommunityShedHome'),
        url(r'^EditTools/(?P<id>\d+)',views.EditTools,name='EditTools'),
        url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
        url(r'^getNotifications/',views.getNotifications ,name='getNotifications'),
        url(r'^Success/', views.RegistrationSuccess, name='registrationSuccess'),
        url(r'^CommunityStatistics/',views.CommunityStatistics,name='CommunityStatistics'),
           ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)