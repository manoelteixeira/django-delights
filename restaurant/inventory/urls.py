from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'inventory'
urlpatterns = [
    path(route='accounts/login/',
         view=auth_views.LoginView.as_view(next_page='inventory:home'),
         name='login'),
    path(route='logout/',
         view=auth_views.LogoutView.as_view(next_page='inventory:login'),
         name='logout'),
    path(route='',  # Index Page
         view=views.homeView.as_view(),
         name='home'),
    path(route='ingredients/',  # Ingredients List
         view=views.IngredientsView.as_view(),
         name='ingredient_list'),
    path(route='ingredient/add/',  # Add Ingredient
         view=views.IngredientCreateView.as_view(),
         name='ingredient_create'),
    path(route='ingredient/<pk>/update/',  # Update Ingredient
         view=views.IngredientUpdateView.as_view(),
         name='ingredient_update'),
    path(route='ingredient/<pk>/delete/',  # Delete Ingredient
         view=views.IngredientDeleteView.as_view(),
         name='ingredient_delete'),
    path(route='menu/',  # Menu Items List
         view=views.MenuItemsView.as_view(),
         name='menu_item_list'),
    path(route='menu/add',  # Add Item to Menu
         view=views.MenuItemCreateView.as_view(),
         name='menu_item_create'),
    path(route='menu/<pk>',  # Menu Item Detail
         view=views.MenuItemDetailView.as_view(),
         name='menu_item_detail'),
    path(route='menu/<pk>/update',  # Update Menu Item
         view=views.MenuItemUpdateView.as_view(),
         name='menu_item_update'),
    path(route='menu/<pk>/delete/',  # Delete Menu Item
         view=views.MenuItemDeleteView.as_view(),
         name='menu_item_delete'),
    path(route='menu/<pk>/ingredient/add/',
         view=views.RecipeRequirementsCreateView.as_view(),
         name='recipe_requirement_create'),
    path(route='menu/<menu_pk>/ingredient/<pk>/update/',
         view=views.RecipeRequirementUpdateView.as_view(),
         name='recipe_requirement_update'),
    path(route='menu/ingredient/<menu_pk>/delete/<pk>/',
         view=views.RecipeRequirementDeleteView.as_view(),
         name='recipe_requirement_delete'),
    path(route='purchases/',
         view=views.PurchasesView.as_view(),
         name='purchase_list'),
    path(route='purchase/add/',
         view=views.PurchaseCreateView.as_view(),
         name='purchase_create'),
]
