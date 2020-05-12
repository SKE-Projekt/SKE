from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SKE_SANDBOX.urls')),
    path('user/', include('SKE_USERS.urls'))
]
