# Generated by Django 5.0.3 on 2024-05-07 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HastaneUyg', '0007_randevu_idrandevu'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='doctor',
            table='doktorlar2',
        ),
        migrations.AlterModelTable(
            name='hasta',
            table='hastalar2',
        ),
        migrations.AlterModelTable(
            name='randevu',
            table='randevular2',
        ),
        migrations.AlterModelTable(
            name='tibbiraporlar',
            table='tibbiraporlar2',
        ),
        migrations.AlterModelTable(
            name='yonetici',
            table='yonetici2',
        ),
    ]
