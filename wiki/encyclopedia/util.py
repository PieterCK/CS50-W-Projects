import re

from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django import forms
from markdown2 import Markdown

markdowner = Markdown()

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return markdowner.convert(f.read().decode("utf-8"))
    except FileNotFoundError:
        return None


class search_entry(forms.Form):
    """
    a Class form for searching entries, contained in layout.html
    """
    query = forms.CharField(label="Search Entries")


def load_error(request, message):
    """
    Prompt to load error page
    """
    return render(request, "encyclopedia/error.html", {
        "error": message,
        "form": search_entry()
    })


def load_entry(request, title):
    """
    Function to load entry pages
    """
    if (get_entry(title)):
        return render(request, "encyclopedia/entry.html", {
            "entry": get_entry(title),
            "title": title,
            "form": search_entry()
        })

    src_result = []
    entries = list_entries()
    for i in range(len(entries)):
        if entries[i].__contains__(title):
            src_result.append(entries[i])
    if len(src_result) > 0:
        return render(request, "encyclopedia/src_result.html", {
            "entries": src_result,
            "title": title,
            "form": search_entry()
        })
    return load_error(request, "No matching entry")


def create_entry(title_int, cont_int):
    class entry(forms.Form):
        """

        """
        entry_title = forms.CharField(label="Entry Title", initial=title_int)
        entry_content = forms.CharField(
            widget=forms.Textarea, label="Entry Content", initial=cont_int)
    return entry
