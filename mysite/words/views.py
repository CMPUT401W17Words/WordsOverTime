from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Question
import random

from .forms import MainForm

def getKeywords(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MainForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MainForm()

    return render(request, 'words/401.html', {'form': form})


# Create your views here.
def index(request):
    return render(request, 'words/401.html')

def graph(request):
    #testList = [0.1,0.1,0.1,0.1]
    #testDict = {}
    #testDict["hello"] = testList
    #testList2 = [1, 2, 3, 4]
    #testDict2 = {}
    #testDict2["foobar"] = testList2
    keyWords = []
    startDate = 0
    endDate = 0
    form = MainForm(request.POST)
    if form.is_valid():
        keyWords = form.cleaned_data['keywords']
        startDate = form.cleaned_data['startDate']
        endDate = form.cleaned_data['endDate']
    years = []
    for i in range (int(startDate), int(endDate)):
        years.append(i)

    yValues = []
    for i in range(0, len(years)):
        randomNum = random.randint(1,4)
        yValues.append(randomNum)

    #yValuesList = []
    #for j in range (0, len(keyWords)):
    #    yValuesList.append([])
    #    for i in range (0, len(years)):
    #        randomNum = random.randint(1,4)
    #        yValuesList[j].append(randomNum)
        
    
    xAxis = "Date"
    yAxis = "Valence"
    word1 = "Hello"
    word2 = "Hi"
    #w1x = [1,6,3,4]
    #w1y = [1,3,6,7]
    #w2x = [2,5,6,7]
    #w2y = [1,4,7,9]
    context = {
        'xAxis': xAxis,
        'yAxis': yAxis,
        #'word1': word1,
        #'word2': word2, 
        'xValues': years,
        #'w1x': w1x,
        #'w1y': w1y,
        #'w2x': w2x,
        #'w2y': w2y,
        'keywords': keyWords,
        'yValues': yValues
    }
    return render(request, 'words/graph2.html', context)
 

#class IndexView(generic.DetailView):
  #template_name = "words/index.html"
