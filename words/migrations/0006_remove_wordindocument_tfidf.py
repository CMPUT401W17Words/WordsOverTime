# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0005_auto_20170308_0212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordindocument',
            name='tfidf',
        ),
    ]
