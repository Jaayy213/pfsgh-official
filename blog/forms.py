from django import forms
from .models import BlogPost, BlogCategory

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "subtitle", "category", "excerpt", "content", "image", "is_featured"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "subtitle": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "period": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "excerpt": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }