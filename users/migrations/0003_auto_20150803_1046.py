# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_delete_usermodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_project',
            new_name='project',
        ),
    ]
