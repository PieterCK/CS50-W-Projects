from django.shortcuts import render
from random import randint

from . import util

entries = util.list_entries()


def index(request):
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": util.search_entry()
        })

    form = util.search_entry(request.POST)
    if form.is_valid():
        query = form.cleaned_data["query"]
        return util.load_entry(request,query)

def entryPage(request, title):
    return util.load_entry(request, title)

def newEntry(request):
    new_entry = util.create_entry(None, None)
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html", {
            "form2": new_entry(),
            "form": util.search_entry()
        })

    form = new_entry(request.POST)
    if form.is_valid():
        entry_title = form.cleaned_data["entry_title"]
        entry_content = form.cleaned_data["entry_content"]

        if entry_title in entries:
            return util.load_error(request, "Entry with the same title already exist, please submit new entry with another title")

        util.save_entry(entry_title, entry_content)
        return util.load_entry(request, entry_title)

    return util.load_error(request, "Invalid submission")


def editEntry(request, title):
    content = util.get_entry(title)
    if content:
        edit_entry = util.create_entry(title, content)
        if request.method == "GET":
            return render(request, "encyclopedia/edit_entry.html", {
                "form3": edit_entry,
                "title": title,
                "form": util.search_entry()
            })

        form = edit_entry(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            entry_content = form.cleaned_data["entry_content"]
            if entry_title != title:
                return render(request, "encyclopedia/new_entry.html", {
                    "form2": edit_entry(),
                    "form": util.search_entry()
                })
            util.save_entry(entry_title, entry_content)
            return util.load_entry(request, entry_title)
    return util.load_error(request, "Invalid submission")

def randomEntry(request):
    entries = util.list_entries()
    return util.load_entry(request, entries[randint(0,len(entries)-1)])