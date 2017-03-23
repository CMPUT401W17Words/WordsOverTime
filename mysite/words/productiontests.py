from datetime import date
import dataretrieval
import requesthandler
import databaseinput
from models import Document_Data, Word_Data

dateRange = (date(2000, 5, 19), date(2008, 10, 11))
granularity = 'Year'
word1 = 'credit'
word2 = 'company'
request = words.requesthandler.CosDistanceOverTimeRequest(dateRange, granularity, word1, word2, False)
result = request.execute()
print('cos distance over time')
print(result.xValues)
print(result.yValues)
result.generateCSV(self.csvFilePath)