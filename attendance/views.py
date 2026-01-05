from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Attendance, Break


@login_required
def attendance_dashboard(request):
    attendance, created = Attendance.objects.get_or_create(
        user=request.user,
        date=timezone.localdate()
    )

    active_break = attendance.breaks.filter(end_time__isnull=True).last()

    context = {
        "attendance": attendance,
        "active_break": active_break,
    }
    return render(request, "attendance/dashboard.html", context)

@login_required
def check_in(request):
    attendance, _ = Attendance.objects.get_or_create(
        user=request.user,
        date=timezone.localdate()
    )

    if not attendance.check_in_time:
        attendance.check_in_time = timezone.now()
        attendance.save(update_fields=["check_in_time", "updated_at"])

    return redirect("attendance:dashboard")

@login_required
def check_out(request):
    attendance = get_object_or_404(
        Attendance,
        user=request.user,
        date=timezone.localdate()
    )

    if not attendance.check_out_time:
        attendance.check_out_time = timezone.now()
        attendance.calculate_total_work_time()
        attendance.status = Attendance.STATUS_PRESENT
        attendance.save()

    return redirect("attendance:dashboard")

@login_required
def start_break(request):
    attendance = get_object_or_404(
        Attendance,
        user=request.user,
        date=timezone.localdate()
    )

    # Prevent multiple active breaks
    if not attendance.breaks.filter(end_time__isnull=True).exists():
        Break.objects.create(
            attendance=attendance,
            start_time=timezone.now()
        )

    return redirect("attendance:dashboard")

@login_required
def end_break(request):
    attendance = get_object_or_404(
        Attendance,
        user=request.user,
        date=timezone.localdate()
    )

    br = attendance.breaks.filter(end_time__isnull=True).last()
    if br:
        br.end_time = timezone.now()
        br.save()  # signals update attendance automatically

    return redirect("attendance:dashboard")
