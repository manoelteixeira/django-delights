from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .helpers import convert_unit

SOLID_UNIT = [
    ('mg', 'Miligram'),
    ('g', 'Gram'),
    ('kg', 'Kilogram'),
    ('un', 'Unit'),
]

LIQUID_UNIT = [
    ('ml', 'Mililiter'),
    ('l', 'Liter'),
]

UNIT_LIST = SOLID_UNIT + LIQUID_UNIT

# Validators


def menu_item_available(menu_item_id):
    menu_item = MenuItem.objects.get(id=menu_item_id)
    if not menu_item.is_available():
        raise ValidationError(
            _("%(value)s is not available"),
            params={"value": menu_item.name},
        )

# Models


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=2, choices=UNIT_LIST)
    unit_price = models.FloatField(default=0)

    @property
    def type(self):
        if self.unit in [l[0] for l in LIQUID_UNIT]:
            return 'Liquid'
        else:
            return 'Solid'

    def subtract(self, quantity, unit):
        if unit != 'un':
            quantity = convert_unit(quantity, unit_in=unit, unit_out=self.unit)

        self.quantity = self.quantity - quantity
        self.save()

    def __str__(self) -> str:
        # return f'{self.name} - {self.quantity} {self.unit} - ${self.unit_price}/{self.unit}'
        return self.name

    def get_absolute_url(self):
        return '/ingredients/'


class MenuItem(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField(default=0)

    def __str__(self):
        # return f'{self.name} - ${self.price}'
        return f'{self.name}'

    def get_absolute_url(self):
        return '/menu/'

    def get_ingredients(self):
        return self.reciperequirements_set.all()

    def is_available(self):
        return all(item.is_available() for item in self.get_ingredients())

    def get_cost(self):
        cost = 0
        for item in self.get_ingredients():
            if item.unit == 'un':
                cost += (item.quantity * item.ingredient.unit_price)
            else:
                qty = convert_unit(
                    value=item.quantity, unit_in=item.unit, unit_out=item.ingredient.unit)
                cost += (qty * item.ingredient.unit_price)
        return cost


class RecipeRequirements(models.Model):
    menu_item = models.ForeignKey(to=MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=2, choices=UNIT_LIST)

    def is_available(self):
        if self.unit == self.ingredient.unit:
            return self.quantity <= self.ingredient.quantity
        else:
            required_qty = convert_unit(value=self.quantity,
                                        unit_in=self.unit,
                                        unit_out=self.ingredient.unit)
            return required_qty <= self.ingredient.quantity

    def __str__(self) -> str:
        return f'{self.menu_item.name} - {self.ingredient.name}'

    def get_absolute_url(self):
        return f'/menu/{self.menu_item.pk}'


class Purchase(models.Model):
    menu_item = models.ForeignKey(
        to=MenuItem, on_delete=models.CASCADE, validators=[menu_item_available])
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        ingredient_list = self.menu_item.reciperequirements_set.all()
        for item in ingredient_list:
            item.ingredient.subtract(item.quantity, item.unit)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return '/purchases/'

    def __str__(self) -> str:
        return f'{self.menu_item.name} - {self.timestamp.date()}'
