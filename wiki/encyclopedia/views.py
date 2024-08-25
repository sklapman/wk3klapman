from django.shortcuts import render, redirect
from django.http import Http404
from . import util
from django import forms
import random
import markdown2

class SearchWiki(forms.Form):
    search = forms.CharField(label="Search Encyclopedia")



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchWiki()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        raise Http404("Page not found.")
    
        # Convert Markdown content to HTML
    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "content": html_content,
        "title": title
    })

def search(request):
    query = request.GET.get("q")
    if query:
        entries = util.list_entries()
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
        if len(matching_entries) == 1 and matching_entries[0].lower() == query.lower():
            return redirect("entry", title=matching_entries[0])
        return render(request, "encyclopedia/search.html", {
            "entries": matching_entries,
            "query": query
        })
    return redirect("encyclopedia/index.html")


def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        if util.get_entry(title):
            return render(request, "encyclopedia/create_page.html", {
                "error": "An entry with this title already exists.",
                "title": title,
                "content": content
            })
        
        util.save_entry(title, content)
        return redirect("encyclopedia:entry", title=title)
    
    return render(request, "encyclopedia/create_page.html")


def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("encyclopedia:entry", title=title)
    
    content = util.get_entry(title)
    if content is None:
        raise Http404("Page not found.")
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    if not entries:
        raise Http404("No entries found.")
    random_entry = random.choice(entries)
    return redirect("encyclopedia:entry", title=random_entry)