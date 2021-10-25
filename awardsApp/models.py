from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from profiles.models import Profile
from tinymce.models import HTMLField




# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length = 30)
    project_image = CloudinaryField('Project image')
    description = HTMLField()
    technologies = models.CharField(max_length=200, blank=True)
    project_link = models.URLField()
    publisher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True, null = True)
    

    def __str__(self):
        return self.title

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    

    @classmethod
    def display_all_projects(cls):
        return cls.objects.all()

    @classmethod 
    def search_project(cls,project_title):
        return Project.objects.filter(title__icontains = project_title)

 
    @classmethod
    def get_user_projects(cls,profile):
        return cls.objects.filter(profile=profile)
     
    @classmethod
    def update_project(cls, proj_id, updated_proj_title):
        project = cls.objects.filter(id = proj_id).update(title = updated_proj_title)
        return project

    class Meta:
        ordering = ['-date_published']



class Review(models.Model):
    project = models.ForeignKey(Project, on_delete= models.CASCADE, related_name='reviews')
    review = models.TextField()
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    reviewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.project} Review'


    def save_review(self):
        self.save()

    def delete_review(self):
            self.delete()

    @classmethod
    def update_review(cls, proj_id, updated_review):
        review = cls.objects.filter(id = proj_id).update(review = updated_review)
        return review


    class Meta:
        ordering = ['-reviewed_on']


class Rating(models.Model):
   
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings', null=True)
    design = models.IntegerField(blank=True)
    usability = models.IntegerField(blank=True)
    content = models.IntegerField(blank=True)
    score = models.FloatField(default=0, blank=True)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')


    def __str__(self):
            return f'{self.project} Rating'

    def save_rating(self):
        self.save()

    def delete_rating(self):
        self.delete()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings

    @classmethod
    def update_rating(cls, reviewId, newReview):
        design_rating = cls.objects.filter(id = reviewId).update(design = newReview)
        # usability = cls.objects.filter(id = reviewId).update(usability = newReview)
        # content = cls.objects.filter(id = reviewId).update(content = newReview)
        return design_rating
