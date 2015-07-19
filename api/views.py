from django.shortcuts import render, redirect
import datetime
import time
import json
import os
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from admin.models import *
from django.db import connection
import random

def index(request):
		print_this = request.GET['test']
		return HttpResponse('Default Index Page ' + print_this)

@csrf_exempt
def add_business(request):
		if request.method == "POST":
				bName = request.POST['bName']
				desc = request.POST['bDesc']
				phone = request.POST['bPhone']
				alt_phone = request.POST['bAltPhone']
				alt_phone2 = request.POST['bAltPhone2']
				cat1 = request.POST['bCategory']
				lon = request.POST['bLon']
				lat = request.POST['bLat']
				website = request.POST['bWebsite']
				facebook = request.POST['facebook']
				twitter = request.POST['twitter']
				take_credit = request.POST['bTakeCredit']
				email = request.POST['bEmail']
				products = request.POST['bProducts']
				if products.find(","):
						products = request.POST['bProducts'].split(",")
						loggit(products)
				bid = add_business_info(bName, desc, lon, lat, website, phone, alt_phone, alt_phone2, email, facebook, twitter, take_credit)
				if bid:
						add_cat = add_to_cat(bid, cat1) 
				if products and bid:
						update_products(bid, products)
						
				return HttpResponseRedirect('http://api.sjdsdirectory.com/admin')
		return HttpResponse('http://api.sjdsdirectory.com/admin')

@csrf_exempt
def update_business(request):
		if request.method == "POST":
				bName = request.POST['bName']
				desc = request.POST['bDesc']
				phone = request.POST['bPhone']
				alt_phone = request.POST['bAltPhone']
				alt_phone2 = request.POST['bAltPhone2']
				cat1 = request.POST['bCategory']
				lon = request.POST['bLon']
				lat = request.POST['bLat']
				website = request.POST['bWebsite']
				facebook = request.POST['facebook']
				twitter = request.POST['twitter']
				take_credit = request.POST['bTakeCredit']
				if not take_credit:
						take_credit = 0
				email = request.POST['bEmail']
				bid = request.POST['hidden-bid']
				products = request.POST['bProducts']
				if products.find(","):
						products = request.POST['bProducts'].split(",")
						loggit(products)
				update_business_info(bid, bName, desc, lon, lat, website, phone, alt_phone, alt_phone2, email, facebook, twitter, take_credit)
				if bid:
						update_to_cat(bid, cat1) 
				if products and bid:
						update_products(bid, products)
				if request.FILES:
						update_photos(request, bid)
				return HttpResponseRedirect('/admin/')
		return HttpResponse('2')

def update_products(bid, products):
		''' products should be seperated by commas and inputted
			into the db '''
		# Delete all related products first then add them back
		del_prod = ProductsBusiness.objects.filter(business_id=bid)
		del_prod.delete()
		for p in products:
				prod = Products.objects.filter(name=p.strip())
				if len(prod) < 1:
						pEntry = Products(name=p.strip())
						pEntry.save()
						prodid = pEntry.id
				else:
						prodid = prod[0].id
				pc = ProductsBusiness.objects.filter(business_id=bid).filter(product_id=prodid)
				if len(pc) < 1:
						add_pc = ProductsBusiness(business_id=bid, product_id=prodid)
						add_pc.save()

def update_photos(request, bid):
		""" Up to four business photos can be processed here.  There are four positions and the file'#' matters """
		for i in range(1,5):
				if request.FILES.has_key('file%s' % i):
						name = request.FILES['file%s' % i].name
						add_photo_to_db(name, i, bid)
						handle_uploaded_file(request.FILES['file%s' % i], name, bid)


def add_photo_to_db(file, i, bid):
		p = BusinessImages.objects.filter(business_id=bid).filter(position=i)
		if p:
				p[0].photo_name = file
				p[0].position = i
				p[0].save()
		else:
				p = BusinessImages(business_id=bid, position=i, photo_name=file)
				p.save()

def handle_uploaded_file(f, name, bid):
		target_folder = check_for_folder(bid)
		with open('%s/%s' % (target_folder, name), 'wb+') as destination:
				for chunk in f.chunks():
						destination.write(chunk)

def check_for_folder(bid):
		base_folder = '/www/sites/sjdsdirectory/media/business_images/'
		target_folder = base_folder + bid
		if not os.path.exists(target_folder):
				os.makedirs(target_folder, 0775)
		return target_folder

def update_business_info(bid, bName, desc, lon, lat, bWebsite, phone, alt_phone, alt_phone2, email, facebook, twitter, take_credit):
		b = Business.objects.get(pk=bid)
		b.name = bName
		b.description = desc
		b.gps_long = lon
		b.gps_lat = lat
		b.website = bWebsite
		b.facebook = facebook
		b.twitter = twitter
		b.take_credit = take_credit
		b.phone = phone
		b.alt_phone = alt_phone
		b.alt2_phone = alt_phone2
		b.email = email
		b.save()


def add_business_info(bName, desc, lon, lat, bWebsite, phone, alt_phone, alt_phone2, email, facebook, twitter, take_credit):
		b = Business(name=bName, description=desc, gps_long=lon, gps_lat=lat, website=bWebsite, phone=phone, alt_phone=alt_phone, alt2_phone=alt_phone2, email=email, facebook=facebook, twitter=twitter, take_credit=take_credit)
		b.save()
		return b.id

@csrf_exempt
def get_one_business(request):
		if request.method == 'GET':
				biz = get_business(request.GET['id'])
				biz_json = json.dumps(biz)
				return HttpResponse(biz_json)
		return 0

def get_photos(bid):
		""" Retrieves related photos to business """
		photoList = []
		photos = BusinessImages.objects.filter(business_id=bid)
		for p in photos:
				photoList.append(p.photo_name)
		return photoList

def get_products(bid):
		""" Retrieves products for a specific business """
		sql = 'select p.id, p.name from admin_products p right join admin_productsbusiness pb on pb.product_id = p.id where pb.business_id = %s'
		products = ProductsBusiness.objects.raw(sql, bid)
		prod = []
		for p in products: 
				prod.append(p.name)
		return prod
				
def get_business(bid):
		b = Business.objects.get(pk=bid)
		c = CategoriesBusiness.objects.filter(business_id=bid)
		cat = {}
		if c:
				cat['id'] = c[0].business_id
				catname = Categories.objects.get(pk=c[0].name)
				cat['name'] = catname.name
		prod = get_products(bid)
		pics = get_photos(bid)
		biz = {}
		biz['id'] = bid
		biz['name'] = b.name
		biz['phone'] = b.phone
		biz['alt_phone'] = b.alt_phone
		biz['alt2_phone'] = b.alt2_phone
		biz['email'] = b.email
		biz['description'] = b.description
		biz['gps_long'] = b.gps_long
		biz['gps_lat'] = b.gps_lat
		biz['website'] = b.website
		biz['facebook'] = b.facebook
		biz['twitter'] = b.twitter
		biz['take_credit'] = b.take_credit
		biz['cat_info'] = cat
		biz['products'] = prod
		biz['photos'] = pics
		return biz

def update_to_cat(bid, cat1):
		c = CategoriesBusiness.objects.filter(name=cat1).filter(business_id=bid)
		if c:
				c.name = cat1
				c[0].save()
		else:
				c = CategoriesBusiness(business_id=bid, name=cat1)
				c.save()
		return 1


def add_to_cat(bid, cat1):
		if cat1:
				cb = CategoriesBusiness(business_id=bid, name=cat1)
				cb.save()
		return 1

def get_categories_for_biz(bid):
		cat = Categories.objects.raw("select c.id, c.name from admin_categories c Inner Join admin_categoriesbusiness cb on cb.name = c.id where cb.business_id = %s" % bid)

def generate_catlist():
		# Generates a list of available categories
		cat = Categories.objects.all().distinct()
		cats = {}
		i = 0
		for c in cat:
				cats[c.id] = c.name
				i += 1
		cats_json = json.dumps(cats)	
		return cats_json

def generate_catfull():
		cat = Categories.objects.all().distinct()
		cats = {}
		for c in cat:
				cats[c.id] = {}
				cats[c.id]['name'] = c.name
				cats[c.id]['cid'] = c.id
				cats[c.id]['desc'] = c.desc
				cats[c.id]['image'] = c.image
		cats_json = json.dumps(cats)
		return cats_json

def generate_catlist_for_biz(bid):
		""" Return categories for one business """
		cats = CategoriesBusiness.objects.filter(business_id=bid)
		cat_list = []
		for cid in cats:
				catname = Categories.objects.get(pk=cid.name) 
				cat_list.append(catname.name)
		return cat_list
				
def generate_catlist_with_biz():
		""" Return only categories that have a related business """
		cat = Categories.objects.all().distinct()
		cat = Categories.objects.raw("select c.id, c.name, c.desc, c.image from admin_categories c Inner Join admin_categoriesbusiness cb on cb.name = c.id")
		cats = {}
		for c in cat:
				cats[c.id] = {}
				cats[c.id]['name'] = c.name
				cats[c.id]['cid'] = c.id
				cats[c.id]['desc'] = c.desc
				cats[c.id]['image'] = c.image
		cats_json = json.dumps(cats)
		return cats_json

@csrf_exempt
def get_full_categories(request):
		cats_json = generate_catfull()
		return HttpResponse(cats_json)
		
def get_categories(request):
		cats_json = generate_catlist()
		return HttpResponse(cats_json)

@csrf_exempt
def get_categories_for_biz(request):
		catlist_json = ''
		if request.method == "POST":
				bid = request.POST['bid']
				c = CategoriesBusiness.objects.filter(business_id=bid)

				
		return HttpResponse(catlist_json)

@csrf_exempt
def get_business_category(request, category=None):
		bizs = {}
		if category:
				cat = Categories.objects.filter(name=category)
				if cat: 
						cb = CategoriesBusiness.objects.raw('Select b.id, b.name from admin_business b Inner Join admin_categoriesbusiness cb on cb.business_id = b.id where cb.name = %s' % cat[0].id)
						for biz in cb:
								bizs[biz.id] = {}
								bizs[biz.id] = biz.name
		biz_json = json.dumps(bizs)
		return HttpResponse(biz_json)
		
def product_lookup(request, product_id=None):
		if product_id:
				try:
						int(product_id)
				except:
						prod = Products.objects.filter(name=product_id)
						if prod:
								product_id = prod[0].id 
				bizs = Business.objects.raw("select b.id, b.name, b.description from admin_business b Right Join admin_productsbusiness pb on b.id = pb.business_id where pb.product_id = '%s'" % product_id) 
				biz = {}
				for b in bizs:
						biz[b.id] = {}
						biz[b.id]['id'] = b.id 
						biz[b.id]['name'] = b.name
						biz[b.id]['description'] = b.description
						biz[b.id]['photos'] = get_photos(b.id)
				biz_json = json.dumps(biz)
				return HttpResponse(biz_json)
						

def category_lookup(request, category_name=None):
		start_time = time.time()
		if category_name:
				cat = Categories.objects.filter(name=category_name)
				if cat:
						catid = cat[0].id
						cb = Business.objects.raw('Select b.id, b.name from admin_business b Inner Join admin_categoriesbusiness cb on cb.business_id = b.id where cb.name = %s', catid)
						biz = {}
						if cb:
								for b in cb:
										biz[b.id] = {}
										biz[b.id]['id'] = b.id 
										biz[b.id]['name'] = b.name
										biz[b.id]['description'] = b.description
										biz[b.id]['photos'] = get_photos(b.id)
				biz_json = json.dumps(biz)
				end_time = time.time()-start_time
				time_info = {}
				time_info['time'] = end_time
				time_json = json.dumps(time_info)
				all_info = {}
				all_info['results'] = biz
				all_info['time'] = time_info
				all_info['count'] = len(biz)
				full_json = json.dumps(all_info)
				return HttpResponse(full_json)

@csrf_exempt
def add_category(request):
		if request.method == "POST":
				c = Categories(name=request.POST['cName'], desc=request.POST['cDesc'], image=request.POST['cFawesome'])
				c.save()
				return HttpResponse('updated')
		return HttpResponse('false')

@csrf_exempt
def delete_category(request):
		if request.method == "POST":
				id = request.POST['cid']
				try:
						c = Categories.objects.get(pk=id)
						c.delete()
				except:
						pass
		cats = generate_catlist()
		return HttpResponse(cats)

def get_category(cid):
		try:
				c = Categories.objects.get(pk=cid)
		except:
				c = 0
		return c

@csrf_exempt
def edit_category(request):
		if request.method == 'POST':
				cid = request.POST['cid']
				c  = get_category(cid)
				cat_info = {}
				if c:
						cat_info['cid'] = c.id
						cat_info['name'] = c.name
						cat_info['image'] = c.image
						cat_info['desc'] = c.desc
						cat_info['active'] = c.active
						cat_info_json = json.dumps(cat_info)
						return HttpResponse(cat_info_json)
		return HttpResponse('0')

@csrf_exempt
def update_category(request):
		if request.method == 'POST':
				cid = request.POST['cid']
				c  = get_category(cid)
				if c:
						c.name = request.POST['cName']
						c.desc = request.POST['cDesc']
						c.image = request.POST['cFawesome']
						c.save()
						return HttpResponse('1')
				return HttpResponse('2')
		return HttpResponse('0')

def search_businesses(keyword):
		if keyword.find(" ") > 0:
				#results = Business.objects.raw('select id, name from admin_business where match(name, description) against("%s")' % keyword)
				results = Business.objects.filter(name__icontains=keyword).order_by('name')[:3]
		else:
				results = Business.objects.filter(name__icontains=keyword).order_by('name')[:3]
		return results

def search_products(keyword):
		keyword = "%" + keyword + "%"
		products_sql = 'select b.product_id, p.name from admin_products p inner join admin_productsbusiness b on p.id = b.product_id where p.name like %s order by p.name asc limit 0,8'
		cursor = connection.cursor()
		cursor.execute(products_sql, keyword)
		products = cursor.fetchall()
		product_list = []
		for p in products:
				if (p[0],p[1]) not in product_list:
						product_list.append((p[0], p[1]))
				if len(product_list) >= 3:
						break
		return product_list

def search_all(keyword):
		keyword = '%' + keyword + '%'
		Sql = "select id, name, description from admin_business where id in (select b.business_id from admin_products a inner join admin_productsbusiness b on b.product_id = a.id where a.name like %s) or name like %s"
		cursor = connection.cursor()
		cursor.execute(Sql, (keyword,keyword))
		prods = cursor.fetchall()
		return prods

def save_keyword(keyword):
		s = SearchKeywords(keyword_phrase=keyword)
		s.save()

@csrf_exempt
def search_result(request):
		''' Test the keyword against the business table name and description columns as well as the product table looking for the best match '''
		if request.method == 'GET':
				keyword = request.GET['keyword']
				save_keyword(keyword)
				result = {} #create result dict
				i=0
				results = search_all(keyword)
				biz = {}
				for r in results:
						biz[i] = {}
						biz[i]['id'] = r[0]
						biz[i]['name'] = r[1]
						biz[i]['description'] = r[2]
						biz[i]['photos'] = get_photos(r[0])
						i = i+1
				biz_json = json.dumps(biz)
				return HttpResponse(biz_json) 
		
@csrf_exempt
def search(request):
		''' Test the keyword against the database looking for the best match '''
		if request.method == 'POST':
				keyword = request.POST['keyword']
				result = {}
				i=0
				results = search_businesses(keyword)
				products = search_products(keyword)
				for r in results:
						result[i] = {}
						result[i]['id'] = r.id
						result[i]['name'] = r.name
						i=i+1
				prods = {}
				i=0
				for p in products:
						prods[i] = {}
						prods[i]['id'] = p[0]
						prods[i]['name'] = p[1]
						i=i+1
				all_results = {}
				all_results['prods'] = prods
				all_results['results'] = result 
				all_results['keyword'] = keyword
				res_json = json.dumps(all_results)
				#prod_json = json.dumps(prods)
				return HttpResponse(res_json)
		return HttpResponse('None')

def generate_bizfull():
		biz = Business.objects.all()
		bizs = {}
		for b in biz:
				bizs[b.id] = {}
				b = bizs[b.id]
				b['name'] = b.name
		return cats_json

def get_full_businesses(request):
		cats_json = generate_catfull()
		return HttpResponse(cats_json)

def get_businesses_order(request):
		''' Get all business and order them by name '''
		biz = Business.objects.all().order_by('name')
		bizs = {}
		i = 0
		for b in biz:
				bizs[i] = {}
				bizs[i]['name'] = b.name
				bizs[i]['id'] = b.id
				i = i+1
		bizs['count'] = i
		biz_json = json.dumps(bizs)
		return HttpResponse(biz_json)
		
def get_businesses(request):
		biz = Business.objects.all()
		bizs = {}
		for b in biz:
				bizs[b.id] = b.name
		biz_json = json.dumps(bizs)
		return HttpResponse(biz_json)

def get_featured_biz():
		fBiz = Business.objects.filter(featured=1)
		fBizs = {}
		for b in fBiz:
				fBizs[b.id] = b.name
		return fBizs 

def not_featured_biz():
		not_featured_biz = Business.objects.filter(featured=0)
		nfBizs = {}
		for nf in not_featured_biz:
				nfBizs[nf.id] = nf.name
		return nfBizs

def get_featured_businesses(request):
		bizs = {}
		bizs['featured'] = get_featured_biz()
		bizs['not_featured'] = not_featured_biz()
		biz_json = json.dumps(bizs)
		return HttpResponse(biz_json)

def get_number_featured_biz(request, num_of_biz=0):
		if num_of_biz:
				D = get_featured_biz()
				biz_list = {}
				i = 0
				for k,v in D.items():
						biz_list[i] = get_business(k) 
						i = i+1
				if int(num_of_biz) > len(D):
						num_of_biz = len(D)
				dList = random.sample(biz_list.items(), int(num_of_biz))
				dList_json = json.dumps(dList)
		return HttpResponse(dList_json)
		

def update_featured_business(request, bid):
		b = Business.objects.get(pk=bid)
		if b.featured == 0:
				b.featured = 1
		else:
				b.featured = 0
		b.save()
		return HttpResponseRedirect('/admin/manage_featured/') 
		
@csrf_exempt
def edit_business(request):
		if request.method == 'POST':
				bid = request.POST['bid']
				business = get_business(bid)
				business_json = json.dumps(business)
				return HttpResponse(business_json)
		return HttpResponse('0')

def loggit(msg):
		msg = str(msg)
		cTime = datetime.datetime.now()
		logtime = cTime.strftime("%H:%M:%S")
		logfile = "/www/sites/sjdsdirectory/sjdsdirectory/logfile.log"
		with open(logfile, "a") as log:
				log.write(logtime + ": " + msg)
				log.close()

def category_search(request, category=None):
		if not category == None:
				# do a earch for a category
				businesses = Categories.objects.raw("select ")
		return HttpResponse('0')

@csrf_exempt
def add_business_es(request):
		if request.method == "POST":
				bName = request.POST['bName']
				desc = request.POST['bDesc']
				phone = request.POST['bPhone']
				alt_phone = request.POST['bAltPhone']
				alt_phone2 = request.POST['bAltPhone2']
				lon = request.POST['bLon']
				lat = request.POST['bLat']
				website = request.POST['bWebsite']
				email = request.POST['bEmail']
				products = request.POST['bProducts']
				credit = request.POST['bTakeCredit']
				facebook = request.POST['facebook']
				twitter = request.POST['twitter']
				check = BusinessEspanol.objects.filter(name=bName)
				if check:
						return HttpResponse('0')
				dblcheck = BusinessEspanol.objects.filter(gps_lat=lat).filter(gps_long=lon)
				if dblcheck:
						return HttpResponse('2')
				b = BusinessEspanol(name=bName, description=desc, gps_long=lon, gps_lat=lat, website=website, phone=phone, alt_phone=alt_phone, alt2_phone=alt_phone2, email=email, products=products, take_credit=credit, facebook=facebook, twitter=twitter)
				b.save() 
				if request.FILES:
						add_pics(b.id, request)
				return HttpResponseRedirect('http://api.sjdsdirectory.com/admin/espanol')
		return HttpResponse('0')

def add_pics(bid, request):
		for i in range(1,5):
			try:
					if request.FILES['bPic%s' % i]:
							add_pic(request.FILES['bPic%s' % i])
							add_pic_db(request.FILES['bPic%s' % i], bid)
			except:
					pass

def add_pic_db(filename, bid):
		p = PhotosBusiness(business_id=bid, photo_name=filename)
		p.save()

def add_pic(picture):
		with open('/www/sites/sjdsdirectory/media/business_images/%s' % picture, 'wb+') as destination:
				for chunk in picture.chunks():
						destination.write(chunk)

def get_businesses_es(request):
		biz = BusinessEspanol.objects.all()
		bizs = {}
		for b in biz:
				bizs[b.id] = b.name
		biz_json = json.dumps(bizs)
		return HttpResponse(biz_json)

@csrf_exempt
def edit_business_es(request):
		if request.method == 'POST':
				bid = request.POST['bid']
				business = get_business_es(bid)
				business_json = json.dumps(business)
				return HttpResponse(business_json)
		return HttpResponse('000')

		
def get_business_es(bid):
		b = BusinessEspanol.objects.get(pk=bid)
		c = CategoriesBusiness.objects.filter(business_id=bid)
		cat = {}
		if c:
				cat['id'] = c[0].business_id
				catname = Categories.objects.get(pk=c[0].name)
				cat['name'] = catname.name
		#sql = 'select p.id, p.name from admin_products p right join admin_productsbusiness pb on pb.product_id = p.id where pb.business_id = %s' % bid
		sql = 'select * from admin_businessespanol where id = %s' % bid
		biz = {}
		biz['id'] = bid
		biz['name'] = b.name
		biz['phone'] = b.phone
		biz['alt_phone'] = b.alt_phone
		biz['alt2_phone'] = b.alt2_phone
		biz['email'] = b.email
		biz['description'] = b.description
		biz['gps_long'] = b.gps_long
		biz['gps_lat'] = b.gps_lat
		biz['website'] = b.website
		biz['products'] = b.products
		biz['facebook'] = b.facebook
		biz['twitter'] = b.twitter
		return biz

@csrf_exempt
def delete_business_es(request):
		if request.method == "POST":
				bid = request.POST['bid']
				b = BusinessEspanol.objects.get(id=bid)
				b.delete()
				p = PhotosBusiness.objects.filter(business_id=bid)
				p.delete()
				return HttpResponseRedirect('1')
		return HttpResponseRedirect('0')

@csrf_exempt
def translate_business(request):
		""" Take the spanish version of the business and create an english version """
		if request.method == "POST":
				bid_es = request.POST['hidden-bid']
				biz_name = request.POST['bName']
				biz_es = BusinessEspanol.objects.get(pk=bid_es)
				b = Business.objects.filter(name=biz_name)
				products = request.POST['nProducts']
				nDesc = request.POST['nDesc']
				categories = [request.POST['cat1'], request.POST['cat3'], request.POST['cat4']]
				# Update Spanish
				
				if not b:
						bid = add_business_info(biz_es.name, nDesc, biz_es.gps_long, biz_es.gps_lat, biz_es.website, biz_es.phone, biz_es.alt_phone, biz_es.alt2_phone, biz_es.email, biz_es.facebook, biz_es.twitter, biz_es.take_credit)
				else:
						bid = b[0].id
				for cat in categories:
						if bid: #add category
								update_to_cat(bid, cat) 
				if products.find(","):
						products = request.POST['nProducts'].split(",")
				if products and bid:
						update_products(bid, products)
				biz_es.description = request.POST['bDesc']
				biz_es.products = request.POST['bProducts']
				biz_es.save()
		return HttpResponseRedirect('/admin/translate')

@csrf_exempt
def get_english_from_name(request):
		bizDict = {}
		if request.method == "POST":
				biz_name = request.POST['biz_name']
				biz = Business.objects.filter(name=biz_name)
				if biz:
						bizDict['description'] = biz[0].description
						bizDict['products'] = get_products(biz[0].id)
		biz_json = json.dumps(bizDict)
		return HttpResponse(biz_json)
