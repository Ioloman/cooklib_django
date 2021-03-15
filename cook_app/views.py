from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views import View

from .forms import IngredientForm, RecipeForm
from .models import Recipe, IngredientList, RecipeLine, Ingredient


class Home(TemplateView):
    template_name = 'html/index.html'


class RecipeList(ListView):
    model = Recipe
    template_name = 'html/recipes.html'
    context_object_name = 'recipes'

    def post(self, request):
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            if request.FILES.get('recipe_image'):
                recipe.image = request.FILES.get('recipe_image')
            recipe.save()

            for name, amount, measurement in zip(
                    request.POST.getlist('ingredient_name'),
                    request.POST.getlist('amount'),
                    request.POST.getlist('measurement')
            ):
                if int(name) != -1:
                    ingredient_list = IngredientList.objects.create(
                                                                    ingredient_id=name,
                                                                    amount=amount,
                                                                    measurement=measurement,
                                                                    recipe=recipe
                                                                )
                    ingredient_list.save()

            step_number = 1
            for order_number, title, step_description in zip(
                    request.POST.getlist('order_number'),
                    request.POST.getlist('title'),
                    request.POST.getlist('step_description'),
            ):
                if title and step_description:
                    step = RecipeLine.objects.create(
                        title=title, discription=step_description,
                        order_number=step_number, recipe=recipe
                    )
                    step_number += 1
                    if request.FILES.get('step_image_' + order_number):
                        step.image = request.FILES.get('step_image_' + order_number)
                    step.save()

            return redirect('recipe', id=recipe.id)
        return redirect('managing')


class RecipeView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'html/one_recipe.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['ingredients'] = IngredientList.objects.filter(recipe__id=self.kwargs['id'])
        context['steps'] = RecipeLine.objects.filter(recipe__id=self.kwargs['id']).order_by('order_number')
        return context


class Managing(View):
    template_name = 'html/managing.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            {'recipes': Recipe.objects.all(), 'ingredients': Ingredient.objects.all()}
        )


class IngredientEdit(UpdateView):
    model = Ingredient
    success_url = reverse_lazy('managing')
    template_name = 'html/ingredient_modify.html'
    context_object_name = 'ingredient'
    pk_url_kwarg = 'id'
    fields = '__all__'


def ingredient_delete(request, id):
    if request.method == 'POST':
        ingredient = get_object_or_404(Ingredient, id=id)
        ingredient.delete()
        return redirect('managing')


def ingredient_create(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            if request.FILES.get('image'):
                ingredient.image = request.FILES.get('image')
            ingredient.save()
        return redirect('managing')


def recipe_delete(request, id):
    if request.method == 'POST':
        ingredient = get_object_or_404(Recipe, id=id)
        ingredient.delete()
        return redirect('managing')


class RecipeEdit(UpdateView):
    model = Recipe
    success_url = reverse_lazy('managing')
    template_name = 'html/recipe_modify.html'
    context_object_name = 'recipe'
    pk_url_kwarg = 'id'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['ingredients'] = IngredientList.objects.filter(recipe__id=self.kwargs['id'])
        context['steps'] = RecipeLine.objects.filter(recipe__id=self.kwargs['id']).order_by('order_number')
        context['all_ingredients'] = Ingredient.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        for ingredient, name, amount, measurement in zip(
                                                        request.POST.getlist('ingredient_id'),
                                                        request.POST.getlist('ingredient_name'),
                                                        request.POST.getlist('amount'),
                                                        request.POST.getlist('measurement')
                                                    ):
            ingredient_list = get_object_or_404(IngredientList, id=ingredient)
            ingredient_list.ingredient_id = name
            ingredient_list.amount = amount
            ingredient_list.measurement = measurement
            ingredient_list.save()

        for order_number, title, step_description in zip(
                                                        request.POST.getlist('order_number'),
                                                        request.POST.getlist('title'),
                                                        request.POST.getlist('step_description'),
                                                    ):
            step = get_object_or_404(RecipeLine, recipe__id=self.object.id, order_number=order_number)
            step.title = title
            step.discription = step_description
            if request.FILES.get('step_image_' + order_number):
                step.image = request.FILES.get('step_image_' + order_number)
            step.save()

        return result
