"""Data definitions for MyProjects application
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
import django.utils.timezone


class Project(models.Model):
    """Software project
    """
    section = ''
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    oms = models.TextField()
    start = models.CharField(max_length=80)
    fysloc = models.CharField(max_length=80)
    actiereg = models.CharField(max_length=40)
    aruser = models.CharField(max_length=40)
    status = models.TextField()

    def __str__(self):
        return f"{self.naam}: {self.kort}"

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projecten")


class Userspec(models.Model):
    """User wish / requirement
    """
    section = 'user'
    to_titles = {}
    from_titles = {'gebrtaak': _('Betrokken'),
                   'funcproc': _('Betrokken')}
    project = models.ForeignKey(Project, related_name="specs", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    functie = models.TextField()
    beeld = models.TextField()
    product = models.TextField()
    baten = models.CharField(max_length=80)
    kosten = models.CharField(max_length=80)
    opmerkingen = models.TextField()

    def __str__(self):
        return f"{self.naam}: {self.kort}"

    class Meta:
        verbose_name = _("gebruikersspecificatie")
        verbose_name_plural = _("gebruikersspecificaties")


class Userdoc(models.Model):
    """Any other document pertaining to the user side of things
    """
    section = 'user'
    to_titles = {}
    from_titles = {}
    project = models.ForeignKey(Project, related_name="docs", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    link = models.FileField(upload_to='userdocs')
    tekst = models.TextField()

    def __str__(self):
        return f"{self.naam}: {self.oms}"

    class Meta:
        verbose_name = _("naslagdocument")
        verbose_name_plural = _("naslagdocumenten")


class Userwijz(models.Model):
    """Request for change
    """
    section = 'user'
    to_titles = {}
    from_titles = {'gebrtaak': _('Raakt'), 'gebrtaak_rfc': _('Raakt'),
                   'funcproc': _('Raakt'),
                   'entiteit': _('Raakt')}
    project = models.ForeignKey(Project, related_name="rfcs", on_delete=models.CASCADE)
    nummer = models.CharField(max_length=10)
    datum_in = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    gereed = models.BooleanField()
    datum_gereed = models.DateTimeField(null=True)
    wens = models.CharField(max_length=80)
    toelichting = models.TextField()
    opmerkingen = models.TextField()
    actie = models.IntegerField(null=True)
    actienummer = models.CharField(max_length=10)

    def __str__(self):
        oms = _(" [afgesloten]") if self.gereed else ""
        return f"{self.nummer}: {self.wens} {oms}"

    class Meta:
        verbose_name = _("aanvraag wijziging")
        verbose_name_plural = _("aanvraag wijzigingen")


class Userprob(models.Model):
    """Incident / defect found in production environment
    """
    section = 'user'
    to_titles = {}
    from_titles = {}
    project = models.ForeignKey(Project, related_name="probs", on_delete=models.CASCADE)
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
        return f"{self.nummer}: {self.kort} {oms}"

    class Meta:
        verbose_name = _("incident/probleem")
        verbose_name_plural = _("incidenten/problemen")


class Funcdoc(models.Model):
    """Any other document pertaining to the design side of things
    """
    section = 'func'
    to_titles = {}
    from_titles = {}
    project = models.ForeignKey(Project, related_name="fdocs", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    link = models.FileField(upload_to='funcdocs')
    tekst = models.TextField()

    def __str__(self):
        return f"{self.naam}: {self.oms}"

    class Meta:
        verbose_name = _("functioneel document")
        verbose_name_plural = _("functionele documenten")


class Gebrtaak(models.Model):
    """Functional description / design of a user action in the system
    """
    section = 'func'
    to_titles = {'userspec': _('Hoort bij'),
                 'userwijz': _('Is geraakt door')}
    from_titles = {'funcproc': _('Wordt bediend door'),
                   'techtaak': _('Gerelateerde'),
                   'layout': _('Bijbehorende'),
                   'testplan': _('Zie'),
                   'gebrtaak_rfc': _('Gerelateerde')}
    project = models.ForeignKey(Project, related_name="gtaken", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    doel = models.CharField(max_length=80)
    wanneer = models.TextField()
    wie = models.TextField()
    condities = models.TextField()
    waarvoor = models.TextField()
    beschrijving = models.TextField()
    spec = models.ForeignKey(Userspec, related_name="gtaken", null=True, on_delete=models.CASCADE)
    rfc = models.ManyToManyField(Userwijz, related_name="gtaken")

    def __str__(self):
        return f"{self.naam}: {self.doel}"

    class Meta:
        verbose_name = _("gebruikerstaak")
        verbose_name_plural = _("gebruikerstaken")


class Funcproc(models.Model):
    """Functional description / design of a process in the system
    """
    section = 'func'
    to_titles = {'userspec': _('Hoort bij'),
                 'userwijz': _('Is geraakt door'),
                 'gebrtaak': _('Bedient'),
                 'funcproc': _('Wordt gebruikt door')}
    from_titles = {'entiteit': _('Betrokken'),
                   'funcproc': _('Gebruikt'),
                   'techproc': _('Gebruikt'),
                   'testplan': _('Zie')}
    project = models.ForeignKey(Project, related_name="fprocs", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    doel = models.CharField(max_length=80)
    invoer = models.TextField()
    uitvoer = models.TextField()
    beschrijving = models.TextField()
    spec = models.ForeignKey(Userspec, related_name="fprocs", on_delete=models.CASCADE)
    rfc = models.ManyToManyField(Userwijz, related_name="fprocs")
    gt = models.ManyToManyField(Gebrtaak, related_name="fprocs")
    bom = models.ManyToManyField('self', symmetrical=False, related_name="used_by")

    def __str__(self):
        return f"{self.naam}: {self.doel}"

    class Meta:
        verbose_name = _("functioneel proces")
        verbose_name_plural = _("functionele processen")


class Entiteit(models.Model):
    """Logical unit of data as part of data model
    """
    section = 'func'
    to_titles = {'userwijz': _('Is geraakt door'),
                 'funcproc': _('Wordt gebruikt door')}
    from_titles = {'dataitem': _('Wordt gerealiseerd door'),
                   'testplan': _('Zie')}
    project = models.ForeignKey(Project, related_name="fdata", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    functie = models.TextField()
    levensloop = models.TextField()
    rfc = models.ManyToManyField(Userwijz, related_name="fdata")
    fp = models.ManyToManyField(Funcproc, related_name="fdata")

    def __str__(self):
        return f"{self.naam}: {self.kort}"

    class Meta:
        verbose_name = _("entiteit")
        verbose_name_plural = _("entiteiten")


class Attribuut(models.Model):
    """Data element
    """
    section = 'func'  # stond er eerder niet, krijg ik hopenlijk geen problmen mee
    type_choices = (('A', _('Tekst')),
                    ('N', _('Numeriek (geheel getal)')),
                    ('B', _('Bedrag (numeriek, cijfers achter de komma)')),
                    ('D', _('Datum')))
    hoort_bij = models.ForeignKey(Entiteit, related_name="attrs", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)  # ,core=True)
    type = models.CharField(max_length=10, choices=type_choices)
    bereik = models.TextField()
    primarykey = models.PositiveSmallIntegerField()
    relatie = models.ForeignKey(Entiteit, related_name="relatie", null=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name = _("attribuut")
        verbose_name_plural = _("attributen")


class Techtask(models.Model):
    """Functional description / design of a user action in the system
    """
    section = 'tech'
    to_titles = {'gebrtaak': _('Bedient')}
    from_titles = {'techproc': _('Wordt bediend door')}
    project = models.ForeignKey(Project, related_name="ttask", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    doel = models.TextField()
    periode = models.TextField()
    verloop = models.TextField()
    gt = models.ForeignKey(Gebrtaak, related_name="ttask", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.naam}: {self.kort}"

    class Meta:
        verbose_name = _("systeemtaak")
        verbose_name_plural = _("systeemtaken")


class Techproc(models.Model):
    """Functional description / design of a process in the system
    """
    section = 'tech'
    to_titles = {'funcproc': _('Wordt gebruikt door'),
                 'techtaak': _('Bedient'),
                 'techproc': _('Wordt gebruikt door')}
    from_titles = {'dataitem': _('Betrokken'),
                   'techproc': _('Gebruikt'),
                   'layout': _('Gebruikt'),
                   'programma': _('Gebruikt')}
    project = models.ForeignKey(Project, related_name="tproc", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    doel = models.CharField(max_length=80)
    invoer = models.TextField()
    uitvoer = models.TextField()
    beschrijving = models.TextField()
    omgeving = models.TextField()
    fp = models.ManyToManyField(Funcproc, related_name="tproc")
    tt = models.ManyToManyField(Techtask, related_name="tproc")
    bom = models.ManyToManyField('self', symmetrical=False, related_name="used_by")

    def __str__(self):
        return f"{self.naam}: {self.doel}"

    class Meta:
        verbose_name = _("technisch proces")
        verbose_name_plural = _("technische processen")


class Dataitem(models.Model):
    """Technical data model - unit of data
    """
    section = 'tech'
    to_titles = {'entiteit': _('Is technische vertaling van'),
                 'techproc': _('Wordt gebruikt door')}
    from_titles = {}
    project = models.ForeignKey(Project, related_name="tdata", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    functie = models.CharField(max_length=80)
    levensloop = models.TextField()
    ent = models.ManyToManyField(Entiteit, related_name="tdata")
    tp = models.ManyToManyField(Techproc, related_name="tdata")

    def __str__(self):
        return f"{self.naam}: {self.functie}"

    class Meta:
        verbose_name = _("data-item")
        verbose_name_plural = _("data-items")


class Dataelement(models.Model):
    """element belonging to technical unit of data
    """
    section = 'tech'  # stond er eerder niet, krijg ik hopenlijk geen problmen mee
    hoort_bij = models.ForeignKey(Dataitem, related_name="elems", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)  # ,core=True)
    omschrijving = models.CharField(max_length=80)
    soort = models.CharField(max_length=40)
    sleutel = models.PositiveSmallIntegerField(verbose_name="volgorde in sleutel")
    relatie = models.ForeignKey(Dataitem, related_name="relatie", null=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.naam}: {self.omschrijving}"

    class Meta:
        verbose_name = _("data-element")
        verbose_name_plural = _("data-elementen")


class Layout(models.Model):
    """Presentation design for screen or document output
    """
    section = 'tech'
    to_titles = {'gebrtaak': 'Bedient',
                 'techproc': 'Wordt gebruikt door'}
    from_titles = {}
    project = models.ForeignKey(Project, related_name="layout", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    kort = models.CharField(max_length=80)
    data = models.TextField()
    link = models.FileField(upload_to='layouts')
    gt = models.ManyToManyField(Gebrtaak, related_name="layout")
    tp = models.ManyToManyField(Techproc, related_name="layout")

    def __str__(self):
        return f"{self.naam}: {self.kort}"


class Procproc(models.Model):
    """Definition of procedure / program realizing (part of) a process in the system"""
    section = 'tech'
    to_titles = {'techproc': _('Wordt gebruikt door')}
    from_titles = {}
    project = models.ForeignKey(Project, related_name="pproc", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    doel = models.CharField(max_length=80)
    invoer = models.TextField()
    uitvoer = models.TextField()
    werkwijze = models.TextField()
    bijzonder = models.TextField()
    hoetetesten = models.TextField()
    testgevallen = models.TextField()
    tp = models.ManyToManyField(Techproc, related_name="pproc")

    def __str__(self):
        return f"{self.naam}: {self.doel}"

    class Meta:
        verbose_name = _("programmabeschrijving")
        verbose_name_plural = _("programmabeschrijvingen")


class Testplan(models.Model):
    """Plan for testing functionality of the system (how)
    """
    section = 'test'
    to_titles = {'gebrtaak': _('t.b.v.'),
                 'funcproc': _('t.b.v.'),
                 'entiteit': _('t.b.v.')}
    from_titles = {'testcase': _('Betrokken'),
                   'bevinding': _('Betrokken')}
    project = models.ForeignKey(Project, related_name="tplan", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    tekst = models.TextField()
    gt = models.ManyToManyField(Gebrtaak, related_name="tplan")
    fp = models.ManyToManyField(Funcproc, related_name="tplan")
    ent = models.ManyToManyField(Entiteit, related_name="tplan")

    def __str__(self):
        return f"{self.naam}: {self.oms}"

    class Meta:
        verbose_name = _("testplan")
        verbose_name_plural = _("testplannen")


class Testcase(models.Model):
    """Description of test data (why and what)
    """
    section = 'test'
    to_titles = {'testplan': _('Hoort bij')}
    from_titles = {}
    project = models.ForeignKey(Project, related_name="tcase", on_delete=models.CASCADE)
    naam = models.CharField(max_length=40)
    oms = models.CharField(max_length=80)
    tekst = models.TextField()
    tplan = models.ManyToManyField(Testplan, related_name="tcase")

    def __str__(self):
        return f"{self.naam}: {self.oms}"

    class Meta:
        verbose_name = _("testgeval")
        verbose_name_plural = _("testgevallen")


class Bevinding(models.Model):
    """Issues arising from testing
    """
    section = 'test'
    to_titles = {'testplan': _('Hoort bij')}
    from_titles = {}
    project = models.ForeignKey(Project, related_name="tbev", on_delete=models.CASCADE)
    nummer = models.CharField(max_length=10)
    datum_in = models.DateTimeField(auto_now_add=True)
    gereed = models.BooleanField()
    datum_gereed = models.DateTimeField(null=True)
    kort = models.CharField(max_length=80)
    melding = models.TextField()
    oplossing = models.TextField()
    actie = models.IntegerField(null=True)
    actienummer = models.CharField(max_length=10)
    tplan = models.ManyToManyField(Testplan, related_name="tbev")

    def __str__(self):
        oms = _(" [afgehandeld]") if self.gereed else ""
        return f"{self.nummer}: {self.kort} {oms}"

    class Meta:
        verbose_name = _("bevinding")
        verbose_name_plural = _("bevindingen")


rectypes = {'project': Project,
            'userspec': Userspec,
            'userdoc': Userdoc,
            'userwijz': Userwijz,
            'userprob': Userprob,
            'funcdoc': Funcdoc,
            'gebrtaak': Gebrtaak,
            'funcproc': Funcproc,
            'entiteit': Entiteit,
            'attribuut': Attribuut,
            'techtaak': Techtask,
            'techproc': Techproc,
            'dataitem': Dataitem,
            'element': Dataelement,
            'layout': Layout,
            'programma': Procproc,
            'testplan': Testplan,
            'testcase': Testcase,
            'bevinding': Bevinding}
