import json

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import NewUserForm, BoardForm, ScenarioForm
from .models import Category, TestBoard, Obstacle, SingleTest


# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"categories": Category.objects.all()})


def boards(request):
    return render(request=request,
                  template_name=f"main/boards.html",
                  context={"boards": TestBoard.objects.all()})


@csrf_exempt
def create_board(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.save()
            name = board.name
            loaded_json = json.loads(board.obstacles_json)
            for obs in loaded_json:
                o = Obstacle(x=obs['x'], y=obs['y'], type=obs['type'])
                o.save()
                board.obstacles.add(o)

            messages.success(request, f"Utworzono planszę {name}!")
            return redirect("main:boards")

    form = BoardForm
    return render(request,
                  'main/create_board.html',
                  context={'form': form})


def edit_board(request, board_id):
    grid = TestBoard.objects.filter(board_id=board_id)
    return render(request=request,
                  template_name=f"main/edit_board.html",
                  context={"grid": grid.first()})


def scenarios(request):
    return render(request=request,
                  template_name=f"main/scenarios.html",
                  context={"tests": SingleTest.objects.all()})


@csrf_exempt
def create_scenario(request):
    if request.method == "POST":
        form = ScenarioForm(request.POST)
        if form.is_valid():
            scenario = form.save()
            name = scenario.name
            messages.success(request, f'Utworzono scenariusz "{name}"!')
            return redirect("main:scenarios")

    testboards = TestBoard.objects.all()
    form = ScenarioForm
    context = (form, testboards)

    return render(request=request,
                  template_name=f"main/create_scenario.html",
                  context={'context': context})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Utworzono konto {username} ")
            login(request, user)
            messages.info(request, f"Jesteś zalogowany jako {username} ")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    return render(request,
                  "main/register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowano pomyślnie!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"jestes zalogowany jako {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Niepoprawna nazwa użytkownika lub hasło")
        else:
            messages.error(request, "Niepoprawna nazwa użytkownika lub hasło")

    else:
        form = AuthenticationForm()
        return render(request, "main/login.html", {"form": form})
