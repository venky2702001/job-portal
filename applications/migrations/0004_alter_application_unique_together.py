from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_alter_application_status_delete_notification'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='application',
            unique_together={('candidate', 'job')},
        ),
    ]
