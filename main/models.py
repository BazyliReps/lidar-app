from django.db import models
from datetime import datetime
import uuid


# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


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


class Grid(models.Model):
    rows = models.PositiveSmallIntegerField()
    columns = models.PositiveSmallIntegerField()
    cell_size = models.PositiveSmallIntegerField(default=20, verbose_name="cell size")


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
    board = models.ForeignKey(TestBoard, default=1, verbose_name="plansza testowa", on_delete=models.SET_DEFAULT)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reps = models.PositiveSmallIntegerField(verbose_name="powtórzenia pomiaru")
    operating_mode = models.CharField(
        choices=OPERATING_MODES,
        max_length=2,
        default='1',
        verbose_name='tryb pracy'
    )

    class Meta:
        verbose_name_plural = "pojedyńczy scenariusz"

    def __str__(self):
        return self.name


class TestScenario(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    created = models.DateTimeField(default=datetime.now())
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name_plural = "Test Scenarios"

    def __str__(self):
        return self.name
