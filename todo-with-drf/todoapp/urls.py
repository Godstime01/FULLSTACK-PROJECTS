from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, RegisterView

router = DefaultRouter()
router.register(r"todos", TodoViewSet, basename = "todos")

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("sign-up/", RegisterView.as_view(), name = "create_account"),
    path('', include(router.urls)), 
]