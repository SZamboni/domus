from django.shortcuts import render,get_object_or_404,redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView , DeleteView
from .models import Category, Device, DeviceType, StateAttribute, StateAttributeRecord, FunctionParameter, Function
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404  
from django.views.decorators.csrf import csrf_exempt
import json
from .myfunctions import parseRegistrationJson, parseStateData, sendFunctionRequest


def about(request):
    return render(request,'devices/about.html', {'title':'About'})

def landingPage(request):
    return render(request,'devices/landing_page.html')

def home(request):
    return render(request,'devices/home.html', {'title':'Domus Home Page'})

class UserCategoriesView(LoginRequiredMixin,ListView):
    model = Category
    template_name = 'devices/home.html'
    context_object_name = 'categories'
    paginate_by = 2

    def get_queryset(self):
       user = self.request.user
       return Category.objects.filter(owner=user).order_by('name')

class CategoryCreateView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    model = Category
    fields = ['name','description']
    success_url= '/userDevices/'
    success_message = 'Category successfully created'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Category
    fields = ['name','description']
    success_url= '/userDevices/'
    success_message = 'Category successfully updated'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        cat = self.get_object()
        if self.request.user == cat.owner:
            return True
        return False

class CategoryDeleteView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Category
    success_url = '/userDevices/'
    success_message = 'Category successfully deleted'

    def test_func(self):
        cat = self.get_object()
        if self.request.user == cat.owner and cat.devices.count() == 0:
            return True
        return False

class DevicesCategoryView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Device
    template_name = 'devices/category.html'
    context_object_name = 'devices'
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, id=self.kwargs.get('pk'))
        context['cat'] = cat
        return context

    def get_queryset(self):
       cat = get_object_or_404(Category, id=self.kwargs.get('pk'))
       return Device.objects.filter(category = cat).order_by('name')

    def test_func(self):
        cat = get_object_or_404(Category, id=self.kwargs.get('pk'))
        if(cat.owner == self.request.user):
            return True
        return False

class DeviceUpdateView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Device
    fields = ['name','description']
    success_url= '/userDevices/'
    success_message = 'Device successfully updated'

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('pk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if self.request.user == cat.owner:
            return True
        return False

class DeviceDeleteView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Device
    success_url = '/userDevices/'
    success_message = 'Device successfully deleted'

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('pk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if self.request.user == cat.owner:
            return True
        return False

class ChangeCategoryView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Category
    template_name = 'devices/change_category.html'
    context_object_name = 'categories'
    paginate_by = 2
    success_message = 'Device category successfully updated'

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('pk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if(cat.owner == self.request.user):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dev = get_object_or_404(Device, id=self.kwargs.get('pk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'))
        oldcat = get_object_or_404(Category, id=self.kwargs.get('oldcatpk'))
        context['dev'] = dev
        context['cat'] = cat
        context['oldcat'] = oldcat
        return context

    def post(self, request, *args, **kwargs):
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'))
        dev = get_object_or_404(Device, id=self.kwargs.get('pk'))
        oldcat = get_object_or_404(Category, id=self.kwargs.get('oldcatpk'))
        oldcat.devices.remove(dev)
        oldcat.save()
        cat.devices.add(dev)
        cat.save()

        return redirect('category',pk=cat.id)


class DeviceView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = StateAttribute
    template_name = 'devices/device.html'
    context_object_name = 'stateatt'
    

    def get_queryset(self):
       dev = get_object_or_404(Device, id=self.kwargs.get('pk'))
       return StateAttribute.objects.filter(devType = dev.Devtype).order_by('name')
    
    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('pk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        
        if(cat.owner == self.request.user):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'))
        context['cat'] = cat
        dev = get_object_or_404(Device, id=self.kwargs.get('pk'))
        context['dev'] = dev
        functions = Function.objects.filter(devType = dev.Devtype).order_by('name')
        context['functions'] = functions

        stateatt = StateAttribute.objects.filter(devType = dev.Devtype).order_by('name')

        values = []
        for st in stateatt:
            values.append( StateAttributeRecord.objects.filter(device=dev,attribute=st).order_by('-date_received').first())

        print(values)
        context['values'] = values

        return context
    
class FunctionsView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = FunctionParameter
    template_name = 'devices/function.html'
    context_object_name = 'parameters'

    def get_queryset(self):
       fun = get_object_or_404(Function, id=self.kwargs.get('funpk'))
       return FunctionParameter.objects.filter(funct = fun).order_by('name')
    
    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if(cat.owner == self.request.user):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'))
        context['cat'] = cat
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        context['dev'] = dev
        fun = get_object_or_404(Function, id=self.kwargs.get('funpk'))
        context['fun'] = fun
        return context
    
    def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'))
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        fun = get_object_or_404(Function, id=self.kwargs.get('funpk'))

        parameters = FunctionParameter.objects.filter(funct = fun)
        values = {}

        for par in parameters:
            val = request.POST.get(str(par.id),"")
            if par.data_type == 'B':
                if val == '':
                    val = False
                else:
                    val = True
            values[str(par.name)] = val
        
        print(values)
        # send values to a function that performs a http request to the device in order to send the data

        sending_ok = sendFunctionRequest(request,cat,dev,fun,values)

        if sending_ok:
            messages.add_message(request,messages.SUCCESS,'Command sended successfully to the device')
        else :
            messages.add_message(request,messages.ERROR,'Command not sended to the device!')

        return redirect('device',catpk=cat.id,pk=dev.id)

@csrf_exempt
def registerDevice(request):
    if request.method != 'POST':
        return Http404
    
    return parseRegistrationJson(request)

@csrf_exempt
def postStateData(request):
    if request.method != 'POST':
        return Http404
    return parseStateData(request)
    