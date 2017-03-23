import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import words.requesthandler
from words.models import Document_Data, Word_Data
from datetime import date

dateRange = (date(2000, 5, 19), date(2002, 10, 11))
granularity = 'Year'
word1 = 'credit'
word2 = 'company'

request = words.requesthandler.CosDistanceOverTimeRequest(dateRange, granularity, word1, word2, False)
result = request.execute()
print('cos distance over time')
print(result.xValues)
print(result.yValues)

request = words.requesthandler.TfidfOverTimeRequest(dateRange, granularity, word1)
result = request.execute()
print('average tfidf over time')
print(result.xValues)
print(result.yValues)

N = 2
request = words.requesthandler.NClosestNeighboursOverTimeRequest(dateRange, granularity, word, N, True)
result = request.execute()
print('n closest neighbours over time')
print(result.xValues)
print(result.yValues)

request = words.requesthandler.PairwiseProbabilitiesOverTimeRequest(dateRange, granularity, word1, word2)
result = request.execute()
print('pairwise probabilities over time')
for k,v in result.items():
    print(v.yTitle)
    print(v.xValues)
    print(v.yValues)
    
request = words.requesthandler.WordFrequencyOverTimeRequest(dateRange, granularity, 'bird')
result = request.execute()
print('word frequency over time')
print(result.xValues)
print(result.yValues)

request = words.requesthandler.RelativeWordFrequencyOverTimeRequest(dateRange, granularity, 'bird')
result = request.execute()
print('relative word frequency over time')
print(result.xValues)
print(result.yValues) 