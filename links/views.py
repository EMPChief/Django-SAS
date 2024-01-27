from django.shortcuts import render, redirect, get_object_or_404
from .models import Link, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CategoryForm, LinkForm

@login_required(login_url='/login/')
def links(request):
    query = request.GET.get('query', '')
    selected_category = request.GET.get('category', '')
    selected_status = request.GET.get('status', '')
    selected_priority = request.GET.get('priority', '')
    links = Link.objects.filter(created_by=request.user)

    if query:
        links = links.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(url__icontains=query) |
            Q(category__name__icontains=query)
        )

    if selected_category:
        links = links.filter(category__id=selected_category)

    if selected_status:
        links = links.filter(status=selected_status)

    if selected_priority:
        links = links.filter(priority=selected_priority)

    categories = Category.objects.filter(created_by=request.user)
    status_choices = Link.STATUS_CHOICES
    priority_choices = Link.PRIORITY_CHOICES

    context = {
        'links': links,
        'categories': categories,
        'selected_category': selected_category,
        'selected_status': selected_status,
        'selected_priority': selected_priority,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
    }
    return render(request, 'links/links.html', context)

@login_required(login_url='/login/')
def categories(request):
    categories = Category.objects.filter(created_by=request.user)
    context = {'categories': categories}
    return render(request, 'links/categories.html', context)

@login_required(login_url='/login/')
def create_category(request):
    title = 'Create Category'
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/links/categories/')
    else:
        form = CategoryForm(user=request.user)

    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'links/create_category.html', context)

@login_required(login_url='/login/')
def create_link(request):
    title = 'Create Link'
    if request.method == 'POST':
        form = LinkForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('create-link')
        else:
            print(form.errors)
    else:
        form = LinkForm(user=request.user)
        
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'links/create_link.html', context)


@login_required(login_url='/login/')
def edit_category(request, pk):
    category = get_object_or_404(Category, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/links/categories/')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'links/create_category.html', {
        'form': form,
        'title': 'Edit category',
    })

@login_required(login_url='/login/')
def edit_link(request, pk):
    title = 'Edit Link'
    link = get_object_or_404(Link, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('links')
    else:
        form = LinkForm(instance=link, user=request.user)

    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'links/create_link.html', context)

@login_required(login_url='/login/')
def delete_category(request, pk):
    category = get_object_or_404(Category, created_by=request.user, pk=pk)
    category.delete()
    return redirect('categories')

def delete_link(request, pk):
    link = get_object_or_404(Link, pk=pk, created_by=request.user)
    link.delete()
    return redirect('links')
