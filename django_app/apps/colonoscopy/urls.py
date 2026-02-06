from django.urls import path

from . import views

app_name = "colonoscopy"

urlpatterns = [
    path('', views.colonoscopy_list_view, name='colonoscopy-list'),
    path('<int:pk>/', views.colonoscopy_detail_view, name='colonoscopy-detail'),
    path('new/', views.colonoscopy_create_view, name='colonoscopy-create'),
]