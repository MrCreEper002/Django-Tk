from itertools import chain

from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Actor)
admin.site.register(Films)
admin.site.register(ListFilmsActor)
