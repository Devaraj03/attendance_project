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
    
    def calculate_total_break_time(self):            #-> newly committed
        total = timedelta()
        for br in self.breaks.all():
            if br.duration:
                total += br.duration
            
        self.total_break_time = total
        return total

    def calculate_total_work_time(self):
        if self.check_in_time and self.check_out_time:

            self.calculate_total_break_time()       #-> newly committed
            self.total_work_time =(
                self.check_out_time - self.check_in_time
            ) - self.total_break_time

            return self.total_work_time
        return None
    


class Break(models.Model):
    attendance = models.ForeignKey("Attendance",on_delete=models.CASCADE,related_name="breaks")

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True,blank=True)

    duration = models.DurationField(null=True,blank= True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def calculate_duration(self):
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
            return self.duration
        return None
    
    def save(self,*args,**kwargs):
        self.calculate_duration()
        super().save(*args,**kwargs)

    def __str__(self):
        return f"Break ({self.attendance.user})"