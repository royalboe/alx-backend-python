from rest_framework import routers
from .views import MessageView, UserView

router = routers.DefaultRouter()
router.register('users', UserView)
router.register('messages', MessageView)