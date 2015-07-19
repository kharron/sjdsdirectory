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
