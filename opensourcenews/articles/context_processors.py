from articles.models import Category

def categories_context(request):
    categories = Category.objects.all()  # Fetch all categories
    return {'full_categories': categories}