from django.conf import settings
from django.conf.urls.static import static


from django.urls import path
from . import views
from .views import FoodView, SignUpView

urlpatterns = [
    path('',views.index,name='index'),
    path('search',FoodView.as_view(),name='food'),
    # path('search/',views.food,name='food'),
    # path('signup',views.signup,name='signup'),

    path('signup/', SignUpView.as_view(), name='signup'),

    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),


    path('recipe/<int:recipe_id>/', views.recipe_details, name='recipe_details'),

]