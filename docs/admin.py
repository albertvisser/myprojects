"""Register models to the admin site
"""
from django.contrib import admin
import docs.models as my

admin.site.register(my.Project)      # , ProjectAdmin)
admin.site.register(my.Userspec)     # , UserspecAdmin)
admin.site.register(my.Userdoc)      # , UserdocAdmin)
admin.site.register(my.Userwijz)     # , UserwijzAdmin)
admin.site.register(my.Userprob)     # , UserprobAdmin)
admin.site.register(my.Funcdoc)      # , FuncdocAdmin)
admin.site.register(my.Gebrtaak)     # , GebrtaakAdmin)
admin.site.register(my.Funcproc)     # , FuncprocAdmin)
admin.site.register(my.Entiteit)     # , EntiteitAdmin)
admin.site.register(my.Attribuut)    # , AttribuutAdmin)
admin.site.register(my.Techtask)     # , TechtaskAdmin)
admin.site.register(my.Techproc)     # , TechprocAdmin)
admin.site.register(my.Dataitem)     # , DataitemAdmin)
admin.site.register(my.Dataelement)  # , DataelementAdmin)
admin.site.register(my.Layout)       # , LayoutAdmin)
admin.site.register(my.Procproc)     # , ProcprocAdmin)
admin.site.register(my.Testplan)     # , TestplanAdmin)
admin.site.register(my.Testcase)     # , TestcaseAdmin)
admin.site.register(my.Bevinding)    # , BevindingAdmin)
