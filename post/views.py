from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from collections import Counter, OrderedDict
from math import ceil

from .models import Post, Product, InternalLink, OutboundLink, ImageAltText, H1, H2, H3, H4
from project.models import Project

from .scrapper import SiteScrapper
from .utils import get_plot

# Create your views here.
class PostListView(ListView):
    # paginate_by = 20
    template_name = 'post/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(project__pk=self.kwargs['project_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['project_id']
        context['project_id'] = project_id
        context['project_name'] = Project.objects.get(pk=project_id).name

        if self.object_list.count()>0:
            content_lens = [len(post.contents.split()) for post in self.object_list if post.contents is not None]
            if len(content_lens)>0:
                content_len = ceil((sum(content_lens)/len(content_lens))/100*110)
                context['content_len'] = content_len
        headings = dict()
        headings['h1'] = []
        headings['h2'] = []
        headings['h3'] = []
        headings['h4'] = []
        for post in self.object_list:
            headings['h1'].append(H1.objects.filter(post=post.id))
            headings['h2'].append(H2.objects.filter(post=post.id))
            headings['h3'].append(H3.objects.filter(post=post.id))
            headings['h4'].append(H4.objects.filter(post=post.id))
        context['sub_headings'] = headings

        products = Product.objects.filter(post__project=project_id).order_by('-name')
        products_name = Counter([product.name for product in products])
        # products_name = OrderedDict(Counter([product.name for product in products]))
        if len(products_name)>0:
            names = list(products_name.keys())
            product_count = list(products_name.values())
            chart = get_plot(product_count,names,context['project_name'])
            context['chart'] = chart
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(post=self.object.pk)
        context['internal_links'] = InternalLink.objects.filter(post=self.object.pk)
        context['outbound_links'] = OutboundLink.objects.filter(post=self.object.pk)
        context['image_alt_texts'] = ImageAltText.objects.filter(post=self.object.pk)
        context['h1'] = H1.objects.filter(post=self.object.pk)
        context['h2'] = H2.objects.filter(post=self.object.pk)
        context['h3'] = H3.objects.filter(post=self.object.pk)
        context['h4'] = H4.objects.filter(post=self.object.pk)
        return context

class PostAddView(CreateView):
    model = Post
    fields = ['url']
    template_name = 'post/form.html'

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs.get('project_id'))
        form.instance.project = project
        post = Post.objects.filter(url=form.instance.url)
        if len(post)!=0:
            print("Already have this.")
            return redirect(post[0])
        else:
            return super().form_valid(form)
        

class PostUpdateView(UpdateView):
    model = Post
    fields = ['project','url']
    template_name = 'post/form.html'

class PostDeleteView(DeleteView):
    model = Post
    # success_url = reverse_lazy('post:post-list', kwargs={})
    template_name = 'post/delete_confirm.html'

    def get_success_url(self):
        return reverse_lazy('post:post-list', kwargs={'project_id': self.kwargs['project_id']})
    
def scrapeSite(sender, instance, created, **kwargs):
    if created:
        print("Creating instance")
        Sc = SiteScrapper(instance.url)
        instance.title = Sc.title
        print("Getting contents")
        instance.contents = Sc.review_content
        print("Getting meta data")
        instance.meta = Sc.getMetaDescription()
        instance.save()
        # Internal links
        print("Getting links")
        for link in Sc.internal_links:
            obj = InternalLink(address=link, post=instance)
            obj.save()
        # Outbound links
        for link in Sc.outbound_links:
            obj = OutboundLink(address=link, post=instance)
            obj.save()
        # Image Alt-text
        print("Getting Image-Alt-Text")
        for alt_text in Sc.getImageAltText():
            try:
                obj = ImageAltText( text=alt_text['alt'], 
                                    src=alt_text['src'],
                                    post=instance) 
                obj.save()
            except: pass
        # Sub Headings
        print("Getting Sub-headings")
        subheadings = Sc.getSubHeadings()
        # h1
        for h in subheadings['h1']:
            obj = H1(heading=h, post=instance)
            obj.save()
        # h2
        for h in subheadings['h2']:
            obj = H2(heading=h, post=instance)
            obj.save()
        # h3
        for h in subheadings['h3']:
            obj = H3(heading=h, post=instance)
            obj.save()
        # h4
        for h in subheadings['h4']:
            obj = H4(heading=h, post=instance)
            obj.save()
        print("End scrapping")


post_save.connect(scrapeSite, sender=Post)

class GetProductsView(TemplateView):
    template_name = 'post/get_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        Sc = SiteScrapper(post.url)
        context['tags'] = Sc.getProducts()
        tagnames = [tag['name'] for tag in context['tags']]
        context['max'] = max(tagnames, key=tagnames.count)
        return context
    
    def post(self, request, *args, **kwargs):
        products = request.POST.getlist('products')
        for product in products:
            obj = Product(name=product,post=Post.objects.get(pk=self.kwargs.get('pk')))
            obj.save()
        return redirect('post:post-detail',project_id=self.kwargs.get('project_id'),pk=self.kwargs.get('pk'))
