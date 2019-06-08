import json
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import paho.mqtt.publish as publish
from reportlab.graphics import renderPDF
import xml.dom.minidom
from svglib.svglib import SvgRenderer
from svglib.svglib import svg2rlg

from .forms import NewUserForm, BoardForm, SingleTestForm, ScenarioForm
from .models import TestBoard, Obstacle, SingleTest, TestScenario, SingleScanResult


# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={})


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


def tests(request):
    return render(request=request,
                  template_name=f"main/tests.html",
                  context={"tests": SingleTest.objects.all()})


@csrf_exempt
def create_single_test(request):
    if request.method == "POST":
        form = SingleTestForm(request.POST)
        if form.is_valid():
            test = form.save()
            name = test.name
            messages.success(request, f'Utworzono test "{name}"!')
            return redirect("main:tests")

    form = SingleTestForm

    return render(request=request,
                  template_name=f"main/create_single_test.html",
                  context={'form': form})


def scenarios(request):
    return render(request=request,
                  template_name=f"main/scenarios.html",
                  context={"scenarios": TestScenario.objects.all()})


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
    testmodes = SingleTest.objects.all()
    form = ScenarioForm
    context = (form, testboards, testmodes)

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


def execute_test(request, test_id):
    test = SingleTest.objects.filter(test_id=test_id)[0]
    print(test)
    delay = test.delay
    mode = test.operating_mode
    params = {"delay": delay, "mode": mode}
    params_json = json.dumps(params)
    publish.single("make_scan", params_json, hostname="192.168.0.50")
    return redirect("main:tests")


def execute_scenario(request, id):
    scenario = TestScenario.objects.filter(id=id)[0]
    tests_set = list(scenario.tests.all().values())
    data = {"id": id, "tests": tests_set}
    data_json = json.dumps(data, default=lambda d: '<>')
    print(data_json)
    publish.single("make_scan", data_json, hostname="192.168.0.50")
    return redirect("main:scenarios")


def results(request):
    results = SingleScanResult.objects.all()
    results = results.extra(order_by=['mode'])
    return render(request=request,
                  template_name=f"main/results.html",
                  context={"results": results})


def display_result(request, pk):
    result = SingleScanResult.objects.filter(pk=pk)[0]
    return render(request=request,
                  template_name=f"main/display_measurements.html",
                  context={"measurements": result.measurements})


@csrf_exempt
def create_pdf(request):
    print("w views")

    drawing = svg2rlg("file:///C:/Users/bazyli/Downloads/skan.svg")

    renderPDF.drawToFile(drawing, "C:/Users/bazyli/Downloads/file.pdf")

    return redirect("main:results")
