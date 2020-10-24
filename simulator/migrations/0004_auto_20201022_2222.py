# Generated by Django 3.1.2 on 2020-10-22 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simulator', '0003_auto_20201022_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=10000, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('units', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('action', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulator.stock')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='dateBuy',
            new_name='dateBought',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='UnitSold',
            new_name='unitSold',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='dateSell',
        ),
        migrations.AddField(
            model_name='purchase',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
