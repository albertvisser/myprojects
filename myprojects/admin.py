import myprojects.models as my
from django.contrib import admin

## class ProjectAdmin(admin.ModelAdmin):
    ## pass
## class UserspecAdmin(admin.ModelAdmin):
    ## pass
## class UserdocAdmin(admin.ModelAdmin):
    ## pass
## class UserwijzAdmin(admin.ModelAdmin):
    ## pass
## class UserprobAdmin(admin.ModelAdmin):
    ## pass
## class FuncdocAdmin(admin.ModelAdmin):
    ## pass
## class GebrtaakAdmin(admin.ModelAdmin):
    ## pass
## class FuncprocAdmin(admin.ModelAdmin):
    ## pass
## class EntiteitAdmin(admin.ModelAdmin):
    ## pass
## class AttribuutAdmin(admin.ModelAdmin):
    ## pass
## class TechtaskAdmin(admin.ModelAdmin):
    ## pass
## class TechprocAdmin(admin.ModelAdmin):
    ## pass
## class DataitemAdmin(admin.ModelAdmin):
    ## pass
## class DataelementAdmin(admin.ModelAdmin):
    ## pass
## class LayoutAdmin(admin.ModelAdmin):
    ## pass
## class ProcprocAdmin(admin.ModelAdmin):
    ## pass
## class TestplanAdmin(admin.ModelAdmin):
    ## pass
## class TestcaseAdmin(admin.ModelAdmin):
    ## pass
## class BevindingAdmin(admin.ModelAdmin):
    ## pass

admin.site.register(my.Project)     # , ProjectAdmin)
admin.site.register(my.Userspec)    # , UserspecAdmin)
admin.site.register(my.Userdoc)     # , UserdocAdmin)
admin.site.register(my.Userwijz)    # , UserwijzAdmin)
admin.site.register(my.Userprob)    # , UserprobAdmin)
admin.site.register(my.Funcdoc)     # , FuncdocAdmin)
admin.site.register(my.Gebrtaak)    # , GebrtaakAdmin)
admin.site.register(my.Funcproc)    # , FuncprocAdmin)
admin.site.register(my.Entiteit)    # , EntiteitAdmin)
admin.site.register(my.Attribuut)   # , AttribuutAdmin)
admin.site.register(my.Techtask)    # , TechtaskAdmin)
admin.site.register(my.Techproc)    # , TechprocAdmin)
admin.site.register(my.Dataitem)    # , DataitemAdmin)
admin.site.register(my.Dataelement) # , DataelementAdmin)
admin.site.register(my.Layout)      # , LayoutAdmin)
admin.site.register(my.Procproc)    # , ProcprocAdmin)
admin.site.register(my.Testplan)    # , TestplanAdmin)
admin.site.register(my.Testcase)    # , TestcaseAdmin)
admin.site.register(my.Bevinding)   # , BevindingAdmin)

