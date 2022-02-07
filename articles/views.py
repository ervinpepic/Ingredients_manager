from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect

from .models import Article
from .forms import ArticleForm

def article_list_view(request):
    article_list = Article.objects.all()
    context = {
        "articles": article_list,
    }
    return render(request, 'articles/list.html', context=context)

def article_detail_view(request, slug=None):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except: 
            raise Http404
    context = {
        "article_obj": article_obj
    }
    return render(request, "articles/detail.html", context=context)

@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        "form": form
    }    
    if form.is_valid():
        article_obj = form.save()
        context['form'] = ArticleForm()
        # return redirect("article-detail", slug=article_obj.slug)
        return redirect(article_obj.get_absolute_url())
    return render(request, "articles/create.html", context=context)
    

def article_search_view(request):
    search_query = request.GET.get("query") #this is a dictionary type of data
    qs = Article.objects.search_for_call_in_views_py(search_query=search_query)
    context = {
        "object_list": qs
        }
    return render(request, "articles/search.html", context)