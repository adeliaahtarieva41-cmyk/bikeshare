from django import forms
from django.core.exceptions import ValidationError
from .models import Bike, Category, TagBike


class AddBikeForm(forms.ModelForm):
    """Форма для добавления велосипеда, связанная с моделью Bike"""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию",
        label="Категория",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=TagBike.objects.all(),
        required=False,
        label="Теги",
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5})
    )

    class Meta:
        model = Bike
        fields = [
            'name', 'slug', 'brand', 'model', 'category', 'tags',
            'price_per_hour', 'price_per_day', 'address', 'description',
            'is_available', 'photo'
        ]

        labels = {
            'name': 'Название велосипеда',
            'slug': 'URL (слаг)',
            'brand': 'Бренд',
            'model': 'Модель',
            'price_per_hour': 'Цена за час (₽)',
            'price_per_day': 'Цена за день (₽)',
            'address': 'Адрес парковки',
            'description': 'Описание',
            'photo': 'Фото',
        }

        help_texts = {
            'slug': 'Только латинские буквы, цифры, дефис и подчёркивание',
        }

        error_messages = {
            'name': {
                'required': 'Пожалуйста, введите название велосипеда',
            },
            'slug': {
                'required': 'Пожалуйста, введите URL',
                'unique': 'Велосипед с таким URL уже существует',
            },
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Например: Городской велосипед'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'gorodskoy-velosiped'}),
            'brand': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Stels'}),
            'model': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Navigator 700'}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-input', 'step': '10', 'min': '0'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-input', 'step': '50', 'min': '0'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ул. Баумана, 15'}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'form-textarea'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError('Название не должно превышать 50 символов')
        return name

    def clean(self):
        cleaned_data = super().clean()
        price_hour = cleaned_data.get('price_per_hour')
        price_day = cleaned_data.get('price_per_day')

        if price_hour and price_day and price_day < price_hour:
            raise ValidationError('Цена за день не может быть меньше цены за час!')

        return cleaned_data


class UploadFileForm(forms.Form):
    """Форма для загрузки произвольного файла"""
    file = forms.FileField(
        label="Выберите файл",
        help_text="Максимальный размер файла: 10 МБ",
        widget=forms.FileInput(attrs={'class': 'form-file'})
    )


class UploadImageForm(forms.Form):
    """Форма для загрузки изображения"""
    image = forms.ImageField(
        label="Выберите изображение",
        help_text="Поддерживаются форматы: JPG, PNG, GIF",
        widget=forms.FileInput(attrs={'class': 'form-file'})
    )