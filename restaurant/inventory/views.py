from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db.models import Sum
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Ingredient, MenuItem, RecipeRequirements, Purchase
from .forms import IngredientForm, MenuItemForm, RecipeRequirementsForm, PurchaseForm

# Create your views here.


class homeView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.all()
        context['purchases'] = Purchase.objects.order_by('-timestamp')
        return context


class IngredientsView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'invenotory/ingredient_list.html'


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_create.html'


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    context_object_name = 'ingredient'
    template_name = 'inventory/ingredient_update.html'


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    context_object_name = 'ingredient'
    template_name = 'inventory/ingredient_delete.html'
    success_url = '/ingredients'


class MenuItemsView(LoginRequiredMixin, ListView):
    model = MenuItem
    context_object_name = 'menu_item_list'
    template_name = 'inventory/menu_item_list.html'


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/menu_item_create.html'


class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    context_object_name = 'menu_item'
    template_name = 'inventory/menu_item_update.html'


class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    context_object_name = 'menu_item'
    template_name = 'inventory/menu_item_delete.html'
    success_url = '/menu'


class MenuItemDetailView(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = 'inventory/menu_item_detail.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context['ingredients_requirements'] = context['menuitem'].reciperequirements_set.all()
        context['ingredients_requirements'] = context['menuitem'].get_ingredients()
        return context


class RecipeRequirementsCreateView(LoginRequiredMixin, CreateView):
    model = RecipeRequirements
    form_class = RecipeRequirementsForm
    template_name = 'inventory/recipe_requirement_create.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['item'] = MenuItem.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.menu_item = MenuItem.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


class RecipeRequirementUpdateView(LoginRequiredMixin, UpdateView):
    model = RecipeRequirements
    form_class = RecipeRequirementsForm
    template_name = 'inventory/recipe_requirement_update.html'


class RecipeRequirementDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipeRequirements
    context_object_name = 'item'
    template_name = 'inventory/recipe_requirement_delete.html'

    def get_success_url(self) -> str:
        return reverse('inventory:menu_item_detail',
                       kwargs={
                           'pk': self.kwargs['menu_pk']
                       })


class PurchasesView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context['purchases'] = Purchase.objects.all()
        context['purchases'] = Purchase.objects.order_by("timestamp")
        revenue = Purchase.objects.aggregate(
            total=Sum('menu_item__price'))['total']
        context['revenue'] = revenue
        cost = 0
        for item in Purchase.objects.all():
            cost += item.menu_item.get_cost()
        context['total_cost'] = cost
        context['profit'] = revenue - cost
        return context


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase_create.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # print(form.data)
        return super().form_valid(form)
