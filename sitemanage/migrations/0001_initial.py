# Generated by Django 3.1 on 2021-02-20 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(max_length=100, verbose_name='meta_title')),
                ('meta_discription', models.CharField(max_length=300, verbose_name='meta_discription')),
                ('meta_keywords', models.CharField(max_length=300, verbose_name='SEOキーワード')),
                ('author', models.CharField(max_length=30, verbose_name='管理者')),
                ('top_title', models.CharField(max_length=100, verbose_name='Topページタイトル')),
                ('top_subtitle', models.CharField(max_length=300, verbose_name='Topページサブタイトル')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='sites.site', verbose_name='Site')),
            ],
        ),
    ]
