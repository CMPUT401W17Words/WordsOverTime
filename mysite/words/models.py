from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class SentimentDictionary(models.Model):
    word = models.CharField(max_length=255, primary_key=True)
    valence = models.DecimalField(max_digits=15, decimal_places=13)
    arousal = models.DecimalField(max_digits=15, decimal_places=13)
    dominance = models.DecimalField(max_digits=15, decimal_places=13)
    concreteness = models.DecimalField(max_digits=15, decimal_places=13)
    aoa = models.DecimalField(max_digits=15, decimal_places=13)

class ArticlesCan(models.Model):
    #id is auto included
    articleID = models.PositiveIntegerField()
    language = models.CharField(max_length=255)
    province = models.CharField(max_length=2)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=3)
    publication_date = models.DateField()
    word_count = models.PositiveIntegerField()
    parsed_article = models.TextField()

class DocumentData(models.Model):
    articleID = models.PositiveIntegerField(primary_key = True)
    language = models.CharField(max_length=255)
    province = models.CharField(max_length=2)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=3)
    publication_date = models.DateField()
    word_count = models.PositiveIntegerField()
    word_one = models.CharField(max_length=255, null=True, default="")
    word_two = models.CharField(max_length=255, null=True, default="")
    word_three = models.CharField(max_length=255, null=True, default="")
    word_four = models.CharField(max_length=255, null=True, default="")
    word_five = models.CharField(max_length=255, null=True, default="")
    average_arousal_doc = models.DecimalField(max_digits=13, decimal_places=12)
    average_valence_doc = models.DecimalField(max_digits=13, decimal_places=12)
    average_arousal_words = models.DecimalField(max_digits=13, decimal_places=12, null=True, blank=True)
    average_valence_words = models.DecimalField(max_digits=13, decimal_places=12, null=True, blank=True)
  
class WordData(models.Model):
    word = models.CharField(max_length=255)
    articleID = models.PositiveIntegerField()
    word_count = models.PositiveIntegerField()
    term_frequency = models.DecimalField(max_digits=14, decimal_places=12, null=True, blank=True)
    tfidf = models.DecimalField(max_digits=14, decimal_places=12, null=True, blank=True)

    class Meta:
        unique_together = (("word", "articleID"),)

class CorpusData(models.Model):
    corpusID = models.PositiveIntegerField(primary_key = True)
    start_date = models.DateField()
    end_date = models.DateField()