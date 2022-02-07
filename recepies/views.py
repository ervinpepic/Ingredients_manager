from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory #basicaly is model form for querysets
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "recipes_list" : qs
    }
    return render(request, "recepies/list.html", context)

@login_required
def recipe_detail_view(request, id=None):
    recipe = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        "recipe": recipe
    }
    return render(request, "recepies/detail.html", context)

@login_required
def recipe_create_view(request, id=None):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "recepies/create-update.html", context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    RecipeIngredientFormset = modelformset_factory(
        RecipeIngredient, 
        form=RecipeIngredientForm, 
        extra=0)
    qs = obj.recipeingredient_set.all() #[]
    formset = RecipeIngredientFormset(request.POST or None, queryset=qs)

    context = {
        "form": form,
        "formset": formset,
        "object": obj
    }
    
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.recipe = parent
            child.save()
        context['message'] = "Data is saved!"
        
    return render(request, "recepies/create-update.html", context)