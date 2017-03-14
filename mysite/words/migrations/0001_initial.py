# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 07:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('publicationDate', models.DateField()),
                ('wordCount', models.IntegerField()),
                ('average_arousal', models.DecimalField(decimal_places=12, max_digits=14)),
                ('average_valence', models.DecimalField(decimal_places=12, max_digits=14)),
                ('average_arousal_five_highest', models.DecimalField(decimal_places=12, max_digits=14)),
                ('average_valence_five_highest', models.DecimalField(decimal_places=12, max_digits=14)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('word', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('valence', models.DecimalField(decimal_places=12, max_digits=14)),
                ('arousal', models.DecimalField(decimal_places=12, max_digits=14)),
                ('corpusFrequency', models.DecimalField(decimal_places=12, max_digits=14)),
                ('idf', models.DecimalField(decimal_places=12, max_digits=14)),
                ('dominance', models.DecimalField(decimal_places=12, max_digits=14)),
                ('concreteness', models.DecimalField(decimal_places=12, max_digits=14)),
                ('aoa', models.DecimalField(decimal_places=12, max_digits=14)),
            ],
        ),
        migrations.CreateModel(
            name='WordInDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentFrequency', models.DecimalField(decimal_places=12, max_digits=14)),
                ('tf', models.DecimalField(decimal_places=12, max_digits=14)),
                ('tfidf', models.DecimalField(decimal_places=12, max_digits=14)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.Document')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.Word')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='words',
            field=models.ManyToManyField(through='words.WordInDocument', to='words.Word'),
        ),
        migrations.AlterUniqueTogether(
            name='wordindocument',
            unique_together=set([('word', 'document')]),
        ),
    ]
