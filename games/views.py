from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from .models import Genre
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def home(request):

    query = request.GET.get("search")
    genre_id = request.GET.get("genre")

    games = Game.objects.all()
    featured_games = Game.objects.filter(featured=True)

    if query:
        games = games.filter(
            Q(title__icontains=query) |
            Q(genre__name__icontains=query) |
            Q(platform__icontains=query)
        )

    if genre_id:
        games = games.filter(genre_id=genre_id)
        featured_games = featured_games.filter(genre_id=genre_id)

    return render(request, "home.html", {
        "games": games,
        "featured_games": featured_games,
        "query": query,
        "selected_genre": genre_id,
    })


def game_detail(request, id):
    game = get_object_or_404(Game, id=id)
    return render(request, "game_detail.html", {"game":game })

def add_to_cart(request, id):

    cart = request.session.get("cart", {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session["cart"] = cart

    return redirect("home")

def cart(request):

    cart = request.session.get("cart", {})

    if not cart:
        return render(request, "cart.html", {
            "cart_items": [],
            "total": 0
        })

    games = Game.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for game in games:

        quantity = cart[str(game.id)]
        subtotal = game.price * quantity

        total += subtotal

        cart_items.append({
            "game": game,
            "quantity": quantity,
            "subtotal": subtotal
        })

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })

def genre_games(request, id):

    games = Game.objects.filter(genre_id=id)
    genre = Genre.objects.get(id=id)

    return render(request, "genre.html", {
        "games": games,
        "genre": genre
    })


def base_context(request):
    return {
        "all_genres": Genre.objects.all()
    }

def increase_cart(request, id):

    cart = request.session.get("cart", {})

    cart[str(id)] = cart.get(str(id), 0) + 1

    request.session["cart"] = cart

    return redirect("cart")

def decrease_cart(request, id):

    cart = request.session.get("cart", {})

    if str(id) in cart:

        if cart[str(id)] > 1:
            cart[str(id)] -= 1
        else:
            del cart[str(id)]

    request.session["cart"] = cart

    return redirect("cart")

def remove_from_cart(request, id):

    cart = request.session.get("cart", {})

    if str(id) in cart:
        del cart[str(id)]

    request.session["cart"] = cart

    return redirect("cart")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully. Please log in.",
            )
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(
        request,
        "signup.html",
        {"form": form},
    )


def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("landing_page")


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    return redirect("signup")



def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully. Please log in.",
            )
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(
        request,
        "signup.html",
        {"form": form},
    )


def logout_view(request):
    logout(request)
    return redirect("signup")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")

    return redirect("home")