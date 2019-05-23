from django.db import models
from datetime import datetime
import uuid


# Create your models here.

class Obstacle(models.Model):
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "przeszkody"


class TestBoard(models.Model):
    name = models.CharField(max_length=200, verbose_name="opis")
    rows = models.PositiveSmallIntegerField(default=20, verbose_name="rzędy")
    columns = models.PositiveSmallIntegerField(default=20, verbose_name="kolumny")
    cell_size = models.PositiveSmallIntegerField(default=20, verbose_name="rozmiar komórki")
    summary = models.CharField(max_length=200, verbose_name="uwagi")
    board_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    obstacles_json = models.CharField(max_length=10000, blank=True, null=True)
    obstacles = models.ManyToManyField(Obstacle)
    lidar_x = models.PositiveSmallIntegerField(default=0)
    lidar_y = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Test Boards"

    def __str__(self):
        return self.name


class SingleTest(models.Model):
    OPERATING_MODES = (
        ('const', 'ciągły'),
        ('1', '1'),
        ('2', '1/2'),
        ('4', '1/4'),
        ('8', '1/8'),
        ('16', '1/16'),
        ('32', '1/32'),
    )

    name = models.CharField(max_length=200, verbose_name='opis')
    test_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delay = models.FloatField(default=0.001)
    operating_mode = models.CharField(
        choices=OPERATING_MODES,
        max_length=2,
        default='1',
        verbose_name='tryb pracy'
    )

    class Meta:
        verbose_name_plural = "pojedyńczy test"

    def __str__(self):
        return str(self.operating_mode) + " " + str(self.delay)


class TestScenario(models.Model):
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, verbose_name="uwagi")
    created = models.DateTimeField(default=datetime.now())
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tests = models.ManyToManyField(SingleTest)
    board = models.ForeignKey(TestBoard, default=1, verbose_name="plansza testowa", on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = "Scenariusz testowy"

    def __str__(self):
        return self.name


class SingleScanResult(models.Model):
    single_scan_result_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=datetime.now())
    delay = models.FloatField(default=0.001)
    mode = models.PositiveSmallIntegerField()
    scenario = models.ForeignKey(TestScenario, on_delete=models.CASCADE)


class Measurement(models.Model):
    step_number = models.SmallIntegerField()
    distance = models.FloatField()
    signal_strength = models.FloatField()
    scan = models.ForeignKey(SingleScanResult, on_delete=models.CASCADE)
