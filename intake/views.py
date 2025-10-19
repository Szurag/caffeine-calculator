from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from intake.forms import IntakeForm
from intake.models import Intake


@login_required(login_url='login')
def add_intake(request):
    if request.method == "POST":
        form = IntakeForm(request.POST, user=request.user)
        if form.is_valid():
            intake = form.save(commit=False)
            intake.user = request.user
            intake.save()
            messages.success(request,
                             f'Dodano {intake.quantity}x {intake.product.name} ({intake.total_caffeine} mg kofeiny)')
            return redirect('dashboard')
    else:
        form = IntakeForm(user=request.user)

    return render(request, "intake/add_intake.html", {"form": form})


def delete_intake(request, intake_id):
    try:
        intake = Intake.objects.get(id=intake_id, user=request.user)
        intake.delete()
        messages.success(request, 'Pozycja spożycia została usunięta.')
    except Intake.DoesNotExist:
        messages.error(request, 'Nie znaleziono pozycji spożycia lub nie masz do niej dostępu.')

    return redirect('dashboard')
