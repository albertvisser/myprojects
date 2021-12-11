"""Processing for MyProjects Web Application
"""
import datetime
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, FieldError    # , DoesNotExist
from django.utils.translation import ugettext as _
import docs.models as my
from myprojects.settings import MEDIA_ROOT, SITES
RELTXT = '<br/><a href="/docs/{0}/{1}/{2}/">{3}</a>'
BTNTXT = '<a href="/docs/{0}/{1}/{2}/{3}/{4}/"><input type="button" value="{5}" /></a>'
ADD_TEXT, REMOVE_TEXT = _("leg relatie"), _("verwijder relatie")
# let op: obj.model._meta bestaat niet (meer), obj,_meta.model wel
# maar in get_related heb ik model._meta nou juist vervangen door _meta
# ook is daar rel.to._meta.model_name vervangen door related_model
# maar ook is dat vergelijken met _meta.model_name vervangen door vergelijken met_meta.model
# in dit geval vergelijken we met een naam dus moeten we _meta.model_name blijven gebruiken
# in deze vergelijking vervangen we dus alleen rel.to door related_model

def get_related(this_obj, other_obj, m2m=False):
    """geeft het resultaat van een reversed relatie terug

    eerst wordt in het gerelateerde model de related_name opgezocht
    dan wordt hiermee het betreffende attribuut van het huidige object bepaald
    """
    # is het niet raar dat je voor twee concrete objecten ophaalt naar welke van het ene type
    # verwezen wordt vanuit het andere type? Of is dat om de vorige/volgende te kunnen bepalen?
    # als ik kijk naar het gebruik in GetRelations dan is het tweede argument ook niet een object
    # maar een relatie (uit de fields verzameling)
    if m2m:
        fields = [x for x in other_obj._meta.many_to_many]
    else:
        fields = [x for x in other_obj._meta.get_fields() if x.name != 'project' and
                  x.get_internal_type() == 'ForeignKey']
    for fld in fields:
        if fld.related_model == this_obj._meta.model:
            related_name = fld.related_query_name()
            break
    else:
        return None  # not found
    try:
        return this_obj.__getattribute__(related_name).all()
    except UnboundLocalError:
        return None
    # zou je deze ook kunnen vervangen door een aanroep van get_relation en dan met de opgehaalde
    # naam de gerelateerde objecten ophalen en meteen de vorige en de volgende bepalen?
    # (heeft uiteraard konsekwenties voor de aanroepende code)
    # oorspronkelijk lijkt dat ook zo geweest te zijn, de functie heette toen get_relation en het
    # gedeelte dat nu nog zo heet was daarin hardgecodeerd
    # deze functie wordt alleen aangeroepen in een paar methoden van de hieronder opgenomen klasse
    # GetRelations, namelijk om de namen van relaties uit andere objecten naar het huidige te kunnen
    # bepalen.
    # Als je get_relation zoals die nu is gebruikt zou je dat onderscheid (van versus naar relaties)
    # met dezelfde functie kunnen afhandelen


def get_relation(srt, soort):
    """Geeft veldnaam en cardinaliteit terug voor een relatie van srt naar soort
    """
    result, multiple = None, None
    if srt != soort or soort in ('funcproc', 'techproc'):
        for relobj in my.rectypes[srt]._meta.get_fields():
            if relobj.related_model and corr_naam(relobj.related_model._meta.model_name) == soort:
                result = relobj.name
                multiple = False if relobj.get_internal_type() == 'ForeignKey' else True
                break
    return result, multiple


def set_relation(o, soort, r, srt):
    attr_name, multiple = get_relation(soort, srt)
    if multiple:
        o.__getattribute__(attr_name).add(r)
    else:
        o.__setattr__(attr_name, r)
    o.save()


def remove_relation(o, soort, r, srt):
    attr_name, multiple = get_relation(soort, srt)
    if multiple:
        o.__getattribute__(attr_name).remove(r)
    else:
        o.__setattr__(attr_name, None)
    o.save()


def corr_naam(name):
    """convert name used in program to model name and back

    Note: all names must be unique!
    """
    names = (("techtaak", 'techtask'), ("programma", 'procproc'))
    for name1, name2 in names:
        if name == name1:
            return name2
        if name == name2:
            return name1
    return name


def get_field_attr(name):
    """leidt veldnaam, type en lengte af uit de definities in models.py
    """
    # de variant met een repeating group (entiteit, dataitem) levert hier nog een probleem op.
    # is dat omdat er twee entiteiten in 1 scherm staan?
    fields = []
    opts = my.rectypes[name]._meta
    for x in opts.get_fields():  # fields:
        fldname = x.name
        fldtype = x.get_internal_type()
        if fldname == 'id' or fldtype in ('ForeignKey', 'ManyToManyField'):
        # if fldname == 'id' or any((x.many2one, x.many2many, x.one2many))
            continue
        try:
            length = x.max_length
        except AttributeError:
            length = -1
        fields.append((fldname, fldtype[:-5], length))
    return fields


def get_relation_fields(name):
    """deze functie is van de vorige afgesplitst (afwijkend pad als tweede argument alles = True)
    enig gemeenschappelijke is loopen over get_fields
    deze werd bovendien nergens gebruikt
    """
    fields = []
    opts = my.rectypes[name]._meta
    for rel in opts.get_fields():
        # print(rel, rel.one_to_many or rel.many_to_many)
            if rel.one_to_many or rel.many_to_many:
                try:
                    fields.append((rel.name, rel.get_internal_type(), rel.max_length))
                except AttributeError:
                    fields.append((rel.name, rel.get_internal_type(), -1))
    return fields


def get_new_numberkey_for_soort(owner_proj, soort):
    """generate new id for certain document types
    """
    if soort == 'userwijz':
        sel = owner_proj.rfcs
    elif soort == 'userprob':
        sel = owner_proj.probs
    elif soort == 'bevinding':
        sel = owner_proj.tbev
    else:
        return ''
    ny = str(datetime.date.today().year)
    h = ''
    try:
        last_id = sel.latest(field_name="datum_in").nummer
    except ObjectDoesNotExist:
        pass
    else:
        yr, nr = last_id.split('-')
        if yr == ny:
            h = '-'.join((yr, '%04i' % (int(nr) + 1)))
    if h == '':
        h = '-'.join((ny, '0001'))
    return h


def get_stats_texts(proj, action_type):
    """get certain texts for certain document types (also registered in actiereg)
    """
    first = _("(nog) geen")
    if action_type == 'userwijz':
        all_objects = my.Userwijz.objects.filter(project=proj)
        second = _('ingediend')
        hlp = _("gerealiseerd"), _('in behandeling via')
    elif action_type == 'probleem':
        all_objects = my.Userprob.objects.filter(project=proj)
        second = _("gemeld")
        hlp = _('opgelost'), _('doorgekoppeld naar')
    elif action_type == 'bevinding':
        all_objects = my.Bevinding.objects.filter(project=proj)
        second = _("opgevoerd")
        hlp = _('opgelost'), _('doorgekoppeld naar')
    else:
        return '', ''
    solved = all_objects.filter(gereed=True).count()
    working = all_objects.filter(gereed=False).filter(actie__isnull=False).count()
    if all_objects.count() != 0:
        first = all_objects.count()
        second = str(_("waarvan {} {} en {} {} Actiereg").format(solved, hlp[0], working, hlp[1]))
    return first, second


def get_names_for_type(typename):
    "get verbose names from model definition"
    return (my.rectypes[typename]._meta.verbose_name,
            my.rectypes[typename]._meta.verbose_name_plural,
            my.rectypes[typename].section)


def get_projectlist():
    "return list of all the projects"
    return my.Project.objects.all().order_by('naam')


def get_ordered_objectlist(proj, soort):
    "return ordered list of objects of the given type for the given project"
    # if soort in my.rectypes:  -- overbodige test volgens mij
    #     return None
    # if proj:
    lijst = my.rectypes[soort].objects.filter(project=proj)
    # else:
    #     lijst = my.rectypes[soort].objects.select_related()
    # ik denk dat het voorgaande nooit gewerkt heeft. Om te beginnen omdat het vanaf het begin af aan
    # select.related heeft gestaan en dat heeft noit bestaan, dus ik denk dat je hier nooit komt met een
    # leeg project (want dan ga je naar get_projectlist) - dus maar weghalen:w

    # if soort in ('userwijz', 'userprob', 'bevinding'):
    if 'naam' in [x[0] for x in get_field_attr(soort)]:
        return lijst.order_by('naam')
    return lijst.order_by('nummer')


def get_object(soort, id, new=False):
    "return specified document object"
    if soort not in my.rectypes:
        raise Http404('Onbekend type `{}`'.format(soort))
    if new:
        o = my.rectypes[soort]()
    else:
        try:
            o = my.rectypes[soort].objects.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404(str(id).join((soort + ' ', _(' bestaat niet'))))
    return o


def determine_adjacent(all_items, o):
    "return keys for previous and next object"
    prev = next = 0
    nog_een = False
    for x in all_items:
        if nog_een:
            next = x.id
            nog_een = False
            break
        if x == o:
            nog_een = True
        else:
            prev = x.id
    return prev, next


def get_list_title_attrs(proj, soort, srt, id, rel):
    "return title, name (single and plural) and section for object type"
    soortnm_ev, soortnm_mv, sect = get_names_for_type(soort)
    if srt:
        srtnm_ev, srtnm_mv = get_names_for_type(srt)[:2]
    if proj:
        pr = my.Project.objects.get(pk=proj)
        title = _(' bij project ').join((soortnm_mv.capitalize(), pr.naam))
    else:
        pr = None
        title = _('Lijst ') + str(soortnm_mv)
    if rel:
        document = my.rectypes[srt].objects.get(pk=id)
        if srt in ('userwijz', 'userprob', 'bevinding'):
            docid = document.nummer
        else:
            docid = document.naam
        itemoms = '{} "{}"'.format(srtnm_ev, docid)
        relstr = str(_('{} relateren aan {}'))
        if rel == 'from':
            title = relstr.format(itemoms, soortnm_ev)
        else:
            title = relstr.format(soortnm_ev, itemoms)
    if pr:  # is dit niet dubbel? Ja zeker
        title = "Project {0} - {1}".format(pr.naam, title)
    return title, soortnm_ev, soortnm_mv, sect


def init_infodict_for_detail(proj, soort, edit, meld):
    return {'start': '', 'soort': soort, 'prev': '', 'notnw': 'new', 'next': '', "sites": SITES,
            'proj': '' if proj == 'proj' else proj, 'sect': '', 'meld': meld,
            'projecten': get_projectlist(),
            # 'edit': 'view' if edit else '',
            # 'view': 'edit' if not edit else '',
            'mode': 'edit' if edit else 'view',
            'new': 'nieuw' if edit == 'new' else ''}


def get_update_url(proj, edit, soort='', id='', srt='', verw=''):
    "return url to view that does the actual update"
    if edit == 'new':  # form action for new document
        if soort:
            ref = '{}/{}/'.format(srt, verw) if srt else ''
            return "/{}/{}/mut/{}".format(proj, soort, ref)
        return "/proj/mut/"
    elif edit:             # form action for existing
        if soort:
            return "/{}/{}/{}/mut/".format(proj, soort, id)
        return "/{}/mut/".format(proj)
    return ''


def get_fieldlengths(soort):
    "return dictionary of maxlength per field"
    return {x: z for x, y, z in get_field_attr(soort)}


def get_margins_for_type(typename):
    "geeft voor een aantal soorten afwijkende marges terug"
    left_margin = {"project": 140,
                   "userspec": 230,
                   "funcdoc": 160,
                   "gebrtaak": 240,
                   "funcproc": 160,
                   "entiteit": 140,
                   "techtaak": 200,
                   "techproc": 140,
                   "testplan": 140,
                   "bevinding": 140} .get(typename, 120)
    leftw = "{0}px".format(left_margin)
    rightw = "{0}px".format(910 - left_margin)
    rightm = "{0}px".format(left_margin + 5)
    return leftw, rightw, rightm


def get_detail_title(soort, edit, obj):
    """geeft titel zonder "DocTool!" terug"""
    naam_ev = get_names_for_type(soort)[0]
    if edit == 'new':
        return _('Nieuw(e) ') + str(naam_ev)
    try:
        title = " ".join((naam_ev.capitalize(), obj.naam))
    except AttributeError:
        title = " ".join((naam_ev.capitalize(), obj.nummer))
    return title


def get_relation_buttons(proj, soort, id, button_lijst):
    "build buttons to create related documents"
    # in het document krijg ik per soort te relateren document eerst een "leg relatie" knop
    # daarna als er relaties zijn de verwijzingen met een knop "verwijder relatie"
    # en tenslotte dit setje knoppen, dat van mij ook wel bij de "leg relatie" knoppen mag
    buttons = []
    for s in button_lijst:
        buttons.append(BTNTXT.format(proj, s, "new", soort, id, _("Opvoeren ") +
                                     str(my.rectypes[s]._meta.verbose_name)))
    return buttons


def execute_update(soort, obj, postdict, files=None):
    if soort in ('userwijz', 'userprob', 'bevinding'):
        gereed = obj.gereed
    for x, y, z in get_field_attr(soort):  # naam,type,lengte
        if x == 'datum_gereed':
            if postdict['gereed'] == '1' and not gereed:
                obj.datum_gereed = datetime.datetime.today()
        elif x == "gereed":
            obj.gereed = True if postdict[x] == "1" else False
        elif x == 'link':
            if 'link_file' in files:
                uploaded = files['link_file']
                pad = [y.upload_to for y in my.rectypes[soort]._meta.fields if y.name == 'link'][0]
                save_name = "/".join((pad, uploaded.name))
                with open(MEDIA_ROOT + save_name, 'wb+') as destination:
                    for chunk in uploaded.chunks():
                        destination.write(chunk)
                obj.__dict__[x] = save_name
        elif x != 'datum_in':
            obj.__dict__[x] = postdict[x]
    obj.save()


def execute_update_for_link(soort, obj, postdict, files):
    model = models.get_model('myprojects', soort.capitalize())
    manipulator = my.rectypes[soort].AddManipulator()
    new_data = postdict.copy()
    new_data.update({'project': proj})
    for x,y,z in getfields(soort): # naam,type,lengte
        if x == 'link' and y == 'File':
            new_data.update(files)
            continue
    # return HttpResponse(str(new_data))
    errors = manipulator.get_validation_errors(new_data)
    manipulator.do_html2python(new_data)
    if errors:
        return 'errors', HttpResponse('\n'.join((str(errors),str(new_data))))
    new_object = manipulator.save(new_data)
    return 'ok', my.rectypes[soort].objects.get(pk=new_object.id)


def update_link_from_actiereg(obj, arid, arnum):
    obj.actie = int(arid)  # int(data.get("id","0"))
    obj.actienummer = arnum  # data.get("actie","")
    obj.save()


def update_status_from_actiereg(obj, arstat):
    obj.gereed = {"arch": True, "herl": False}[arstat]
    obj.save()


def update_subitem(srt1, obj1, srt2, obj2, new, data):
    if new:
        obj2.hoort_bij = obj1
    obj2.naam = data["naam"]
    if (srt1, srt2) == ('entiteit', 'attribuut'):
        obj2.type = data["type"]
        obj2.bereik = data["bereik"]
        obj2.primarykey = data["key"] if data["key"] in ('1', '2', '3', '4', '5') else '0'
    elif (srt1, srt2) == ('dataitem', 'element'):
        obj2.soort = data["type"]
        obj2.omschrijving = data["oms"]
        obj2.sleutel = data["sleutel"] if data["sleutel"] in ('1', '2', '3', '4', '5') else '0'
    if "rel" in data:
        if data["rel"] in [x.naam for x in my.Entiteit.objects.filter(project=obj1.project)]:
            # try:
            obj2.relatie = my.rectypes[srt1].objects.get(naam=data["rel"])
            # except ObjectDoesNotExist:
            # pass
    obj2.save()


def update_related(soort, obj, related, relobj):
    "bijwerken van de eventueel meegegeven relatie"
    if related not in my.rectypes:
        raise Http404('Onbekend type `{}` voor relatie'.format(related))
    data = my.rectypes[related].objects.get(pk=relobj)
    set_relation(obj, soort, data, related)


class GetRelations:
    "zoek relaties bij gegeven object"
    def __init__(self, obj, soort):  # , related_soort):
        self.obj = obj
        self.soort = soort
        # self.srt = related_soort
        self.opts = my.rectypes[soort]._meta
        # dit opnieuw opzetten met één lus over opts.get_fields(show_hidden=True)
        # in plaats van de vier lussen die ik nu heb
        # maar eerst nog even met 4 functies

    def get_foreignkeys_to(self):
        fkeys_to = []
        for fld in self.opts.fields:
            if fld.name == "project":
                continue
            if fld.get_internal_type() == 'ForeignKey':
                srt = corr_naam(fld.related_model._meta.model_name)
                result = self.obj.__getattribute__(fld.name)
                rel = {'text': ' '.join((str(my.rectypes[self.soort].to_titles[srt]),
                                         str(my.rectypes[srt]._meta.verbose_name))),
                       'links': []}
                if result:
                    rel['links'].append(RELTXT.format(self.obj.project.id, srt, result.id, result) +
                                        " " +
                                        BTNTXT.format(self.obj.project.id, self.soort, self.obj.id,
                                                      "unrel/van/" + srt, result.id, REMOVE_TEXT))
                else:
                    rel['btn'] = BTNTXT.format(self.obj.project.id, srt, "rel", self.soort,
                                               self.obj.id, ADD_TEXT)
                fkeys_to.append(rel)
        return fkeys_to

    def get_many2many_to(self):
        m2ms_to = []
        for x in self.opts.many_to_many:
            srt = corr_naam(x.related_model._meta.model_name)
            y = {'text': ' '.join((str(my.rectypes[self.soort].to_titles[srt]),
                                   str(my.rectypes[srt]._meta.verbose_name))),
                 'btn': BTNTXT.format(self.obj.project.id, srt, "rel", self.soort, self.obj.id,
                                      ADD_TEXT),
                 'links': []}
            result = self.obj.__getattribute__(x.name)
            for item in result.all():
                y['links'].append(RELTXT.format(self.obj.project.id, srt, item.id, item) + " " +
                                  BTNTXT.format(self.obj.project.id, self.soort, self.obj.id,
                                                "unrel/van/" + srt, item.id, REMOVE_TEXT))
            m2ms_to.append(y)
        return m2ms_to

    def get_foreignkeys_from(self):
        button_lijst, fkeys_from, andere, attrs = [], [], [], []
        # for relobj in opts.get_all_related_objects():
        for relobj in [x for x in self.opts.get_fields()
                       if (x.one_to_many or x.one_to_one) and x.auto_created and not x.concrete]:
            # print(self.obj, relobj, self.soort)
            srt = corr_naam(relobj.related_model._meta.model_name)
            if (self.soort, srt) == ('entiteit', 'attribuut'):
                andere = [x.naam for x in my.Entiteit.objects.filter(project=self.obj.project)
                          if x != self.obj]
                attrs = self.obj.attrs.all()
            elif (self.soort, srt) == ('dataitem', 'dataelement'):
                andere = [x.naam for x in my.Dataitem.objects.filter(project=self.obj.project)
                          if x != self.obj]
                attrs = self.obj.elems.all()
            else:
                button_lijst.append(srt)
                y = {'text': ' '.join((str(my.rectypes[self.soort].from_titles[srt]),
                                       str(my.rectypes[srt]._meta.verbose_name))),
                     'btn': BTNTXT.format(self.obj.project.id, self.soort, self.obj.id, "rel", srt,
                                          ADD_TEXT),
                     'links': []}
                #result = get_related(self.obj, relobj)
                result = self.obj.__getattribute__(relobj.related_name).all()
                if result:
                    for item in result.all():
                        y['links'].append(RELTXT.format(self.obj.project.id, srt, item.id, item) +
                                          " " +
                                          BTNTXT.format(self.obj.project.id, srt, item.id,
                                                        "unrel/naar/" + self.soort, self.obj.id,
                                                        REMOVE_TEXT))
                fkeys_from.append(y)
        return button_lijst, fkeys_from, andere, attrs

    def get_many2many_from(self):
        button_lijst, m2ms_from = [], []
        # for x in opts.get_all_related_many_to_many_objects():
        for x in [y for y in self.opts.get_fields()  # include_hidden=True)
                  if y.many_to_many and y.auto_created]:
            srt = corr_naam(x.related_model._meta.model_name)
            button_lijst.append(srt)
            y = {'text': ' '.join((str(my.rectypes[self.soort].from_titles[srt]),
                                   str(my.rectypes[srt]._meta.verbose_name))),
                 'btn': BTNTXT.format(self.obj.project.id, self.soort, self.obj.id, "rel", srt,
                                      ADD_TEXT),
                 'links': []}
            # result = get_related(self.obj, x, m2m=True)
            result = self.obj.__getattribute__(x.related_name).all()
            if result:
                for item in result.all():
                    y['links'].append(RELTXT.format(self.obj.project.id, srt, item.id, item) + " " +
                                      BTNTXT.format(self.obj.project.id, srt, item.id,
                                                    "unrel/naar/" + self.soort, self.obj.id,
                                                    REMOVE_TEXT))
            m2ms_from.append(y)
        return button_lijst, m2ms_from
