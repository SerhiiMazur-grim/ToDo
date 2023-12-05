from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from .permissions import IsOwner
from .forms import TaskForm
from .models import Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_create')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, _('Ticket created successfully!'))
        return super().form_valid(form)


class TaskListView(generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        done = self.request.GET.get('done', None)
        if done is None:
            queryset = Task.objects.filter(
                owner=self.request.user
                ).order_by('done', 'created')
        else:
            
            done.capitalize()
            if done in ('True', 'False'):
                queryset = Task.objects.filter(
                    owner=self.request.user,
                    done=done
                    ).order_by('created')
            else:
                raise Http404(_("Invalid 'done' parameter provided."))
            
        return queryset


class TaskDetailView(IsOwner, generic.DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskUpdateView(IsOwner, generic.UpdateView):    
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    context_object_name = 'task'

    def get_success_url(self):
        messages.success(self.request, 'Task updated successfully')
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, 'Task update failed')
        return super().form_invalid(form)


class TaskIsDoneView(IsOwner, View):
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.task_done()
        messages.success(self.request, 'Task is done!')
        
        return redirect('/tasks/?done=False')
    
    def get_object(self):
        object = get_object_or_404(Task, pk=self.kwargs['pk'])
        
        return object


class TaskToInProgressView(IsOwner, View):
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.task_to_in_progress()
        messages.success(self.request, 'Task replace to in progress!')
        
        return redirect('/tasks/?done=False')
    
    def get_object(self):
        object = get_object_or_404(Task, pk=self.kwargs['pk'])
        
        return object


class TaskDeleteView(IsOwner, View):
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        messages.success(self.request, 'Task is deleted!')
        
        return redirect('/tasks/?done=False')
    
    def get_object(self):
        object = get_object_or_404(Task, pk=self.kwargs['pk'])
        
        return object
