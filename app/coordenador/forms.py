from .models import Funcionario, Plantao, Folga, PlantaoExtra
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CoordenadorForm(UserCreationForm):
    photo = forms.ImageField(required=False)

    class Meta(UserCreationForm):
        model = Coordenador
        fields = ('username', 'email', 'equipe', 'password1', 'password2',)


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('nome', 'sobrenome', 'extra', 'turno',)


class FuncionarioUpdate(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('nome', 'sobrenome', 'extra', 'turno',)


class PlantaoForm(forms.ModelForm):
    class Meta:
        model = Plantao
        fields = ('turno',)


class FolgaForm(forms.ModelForm):
    class Meta:
        model = Folga
        fields = ('data', 'plantao')


class PlantaoExtraForm(forms.ModelForm):
    class Meta:
        model = PlantaoExtra
        fields = ('data', 'plantao',)
