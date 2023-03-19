from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods 
from django.views.decorators.cache import cache_page
from django.views import View
from django.views.generic import TemplateView,ListView

def index(request):
    return HttpResponse("Hello there, e-commerce store front coming soon...")

def detail(request):
    return HttpResponse("This is a detail page")

def logout(request):
    try:
        del request.session['customer']
    except KeyError:
        print("Error while logging out")
    return HttpResponse("You're logged out")


@require_http_methods(["GET"])
@csrf_exempt
def electronics(request):
    items = ("Windows PC","Apple Mac","Apple Iphone", "Lenovo Laptop", "Samsung Electronics", "Google")
    if request.method == 'GET':
        paginator = Paginator(items,2)
        pages= request.GET.get('page',1)
        name = "Fabio"
        try:
            items = paginator.page(pages)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        if not request.session.has_key('customer'):
            request.session['customer'] = name
            print("Session value set")
        response = render(request, 'store/list.html',{'items': items})
        if request.COOKIES.get('visits'):
            value = int(request.COOKIES.get('visits'))
            print("Getting Cookie")
            response.set_cookie('visits', value + 1)
        else:
            value = 1
            print("Setting Cookie.")
            response.set_cookie('visits', value)
        return response    
    elif request.method == "POST":
        return HttpResponseNotFound("Page Not Found")
    
class ElectronicsView(View):
    def get(self, request):
        items = ("Windows PC","Apple Mac","Apple Iphone", "Lenovo Laptop", "Samsung Electronics", "Google")
        paginator = Paginator(items,2)
        pages = request.GET.get('page',1)
        self.process()
        try:
            items= paginator.page(pages)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        return render(request, 'store/list.html', {'items':items})
    
    def process(self):
        print("We are processing Electronics")

class ComputersView(ElectronicsView):
    def process(self):
        print("We are processing Computers")

class MobileView():
    def process(self):
        print("We are Processing Mobile phones")

class EquipmentView(MobileView,ComputersView):
    pass

class ElectronicsView2(TemplateView):
    template_name = 'store/list.html'
    def get_context_data(self, **kwargs):
        items = ("Windows PC","Apple Mac","Apple Iphone", "Lenovo Laptop", "Samsung Electronics", "Google")
        context = {'items': items}
        return context
    
class ElectronicsView3(ListView):
    template_name = 'store/list.html'
    queryset = ("Windows PC","Apple Mac","Apple Iphone", "Lenovo Laptop", "Samsung Electronics", "Google")
    context_object_name = 'items'
    paginate_by = 2