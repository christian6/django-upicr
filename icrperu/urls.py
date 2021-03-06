from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'icrperu.views.home', name='home'),
    # url(r'^icrperu/', include('icrperu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^logistica/', include('icrperu.apps.logistica.urls')),
    url(r'^proveedor/', include('icrperu.apps.proveedor.urls')),
    url(r'^ws/logistica/', include('icrperu.apps.logistica.inclogistica.urls')),
    url(r'^ws/proveedor/', include('icrperu.apps.proveedor.incproveedor.urls')),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
