from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet,TaskGroupedByDateView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calander_view/',TaskGroupedByDateView.as_view())
]

