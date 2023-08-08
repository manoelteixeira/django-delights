from django import forms
from .models import Ingredient
from .models import MenuItem
from .models import RecipeRequirements
from .models import Purchase


# Forms


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'


class RecipeRequirementsForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirements
        fields = ['ingredient', 'quantity', 'unit']


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
