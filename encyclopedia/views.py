from django.shortcuts import render, redirect
from django import forms
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from . import util
import markdown2
from django.db import models
import re

# class NewEntryForm(forms.Form):
#     entryTitle = forms.CharField(label="Entry Name for File")
#     entryBody = forms.CharField(label="Full Entry Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    
    
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "entryBody": markdown2.markdown(util.get_entry(entry)),
    })


def edit(request, entry):

    if request.method == "POST":
        util.save_entry(entry, request.POST["newEntry"])
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "entryBody": markdown2.markdown(util.get_entry(entry)),
        })
    # if there is a request sent post here, save the edited entry and return to the entry's page

    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "entryBody": (util.get_entry(entry))
    })


def new(request):
    if request.method == "POST":
        allEntries = util.list_entries()
        entryTitle = request.POST["entryTitle"]
        entryBody = request.POST["entryBody"]

        if entryTitle in allEntries:
            raise forms.ValidationError("That entry already exists.")
       
        util.save_entry(entryTitle, entryBody)
        
        return render(request, "encyclopedia/entry.html", {
            "entry": entryTitle,
            "entryBody": markdown2.markdown(util.get_entry(entryTitle)),
        })
        
        # return render(request, "encyclopedia/index.html", {
        #     "entries": util.list_entries()
        # })

    return render(request, "encyclopedia/new.html")


def randomPage(request):
    entryList = util.list_entries()
    entry = random.choice(entryList)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "entryBody": markdown2.markdown(util.get_entry(entry)),
    })


def search(request):
    if request.method == "POST":
        allEntries = util.list_entries()
        searchStr = request.POST["q"]
        
        if searchStr == "":
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
        
        if searchStr in allEntries:
            return render(request, "encyclopedia/entry.html", {
                "entry": searchStr,
                "entryBody": markdown2.markdown(util.get_entry(searchStr))
            })
        
        # if any(searchStr in entry for entry in allEntries):
        simEntries = []
        for entStr in allEntries:
            if re.search(searchStr, entStr, re.IGNORECASE):
                simEntries.append(entStr)
                
        if simEntries:
            return render(request, "encyclopedia/search.html", {
                "entries": simEntries
            })
        
        return render(request, "encyclopedia/search.html", {
            "myError" : "There are no entries that match your query."
         })
        