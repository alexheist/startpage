import json
import random

from django import http
from django.conf import settings
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
    if request.is_ajax():
        prompt = models.Prompt.objects.get(prompt=request.POST["prompt"])
        entry = request.POST["entry"]
        secret = request.POST["secret"]
        if secret == settings.FORM_SECRET:
            models.Entry.objects.create(
                prompt=prompt,
                text=entry,
            )
            return http.JsonResponse({"status": 200})
        return http.JsonResponse({"status": 401})
    links = models.Link.objects.filter(active=True)
    prompt = _get_daily_prompt()
    return render(request, "base.html", {"links": links, "prompt": prompt})
