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
    queryset = SheduledTask.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskGroupedByDateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            try:
                # Convert to datetime objects
                start_date = datetime.fromisoformat(start_date)
                end_date = datetime.fromisoformat(end_date)

                # Group by date and aggregate task information
                tasks_by_date = (
                    SheduledTask.objects
                    .filter(due_date__range=(start_date, end_date))
                    .annotate(task_date=TruncDate('due_date'))  # Truncate time from due_date
                    .values('task_date')  # Get unique task dates
                    .annotate(
                        tasks=JSONBAgg(
                            Value({
                                'id': F('id'),
                                'title': F('title'),
                                'description': F('description'),
                                'completed': F('completed')
                            })
                        )
                    )
                    .order_by('task_date')  # Optional: Order by date
                )

                # Create a dictionary from the aggregated results
                result = {item['task_date']: item['tasks'] for item in tasks_by_date}

                return Response(result)

            except ValueError:
                return Response({"error": "Invalid date format"}, status=400)

        return Response({"error": "Start date and end date are required"}, status=400)