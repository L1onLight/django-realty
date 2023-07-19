from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Pagination settings
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from users.models import CustomUser
from .decorators import *
from .models import Item, Favorite, Message, Image, Review

PAGINATION_COUNT = 12


# PAGINATION_COUNT = 1


def get_items():
    return Item.objects.all()


# Create your views here.
def home(request):
    items = get_items()
    context = {"items": items[:6], 'signed': items.filter(signed=True).count(), }
    return render(request, 'core/index.html', context)


def item(request, slug):
    """Returns the element's page using slug.
    POST method might be used to send a message directly to the real estate agent.
    If no real estate agent is associated with the property, a message is sent to the administrator."""
    # apartment = Item.objects.get(slug=slug)
    apartment = get_object_or_404(Item, slug=slug)
    if request.method == "POST":
        if request.user.is_authenticated:
            message = Message.objects.create(user=request.user, product=apartment,
                                             message_body=request.POST["message"])
        else:
            message = Message.objects.create(user_name=request.POST["name"], user_email=request.POST["email"],
                                             user_phone=request.POST["phone"], product=apartment,
                                             message_body=request.POST["message"])

    fav = False

    if request.user.is_authenticated:
        try:
            fav_ = Favorite.objects.get(user=request.user)
            if apartment in fav_.fav_product.all():
                fav = True
        except Favorite.DoesNotExist or Item.DoesNotExist:
            pass
    # images = apartment.not_first()
    context = {'item': apartment, "fav": fav}

    return render(request, 'core/item.html', context)


def search(request):
    """Requires query from request.GET to filter Item model"""
    query = get_items()
    if request.method == 'GET':
        city = request.GET.get('city')
        street = request.GET.get('street')
        nr = request.GET.get('rooms')
        min_sqm = request.GET.get('sqm_min')
        max_sqm = request.GET.get('sqm_max')
        if city:
            query = query.filter(Q(city__icontains=city))
        if street:
            query = query.filter(Q(address__icontains=street))
        if nr:
            query = query.filter(Q(bedrooms=nr))
        if min_sqm:
            query = query.filter(Q(area__gte=min_sqm))
        if max_sqm:
            query = query.filter(Q(area__lte=max_sqm))

    p = Paginator(query.distinct(), PAGINATION_COUNT)
    paginator_item_list = p.get_page(request.GET.get("page"))
    context = {'paginator_item_list': paginator_item_list, "p_count": PAGINATION_COUNT, "paginator": p}
    # context = {'items': query.distinct()}
    return render(request, 'core/search.html', context)


@login_required_my
def profile(request):
    # user = get_user_model()
    context = {}
    try:
        query = request.GET.get("query") if not "" else None
        favs = Favorite.objects.get(user=request.user).fav_product.all()
        if query:
            favs = favs.filter(Q(title__icontains=query) | Q(city__icontains=query))

        p = Paginator(favs.distinct(), PAGINATION_COUNT)
        favs = p.get_page(request.GET.get("page"))

        context = {'paginator_item_list': favs, "p_count": PAGINATION_COUNT, "paginator": p}

    except Favorite.DoesNotExist:
        pass

    return render(request, 'core/profile.html', context)


@login_required_my
def profile_info(request):
    if request.method == 'POST':
        email = request.POST["email"] if not '' else None
        f_name = request.POST["first_name"] if not '' else None
        l_name = request.POST["last_name"] if not '' else None
        phone = request.POST["phone"] if not '' else None
        if email or f_name or l_name or phone:
            user = CustomUser.objects.get(pk=request.user.pk)
            trigger = False
            if email and email != user.email:
                user.email = email
                trigger = True
            if f_name and f_name != user.first_name:
                user.first_name = f_name
                trigger = True
            if l_name and l_name != user.last_name:
                user.last_name = l_name
                trigger = True
            if phone and phone != user.phone:
                phone = phone.replace("+", '')
                phone = "+" + phone
                user.phone = phone
                trigger = True
            if trigger:
                user.save()
                return redirect('profile_info')
    return render(request, "core/profile-information.html")


@agent_only
def profile_messages(request):
    non_archived = Message.objects.filter(is_archive=False, product__agent=request.user)
    query = request.GET.get("e_phone") if not "" else None
    if query:
        non_archived = non_archived.filter(Q(user_email__icontains=query) | Q(user__email__icontains=query))

    p = Paginator(non_archived, PAGINATION_COUNT)
    paginator_item_list = p.get_page(request.GET.get("page"))
    context = {'paginator_item_list': paginator_item_list, "p_count": PAGINATION_COUNT, "paginator": p}
    return render(request, 'core/profile-messages.html', context)


@agent_only
def profile_archive(request):
    archived = Message.objects.filter(is_archive=True, product__agent=request.user)
    p = Paginator(archived, PAGINATION_COUNT)
    paginator_item_list = p.get_page(request.GET.get("page"))
    context = {'paginator_item_list': paginator_item_list, "p_count": PAGINATION_COUNT, "paginator": p}

    return render(request, 'core/profile-messages-archive.html', context)


@agent_only
def add_object(request):
    if request.method == "POST":
        pets = request.POST.get("pets")
        pets = True if pets == 'on' else False

        image_list = request.FILES.getlist("images")
        obj = Item.objects.create(title=request.POST.get("title"),
                                  body=request.POST.get("body"),
                                  agent=request.user,
                                  published=True,
                                  price=request.POST.get("price"),
                                  country=request.POST.get("country"),
                                  city=request.POST.get("city"),
                                  state=request.POST.get("state"),
                                  address=request.POST.get("address"),
                                  area=request.POST.get("total_area"),
                                  bedrooms=request.POST.get("bedrooms"),
                                  baths=request.POST.get("bathrooms"),
                                  pets=pets,
                                  )

        for image in image_list:
            img_item = Image.objects.create(img=image)
            obj.itemImg.add(img_item)
        obj.save()
        return redirect("item", obj.slug)
    context = {}
    return render(request, "core/profile-add-object.html", context)


@logout_required
def log_in(request):
    if request.method == "POST":
        remember = True if request.POST.get("remember") == "on" else False
        user = auth.authenticate(request, email=request.POST["username"], password=request.POST['password'])
        if user:
            auth.login(request, user)
            if not remember:
                request.session.set_expiry(0)
            return redirect('home')
        else:
            messages.error(request, 'Email or Password does not exist.')
            # context = ''
            # return render(request, "core/login.html", context)

    return render(request, 'core/login.html')


@logout_required
def register(request):
    if request.method == "POST":
        try:
            user = CustomUser.objects.create(email=request.POST['username'], phone=request.POST['phone'],
                                             password=make_password(request.POST.get('password')),
                                             first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            auth.login(request, user)
            return redirect('home')
        except IntegrityError:
            messages.error(request, "Email or Phone already taken.")

    return render(request, 'core/register.html')


def about(request):
    return render(request, 'core/about.html')


def faq(request):
    return render(request, 'core/faq.html')


def privacy(request):
    return render(request, 'core/privacy.html')


def tos(request):
    return render(request, 'core/tos.html')


def log_out(request):
    auth.logout(request)
    return redirect('home')


def reviews(request):
    reviews = Review.objects.all()
    reviewed = False
    if request.user.is_authenticated:
        try:
            reviewed = reviews.filter(user=request.user).first()
            reviews = reviews.exclude(id=reviewed.id)

        except Review.DoesNotExist:
            pass
        except AttributeError:
            pass
        if request.method == "POST" and request.user.is_authenticated:
            edit_form = request.POST.get("review_body_edit")
            rating = request.POST.get("rating")
            usual_form = request.POST.get("review_body")
            if edit_form and rating:
                reviewed.review = edit_form
                reviewed.rating = rating
                reviewed.save()
            elif usual_form and rating:
                if reviewed:
                    return redirect("reviews")
                review = Review.objects.create(user=request.user, review=usual_form, rating=rating)
            return redirect("reviews")
    p = Paginator(reviews, PAGINATION_COUNT)
    paginator_item_list = p.get_page(request.GET.get("page"))
    context = {'paginator_item_list': paginator_item_list, "p_count": PAGINATION_COUNT, "paginator": p,
               'reviewed': reviewed}
    return render(request, "core/reviews.html", context)
