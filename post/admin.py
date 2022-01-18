from django.contrib import admin
from .models import Post, Product, InternalLink, OutboundLink, ImageAltText, H1, H2, H3, H4
# Register your models here.
admin.site.register(Post)
admin.site.register(Product)
admin.site.register(InternalLink)
admin.site.register(OutboundLink)
admin.site.register(ImageAltText)
admin.site.register(H1)
admin.site.register(H2)
admin.site.register(H3)
admin.site.register(H4)
