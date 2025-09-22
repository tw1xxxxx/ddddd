from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_model_body_type_remove_model_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='year',
            field=models.IntegerField(verbose_name='Год выпуска', null=True),
        ),
    ] 