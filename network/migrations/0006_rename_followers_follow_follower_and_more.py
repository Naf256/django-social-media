# Generated by Django 4.1.6 on 2023-02-13 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_user_followers_remove_user_follows_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='followers',
            new_name='follower',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='followings',
            new_name='following',
        ),
    ]
