from django.db import models

class Users(models.Model):
		username = models.CharField(blank=True, max_length=200)
		password = models.CharField(blank=True, max_length=200)

class CategoriesBusiness(models.Model):
		name = models.CharField(blank=True, max_length=200)
		business_id = models.IntegerField(blank=True, null=True)

class Categories(models.Model):
		name = models.CharField(blank=True, max_length=200)
		image = models.CharField(blank=True, max_length=200)
		desc = models.TextField(blank=True)
		active = models.IntegerField(default=1)

class ProductsBusiness(models.Model):
		product_id = models.IntegerField(blank=True, null=True)
		business_id = models.IntegerField(blank=True, null=True)

class Products(models.Model):
		name = models.TextField(blank=True)

class Business(models.Model):
		name = models.CharField(blank=True, max_length=200)
		phone = models.CharField(blank=True, max_length=20)
		alt_phone = models.CharField(blank=True, max_length=20)
		alt2_phone = models.CharField(blank=True, max_length=20)
		gps_lat = models.FloatField(blank=True)
		gps_long = models.FloatField(blank=True)
		description = models.TextField(blank=True)
		website = models.CharField(blank=True, max_length=200)
		featured = models.IntegerField(default=0)
		facebook = models.CharField(blank=True, max_length=200)
		twitter = models.CharField(blank=True, max_length=200)
		email = models.CharField(blank=True, max_length=200)
		take_credit = models.IntegerField(blank=True, default=0)
		created_at = models.DateTimeField(auto_now_add=True)

class BusinessEspanol(models.Model):
		name = models.CharField(blank=True, max_length=200)
		phone = models.CharField(blank=True, max_length=20)
		alt_phone = models.CharField(blank=True, max_length=20)
		alt2_phone = models.CharField(blank=True, max_length=20)
		gps_lat = models.FloatField(blank=True)
		gps_long = models.FloatField(blank=True)
		description = models.TextField(blank=True)
		website = models.CharField(blank=True, max_length=200)
		facebook = models.CharField(blank=True, max_length=200)
		twitter = models.CharField(blank=True, max_length=200)
		email = models.CharField(blank=True, max_length=200)
		products = models.CharField(blank=True, max_length=500)
		take_credit = models.IntegerField(blank=True)
	
class PhotosBusiness(models.Model):
		business_id = models.IntegerField(blank=True)
		photo_name = models.CharField(blank=True, max_length=100)
		directory = models.CharField(blank=True, max_length=200)

class BusinessImages(models.Model):
		business_id = models.IntegerField(blank=True)
		photo_name = models.CharField(blank=True, max_length=300)
		position = models.IntegerField(blank=True, default=0)

class ProductImages(models.Model):
		business_id = models.IntegerField(blank=True)
		photo_name = models.CharField(blank=True, max_length=300)
	
class SearchKeywords(models.Model):
		keyword_phrase = models.CharField(blank=True, max_length=200)
		created_at = models.DateTimeField(auto_now_add=True)

class FishPrices(models.Model):
        fishname_english = models.CharField(blank=True, max_length=64)
        fishname_spanish = models.CharField(blank=True, max_length=64)
        fish_description = models.CharField(blank=True, max_length=254)
        price = models.CharField(blank=True, max_length=16)
        fish_date = models.DateField()

