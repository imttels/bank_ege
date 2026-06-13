from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tasks import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("tasks/", include("tasks.urls")),

    path("topics/", views.topic_list, name="topic_list"),
    path("topics/<int:topic_id>/", views.tasks_by_topic, name="tasks_by_topic"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)