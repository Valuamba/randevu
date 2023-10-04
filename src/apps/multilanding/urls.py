from django.urls import path
from apps.multilanding.api.view import WebSiteViewSet


urlpatterns = [
    path('website', WebSiteViewSet.as_view({'get': 'retrieve'}), name='get-website'),
    path('website/update', WebSiteViewSet.as_view({'put': 'update'})),
    path('open/website', WebSiteViewSet.as_view({'get': 'retrieve'}), name='get-website'),

    path('open/company', WebSiteViewSet.as_view({'get': 'company'})),

    path('company', WebSiteViewSet.as_view({'get': 'info'})),
    path('open/info', WebSiteViewSet.as_view({'get': 'info'})),

    path('settings', WebSiteViewSet.as_view({'get': 'retrieve_settings'})),
    path('settings/update', WebSiteViewSet.as_view({'put': 'update_settings'}))

] 
