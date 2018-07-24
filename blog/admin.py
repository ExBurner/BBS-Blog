from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Sort)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(ArticleToTag)
admin.site.register(Like)
admin.site.register(Comment)
