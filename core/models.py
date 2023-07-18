from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from users.models import CustomUser


# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    itemImg = models.ManyToManyField('Image')
    agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    # # #Item Descriptions
    price = models.IntegerField()
    # Address
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50, )
    state = models.CharField(max_length=50, )
    address = models.CharField(max_length=50, )
    # Other Desc.
    area = models.FloatField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    pets = models.BooleanField(blank=True)
    # Signed
    signed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.slug += f"-{self.id}"
        super(Item, self).save(*args, **kwargs)

    def first_image(self):
        first_img = self.itemImg.first()
        if first_img:
            return first_img
        else:
            return None

    def all_images(self):
        if self.itemImg.all():
            return self.itemImg.all()
        else:
            return None

    def get_absolute_url(self):
        return reverse('item', kwargs={"slug": self.slug})

    def get_agent(self):
        return self.agent


class Image(models.Model):
    img = models.ImageField(upload_to="photos/%Y/%m/%d/")

    def __str__(self):
        return f"{settings.MEDIA_URL}{self.img}"


class Review(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    review = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(10)])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created", "review")

    def __str__(self):
        # return f"{self.user}"
        return f'User: {self.user}. Review: {self.review[:70]}'


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.CharField(max_length=255, blank=True, null=True)
    user_phone = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(Item, on_delete=models.PROTECT)
    message_body = models.TextField()
    is_archive = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        if self.user:
            user = f"User: {self.user}"
        else:
            user = f"Non-reg user: {self.user_email}"
        return f'{user}. Product: {self.product}'

    def get_user(self):
        if self.user:
            return self.user
        else:
            return {"user_name": self.user_name, "user_email": self.user_email, "user_phone": self.user_phone}

    def get_email(self):
        if self.user:
            return self.user.email
        else:
            return self.user_email

    def get_name(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return self.user_name

    def get_phone(self):
        if self.user:
            return self.user.phone
        else:
            return self.user_phone


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fav_product = models.ManyToManyField(Item)

    def __str__(self):
        return f"{self.user}"
