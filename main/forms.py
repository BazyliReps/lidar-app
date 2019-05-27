from datetime import datetime
from django import forms
from django.forms import ModelForm

from .models import TestBoard, SingleTest, TestScenario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", 'email', "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class BoardForm(ModelForm):
    class Meta:
        model = TestBoard
        fields = ["name", "rows", "columns", "cell_size", "summary", "obstacles_json", "lidar_x", "lidar_y"]
        widgets = {'obstacles_json': forms.HiddenInput(), 'lidar_x': forms.HiddenInput(),
                   'lidar_y': forms.HiddenInput()}


class ScenarioForm(ModelForm):
    board_set = TestBoard.objects.all()
    board = forms.ModelChoiceField(queryset=board_set, required=True, label="Plansza")
    test_set = SingleTest.objects.all()
    tests = forms.ModelMultipleChoiceField(queryset=test_set, required=True,
                                           label="Testy")

    class Meta:
        model = TestScenario
        fields = ["name", "summary", "board", "tests"]


class SingleTestForm(ModelForm):
    class Meta:
        model = SingleTest
        fields = ["name", "operating_mode", "delay", "repetitions"]
