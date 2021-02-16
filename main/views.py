import random

from django.shortcuts import render
from django.utils import timezone

from main import models


def _get_daily_prompt():
    today = timezone.now().date()
    try:
        prompt = models.Prompt.objects.get(selected_date=today)
    except models.Prompt.DoesNotExist:
        prompt = random.choice(models.Prompt.objects.all())
        prompt.selected_date = today
        prompt.save()
    return prompt


def index(request):
    links = models.Link.objects.filter(active=True)
    prompt = _get_daily_prompt()
    return render(request, "base.html", {"links": links, "prompt": prompt})
