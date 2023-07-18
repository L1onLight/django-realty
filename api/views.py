from django.db.models import Avg
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Item, Favorite, Message, Review
from .decorators import check_auth, check_agent


# from .serializers import PostSerializer, UserSerializer

# Create your views here.
@api_view(["GET"])
def get_routes(request):
    """Get all routes"""
    routes = [
        {'method': 'GET',
         'url': 'api/',
         'def': get_routes.__doc__
         },
        {'method': 'GET',
         'url': 'api/get-average-rating/',
         'def': get_rating.__doc__
         },
        {'method': 'POST',
         'url': 'api/add-fav/<slug:slug>/',
         'def': add_favorite.__doc__
         },
        {'method': 'POST',
         'url': 'api/remove-fav/<slug:slug>/',
         'def': remove_favorite.__doc__
         },
        {'method': 'POST',
         'url': 'api/move-to-archive/<slug:slug>/',
         'def': move_to_archive.__doc__
         },
        {'method': 'POST',
         'url': 'api/remove-from-archive/<slug:slug>/',
         'def': remove_from_archive.__doc__
         },

    ]
    return Response(routes)


@api_view(["GET"])
def get_rating(request):
    """Returns average rating and satisfied(reviews with rating more than 5) user reviews. Returns both 0 if no reviews found."""
    reviews = Review.objects.all()
    if reviews.count() == 0:
        return Response({"rating": "0", "satisfied": "0"})
    av = reviews.aggregate(avg_rating=Avg("rating"))['avg_rating']
    av = round(av, 1)

    context = {"rating": av,
               "satisfied": reviews.filter(rating__gt=5).count()}
    return Response(context)


@api_view(["POST"])
@check_auth
def add_favorite(request, slug):
    """Adds favorite to request.user. Requires user and slug for object."""
    fav, created = Favorite.objects.get_or_create(user=request.user)
    fav.fav_product.add(Item.objects.get(slug=slug))
    return Response({'message': 'Ok'})


@check_auth
@api_view(["POST"])
def remove_favorite(request, slug):
    """Removes favorite from request.user. Requires user and slug for object."""
    if request.method == 'POST':
        fav, created = Favorite.objects.get_or_create(user=request.user)
        fav.fav_product.remove(Item.objects.get(slug=slug))
    return Response({'message': 'Ok'})


@check_agent
@api_view(["POST"])
def move_to_archive(request, slug):
    """Sets message is_archive bool to True. Requires message id and slug for object. Request.user should be agent==True"""

    try:

        msg = Message.objects.get(product__slug=slug, id=request.data['message_id'])
        msg.is_archive = True
        msg.save()
    except Message.DoesNotExist:
        return Response({'message': 'Does Not Exist'}, status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Ok'})


@check_agent
@api_view(["POST"])
def remove_from_archive(request, slug):
    """Sets message is_archive bool to False. Requires message id and slug for object. requires.user should be agent==True"""

    try:
        msg = Message.objects.get(product__slug=slug, id=request.data['message_id'])
        msg.is_archive = False
        msg.save()
    except Message.DoesNotExist:
        return Response({'message': 'Does Not Exist'}, status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Ok'})
