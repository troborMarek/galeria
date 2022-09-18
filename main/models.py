from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=80, )
    surname = models.CharField(max_length=80, default='zalogowany')
    email = models.EmailField(default='zalogowany@zalogowany.pl')
    bio = models.TextField()

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    price = models.FloatField()
    apr_by_admin = models.BooleanField('Approved', default=False)

    def __str__(self):
        return f'{self.user}=> {self.title}'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    score = models.IntegerField(default=0,
                                validators=[
                                    MaxValueValidator(5),
                                    MinValueValidator(0),
                                ]
                                )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.score


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    start_price = models.FloatField()
    end_price = models.FloatField()
    min_price = models.FloatField()
    till = models.DateTimeField()
    winner = models.ForeignKey(User, null=True, related_name='winner', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} sell=> {self.post} => {self.till}'



