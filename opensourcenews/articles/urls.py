from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views


urlpatterns = [
     path("", views.index, name="index"),
     path("topic/<slug:slug>", views.category_list , name = "category-list"),
     path("article/<slug:slug>", views.single_post, name="single-post"),
     path('comment/<int:comment_id>/upvote/', views.upvote_comment, name='upvote_comment'),
     path('comment/<int:comment_id>/downvote/', views.downvote_comment, name='downvote_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)