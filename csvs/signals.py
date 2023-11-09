from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Csvs
from .csv_parser import parse_csv
import csv

@receiver(post_save, sender=Csvs)
def process_csv(sender, instance, created, **kwargs):
    if created:
        with instance.csv_file.open(mode='r') as file:
            reader = csv.reader(file)
            parse_csv(reader)
