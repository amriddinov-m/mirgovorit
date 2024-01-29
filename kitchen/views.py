from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Product, Recipe, RecipeIngredient


def add_product_to_recipe(request):
    """Проверка, существует ли такой ингредиент в рецепте, если ингредиент уже существует, обновляем его вес"""
    if request.method == 'GET':
        recipe_id = request.GET.get('recipe_id')
        product_id = request.GET.get('product_id')
        weight = request.GET.get('weight')

        recipe = get_object_or_404(Recipe, id=recipe_id)
        product = get_object_or_404(Product, id=product_id)

        recipe_ingredient, created = RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            product=product,
            defaults={'weight': weight}
        )

        if not created:
            recipe_ingredient.weight = weight
            recipe_ingredient.save()

        return HttpResponse(f"Продукт {product.name} добавлен к рецепту {recipe.name} в количестве {weight} грамм.")


def cook_recipe(request):
    """Увеличиваем количество приготовлений для каждого продукта в рецепте"""
    if request.method == 'GET':
        recipe_id = request.GET.get('recipe_id')

        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredients = RecipeIngredient.objects.select_related('product').filter(recipe=recipe)
        for ingredient in ingredients:
            ingredient.product.quantity_cooked += 1
            ingredient.product.save()

        return HttpResponse(f"Блюдо {recipe.name} было приготовлено.")


def show_recipes_without_product(request):
    """Выводим все рецепты, в которых указанный продукт отсутствует, или присутствует в количестве меньше 10 грамм."""
    if request.method == 'GET':
        product_id = request.GET.get('product_id')

        product = get_object_or_404(Product, id=product_id)
        recipes = Recipe.objects.filter(~Q(recipeingredient__product=product) | Q(recipeingredient__weight__lt=10))

        html_content = "<h1>Рецепты без продукта {} или в которых его вес меньше 10 грамм</h1>".format(product.name)
        html_content += "<table border='1'><tr><th>ID</th><th>Название рецепта</th></tr>"
        for recipe in recipes:
            html_content += f"<tr><td>{recipe.id}</td><td>{recipe.name}</td></tr>"
        html_content += "</table>"
        return HttpResponse(html_content)
