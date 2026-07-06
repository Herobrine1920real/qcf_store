from .models import Genre

def genre_list(request):

    return {
        "genres": Genre.objects.all()
    }


def cart_count(request):

    cart = request.session.get("cart", {})

    count = sum(cart.values())

    return {
        "cart_count": count
    }