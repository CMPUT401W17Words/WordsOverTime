from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
  
class Sentiment_Dict(models.Model):
  word = models.CharField(primary_key=True, max_length=255)
  valence = models.DecimalField(max_digits=14, decimal_places=12)
  arousal = models.DecimalField(max_digits=14, decimal_places=12) 
  dominance = models.DecimalField(max_digits=14, decimal_places=12)
  concreteness = models.DecimalField(max_digits=14, decimal_places=12)
  aoa = models.DecimalField(max_digits=14, decimal_places=12)  
  
class Articles_Can(models.Model):
  id = models.IntegerField(primary_key=True, default=-1)
  article_id = models.IntegerField()
  language = models.CharField(max_length=255)
  province = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  country = models.CharField(max_length=255)
  publicationDate = models.DateField()
  wordCount = models.IntegerField()
  parsed_article = models.TextField()
  
class Document_Data(models.Model):
  article_id = models.IntegerField(primary_key=True, default=-1)
  language = models.CharField(max_length=255)
  province = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  country = models.CharField(max_length=255)
  publication_Date = models.DateField()
  word_count = models.IntegerField()
  word_one = models.CharField(max_length=255)
  word_two = models.CharField(max_length=255)
  word_three = models.CharField(max_length=255)
  word_four = models.CharField(max_length=255)
  word_five = models.CharField(max_length=255)
  average_arousal_doc = models.DecimalField(max_digits=14, decimal_places=12)  
  average_valence_doc = models.DecimalField(max_digits=14, decimal_places=12)  
  average_arousal_words = models.DecimalField(max_digits=14, decimal_places=12)  
  average_valence_words   = models.DecimalField(max_digits=14, decimal_places=12)  
  
class Word_Data(models.Model):
  word = models.CharField(max_length=255)
  #word = models.CharField(primary_key=True, max_length=255)
  article_id = models.IntegerField()
  word_count = models.IntegerField()
  term_frequency = models.DecimalField(max_digits=14, decimal_places=12) 
  tfidf = models.DecimalField(max_digits=14, decimal_places=12) 

  class Meta:
    unique_together = (("word", "article_id"),)  
    
class Corpus_Data(models.Model):
  start_date = models.DateField()
  end_date = models.DateField()  