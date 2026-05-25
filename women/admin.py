from django.contrib import admin
from django.utils.html import format_html
from .models import Bike, Category, TagBike, TechPassport


# ПОЛЬЗОВАТЕЛЬСКИЙ ФИЛЬТР ПО ТЕГАМ
class TagFilter(admin.SimpleListFilter):
    title = 'По тегам'
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        return [
            ('has_tags', 'Есть теги'),
            ('no_tags', 'Без тегов'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'has_tags':
            return queryset.filter(tags__isnull=False).distinct()
        if self.value() == 'no_tags':
            return queryset.filter(tags__isnull=True)
        return queryset


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'brand', 'price_per_hour', 'is_available', 'category', 'post_photo')
    list_display_links = ('name',)
    list_editable = ('is_available',)
    ordering = ('-time_create', 'name')
    search_fields = ('name', 'brand', 'model', 'category__name', 'tags__tag')

    # ФИЛЬТРЫ (добавлен TagFilter)
    list_filter = (TagFilter, 'is_available', 'category', 'brand')

    list_per_page = 10
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)

    # Поля в форме редактирования
    fields = (
        'name', 'slug', 'brand', 'model', 'category', 'tags',
        'price_per_hour', 'price_per_day', 'address', 'description',
        'is_available', 'photo', 'post_photo', 'tech_passport'
    )
    readonly_fields = ('post_photo',)

    # Показывать кнопки сохранения сверху
    save_on_top = True

    # МЕТОД ДЛЯ ОТОБРАЖЕНИЯ МИНИАТЮРЫ В АДМИНКЕ
    @admin.display(description="Фото")
    def post_photo(self, bike: Bike):
        if bike.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 8px;" />',
                bike.photo.url
            )
        return "Без фото"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(TagBike)
class TagBikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    search_fields = ('tag',)
    prepopulated_fields = {'slug': ('tag',)}
    ordering = ('tag',)


@admin.register(TechPassport)
class TechPassportAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'year_of_manufacture', 'mileage', 'battery_health')
    list_display_links = ('id', 'serial_number')
    search_fields = ('serial_number',)
    list_filter = ('year_of_manufacture', 'battery_health')
    ordering = ('-year_of_manufacture',)