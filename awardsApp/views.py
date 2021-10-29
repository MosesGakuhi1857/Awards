import statistics
from awardsApp.models import Project, Profile, Rating, Review
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UpdateUserProjectForm, UserRegistrationForm, PublishProjectForm, RatingsForm, ReviewForm
from .email import send_welcome_email
from django.template import loader
from django.db.models import Avg
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectSerializer
from rest_framework import viewsets
from rest_framework import status
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


# Create your views here
def register(request):
    reg_form = UserRegistrationForm()

    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            user = reg_form.cleaned_data.get('username')
            email = reg_form.cleaned_data['email']
            messages.success(request, 'Account was created for ' + user)
            # send_welcome_email(user,email)
            return redirect('login')
        else:
            reg_form = UserRegistrationForm()

    
    return render(request, 'registration/sign_up.html', {'reg_form': reg_form})


def login_user(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'registration/login.html')


def home(request):
    projects= Project.objects.all()
    top_project = Rating.objects.order_by('-score').first()
       
    context = {
        "projects": projects,
        "top_project":top_project
    }
    return render(request, 'awards/index.html', context)


@login_required(login_url='login')
def publishProject(request):
    current_user = request.user
    if request.method == 'POST':
        pForm = PublishProjectForm(request.POST, request.FILES)
        if pForm.is_valid():
            project_post = pForm.save(commit=False)
            project_post.publisher = current_user.profile
            project_post.save()
            return redirect('home')
    else:
        pForm = PublishProjectForm()

   
    title = 'Publish'
    context = {
        "title": title,
        "pForm":pForm
    }
    return render(request, 'awards/submit-project.html', context)


class UpdateProjectView(UpdateView):
        model=Project
        form_class =UpdateUserProjectForm
        template_name ='awards/editProject.html'
        
        def get_queryset(self): 
            return Project.objects.all()


        def get_success_url(self):
       
            return reverse_lazy('home') 


@login_required(login_url='login')
def projectDetails(request, id):
    current_user = request.user
    project = get_object_or_404(Project, id=id)
    rating = Rating.objects.filter(project_id=id)
    review = Review.objects.filter(project_id=id)

    
    #Total ratings for a single project
    average_design = Rating.objects.filter(id=id).aggregate(Avg('design'))
    average_usability = Rating.objects.filter(id=id).aggregate(Avg('usability'))
    average_content = Rating.objects.filter(id=id).aggregate(Avg('content'))
    average_score = Rating.objects.filter(id=id).aggregate(Avg('score'))


     # Ratings 
    design = Rating.objects.filter(project_id=id).values_list('design',flat=True)
    usability = Rating.objects.filter(project_id=id).values_list('usability',flat=True)
    content = Rating.objects.filter(project_id=id).values_list('content',flat=True)
    if ( len(design) > 0) and ( len(usability) > 0) and ( len(content) > 0):

        avg_design = round(statistics.mean(design),2)
        avg_usability = round(statistics.mean(usability),2)
        avg_content = round(statistics.mean(content),2)
        total_score = float(avg_usability + avg_design + avg_content)
        avg_score =round((total_score/3),2 )


        
    else:
        avg_design = 0
        avg_usability = 0
        avg_content = 0
        total_score = 0
        avg_score = 0
           

    
    #Review Form
    if request.method == 'POST':
        reviewForm = ReviewForm(request.POST, request.FILES)
        if reviewForm.is_valid():
            project_review = reviewForm.save(commit=False)
            project_review.project = project
            project_review.reviewed_by = current_user
            project_review.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        reviewForm = ReviewForm()
   

    #Rating Form
    if request.method == 'POST':
        rateForm = RatingsForm(request.POST, request.FILES)
        if rateForm.is_valid():
            project_rating = rateForm.save(commit=False)
            project_rating.project = project
            project_rating.rated_by = current_user
            project_rating.save()
              # Ratings 
            design = Rating.objects.filter(project_id=id).values_list('design',flat=True)
            usability = Rating.objects.filter(project_id=id).values_list('usability',flat=True)
            content = Rating.objects.filter(project_id=id).values_list('content',flat=True)
            if ( len(design) > 0) and ( len(usability) > 0) and ( len(content) > 0):

                avg_design = round(statistics.mean(design),2)
                avg_usability = round(statistics.mean(usability),2)
                avg_content = round(statistics.mean(content),2)
                total_score = float(avg_usability + avg_design + avg_content)
                avg_score =round((total_score/3),2 )

                # percentage_design= avg_design * 10
                # percentage_usability= avg_usability * 10
                # percentage_content= avg_content * 10
                # percentage_score= avg_score * 10

            else:
                avg_design = 0
                avg_usability = 0
                avg_content = 0
                total_score = 0
                avg_score = 0


            project_rating.average_design = avg_design
            project_rating.average_usability = avg_usability
            project_rating.average_content = avg_content
            project_rating.score = avg_score
            project_rating.save()
        
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        rateForm = RatingsForm()
   
    title = 'Project Details'
    context = {
        "title": title,
        "project": project,
        "reviewForm":reviewForm,
        "rateForm":rateForm,
        "rating":rating,
        "design":avg_design,
        "usability":avg_usability,
        "content":avg_content,
        "score":avg_score,
       
      
    }
    # template = loader.get_template('awards/project-details.html')
    # return HttpResponse(template.render(context, request))

    return render(request, 'awards/project-details.html', context )


def search_project(request):
    if 'project_title' in request.GET and request.GET["project_title"]:
        search_project = request.GET.get("project_title")
        print(search_project)
        searched_projects = Project.search_project(search_project)
        print(searched_projects)
        message = f"{search_project}"

        context = {
            "message":message,
            "searched_projects": searched_projects
        }


        return render(request, 'awards/search.html', context)

    else:
        message = "You haven't searched for any term"
        return render(request, 'awards/search.html',{"message":message})


# API
class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializers = ProfileSerializer(profiles, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = Profile(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = Project(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




class ProjectDescription(APIView):
    permission_classes = (IsAuthenticated,)
    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)

    
    def put(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)