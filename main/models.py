import datetime
import uuid

from django.db import models
from django.utils import timezone


class Link(models.Model):
    active = models.BooleanField(default=None)
    icon = models.ImageField()
    name = models.CharField(max_length=127)
    url = models.URLField()


class WordOfTheDay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=datetime.date.today)
    word = models.CharField(max_length=127)


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(WordOfTheDay, on_delete=models.CASCADE)
    part_of_speech = models.CharField(max_length=31)
    definition = models.TextField()


class Example(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(WordOfTheDay, on_delete=models.CASCADE)
    example = models.TextField()


class Prompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.CharField(max_length=255)
    selected_date = models.DateField(null=True, blank=True)


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.ForeignKey(Prompt, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    wordcount = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        self.wordcount = len(self.text.split(" "))
        super().save(*args, **kwargs)
