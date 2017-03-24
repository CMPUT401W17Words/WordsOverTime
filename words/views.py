from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
import random
from datetime import datetime, date, time, timedelta
import time
import csv

from .forms import MainForm
from .requesthandler import *
from .hash import *
from .models import *

GRANULARITY_WEEKLY = 'Week'
GRANULARITY_MONTHLY = 'Month'
GRANULARITY_YEARLY = 'Year'

def genHash():
    randomNum1 = random.randint(1, 100)
    randomNum2 = random.randint(1, 6)
    start = int(time.time())
    start = int((start + randomNum1) / randomNum2)
    return str(start)

#http://stackoverflow.com/questions/8380006/file-open-function-with-try-except-python-2-7-1
def checkForFile(hashStr):
    filePath = "/mnt/vol/csvs/"
    try:
      open(filePath + hashStr + ".csv", "r")
      return True
    except IOError:
      return False

#http://stackoverflow.com/questions/13259288/returning-a-list-of-words-after-reading-a-file-in-python
def read_words(words_file):
    return [word for line in words_file for word in line.split()]

# Create your views here.
def index(request):
    return render(request, 'words/index.html')
    #return HttpResponse("Hello world")

def success(request):
    #Get Form Data!
    if "startDate" in request.POST:
        startDateString = request.POST["startDate"]
        startDate = datetime.strptime(startDateString, '%Y-%m-%d')
    else:
        #error page
        return HttpResponse("Must enter a start date")
        startDateString = ''
    if "endDate" in request.POST:
        endDateString = request.POST["endDate"]
        endDate = datetime.strptime(endDateString, '%Y-%m-%d')
    else:
        #error
        return HttpResponse("Must enter an end date")
        endDateString = ''
    granularity = request.POST["granularity"]
    
    #Form data for n closest neighbors
    if "Nneighbor" in request.POST:
        n = request.POST["Nneighbor"]
    else:
        n = ''
    if "keywords" in request.POST:
        keyWords = request.POST["keywords"]
        keyWordsList = keyWords.split()
    else:
        #error
        keyWords = ''
        keyWordsList = [] 
    if "text_file" in request.FILES:
        textFile = request.FILES["text_file"]
        textFileWords = read_words(textFile)
    else:
        textFile = ''
        textFileWords = []
    skipOrCBOW1 = request.POST["skipOrCBOW1"]
    closeCBOW = False
    if(skipOrCBOW1 == 'CBow'):
        closeCBOW = True
    #TODO: read in file and create list of strings from it
    #How to separate words?

    #Form data for cosine distance
    if "wordPairs" in request.POST:
        wordPair = request.POST["wordPairs"]
        wordPairList = wordPair.split()
    else:
        wordPair = ''
        wordPairList = []
    if "text_file2" in request.FILES:
        textFile2 = request.FILES["text_file2"]
        textFile2Words = read_words(textFile2)
    else:
        textFile2 = ''
        textFile2Words = []
    skipOrCBOW2 = request.POST["skipOrCBOW2"]
    cosCBOW = False
    if(skipOrCBOW2 == 'CBow'):
        cosCBOW = True
    #TODO: read in file and create list of strings from it
    #How to separate words?
    
    #Form data for tfidf
    if "tfidfWord" in request.POST:
        tfidfWord = request.POST["tfidfWord"]
        tfidfWordList = tfidfWord.split()
    else:
        tfidfWord = ''
    
    #Form data for Pairwise Conditional Probabilities
    if "conditionalWord" in request.POST:
        conditionalWordPair = request.POST["conditionalWord"]
        conditionalWordPairList = conditionalWordPair.split()
    else:
        conditionalWordPair = ''
        conditionalWordPairList = []
    if "fileConditional" in request.FILES:
        fileConditional = request.FILES["fileConditional"]
    else:
        fileConditional = ''
    #TODO: read in file and create list of strings from it
    #How to separate words?

    #Form data from checkboxes
    if "Average valence" in request.POST:
        averageValence = request.POST["Average valence"]
    else:
        averageValence = 0
    if "Average arousal" in request.POST:
        averageArousal = request.POST["Average arousal"]
    else:
        averageArousal = 0
    if "5 Words Average valence" in request.POST:
        top5averageValence = request.POST["5 Words Average valence"]
    else:
        top5averageValence = 0
    if "5 Words Average arousal" in request.POST:
        top5averageArousal = request.POST["5 Words Average arousal"]
    else:
        top5averageArousal = 0

    #Form data for word frequency
    if "frequencyWord" in request.POST:
        wordFrequencyWords = request.POST["frequencyWord"]
        wordFrequencyList = wordFrequencyWords.split()
    else:
        wordFrequencyWords = ''
        wordFrequencyList = []
    if "wordFrequencyFile" in request.FILES:
        wordFrequencyFile = request.FILES["wordFrequencyFile"]
        freqFileWords = read_words(wordFrequencyFile)
    else:
        wordFrequencyFile = ''
        freqFileWords = []
    #TODO: read in file and create list of strings from it
    #How to separate words?

    #Form data for relative word frequency
    if "relativeWord" in request.POST:
        relativeWords = request.POST["relativeWord"]
        relativeList = relativeWords.split()
    else:
        relativeWords = ''
        relativeList = []
    if "relativeFile" in request.FILES:
        relativeFile = request.FILES["relativeFile"]
        relativeFileWords = read_words(relativeFile)
    else:
        relativeFile = ''
        relativeFileWords = []
    #TODO: read in file and create list of strings from it
    #How to separate words?

    #Form data for email
    if "userEmail" in request.POST:
        email = request.POST["userEmail"]
    else:
        #error
        email = ''
        return HttpResponse("Must enter an email")
    #print(keyWordsList)  
    
    hashList = []
    requestList = []
    #print(textFileWords)

    #Handle N closest neighbor request
    if(n != '' and (keyWordsList or textFileWords)):
        n = int(n)
        closeHash = genHash()
        if(keyWordsList):
            nClosestReq = NClosestNeighboursOverTimeRequest((startDate, endDate), granularity, keyWordsList, n, closeCBOW, closeHash)
        else:
            decodedList = []
            for word in textFileWords:
                word = word.decode("utf-8")
                decodedList.append(word)
            nClosestReq = NClosestNeighboursOverTimeRequest((startDate, endDate), granularity, decodedList, n, closeCBOW, closeHash)
        #nClosestResult = nClosestReq.execute()
        #nClosestResult.generateCSV(closeHash)
        requestList.append(nClosestReq)
        hashList.append(closeHash)

    #Handle CosineDistance request        
    if (wordPairList or textFile2Words):
        cosHash = genHash()
        newList = []
        if(wordPairList):
            newList = wordPairList
        else:
            decodedList = []
            for word in textFile2Words:
                word = word.decode("utf-8")
                decodedList.append(word)
            newList = decodedList
        #Convert list of word pairs into list of tuples containing the pairs
        wordPairTuples = []
        for i in range(len(newList)):
            temp = newList[i].split(",")
            wordPairTuples.append((temp[0], temp[1]))
        cosReq = CosDistanceOverTimeRequest((startDate, endDate), granularity, wordPairTuples, cosCBOW, cosHash)
        #cosResult = cosReq.execute()
        #cosResult.generateCSV(cosHash)
        requestList.append(cosReq)
        hashList.append(cosHash)

    #Handle tfidf request
    if (tfidfWord != ''):
        tfidfHash = genHash()
        tfidfReq = TfidfOverTimeRequest((startDate, endDate), granularity, tfidfWordList, tfidfHash)
        #tfidfResult = tfidfReq.execute()
        #tfidfResult.generateCSV(tfidfHash)
        requestList.append(tfidfReq)
        hashList.append(tfidfHash)

    #Handle Pairwise Probability request
    if (conditionalWordPairList):
        pairHash = genHash()
        pairReq = PairwiseProbabilitiesOverTimeRequest((startDate, endDate), granularity, conditionalWordPairList[0], conditionalWordPairList[1], pairHash)
        pairResult = pairReq.execute()
        for key in pairResult:
            pairHash = genHash()
            pairResult[key].generateCSV(pairHash)
            hashList.append(pairHash)
        #pairResult = pairReq.execute()
        #pairResult.generateCSV(pairHash)
        #hashList.append(pairHash)

    #avgHash = 5
    #Handle Average Valence Request
    if (averageValence == '1'):
        avgValHash = genHash()       
        avgValReq = AverageValenceOverTimeRequest((startDate, endDate), granularity, avgValHash)
        #avgValResult = avgValReq.execute()
        #avgValResult.generateCSV(avgValHash)
        requestList.append(avgValReq)
        hashList.append(avgValHash)

    #Handle Average Arousal Request
    if (averageArousal == '1'):
        avgAroHash = genHash()  
        avgAroReq = AverageArousalOverTimeRequest((startDate, endDate), granularity, avgAroHash)
        #avgAroResult = avgAroReq.execute()
        #avgAroResult.generateCSV(avgAroHash)
        requestList.append(avgAroReq)
        hashList.append(avgAroHash)  

    #Handle Average 5 Word Valence Request
    if (top5averageValence == '1'):
        avgVal5Hash = genHash()      
        avgVal5Req = AverageValenceFiveWordsOverTimeRequest((startDate, endDate), granularity, avgVal5Hash)
        #avgVal5Result = avgVal5Req.execute()
        #avgVal5Result.generateCSV(avgVal5Hash)
        requestList.append(avgVal5Req)
        hashList.append(avgVal5Hash)   

    #Handle Average 5 Word Arousal Request
    if (top5averageArousal == '1'):
        avgAro5Hash = genHash()      
        avgAro5Req = AverageArousalFiveWordsOverTimeRequest((startDate, endDate), granularity, avgAro5Hash)
        #avgAro5Result = avgAro5Req.execute()
        #avgAro5Result.generateCSV(avgAro5Hash) 
        requestList.append(avgAro5Req)
        hashList.append(avgAro5Hash)  
    
    #Handle Word Freqency
    if (wordFrequencyList or freqFileWords):
        frequencyHash = genHash()
        newList = []
        if(wordFrequencyList):
            newList = wordFrequencyList
        else:
            decodedList = []
            for word in freqFileWords:
                word = word.decode("utf-8")
                decodedList.append(word)
            newList = decodedList
        freqReq = WordFrequencyOverTimeRequest((startDate, endDate), granularity, newList, frequencyHash)
        #freqResult = freqReq.execute()
        #freqResult.generateCSV(frequencyHash)
        requestList.append(freqReq)
        hashList.append(frequencyHash)

    #Handle relative word frequency
    if (relativeList or relativeFileWords):
        relativeHash = genHash()
        newList = []
        if(relativeList):
            newList = relativeList
        else:
            decodedList = []
            for word in relativeFileWords:
                word = word.decode("utf-8")
                decodedList.append(word)
            newList = decodedList
        relReq = WordFrequencyOverTimeRequest((startDate, endDate), granularity, newList, relativeHash)
        #relResult = freqReq.execute()
        #relResult.generateCSV(relativeHash)
        requestList.append(relReq)
        hashList.append(relativeHash)
    
    #req = CosDistanceOverTimeRequest(hashStr, (startDate, endDate), 'Year', keyWordsList[0], keyWordsList[1], True)
    
    #result = req.execute()
    #result.generateCSV(hashStr)

    #print(hashList)

    context = {}
    for index in range (0, len(hashList)):
        context["Hash%s" %index] = hashList[index]
    
    context["nHashes"] = len(hashList)

    requests = RequestsExecuteThread(requestList)
    requests.start()

    return render(request, 'words/success.html', context)
    

def graph(request, hash):
    filePath = '/mnt/vol/csvs/'
    #keyWords = ["bird", "thing"]
    #valuesList = [(2009, 0.8, 'bird'), (2010, 0.8, 'bird'), (2009, 0.1, 'thing'), (2010, 0.1, 'thing')]
    yValues = []
    xValues = []
    xAxis = ''
    yAxis = ''
    thing = []
    valuesList = []
    keyWords = []
    with open(filePath + hash + '.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        xAxis = reader.fieldnames[0]
        yAxis = reader.fieldnames[1]
        keyword = reader.fieldnames[2]
        for row in reader:
            #xValues.append(row[xAxis])
            #thing = row[yAxis]
            #yValues.append(thing[1])
            #keyWords.append(thing[0])
            valuesList.append((row[xAxis], row[yAxis], row[keyword]))

    #print(valuesList)

    for item in valuesList:
        if(item[2] not in keyWords):
            keyWords.append(item[2])

    #print(keyWords)

    yDict = {}
    yValuesList = []
    for word in keyWords:
        yDict[word] = []
        yTempValues = []
        for thing in valuesList:
            #print(thing)
            if(thing[2] == word):
                yDict[word].append(float(thing[1]))
                yTempValues.append(float(thing[1]))
                date = datetime.strptime(thing[0], '%Y-%m-%d').date()
                timestamp = int(time.mktime(date.timetuple())) * 1000
                if(timestamp not in xValues):
                    xValues.append(timestamp)
        yValuesList.append(yTempValues)
    
    #print(yDict)
    #print(xAxis)
    #print(yAxis)

    #print(xValues)

    #print(yValuesList)

    #print (keyWords)

    context = {
        'xAxis': xAxis, 
        'yAxis': yAxis, 
        'xValues': xValues, 
        'keywords': keyWords,
        'yValues': yValuesList,
    }


    #generateCSV(xAxis, yAxis, xValues, yDict, hash)
    #for index in range (0, len(keyWords)):
    #    context["yValues%s" %index] = int(hashList[index])
    #with open(hash + '.csv', 'w') as csvfile:
    #    resultWriter = csv.writer(csvfile, dialect='excel')
    #    resultWriter.writerow([xAxis, yAxis, 'keyword'])
    #    for item in valuesList:
    #        resultWriter.writerow([item[0], item[1], item[2]])
        #for j in range(0, len(keyWords)):
        #    for i in range(0, len(xValues)):
        #        resultWriter.writerow([xValues[i], yValues[j][i], keyWords[j]])
        #for i in range(len(self.xValues)):
        #    resultWriter.writerow([self.xValues[i], self.yValues[i]])

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
