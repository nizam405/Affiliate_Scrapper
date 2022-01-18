from django.db import models
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=256)
    # slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return reverse("project:project-detail", kwargs={"project_id": self.pk})

    def __str__(self):
        return self.name