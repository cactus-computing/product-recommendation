from django.shortcuts import render
from django.http import HttpResponse
from .forms import SnippetForm

def snippet_detail(request):
    if request.method == "POST":
        form = SnippetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()


    form = SnippetForm
    return render(request, 'form/form.html', {'form':form})
