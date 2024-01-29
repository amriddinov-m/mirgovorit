from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    quantity_cooked = models.IntegerField(verbose_name='Кол-во раз приготовлено', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', verbose_name='Рецепт', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.CASCADE)
    weight = models.IntegerField(verbose_name='Вес')

    def __str__(self):
        return f"{self.recipe.name} - {self.product.name} ({self.weight}г)"

    class Meta:
        verbose_name = 'Набор входящих в рецепт продуктов'
        verbose_name_plural = 'Набор входящих в рецепт продуктов'
