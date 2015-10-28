
from django.shortcuts import render

from articles.models import Article, Thumbnail
from textboxes.models import Textbox


def index(request):
    article_list = Article.objects.order_by('-pub_date')
    thumbnail_list = Thumbnail.objects.all()
    textbox_list = Textbox.objects.order_by('-pub_date')
    context = {
        'article_list': article_list,
        'thumbnail_list': thumbnail_list,
        'textbox_list': textbox_list
    }

    return render(request, 'start.html', context)
