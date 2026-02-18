from django.urls import path
from . import views
urlpatterns = [
    path('notes/', views.notes_view, name='notes_view'),
    path('notes/<int:pk>/', views.notes_detail_view, name='notes_detail_view')
]