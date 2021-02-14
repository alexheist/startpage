from django.core.management.base import BaseCommand
from django.conf import settings
from main import models


class Command(BaseCommand):
    help = "Imports prompts from prompts.txt"

    def handle(self, *args, **kwargs):
        prompts_file_path = f"{settings.ROOT_DIR}/prompts.txt"
        with open(prompts_file_path, "r") as f:
            prompts = f.readlines()
        for prompt in prompts:
            models.Prompt.objects.create(prompt=prompt.strip())
        self.stdout.write("Done.")
