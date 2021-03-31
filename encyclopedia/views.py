from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

import markdown2
import random

class NewEntryForm(forms.Form):
	title = forms.CharField(label="Title")
	entry = forms.CharField(widget=forms.Textarea,label="NewEntry")
	

class EditEntryForm(forms.Form):
	entry = forms.CharField(widget=forms.Textarea, initial="Hola")

def index(request):
	if request.method == "POST":
		title=request.POST.get("q")
		text = util.get_entry(title.capitalize())
		if text:
			return render(request, "encyclopedia/title.html", {
				"text": util.get_entry(title.capitalize()),
				"title": title.capitalize(),
				})
		else:
			all_entries = list(util.list_entries())
			new_list=[]
			for entry in all_entries:
				if entry.upper().count(title.upper()) > 0:
					new_list.append(entry)
			return render(request, "encyclopedia/index.html", {
    			"entries": new_list
    			})
    			
	return render(request, "encyclopedia/index.html", {
    	"entries": util.list_entries()
    	})


def title(request,title):
	return render(request, "encyclopedia/title.html", {
		"text": util.get_entry(title.capitalize()),
		"title": title.capitalize(),

		})

def new_entry(request):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			entry = form.cleaned_data["entry"]
			title = form.cleaned_data["title"]
			#If entry does not exist, save it
			if not util.get_entry(title.capitalize()):
				util.save_entry(title,entry)
				return HttpResponseRedirect(reverse("title", kwargs={'title': title}))
			else:
				return render(request,"encyclopedia/errormsg.html",{
					"errormsg": 'Entry "'+title.capitalize()+'" alreay exists!'
					})	
		else:
			return render(request,"encyclopedia/new_entry.html",{
				"form": form
				})
	return render(request,"encyclopedia/new_entry.html",{
		"form": NewEntryForm()
		})	

def edit_entry(request, title):
	if request.method == "POST":
		form = EditEntryForm(request.POST)
		if form.is_valid():
			entry = form.cleaned_data["entry"]
			util.save_entry(title,entry)
			return HttpResponseRedirect(reverse("title", kwargs={'title': title}))
		else:
			return render(request,"encyclopedia/edit_entry.html",{
				"form": form
				})

	return render(request, "encyclopedia/edit_entry.html", {
		"title": title.capitalize(),
		"form": EditEntryForm(initial={'entry': util.get_entry(title.capitalize())})
		})

def random_entry(request):
	index = random.randint(0, len(util.list_entries())-1)
	title = util.list_entries()[index].capitalize()
	return render(request, "encyclopedia/title.html", {
		"text": util.get_entry(title),
		"title": title,

		})	

	
