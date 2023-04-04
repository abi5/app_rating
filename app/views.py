# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
# from django.contrib.auth.models import User as admin_user
from rest_framework import viewsets, permissions
from .models import App, User, TaskCompletion
from .serializer import AppSerializer, UserSerializer, TaskCompletionSerializer
# import re
# from django.http import JsonResponse

# def my_view(request):
#     text = '{"orders":[{"id":1},{"id":2},{"id":3},{"id":4},{"id":5},{"id":6},{"id":7},{"id":8},{"id":9},{"id":10},{"id":11},{"id":648},{"id":649},{"id":650},{"id":651},{"id":652},{"id":653}],"errors":[{"code":3,"message":"[PHP Warning #2] count(): Parameter must be an array or an object that implements Countable (153)"}]}'
#
#     numbers = re.findall(r'(?<=background-color: orange;">)\d+(?=<)', text)
#
#     return JsonResponse(numbers, safe=False)



class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskCompletionViewSet(viewsets.ModelViewSet):
    queryset = TaskCompletion.objects.all()
    serializer_class = TaskCompletionSerializer
    permission_classes = [permissions.IsAuthenticated]

@login_required(login_url='login_view')
def home(request):
    user = request.user
    print(user)
    p_and_t = User.objects.get(username=request.user)
    return render(request, 'home.html', {'user': user, 'point': p_and_t},)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # name = request.POST['name']
        profile_picture = request.FILES['profile_picture']
        user_a = User.objects.create_user(username=username, password=password, profile_picture=profile_picture)
        user_a.save()
        # user = User(username=username, password=password, profile_picture=profile_picture)
        # user.save()
        # login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

@login_required
def apps_list(request):
    apps = App.objects.all()
    return render(request, 'apps_list.html', {'apps': apps})

@login_required
def app_detail(request, app_id):
    app = App.objects.get(id=app_id)
    return render(request, 'app_detail.html', {'app': app})

@login_required
def task_submit(request, app_id, app_name,points):
    print(app_id, request.user, app_name, points)
    print(request.user.id)
    # user_id=request.user.id
    # task = TaskCompletion.objects.get(id=app_id)
    point = User.objects.get(username=request.user)
    app = App.objects.get(name=app_name)
    if request.method == 'POST':
        screenshot = request.FILES['screenshot']
        # task.screenshot = screenshot
        task = TaskCompletion(user=point, app=app, screenshot=screenshot)
        task.save()

        point.points += points
        point.save()

        return redirect('home')
    return render(request, 'task_submit.html',) # {'task': task}


