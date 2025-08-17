from .views import UserViewSet, MessageViewSet, ConversationViewSet, ExampleView, HealthCheckView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'conversations', ConversationViewSet)
# router.register(r'example', ExampleView, basename='example')

urlpatterns = router.urls
from .views import ExampleView
from django.urls import path, include, re_path

urlpatterns += [
    path('example/', ExampleView.as_view(), name='example'),
    path('health/', HealthCheckView.as_view(), name='health'),
]
