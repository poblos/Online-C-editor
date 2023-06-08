from django.contrib import messages
import subprocess
import os
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


def getDataOrNothing(file):
    try:
        text_file = open(file + ".asm", "r")
        data = text_file.read()
        text_file.close()
    except:
        return ("")

    return (data)


def append_descendants(user, name, list):
    children = Directory.objects.filter(
        parent=name).filter(alive=True, owner=user).order_by("name")
    children2 = File.objects.filter(
        parent=name).filter(alive=True, owner=user).order_by("name")
    if children.count() or children2.count() >= 1 and name != None:
        list.append("in")
    for child in children:
        list.append(child)
        list = append_descendants(user, child, list)
    for child in children2:
        list.append(child)
    if children.count() or children2.count() >= 1 and name != None:
        list.append("out")
    return list


@login_required
def index(request):
    add_dir_form = DirectoryForm()
    add_file_form = FileForm()
    list = append_descendants(request.user, None, [])
    standard_list = Standard.objects.all()
    processor_list = Processor.objects.all()
    optimizations_form = OptimizationsForm()
    dependant_form = DependantForm()
    settings = CompilationSettings.objects.order_by("id")[0]
    return render(request, "dir_browse/index.html", {"add_dir_form":add_dir_form, "add_file_form": add_file_form, "settings": settings, "dependant_form": dependant_form, "optimizations_form": optimizations_form, "directory_list": list, "standard_list": standard_list, "processor_list": processor_list})


def delete_dir(request, pk):
    data = get_object_or_404(Directory, id=pk)
    data.alive = False
    data.delete_date = timezone.now()
    data.save()
    return redirect('dir_browse:index')


@login_required
def dir_detail(request, pk):
    directory = get_object_or_404(Directory, id=pk)
    if directory.owner != request.user:
        return HttpResponseNotFound()      
    add_dir_form = DirectoryForm()
    add_file_form = FileForm()
    list = append_descendants(request.user, None, [])
    standard_list = Standard.objects.all()
    processor_list = Processor.objects.all()
    optimizations_form = OptimizationsForm()
    dependant_form = DependantForm()
    settings = CompilationSettings.objects.order_by("id")[0]
    return render(request, "dir_browse/dir_detail.html", {"pk": pk, "add_dir_form": add_dir_form, "add_file_form": add_file_form, "settings": settings, "dependant_form": dependant_form, "optimizations_form": optimizations_form, "directory": directory, "directory_list": list, "standard_list": standard_list, "processor_list": processor_list})


def add_dir(request, pk):
    if request.method == "POST":
        add_dir_form = DirectoryForm(request.POST)
        if add_dir_form.is_valid():
            name = add_dir_form.cleaned_data["name"]
            desc = add_dir_form.cleaned_data["desc"]
            owner = request.user
            dir = Directory.objects.create(name=name, desc=desc, owner=owner)
            if pk != 0:
                dir.parent_id = pk
            else:
                dir.parent_id = None
            dir.save()
        return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))


def add_file(request, pk):
    if request.method == "POST":
        form = FileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            desc = form.cleaned_data["desc"]
            text = form.cleaned_data["text"]
            owner = request.user
            file = File.objects.create(
                name=name, desc=desc, owner=owner, text=text)
            if pk != 0:
                file.parent_id = pk
            else:
                file.parent_id = None
            file.save()
    return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))


def delete_file(request, pk):
    data = get_object_or_404(File, id=pk)
    data.delete_date = timezone.now()
    data.alive = False
    data.save()
    return redirect('dir_browse:index')


@login_required
def file_detail(request, pk):
    file = get_object_or_404(File, id=pk)
    if file.owner != request.user:
        return HttpResponseNotFound()     
    if request.method == "POST":
        form = EditorForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            file.text = text
            file.change_date = timezone.now()
            file.save()
            return HttpResponse()
    else:
        form = EditorForm(initial={'text': file.text})

    list = append_descendants(request.user, None, [])
    standard_list = Standard.objects.all()
    processor_list = Processor.objects.all()
    asm = getDataOrNothing(file.name)
    optimizations_form = OptimizationsForm()
    dependant_form = DependantForm()
    settings = CompilationSettings.objects.order_by("id")[0]
    return render(request, "dir_browse/file_detail.html", {"settings": settings, "dependant_form": dependant_form, "optimizations_form": optimizations_form, "form": form, "file": file, "directory_list": list, "pk": pk, "standard_list": standard_list, "asm": asm, "processor_list": processor_list})


def choose_standard(request):
    settings = CompilationSettings.objects.order_by("id")[0]
    try:
        selected_standard = Standard.objects.get(pk=request.POST["standard"])
    except (KeyError, Standard.DoesNotExist):
        return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))
    else:
        settings.standard = selected_standard
        settings.save()
        return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))


def choose_processor(request):
    settings = CompilationSettings.objects.order_by("id")[0]
    try:
        selected_processor = Processor.objects.get(
            pk=request.POST["processor"])
    except (KeyError, Processor.DoesNotExist):
        return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))
    else:
        settings.processor = selected_processor
        settings.save()
        return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))


def choose_optimizations(request):
    optimizations = Optimization.objects.all()
    form = OptimizationsForm(request.POST or None)
    if request.POST and form.is_valid():
        selected = form.cleaned_data["options"]
        for c in optimizations:
            if c.name in selected:
                c.active = True
                c.save()
            else:
                c.active = False
                c.save()
    return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))


def choose_dependant(request):
    dependant = DependantOption.objects.all()
    form = DependantForm(request.POST or None)
    if request.POST and form.is_valid():
        selected = form.cleaned_data["options"]
        for c in dependant:
            if c.name in selected and c.processor == CompilationSettings.objects.order_by("id")[0].processor:
                c.active = True
                c.save()
            else:
                c.active = False
                c.save()
    return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))


def compile(request, pk):
    settings = CompilationSettings.objects.order_by("id")[0]
    standard = "--std-" + settings.standard.name
    processor = "-m" + settings.processor.name.lower()
    fileModel = File.objects.get(id=pk)
    name = fileModel.name + ".c"
    f = open(name, "w")
    f.write(fileModel.text)
    f.close()
    t = ["sdcc", "-S", processor, standard]
    opti = Optimization.objects.filter(active=True)
    for opt in opti:
        t.append(opt.name)
    opti = DependantOption.objects.filter(active=True)
    for opt in opti:
        t.append(opt.name)
    t.append(name)
    subprocess.run(t)
    os.remove(name)

    return redirect(request.META.get('HTTP_REFERER', '/dir_browse/'))


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dir_browse:index') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))