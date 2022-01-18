from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Project
from post.models import Post

# Create your views here.
class DashboardView(ListView):
    model = Project
    paginate_by = 20
    template_name = 'project/dashboard.html'

# class ProjectDetailView(DetailView):
#     model = Project
#     context_object_name = 'Projects'
#     template_name = 'project/details.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['posts'] = Post.objects.filter(project=self.kwargs.get('pk'))
#         return context

class ProjectDetailView(RedirectView):
    pattern_name = 'post:post-list'

class ProjectCreateView(CreateView):
    model = Project
    fields = ['name']
    template_name = 'project/form.html'

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name']
    template_name = 'project/form.html'

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project:dashboard')
    template_name = 'project/delete_confirm.html'