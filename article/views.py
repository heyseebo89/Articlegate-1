from django.core.checks import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post, Comment, Tag
from django.contrib.auth.decorators import login_required
from .forms import CustomForm
# Create your views here.

def home(request):
    check = 0
    list_tags = []
    l_tags_intial = Tag.objects.all()
    for i in l_tags_intial:
        if i.tag not in list_tags:
            list_tags.append(i.tag)
    print(list_tags)
    context = {
            'posts': Post.objects.order_by('-date_posted')[:50],
            'list_tags':list_tags,
            # stores top 50 liked objects
        }
    return render(request , 'article/home1.html', context)


def tagName(request, tagname):
    list_tag_obj = []
    objs = Post.objects.all()
    for obj in objs:
        if obj.tags == tagname:
            list_tag_obj.append(obj)
    context = {
        'list_tag_obj':list_tag_obj,
        'tagname':tagname
    }
    return render(request, 'article/tag_search.html', context)


def aboutus(request):
    return render(request,'article/aboutus.html')

def fullArticle(request,title,article_id):
    # print(article_id)
    # user = User.objects.get(id=request.user.pk)
    post = Post.objects.get(id=article_id)
    comments = post.comment_set.order_by('-date_posted')
    context = {
        'post':post,
        'comments':comments,
        # 'user':user
        }


    if request.method == 'POST':
        content = request.POST.get('addComment')
        com = Comment(post=post,comment=content)
        com.author = request.user.username
        com.image_url = request.user.profile.image.url
        com.save()
        # return render(request, 'article/full_article1.html', context=context)
        return redirect(f'../../{post.title}/{post.id}')

    return render(request, 'article/full_article1.html', context=context)

@login_required
def addArticle(request):
    newPost = Post()
    user = User.objects.get(id=request.user.pk)
    if request.method != 'POST':
        form = CustomForm()
    else:
        newPost.author = user
        newPost.title = request.POST['title']
        newPost.about = request.POST['about']
        newPost.content = request.POST['content']
        newPost.tags = request.POST['tags']
        newPost.save()
        t = request.POST['tags']
        t1 = Tag()
        t1.post = newPost
        t1.tag  = request.POST['tags']
        t1.save()
        return redirect('../../../')

    context = {
        'form':form
    }
    return render(request , 'article/add_article.html',context)

@login_required
def editArticle(request,title, article_id):
    post = Post.objects.get(id=article_id)
    if request.user.pk == post.author.pk:
        comments = post.comment_set.all()
        data_original = {
            'title': post.title,
            'about' : post.about,
            'content': post.content,
        }
        if request.method != 'POST':
            form = CustomForm(data = data_original)
        else:
            post.title = request.POST['title']
            post.about = request.POST['about']
            post.content = request.POST['content']
            post.save()
            return redirect('../../../')
        context = {
            'form':form,
            'post':post,
            'comments':comments,
            }
        return render(request, 'article/edit_article.html', context=context)
    else:
        return HttpResponse('<p> You are not authorised to edit this article </p>') 


def search(request):
    query = request.GET['query']
    if len(query) == 0 or len(query) > 32:
        allposts = Post.objects.none()
    else:
        postTitle = Post.objects.filter(title__icontains=query)
        postContent = Post.objects.filter(content__icontains=query)
        allposts = postTitle.union(postContent)
    context = {
        'allposts':allposts,
        'query':query
    }
    return render(request, 'article/search.html',context)



def viewProfile(request, username):
    user = User.objects.get(username = username)
    context = {
        'user':user
    }
    return render(request, 'article/profilepublic.html',context)