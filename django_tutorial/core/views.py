from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.http import HttpResponse


def home(request):
    # return HttpResponse("Hello Django! 🚀")
    # return render(request, "home.html")
    tasks = Task.objects.all().order_by("-created_at")
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TaskForm()

    return render(request, "home.html", {"tasks": tasks,"form": form})
