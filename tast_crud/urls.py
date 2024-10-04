from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet,ChangeStatus

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('change-status/<int:id>',ChangeStatus.as_view())
]

