from django.contrib import admin
from .models import User, Card, Item, Date

# Register your models here.

admin.site.register(User)
admin.site.register(Card)
admin.site.register(Item)
admin.site.register(Date)