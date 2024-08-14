from django.contrib import admin
from .models import Question
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['title', 'sort_order', 'expanded']


admin.site.register(Question, OrderAdmin)

