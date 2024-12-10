from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views


urlpatterns = [
     path("", views.index, name="index"),
     path("topic/<slug:slug>", views.category_list , name = "category-list"),
     path("article/<slug:slug>", views.single_post, name="single-post"),
     path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit-comment'),
     path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete-comment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)