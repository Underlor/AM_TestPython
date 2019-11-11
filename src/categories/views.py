import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from categories.models import Category


class CategoriesView(View):
    def create_categories(self, categories_list: list, parent: Category = None):
        for dict_category in categories_list:
            category = Category.objects.create(
                parent=parent,
                name=dict_category.get('name')
            )

            if dict_category.get('children'):
                self.create_categories(dict_category.get('children'), category)

    def post(self, request, *args, **kwargs):
        categories_list = json.loads(request.body)

        if isinstance(categories_list, dict):
            categories_list = [categories_list]

        try:
            self.create_categories(categories_list)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({}, status=200)


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        root_category = get_object_or_404(Category, id=kwargs.get('id'))

        return JsonResponse(root_category.get_data(), safe=False)
