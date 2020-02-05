from django.contrib.auth.models import AbstractUser
from django.db import models


class Coordenador(AbstractUser):
    EQUIPE_CHOICES = (
        ('RO', 'RO'),
        ('TARM', 'TARM'),
    )
    equipe = models.CharField(
        max_length=15, choices=EQUIPE_CHOICES, default='TARM')
    photo = models.ImageField(
        upload_to="gerente/", default='gerente/default.jpg', blank=True, null=True)
    email = models.EmailField(
        primary_key=True, blank=False, null=False, unique=True)

    def __str__(self):
        return self.username


class Funcionario(models.Model):
    EXTRAS_CHOICES = (
        ('Folguista', 'Folguista'),
        ('Feirista', 'Feirista'),
    )
    EQUIPE_CHOICES = (
        ('RO', 'RO'),
        ('TARM', 'TARM'),
    )
    nome = models.CharField(max_length=50, null=False, blank=False)
    sobrenome = models.CharField(max_length=50, null=False, blank=False)
    extra = models.CharField(max_length=15, blank=True, choices=EXTRAS_CHOICES)
    turno = models.CharField(max_length=50, default=True)
    equipe = models.CharField(
        max_length=15, choices=EQUIPE_CHOICES, default='TARM')
    REQUIRED_FIELDS = ['nome', 'sobrenome', 'turno']


class Plantao(models.Model):
    turno = models.CharField(max_length=20, primary_key=True, choices=(
        ("NDA", "NDA"),
        ("A - Madrugada", "A - Madrugada"),
        ("B - Manhã", "B - Manhã"),
        ("C - Tarde", "C - Tarde"),
        ("D - Noite", "D - Noite"),
    ),)
    funcionario = models.ManyToManyField(Funcionario)
    REQUIRED_FIELDS = ['turno']

    class Meta:
        ordering = ['turno']


class Folga(models.Model):
    EQUIPE_CHOICES = (
        ('RO', 'RO'),
        ('TARM', 'TARM'),
    )

    folga_id = models.AutoField(primary_key=True)
    data = models.DateField()
    plantao = models.ForeignKey("Plantao", on_delete=models.DO_NOTHING, related_name='plantao_folga')
    equipe = models.CharField(max_length=15, choices=EQUIPE_CHOICES, default='TARM')

    class Meta:
        unique_together = (('data', 'plantao', 'equipe'),)

    def get_year(self):
        return self.data.year

    def get_mes(self):
        return self.data.month


class PlantaoExtra(models.Model):
    EQUIPE_CHOICES = (
        ('RO', 'RO'),
        ('TARM', 'TARM'),
    )
    p_extra_id = models.AutoField(primary_key=True)
    data = models.DateField()
    plantao = models.ForeignKey(
        "Plantao", on_delete=models.DO_NOTHING, related_name='plantao_extra')
    equipe = models.CharField(
        max_length=15, choices=EQUIPE_CHOICES, default='TARM')

    class Meta:
        unique_together = (('data', 'plantao', 'equipe'),)

    def get_year(self):
        return self.data.year

    def get_mes(self):
        return self.data.month
