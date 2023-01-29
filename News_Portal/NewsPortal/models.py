from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0.0)

    def update_rating(self):
        agg_rating_author_post = self.post_set.all().aggregate(Avg('rating')).get('rating__avg') * 3
        agg_rating_author_comment = self.user.comment_set.all().aggregate(Avg('rating')).get('rating__avg')
        agg_rating_author_post_comment = \
            Comment.objects.filter(post__author=self.id).aggregate(Avg('rating')).get('rating__avg')
        self.user_rating = agg_rating_author_post + agg_rating_author_comment + agg_rating_author_post_comment
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):

    post = 'Post'
    news = 'News'
    POST_OR_NEWS = [
        (post, 'Post'),
        (news, 'News')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_or_news = models.CharField(max_length=4, choices=POST_OR_NEWS, default=post)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    headline = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.headline.title()}:{self.text[:20]}'

    def like(self):
        self.rating += 1.0

    def dislike(self):
        self.rating -= 1.0

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1.0

    def dislike(self):
        self.rating -= 1.0
