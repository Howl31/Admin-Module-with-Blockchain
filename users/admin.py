from django.contrib import admin
from .models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserDetail._meta.fields]


class HashAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HashTable._meta.fields]


admin.site.register(HashTable, HashAdmin)
admin.site.register(UserDetail, UserAdmin)