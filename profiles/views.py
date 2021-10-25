from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Profile
from awardsApp.models import Project
from .forms import UpdateUserProfileForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy




# Create your views here.


def userProfile(request, username):
    otherUser = get_object_or_404(User, username=username)
    userProfile = Profile.objects.get(user=otherUser)
    myProfile = Profile.objects.get(user=request.user)
    projects = Project.objects.filter(publisher = otherUser.profile)

    if userProfile.user in myProfile.following.all():
            follow = True
    else:
        follow = False

    if myProfile.user in userProfile.followers.all():
        follower = True
    else:
        follower = False

    context ={
        "otherUser":otherUser,
        "profile":userProfile,
        "projects": projects,
        "follow":follow,
        "follower": follower,  
                  
    }


    return render(request, 'profile/userProfile.html', context)




class UpdateProfileView(UpdateView):
        model=Profile
        slug_field = "username"
        form_class =UpdateUserProfileForm
        template_name ='profile/editProfile.html'
        
        def get_queryset(self): 
            return Profile.objects.all()


        def get_success_url(self):
        
            return reverse_lazy('userProfile',args=[self.request.user.username]) 


def follow_unfollow(request):
    if request.method == 'POST':
            if 'userProf_id' in request.POST:
                userProf_id = request.POST.get('userProf_id')
                userProf = User.objects.get(id=userProf_id) 

                myProf = Profile.objects.get(user=request.user)
                oProf = Profile.objects.get(user=userProf)


                if  oProf.user in myProf.following.all():
                    myProf.following.remove(oProf.user)
                    myProf.save()
                else:
                    myProf.following.add(userProf) 
                    myProf.save()

                if  myProf.user in oProf.followers.all():
                    oProf.followers.remove(myProf.user)
                    oProf.save()
                else:
                    oProf.followers.add(myProf.user)
                    oProf.save()

                return redirect(request.META.get('HTTP_REFERER'))