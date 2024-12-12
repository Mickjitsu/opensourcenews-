from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.core.paginator import Paginator
from .models import Article, Comment, Category, Vote
from contributors.models import Journalist
# Create your views here.

def get_date(post):
    return post.get("date")


def index(request):
    categories = Category.objects.all()[:5]  
    full_categories = Category.objects.all()
    article_lists = Article.objects.filter(is_published=True).order_by('-created_at')  
    paginator = Paginator(article_lists, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number) 
    breaking_article = Article.objects.filter(is_breaking=True).order_by('-created_at').first()

    return render(request, 'articles/index.html', {
        "article_lists": article_lists, 
        "full_categories": full_categories,
        "categories": categories,
        "page_obj": page_obj,
        'breaking_article': breaking_article,
    })


def category_list(request, slug):
    categories = Category.objects.all()
    full_categories = Category.objects.all()
    posts = Article.objects.all()
    this_category = next(cat for cat in categories if cat.slug == slug)
    relevant_posts = posts.filter(category=this_category)
    return render(request, 'articles/category.html', {
    'full_categories': full_categories,
    'posts': relevant_posts,    
    'categories': this_category
    })

def single_post(request, slug):
    this_post = get_object_or_404(Article, slug=slug)
    full_categories = Category.objects.all()
    this_journalist = this_post.created_by
    user = this_journalist.user
    journalist_first_name = this_journalist.first_name
    journalist_last_name = this_journalist.last_name
    journalist_bio = this_journalist.bio
    journalist_image = this_journalist.profile_picture.url

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  
            comment.article = this_post 
            comment.save()  
            return redirect('single-post', slug=this_post.slug)  

    else:
        form = CommentForm()

    return render(request, 'articles/single_post.html', {
        'full_categories': full_categories,
        'post': this_post,
        'form': form,
        'journalist_image': journalist_image,
        'journalist': user,
        'journalist_bio': journalist_bio,
        'first_name': journalist_first_name,
        'last_name': journalist_last_name
    })

@login_required
@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)
    
    
    if comment.author != request.user:
        return redirect('single-post', slug=comment.article.slug) 
    
   
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()  
            return redirect('single-post', slug=comment.article.slug)  
    else:
        form = CommentForm(instance=comment)  

    return render(request, 'articles/edit_comment.html', {
        'form': form,
        'comment': comment,
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    
    if comment.author != request.user:
        return redirect('single-post', slug=comment.article.slug)  

    comment.delete()  

    return redirect('single-post', slug=comment.article.slug) 

@login_required
def upvote_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    user = request.user

    # Check if the user has already voted
    existing_vote = Vote.objects.filter(user=user, comment=comment).first()

    if existing_vote:
        if existing_vote.vote_type == 'downvote':
            # Change from downvote to upvote
            existing_vote.vote_type = 'upvote'
            existing_vote.save()
    else:
        # Create a new vote if none exists
        Vote.objects.create(user=user, comment=comment, vote_type='upvote')

    # Update upvotes and downvotes count
    upvotes = comment.votes.filter(vote_type='upvote').count()
    downvotes = comment.votes.filter(vote_type='downvote').count()

    # Save the updated vote counts to the comment
    comment.upvotes = upvotes
    comment.downvotes = downvotes
    comment.save()

    return JsonResponse({'upvotes': upvotes, 'downvotes': downvotes})

@login_required
def downvote_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    user = request.user

    # Check if the user has already voted
    existing_vote = Vote.objects.filter(user=user, comment=comment).first()

    if existing_vote:
        if existing_vote.vote_type == 'upvote':
            # Change from upvote to downvote
            existing_vote.vote_type = 'downvote'
            existing_vote.save()
    else:
        # Create a new vote if none exists
        Vote.objects.create(user=user, comment=comment, vote_type='downvote')

    # Update upvotes and downvotes count
    upvotes = comment.votes.filter(vote_type='upvote').count()
    downvotes = comment.votes.filter(vote_type='downvote').count()

    # Save the updated vote counts to the comment
    comment.upvotes = upvotes
    comment.downvotes = downvotes
    comment.save()

    return JsonResponse({'upvotes': upvotes, 'downvotes': downvotes})
