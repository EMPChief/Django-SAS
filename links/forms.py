from django import forms
from .models import Category, Link

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'name': forms.TextInput(attrs={'class': 'block font-bold text-lg mb-2 text-gray-700'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        category = super().save(commit=False)
        if not category.pk:
            category.created_by = self.user
        if commit:
            category.save()
        return category

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['name', 'url', 'description', 'category', 'is_active', 'status', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'block w-full p-2 border border-gray-300 rounded-lg'}),
            'url': forms.URLInput(attrs={'placeholder': 'https://example.com', 'class': 'block w-full p-2 border border-gray-300 rounded-lg'}),
            'name': forms.TextInput(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-lg'}),
            'category': forms.Select(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-lg'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'status': forms.Select(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-lg'}),
            'priority': forms.Select(attrs={'class': 'block w-full p-2 border border-gray-300 rounded-lg'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        initial_url = kwargs.pop('initial_url', None)

        super(LinkForm, self).__init__(*args, **kwargs)

        if self.user is not None:
            self.fields['category'].queryset = Category.objects.filter(created_by=self.user)

        if initial_url and not self.initial.get('name'):
            self.initial['name'] = initial_url

    def clean_name(self):
        url = self.cleaned_data.get('url')
        name = self.cleaned_data.get('name')

        if not name and url:
            self.cleaned_data['name'] = url

        return self.cleaned_data['name']




    def save(self, commit=True):
        link = super(LinkForm, self).save(commit=False)
        if not link.pk:
            link.created_by = self.user
        if commit:
            link.save()
        return link


