from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from .views import (
	CourseListView,
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView
)
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
	path('', views.home, name='home'),
	path('register/', views.register, name='register'),
	path('login/', auth_views.LoginView.as_view(template_name='webgen/login.html'), name = 'login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='webgen/logout.html'), name = 'logout'),
	path('profile/', views.profile, name='profile'),
	# Courses -->
	path('teaching/', CourseListView.as_view(), name='teaching'),
    path('teaching/course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('teaching/course/new/', CourseCreateView.as_view(), name='course-create'),
    path('teaching/course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('teaching/course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('about/', views.about, name='about'),
   	path('upload/', views.upload, name='upload'),
   	path('search/<int:pk>/', views.prof_page, name='prof_page'),
]


if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)