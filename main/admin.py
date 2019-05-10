from django.contrib import admin
from .models import Category, TestBoard, TestScenario, Obstacle
from django.db import models


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ["category",
              "summary",
              "slug"]


admin.site.register(TestBoard)
admin.site.register(Obstacle)
admin.site.register(TestScenario)
admin.site.register(Category, CategoryAdmin)
