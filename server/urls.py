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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(
        settings.API_VERSION,
        include(
            [
                path("auth/", include("iam.urls")),
                path("student/", include("student.urls")),
                path("teacher/", include("teacher.urls")),
                path("course/", include("course.urls")),
                path("classes/", include("classes.urls")),
                path("score/", include("score.urls")),
                path("chat/", include("chat.urls")),
                path("", include("common.urls")),
            ]
        ),
    ),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    urlpatterns.append(
        path("docs/", include_docs_urls(title="Next数字校园Api文档", description="Django"))
    )
