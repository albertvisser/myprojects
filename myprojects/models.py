from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime

class Project(models.Model):
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    oms = models.TextField()
    start = models.CharField(max_length=80)
    fysloc = models.CharField(max_length=80)
    actiereg = models.CharField(max_length=40)
    aruser = models.CharField(max_length=40)
    status = models.TextField()
    def __str__(self):
        return ": ".join((self.naam,self.kort))
    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projecten")

class Userspec(models.Model):
    section = 'user'
    to_titles = {
    }
    from_titles = {
        'gebrtaak': _('Betrokken'),
        'funcproc': _('Betrokken'),
    }
    project = models.ForeignKey(Project,related_name="specs")
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    functie = models.TextField()
    beeld = models.TextField()
    product = models.TextField()
    baten = models.CharField(max_length=80)
    kosten = models.CharField(max_length=80)
    opmerkingen = models.TextField()
    def __str__(self):
        return ": ".join((self.naam,self.kort))
    class Meta:
        verbose_name = _("gebruikersspecificatie")
        verbose_name_plural = _("gebruikersspecificaties")

class Userdoc(models.Model):
    section = 'user'
    to_titles = {}
    from_titles = {}
    project = models.ForeignKey(Project,related_name="docs")
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    link = models.FileField(upload_to='userdoc')
    tekst = models.TextField()
    def __str__(self):
        return ": ".join((self.naam,self.oms))
    class Meta:
        verbose_name = _("naslagdocument")
        verbose_name_plural = _("naslagdocumenten")

class Userwijz(models.Model):
    section = 'user'
    to_titles = {
    }
    from_titles = {
        'gebrtaak': _('Raakt'),
        'funcproc': _('Raakt'),
        'entiteit': _('Raakt'),
    }
    project = models.ForeignKey(Project,related_name="rfcs")
    nummer = models.CharField(max_length=10)
    datum_in = models.DateTimeField(default = datetime.datetime.now,
        editable = False) # auto_now_add=True)
    gereed = models.BooleanField()
    datum_gereed = models.DateTimeField(null=True)
    wens = models.CharField(max_length=80)
    toelichting = models.TextField()
    opmerkingen = models.TextField()
    actie = models.IntegerField(null=True)
    actienummer = models.CharField(max_length=10)
    def __str__(self):
        oms = _(" [afgesloten]") if self.gereed else ""
        return ": ".join((self.nummer,self.wens + oms))
    class Meta:
        verbose_name = _("aanvraag wijziging")
        verbose_name_plural = _("aanvraag wijzigingen")

class Userprob(models.Model):
    section = 'user'
    to_titles = {}
    from_titles = {}
    project = models.ForeignKey(Project,related_name="probs")
    nummer = models.CharField(max_length=10)
    datum_in = models.DateTimeField(auto_now_add=True)
    gereed = models.BooleanField()
    datum_gereed = models.DateTimeField(null=True)
    kort = models.CharField(max_length=80)
    melding = models.TextField()
    oplossing = models.TextField()
    actie = models.IntegerField(null=True)
    actienummer = models.CharField(max_length=10)
    def __str__(self):
        oms = _(" [afgesloten]") if self.gereed else ""
        return "{0}: {1} {2}".format(self.nummer,self.kort,oms)
    class Meta:
        verbose_name = _("incident/probleem")
        verbose_name_plural = _("incidenten/problemen")

class Funcdoc(models.Model):
    section = 'func'
    to_titles = {}
    from_titles = {}
    project = models.ForeignKey(Project,related_name="fdocs")
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    link = models.FileField(upload_to='funcdoc')
    tekst = models.TextField()
    def __str__(self):
        return ": ".join((self.naam,self.oms))
    class Meta:
        verbose_name = _("functioneel document")
        verbose_name_plural = _("functionele documenten")

class Gebrtaak(models.Model):
    section = 'func'
    to_titles = {
        'userspec': _('Hoort bij'),
        'userwijz': _('Is geraakt door'),
    }
    from_titles = {
        'funcproc': _('Wordt bediend door'),
        'techtaak': _('Gerelateerde'),
        'layout': _('Bijbehorende'),
        'testplan': _('Zie'),
    }
    project = models.ForeignKey(Project,related_name="gtaken")
    naam = models.CharField(max_length=40)
    doel = models.CharField(max_length=80)
    wanneer = models.TextField()
    wie = models.TextField()
    condities = models.TextField()
    waarvoor = models.TextField()
    beschrijving = models.TextField()
    spec = models.ForeignKey(Userspec,related_name="gtaken",null=True)
    rfc = models.ManyToManyField(Userwijz,related_name="gtaken",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.doel))
    class Meta:
        verbose_name = _("gebruikerstaak")
        verbose_name_plural = _("gebruikerstaken")

class Funcproc(models.Model):
    section = 'func'
    to_titles = {
        'userspec': _('Hoort bij'),
        'userwijz': _('Is geraakt door'),
        'gebrtaak': _('Bedient'),
        'funcproc': _('Wordt gebruikt door'),
    }
    from_titles = {
        'entiteit': _('Betrokken'),
        'funcproc': _('Gebruikt'),
        'techproc': _('Gebruikt'),
        'testplan': _('Zie'),
    }
    project = models.ForeignKey(Project,related_name="fprocs")
    naam = models.CharField(max_length=40)
    doel = models.CharField(max_length=80)
    invoer = models.TextField()
    uitvoer = models.TextField()
    beschrijving = models.TextField()
    spec = models.ForeignKey(Userspec,related_name="fprocs",null=True)
    rfc = models.ManyToManyField(Userwijz,related_name="fprocs",null=True)
    gt = models.ManyToManyField(Gebrtaak,related_name="fprocs",null=True)
    bom = models.ManyToManyField('self',symmetrical=False,related_name="used_by",
        null=True)
    def __str__(self):
        return ": ".join((self.naam,self.doel))
    class Meta:
        verbose_name = _("functioneel proces")
        verbose_name_plural = _("functionele processen")

class Entiteit(models.Model):
    section = 'func'
    to_titles = {
        'userwijz': _('Is geraakt door'),
        'funcproc': _('Wordt gebruikt door'),
    }
    from_titles = {
        'dataitem': _('Wordt gerealiseerd door'),
        'testplan': _('Zie'),
    }
    project = models.ForeignKey(Project,related_name="fdata")
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    functie = models.TextField()
    levensloop = models.TextField()
    rfc = models.ManyToManyField(Userwijz,related_name="fdata",null=True)
    fp = models.ManyToManyField(Funcproc,related_name="fdata",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.kort))
    class Meta:
        verbose_name = _("entiteit")
        verbose_name_plural = _("entiteiten")

class Attribuut(models.Model):
    TYPE_CHOICES = (
        ('A', _('Tekst')),
        ('N', _('Numeriek (geheel getal)')),
        ('B', _('Bedrag (numeriek, cijfers achter de komma)')),
        ('D', _('Datum')),
    )
    hoort_bij = models.ForeignKey(Entiteit,related_name="attrs",
        ## edit_inline=models.TABULAR, num_in_admin=3,
    )
    naam = models.CharField(max_length=40) #,core=True)
    type = models.CharField(max_length=10,choices=TYPE_CHOICES)
    bereik = models.TextField()
    primarykey = models.PositiveSmallIntegerField()
    relatie = models.ForeignKey(Entiteit,related_name="relatie",null=True)
    def __str__(self):
        return self.naam
    class Meta:
        verbose_name = _("attribuut")
        verbose_name_plural = _("attributen")

class Techtask(models.Model):
    section = 'tech'
    to_titles = {
        'gebrtaak': _('Bedient'),
    }
    from_titles = {
        'techproc': _('Wordt bediend door'),
    }
    project = models.ForeignKey(Project,related_name="ttask")
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    doel = models.TextField()
    periode = models.TextField()
    verloop = models.TextField()
    gt = models.ForeignKey(Gebrtaak,related_name="ttask",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.kort))
    class Meta:
        verbose_name = _("systeemtaak")
        verbose_name_plural = _("systeemtaken")

class Techproc(models.Model):
    section = 'tech'
    to_titles = {
        'funcproc': _('Wordt gebruikt door'),
        'techtaak': _('Bedient'),
        'techproc': _('Wordt gebruikt door'),
    }
    from_titles = {
        'dataitem': _('Betrokken'),
        'techproc': _('Gebruikt'),
        'layout': _('Gebruikt'),
        'programma': _('Gebruikt'),
    }
    project = models.ForeignKey(Project,related_name="tproc")
    naam = models.CharField(max_length=40)
    doel = models.CharField(max_length=80)
    invoer = models.TextField()
    uitvoer = models.TextField()
    beschrijving = models.TextField()
    omgeving = models.TextField()
    fp = models.ManyToManyField(Funcproc,related_name="tproc",null=True)
    tt = models.ManyToManyField(Techtask,related_name="tproc",null=True)
    bom = models.ManyToManyField('self',symmetrical=False,related_name="used_by",
        null=True)
    def __str__(self):
        return ": ".join((self.naam,self.doel))
    class Meta:
        verbose_name = _("technisch proces")
        verbose_name_plural = _("technische processen")

class Dataitem(models.Model):
    section = 'tech'
    to_titles = {
        'entiteit': _('Is technische vertaling van'),
        'techproc': _('Wordt gebruikt door'),
    }
    from_titles = {}
    project = models.ForeignKey(Project,related_name="tdata")
    naam = models.CharField(max_length=40)
    functie = models.CharField(max_length=80)
    levensloop = models.TextField()
    ent = models.ManyToManyField(Entiteit,related_name="tdata",null=True)
    tp = models.ManyToManyField(Techproc,related_name="tdata",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.functie))
    class Meta:
        verbose_name = _("data-item")
        verbose_name_plural = _("data-items")

class Dataelement(models.Model):
    hoort_bij = models.ForeignKey(Dataitem,related_name="elems",
        ## edit_inline=models.TABULAR, num_in_admin=3,
    )
    naam = models.CharField(max_length=40) # ,core=True)
    omschrijving = models.CharField(max_length=80)
    soort = models.CharField(max_length=40)
    sleutel = models.PositiveSmallIntegerField(verbose_name="volgorde in sleutel")
    relatie = models.ForeignKey(Dataitem,related_name="relatie",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.omschrijving))
    class Meta:
        verbose_name = _("data-element")
        verbose_name_plural = _("data-elementen")

class Layout(models.Model):
    section = 'tech'
    to_titles = {
        'gebrtaak': 'Bedient',
        'techproc': 'Wordt gebruikt door',
    }
    from_titles = {
    }
    project = models.ForeignKey(Project,related_name="layout")
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    data = models.TextField()
    link = models.FileField(upload_to='layout')
    gt = models.ManyToManyField(Gebrtaak,related_name="layout",null=True)
    tp = models.ManyToManyField(Techproc,related_name="layout",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.kort))

class Procproc(models.Model):
    section = 'tech'
    to_titles = {
        'techproc': _('Wordt gebruikt door'),
    }
    from_titles = {}
    project = models.ForeignKey(Project,related_name="pproc")
    naam = models.CharField(max_length=40)
    doel = models.CharField(max_length=80)
    invoer = models.TextField()
    uitvoer = models.TextField()
    werkwijze = models.TextField()
    bijzonder = models.TextField()
    hoetetesten = models.TextField()
    testgevallen = models.TextField()
    tp = models.ManyToManyField(Techproc,related_name="pproc",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.doel))
    class Meta:
        verbose_name = _("programmabeschrijving")
        verbose_name_plural = _("programmabeschrijvingen")

class Testplan(models.Model):
    section = 'test'
    to_titles = {
        'gebrtaak': _('t.b.v.'),
        'funcproc': _('t.b.v.'),
        'entiteit': _('t.b.v.'),
    }
    from_titles = {
        'testcase': _('Betrokken'),
        'bevinding': _('Betrokken'),
    }
    project = models.ForeignKey(Project,related_name="tplan")
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    tekst = models.TextField()
    gt = models.ManyToManyField(Gebrtaak,related_name="tplan",null=True)
    fp = models.ManyToManyField(Funcproc,related_name="tplan",null=True)
    ent = models.ManyToManyField(Entiteit,related_name="tplan",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.oms))
    class Meta:
        verbose_name = _("testplan")
        verbose_name_plural = _("testplannen")

class Testcase(models.Model):
    section = 'test'
    to_titles = {
        'testplan': _('Hoort bij'),
    }
    from_titles = {}
    project = models.ForeignKey(Project,related_name="tcase")
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    tekst = models.TextField()
    tplan = models.ManyToManyField(Testplan,related_name="tcase",null=True)
    def __str__(self):
        return ": ".join((self.naam,self.oms))
    class Meta:
        verbose_name = _("testgeval")
        verbose_name_plural = _("testgevallen")

class Bevinding(models.Model):
    section = 'test'
    to_titles = {
        'testplan': _('Hoort bij'),
    }
    from_titles = {
    }
    project = models.ForeignKey(Project,related_name="tbev")
    nummer = models.CharField(max_length=10)
    datum_in = models.DateTimeField(auto_now_add=True)
    gereed = models.BooleanField()
    datum_gereed = models.DateTimeField(null=True)
    kort = models.CharField(max_length=80)
    melding = models.TextField()
    oplossing = models.TextField()
    actie = models.IntegerField(null=True)
    actienummer = models.CharField(max_length=10)
    tplan = models.ManyToManyField(Testplan,related_name="tbev",null=True)
    def __str__(self):
        oms = _(" [afgehandeld]") if self.gereed else ""
        return ": ".join((self.nummer,self.kort + oms))
    class Meta:
        verbose_name_plural = _("bevinding")
        verbose_name_plural = _("bevindingen")

rectypes = {
    'project':   Project,
    'userspec':  Userspec,
    'userdoc':   Userdoc,
    'userwijz':  Userwijz,
    'userprob':  Userprob,
    'funcdoc':   Funcdoc,
    'gebrtaak':  Gebrtaak,
    'funcproc':  Funcproc,
    'entiteit':  Entiteit,
    'attribuut': Attribuut,
    'techtaak':  Techtask,
    'techproc':  Techproc,
    'dataitem':  Dataitem,
    'element':   Dataelement,
    'layout':    Layout,
    'programma': Procproc,
    'testplan':  Testplan,
    'testcase':  Testcase,
    'bevinding': Bevinding,
    }
