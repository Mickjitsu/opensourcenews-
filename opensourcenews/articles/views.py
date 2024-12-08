from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Article, Comment, Category, Vote

# Create your views here.

def get_date(post):
    return post.get("date")


def index(request):
    categories = Category.objects.all()[:5]  
    article_lists = Article.objects.filter(is_published=True).order_by('-created_at')  
    paginator = Paginator(article_lists, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number) 

    return render(request, 'articles/index.html', {
        "article_lists": article_lists, 
        "categories": categories,
        "page_obj": page_obj
    })


def category_list(request, slug):
    categories = Category.objects.all()
    this_category = next(cat for cat in categories if cat.name == name)
    return render(request, 'articles/categories.html',{
    'categories': this_category})

def single_post(request, slug):
    this_post = get_object_or_404(Article, slug=slug)
    return render(request, 'articles/single_post.html', {
        'post': this_post
    })