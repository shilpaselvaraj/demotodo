from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . models import Task
from .form import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView


class Tasklistview(ListView):
    model=Task
    template_name = 'index.html'
    context_object_name = 'tasks'
class Taskdetailview(DetailView):
    model=Task
    template_name = 'details.html'
    context_object_name = 'i'
class Taskupdateview(UpdateView):
    model=Task
    template_name='update.html'
    context_object_name='tasks'
    fields=('task','priority','date')
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})
class Taskdeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')




# Create your views here.


def index(request):
    tasks = Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority = request.POST.get('priority', '')
        date=request.POST.get('date','')
        tasks=Task(task=name,priority=priority,date=date)
        tasks.save()
        return redirect('/')

    return render(request,'index.html',{'tasks':tasks})

def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method=='POST':
        task.delete()
        return redirect('/')

    return render(request,'delete.html')
def update(request,id):
    tasks=Task.objects.get(id=id)
    f=TodoForm(request.POST or None,instance=tasks)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':tasks})
