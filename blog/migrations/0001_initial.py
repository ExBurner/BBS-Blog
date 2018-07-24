# Generated by Django 2.0.6 on 2018-07-10 08:21

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11, null=True, unique=True)),
                ('avatar', models.FileField(default='/avatars/default.jpg', upload_to='avatars/')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建日期')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='文章标题')),
                ('abstract', models.CharField(max_length=32, verbose_name='文章摘要')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建日期')),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ArticleToTag',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article', to_field='title', verbose_name='文章题目')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('bid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='个人博客标题')),
                ('theme', models.CharField(max_length=32, verbose_name='博客主题')),
                ('site', models.CharField(max_length=32, verbose_name='个人站点名称')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建日期')),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
                ('parent_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('lid', models.AutoField(primary_key=True, serialize=False)),
                ('is_like', models.BooleanField(default=True)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sort',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='标签名称')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
        ),
        migrations.AddField(
            model_name='articletotag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Tag', to_field='name', verbose_name='文章标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='sort',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Sort'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(through='blog.ArticleToTag', to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='user',
            name='blog',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
