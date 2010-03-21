from django.db import models

class Project(models.Model):
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    oms = models.TextField()
    start = models.CharField(max_length=80)
    fysloc = models.CharField(max_length=80)
    actiereg = models.CharField(max_length=40)
    aruser = models.CharField(max_length=40)
    status = models.TextField()
    def __unicode__(self):
        return ": ".join((self.naam,self.kort))
    class Meta:
        verbose_name = "project"
        verbose_name_plural = verbose_name + "en"
    ## class Admin:
        ## pass

class Userspec(models.Model):
    section = 'user'
    to_titles = {
    }
    from_titles = {
        'gebrtaak': 'Betrokken',
        'funcproc': 'Betrokken',
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
    def __unicode__(self):
        return ": ".join((self.naam,self.kort))
    class Meta:
        verbose_name = "gebruikersspecificatie"
    ## class Admin:
        ## pass

class Userdoc(models.Model):
    section = 'user'
    to_titles = {}
    from_titles = {}
    project = models.ForeignKey(Project,related_name="docs")
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    link = models.FileField(upload_to='doctool/userdoc')
    tekst = models.TextField()
    def __unicode__(self):
        return ": ".join((self.naam,self.oms))
    class Meta:
        verbose_name = "naslagdocument"
        verbose_name_plural = verbose_name + "en"
    ## class Admin:
        ## pass

class Userwijz(models.Model):
    section = 'user'
    to_titles = {
    }
    from_titles = {
        'gebrtaak': 'Raakt',
        'funcproc': 'Raakt',
        'entiteit': 'Raakt',
    }
    project = models.ForeignKey(Project,related_name="rfcs")
    nummer = models.CharField(max_length=10)
    datum_in = models.DateTimeField(auto_now_add=True)
    gereed = models.BooleanField()
    datum_gereed = models.DateTimeField(null=True)
    wens = models.CharField(max_length=80)
    toelichting = models.TextField()
    ## oplossing = models.TextField()
    ## ontwerp = models.TextField()
    ## realisatie = models.TextField()
    ## verslag = models.TextField()
    opmerkingen = models.TextField()
    actie = models.IntegerField(null=True)
    actienummer = models.CharField(max_length=10)
    def __unicode__(self):
        oms = " [afgesloten]" if self.gereed else ""
        return ": ".join((self.nummer,self.wens + oms))
    class Meta:
        verbose_name = "aanvraag wijziging"
        verbose_name_plural = verbose_name + "en"
    ## class Admin:
        ## pass

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
    ## analyse = models.TextField()
    oplossing = models.TextField()
    ## vervolg = models.TextField()
    actie = models.IntegerField(null=True)
    actienummer = models.CharField(max_length=10)
    def __unicode__(self):
        oms = " [afgesloten" if self.gereed else ""
        verv = " - vervolg]" if self.vervolg else "]" if self.gereed else ""
        return "{0}: {1} {2}{3}".format(self.nummer,self.kort,oms,verv)
    class Meta:
        verbose_name = "incident/probleem"
        verbose_name_plural = "en/".join(verbose_name.split("/"))[:-2] + "men"
    ## class Admin:
        ## pass

class Funcdoc(models.Model):
    section = 'func'
    to_titles = {}
    from_titles = {}
    project = models.ForeignKey(Project,related_name="fdocs")
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    link = models.FileField(upload_to='doctool/funcdoc')
    tekst = models.TextField()
    def __unicode__(self):
        return ": ".join((self.naam,self.oms))
    class Meta:
        verbose_name = "functioneel document"
        verbose_name_plural = "le".join((verbose_name[:9],verbose_name[11:])) + "en"
    ## class Admin:
        ## pass

class Gebrtaak(models.Model):
    section = 'func'
    to_titles = {
        'userspec': 'Hoort bij',
        'userwijz': 'Is geraakt door',
    }
    from_titles = {
        'funcproc': 'Wordt bediend door',
        'techtaak': 'Gerelateerde',
        'layout': 'Bijbehorende',
        'testplan': 'Zie',
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
    def __unicode__(self):
        return ": ".join((self.naam,self.doel))
    class Meta:
        verbose_name = "gebruikerstaak"
        verbose_name_plural = verbose_name[:-2] + "ken"
    ## class Admin:
        ## pass

class Funcproc(models.Model):
    section = 'func'
    to_titles = {
        'userspec': 'Hoort bij',
        'userwijz': 'Is geraakt door',
        'gebrtaak': 'Bedient',
        'funcproc': 'Wordt gebruikt door',
    }
    from_titles = {
        'entiteit': 'Betrokken',
        'funcproc': 'Gebruikt',
        'techproc': 'Gebruikt',
        'testplan': 'Zie',
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
    bom = models.ManyToManyField('self',symmetrical=False,related_name="used_by",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.doel))
    class Meta:
        verbose_name = "functioneel proces"
        verbose_name_plural = "le".join((verbose_name[:9],verbose_name[11:])) + "sen"
    ## class Admin:
        ## pass

class Entiteit(models.Model):
    section = 'func'
    to_titles = {
        'userwijz': 'Is geraakt door',
        'funcproc': 'Wordt gebruikt door',
    }
    from_titles = {
        'dataitem': 'Wordt gerealiseerd door',
        'testplan': 'Zie',
    }
    project = models.ForeignKey(Project,related_name="fdata")
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    functie = models.TextField()
    levensloop = models.TextField()
    rfc = models.ManyToManyField(Userwijz,related_name="fdata",null=True)
    fp = models.ManyToManyField(Funcproc,related_name="fdata",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.kort))
    class Meta:
        verbose_name_plural = "entiteiten"
    ## class Admin:
        ## pass

class Attribuut(models.Model):
    TYPE_CHOICES = (
        ('A','Tekst'),
        ('N','Numeriek (geheel getal)'),
        ('B','Bedrag (numeriek, cijfers achter de komma)'),
        ('D','Datum'),
    )
    hoort_bij = models.ForeignKey(Entiteit,related_name="attrs",
        ## edit_inline=models.TABULAR, num_in_admin=3,
    )
    naam = models.CharField(max_length=40) #,core=True)
    type = models.CharField(max_length=10,choices=TYPE_CHOICES)
    bereik = models.TextField()
    primarykey = models.PositiveSmallIntegerField()
    relatie = models.ForeignKey(Entiteit,related_name="relatie",null=True)
    def __unicode__(self):
        return self.naam
    class Meta:
        verbose_name_plural = "attributen"
    ## class Admin:
        ## pass

class Techtask(models.Model):
    section = 'tech'
    to_titles = {
        'gebrtaak': 'Bedient',
    }
    from_titles = {
        'techproc': 'Wordt bediend door',
    }
    project = models.ForeignKey(Project,related_name="ttask")
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    doel = models.TextField()
    periode = models.TextField()
    verloop = models.TextField()
    gt = models.ForeignKey(Gebrtaak,related_name="ttask",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.kort))
    class Meta:
        verbose_name = "systeemtaak"
        verbose_name_plural = verbose_name[:-2] + "ken"
    ## class Admin:
        ## pass

class Techproc(models.Model):
    section = 'tech'
    to_titles = {
        'funcproc': 'Wordt gebruikt door',
        'techtaak': 'Bedient',
        'techproc': 'Wordt gebruikt door',
    }
    from_titles = {
        'dataitem': 'Betrokken',
        'techproc': 'Gebruikt',
        'layout': 'Gebruikt',
        'programma': 'Gebruikt',
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
    bom = models.ManyToManyField('self',symmetrical=False,related_name="used_by",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.doel))
    class Meta:
        verbose_name = "technisch proces"
        verbose_name_plural = "e ".join(verbose_name.split()) + "sen"
    ## class Admin:
        ## pass

class Dataitem(models.Model):
    section = 'tech'
    to_titles = {
        'entiteit': 'Is technische vertaling van',
        'techproc': 'Wordt gebruikt door',
    }
    from_titles = {}
    project = models.ForeignKey(Project,related_name="tdata")
    naam = models.CharField(max_length=40)
    functie = models.CharField(max_length=80)
    levensloop = models.TextField()
    ent = models.ManyToManyField(Entiteit,related_name="tdata",null=True)
    tp = models.ManyToManyField(Techproc,related_name="tdata",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.functie))
    class Meta:
        verbose_name = "data-item"
    ## class Admin:
        ## pass

class Dataelement(models.Model):
    hoort_bij = models.ForeignKey(Dataitem,related_name="elems",
        ## edit_inline=models.TABULAR, num_in_admin=3,
    )
    naam = models.CharField(max_length=40) # ,core=True)
    omschrijving = models.CharField(max_length=80)
    soort = models.CharField(max_length=40)
    sleutel = models.PositiveSmallIntegerField(verbose_name="volgorde in sleutel")
    relatie = models.ForeignKey(Dataitem,related_name="relatie",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.omschrijving))
    class Meta:
        verbose_name = "data-element"
        verbose_name_plural = verbose_name + "en"
    ## class Admin:
        ## pass

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
    link = models.FileField(upload_to='doctool/layout')
    gt = models.ManyToManyField(Gebrtaak,related_name="layout",null=True)
    tp = models.ManyToManyField(Techproc,related_name="layout",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.kort))
    ## class Admin:
        ## pass

class Procproc(models.Model):
    section = 'tech'
    to_titles = {
        'techproc': 'Wordt gebruikt door',
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
    def __unicode__(self):
        return ": ".join((self.naam,self.doel))
    class Meta:
        verbose_name = "programmabeschrijving"
        verbose_name_plural = verbose_name + "en"
    ## class Admin:
        ## pass

class Testplan(models.Model):
    section = 'test'
    to_titles = {
        'gebrtaak': 't.b.v.',
        'funcproc': 't.b.v.',
        'entiteit': 't.b.v.',
    }
    from_titles = {
        'testcase': 'Betrokken',
        'bevinding': 'Betrokken',
    }
    project = models.ForeignKey(Project,related_name="tplan")
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    tekst = models.TextField()
    gt = models.ManyToManyField(Gebrtaak,related_name="tplan",null=True)
    fp = models.ManyToManyField(Funcproc,related_name="tplan",null=True)
    ent = models.ManyToManyField(Entiteit,related_name="tplan",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.oms))
    class Meta:
        verbose_name_plural = "testplannen"
    ## class Admin:
        ## pass

class Testcase(models.Model):
    section = 'test'
    to_titles = {
        'testplan': 'Hoort bij',
    }
    from_titles = {}
    project = models.ForeignKey(Project,related_name="tcase")
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    tekst = models.TextField()
    tplan = models.ManyToManyField(Testplan,related_name="tcase",null=True)
    def __unicode__(self):
        return ": ".join((self.naam,self.oms))
    class Meta:
        verbose_name = "testgeval"
        verbose_name_plural = verbose_name + "len"
    ## class Admin:
        ## pass

class Bevinding(models.Model):
    section = 'test'
    to_titles = {
        'testplan': 'Hoort bij',
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
    ## analyse = models.TextField()
    oplossing = models.TextField()
    ## vervolg = models.TextField()
    actie = models.IntegerField(null=True)
    actienummer = models.CharField(max_length=10)
    tplan = models.ManyToManyField(Testplan,related_name="tbev",null=True)
    def __unicode__(self):
        oms = " [afgehandeld]" if self.gereed else ""
        return ": ".join((self.nummer,self.kort + oms))
    class Meta:
        verbose_name_plural = "bevindingen"
    ## class Admin:
        ## pass

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
