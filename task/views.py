from sre_constants import CATEGORY
from django.shortcuts import render
from task.forms import CategoryForm
from django.http import HttpResponse
from task import script
from django.views.generic.base import TemplateView
import csv
from django.shortcuts import redirect

def form_request(request):
    global data
    if request.method == 'POST':
        category = CategoryForm(request.POST)
        categories = request.POST.get("categories")
        data=script.get_attr(categories)
        return redirect('/result')
    else:
        category = CategoryForm()
        return render(request, "form.html", {'form': category})

class CSVPageView(TemplateView):
    template_name = "output.html"

def write_to_csv(request):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="courses.csv"'
        fieldnames = ['Category Name', 'Course Name', 'First Instructor Name', 'Course Description','# of Students Enrolled','# of Ratings']
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for element in data:
            writer.writerow(element)
        return response