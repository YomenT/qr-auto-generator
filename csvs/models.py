from django.db import models

import uuid


class Csvs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    associated_program_name = models.CharField(max_length=100, blank=True)
    associated_program_description = models.TextField(blank=True)
    file_name = models.CharField(max_length=100)
    csv_file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
