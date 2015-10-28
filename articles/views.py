from django.shortcuts import render

from articles.models import Article, Image, Thumbnail


def index(request):
    article_list = Article.objects.order_by('-pub_date')
    thumbnail_list = Thumbnail.objects.all()
    context = {
        'article_list': article_list,
        'thumbnail_list': thumbnail_list
    }

    return render(request, 'articles.html', context)


def article(request, article_id):
    requested_article = Article.objects.get(pk=article_id)
    try:
        image_list = Image.objects.filter(article_id=article_id)
    except Image.DoesNotExist:
        image_list = None
    if image_list:
        return render(request, 'article.html', {
            'article': requested_article,
            'image_list': image_list
        })
    else:
        return render(request, 'article.html', {
            'article': requested_article
        })
