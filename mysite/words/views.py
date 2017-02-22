from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Question

# Create your views here.
def index(request):
  return render(request, 'words/401.html')
 

#class IndexView(generic.DetailView):
  #template_name = "words/index.html"
