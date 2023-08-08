from django.contrib import admin
from .models import Ingredient
from .models import MenuItem
from .models import RecipeRequirements
from .models import Purchase


# InLines
class IngredientInLine(admin.TabularInline):
    model = Ingredient
    extra = 1


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    # extra = 3


class RecipeRequirementsInLine(admin.TabularInline):
    model = RecipeRequirements
    extra = 1

# Admin


class IncredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'unit', 'unit_price']


class RecipeRequirementsAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'ingredient', 'quantity', 'unit']


class MenuItemAdmin(admin.ModelAdmin):
    inlines = [RecipeRequirementsInLine]
    list_display = ['name', 'price']


# Register models here.
admin.site.register(Ingredient, IncredientAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(RecipeRequirements, RecipeRequirementsAdmin)
admin.site.register(Purchase)
