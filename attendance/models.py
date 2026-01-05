from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL

class Attendance(models.Model):
    STATUS_PRESENT = "PRESENT"            #Attendance status
    STATUS_INCOMPLETE = "INCOMPLETE"
    STATUS_ABSENT = "ABSENT"

    STATUS_CHOICES = (
        (STATUS_PRESENT,"Present"),
        (STATUS_INCOMPLETE,"Incomplete"),
        (STATUS_ABSENT,"Absent"),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="attendances")
    date = models.DateField(default=timezone.localdate)

    check_in_time = models.DateTimeField(null=True,blank=True)
    check_out_time = models.DateTimeField(null=True,blank=True)

    total_break_time = models.DurationField(default=timedelta())
    total_work_time  = models.DurationField(null=True,blank=True)

    status = models.CharField(max_length=25,choices=STATUS_CHOICES,default=STATUS_INCOMPLETE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user","date")
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user","date"]),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.date}"
    
    def calculate_total_work_time(self):
        
        if self.check_in_time and self.check_out_time:
            self.total_work_time =(
                self.check_out_time - self.check_in_time
            ) - self.total_break_time

            return self.total_work_time
        return None