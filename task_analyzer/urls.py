from django.contrib import admin
from django.urls import path, include
from tasks import views  # <--- We import the views from your app

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This line handles the API calls (like analyze tasks)
    path('api/tasks/', include('tasks.urls')),
    
    # This NEW line tells Django: "When someone visits the homepage (''), show the index view"
    path('', views.index, name='home'),
]