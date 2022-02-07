# """
# Render html web pages
# """

# from django.http import HttpResponse
# import random
# from django.template.loader import render_to_string, get_template
# from articles.models import Article

# def home_view(request):
#     """
#     Take in a request (Django sends request) 
#         and return html as a response (We pick to return the response)
#     """
#     # name = "Ervin Pepic"
#     # number = random.randint(1, 4) #some api call with python & python request
    
#     # article_obj = Article.objects.get(id=id)
#     article_list = Article.objects.all()
#     context = {
#         "articles": article_list,
#     }
#     html_string = render_to_string("home-view.html", context)
#     return HttpResponse(html_string)