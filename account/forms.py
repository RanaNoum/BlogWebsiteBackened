# from django import forms
# from tinymce.widgets import TinyMCE
# from .models import BlogPost
# ,Case
# from .models import PricingEstimate

# class BlogPostForm(forms.ModelForm):
#     content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

#     class Meta:
#         model = BlogPost
#         fields = ['title', 'description','content', 'category', 'published_date' 'image']
        # Make sure to include all other fields you want to be part of the form

# class CaseForm(forms.ModelForm):
#     content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

#     class Meta:
#         model = Case
#         fields = '__all__'
        
        # Make sure to include all other fields you want to be part of the form

# class PricingEstimateForm(forms.ModelForm):
#     class Meta:
#         model = PricingEstimate
#         fields = ['service_type', 'feature_set', 'complexity', 'estimated_hours', 'hourly_rate', 'additional_costs', 'discounts', 'contact_information', 'file']


from django import forms
from tinymce.widgets import TinyMCE
from .models import BlogPost, Project, Service, TeamMember, About_U

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = BlogPost
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Project
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Service
        fields = '__all__'

# class CourseForm(forms.ModelForm):
#     content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

#     class Meta:
#         model = Course
#         fields = '__all__'


class TeamMemberForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = TeamMember
        fields = '__all__'


class AboutUsForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = About_U
        fields = '__all__'
