from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .tokens import generate_token
from django.contrib.auth.decorators import login_required
from .models import FinalRecipe


from django.core.paginator import Paginator
from django.views.generic import ListView
from django import template
register = template.Library()



# Create your views here.
def index(request):
    # return HttpResponse("Hello World!")
    recipes = FinalRecipe.objects.all()
    context = {
        'recipe':recipes
    }
    return render(request,'index3.html',context)

# @login_required
# def food(request):
#     qs = FinalRecipe.objects.all()
#     ingredients_contain_query = request.GET.get('ingredients_contain')
#     cuisine_contain_query = request.GET.get('cuisine_name')

#     # if ingredients_contain_query != '' and ingredients_contain_query is not None:
#     #     qs = qs.filter(Q(ingredients__icontains=ingredients_contain_query))

#     if not request.user.is_authenticated:
#         messages.error(request,"Please login to access this page")
#         return redirect('signin')

#     if ingredients_contain_query:
#         ingredients = ingredients_contain_query.split(', ')
#         ingredient_queries = [Q(ingredients__icontains=ingredient) for ingredient in ingredients]
#         ingredient_query = Q()
#         for query in ingredient_queries:
#             ingredient_query &= query
#         qs = qs.filter(ingredient_query)

#     if cuisine_contain_query != '' and cuisine_contain_query is not None:
#         qs = qs.filter(cuisine__icontains=cuisine_contain_query)
#     # context = {
#     #     'queryset':qs
#     # }
#     paginator = Paginator(qs, {2})
#     page_number = request.GET.get('page', (1))
#     page = paginator.get_page(page_number)
#     context = {
#         'queryset':qs,
#         'page':page
#     }
#     return render(request,'food.html',context)



from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class FoodView(LoginRequiredMixin, ListView):
    queryset = FinalRecipe.objects.all().order_by('id')
    paginate_by = 8
    template_name = 'recipeLIST.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        ingredients_contain_query = self.request.GET.get('ingredients_contain')
        cuisine_contain_query = self.request.GET.get('cuisine_name')
        

        if ingredients_contain_query:
            ingredients = ingredients_contain_query.split(', ')
            ingredient_queries = [Q(ingredients__icontains=ingredient) for ingredient in ingredients]
            ingredient_query = Q()
            for query in ingredient_queries:
                ingredient_query &= query
            qs = qs.filter(ingredient_query)

        if cuisine_contain_query != '' and cuisine_contain_query is not None:
            qs = qs.filter(cuisine__icontains=cuisine_contain_query)
        
        return qs
        


from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


class SignUpView(FormView):
    template_name = "signup3.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        user = form.save()
        messages.success(request, "Your Account has been successfully created. We have send you a confirmation email, "
                                  "please confim your email in order to activate your account")

        # SENDING MAIL
        subject = "Welcome to Dish Discovery"
        email_message = (f"Hello {myuser.first_name} \nWelcome to Dish Discovery \nWe have send you a confirmation "
                         f"link on your registered email, Please click on the link in order to activate your account. \n\nThanking you \nTeam Dish Discovery")
        from_email = settings.EMAIL_HOST_USER
        to_user = [myuser.email]
        send_mail(subject, email_message, from_email, to_user, fail_silently=True)

        # CONFIRMATION EMAIL
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email @Dish Discovery!"
        email_message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            email_message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect("signin")
        # send your mails
        # set your messages
        return super().form_valid(form)





# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
#
#         if User.objects.filter(username=username):
#             messages.error(request,"Username Already Exist!. Try something other username")
#             return render(request, 'signup3.html')
#
#         if User.objects.filter(email=email):
#             messages.error(request,"Email Alreday Exist")
#             return render(request, 'signup3.html')
#
#         if len(username) > 10 and username != fname:
#             messages.error(request,"Username should be less than 10 Characters")
#             return render(request, 'signup3.html')
#
#         if pass1 != pass2:
#             messages.error(request,"Password Didn't Match")
#             return render(request, 'signup3.html')
#
#         if not username.isalnum():
#             messages.error(request,"Username should have Alpha-numeric")
#             return render(request, 'signup3.html')
#
#         # if not email.endswith('@gmail.com'):
#         #     messages.error(request,"Only Gmail accounts are allowed.")
#         #     return redirect('index')
#
#         myuser = User.objects.create_user(username,email,pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.is_active = False
#
#         myuser.save()
#         messages.success(request,"Your Account has been successfully created. We have send you a confirmation email, "
#                                  "please confim your email in order to activate your account")
#
#         #SENDING MAIL
#         subject = "Welcome to Dish Discovery"
#         email_message = (f"Hello {myuser.first_name} \nWelcome to Dish Discovery \nWe have send you a confirmation "
#                     f"link on your registered email, Please click on the link in order to activate your account. \n\nThanking you \nTeam Dish Discovery")
#         from_email = settings.EMAIL_HOST_USER
#         to_user = [myuser.email]
#         send_mail(subject,email_message,from_email,to_user, fail_silently=True)
#
#         #CONFIRMATION EMAIL
#         current_site = get_current_site(request)
#         email_subject = "Confirm Your Email @Dish Discovery!"
#         email_message2 = render_to_string('email_confirmation.html',{
#             'name':myuser.first_name,
#             'domain':current_site.domain,
#             'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token':generate_token.make_token(myuser)
#         })
#         email = EmailMessage(
#             email_subject,
#             email_message2,
#             settings.EMAIL_HOST_USER,
#             [myuser.email],
#         )
#         email.fail_silently = True
#         email.send()
#
#
#         return redirect("signin")
#
#     return render(request,'signup3.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        print(user)

        if user is not None:
            login(request, user)
            fname = user.first_name
            request.session['username'] = username
            return render(request, 'index2.html', {'fname': fname})
        else:
            messages.error(request, "Account not activated. Please check your email.")
            return redirect('index')

    return render(request,'signin2.html')

def signout(request):
    logout(request)
    messages.success(request,"You have Successfully Log out")
    return redirect('index')

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('index')
    else:
        return render(request,'activation_failed.html')





def recipe_details(request, recipe_id):
    recipe = get_object_or_404(FinalRecipe, pk=recipe_id)
    return render(request, 'recipe_details.html', {'recipe': recipe})
