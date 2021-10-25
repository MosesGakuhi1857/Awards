from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Project, Review, Rating

class TestAppModelsClass(TestCase):
    def setUp(self):
        self.frank = User(id=4, username = "frank", email = "frankngumbi@gmail.com",password = "1234567")
        # self.frank.save()

        self.profile = Profile(id=3, user= self.frank, bio='myself',  profile_pic='frank.jpg', location='Nairobi')
        # self.profile.save()

        self.project = Project(id=6,title = 'AIB',project_image = 'aib.jpg', description = 'Its all about', publisher = self.profile)
        # self.project.save()

        self.rating = Rating(id=5,project=self.project, design= 7, usability=8, content=8, score =7.67, rated_by = self.frank)
        # self.review.save_review()

        self.review = Review(id=7,project=self.project, review= 'Great idea', reviewed_by = self.frank)
        # self.review.save_review()
   
    # Teardown
    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Project.objects.all().delete()   
        Rating.objects.all().delete()
        Review.objects.all().delete()


    # Instances

    def test_user_instance(self):
        self.assertTrue(isinstance(self.frank, User))

    def test_profile_instance(self):
         self.assertTrue(isinstance(self.profile, Profile))

    def test_image_instance(self):
        self.assertTrue(isinstance(self.project, Project))

    def test_instance(self):
            self.assertTrue(isinstance(self.rating, Rating))

    def test_instance(self):
            self.assertTrue(isinstance(self.review, Review))



    # Save method
    def test_save_Profile(self):
        self.profile.save()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)> 0)

    def test_save_project(self):
        self.project.save()
        projects = Project.objects.all()
        self.assertTrue(len(projects)> 0)

    def test_save_rating(self):
        self.rating.save_rating()
        rating = Rating.objects.all()
        self.assertTrue(len(rating)> 0)

    def test_save_review(self):
        self.review.save_review()
        reviews = Review.objects.all()
        self.assertTrue(len(reviews)> 0)


    #Update method
    def test_update_profile(self):
        self.profile.save()
        profile = Profile.objects.last().id
        Profile.update_profile(profile,'The man')
        update_profile = Profile.objects.get(id = profile)
        self.assertEqual(update_profile.bio,'The man')

    def test_update_project(self):
        self.project.save()
        project = Project.objects.last().id
        Project.update_project(project, 'ML')
        new = Project.objects.get(id = project)
        self.assertEqual(new.title, 'ML')

    def test_update_rating(self):
        self.rating.save()
        rating = Rating.objects.last().id
        Rating.update_rating(rating, 6)
        update = Rating.objects.get(id = rating)
        self.assertEqual(update.design, 6)

    def test_update_review(self):
        self.review.save()
        review = Review.objects.last().id
        Review.update_review(review, "Great concept")
        update = Review.objects.get(id = review)
        self.assertEqual(update.review, "Great concept")


    

    #Delete Method
    def test_delete_project(self):
        self.project.delete_project()
        after_del = Project.objects.all()
        self.assertEqual(len(after_del),0)



    def test_delete_review(self):
        # before_del = Review.objects.all()
        # self.assertEqual(len(before_del),1)
        self.review.delete_review()
        after_del  = Review.objects.all()
        self.assertTrue(len(after_del)==0)

  
    # search
    def test_search_by_title(self):
            self.project.save()
            project = Project.search_project('AIB')
            self.assertTrue(len(project)== 1)
   