from django.contrib import admin
from NewBroadcast.models import *

'''
class SourceInline(admin.StackedInline):
    model = Source;
    fields = ['doc'];
    extra = 1;


class PictureInline(admin.StackedInline):
    model = Picture;
    fields = ['doc'];
    extra = 1;


class ProgramAdmin(admin.ModelAdmin):
    fields = ['series', 'title', 'description', 'weight',
              'page_format', 'recorder', 'workers']
    inlines = [SourceInline, PictureInline]


admin.site.register((User, ProgramGroup, ProgramSeries, Comment))
# admin.site.register(ProgramGroup, ProgramGroupAdmin)
# admin.site.register(ProgramSeries, ProgramSeriesAdmin)
admin.site.register(Program, ProgramAdmin)
'''

admin.site.register((User, ProgramGroup, ProgramSeries, Program,
                     Source, Comment, Praise, Favorite))
