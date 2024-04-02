"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path("docs/", include_docs_urls(title="DRF Api文档", description="Django")),
    path("api/v1/auth/", include("iam.urls")),
    path("api/v1/student/", include("student.urls")),
    path("api/v1/teacher/", include("teacher.urls")),
    path("api/v1/course/", include("course.urls")),
    path("api/v1/classes/", include("classes.urls")),
    path("api/v1/", include("common.urls")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
