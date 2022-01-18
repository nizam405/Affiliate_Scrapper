from django.db import models
from django.urls.base import reverse
from project.models import Project

# Create your models here.
class Post(models.Model):
    project         = models.ForeignKey(Project, on_delete=models.CASCADE)
    url             = models.URLField(max_length=256)
    title           = models.CharField(max_length=256, blank=True, null=True)
    contents        = models.TextField(blank=True, null=True)
    # html            = models.TextField(default="")
    meta            = models.TextField(blank=True, null=True)
    last_updated    = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        unique_together = ('project','url',)

    def __str__(self):
        return self.url
    
    def get_absolute_url(self):
        # Add project info
        return reverse('post:post-detail', kwargs={'project_id':self.project.pk,'pk': self.pk})

class Product(models.Model):
    name    = models.CharField(max_length=256)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
    #     unique_together = ('name','post',)

    def __str__(self):
        return self.name

class InternalLink(models.Model):
    address = models.CharField(max_length=256)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

class OutboundLink(models.Model):
    address = models.CharField(max_length=256)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

class ImageAltText(models.Model):
    text    = models.CharField(max_length=256)
    src     = models.URLField(max_length=255,default="")
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    class Meta:
        unique_together = ('post','text')

class H1(models.Model):
    heading = models.CharField(max_length=256)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading

class H2(models.Model):
    heading = models.CharField(max_length=256)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading

class H3(models.Model):
    heading = models.CharField(max_length=256)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading

class H4(models.Model):
    heading = models.CharField(max_length=256)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading