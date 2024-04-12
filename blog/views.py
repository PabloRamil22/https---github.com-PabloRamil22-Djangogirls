from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required





@login_required
def toggle_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if request.user in post.favoritos.all():
            post.favoritos.remove(request.user)
            favorited = False
        else:
            post.favoritos.add(request.user)
            favorited = True
        post.save()
        return JsonResponse({'favorited': favorited})
    return JsonResponse({'error': 'Invalid request'})




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        author = request.POST['author']
        text = request.POST['text']
        Comment.objects.create(post=post, author=author, text=text)
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/comments.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
