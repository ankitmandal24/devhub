from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db.models import Q
from . models import Project, Tag
from .forms import ProjectForm,ReviewForm
from .utils import SearchProject, paginateProjects
import cloudinary.uploader
import cloudinary
# Create your views here.

def projects(request):
    projects, search_query = SearchProject(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects.html', context)

def project(request, pk):
    projectobj = Project.objects.get(id=pk)
    # tags = projectobj.tags.all()
    # print('projectobj:', projectobj)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectobj
        review.owner = request.user.profile
        review.save()


        projectobj.getvotecount

        messages.success(request,'Your review has successfully submitted')
        return redirect('project', pk=projectobj.id)
    return render(request, "single-project.html",{'project':projectobj,'form': form})

@login_required(login_url="login")
def createproject(request):
    profile = request.user.profile

    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',' , " ").split()
        form = ProjectForm(request.POST, request.FILES,)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name = tag)
                project.tags.add(tag)
            return redirect('account')

    context ={'form': form,}
    return render(request, "project_form.html", context)
@login_required(login_url="login")
def updateproject(request, pk ):
    profile = request.user.profile

    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',' , " ").split()
        form = ProjectForm(request.POST, request.FILES,instance=project)
        if form.is_valid():
            form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name = tag)
                project.tags.add(tag)
            return redirect('account')

    context ={'form': form,'project': project}
    return render(request, "project_form.html", context)

@login_required(login_url="login")
def deleteproject(request, pk):
    profile = request.user.profile

    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        # cloudinary.uploader.destroy(Project.image.public_id,invalidate=True)
        return redirect('projects')
    context = {'object': project}
    return render(request, "delete_object.html", context)

# @login_required(login_url="login")
# def deleteproject(request,pk):
#     profile = request.user.profile
#
#     project = profile.project_set.get(id=pk)
#     if request.method == 'POST':
#         # Store the image public_id in a variable
#         # image_public_id = project.featured_image
#
#         # Delete the project instance
#         project.delete()
#
#         # Delete the image from Cloudinary
#         try:
#             cloudinary.uploader.destroy(project.featured_image.public_id, invalidate=True)
#         except cloudinary.exceptions.Error as e:
#             # Handle Cloudinary deletion error, if any
#             # You can log the error or show a user-friendly message
#             pass
#
#         return redirect('projects')
#
#     context = {'object': project}
#     return render(request, "delete_object.html", context)
