# Generated by Django 2.2.13 on 2020-12-17 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('star', models.IntegerField()),
                ('pub_time', models.DateTimeField()),
            ],
        ),
    ]
