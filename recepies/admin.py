from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import RecipeIngredient, RecipeIngredientImage, Recipe

User = get_user_model()


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['quantity_as_float',
                       'as_mks', 'as_imperial']  # 'to_ounces'#
    # fields = ['name', 'quantity', 'unit', 'direction']


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredientImage)
