from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
 
# creating a validator function
def validate_my_mail(value):
    if "@gmail.com" in value:
        return value
    else:
        raise ValidationError("This field accepts mail id of google only")
 
 
class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name
    

class Pet(models.Model):
    petname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField(blank=True, null=True)
    image=models.ImageField(upload_to='images/')

    def __str__(self):
        return self.petname
    

class Order(models.Model):
     
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Pet,on_delete=models.CASCADE,db_column="pid")
    
    qty=models.IntegerField(default=1)  
                  
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Pet,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)  
    




class Orders(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
   
    def __str__(self):
        return f"Order #{self.id} - {self.status}"

 
  
  
 
  
 






 













    
class PetDetails(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE)
    medical_history = models.TextField(blank=True, null=True)
    last_vet_visit = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Details of {self.pet}"
    


    
class customer(models.Model):
    cust_name=models.CharField(max_length=100)
    
    email = models.CharField(
                         max_length = 200,
                         validators =[validate_my_mail]
                         )
    mobile=models.BigIntegerField()
    address=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_name

class Customer_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # we have created Many-to-one relationship i.e multiple order can be done by one user
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    pincode = models.IntegerField(
        default=0,
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return str(self.id)