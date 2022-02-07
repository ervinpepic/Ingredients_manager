from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Article.objects.filter(title__icontains=title)
        if qs.exists():
            self.add_error('title', f"\"{title}\" is alerady taken!")
        return data


class ArticleFormOld(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(max_length=255)

    # def clean_title(self):
    #     cleaned_data = self.cleaned_data #this is dict type
    #     title = cleaned_data.get('title')
    #     if title.lower().strip() == "the office":
    #         raise forms.ValidationError("This title is already taken!")
    #     return title

    def clean(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title.lower().strip() == 'empty':
            self.add_error('title', 'this title is not allowed')
        if "empty" in content.lower() or "empty" in title.lower().strip():
            # this error is valid only on the field itslef
            self.add_error(
                'content', "empty is not allowed in the content field")
            # this error is valid on the whole form
            raise forms.ValidationError("Validation error non field")
        return
