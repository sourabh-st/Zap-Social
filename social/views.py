from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView

from django.contrib.auth.decorators import login_required

from social.models import  MyPost, Follower, MyProfile

from django.db.models.query_utils import Q
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login

from django.utils.decorators import method_decorator

from django.contrib.auth.models import User




class Login(View):

    def get(self, request):
        return render(request, 'social/login.html')

    def post(self,request):
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
            
        else:
            error_message = "Phone no. or Password Invalid!"
            return  render(request, 'social/login.html',{'error':error_message })


def logout(request):
    request.session.clear()
    return redirect('/social/login')
#----------------------------------------------------------------------------
###################  SIGN-UP   #############################################

class Signup(View):
    def get(self, request):
        return render(request, 'social/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('first_name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        address = postData.get('address') or ""
        age = postData.get('age') or ""
        status = postData.get('status') or ""
        gender = postData.get('gender') or ""
        try:

            user = User.objects.create_user(phone, email , password)

            user.first_name = first_name
            user.save()
            MyProfile.objects.create(user=user,profilename=first_name, age=age , address = address,status=status,gender=gender)

        except Exception as e:
            return JsonResponse({"error":str(e)})
        


        return redirect('login')


@login_required
def profile_get(request):
    try:
        profile_object = MyProfile.objects.get(user=request.user)
    except MyProfile.DoesNotExist:
        profile_object = MyProfile.objects.create(user = request.user)
    if profile_object.age == None  or profile_object.address == None or profile_object.description == None or profile_object.status == None or profile_object.profilepic == None:
        profile_edit = True
    else:
        profile_edit = False
    context = {
            "profile_edit" : profile_edit,
            "age": profile_object.age,
            "address": profile_object.address,
            "description" : profile_object.description,
            "status":profile_object.status,
            "gender":profile_object.gender,
            "profilepic":profile_object.profilepic
    }
    return render(request,'social/myprofile.html',context)


################################################################################

def HomeView(request):
    followings = []
    suggestions = []
    followers = []
    my_followings = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).exclude(is_superuser = True).order_by("-id")
        try:
            
            user_follower_object = Follower.objects.get(user = request.user)
        except Follower.DoesNotExist:
            user_follower_object = Follower.objects.create(user = request.user)
        
        followers = user_follower_object.followers.all()

        my_followings = User.objects.filter(pk__in=followings)
        print("my_followings",my_followings)
    
    return render(request, "social/connections.html", {
        "suggestions": suggestions,
        "followers" : followers,
        "my_followings" : my_followings,
        })
        
#............................POST_RELATED_VIEWS.........................................
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["pic","subject"]
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required,name="dispatch")
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        return MyPost.objects.filter(Q(uploaded_by = self.request.user)).filter(Q(subject__icontains = si)).order_by("-id")

@method_decorator(login_required,name="dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost



@login_required
def feed_view(request):
    followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
    post = MyPost.objects.filter(uploaded_by__in=followings).order_by("-id")
    
    context = {
        "posts":post,
    }
    return render(request,"social/feeds.html" ,context)



#............................FOLLOWER_VIEWS.........................................
@login_required
def follow(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        print(f".....................User: {user}......................")
        print(f".....................Follower: {request.user}......................")
        try:
            (follower, create) = Follower.objects.get_or_create(user=user)
            follower.followers.add(request.user)
            follower.save()
            return redirect("/social/connections/")
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponseRedirect(reverse('login'))


