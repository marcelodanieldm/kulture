
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Post, BlogCategory, Tag
from django.utils import timezone

from django.core.paginator import Paginator

def blog_list(request):
	posts_qs = Post.objects.filter(published=True).order_by('-created_at')
	paginator = Paginator(posts_qs, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	categories = BlogCategory.objects.all()
	return render(request, 'blog/blog_list.html', {'page_obj': page_obj, 'categories': categories})

def blog_detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'blog/blog_detail.html', {'post': post})

def is_colaborador(user):
	return hasattr(user, 'user_type') and user.user_type in ['colaborador', 'collaborator']

@login_required
@user_passes_test(is_colaborador)
def home_colaborador(request):
	posts = Post.objects.filter(author=request.user).order_by('-created_at')
	return render(request, 'blog/home_colaborador.html', {'posts': posts})

@login_required
@user_passes_test(is_colaborador)
def post_create(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		content = request.POST.get('content')
		category_id = request.POST.get('category')
		scheduled_for = request.POST.get('scheduled_for')
		tag_ids = request.POST.getlist('tags')
		thumbnail = request.FILES.get('thumbnail')
		category = BlogCategory.objects.get(pk=category_id) if category_id else None
		post = Post.objects.create(
			title=title,
			content=content,
			author=request.user,
			category=category,
			scheduled_for=scheduled_for if scheduled_for else None,
			created_at=timezone.now(),
			published=True,
			thumbnail=thumbnail
		)
		if tag_ids:
			post.tags.set(tag_ids)
		return redirect('home_colaborador')
	categories = BlogCategory.objects.all()
	tags = Tag.objects.all()
	return render(request, 'blog/post_form.html', {'categories': categories, 'tags': tags})

@login_required
@user_passes_test(is_colaborador)
def post_update(request, post_id):
	post = get_object_or_404(Post, pk=post_id, author=request.user)
	if request.method == 'POST':
		post.title = request.POST.get('title')
		post.content = request.POST.get('content')
		category_id = request.POST.get('category')
		post.category = BlogCategory.objects.get(pk=category_id) if category_id else None
		post.scheduled_for = request.POST.get('scheduled_for') or None
		thumbnail = request.FILES.get('thumbnail')
		if thumbnail:
			post.thumbnail = thumbnail
		post.save()
		tag_ids = request.POST.getlist('tags')
		if tag_ids:
			post.tags.set(tag_ids)
		else:
			post.tags.clear()
		return redirect('home_colaborador')
	categories = BlogCategory.objects.all()
	tags = Tag.objects.all()
	return render(request, 'blog/post_form.html', {'post': post, 'categories': categories, 'tags': tags})

@login_required
@user_passes_test(is_colaborador)
def post_delete(request, post_id):
	post = get_object_or_404(Post, pk=post_id, author=request.user)
	if request.method == 'POST':
		post.delete()
		return redirect('home_colaborador')
	return render(request, 'blog/post_confirm_delete.html', {'post': post})
