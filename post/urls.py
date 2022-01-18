from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('<int:pk>/details/',views.PostDetailView.as_view(), name="post-detail"),
    path('new/',views.PostAddView.as_view(),name='add-post'),
    path('<int:pk>/update/',views.PostUpdateView.as_view(),name='update-post'),
    path('<int:pk>/delete/',views.PostDeleteView.as_view(),name='delete-post'),
    path('<int:pk>/get-products/',views.GetProductsView.as_view(), name='get-products'),
]
