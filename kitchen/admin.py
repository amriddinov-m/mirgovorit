from django.contrib import admin

from kitchen.models import Product, Recipe, RecipeIngredient


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'name', 'quantity_cooked'
    search_fields = 'name',


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = 'name',
    search_fields = 'name',
