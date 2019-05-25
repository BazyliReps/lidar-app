from django.contrib import admin
from .models import TestBoard, TestScenario, Obstacle, SingleTest, SingleScanResult


# Register your models here.

admin.site.register(TestBoard)
admin.site.register(Obstacle)
admin.site.register(SingleTest)
admin.site.register(TestScenario)
admin.site.register(SingleScanResult)
