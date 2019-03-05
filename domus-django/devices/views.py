from django.shortcuts import render,get_object_or_404,redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView , DeleteView, View,TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404  
from django.views.decorators.csrf import csrf_exempt
import json
from .myfunctions import parseRegistrationJson, parseStateData, sendFunctionRequest
from .insert_data import *


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
    
class FunctionsView(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    template_name = 'devices/function.html'
    
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

        context['parameters'] = FunctionParameter.objects.filter(funct = fun).order_by('name')
        
        options = {}

        for par in context['parameters']:
            opts = FunctionParameterOption.objects.filter(parameter = par)
            par.options = opts
            const = FunctionParameterConstraint.objects.filter(parameter = par)
            par.constraints = const

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
            if par.data_type == BOOL:
                if val == '':
                    val = False
                else:
                    val = True
            elif par.data_type == FLOAT:
                if val == '':
                    val = 0
                else:
                    val = float(val)
            values[str(par.name)] = val
            constraints = FunctionParameterConstraint.objects.filter(parameter = par)
            for con in constraints:
                if con.constraintType == CONSTRAINT_MAX and par.data_type == FLOAT:
                    if val > float(con.value):
                        messages.add_message(request,messages.ERROR,'ERROR: PARAMETER ' + str(par.name) + ' MAX VALUE: ' + str(con.value))
                        return redirect('function',catpk=cat.id,devpk=dev.id,funpk=fun.id)
                elif con.constraintType == CONSTRAINT_MIN and par.data_type == FLOAT:
                    if val < float(con.value):
                        messages.add_message(request,messages.ERROR,'ERROR: PARAMETER ' + str(par.name) + ' MIN VALUE: ' + str(con.value))
                        return redirect('function',catpk=cat.id,devpk=dev.id,funpk=fun.id)
                elif con.constraintType == CONSTRAINT_DIFFERENT:
                    if par.data_type == FLOAT:
                        if val == float(con.value):
                            messages.add_message(request,messages.ERROR,'ERROR: PARAMETER ' + str(par.name) + ' VALUE MUST BE DIFFERENT FROM: ' + str(con.value))
                            return redirect('function',catpk=cat.id,devpk=dev.id,funpk=fun.id)
                    elif val == con.value:
                        messages.add_message(request,messages.ERROR,'ERROR: PARAMETER ' + str(par.name) + ' VALUE MUST BE DIFFERENT FROM: ' + str(con.value))
                        return redirect('function',catpk=cat.id,devpk=dev.id,funpk=fun.id)
        
        print(values)
        # send values to a function that performs a http request to the device in order to send the data

        sending_ok = sendFunctionRequest(dev,fun,values)

        if sending_ok:
            messages.add_message(request,messages.SUCCESS,'Command sended successfully to the device')
        else :
            messages.add_message(request,messages.ERROR,'Command not sended to the device!')

        return redirect('device',catpk=cat.id,pk=dev.id)

class AlertCreateView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Alert
    fields = ['description','alert_condition','alert_level','value']
    success_url= '/userDevices/'
    success_message = 'Alert successfully created'      

    def form_valid(self,form):
        att = get_object_or_404(StateAttribute, id=self.kwargs.get('pk'))
        form.instance.attribute = att
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        form.instance.device = dev
        form.instance.user = self.request.user

        if att.data_type == FLOAT:
            try:
                float(form.data['value'])
            except:
                return super().form_invalid(form)
        elif att.data_type == BOOL:
            try:
                bool(form.data['value'])
            except:
                return super().form_invalid(form)

        return super().form_valid(form)

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if(cat.owner == self.request.user):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catid']=self.kwargs.get('catpk')
        context['devid']=self.kwargs.get('devpk')
        att = get_object_or_404(StateAttribute, id=self.kwargs.get('pk'))
        context['atttype'] = att.data_type
        return context

class AlertListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Alert
    template_name = 'devices/alerts.html'
    context_object_name = 'alert_list'
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['catid'] = self.kwargs.get('catpk')
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        context['dev'] = dev
        return context

    def get_queryset(self):
       dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
       return Alert.objects.filter(device = dev, user = self.request.user)

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if(cat.owner == self.request.user):
            return True
        return False

class AlertDeleteView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Alert
    success_url = '/userDevices/'
    success_message = 'Alert successfully deleted'

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if self.request.user == cat.owner:
            return True
        return False

class AlertUpdateView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Alert
    fields = ['description','alert_condition','alert_level','value']
    success_url= '/userDevices/'
    success_message = 'Alert successfully updated'

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if self.request.user == cat.owner:
            return True
        return False
    
    def form_valid(self,form):
        alert = get_object_or_404(Alert,id=self.kwargs.get('pk'))
        att = alert.attribute
        form.instance.attribute = att
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        form.instance.device = dev
        form.instance.user = self.request.user

        if att.data_type == FLOAT:
            try:
                float(form.data['value'])
            except:
                return super().form_invalid(form)
        elif att.data_type == BOOL:
            try:
                bool(form.data['value'])
            except:
                return super().form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catid']=self.kwargs.get('catpk')
        context['devid']=self.kwargs.get('devpk')
        alert = get_object_or_404(Alert,id=self.kwargs.get('pk'))
        att = alert.attribute
        context['atttype'] = att.data_type
        return context

class NotificationsListView(LoginRequiredMixin,ListView):
    model = Notification
    template_name = 'devices/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 2

    def get_queryset(self):
        user = self.request.user
        user.userprofile.unreaded_notifications = 0
        user.userprofile.save()
        categories = Category.objects.filter(owner = user)

        notifications = []

        for cat in categories:
            devs = cat.devices.all()
            for dev in devs:
                alerts = Alert.objects.filter(device = dev)
                for al in alerts:
                    notifications.extend(Notification.objects.filter(alert=al,readed = False))
        
        for n in notifications:
            n.readed = True
            n.save()

        notifications.sort(key=lambda x: x.date,reverse=True)
        return notifications
    
class OldNotificationsListView(LoginRequiredMixin,ListView):
    template_name = 'devices/old_notifications.html' 
    model = Notification
    paginate_by = 2      
    context_object_name = 'notifications'
    
    def get_queryset(self):
        user = self.request.user
        categories = Category.objects.filter(owner = user)

        notifications = []

        for cat in categories:
            devs = cat.devices.all()
            for dev in devs:
                alerts = Alert.objects.filter(device = dev)
                for al in alerts:
                    notifications.extend(Notification.objects.filter(alert=al,readed = True))

        notifications.sort(key=lambda x: x.date,reverse=True)
        return notifications

class FeedbackFunctionChoiceView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Function
    paginate_by = 2
    context_object_name = 'functions'
    template_name = 'devices/select_feedback_funct.html' 

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if self.request.user == cat.owner:
            al = get_object_or_404(Alert,id=self.kwargs.get('alpk'))
            if al.user == self.request.user:
                return True
            else:
                return False
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catid']=self.kwargs.get('catpk')
        context['devid']=self.kwargs.get('devpk')
        context['alid']=self.kwargs.get('alpk')
        return context
    
    def get_queryset(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        devtype = dev.Devtype
        return Function.objects.filter(devType = devtype)

class CreateFeedbackFunctionView(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    template_name = 'devices/create_feedback_funct.html' 

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if self.request.user == cat.owner:
            al = get_object_or_404(Alert,id=self.kwargs.get('alpk'))
            if al.user == self.request.user:
                return True
            else:
                return False
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catid']=self.kwargs.get('catpk')
        context['devid']=self.kwargs.get('devpk')
        al = get_object_or_404(Alert,id=self.kwargs.get('alpk'))
        context['alert'] = al
        fun = get_object_or_404(Function, id=self.kwargs.get('pk'))
        context['fun']= fun
        params = FunctionParameter.objects.filter(funct = fun)
        context['parameters'] = params

        return context

    def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'))
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        fun = get_object_or_404(Function, id=self.kwargs.get('pk'))
        al = get_object_or_404(Alert,id=self.kwargs.get('alpk'))

        parameters = FunctionParameter.objects.filter(funct = fun)
        values = {}

        fdbf = FeedbackFunction(alert = al, description = ' ', function = fun)
        fdbf.save()

        for par in parameters:
            val = request.POST.get(str(par.id),"")
            if par.data_type == BOOL:
                if val == '':
                    val = False
                else:
                    val = True
            elif par.data_type == FLOAT:
                if val == '':
                    val = 0
                else:
                    val = float(val)
            values[str(par.name)] = val
            constraints = FunctionParameterConstraint.objects.filter(parameter = par)
            for con in constraints:
                if con.constraintType == CONSTRAINT_MAX and par.data_type == FLOAT:
                    if val > float(con.value):
                        messages.add_message(request,messages.ERROR,'ERROR: PARAMETER ' + str(par.name) + ' MAX VALUE: ' + str(con.value))
                        return redirect('alerts',catpk=cat.id,devpk=dev.id)
                elif con.constraintType == CONSTRAINT_MIN and par.data_type == FLOAT:
                    if val < float(con.value):
                        messages.add_message(request,messages.ERROR,'ERROR: PARAMETER ' + str(par.name) + ' MIN VALUE: ' + str(con.value))
                        return redirect('alerts',catpk=cat.id,devpk=dev.id)
                elif con.constraintType == CONSTRAINT_DIFFERENT:
                    if par.data_type == FLOAT:
                        if val == float(con.value):
                            messages.add_message(request,messages.ERROR,'ERROR: PARAMETER ' + str(par.name) + ' VALUE MUST BE DIFFERENT FROM: ' + str(con.value))
                            return redirect('alerts',catpk=cat.id,devpk=dev.id)
                    elif val == con.value:
                        messages.add_message(request,messages.ERROR,'ERROR: PARAMETER ' + str(par.name) + ' VALUE MUST BE DIFFERENT FROM: ' + str(con.value))
                        return redirect('alerts',catpk=cat.id,devpk=dev.id)
            feedback_par = FeedbackParameter(feedbackfunction = fdbf,parameter = par, value = val)
            feedback_par.save()
        
        print(values)

        messages.add_message(request,messages.SUCCESS,'Feedback function created successfully!')
        return redirect('alerts',catpk=cat.id,devpk=dev.id)

class FeedbackFunctionsListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    template_name = 'devices/feedbackfunctions.html'
    paginate_by = 2
    context_object_name = 'functions'
    model = FeedbackFunction

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if self.request.user == cat.owner:
            return True
        return False

    def get_queryset(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        user = self.request.user
        alerts = Alert.objects.filter(device = dev, user = user)
        
        functs = []

        for al in alerts:
            al_func = FeedbackFunction.objects.filter(alert = al)
            functs.extend(al_func)

        for fun in functs:
            pars = FeedbackParameter.objects.select_related().filter(feedbackfunction = fun)
            fun.feedbackparameters = pars
        
        return functs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catid']=self.kwargs.get('catpk')
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        context['dev']=dev
        return context

class FeedbackFunctionDeleteView(SuccessMessageMixin,LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = FeedbackFunction
    success_url = '/userDevices/'
    success_message = 'Feedback function successfully deleted'

    def test_func(self):
        dev = get_object_or_404(Device, id=self.kwargs.get('devpk'))
        cat = get_object_or_404(Category, id=self.kwargs.get('catpk'), devices=dev)
        if self.request.user == cat.owner:
            fun = get_object_or_404(FeedbackFunction, id= self.kwargs.get('pk'))

            if(fun.alert.device == dev and fun.alert.user == self.request.user):
                return True
            else :
                return True
        return False

class TestView(TemplateView):
    template_name = 'devices/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        create_data()

        return context


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
    