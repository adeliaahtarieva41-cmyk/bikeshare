import os
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Bike, Category, TagBike, TechPassport
from .forms import AddBikeForm, UploadFileForm, UploadImageForm

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить велосипед", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'users:login'},
]

def index(request):
    bikes = Bike.available.all()
    return render(request, 'women/index.html', {
        'title': 'Аренда велосипедов',
        'bikes': bikes,
        'menu': menu,
        'cat_selected': 0,
    })

def show_bike(request, bike_slug):
    bike = get_object_or_404(Bike, slug=bike_slug, is_available=Bike.Status.AVAILABLE)
    return render(request, 'women/bike.html', {'bike': bike})

def all_bikes(request):
    bikes = Bike.objects.all()
    return render(request, 'women/all_bikes.html', {
        'title': 'Все велосипеды',
        'bikes': bikes,
        'menu': menu,
    })


def about(request):
    uploaded_file_name = None

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            file_name = handle_uploaded_file(uploaded_file)
            uploaded_file_name = file_name
            print(f"Файл загружен: {file_name}")
    else:
        form = UploadFileForm()

    return render(request, 'women/about.html', {
        'title': 'О сайте',
        'menu': menu,
        'form': form,
        'uploaded_file_name': uploaded_file_name,
    })

def contact(request):
    return render(request, 'women/contact.html', {
        'title': 'Обратная связь',
        'menu': menu,
    })

def login(request):
    return render(request, 'women/login.html', {
        'title': 'Вход',
        'menu': menu,
    })

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    bikes = Bike.available.filter(category=category)
    return render(request, 'women/index.html', {
        'title': category.name,
        'bikes': bikes,
        'menu': menu,
        'cat_selected': category.id,
    })

def show_tag(request, tag_slug):
    tag = get_object_or_404(TagBike, slug=tag_slug)
    bikes = Bike.available.filter(tags=tag)
    return render(request, 'women/index.html', {
        'title': f'Тег: {tag.tag}',
        'bikes': bikes,
        'menu': menu,
    })


@login_required
def addpage(request):
    if request.method == 'POST':
        form = AddBikeForm(request.POST, request.FILES)
        if form.is_valid():
            bike = form.save(commit=False)
            bike.author = request.user  # ← добавить автора
            bike.save()
            form.save_m2m()
            print(f"Добавлен новый велосипед: {bike.name}")
            return redirect('home')
        else:
            print("Форма не прошла валидацию")
            print(form.errors)
    else:
        form = AddBikeForm()

    return render(request, 'women/addpage.html', {
        'title': 'Добавление велосипеда',
        'menu': menu,
        'form': form,
    })

#Сохраняет загруженный файл в папку uploads
def handle_uploaded_file(f):
    """Сохраняет загруженный файл в папку uploads с уникальным именем"""
    # Создаём папку uploads, если её нет
    upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Получаем имя и расширение файла
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]

    # Генерируем уникальное имя
    unique_name = f"{name}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(upload_dir, unique_name)

    # Сохраняем файл
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return unique_name


