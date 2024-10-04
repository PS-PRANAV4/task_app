from django.shortcuts import render

from rest_framework import viewsets
from .models import SheduledTask
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views
from datetime import datetime
from django.db.models import Value, F
from django.db.models.functions import TruncDate
from django.contrib.postgres.aggregates import JSONBAgg



class TaskViewSet(viewsets.ModelViewSet):
    queryset = SheduledTask.objects.all().order_by("id")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SheduledTask.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    

class ChangeStatus(views.APIView):
    def get(self,request,id):
        try:
            task = SheduledTask.objects.get(id=id)
            task.task_status = True if task.task_status == False else False
            task.save()
        except Exception as e:
            return Response({"msg":"failed"},status=400)

        return Response({"msg":"success"},status=200)