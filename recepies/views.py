from django.urls import reverse
from django.contrib.auth.decorators import login_required
# basicaly is model form for querysets
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient


@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "recipes_list": qs
    }
    return render(request, "recepies/list.html", context)


@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse("recepies:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "recepies/detail.html", context)

@login_required
def recipe_delete_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    if request.method == "POST":
        print("OBJEKAT JE", obj)
        obj.delete()
        success_url = reverse('recepies:list')
        return redirect(success_url)
    context = {
        "recipe": obj
    }
    return render(request, "recepies/delete.html", context)

@login_required
def recipe_ingredient_delete_view(request, parent_id=None, id=None):
    obj = get_object_or_404(RecipeIngredient, recipe__id=parent_id, id=id, recipe__user=request.user)
    if request.method == "POST":
        print("OBJEKAT JE", obj)
        obj.delete()
        success_url = reverse('recepies:detail', kwargs={"id": parent_id})
        return redirect(success_url)
    context = {
        "recipe": obj
    }
    return render(request, "recepies/delete.html", context)


@login_required
def recipe_detail__hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        recipe = Recipe.objects.get(id=id, user=request.user)
    except:
        recipe = None
    if recipe is None:
        return HttpResponse("Not Found.")
    # recipe = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        "recipe": recipe
    }
    return render(request, "recepies/snipets/detail.html", context)


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
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "recepies/create-update.html", context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    new_ingredient_url = reverse("recepies:hx-ingredient-create", kwargs={"parent_id": obj.id})
    context = {
        "form": form,
        "object": obj,
        "new_ingredient_url": new_ingredient_url
    }
    if form.is_valid():
        form.save()
        context['message'] = "Data is saved!"
    if request.htmx:
        return render(request, 'recepies/snipets/forms.html', context)
    return render(request, "recepies/create-update.html", context)


@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not Found.")
    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    url = reverse("recepies:hx-ingredient-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "recipe": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "recepies/snipets/ingredient-inline.html", context)

    return render(request, "recepies/snipets/ingredient-form.html", context)
