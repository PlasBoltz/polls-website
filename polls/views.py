from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
import datetime
# classes to handle auth
class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = '../'

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_message = "Your profile was created successfully"
    success_url = '../'

def Profile(request):
    user = request.user
    try:
        if request.method == "POST":
            print("profile changed")
            data= request.POST
            user.username = data.get("username")
            user.profile.display_name = data.get("display_name")
            user.save()
            user.profile.save()
    except:
        # display error
        pass

    return render(request, 'polls/profile.html', {
        'user': user,
        'user_posts' : user.profile.get_posts()
        })

def Change_Password(request):
    user = request.user
    try:
        if request.method == "POST":
            data= request.POST
            p1 = data.get("p1")
            p2 = data.get("p2")
            if p1 == p2:
                user.set_password(p1)
                user.save()
    except:
        pass
    return render(request, 'polls/change_password.html', {
        'user' :user}
    )
def Make_Post(request):
    user= request.user
    try:
        if request.method =="POST":
            print("triggered")
            data=request.POST
            post_title = data.get("title")
            post_content = data.get("content")
            post_metatags = data.get("metatags")

            new = Post.create(user.profile)
            new.set_title(post_title)
            new.set_content(post_content)
            for meta_tag in post_metatags.split():
                new.add_meta_tag(meta_tag)
            new.save()
            user.profile.add_post(new)
            user.profile.save()
            print(Post.objects.all())
            return redirect('/polls/')
    except:
        pass
    return render(request, 'polls/make_post.html', {'user' :user})

def IndexView(request):
    user = request.user
    return render(request, "polls/index.html", {
        "user" : user,
        "posts" : Post.objects.all()[::-1]
    })

def UserView(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, "polls/user.html", {
        "user_posts" : [Post.objects.get(pk=int(id)) for id in user.profile.posts.split()]
    })

def PostView(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    try:
        if request.method == "POST":
            if "submit" in request.POST:
                data=request.POST
                comment_content = data.get("comment")
                new = Comment.create(user.profile)
                new.set_content(comment_content)
                new.save()

                post.add_comment(new)
                post.save()
            else:
                print("pass")
                post.set_viewable(False)
                post.save()
    except:
        pass

    return render(request, "polls/post.html",{
        "user" :user,
        "post" : post,
        "comments" : [Comment.objects.get(pk=int(id)) for id in post.comments.split()]
    })

def CommentView(request, pk):
    main = Comment.objects.get(pk=pk)

    user = request.user

    try:
        if request.method == "POST":
            
            if "delete" in request.POST:
                print("bruh")
                main.set_viewable(False)
                main.save()
                
            else:
                data=request.POST
                comment_content = data.get("comment")
                new = Comment.create(user.profile)
                new.set_content(comment_content)
                new.save()

                main.add_comment(new)
                main.save()
                
    except:
        pass

    return render(request, "polls/comment.html", {
        "user" : user,
        "main_comment": main,
        "comments" : [Comment.objects.get(pk=int(id)) for id in main.comments.split()]
    })

def SearchView(request):
    results = []
    def searchValue(terms, post):
        value = 0
        for term in terms:
            if term in post.meta_tags:
                value += 2
            if term in post.title:
                value += 1
        return value

    searched = False
    try:
        if request.method == "POST":
            searched = True
            data = request.POST
            term = data.get("search-term")
            results = Post.objects.all()
            results = sorted(results, key = lambda x : searchValue(term, x), reverse=True)
            return render(request, "polls/search.html", {
        "results" : results
    })
    except:
        pass

    return render(request, "polls/search.html", {"results":results})
