from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from datetime import timedelta
from .models import Break


@receiver(post_save,sender=Break)
def update_attendance_on_break_save(sender,instance,**kwargs):
    attendance = instance.attendance
    attendance.calculate_total_break_time()
    attendance.calculate_total_work_time()

    attendance.save(
        update_fields = ["total_break_time","total_work_time","updated_at"]

    )


@receiver(post_delete,sender=Break)
def update_attendance_on_break_delete(sender,instance,**kwargs):
    attendance = instance.attendance
    attendance.calculate_total_break_time()
    attendance.calculate_total_work_time()
    attendance.save(
        update_fields=["total_break_time","total_work_time","updated_at"]
    )