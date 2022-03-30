from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import Projectarticle

admin.site.register(Projectarticle, MarkdownxModelAdmin)
