from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    homepage = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.lower())
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey('contributors.Journalist', on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ForeignKey(Category, related_name="articles", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to='articles/', blank=False, null=False)
    is_published = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)
    is_headline = models.BooleanField(default=False)
    short_description = models.TextField(max_length=300)

    def get_excerpt(self):
        return Truncator(self.content).chars(400)
    
    def get_excerpt_less(self):
        return Truncator(self.content).chars(220)

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="width: 100px; height: auto;" />')
        return "No Image"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title.lower())
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    
    def get_upvotes_count(self):
        return Vote.objects.filter(comment=self, vote_type='upvote').count()

    def get_downvotes_count(self):
        return Vote.objects.filter(comment=self, vote_type='downvote').count()

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"

class Vote(models.Model):
    VOTE_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who voted
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')  # Associated comment
    vote_type = models.CharField(max_length=8, choices=VOTE_CHOICES)  # Type of vote
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures that a user can only vote once per comment
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on comment {self.comment.id}"
