from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.http import Http404
from django.conf import settings
from .forms import PostNewsForm
import json


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        # return render(request, "index.html")
        return redirect("/news/")


class ListNewsPage(View):
    def get(self, request):

        with open(settings.NEWS_JSON_PATH) as file:
            data = json.load(file)

        article = request.GET.get('q')

        if article is not None:
            result = []
            for art in data:
                if article in art.get('title'):
                    result.append(art)

            if result:
                context = {"data": result}
                return render(request, "news.html", context)
            else:
                context = {"data": "not found"}
                return render(request, "news.html", context)

        sorted_data = sorted(data, key=(lambda x: x['created']), reverse=True)
        return render(request, "news.html", {"data": sorted_data})


class NewsPageView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as file:
            data = json.load(file)
        return HttpResponse(f"""<a href='/news/9234732/'> title: {data[0]["title"]}</a>
        """)


class NewsTestPageView(View):
    def get(self, request, post_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as file:
            data = json.load(file)

        for d in data:
            if d['link'] == post_id:
                return render(request, "Article.html", {"data": d})

        raise Http404


def create_news(request):
    form = PostNewsForm(request.POST or None)
    with open(settings.NEWS_JSON_PATH) as file:
        data = json.load(file)

    if form.is_valid():
        article = form.save()
        article['link'] = len(data) + 1
        print(article)
        data.append(article)

        with open(settings.NEWS_JSON_PATH, "w") as f1:
            json.dump(data, f1)

        return redirect("/news/")

    context = {"form": form}
    return render(request, "create_news.html", context)
