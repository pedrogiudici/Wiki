from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from random import randrange

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def greet(request, page):
    for i in util.list_entries():
        if i.lower() == page.lower():
            return render(request, 'encyclopedia/pages.html', {
                'page': util.get_entry(page),
                'pagetitle': page.capitalize()
            })
    return render(request, 'encyclopedia/pages.html', {
        'page': util.get_entry(page),
        'pagetitle': 'Error'
    })

def search(request):
    if request.method == 'GET':
        s = request.GET.get('q')
        entries = []
        for i in util.list_entries():
            if i.lower() == s.lower():
                return render(request, 'encyclopedia/pages.html', {
                    'page': util.get_entry(s),
                    'pagetitle': s.capitalize()
                })
            if i.lower().find(s.lower()) != -1:
                entries.append(i)
        return render(request, 'encyclopedia/search.html', {
            'entries': entries
        })

def add(request):
    class NewPageForm(forms.Form):
        title = forms.CharField(label='Title')
        cont = forms.CharField(label='Content', widget=forms.Textarea)
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            cont = form.cleaned_data['cont']
            for i in util.list_entries():
                if title.lower() == i.lower():
                    return render(request, 'encyclopedia/add.html', {
                        'form': 'There is already a page with that title'
                    })
            util.save_entry(title.capitalize(), cont)
            return render(request, 'encyclopedia/pages.html', {
                'page': util.get_entry(title),
                'pagetitle': title.capitalize()
            })
    return render(request, 'encyclopedia/add.html',{
        'form': NewPageForm()
    })

def edit(request):
    class EditPageForm(forms.Form):
        title = forms.CharField(label='Edit Title')
        cont = forms.CharField(label='Edit Content', widget=forms.Textarea)
    if request.method == "GET":
        e = request.GET.get('e')
        data = {'title': e, 'cont': util.get_entry(e).replace('\r','')}
        form = EditPageForm(data)
        return render(request, 'encyclopedia/edit.html', {
            'form': form
        })
    if request.method =='POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            cont = form.cleaned_data['cont']
            util.save_entry(title, cont)
            return render(request, "encyclopedia/pages.html", {
                'page': util.get_entry(title),
                'pagetitle': title.capitalize()
            })

def random(request):
    l = util.list_entries()
    l.remove('Error')
    page = l[randrange(len(l))]
    return render(request, 'encyclopedia/pages.html', {
        'page': util.get_entry(page),
        'pagetitle': page.capitalize()
    })