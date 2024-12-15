 
 
from django.urls import path
from .import views

urlpatterns = [
    
     path('',views.show ,name='home'),
     path('breed/<int:id>/',views.breed_view,name="breed"),
    
     path('addprod/<int:id>/',views.addprod,name="addprod"),
    
     
     path('petform/',views.petview),
     path('register/',views.register,name="register"),

     path('showpet/<int:id>/',views.showpet,name='showpet'),

     path('login/',views.user_login,name='user_login'),
    
     path('logout/',views.signout,name='logout'),
     path('searchproduct/',views.searchproduct,name='searchproduct'),
     

     path('checkout/',views.checkoutnew,name="checkout"),

     path('payment_success/',views.paymentsuccessful,name='paymentsuccess'),

     path('payment_failed/',views.paymentfailed,name='paymentfailed'),









     path('range',views.range,name='range'),

     path('updateqty/<qv>/<cid>/',views.updateqty),
     
     path('remove/<cid>',views.remove),
     
     path('placeorder/',views.placeorder,name='placeorder'),
  
     path('address/',views.customer_address,name="address"),
     path('sort/<sv>',views.sort),
     

     path('forgotpassword/',views.forgot_password, name="forgotpassword"),

     path('reset_password/<uidb64>/<token>/', views.reset_password, name='resetpassword'),

     path('password_reset_done/', views.password_reset_done, name='passwordresetdone'),








      path('addtocart/<pid>',views.addtocart,name='addtocart'),
      path('addpet',views.addpet,name='addpet'),
      
      path('viewcart',views.viewcart),
      path('order/',views.order,name="order"),

      # path('setcookie/',views.set_cookie),

      # path('getcookie/',views.get_cookie),

      path('drf_crud/',views.crud_api.as_view(),name='crud'),
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
      
 
 
]
