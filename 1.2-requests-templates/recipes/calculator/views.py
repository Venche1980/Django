from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def recipe_view(request, dish):
    # Проверяем, существует ли рецепт для данного блюда
    if dish not in DATA:
        return HttpResponse(f"Рецепт для {dish} не найден.", status=404)

    # Получаем количество порций из параметров запроса (по умолчанию 1)
    servings = request.GET.get('servings', 1)
    try:
        servings = int(servings)
        if servings <= 0:
            raise ValueError()
    except ValueError:
        return HttpResponse("Неверное значение параметра servings. Ожидалось положительное целое число.", status=400)

    # Рассчитываем ингредиенты для указанного количества порций
    recipe = DATA[dish]
    scaled_recipe = {ingredient: amount * servings for ingredient, amount in recipe.items()}

    # Формируем контекст для шаблона
    context = {
        'recipe': scaled_recipe,
    }

    # Рендерим шаблон с контекстом
    return render(request, 'calculator/index.html', context)