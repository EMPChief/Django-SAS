from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from links.models import Link, Category

@login_required(login_url='/login/')
def dashboard(request):
    links = Link.objects.filter(created_by=request.user)[:5]
    categories = Category.objects.filter(created_by=request.user)[:5]

    context = {'links': links, 'categories': categories}
    return render(request, 'dashboard/dashboard.html', context)
