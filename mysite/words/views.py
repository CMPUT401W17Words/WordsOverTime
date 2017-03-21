from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
import random
from datetime import datetime, date, time, timedelta
import time

from .forms import MainForm
from .requesthandler import *

GRANULARITY_WEEKLY = 1
GRANULARITY_MONTHLY = 2
GRANULARITY_YEARLY = 3


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
    startDate = date.today()
    endDate = date.today()
    form = MainForm(request.POST)
    if form.is_valid():
        keyWords = form.cleaned_data['keywords']
        #print (keyWords)
        keyWordsList = keyWords.split()
        
        
        #print (keyWordsList)
        
        startDate = form.cleaned_data['startDate']
        endDate = form.cleaned_data['endDate']
        #userChoice = form.cleaned_data['choice_field']
    #if(userChoice == '1'):
        #handle closest_neighbours request
    #elif(userChoice == '2'):
        #handle cosine_distance request
    #etc...

    #print (keyWords)
    #keyWordsList = ['rabbit', 'bird']
    #req = CosDistanceOverTimeRequest((startDate, endDate), 'Year', keyWordsList[0], keyWordsList[1])
    #result = req.execute()

    granularity = 1;
    #granularity = 2;

    xValues = [];
    #weekly
    if(granularity == GRANULARITY_WEEKLY):
        timeDiff = timedelta(days = 7)
    #monthly
    elif (granularity == GRANULARITY_MONTHLY):
        #TODO: change it to be correct number of days for each month?
        timeDiff = timedelta(days = 30)
    #yearly
    else:
        timeDiff = timedelta(days = 365) 
    
    tempDate = startDate
    timestamp = 0
    while(tempDate < endDate):
        timestamp = int(time.mktime(tempDate.timetuple())) * 1000
        xValues.append(timestamp)
        tempDate = tempDate + timeDiff
    #yearly
    #if(granularity == 2):
    #    pushDate = startDate
    #    yearDiff = endDate.year - startDate.year
    #    for i in range (0, yearDiff):
    #        pushDate.

    #years = result.xValues
    years = []
    yearDiff = endDate.year - startDate.year
    for i in range (0, yearDiff):
        years.append(startDate.year + i)

    #yValues = result.yValues
    yValues = []
    for i in range(0, len(xValues)):
        randomNum = random.randint(1,4)
        yValues.append(randomNum)

    splitKeywords = keyWords.split()

    #yValuesList = []
    #for j in range (0, len(keyWords)):
    #    yValuesList.append([])
    #    for i in range (0, len(years)):
    #        randomNum = random.randint(1,4)
    #        yValuesList[j].append(randomNum)
        
    
    #xAxis = result.xTitle
    #yAxis = result.yTitle
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
        'xValues': xValues,
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
  
def results(request):
  if request.method == 'POST':
    form = ContactForm(request.POST) 
    if form.is_valid():
      data = myform.cleaned_data
      #process data with field = data['field']
      #generate a Request object (see requesthandler.py)
  return HttpResponseRedirect()
