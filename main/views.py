import datetime
import json
import random
import requests

from django import http
from django.conf import settings
from django.shortcuts import render

from main import models


def _get_daily_prompt():
    today = datetime.date.today()
    try:
        prompt = models.Prompt.objects.get(selected_date=today)
    except models.Prompt.DoesNotExist:
        prompt = random.choice(models.Prompt.objects.all())
        prompt.selected_date = today
        prompt.save()
    return prompt


def _get_wotd():
    today = datetime.date.today()
    api_key = settings.WORDNIK_SECRET
    api_url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?date={today}&api_key={api_key}"
    try:
        wotd = models.WordOfTheDay.objects.get(date=today)
    except models.WordOfTheDay.DoesNotExist:
        response = requests.get(api_url).json()
        wotd = models.WordOfTheDay.objects.create(word=response["word"])
        for definition in response["definitions"]:
            models.Definition.objects.create(
                word=wotd,
                part_of_speech=definition["partOfSpeech"],
                definition=definition["text"],
            )
        for example in response["examples"]:
            models.Example.objects.create(
                word=wotd,
                example=example["text"],
            )
    return wotd


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
    wotd = _get_wotd()
    return render(
        request, "base.html", {"links": links, "prompt": prompt, "wotd": wotd}
    )
