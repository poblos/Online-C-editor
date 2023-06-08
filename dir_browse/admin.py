from django.contrib import admin

from .models import Directory, File, CompilationSettings, Standard, DependantOption, Processor, Optimization

admin.site.register(Directory)
admin.site.register(File)
admin.site.register(CompilationSettings)
admin.site.register(Standard)
admin.site.register(Processor)
admin.site.register(DependantOption)
admin.site.register(Optimization)

# Register your models here.
