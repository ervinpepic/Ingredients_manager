import pint
from django.db import models

from django.conf import settings
from django.urls import reverse

from .validators import validate_unit_of_measure
from .utils import number_str_to_float

User = settings.AUTH_USER_MODEL

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    directions = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("recepies:detail", kwargs={"id": self.id})
    
    def get_update_url(self):
        return reverse("recepies:update", kwargs={"id": self.id})
    
    def get_ingredients_children(self):
        return self.recipeingredient_set.all()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    quantity = models.CharField(max_length=50)
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure])
    directions = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def convert_to_system(self, system='mks'):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        print(measurement)
        return measurement #.to_base_unit()

    # def to_ounces(self):
    #     measurement = self.convert_to_system()
    #     return measurement.to('ounces')

    def as_mks(self):
        #mks means Meter, Kilogram, Second
        measurement = self.convert_to_system(system='mks')
        return measurement.to_base_units()

    def as_imperial(self):
        #imperial means Miles, Pounds, Seconds
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)