from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import BlogPost

# class BlogPostForm(forms.ModelForm):
#     content = forms.CharField(
#         widget=CKEditor5Widget(config_name='default'),
#         label="Content"
#     )

#     class Meta:
#         model = BlogPost
#         fields = [
#             "title",
#             "category",
#             "image",
#             "excerpt",
#             "content",
#             "is_featured",
#         ]
#         widgets = {
#             "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter post title"}),
#             "category": forms.Select(attrs={"class": "form-select"}),
#             "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
#             "excerpt": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Short summary"}),
#             "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
#         }
#         labels = {
#             "excerpt": "Short Description",
#             "image": "Cover Image",
#             "is_featured": "Feature this post",
#         }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'class': 'ckeditor'}),
        }