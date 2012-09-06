import os
import datetime
import inspect
## from django.template import Context, loader
## from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
## from django.core.exceptions import MultiValueDictKeyError, ObjectDoesNotExist #, DoesNotExist
from django.core.exceptions import ObjectDoesNotExist #, DoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.template import RequestContext
from django.db import models
import doctool.models as my
from doctool.settings import MEDIA_ROOT, SITES
leftw_dict = {
    "project": 140,
    "userspec": 230,
    "funcdoc": 160,
    "gebrtaak": 240,
    "funcproc": 160,
    "entiteit": 140,
    "techtaak": 200,
    "techproc": 140,
    "testplan": 140,
    "bevinding": 140,
    }
RELTXT = '<br/><a href="/{0}/{1}/{2}/">{3}</a>'
BTNTXT = '<a href="/{0}/{1}/{2}/{3}/{4}/"><input type="button" value="{5}" /></a>'

def get_relation(obj, srt_van, srt_naar, richting=''):
    """geeft met behulp van de dictionary relations de query voor een relatie terug

    relations[(srt_van,srt_naar)] geeft een tuple terug van veldnaam en een
    meer-dan-een-mogelijk indicatie
    de indicatie meer-dan-1-mogelijk wordt mee teruggegeven

    richting is van belang bij een bom-structuur"""
    ## print obj
    relations = {
        ('userspec', 'gebrtaak'): ("gtaken", True),
        ('userspec', 'funcproc'): ("fprocs", True),
        ('userwijz', 'gebrtaak'): ("gtaken", True),
        ('userwijz', 'funcproc'): ("fprocs", True),
        ('userwijz', 'entiteit'): ("fdata", True),
        # ('userprob',  'gebrtaak'):  ("gtaken", True),
        # ('userprob',  'funcproc'):  ("fprocs", True),
        # ('userprob',  'entiteit'):  ("fdata", True),
        ('gebrtaak', 'userspec'): ("spec", False),
        ('gebrtaak', 'userwijz'): ("rfc", True),
        ('gebrtaak', 'funcproc'): ("fprocs", True),
        ('gebrtaak', 'techtaak'): ("ttask", True),
        ('gebrtaak', 'layout'): ("layout", True),
        ('gebrtaak', 'testplan'): ("tplan", True),
        ('funcproc', 'userspec'): ("spec", False),
        ('funcproc', 'userwijz'): ("rfc", True),
        ('funcproc', 'gebrtaak'): ("gt", True),
        ('funcproc', 'funcproc_2'): ("used_by", True),
        ('funcproc', 'entiteit'): ("fdata", True),
        ('funcproc', 'funcproc'): ("bom", True),
        ('funcproc', 'techproc'): ("tproc", True),
        ('funcproc', 'testplan'): ("tplan", True),
        ('entiteit', 'userwijz'): ("rfc", True),
        ('entiteit', 'funcproc'): ("fp", True),
        ('entiteit', 'dataitem'): ("tdata", True),
        ('entiteit', 'testplan'): ("tplan", True),
        ('techtaak', 'gebrtaak'): ("gt", False),
        ('techtaak', 'techproc'): ("tproc", True),
        ('techproc', 'funcproc'): ("fp", True),
        ('techproc', 'techtaak'): ("tt", True),
        ('techproc', 'techproc_2'): ("used_by", True),
        ('techproc', 'dataitem'): ("tdata", True),
        ('techproc', 'techproc'): ("bom", True),
        ('techproc', 'layout'): ("layout", True),
        ('techproc', 'programma'): ("pproc", True),
        ('dataitem', 'entiteit'): ("ent", True),
        ('dataitem', 'techproc'): ("tp", True),
        ('layout', 'gebrtaak'): ("gt", True),
        ('layout', 'techproc'): ("tp", True),
        ('programma', 'techproc'): ("tp", True),
        ('testplan', 'gebrtaak'): ("gt", True),
        ('testplan', 'funcproc'): ("fp", True),
        ('testplan', 'entiteit'): ("ent", True),
        ('testplan', 'testcase'): ("tcase", True),
        ('testplan', 'bevinding'): ("tbev", True),
        ('testcase', 'testplan'): ("tplan", True),
        ('bevinding', 'testplan'): ("tplan", True),
    }
    rel, morethan1 = relations[(srt_van, srt_naar)]
    ## print rel
    ## print morethan1
    if srt_van == srt_naar and richting == 'from':
        rel = 'used_by'
    if morethan1:
        q = obj.__getattribute__(rel) # .all()
    else:
        q = obj.__getattribute__(rel)
    return (q, morethan1)

def corr_naam(name):
    if name == "techtaak":
        name = 'techtask'
    elif name == "programma":
        name = 'procproc'
    elif name == "techtask":
        name = 'techtaak'
    elif name == "procproc":
        name = 'programma'
    return name

def naam_dict(name):
    opts = my.rectypes[name]._meta
    try:
        sect = my.rectypes[name].section
    except AttributeError:
        sect = ''
    return opts.verbose_name,opts.verbose_name_plural,sect

def getfields(name,alles=False):
    """leidt veldnaam, type en lengte af uit de definities in models.py
    de variant met een repeating group (entiteit, dataitem) levert hier
    nog een probleem op."""
    fields = []
    opts = my.rectypes[name]._meta
    if alles:
        for x in opts.fields + opts.many_to_many:
            fields.append((x.name,x.get_internal_type(),x.maxlength))
    else:
        for x in opts.fields:
            f = x.name
            h = x.get_internal_type()
            l = -1 if x.max_length is None else x.max_length
            if f != 'id' and h != 'ForeignKey':
                fields.append((f,h[:-5],l))
    return fields

def get_new_id(sel):
    ny = str(datetime.date.today().year)
    h = ''
    try:
        last_id = sel.latest(field_name="datum_in").nummer
    except ObjectDoesNotExist:
        pass
    else:
        yr,nr = last_id.split('-')
        if yr == ny:
            h = '-'.join((yr,'%04i' % (int(nr) + 1)))
    if h == '':
        h = '-'.join((ny,'0001'))
    return h


def index(request):
    meld = ''
    ## return HttpResponse(os.path.splitext(my.__file__)[0] + '.py')
    ## raise ValueError('Testing...')
    return render_to_response('start.html',{
        'title': 'Welcome to DocTool!',
        'meld': meld,
        'start': True,
        'projecten': my.Project.objects.all().order_by('naam'),
        'footer': ''
        }, context_instance=RequestContext(request))

def lijst(request, proj='', soort='', id='',  edit='', srt=''):
    # proj = projectnummer, soort = onderdeelnaam
    ## raise ValueError('Testing...')
    entries = []
    naam_ev, naam_mv, sect = naam_dict(soort)
    info_dict = {
        'soort': soort,
        'srt': srt,
        'id': id,
        'proj': proj,
        'lijstitem': naam_ev,
        'lijstvan': naam_mv,
        'projecten': my.Project.objects.all().order_by('naam'),
        }
    meld = ''
    if soort in my.rectypes:
        if proj:
            lijst = my.rectypes[soort].objects.filter(project=proj)
        else:
            lijst = my.rectypes[soort].objects.select.related()
        if soort in ('userwijz','userprob','bevinding'):
            lijst = lijst.order_by('nummer')
        else:
            lijst = lijst.order_by('naam')
        info_dict['lijst'] = lijst
    soortnm_ev,soortnm_mv, sect = naam_dict(soort)
    if srt:
        srtnm_ev,srtnm_mv, sect = naam_dict(srt)
    if proj:
        pr = my.Project.objects.get(pk=proj)
        title = ' bij project '.join((soortnm_mv.capitalize(), pr.naam))
    else:
        title = 'Lijst ' + soortnm_mv
    if edit == 'rel':
        title = '{} relateren aan {} "{}"'.format(soortnm_ev, srtnm_ev,
            my.rectypes[srt].objects.get(pk=id).naam)
        info_dict['start'] = 'x' # forceert afwezigheid menu
        info_dict['ref'] = (srt,srtnm_mv,id)
        info_dict["soort"] = soort # '/'.join((srt,id,soort))
    info_dict['title'] = 'Doctool! ' + title
    if lijst.count() == 0:
        meld = soortnm_mv.join(("Geen "," aanwezig"))
        if proj:
            meld += " bij dit project"
    info_dict['meld'] = meld
    ## if soort:
        ## info_dict['notnw'] = '%s/new' % soort
    ## else:
        ## info_dict['notnw'] = 'new'
    info_dict["sctn"] = sect
    info_dict['notnw'] = 'new'
    doc = 'relateren.html' if edit == 'rel' else 'lijst.html'
    return render_to_response(doc, info_dict, context_instance=RequestContext(request))

def detail(request, proj='', edit='', soort='', id='', srt='', verw='', meld=''):
    # proj = projectnummer, soort = onderdeelnaam, edit = 'edit' of 'new', id = item nummer of niks bij nieuw
    "toon/wijzig document"
    ## raise ValueError('Testing...')
    ## meld = ''
    try: # do we have form data?
        data = request.POST
    except: # AttributeError?
        data = {}
    ## try: # do we have other form data?
        ## meld = request.GET.get('msg',"")
    ## except: # KeyError?
        ## pass
    ## return HttpResponse('melding: ' + meld)
    ## return HttpResponse("soort = %s, id = %s, proj = %s, edit = %s" % (soort, id,proj,edit))
    info_dict = {'title': '', 'start': '', 'prev': '', 'notnw': '', 'view': '',
        'next': '', 'proj': proj, 'sect': '', 'meld': meld,
        'projecten': my.Project.objects.all().order_by('naam'),
        }
    if edit:      # form/table styles/elements for editing  (incl. update button url)
        if edit == 'new': # form action for new document
            if soort:
                ref = ''
                if srt:
                    ref = '%s/%s/' % (srt,verw)
                info_dict['form_addr'] = "/%s/%s/mut/%s" % (proj,soort,ref)
            else:
                info_dict['form_addr'] = "/proj/mut/"
        else:             # form action for existing
            if soort:
                info_dict['form_addr'] = "/%s/%s/%s/mut/" % (proj,soort,id)
            else:
                info_dict['form_addr'] = "/%s/mut/" % proj
    lengte = {}
    prev = 0
    next = 0
    if not soort: # project: read object, selector, menu
        if proj and proj != 'proj':  # existing project
            try:  # get project
                o = my.Project.objects.get(pk=proj)
            except ObjectDoesNotExist:
                meld = proj.join(('project ',' bestaat niet'))
                proj = ''
        if edit == 'new':
            info_dict['title'] = 'Doctool! | Nieuw project '
        else:
            info_dict['title'] = 'Doctool! | Project ' + o.naam
            info_dict['data'] = o
        info_dict["start"] = ''
        soort = 'project'
    else:         # other: read object(s), selector, menu
        owner_proj = my.Project.objects.get(pk=proj)
        if id:    # existing item
            button_lijst = []
            relaties = []
            if soort in my.rectypes:
                o = my.rectypes[soort].objects.get(pk=id)
                all_items = my.rectypes[soort].objects.filter(project=proj)
                if soort in ('userwijz','userprob','bevinding'):
                    all_items = all_items.order_by('nummer')
                else:
                    all_items = all_items.order_by('naam')
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
                opts = my.rectypes[soort]._meta
                fkeys_to = []
                for fld in opts.fields:
                    if fld.get_internal_type() == 'ForeignKey' \
                            and fld.name != "project":
                        srt = corr_naam(fld.rel.to._meta.module_name)
                        rel = {
                            'text': ' '.join((my.rectypes[soort].to_titles[srt],
                                my.rectypes[srt]._meta.verbose_name)),
                            'btn': '',
                            ## 'btn': BTNTXT.format(proj, srt, id, "rel", soort,
                                ## "leg relatie"),
                            'links': []
                            }
                        result, morethan1 = get_relation(o, soort,  srt)
                        if result:
                            rel['links'].append(RELTXT.format(proj, srt, result.id,
                                result))
                            fkeys_to.append(rel)
                info_dict['fkeys_to'] = fkeys_to
                m2ms_to = []
                for x in opts.many_to_many:
                    srt = corr_naam(x.rel.to._meta.module_name)
                    y = {
                        'text': ' '.join((my.rectypes[soort].to_titles[srt],
                            my.rectypes[srt]._meta.verbose_name)),
                        'btn': '',
                        ## 'btn': BTNTXT.format(proj, srt, id, "rel", soort,
                            ## "leg relatie"),
                        'links': []
                        }
                    result, morethan1 = get_relation(o, soort, srt, 'to')
                    for item in result.all():
                        y['links'].append(RELTXT.format(proj, srt, item.id, item))
                    m2ms_to.append(y)
                info_dict['m2ms_to'] = m2ms_to
                button_lijst = [] # of button_lijst = my.rectypes[soort].from_titles.keys()
                fkeys_from = []
                for x in opts.get_all_related_objects():
                    srt = corr_naam(x.model._meta.module_name)
                    if (soort,srt) == ('entiteit','attribuut'):
                        info_dict["andere"] = [x.naam for x in
                            my.Entiteit.objects.filter(project=o.project) if x != o]
                        info_dict["attrs"] = o.attrs.all()
                    elif (soort,srt) == ('dataitem','dataelement'):
                        info_dict["andere"] = [x.naam for x in
                            my.Dataitem.objects.filter(project=o.project) if x != o]
                        info_dict["attrs"] = o.elems.all()
                    else:
                        button_lijst.append(srt)
                        y = {
                            'text': ' '.join((my.rectypes[soort].from_titles[srt],
                                my.rectypes[srt]._meta.verbose_name)),
                            ## 'btn': '',
                            'btn': BTNTXT.format(proj, soort, id, "rel", srt,
                                "leg relatie"),
                            'links': []
                            }
                        result, morethan1 = get_relation(o, soort, srt)
                        for item in result.all():
                            y['links'].append(RELTXT.format(proj, srt, item.id, item))
                        fkeys_from.append(y)
                info_dict['fkeys_from'] = fkeys_from
                m2ms_from = []
                for x in opts.get_all_related_many_to_many_objects():
                    srt = corr_naam(x.model._meta.module_name)
                    button_lijst.append(srt)
                    y = {
                        'text': ' '.join((my.rectypes[soort].from_titles[srt],
                            my.rectypes[srt]._meta.verbose_name)),
                        ## 'btn': '',
                        'btn': BTNTXT.format(proj, soort, id, "rel", srt,
                            "leg relatie"),
                        'links': []
                        }
                    result, morethan1 = get_relation(o, soort, srt, 'from')
                    for item in result.all():
                        y['links'].append(RELTXT.format(proj, srt, item.id, item))
                    m2ms_from.append(y)
                info_dict['m2ms_from'] = m2ms_from
            if not edit:
                if relaties:  # add relations to page
                    relaties.insert(0, '<div><span class="bold underline">Relaties'
                        '</span></div>')
                    info_dict["e_table"] = '\n'.join((info_dict["e_table"],
                        '\n'.join(relaties)))
                buttons = []
                for s in button_lijst:    #  build buttons to create related documents
                    buttons.append(BTNTXT.format(proj, s, "new", soort, id,
                        "Opvoeren " + naam_dict(s)[0]))
                info_dict["buttons"] = buttons
    info_dict["prev"] = prev
    info_dict["next"] = next
    for x,y,z in getfields(soort): # inhoud per veld (naam,type,lengte) op scherm zetten
        lengte[x] = z
        """bij Entiteit en Dataitem moet nog het vullen van {{attrdata}} met de onderliggende gegevens"""
        if edit:
            ## h = '' if edit == 'new' else o.__dict__[x]
            if y == 'Char':
                ## q = ''
                if x == 'nummer' and edit == 'new':
                    q = 'readonly="readonly"'
                    if soort == 'userwijz':
                        info_dict[x] = get_new_id(owner_proj.rfcs)
                    elif soort == 'userprob':
                        info_dict[x] = get_new_id(owner_proj.probs)
                    elif soort == 'bevinding':
                        info_dict[x] = get_new_id(owner_proj.tbev)
    info_dict['notnw'] = 'new'
    info_dict["lengte"] = lengte
    naam_ev,naam_mv,sect = naam_dict(soort)
    if edit == 'new':
        info_dict['new'] = 'nieuw'
        info_dict['title'] = 'Nieuw(e) '  + naam_ev
    else:
        if edit == 'edit':
            info_dict['edit'] = 'view'
        else:
            info_dict['view'] = 'edit'
        try:
            info_dict['title'] = ": ".join((naam_ev, o.naam))
        except AttributeError:
            info_dict['title'] = ": ".join((naam_ev, o.nummer))
        info_dict['data'] = o
    if soort == 'project':
        if not edit:
            all = my.Bevinding.objects.filter(project=proj)
            solved = all.filter(gereed=True).count()
            working = all.filter(gereed=False).filter(actie__isnull=False).count()
            all = all.count()
            if all == 0:
                test_stats = ("(nog) geen","opgevoerd")
            else:
                test_stats = (all, "waarvan {} opgelost en {} doorgekoppeld naar "
                    "Actiereg".format(solved, working))
            all = my.Userprob.objects.filter(project=proj)
            solved = all.filter(gereed=True).count()
            working = all.filter(gereed=False).filter(actie__isnull=False).count()
            all = all.count()
            if all == 0:
                prob_stats = ("(nog) geen","gemeld")
            else:
                prob_stats = (all, "waarvan {} opgelost en {} doorgekoppeld naar "
                    "Actiereg".format(solved, working))
            all = my.Userwijz.objects.filter(project=proj)
            solved = all.filter(gereed=True).count()
            working = all.filter(gereed=False).filter(actie__isnull=False).count()
            all = all.count()
            if all == 0:
                wijz_stats = ("(nog) geen","ingediend")
            else:
                wijz_stats = (all,"waarvan {} gerealiseerd en {} in behandeling via "
                    "Actiereg".format(solved, working))
            info_dict['test_stats'] = test_stats
            info_dict['prob_stats'] = prob_stats
            info_dict['wijz_stats'] = wijz_stats
    else:
        info_dict['title'] = "Project {0} - {1}".format(
            owner_proj.naam,info_dict["title"])
        if srt != '':
            info_dict['ref'] = (soort,naam_mv,verw)
        else:
            info_dict['lijst'] = soort
            info_dict['lijstvan'] = naam_mv
        info_dict["soort"] = soort
        info_dict["sect"] = '/'.join((soort,id))
        info_dict["sctn"] = sect
    w = leftw_dict.get(soort,120)
    info_dict["leftw"] = "{0}px".format(w)
    info_dict["rightw"] = "{0}px".format(910 - w)
    info_dict["rightm"] = "{0}px".format(w + 5)
    info_dict["sites"] = SITES
    try:
        info_dict["ar_proj"] = o.actiereg if soort == "project" else owner_proj.actiereg
    except UnboundLocalError:
        pass
    else:
        info_dict["ar_user"] = o.aruser if soort == "project" else owner_proj.aruser

    ## return HttpResponse("soort = %s, id = %s, proj = %s, edit = %s" % (soort, id,proj,edit))
    ## return HttpResponse('<br/>'.join((
    ## raise ValueError('Stopped')
    ## return HttpResponse('<br/>'.join((
        ## str(info_dict['fkeys_to']),
        ## str(info_dict['m2ms_to']),
        ## str(info_dict['fkeys_from']),
        ## str(info_dict['m2ms_from'])
        ## )))
    if edit:
        return render_to_response('{0}_edit.html'.format(soort), info_dict,
            context_instance=RequestContext(request)) # {'title': 'nieuw', 'soort': soort, 'id': id, 'proj': proj})
    else:
        return render_to_response('{0}_view.html'.format(soort), info_dict,
            context_instance=RequestContext(request)) # {'title': 'nieuw', 'soort': soort, 'id': id, 'proj': proj})

def koppel(request, proj='',soort='',id='', arid='0', arnum=''):
    """terugkoppeling vanuit probreg:
    neem de teruggegeven actiegegevens op in het huidige item"""
    ## data = request.GET
    ## return HttpResponse("".join(["{0}: {1}".format(x,y) for x,y in data.items()]))
    ## raise ValueError("Exception Intended")
    ## return HttpResponse("""\
    ## vervolg: {0}<br/>
    ## adres: {1}""".format(vervolg,vervolg.format(actie.id,actie.nummer)))
    doc = '/%s/%s/%s/' % (proj,soort,id)
    if arid == '0':
        return HttpResponseRedirect(doc + 'msg/{}'.format(arnum))
    o = my.rectypes[soort].objects.get(pk=id)
    o.actie = int(arid) # int(data.get("id","0"))
    o.actienummer = arnum # data.get("actie","")
    o.save()
    return HttpResponseRedirect(doc)

def meld(request,proj='',soort='',id='', arstat='', arfrom = '', arid=''):
    """terugkoppeling vanuit probreg:
    de actie is gearchiveerd of herleefd"""
    data = request.GET
    o = my.rectypes[soort].objects.get(pk=id)
    o.gereed = {"arch": True, "herl": False}[arstat]
    o.save()
    meld = 'Actie gearchiveerd' if arstat == 'arch' else 'Actie herleefd'
    doc = '/'.join((SITES["probreg"], arfrom, arid, 'mld', meld))
    return HttpResponseRedirect(doc)

def edit_item(request,proj='',soort='',id='',srt='',verw=''):
    ## raise ValueError('Testing...')
    # proj = projectnummer, soort = onderdeelnaam, id = item nummer of niks voor nieuw
    if proj:
        try:
            p = my.Project.objects.get(pk=proj)
        except:
            pass
    if soort == '':
        soort = 'project'
        if proj == 'proj':
            p = my.Project()
        to_actiereg = True if p.actiereg == "" else False
        for x,y,z in getfields('project'): # naam,type,lengte
            p.__dict__[x] = request.POST[x]
        p.save()
        if to_actiereg and p.actiereg != "":
            doc = "{}/addext/{}/{}/{}/".format(SITES["probreg"],
                p.id, p.actiereg, p.kort)
        else:
            proj = p.id
            doc = '/%s/' % proj
    elif soort in my.rectypes:
        if id:
            o = my.rectypes[soort].objects.get(pk=id)
        else:
            o = my.rectypes[soort]()
        ## return HttpResponse("soort = %s, id = %s, proj = %s, srt = %s, verw= %s" % (soort, id,proj,srt,verw))
        if proj:
            o.project = p
        # voor de zekerheid
        if soort == "dummy": # in ('funcdoc','userdoc','layout'):
            # aparte afhandeling voor documenten die een link kunnen bevatten
            model = models.get_model('doctool',soort.capitalize())
            ## manipulator = my.rectypes[soort].AddManipulator()
            ## new_data = request.POST.copy()
            ## new_data.update({'project': proj})
            ## for x,y,z in getfields(soort): # naam,type,lengte
                ## if x == 'link' and y == 'File':
                    ## new_data.update(request.FILES)
                    ## continue
            ## # return HttpResponse(str(new_data))
            ## errors = manipulator.get_validation_errors(new_data)
            ## manipulator.do_html2python(new_data)
            ## if not errors:
                ## new_object = manipulator.save(new_data)
                ## id = new_object.id
            ## else:
                ## return HttpResponse('\n'.join((str(errors),str(new_data))))
            ## id = new_object.id
            ## o = my.rectypes[soort].objects.get(pk=id)
        else:
            if soort in ('userwijz', 'userprob','bevinding'):
                gereed = o.gereed
            for x,y,z in getfields(soort): # naam,type,lengte
                if x == 'datum_gereed':
                    if request.POST['gereed'] == '1' and not gereed:
                        o.datum_gereed = datetime.datetime.today()
                elif x == "gereed":
                    o.gereed = True if request.POST[x] == "1" else False
                elif x == 'link':
                    if 'link_file' in request.FILES:
                        uploaded = request.FILES['link_file']
                        ## pad = [y.upload_to
                            ## for y in my.rectypes[soort]._meta.fields if y.name == 'link'][0]
                        ## save_file = "/".join((MEDIA_ROOT,pad,uploaded.name))
                        save_file = "/".join((MEDIA_ROOT,uploaded.name))
                        destination = open(save_file, 'wb+')
                        for chunk in uploaded.chunks():
                            destination.write(chunk)
                        destination.close()
                        o.__dict__[x] = uploaded.name
                else:
                    if x != 'datum_in':
                        try:
                            o.__dict__[x] = request.POST[x]
                        except KeyError:
                            pass
            o.save()
        # bijwerken van de eventueel meegegeven relatie
        if srt in my.rectypes:
            data = my.rectypes[srt].objects.get(pk=verw)
            rel,multiple = get_relation(o,soort,srt)
            ## return HttpResponse(str(new_data))
            if multiple:
                rel.add(data)
            else:
                rel = data
        o.save()
        id = o.id
        doc = '/%s/%s/%s/' % (proj,soort,id) if proj else '/%s/%s/' % (soort,id)
    return HttpResponseRedirect(doc)

def maak_rel(request,proj='',srt='',id='',soort='',verw=''):
    if srt in my.rectypes:
        o = my.rectypes[srt].objects.get(pk=id)
    if soort in my.rectypes:
        r = my.rectypes[soort].objects.get(pk=verw)
    rel,multiple = get_relation(o,srt,soort)
    if multiple:
        rel.add(r)
    else:
        rel = r
    o.save()
    doc = '/{0}/{1}/{2}/'.format(proj,srt,id) if proj else '/{0}/{1}/'.format(srt,id)
    return HttpResponseRedirect(doc)


# let op: theoretisch kan dit bij edit_item() in:
def edit_sub(request,proj='',srt1='',id1='',srt2='',id2=''):
    try: # do we have form data?
        data = request.POST
    except:
        data = {}
    if id2:
        o2 = my.rectypes[srt2].objects.get(pk=id2)
    else:
        o1 = my.rectypes[srt1].objects.get(pk=id1)
        o2 = my.rectypes[srt2]()
        o2.hoort_bij = o1
    ## return HttpResponse(str(o1.__dict__) + str(o2.__dict__))
    o2.naam = data["naam"]
    if (srt1,srt2) == ('entiteit','attribuut'):
        o2.type = data["type"]
        o2.bereik = data["bereik"]
        o2.primarykey = data["key"] if data["key"] in ('1','2','3','4','5') else '0'
    elif (srt1,srt2) == ('dataitem','element'):
        o2.soort = data["type"]
        o2.omschrijving = data["oms"]
        o2.sleutel = data["sleutel"] if data["sleutel"] in ('1','2','3','4','5') else '0'
    if "rel" in data:
        if data[rel] in [x.naam for x in my.Entiteit.objects.filter(project=o1.project)]:
        ## try:
            o2.relatie = my.rectypes[srt1].objects.get(naam=data["rel"])
        ## except ObjectDoesNotExist:
            ## pass
    o2.save()
    doc = '/%s/%s/%s/edit/' % (proj,srt1,id1) if proj else '/%s/%s/edit/' % (srt1,id1)
    return HttpResponseRedirect(doc)

def viewdoc(request):
    parts = request.path.split('files/')
    return render_to_response(MEDIA_ROOT + parts[1],{})
