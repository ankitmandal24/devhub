from django.db import models
import uuid
from users.models import Profile
# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null = True, blank = True)
    source_link = models.CharField(max_length=2000, null = True, blank = True)
    tags = models.ManyToManyField('Tag', blank = True)
    vote_total = models.IntegerField(default=0, null = True, blank = True)
    vote_ratio = models.IntegerField(default=0, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(unique=True,default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner_id', flat=True)
        return queryset

    @property
    def getvotecount(self):
        reviews = self.review_set.all()
        upvotes = reviews.filter(value='up').count()
        totalvotes = reviews.count()

        ratio = (upvotes/totalvotes)*100
        self.vote_total = totalvotes
        self.vote_ratio = ratio
        self.save()

class Review(models.Model):
    Vote_Type = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,null = True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=200, choices= Vote_Type)

    class meta:
        unique_together = [['owner','project']]
    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(unique=True,default=uuid.uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.name
