from django.shortcuts import render
from main import models


def index(request):
    links = models.Link.objects.filter(active=True)
    return render(request, "base.html", {"links": links})