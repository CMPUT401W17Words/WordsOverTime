import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import words.requesthandler
from words.models import Document_Data, Word_Data
from datetime import date

dateRange = (date(2000, 5, 19), date(2002, 10, 11))
granularity = 'Year'
word1 = 'credit'
word2 = 'company'
N = 2

try:
    request = words.requesthandler.CosDistanceOverTimeRequest(dateRange, granularity, word1, word2, False)
    result = request.execute()
    print('cos distance over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('cos dist error')
    pass

try:
    request = words.requesthandler.TfidfOverTimeRequest(dateRange, granularity, word1)
    result = request.execute()
    print('average tfidf over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('tfidf error')
    pass

try:
    request = words.requesthandler.NClosestNeighboursOverTimeRequest(dateRange, granularity, word, N, True)
    result = request.execute()
    print('n closest neighbours over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('n closest error')
    pass

try:
    request = words.requesthandler.PairwiseProbabilitiesOverTimeRequest(dateRange, granularity, word1, word2)
    result = request.execute()
    print('pairwise probabilities over time')
    for k,v in result.items():
        print(v.yTitle)
        print(v.xValues)
        print(v.yValues)
except:
    print('pairwise error')
    pass    

try:
    request = words.requesthandler.WordFrequencyOverTimeRequest(dateRange, granularity, word2)
    result = request.execute()
    print('word frequency over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('frequency error')
    pass

try:
    request = words.requesthandler.RelativeWordFrequencyOverTimeRequest(dateRange, granularity, word2)
    result = request.execute()
    print('relative word frequency over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('rel frequency error')
    pass

try:
    request = words.requesthandler.AverageValenceFiveWordsOverTimeRequest(dateRange, granularity)
    result = request.execute()
    print('average valence top five words over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('valence 5 error')
    pass

try:
    request = words.requesthandler.AverageArousalFiveWordsOverTimeRequest(dateRange, granularity)
    result = request.execute()
    print('average arousal top five words over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('arousal 5 error')
    pass

try:
    request = words.requesthandler.AverageValenceOverTimeRequest(dateRange, granularity)
    result = request.execute()
    print('average valence over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('valence error')
    pass

try:                   
    request = words.requesthandler.AverageArousalOverTimeRequest(dateRange, granularity)
    result = request.execute()
    print('average arousal over time')
    print(result.xValues)
    print(result.yValues)
except:
    print('arousal error')
    pass