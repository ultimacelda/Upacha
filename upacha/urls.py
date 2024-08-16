from django.contrib import admin
from django.urls import include, path

from innerpost.views import add_view, check_view, status_view, index_view, LetterList, success_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view),
    path('check-messages/', check_view),
    path('status_view/', status_view, name='status_view'),
    path('success/', success_view, name='success'),
    path('add-mail/', add_view),
    path('api/auth/', include('rest_framework.urls')),
    path('api/letter/', LetterList.as_view()),
    
]
