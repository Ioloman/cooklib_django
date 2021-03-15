"""cooklib_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from cooklib_django import settings
from cook_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('recipe/', views.RecipeList.as_view(), name='recipes'),
    path('recipe/<int:id>/', views.RecipeView.as_view(), name='recipe'),
    path('ingredient/<int:id>/edit/', views.IngredientEdit.as_view(), name='ingredient_edit'),
    path('ingredient/', views.ingredient_create, name='ingredient_create'),
    path('recipe/<int:id>/edit/', views.RecipeEdit.as_view(), name='recipe_edit'),
    path('ingredient/<int:id>/delete/', views.ingredient_delete, name='ingredient_delete'),
    path('recipe/<int:id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('managing/', views.Managing.as_view(), name='managing'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
