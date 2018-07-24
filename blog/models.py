from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户信息表
    """
    uid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, unique=True, null=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.gif")
    create_time = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)

    blog = models.OneToOneField(to="Blog", to_field="bid", null=True, on_delete=models.CASCADE)  # 与博客建立一对一关系

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    博客信息表
    """
    bid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name="个人博客标题")
    theme = models.CharField(max_length=32, verbose_name="博客主题")
    site = models.CharField(max_length=32, verbose_name="个人站点名称")

    def __str__(self):
        return self.site


class Sort(models.Model):
    """
    博客文章分类信息表
    """
    sid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name="分类标题")

    blog = models.ForeignKey(to="Blog", to_field="bid", on_delete=models.CASCADE)  # 与博客建立一对多关系

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    博客文章标签信息表
    """
    tid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name="标签名称", unique=True)

    blog = models.ForeignKey(to="Blog", to_field="bid", on_delete=models.CASCADE)  # 与博客建立一对多关系

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    博客文章表
    """
    aid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, verbose_name="文章标题")
    abstract = models.CharField(max_length=195, verbose_name="文章摘要")
    create_time = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    content = models.TextField()

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    user = models.ForeignKey(to="User", to_field="uid", verbose_name="作者", on_delete=models.CASCADE)
    sort = models.ForeignKey(to="Sort", to_field="sid", null=True, on_delete=models.CASCADE)
    # 与标签建立多对多关系
    tag = models.ManyToManyField(to="Tag", through="ArticleToTag", through_fields=("article", "tag"))

    def __str__(self):
        return self.title


class ArticleToTag(models.Model):
    aid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="aid", verbose_name="文章题目", on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag", to_field="tid", verbose_name="文章标签", on_delete=models.CASCADE)

    def __str__(self):
        name = self.article.title + "---" + self.tag.name
        return name


class Like(models.Model):
    """
    文章点赞表
    """
    lid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="User", to_field="uid", null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", to_field="aid", null=True, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)


class Comment(models.Model):
    """
    文章评论表
    """
    cid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="User", to_field="uid", null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", to_field="aid", null=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    content = models.CharField(max_length=255, verbose_name="评论内容")

    parent_comment = models.ForeignKey(to="Comment", to_field="cid", null=True, on_delete=models.CASCADE)  # 根评论

    def __str__(self):
        return self.content
