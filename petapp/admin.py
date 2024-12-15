from django.contrib import admin

# Register your models here.
from .models import Breed,customer,Pet,Cart,Orders,Customer_details

@admin.register(Cart)
class cartadmin(admin.ModelAdmin):
    list_display=['uid','pid','qty']

# admin.site.register(Cart,cartadmin)


@admin.register(Customer_details)
class customeradmin(admin.ModelAdmin):
    list_display=['user','name','city','state','pincode','address']

class adminBreedmodel(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Breed,adminBreedmodel)
 
class petadmin(admin.ModelAdmin):
    list_display=['petname','age','breed','price','description','image']

admin.site.register(Pet,petadmin)
 

class orderadmin(admin.ModelAdmin):
    list_display=['customer','pet','quantity','order_date','status','total_price']

admin.site.register(Orders,orderadmin)

 