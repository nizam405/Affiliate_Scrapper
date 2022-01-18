from django.urls import path, include
from . import views

app_name = 'project'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('<int:project_id>/detail/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('create/', views.ProjectCreateView.as_view(), name='create-project'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name="update-project"),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name="delete-project"),
    # path('<int:project_id>/posts/', include('post.urls', namespace='post')),
]