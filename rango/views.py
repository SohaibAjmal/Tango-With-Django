from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
import contextlib
from rango.models import Category
from rango.models import Page
from django.forms.models import modelformset_factory

from rango.forms import CategoryForm, EditCategoryForm
from rango.forms import PageForm, PageEditForm
from rango.forms import UserForm, UserProfileForm

from django.db.transaction import commit
from django.http.response import HttpResponseRedirect

from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


## User Defined methods
def decode_url(category_name_url):
    
    category_name = category_name_url.replace('_',' ')
    return category_name

def index(request):
    
    context = RequestContext(request)
    
    category_list = Category.objects.order_by('-likes')[:5]
    
    # page_list = Page.objects.order_by('views')[:5]
    
    context_dict = {}
    context_dict['categories'] = category_list
    
   # context_dict['pages'] = page_list
    
    for category in category_list:
        category.url = category.name.replace(' ','_')
    
    return render_to_response('rango/index.html',context_dict, context)



def about(request):
    
    context = RequestContext(request) 
    
    context_dict = {"aboutmessage":"You are in About Page"}
    
    return render_to_response('about/about.html',context_dict,context)

def category(request, category_name_url):
    
    context  = RequestContext(request)
    
    category_name = category_name_url.replace('_',' ')
    
    
    context_dict = {'category_name': category_name}
    context_dict = {'category_name_url': category_name_url}
    
    
    try:
        
        category = Category.objects.get(name = category_name) 
        
        
        pages = Page.objects.filter(category = category)
        
        context_dict['pages'] = pages
        
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        pass
    
    return render_to_response('rango/category.html',context_dict, context)
    
@login_required
def add_category(request):
    
    context = RequestContext(request) 
    
    if request.method == 'POST':
        
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            
            form.save(commit = True)
            
            
            return index(request)
        else:
            
            return HttpResponse("Invalid Form or Data1")
    else:
        
        form = CategoryForm()
        
    return render_to_response('rango/add_category.html', {'form':form} , context)

@login_required
def edit_category(request,category_name_url):
    
    context = RequestContext(request) 
    
    category_name = category_name_url.replace('_',' ')


    if request.method == 'POST':
        
        category = Category.objects.get(name = category_name) 
        
        form = EditCategoryForm(request.POST,initial = {'name':category_name_url, 'views':category.views,'likes':category.likes})
        
        new_views = request.POST.get('views')    
        new_likes = request.POST.get('likes')    
        category.views = new_views
        category.likes = new_likes
        category.save()
        
        
        return index(request)

             
         
         
    else:
     
        form = EditCategoryForm(initial = {'name':category_name_url})
    
       
   # context_dict = {'form':form}
        #return HttpResponse("Category Name Is "+str(category_name_url))
   # return render_to_response('rango/edit_category.html', context_dict , context)

    return render_to_response( 'rango/edit_category.html',
                              {'category_name_url':category_name_url,
                               'category_name': category_name, 'form':form},
                            context)

@login_required
def add_page(request, category_name_url):
    
    context = RequestContext(request) 
    
    category_name = decode_url(category_name_url)
    
    if request.method == 'POST':
        
        form = PageForm(request.POST)
        
        if form.is_valid():
            
            page = form.save(commit = False)
            
            try:
                
                cat = Category.objects.get(name = category_name)
                page.category = cat 
                
            except Category.DoesNotExist:
                
                return render_to_response('rango/add_category.html', {}, context)
            
            page.views = 0
            
            page.save()
            
            return category(request, category_name_url)               
                
            
        else:
            
            return HttpResponse("Invalid Form or Data")
            
        
    else:
        
        form = PageForm()
        
    return render_to_response( 'rango/add_page.html',
                              {'category_name_url':category_name_url,
                               'category_name': category_name, 'form':form},
                            context)

def edit_page(request, category_name_url):  
    
    context = RequestContext(request) 
    
    category_name = decode_url(category_name_url)
 
    category = Category.objects.get(name = category_name) 
                
    pages = Page.objects.filter(category = category)
    
    if request.method == 'POST':
        
        
        form = PageEditForm(request.POST, initial={'title': pages.title, 'url':category_name_url})   
            
        page.save()
            
        return category(request, category_name_url)     
            
        
    else:
        
        form = PageEditForm( initial={'title': "pages.title", 'url':category_name_url})
    
    return render_to_response( 'rango/add_page.html',
                              {'category_name_url':category_name_url,
                               'category_name': category_name, 'form':form}, context)
      
def register(request):
    
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save() 
            
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit = False)
            profile.user = user
            
            if 'picture' in request.FILES:
                
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            registered = True
        else:
            
            print user_form.errors(),  profile_form.errors()
    else:
        
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    
    return render_to_response(
                              'rango/register.html',
                              {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
                              context)
def user_login(request):
    
    context = RequestContext(request)
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        
        if user:
            
            if user.is_active:
                
                login(request, user)
                return HttpResponseRedirect('/rango/')
            
            else:
                
                return HttpResponse("Your rango account is disabled")
        else:
            
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:

        return render_to_response('rango/login.html', {}, context)  

@login_required
def user_logout(request):
    
    logout(request)   
    
    return HttpResponseRedirect('/rango/')


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
   