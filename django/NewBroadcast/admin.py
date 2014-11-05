from django.contrib import admin
from NewBroadcast.models import *

class ProgramInline(admin.ModelAdmin):
    model = Source;
    fields = ('source_type', 'doc');
    extra = 1;
    

class PictureInline(admin.ModelAdmin):
    model = Source;
    fields = ('source_type', 'doc');
    extra = 1;


class ProgramAdmin(admin.ModelAdmin):
    fields = ['series_id', 'title', 'description', 'weight', 'page_format', 'recorder', 'workers']
    inlines = [ProgramInline, PictureInline]


admin.site.register((User, ProgramGroup, ProgramSeries, Comment))
# admin.site.register(ProgramGroup, ProgramGroupAdmin)
# admin.site.register(ProgramSeries, ProgramSeriesAdmin)
admin.site.register(Program, ProgramAdmin)