from django.db import models
from django.contrib.auth.models import AbstractUser

class App(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField()


    def __str__(self) -> str:
        return self.name

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profiles/')
    points = models.IntegerField(default=0)
    tasks_completed = models.ManyToManyField(App, through='TaskCompletion')

    def __str__(self):
        return self.username

class TaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s- %s" % (self.user, self.app)





