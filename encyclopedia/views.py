from django.shortcuts import render

from . import util
import markdown2
from django.shortcuts import redirect

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "A page with this title already exists."
            })
        
        util.save_entry(title, content)
        return redirect('entry', title=title)
        
    return render(request, "encyclopedia/new.html")

def search(request):
    query = request.GET.get('q', '')
    
    if util.get_entry(query) is not None:
        return redirect('entry', title=query)
    
    all_entries = util.list_entries()
    matching_entries = [entry for entry in all_entries if query.lower() in entry.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "entries": matching_entries,
        "query": query
    })

def edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect('entry', title=title)

    title = request.GET.get("title")
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

import random

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)