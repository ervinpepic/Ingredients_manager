from gzip import READ
from multiprocessing import context
from django.shortcuts import render

from recepies.models import Recipe
from articles.models import Article
# Create your views here.
SEARCH_TYPE_MAPPING = {
    'recipe': Recipe,
    'recipes': Recipe,
    'article': Article,
    'articles': Article,

}
def search_view(request):
    query = request.GET.get('query')
    search_type = request.GET.get('type')
    Klass = Recipe
    if search_type in SEARCH_TYPE_MAPPING.keys():
        Klass = SEARCH_TYPE_MAPPING[search_type]
    qs = Klass.objects.search_for_call_in_views_py(search_query=query)
    context = {
        "queryset": qs
    }
    template = "search/results-view.html"
    if request.htmx:
        context['queryset'] = qs[:5]
        template = "search/snipets/results.html"
    return render(request, template, context)