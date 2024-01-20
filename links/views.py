from django.shortcuts import render, redirect
from .forms import CategoryForm, LinkForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('create-category')
    else:
        form = CategoryForm(user=request.user)
    return render(request, 'links/create_category.html', {'form': form})




@login_required(login_url='/login/')
def create_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('create-link')
    else:
        form = LinkForm(user=request.user)
    return render(request, 'links/create_link.html', {'form': form})
