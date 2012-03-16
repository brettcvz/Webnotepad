from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webnotepad.views.home', name='home'),
    # url(r'^webnotepad/', include('webnotepad.foo.urls')),
    url(r'^$', 'webnotepad.editor.views.index'),
    url(r'^open/$', 'webnotepad.editor.views.open'),
    url(r'^save/$', 'webnotepad.editor.views.save'),
    url(r'^import/$', 'webnotepad.editor.views.import_file'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
