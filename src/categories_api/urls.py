from django.contrib import admin
from django.urls import path

from categories.views import CategoriesView, CategoryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoriesView.as_view()),
    path('categories/<int:id>/', CategoryView.as_view())
]
