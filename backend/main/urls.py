from django.urls import path
from rest_framework_simplejwt import views as jwt
from .views import ProductViewSet, OrderViewSet

product_views   = ProductViewSet.as_view({'get' :'list',
                                          'post': 'create'})
product_pkviews = ProductViewSet.as_view({'get'   :'retrieve',
                                          'post'  : 'partial_update',
                                          'delete': 'destroy'})
order_views   = OrderViewSet.as_view({'get' :'list',
                                      'post': 'create'})
order_pkviews = OrderViewSet.as_view({'get'   :'retrieve',
                                      'post'  : 'partial_update',
                                      'delete': 'destroy'})

urlpatterns = [
    path('product/', product_views),
    path('product/<str:pk>/', product_pkviews),
    path('order/', order_views),
    path('order/<str:pk>/', order_pkviews),
    path('api/token/', jwt.TokenObtainPairView.as_view()),
    path('api/token/refresh/', jwt.TokenRefreshView.as_view()),
]
