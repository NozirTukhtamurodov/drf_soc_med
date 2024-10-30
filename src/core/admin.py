from django.contrib import admin
from core.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
