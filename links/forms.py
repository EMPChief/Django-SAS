from django import forms
from .models import Category, Tag, Link

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        category = super(CategoryForm, self).save(commit=False)
        category.created_by = self.user
        if commit:
            category.save()
        return category

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['name', 'url', 'description', 'category', 'is_active', 'tags', 'status', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'tags': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LinkForm, self).__init__(*args, **kwargs)
        if self.user is not None:
            self.fields['category'].queryset = Category.objects.filter(created_by=self.user)

    def save(self, commit=True):
        link = super(LinkForm, self).save(commit=False)
        link.created_by = self.user
        if commit:
            link.save()
            self._save_m2m()
        return link
