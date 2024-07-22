from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cardlist/', views.CardListView.as_view(), name='card-list'),
    path('card/<int:pk>', views.CardDetailView.as_view(), name='card-detail'),
    path('card/<int:pk>/activate/', views.CardDetailView.as_view(), name='card-activate'),
    path('card/<int:pk>/deactivate/', views.CardDetailView.as_view(), name='card-deactivate'),
    path('card/<int:pk>/delete/', views.CardDelete.as_view(), name='card-delete'),
    path('generator/', views.CardGeneratorView.as_view(), name='generator'),
    path('generator/success/', views.success, name='success'),
]

