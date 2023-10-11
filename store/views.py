from django.shortcuts import render, get_object_or_404
from .models import Product, ReviewRating
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from django.shortcuts import render, redirect
import joblib
import random
import re

# Create your views here.

def search(request):
    keyword = request.GET.get('keyword')
    if keyword:
        products = Product.objects.order_by('-created_date').filter(
            Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        product_count = products.count()
        context = {
            'products': products,
            'product_count':product_count
        }
    else:
        products = Product.objects.all()
        context = {
            'products': products,
        }
    return render(request, 'store/store.html', context)


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {'products': paged_products, 'product_count': product_count}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
    except Exception as e:
        raise e
    try:
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct = None
    context = {'single_product': single_product,
               'in_cart': in_cart,
               'orderproduct': orderproduct,
               }
    return render(request, 'store/product_detail.html', context)



# Load the SVM model and TF-IDF vectorizer
svm_model = joblib.load('Sentiment_analysis_and_Recomender_system/sentiment_model.joblib')
tfidf_vectorizer = joblib.load('Sentiment_analysis_and_Recomender_system/tfidf_vectorizer.joblib')

# Function to preprocess the input review
def preprocess(user_review):
    if isinstance(user_review, str):
        user_review = re.sub('[^a-zA-Z0-9]', ' ', user_review)
        user_review = re.sub('\s+', ' ', user_review)
        return user_review
    else:
        return str(user_review)

# Function to predict sentiment based on user input
def predict_sentiment(user_review):
    # Preprocess the input review
    user_review = preprocess(user_review)
    # Vectorize the user review using the TF-IDF vectorizer
    user_review_tfidf = tfidf_vectorizer.transform([user_review])
    # Predict using the trained model (SVM in this case)
    prediction = svm_model.predict(user_review_tfidf)
    # Map predicted sentiment to labels
    sentiment_labels = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    predicted_sentiment_label = sentiment_labels[prediction[0]]
    return predicted_sentiment_label

# Function to map sentiment to rating
def map_sentiment_to_rating(sentiment):
    if sentiment == 'Negative':
        return random.uniform(1, 2)  # Assign a random rating between 1 and 2 for negative sentiment
    elif sentiment == 'Neutral':
        return 3  # Assign a fixed rating of 3 for neutral sentiment
    elif sentiment == 'Positive':
        return random.uniform(4, 5)  # Assign a random rating between 4 and 5 for positive sentiment
    else:
        return None

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        user_review = request.POST.get('review', '')  # Get the review from the form

        # Predict sentiment and map to rating
        predicted_sentiment = predict_sentiment(user_review)
        predicted_rating = map_sentiment_to_rating(predicted_sentiment)

        try:
            # Check if the review already exists for the user and product
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)

            # Update the existing review with the new data from the form
            form = ReviewForm(request.POST)
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                data = form.save(commit=False)
                data.sentiment = predicted_sentiment  # Assign predicted sentiment
                data.rating = predicted_rating 
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect(url)

        except ReviewRating.DoesNotExist:
            # Create a new review entry
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.product_id = product_id
                data.user_id = request.user.id
                data.sentiment = predicted_sentiment  # Assign predicted sentiment
                data.rating = predicted_rating  # Assign predicted rating
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

    # Redirect back to the product detail page if the request method is not POST
    return redirect(url)






