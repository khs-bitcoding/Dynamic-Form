from django.shortcuts import render
from app import models as AM

# Create your views here.
def home(request, type):
    
    data_list = AM.FormFields.objects.filter(form__name=type).select_related('field').all().order_by('index')
    context_data = {
        "Name": type,
        "form_data":data_list
    }
    return render(request, 'index.html', context=context_data)

