from glob import escape
import imp
from shutil import register_unpack_format
from urllib import request
from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from random import choice


from . import util

import markdown





md = markdown.Markdown()

class SavePage(forms.Form):
    title = forms.CharField(label="Entry title",)
    text = forms.CharField(label="Entry text")



def new_page(request):
    return render(request, 'encyclopedia/new_page.html')



def save_page(request):
    if request.method == "POST":
        form = SavePage(request.POST)
        flag = False
 
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            for entry in util.list_entries():
                if title.upper() == entry.upper():
                    flag = True
                else:
                    flag = False
            
                if flag == True:
                    return render(request, 'encyclopedia/exist.html', {
                        "extitle": title,
                    })
                else:
                    util.save_entry(title, text)
                    
                    return render(request, 'encyclopedia/entry.html', {
                        "new_entry": md.convert(text),
                        "entry_title": title
                    })
        else:
           return render(request, 'encyclopedia/new_page.html', {
                "form": form
            })        
    else:
        render(request, 'encyclopedia/new_page', {
            'form': SavePage()
        })


def look_for(request):
    if request.method == "GET":
        q = request.GET['q']
        if util.get_entry(q) is not None:
            return render(request, 'encyclopedia/entry.html', {
                "new_entry": util.get_entry(q),
                "entry_title": q.capitalize()
            })
        else:
            substring = []
            for element in util.list_entries():
                if q.upper() in element.upper():
                    substring.append(element)
            
            return render(request, 'encyclopedia/index.html', {
                "entries": substring
            })



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    gotten_entry = util.get_entry(entry)
    if gotten_entry is None:
        return render(request, "encyclopedia/error.html", { 
        "entry": entry,
        "entry_title": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", { 
        "new_entry": md.convert(gotten_entry),
        "entry_title": entry
        })
        

def edit(request, entry):
    content = util.get_entry(entry)

    return render(request, "encyclopedia/edit_page.html", {
        "content": content,
        "title": entry
    })



def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]

        util.save_entry(title, text)

        return render(request, 'encyclopedia/entry.html', {
            "new_entry": md.convert(text),
            "entry_title": title
        })

def random_page(request):

    names = util.list_entries()

    entry = choice(names)

    return redirect(reverse('entry', args=[entry]))


        
   