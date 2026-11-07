from django.urls import path
from .views import (
    CoffeeListCreateView,
    CoffeeDetailView,
    OriginListCreateView,
    OriginDetailView
)

urlpatterns = [
    path('coffees/', CoffeeListCreateView.as_view(), name='coffee-list-create'),
    path('coffees/<int:pk>/', CoffeeDetailView.as_view(), name='coffee-detail'),

    path('origins/', OriginListCreateView.as_view(), name='origin-list-create'),
    path('origins/<int:pk>/', OriginDetailView.as_view(), name='origin-detail'),
]
