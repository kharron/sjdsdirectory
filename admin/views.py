from django.shortcuts import render, redirect
import datetime
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from admin.models import *

def index(request):
		context = {}
		return render(request, 'admin/admin.html', context)

def testsolr(request):
		a = SearchQuerySet().models(Business).filter(name="chic")
		context = {'result': a}
		return render(request, 'admin/solrtest.html', context) 

def admin_espanol(request):
		context = {}
		return render(request, 'admin/admin-espanol.html', context)

def admin_translate(request):
		context = {}
		return render(request, 'admin/admin-translate.html', context)

def admin_espanol_edit(request):
		context = {}
		return render(request, 'admin/admin-espanol.html', context)

def categories(request):
		context = {}
		return render(request, 'admin/admin-cat.html', context)

def edit_category(request, cid=None):
		context = {'cid': cid}
		return render(request, 'admin/admin-edit.html', context)

def results_page(request, category):
		context = { 'catid': catid }
		return render(request, 'admin/results.html', context)

def company_page(request, company_slug):
		context = { 'company': company_slug }
		return render(request, 'admin/sample-page.html', context)

def manage_featured(request):
		context = {}
		return render(request, 'admin/manage_featured.html', context)
#  --------------  Admin Functions ---------------------  #

def missing_photo_list(request):
        bizs = Business.objects.all()
        biz_without = []
        for biz in bizs: 
                photos = BusinessImages.objects.filter(business_id=biz.id)
                if not photos:
                        biz_without.append(biz.name + "<br />")
        return HttpResponse(biz_without)

def fish_prices(request):
        now = datetime.datetime.now()
        today = now.date()
        fp = FishPrices.objects.filter(fish_date=today)
        fishies = []
        for f in fp:
                fishdict = {}
                fishdict['name_english'] = f.fishname_english
                fishdict['name_spanish'] = f.fishname_spanish
                fishdict['price'] = f.price
                fishdict['description'] = f.fish_description
                fishdict['date'] = f.fish_date
                fishdict['id'] = f.id
                fishies.append(fishdict)
        context = {'fishies': fishies}
        return render(request, 'admin/fish_prices.html', context)

def add_fish_prices(request):
        now = datetime.datetime.now()
        today = now.date()
        if request.method == "POST":
                name_english = request.POST['fishname_english']
                name_spanish = request.POST['fishname_spanish']
                price = request.POST['price']
                desc = request.POST['fish_description']
                #date = request.POST['date']
                f = FishPrices(fishname_english=name_english, fishname_spanish=name_spanish, fish_description=desc, price=price, fish_date=today)
                f.save()
        return HttpResponseRedirect('/admin/fish_prices/')

def del_fish_price(request, fishid=None):
        if fishid:
                f = FishPrices.objects.get(pk=fishid)
                f.delete()
        return HttpResponseRedirect('/admin/fish_prices/')

        
