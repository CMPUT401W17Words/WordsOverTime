from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic

# Create your views here.
def index(request):
  return render(request, 'words/401.html')
 
#class IndexView(generic.DetailView):
  #template_name = "words/index.html"
  
def results(request):
  if request.method == 'POST':
    form = ContactForm(request.POST) 
    if form.is_valid():
      data = myform.cleaned_data
      #process data with field = data['field']
  return HttpResponseRedirect()