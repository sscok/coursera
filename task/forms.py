# Import form modules
from django import forms
from task import script

BASE="https://www.coursera.org"
URL = "https://www.coursera.org/browse"

class CategoryForm(forms.Form):
    
    categories_dict = script.find_categories(URL)
    CATEGORY_CHOICES= [tuple([x['category'],x['category']]) for x in categories_dict]

    categories= forms.CharField(label='Select a Coursera category', widget=forms.Select(choices=CATEGORY_CHOICES))