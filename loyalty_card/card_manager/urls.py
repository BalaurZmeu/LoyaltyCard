from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cardlist/', views.CardListView.as_view(), name='card-list'),
    path('card/<int:pk>', views.CardDetailView.as_view(), name='card-detail'),
    path('generator/', views.generator, name='generator'),
]
