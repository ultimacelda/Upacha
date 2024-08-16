from imapclient.exceptions import LoginError, IMAPClientError
from django.core.paginator import Paginator



from rest_framework import generics

from innerpost.fetching import fetch_emails, get_imap_server
from innerpost.models import Letter, Mail 
from .forms import NewMailForm
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

from .serializers import LetterSerializer




def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return HttpResponse("Unauthorized", status=401)

def success_view(request):
    if request.user.is_authenticated:
        return render(request, 'success.html')
    else:
        return HttpResponse("Unauthorized", status=401)

def check_view(request):
    if request.user.is_authenticated:
        letters = Letter.objects.all()

        paginator = Paginator(letters, 10)  # Показывать 10 писем на странице
        page_number = request.GET.get('page')  # Номер текущей страницы из параметров запроса
        page_obj = paginator.get_page(page_number)

        return render(request, 'box.html', {
            'letters': letters,
            'page_obj': page_obj,
            })
    else:
        return HttpResponse("Unauthorized", status=401)

def status_view(request):
    if request.user.is_authenticated:
        for mail_instance in Mail.objects.all():
            email = mail_instance.login
            password = mail_instance.password
            server_address = get_imap_server(email)

        status = fetch_emails(email, password, server_address)
        
        new_messages = status.get('new_messages', False)
        completed = status.get('status') == 'completed'

        response_data = {
            'status': status['status'],
            'email': email,
            'new_messages': new_messages,
            'completed': completed
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({"status": "unauthorized", "message": "Unauthorized"}, status=401)

def add_view(request):
    if request.method == 'POST':
        form = NewMailForm(request.POST)
        if form.is_valid():
            mail = form.save()
            return redirect('success')  
        else:
            print(form.errors)
    else:
        form = NewMailForm()

    return render(request, 'addmail.html', {
        'form': form,
    })

def fetch_emails_async():
    fetch_emails()



# ------------------------------api--------------------------------


class LetterList(generics.ListCreateAPIView):
    
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer