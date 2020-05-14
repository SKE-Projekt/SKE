from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('_skeadmin/', admin.site.urls),
    path('', include('SKE_SANDBOX.urls')),
    path('user/', include('SKE_USERS.urls')),
    path('courses/', include('SKE_COURSES.urls')),
    path('contests/', include('SKE_CONTESTS.urls'))
]
