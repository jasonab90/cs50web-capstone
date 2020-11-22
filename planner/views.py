from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

import json
from .models import User, Card, Item, Date
import calendar
import datetime

# Create your views here.

@login_required
def index(request):
	cards = Card.objects.filter(owner=User.objects.get(id=request.user.id)).order_by("-timestamp")
	items = Item.objects.filter(card__in=cards)
	return render(request,"planner/index.html", {
		"cards": cards,
		"items": items
		})

def get_profile(request):
	cards = Card.objects.filter(owner=User.objects.get(id=request.user.id)).order_by("-timestamp")

	return render(request,"planner/profile.html", {
		"cards": cards
		})

##### CARD FUNCTIONS #####
@login_required
def add_card(request,current_year=datetime.date.today().year, current_month = datetime.date.today().month, next_day = datetime.date.today().day + 1, check_date=0):

	# Get list of cards for planner/layout.html menu
	cards = get_card_list(request)

	# Grab the number of days in the current month
	current_days = range(1,calendar.monthrange(current_year,current_month)[1]+1)

	# If for whatever reason the inputted year is not between 2020 and 2023, set it to the current year

	years = range(2020,2023)
	if current_year not in years:
		current_year = datetime.date.today().year

	
	if request.method == "POST":

		# Create the initial card
		title = request.POST['title']
		description = request.POST['description']
		user = User.objects.get(id=request.user.id)

		card = Card(owner=user, title=title, description=description)
		card.save()

		# If the add_date checkbox was selected, add the card to the date model
		add_date = request.POST.get('add_date', False)

		if add_date:
			card_date = datetime.datetime(int(request.POST['year']),int(request.POST['month']),int(request.POST['day']))
			date = Date(owner=user,card=card,date=card_date)
			date.save()

		return render(request, "planner/card_add.html",	{
			"message": "Card successfully added.",
			"alert_type": "alert alert-success",
			"cards": cards,
			"months": get_months(),
			"current_month": current_month,
			"next_day": next_day,
			"current_days": current_days,
			"years": years,
			"check_date": check_date
			})

	

	else:
		return render(request, "planner/card_add.html", {
			"cards": cards,
			"months": get_months(),
			"current_month": current_month,
			"next_day": next_day,
			"current_days": current_days,
			"years": years,
			"check_date": check_date
			})



@login_required
def view_card(request, id):

	cards = get_card_list(request)
	user = get_user(request)
	card = Card.objects.get(id=id)

	# Verify that user can view the card.

	if verify_user(request, user, card.id):
		pass
	else:
		return render(request,"planner/error.html", {
			"message": "You do not have permission to access this page."
			})

	if request.method == "POST":

		# Add the item to the item model.
		text = request.POST['item']
		card_id = request.POST['card']
		
		item = Item(text=text,
			card=Card.objects.get(id=card_id),
			owner=user)
		item.save()
	else:
		card_id = id

	# Grab the cards and items
	card = Card.objects.get(id=id)
	items = Item.objects.filter(owner=user, card=Card.objects.get(id=card_id))
	dates = Date.objects.filter(owner=user, card=card)

	return render(request, "planner/card_view.html", {
		"card": card,
		"cards": cards,
		"items": items,
		"dates": dates,
		"add_date": get_default_date(),
		"months": get_months()
		})

@login_required
def edit_card(request, id):
	menu = get_card_list(request)
	user = get_user(request)

	card = Card.objects.get(id=id)

	if verify_user(request, user, card.id):
		pass
	else:
		return render(request,"planner/error.html", {
			"message": "You do not have permission to access this page."
			})

	dates = Date.objects.filter(owner=user,card=card)

	if request.method == "POST":

		# Evaluate if we need to remove dates that are associated with the card

		checkbox_values = request.POST.getlist('checkbox')

		checkbox_dates = []

		# Convert the POST valus to integers
		for date in checkbox_values:
			checkbox_dates.append(int(date))

		title = request.POST['title']
		description = request.POST['description']

		all_dates = Date.objects.filter(owner=user,card=card)

		# Delete all dates that were not checked off
		for date in all_dates:
			if date.id not in checkbox_dates:
				
				Date.objects.get(owner=user,id=date.id).delete()
				
		# Finish other edits
		card.title = title
		card.description = description
		card.save()

		return render(request,"planner/card_edit.html", {
		"cards": menu,
		"message": "Card successfully edited!",
		"alert_type": "alert alert-success",
		"card": card,
		"dates": dates,
		"default_date": get_default_date(),
		"months": get_months()
		})

	return render(request,"planner/card_edit.html", {
		"cards": menu,
		"card": card,
		"dates": dates,
		"default_date": get_default_date(),
		"months": get_months()
		})

@login_required
def copy_card(request, id):
	menu = get_card_list(request)
	user = get_user(request)

	card = Card.objects.get(id=id)

	if verify_user(request, user, card.id):
		pass
	else:
		return render(request,"planner/error.html", {
			"message": "You do not have permission to access this page."
			})

	dates = Date.objects.filter(owner=user,card=card)

	current_year=datetime.date.today().year
	current_month = datetime.date.today().month
	next_day = datetime.date.today().day + 1
	current_days = range(1,calendar.monthrange(current_year,current_month)[1]+1)

	years = range(2020,2023)
	check_date=0

	if request.method == "POST":
		print(request.POST)
		old_card = Card.objects.get(id=id,owner=user)

		# Copy Card

		title = request.POST['title']
		description = request.POST['description']
		user = User.objects.get(id=request.user.id)

		new_card = Card(owner=user, title=title, description=description)
		new_card.save()


		# Copy Items

		copy_items = request.POST.get('copy-items', False)

		if copy_items:
			old_items = Item.objects.filter(owner=user,card=old_card)
			for item in old_items:
				item.card = new_card
				item.pk = None
				item.save()
			
		# Copy Dates

		copy_dates = request.POST.getlist('copy-dates', False)

		if copy_dates:
			for date_id in copy_dates:
				date_id = int(date_id)
				date = Date.objects.get(id=date_id, owner=user,card=old_card)
				date.card = new_card
				date.pk = None
				date.save()

		# Add Date, if selected

		add_date = request.POST.get('add_date', False)

		if add_date:
			month =  request.POST.get('month', 1)
			day =  request.POST.get('day', 1)
			year = request.POST.get('year', 2020)
			card_date = datetime.datetime(int(year),int(month),int(day))
			date = Date(owner=user,card=new_card,date=card_date)
			date.save()

		return HttpResponseRedirect(reverse("view_card", args=(new_card.id,)))

	return render(request, "planner/card_copy.html", {
		"cards": menu,
		"card": card,
		"dates": dates,
		"default_date": get_default_date(),
		"months": get_months(),
		"add_date": get_default_date(),
		"years": years,
		"current_month": current_month,
		"current_days": current_days
		})

##### CARD ACTIONS #####

def verify_user(request, user, card_id):
	card = Card.objects.get(id=card_id)

	if card.owner != user:

		return False

		
	return True

def get_card_list(request):
	cards = Card.objects.filter(owner=User.objects.get(id=request.user.id))

	return cards


@login_required
def add_date(request, id):
	user = get_user(request)
	card = Card.objects.get(id=id,owner=user)

	if request.method == "POST":
		card_date = datetime.datetime(int(request.POST['year']),int(request.POST['month']),int(request.POST['day']))
		date = Date(owner=user,card=card,date=card_date)
		date.save()
	return HttpResponseRedirect(reverse("view_card",args=(id,)))

@csrf_exempt
@login_required
def act_item(request, id):
	item = Item.objects.get(id=id, owner=get_user(request))

	if request.method == "PUT":
		data = json.loads(request.body)
		if data.get("is_active") is not None:
			if item.is_active == data['is_active']:
				pass
			else:
				item.is_active = data['is_active']
				item.save()
		return JsonResponse({"status": "success", "item": item.id, "text": item.text,"is_active": item.is_active})
	return JsonResponse({"status": "success", "item": item.id, "text": item.text,"is_active": item.is_active})

@csrf_exempt
@login_required
def edit_item(request, id):
	item = Item.objects.get(id=id,owner=get_user(request))

	print(request.POST)
	
	if request.method == "POST":
		item.text = request.POST['edit-text']
		item.save()
	return HttpResponseRedirect(reverse("view_card",args=(item.card.id,)))

@csrf_exempt
@login_required
def favorite_card(request, id):
	card = Card.objects.get(id=id, owner=get_user(request))

	if request.method == "PUT":
		data = json.loads(request.body)

		if data.get("favorite") is not None:
			card.favorite = data['favorite']
			card.save()
	return JsonResponse({"status": "success", "card_id": card.id, "favorite": card.favorite}) 

@csrf_exempt
@login_required
def archive_card(request, id):
	card = Card.objects.get(id=id, owner=get_user(request))

	if request.method == "PUT":
		data = json.loads(request.body)
		print(data)
		if data.get("archived") is not None:
			card.archived = data['archived']

			# Unfavorite the card if it has been archived
			if card.archived ==  True:
				card.favorite = False
			card.save()
	return JsonResponse({"status": "success", "card_id": card.id, "archived": card.archived}) 

@csrf_exempt
@login_required
def hide_completed(request, id):

	card = Card.objects.get(id=id, owner=get_user(request))

	card.hide_completed = True
	card.save()

	return HttpResponseRedirect(reverse("view_card",args=(id,)))

@csrf_exempt
@login_required
def show_completed(request, id):

	card = Card.objects.get(id=id, owner=get_user(request))

	card.hide_completed = False

	card.save()
	return HttpResponseRedirect(reverse("view_card",args=(id,)))

@login_required
def get_item_status(request, id):
	item = Item.objects.get(id=id, owner=get_user(request))

	return JsonResponse({"status": "success", "item_id": item.id, "text": item.text, "is_active": item.is_active})

def get_user(request):

	user = User.objects.get(id=request.user.id)

	return user

def get_default_date():

	current_year = datetime.date.today().year
	current_month = datetime.date.today().month
	next_day = datetime.date.today().day + 1
	current_days = range(1,calendar.monthrange(current_year,current_month)[1]+1)
	years = range(2020,2023)

	return {
		"year": current_year,
		"month": current_month,
		"next_day": next_day,
		"day_range": current_days,
		"years": years
	}

def get_months():
	months = []
	i = 0
	for month in calendar.month_name:
		temp = (i, month)
		months.append(temp)
		i = i + 1
	return months



##### CALENDAR FUNCTIONS HERE #####
@login_required
def get_calendar(request, selected_year=datetime.date.today().year, selected_month=datetime.date.today().month):

	c = calendar.Calendar(6)
	today = datetime.date.today()
	
	generate_month = c.itermonthdates(selected_year, selected_month)
	days = []

	# Generate the tuple for the month
	for day in generate_month:
		temp = ()

		date = datetime.date(day.year, day.month, day.day)

		if date.weekday() == 6:
			line = "new"
		elif date.weekday() == 5:
			line = "end"
		else:
			line = None

		card_count = Date.objects.filter(date=date,owner=get_user(request),card__archived=False)

		# Year | Month | Day|  Day of Week (0-6 int) | if it's a Sunday, start a new line/if Saturday, end line | Day of Week (Full Name) | # of cards associated with date | the Card objects themselves
		temp = (day.year, day.month, day.day, date.weekday(), line, date.strftime("%A"), card_count.count(), card_count)

		days.append(temp)

	month_name = datetime.date(selected_year, selected_month, 1).strftime('%B')	

	# Generate the next/previous month links
	previous = ()

	if selected_month - 1 < 1:
		previous = (selected_year - 1, 12)
	else:
		previous = (selected_year, selected_month - 1)

	next = ()

	if selected_month + 1 > 12:
		next = (selected_year + 1, 1)
	else:
		next = (selected_year, selected_month + 1)

	today_date = (today.year, today.month, today.day)

	return render(request, "planner/calendar.html", {
		"days": days,
		"selected_year": selected_year,
		"selected_month": selected_month,
		"month": month_name,
		"previous": previous,
		"next": next,
		"today": today_date,
		"cards": get_card_list(request)
		})

@login_required
def get_date(request, year, month, day):

	date = datetime.datetime(year, month, day)
	user = get_user(request)

	cards = Date.objects.filter(date=date,owner=user)

	month_name = datetime.date(year, month, day).strftime('%B')	
	print(month)
	return render(request, "planner/date.html", {
		"cards": get_card_list(request),
		"date_cards": cards,
		"year": year,
		"month": month_name,
		"day": day,
		"month_number": month
		})



##### LOGIN/REGISTRATION FUNCTIONS #####

def register(request):

	if request.user.id:
		return HttpResponseRedirect(reverse("index"))

	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		password = request.POST["password"]
		confirmation = request.POST["confirmation"]

		if password != confirmation:
			return render(request, "planner/register.html",{
				"message": "Passwords must match.",
				"alert_type": "alert alert-danger"
				})

		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "planner/register.html",{
				"message": "Username already taken.",
				"alert_type": "alert alert-danger"
				})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	return render(request, "planner/register.html")

def login_view(request):
	if request.method == "POST":

		username = request.POST["username"]
		password = request.POST["password"]

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "planner/login.html", {
				"message": "Invalid login credentials.",
				"alert_type": "alert alert-danger" 
				})
	else:
		return render(request, "planner/login.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))