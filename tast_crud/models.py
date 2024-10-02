from django.db import models
from django.contrib.auth.models import User



class SheduledTask(models.Model):
    task_name = models.CharField(max_length=50)
    task_details= models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sheduled_time = models.DateTimeField()
    task_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.task_name}"
    