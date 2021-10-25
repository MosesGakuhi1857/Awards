from django.urls.conf import include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path, include
from .views import UpdateProjectView
from . import api
urlpatterns=[
   
    path('register/', views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('project-details/<int:id>', views.projectDetails, name='project-details'),
    path('publish-project/', views.publishProject, name='publish-project'),
    path('search/', views.search_project, name='search_project'),
    path('update/<int:pk>', UpdateProjectView.as_view(), name='update-project'),
    path('api/profile/', views.ProfileList.as_view()),
    path('api/project/', views.ProjectList.as_view()),

   
    # path('login/', views.login_user, name='login'),




]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)