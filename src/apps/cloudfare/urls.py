from django.urls import path, include

from apps.cloudfare.api.views import RetrieveUniqueCloudfareImageResizingLinks


urlpatterns = [
    path('cloudfare/<str:count>/resizing-links/', RetrieveUniqueCloudfareImageResizingLinks.as_view())
]