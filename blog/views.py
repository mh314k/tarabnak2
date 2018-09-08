from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from taggit.models import Tag
# Create your views here.
from.models import *
from .forms import CommentForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import datetime

class BlogPostClassView(ListView):
    model = Post
    queryset = Post.objects.filter(Status='P')
    template_name = "blog/BlogIndex.html"
    paginate_by = 2
    context_object_name = 'Posts'


def taglistview(request, tagname):
    tag= get_object_or_404(Tag,name=tagname)
    Posts=Post.objects.filter(Tags__in=[tag])
    paginator = Paginator(Posts,2)
    page = request.GET.get('page')
    try:
        Posts = paginator.get_page(page)
    except PageNotAnInteger:
        Posts=paginator.get_page(paginator.num_pages)
    except EmptyPage:
        Posts=paginator.get_page(1)
    return render(request, 'blog/BlogTagList.html',
                  context={'Posts':Posts, 'tag':tagname, 'paginator':paginator})

def postView(request,year,month,day,slug):
    post = get_object_or_404(Post,
                             PublishTime__year=year,
                             PublishTime__month=month,
                             PublishTime__day=day,
                             Slug=slug,
                             Status='P')
    if request.method == 'POST':
        form1 = CommentForm(request.POST)
        if form1.is_valid():
            comm1 = Comment()
            comm1 = form1.save(commit=False)
            comm1.PostTo=post
            if request.POST['reply']!="":
                r=Comment.objects.filter(pk=int(request.POST['reply'])).first()
                comm1.CommentTo=r
            comm1.save()
            comm1.CommentTime=datetime.datetime.now()
    form = CommentForm()

    comments = post.COMMENTS.filter(CommentStatus='A',CommentTo__CommentBody__isnull=True)

    return render(request,
                  template_name='blog/BlogPost.html',
                  context={'Post':post, 'Comments':comments, 'form': form})
    pass

def catlistview(request, slug):
    cat= get_object_or_404(Category,Slug=slug)
    Posts=Post.objects.filter(Categories__in=[cat])
    paginator = Paginator(Posts,2)
    page = request.GET.get('page')
    try:
        Posts = paginator.get_page(page)
    except PageNotAnInteger:
        Posts=paginator.get_page(paginator.num_pages)
    except EmptyPage:
        Posts=paginator.get_page(1)
    return render(request, 'blog/BlogTagList.html',
                  context={'Posts':Posts, 'cat':cat.Name, 'paginator':paginator})