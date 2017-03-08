from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class Corpus(models.Model):
  start_date = models.DateField()
  end_date = models.DateField()
  
class Word(models.Model):
  word = models.CharField(primary_key=True, max_length=255)
  #valence = models.DecimalField(max_digits=14, decimal_places=12)
  #arousal = models.DecimalField(max_digits=14, decimal_places=12)
  #corpusFrequency = models.DecimalField(max_digits=14, decimal_places=12)
  #idf = models.DecimalField(max_digits=14, decimal_places=12)  
  #dominance = models.DecimalField(max_digits=14, decimal_places=12)
  #concreteness = models.DecimalField(max_digits=14, decimal_places=12)
  #aoa = models.DecimalField(max_digits=14, decimal_places=12)
  
class Document(models.Model):
  article_id = models.IntegerField(primary_key=True, default=-1)
  words = models.ManyToManyField(Word, through='WordInDocument')
  #language = models.CharField(max_length=255)
  #province = models.CharField(max_length=255)
  #city = models.CharField(max_length=255)
  #country = models.CharField(max_length=255)
  publicationDate = models.DateField()
  #wordCount = models.IntegerField()
  #word_one = models.ForeignKey('WordInDocument', on_delete=models.CASCADE)
  #word_two = models.ForeignKey('WordInDocument', on_delete=models.CASCADE)
  #word_three = models.ForeignKey('WordInDocument', on_delete=models.CASCADE)
  #word_four = models.ForeignKey('WordInDocument', on_delete=models.CASCADE)
  #word_five = models.ForeignKey('WordInDocument', on_delete=models.CASCADE)
  #average_arousal = models.DecimalField(max_digits=14, decimal_places=12)  
  #average_valence = models.DecimalField(max_digits=14, decimal_places=12)  
  #average_arousal_five_highest = models.DecimalField(max_digits=14, decimal_places=12)  
  #average_valence_five_highest   = models.DecimalField(max_digits=14, decimal_places=12)

class WordInDocument(models.Model):
  class Meta:
    unique_together = (('word', 'document'),) 
  word = models.ForeignKey(Word, on_delete=models.CASCADE)
  document = models.ForeignKey(Document, on_delete=models.CASCADE)
  #documentFrequency = models.DecimalField(max_digits=14, decimal_places=12)
  #tf = models.DecimalField(max_digits=14, decimal_places=12)
  tfidf = models.DecimalField(max_digits=14, decimal_places=12)