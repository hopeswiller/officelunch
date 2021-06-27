from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings
import re   
from django import forms

# Create your models here.

class Employs(models.Model):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email + ' - ' + self.firstname



def validate_product_name(prodname):
    regex_string = r'^\w[\w ]*$'
    search = re.compile(regex_string).search
    result = bool(search(prodname))
    if not result:
        raise ValidationError("Please only use letters, "
                              "numbers and underscores or spaces. "
                              "The name cannot start with a space.")

class Product(models.Model):
    meal = models.CharField(max_length=50,
                            validators=[validate_product_name])
    price = models.DecimalField(max_digits=9,decimal_places=2,default=0)

    def __str__(self):
        return self.meal
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular product instance.
        """
        return reverse('product-detail', args=[str(self.id)])

    def clean(self):
        validate_product_name(self.meal)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.full_clean()
        return super(Product, self).save(*args, **kwargs)


class Order(models.Model):
    email = models.EmailField() 
    meal = models.CharField(max_length=50,default='meal name')                       
    price = models.DecimalField(max_digits=9,decimal_places=2,default=0)
    quantity = models.IntegerField(default=0)
    comments = models.TextField(max_length=500,default='no comments yet...')  
    last_change = models.DateTimeField(auto_now=True)

    #def get_absolute_url(self):
     #   return reverse('view_order', args=[self.id])

    def __str__(self):
        return self.meal + ' - Quantity(' + str(self.quantity) + ') - ' + "Transaction on: {:%B %d, %Y; %H:%M}".format(self.last_change)




class Feedback(models.Model):
    EmployeeFirstname = models.CharField(max_length=20)
    EmployeeDepartment = models.CharField(max_length=20)
    Product = models.CharField(max_length=20)
    Content = models.TextField(max_length=500)
    DateSent = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Employee '+ self.EmployeeFirstname + ' gave feedback on ' + self.Product + " {:%B %d, %Y; %H:%M}".format(self.DateSent)





class Setting(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.key

    def __bool__(self):
        return bool(self.value)

    __nonzero__ = __bool__