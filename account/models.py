from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
import pycountry
from django.conf import settings  # Import settings to reference the AUTH_USER_MODEL
from tinymce.models import HTMLField
from django.db.models.signals import post_migrate
from django.dispatch import receiver


#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser,PermissionsMixin):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  
  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin
  
  def get_all_permissions(self, obj=None):
        if not self.is_active or self.is_anonymous:
            return set()
        if not hasattr(self, '_perm_cache'):
            self._perm_cache = set(super().get_all_permissions(obj))
        return self._perm_cache  





# class CategoryType(models.Choices):
#     blog = 'blog'
#     service = 'service'
#     project = 'project'
#     courses = 'courses'

# class Categorie(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     category_type=models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    


from django.db import models

class CategoryType(models.TextChoices):
    BLOG = 'blog', 'Blog'
    SERVICE = 'service', 'Service'
    PROJECT = 'project', 'Project'
    COURSES = 'courses', 'Courses'


# class CategoryManager(models.Manager):
#     def get_by_type(self, type):
#         return self.filter(category_type=type)

class CategoryManager(models.Manager):
    def get_by_type(self, type=None, name=None):
        """
        Filters categories by type and/or name.
        If both type and name are provided, it filters by both.
        If only one is provided, it filters by whichever is given.
        """
        queryset = self.all()
        if type:
            queryset = queryset.filter(category_type=type)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class Categorie(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    category_type = models.CharField(
        max_length=10,
        choices=CategoryType.choices,
    )
    objects = CategoryManager()

    def __str__(self):
        # return self.name
        return f"{self.name} ({self.category_type})"



class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField(max_length=1500)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # New ImageField
    published_date = models.DateField()
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title



class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    content = models.TextField()
    category = models.ManyToManyField(Categorie,related_name='categories')
    image = models.ImageField(upload_to='Project_images/', blank=True, null=True)  # New ImageField

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to='Service_images/', blank=True, null=True)  # New ImageField
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)



# class Course(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.CharField(max_length=500)
#     content = models.TextField()
#     category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='course_images/', blank=True, null=True)

#     def __str__(self):
#         return self.title


from django.core.validators import RegexValidator
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class TeamMember(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    role = models.CharField(max_length=500)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    description = models.CharField(max_length=5000)
    content = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='team_member_images/', blank=True, null=True)  # New ImageField
 

# from django.core.exceptions import ValidationError
# from PIL import Image
# from io import BytesIO

# def validate_aspect_ratio(image, expected_ratio=21/9):
#     # Open the image file
#         im = Image.open(image)
#         width, height = im.size

#     # Calculate the aspect ratio
#         actual_ratio = width / height

#     # Check the aspect ratio
#         if not (actual_ratio == expected_ratio):
#             raise ValidationError(f'The aspect ratio of the image must be {expected_ratio:.2f}. Current ratio is {actual_ratio:.2f}.')




# class About_U(models.Model):
#     description = models.TextField(max_length=5000)
#     content = models.TextField('write about vision',max_length=5000)
#     # feature_image = models.ImageField(upload_to='aboutUs_images/', blank=True, null=True)  # New ImageField
#     feature_image = models.ImageField(
#         upload_to='aboutUs_images/',
#         blank=True, 
#         null=True,
#         validators=[validate_aspect_ratio]  # Use the custom validator here
#     )


class About_U(models.Model):
    description = models.CharField(max_length=5000)
    content = models.TextField('write about vision', max_length=5000)
    feature_image = models.ImageField(upload_to='aboutUs_images/', blank=True, null=True)



class Contact_U(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    object = models.CharField(max_length=50,blank=True, null=True)
    message = models.TextField()




class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    skuId = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True, upload_to='products/%Y/%m/%d/')
    description = models.TextField(blank=True, null=True)  # Optional text field for product description

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.title} Image"


    # def save(self, *args, **kwargs):
    #     # Process the feature_image if it exists
    #     if self.feature_image:
    #         # Open the image
    #         img = Image.open(self.feature_image)

    #         # Define the new width and height maintaining 21:9 ratio
    #         original_width, original_height = img.size
    #         new_width = original_width
    #         new_height = int(new_width / (16 / 9))

    #         # Resize the image to new dimensions
    #         if img.height != new_height or img.width != new_width:
    #             new_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Updated here
                
    #             # Save the resized image to a BytesIO object
    #             image_temp = BytesIO()
    #             new_img.save(image_temp, format=img.format)

    #             # Set save=False, otherwise it will run in an infinite loop
    #             self.feature_image.save(self.feature_image.name, InMemoryUploadedFile(
    #                 image_temp,  # file
    #                 None,  # field_name
    #                 self.feature_image.name,  # file name
    #                 'image/jpeg',  # content_type
    #                 image_temp.tell(),  # size
    #                 None)  # content_type_extra
    #             , save=False)

    #     super().save(*args, **kwargs)





# class Categorie(models.Model):
    
#     name = models.CharField(max_length=255)
#     blog_post_categories=models.CharField(max_length=255)
#     def __str__(self):
#         return self.name
    

# class Event(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     location = models.CharField(max_length=255, blank=True, null=True)
#     organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
#     image = models.ImageField(upload_to='events_images/', blank=True, null=True)
#     registration_link = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return self.title

#     @property
#     def is_upcoming(self):
#         from django.utils import timezone
#         return self.start_time > timezone.now()

#     @property
#     def duration(self):
#         return self.end_time - self.start_time

#     class Meta:
#         ordering = ['start_time']


# class Technologie(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='technology_images/', blank=True, null=True)  # New ImageField
#     description = models.TextField()
    

# class Industrie(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='industry_images/', blank=True, null=True)  # New ImageField
#     description = models.TextField()    

# class RatingChoices(models.IntegerChoices):
#     ONE = 1, '1'
#     TWO = 2, '2'
#     THREE = 3, '3'
#     FOUR = 4, '4'
#     FIVE = 5, '5'

# class Testimonial(models.Model):
#     client_name = models.CharField(max_length=100)
#     client_company = models.CharField(max_length=100)
#     rating = models.IntegerField(choices=RatingChoices.choices)
#     image = models.ImageField(upload_to='testimonial_images/', blank=True, null=True)
#     content = models.TextField()
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)


# class BlogPost(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     # heading = models.TextField('Heading_Content',blank=True)  # Replaces models.TextField()
#     content = models.TextField()
#     category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
#     category_type = models.CharField(max_length=250)
#     published_date = models.DateTimeField()
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # New ImageField

#     def __str__(self):
#         return self.title



# class Project(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     link = models.URLField()
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_projects')
#     category = models.ForeignKey(Categorie, on_delete=models.CASCADE,related_name='Blog_post_categories')
#     # technologies = models.ForeignKey(Technologie, on_delete=models.CASCADE)

#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     status = models.CharField(
#         max_length=20,
#         choices=[('Active', 'Active'), ('Completed', 'Completed'), ('Paused', 'Paused')]
#     )

#     def __str__(self):
#         return self.name

#     @property
#     def technology_used(self):
#         return self.technologies

# class Service(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     image = models.ImageField(upload_to='Service_images/', blank=True, null=True)  # New ImageField
#     related_projects = models.ForeignKey(Project, on_delete=models.CASCADE)




# class RoleChoices(models.TextChoices):
#     ADMIN = 'Admin', 'Administrator'
#     EDITOR = 'Editor', 'Editor'
#     CONTRIBUTOR = 'Contributor', 'Contributor'
#     GUEST = 'Guest', 'Guest'


# class Author(models.Model):
#     Select_author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     username = models.CharField(max_length=100)
#     email = models.EmailField()
#     Author_image = models.ImageField(upload_to='Auther_images/', blank=True, null=True)  # New ImageField
#     roles = models.CharField(max_length=50, choices=RoleChoices.choices, default=RoleChoices.CONTRIBUTOR)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.username






# class Course(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     image = models.ImageField(upload_to='course_images/', blank=True, null=True)

#     def __str__(self):
#         return self.title




# class Comment(models.Model):
#     author_name = models.CharField(max_length=100)
#     author_email = models.EmailField()
#     content = models.TextField()
#     posted_date = models.DateTimeField()
#     post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

# class CompanyInformation(models.Model):
#     about_us = models.TextField()
#     mission = models.TextField()
#     vision = models.TextField()
#     # Assuming team members are separate for scalability
#     contact = models.IntegerField()

# class TeamMember(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=100)
#     bio = models.TextField()
#     image = models.ImageField(upload_to='team_member_images/', blank=True, null=True)  # New ImageField
#     social_media_links = models.CharField(max_length=255)






# class ContactInquirie(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     received_date = models.DateTimeField(auto_now_add=True)
#     STATUS_CHOICES = [
#         ('New', 'New'),
#         ('In Progress', 'In Progress'),
#         ('Closed', 'Closed'),
#     ]
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)





# class Case(models.Model):
#     STATUS_CHOICES = [
#         ('open', 'Open'),
#         ('in_progress', 'In Progress'),
#         ('closed', 'Closed'),
#         ('on_hold', 'On Hold')
#     ]
#     SERVICE_TYPE_CHOICES = [
#         ('web', 'Web Development'),
#         ('mobile', 'Mobile App Development'),
#         ('software', 'Software Development'),
#     ]
#     PRIORITY_CHOICES = [
#         ('high', 'High'),
#         ('medium', 'Medium'),
#         ('low', 'Low')
#     ]

#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     featured_image = models.ImageField(upload_to='Casefeatured_images/', blank=True, null=True)
#     service_type = models.CharField(max_length=100, choices=SERVICE_TYPE_CHOICES)
#     industries = models.ForeignKey(Industrie, on_delete=models.CASCADE)
#     technologies = models.ForeignKey(Technologie, on_delete=models.CASCADE)
#     country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True, null=True)
#     country_image = models.ImageField(upload_to='case/', blank=True, null=True)
#     case_number = models.CharField(max_length=120, unique=True)
#     status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
#     priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
#     assigned_to = models.ForeignKey(User, related_name='assigned_cases', on_delete=models.SET_NULL, null=True)
#     created_by = models.ForeignKey(User, related_name='created_cases', on_delete=models.CASCADE)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#     due_date = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.case_number} - {self.title}"

#     class Meta:
#         ordering = ['-created_date']



# class ServiceType(models.Model):
#     choice_name = models.TextField(max_length=50)
    


# COUNTRY_CHOICES = [(country.name, country.name) for country in pycountry.countries]
# class Case(models.Model):
#     STATUS_CHOICES = [
#         ('open', 'Open'),
#         ('in_progress', 'In Progress'),
#         ('closed', 'Closed'),
#         ('on_hold', 'On Hold')
#     ]

#     PRIORITY_CHOICES = [
#         ('high', 'High'),
#         ('medium', 'Medium'),
#         ('low', 'Low')
#     ]

#     title = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     featured_image = models.ImageField(upload_to='case_featured_images/', blank=True, null=True)
#     content = models.TextField()
#     service_type = models.ManyToManyField(ServiceType, blank=True)
#     industries = models.ForeignKey(Industrie, on_delete=models.CASCADE)
#     technologies = models.ManyToManyField(Technologie, blank=True)
#     country = models.CharField(max_length=255, choices=COUNTRY_CHOICES, blank=True, null=True)
#     country_image = models.ImageField(upload_to='case_country_images/', blank=True, null=True)
#     status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
#     priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
#     created_by = models.ForeignKey(User, related_name='created_cases', on_delete=models.CASCADE)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#     due_date = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.title}"

#     class Meta:
#         ordering = ['-created_date']




# class Career(models.Model):
#     JOB_TYPES = [
#         ('full_time', 'Full Time'),
#         ('part_time', 'Part Time'),
#         ('contract', 'Contract'),
#         ('internship', 'Internship'),
#     ]

#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     location = models.CharField(max_length=255)
#     job_type = models.CharField(max_length=10, choices=JOB_TYPES, default='full_time')
#     posted_date = models.DateField(auto_now_add=True)
#     closing_date = models.DateField()

#     def __str__(self):
#         return f"{self.title} ({self.job_type})"

#     class Meta:
#         verbose_name = 'Career'
#         verbose_name_plural = 'Careers'
#         ordering = ['-posted_date']




# class PricingEstimate(models.Model):
#     SERVICE_TYPE_CHOICES = [
#         ('web', 'Web Development'),
#         ('mobile', 'Mobile App Development'),
#         ('software', 'Software Development'),
#     ]
#     COMPLEXITY_CHOICES = [
#         ('low', 'Low'),
#         ('medium', 'Medium'),
#         ('high', 'High'),
#     ]

#     service_type = models.CharField(max_length=100, choices=SERVICE_TYPE_CHOICES)
#     feature_set = models.TextField(help_text="Detailed description of the requested features")
#     complexity = models.CharField(max_length=10, choices=COMPLEXITY_CHOICES)
#     estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, help_text="Estimated hours to complete the project")
#     hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Hourly rate for the service")
#     additional_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Additional costs")
#     discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Discounts applied")
#     total_estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Automatically calculated total cost")
#     contact_information = models.EmailField(max_length=255, verbose_name="Contact Information")
#     submitted_on = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=100, default='pending', help_text="Status of the estimate")
    
#     # Add a file upload field
#     file = models.FileField(upload_to='pricing_files/', blank=True, null=True)


#     def save(self, *args, **kwargs):
#         # Calculate total estimated cost
#         self.total_estimated_cost = (self.estimated_hours * self.hourly_rate) + self.additional_costs - self.discounts
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.service_type} for {self.client_information} on {self.submitted_on.strftime('%Y-%m-%d')}"

#     class Meta:
#         verbose_name = 'Pricing Estimate'
#         verbose_name_plural = 'Pricing Estimates'
#         ordering = ['-submitted_on']



# from django.db import models
# from django.core.mail import send_mail
# from django.conf import settings
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from mimetypes import guess_type
# from django.core.mail.message import EmailMessage
# import threading


# class PricingEstimate(models.Model):
#     SERVICE_TYPE_CHOICES = [
#         ('web', 'Web Development'),
#         ('mobile', 'Mobile App Development'),
#         ('software', 'Software Development'),
#     ]
#     COMPLEXITY_CHOICES = [
#         ('low', 'Low'),
#         ('medium', 'Medium'),
#         ('high', 'High'),
#     ]

#     service_type = models.CharField(max_length=100, choices=SERVICE_TYPE_CHOICES)
#     feature_set = models.TextField(help_text="Detailed description of the requested features")
#     complexity = models.CharField(max_length=10, choices=COMPLEXITY_CHOICES)
#     estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, help_text="Estimated hours to complete the project")
#     hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Hourly rate for the service")
#     additional_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Additional costs")
#     discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Discounts applied")
#     total_estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Automatically calculated total cost")
#     contact_information = models.EmailField(max_length=255, verbose_name="Contact Information")
#     submitted_on = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=100, default='pending', help_text="Status of the estimate")
    
#     # Add a file upload field
#     file = models.FileField(upload_to='pricing_files/', blank=True, null=True)

# lock = threading.Lock()

# @receiver(post_save, sender=PricingEstimate)
# def send_email_on_new_estimate(sender, instance, created, **kwargs):
#     if created:
#         subject = 'New Pricing Estimate Received'
#         message = f"""
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Discounts: {instance.discounts}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}
#         """
#         from_email = '18251598-111@uog.edu.pk'
#         recipient_list = [instance.contact_information]
#         # if instance.file:
#         #     file_attachment = instance.file.file
#         #     send_mail(subject, message, from_email, recipient_list, attachments=[(file_attachment.name, file_attachment.read(), mimetypes.guess_type(file_attachment.name)[0])])
#         # else:
#         #     send_mail(subject, message, from_email, recipient_list)
#         # if instance.file:
#         #     file_attachment = instance.file.file
#         #     email = EmailMessage(subject, message, from_email, recipient_list)
#         #     email.attach(file_attachment.name, file_attachment.read(), file_attachment.file.mimetype)
#         #     email.send()
#         # else:
#         #     send_mail(subject, message, from_email, recipient_list)
#         # if instance.file:
#         #     file_attachment = instance.file.file
#         #     mimetype, _ = guess_type(file_attachment.name)
#         #     email = EmailMessage(subject, message, from_email, recipient_list)
#         #     email.attach(file_attachment.name, file_attachment.read(), mimetype)
#         #     email.send()
#         # else:
#         #     send_mail(subject, message, from_email, recipient_list)


#         with lock:
#             if instance.file:
#                 file_attachment = instance.file.file
#                 mimetype, _ = guess_type(file_attachment.name)
#                 email = EmailMessage(subject, message, from_email, recipient_list)
#                 email.attach(file_attachment.name, file_attachment.read(), mimetype)
#                 email.send()
#             else:
#                 send_mail(subject, message, from_email, recipient_list)



# @receiver(post_save, sender=PricingEstimate)
# def send_email_on_new_estimate(sender, instance, created, **kwargs):
#     if created:
#         subject = 'New Pricing Estimate Received'
#         message = f"""
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Discounts: {instance.discounts}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}
#         """
#         from_email = '18251598-111@uog.edu.pk'
#         recipient_list = [instance.contact_information]
#         send_mail(subject, message, from_email, recipient_list)

    # def __str__(self):
    #   return f"{self.service_type} - {self.total_estimated_cost}"

    # def save(self, *args, **kwargs):
    #     is_new = self.pk is None  # Check if the instance is new
    #     super().save(*args, **kwargs)  # Call the real save() method
    #     if is_new:  # Only send email if it's a new instance
    #         subject = 'Thank you for your request'
    #         message = f"Dear user, thank you for your request. Here are the details:\n\nService Type: {self.service_type}\nComplexity: {self.complexity}\nEstimated Hours: {self.estimated_hours}\nHourly Rate: {self.hourly_rate}\nAdditional Costs: {self.additional_costs}\nDiscounts: {self.discounts}\nTotal Estimated Cost: {self.total_estimated_cost}\n\nBest regards,\nYour Company Name"
    #         send_mail(
    #             subject,
    #             message,
    #             settings.EMAIL_HOST_USER,
    #             [self.contact_information],
    #             fail_silently=False,
    #         )

    # def __str__(self):
    #     return f"{self.service_type} - {self.total_estimated_cost}"



    # def save(self, *args, **kwargs):
    #     is_new = self.pk is None
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
    #     if is_new:
    #         send_mail(
    #             'Pricing Estimate Created',
    #             'Here is the message.',
    #             '18251598-111@uog.edu.pk',
    #             [self.contact_information],
    #             fail_silently=False,
    #         )


    # def save(self, *args, **kwargs):
    #     # Calculate total estimated cost
    #     self.total_estimated_cost = (self.estimated_hours * self.hourly_rate) + self.additional_costs - self.discounts
    #     super().save(*args, **kwargs)  # Call the real save() method

    #     # Send email notification to admin
    #     subject = "Pricing Estimate Submission"
    #     message = (f"New Pricing Estimate Submitted:\n\n"
    #                f"Service Type: {self.service_type}\n"
    #                f"Features: {self.feature_set}\n"
    #                f"Complexity: {self.complexity}\n"
    #                f"Estimated Hours: {self.estimated_hours}\n"
    #                f"Hourly Rate: {self.hourly_rate}\n"
    #                f"Additional Costs: {self.additional_costs}\n"
    #                f"Discounts: {self.discounts}\n"
    #                f"Total Estimated Cost: {self.total_estimated_cost}\n"
    #                f"Contact Information: {self.contact_information}\n"
    #                f"Submitted On: {self.submitted_on.strftime('%Y-%m-%d %H:%M')}\n"
    #                f"Status: {self.status}\n")
    #     from_email = settings.EMAIL_HOST_USER
    #     recipient_list = ['admin@example.com']  # Admin's email, adjust as necessary

    #     send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    # def save(self, *args, **kwargs):
    #     # Save the instance
    #      super().save(*args, **kwargs)

    #     # Send email
    #      subject = 'New Pricing Estimate Received'
    #      context = {
    #         'service_type': self.service_type,
    #         'feature_set': self.feature_set,
    #         # Add more fields as needed
    #     }
    #      html_message = render_to_string('pricing_email.html', context)
    #      plain_message = strip_tags(html_message)
    #      from_email = '18251598-111@uog.edu.pk'  # Replace with your email
    #      to_emails = ['admin@example.com']  # Replace with admin's email
    #      send_mail(subject, plain_message, from_email, to_emails, html_message=html_message)
 








# class Update(models.Model):
#     COMPLEXITY_CHOICES = [
#         ('expert', 'Expert'),
#         ('service', 'Service'),
     
#     ]
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     image = models.ImageField(upload_to='updates/', blank=True, null=True)
#     category = models.TextField(max_length=255, choices = COMPLEXITY_CHOICES)

#     def __str__(self):
#         return self.title
    

# class QuestionsAnswer(models.Model):
#     Question = models.TextField(verbose_name="Question")
#     Answer = models.TextField(verbose_name="Answer")

#     def __str__(self):
#         return f"Question: {self.Question} | Answer: {self.Answer}"
    

# # Predefined QnA data
# DEFAULT_QNA_DATA = [
#     {
#         "Question": "What services do you offer?",
#         "Answer": "We offer a variety of services including web development, app development, and digital marketing."
#     },
#     {
#         "Question": "How can I contact customer support?",
#         "Answer": "You can reach our customer support at support@example.com."
#     },
#     {
#         "Question": "Where is your company located?",
#         "Answer": "Our main office is located in New York City."
#     },
#     {
#         "Question": "Do you offer international shipping?",
#         "Answer": "Yes, we offer shipping to numerous countries around the globe."
#     },
#     {
#         "Question": "What are your operating hours?",
#         "Answer": "We operate from 9 AM to 5 PM on weekdays."
#     }
# ]

# @receiver(post_migrate)
# def populate_qna(sender, **kwargs):
#     if sender.name == 'account':  # Replace 'your_app_name' with the name of your app
#         for item in DEFAULT_QNA_DATA:
#             QuestionsAnswer.objects.get_or_create(Question=item["Question"], defaults={'Answer': item["Answer"]})






# class Industries_we_serve(models.Model):
#     name = models.CharField(max_length=255)
#     description = HTMLField('Write description here', blank=True)
#     features_overview = models.TextField()
#     image = models.ImageField(upload_to='Project_weServed_images/')
#     technologies = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name