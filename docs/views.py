"""Views for MyProjects Web Application
"""
from django.shortcuts import render     # , get_object_or_404
from django.template import loader
from django.http import HttpResponseRedirect    # HttpResponse,
from django.utils.translation import gettext as _
import docs.models as my
import docs.helpers as funcs
from myprojects.settings import MEDIA_ROOT, SITES


def index(request):
    """Show the landing page
    """
    return render(request,
                  'start.html',
                  {'title': _('Welcome to MyProjects (formerly known as DocTool)!'),
                   'meld': '',
                   'start': True,
                   'projecten': my.Project.objects.all().order_by('naam'),
                   'sites': SITES,
                   'footer': ''})


def lijst(request, proj, soort='', id='', rel='', srt=''):
    """show a list of documents

    arguments: proj = projectnummer, soort = onderdeelnaam
    """
    meld = ''
    info_dict = {'soort': soort,
                 'srt': srt,
                 'id': id,
                 'proj': proj,
                 'projecten': funcs.get_projectlist(),
                 'lijst': funcs.get_ordered_objectlist(proj, soort)}
    title, naam_ev, naam_mv, sect = funcs.get_list_title_attrs(proj, soort, srt, id, rel)
    info_dict['ref'] = (srt, naam_mv, id) if srt else ()
    # info_dict["soort"] = '/'.join((srt,id,soort))
    info_dict['title'] = title
    info_dict['lijstitem'] = naam_ev

    info_dict['lijstvan'] = naam_mv
    info_dict["sctn"] = sect
    info_dict['orient'] = 'van' if rel == 'from' else 'naar'

    if info_dict['lijst'].count() == 0:  # of   if len(lijst) == 0:
        meld = naam_mv.join((_("Geen "), _(" aanwezig")))
        if proj:
            meld += _(" bij dit project")
    info_dict['meld'] = meld
    info_dict['notnw'] = 'new'
    if rel:
        info_dict['start'] = 'x'  # forceert afwezigheid menu - nodig?
    doc = 'relateren.html' if rel else 'lijst.html'
    return render(request, doc, info_dict)


# "redirect" op basis van gewijzigde urlconf
def new_project(request):
    "opvoeren project"
    return view_project(request, edit='new')


# redirect versie van edit_item op basis van gewijzigde urlconf
def add_new_proj(request):
    "opvoeren project: wijzigingen doorvoeren"
    return update_project(request, proj='proj')


# afsplitsing van oorspronkelijke detail view, alleen voor projects
def view_project(request, proj='', edit='', meld=''):
    "project homepage, al dan niet opengezet voor wijzigen"
    info_dict = funcs.init_infodict_for_detail(proj, '', edit, meld)

    margins = funcs.get_margins_for_type('project')
    info_dict["leftw"], info_dict["rightw"], info_dict["rightm"] = margins

    info_dict['form_addr'] = '/docs' + funcs.get_update_url(proj, edit)
    info_dict["lengte"] = funcs.get_fieldlengths('project')

    if edit == 'new':
        o = None
    #     info_dict['title'] = 'Doctool! | ' + _('Nieuw project ')
    else:
        o = funcs.get_object('project', proj)
        # info_dict['title'] = 'Doctool! | Project ' + o.naam
        info_dict["ar_proj"] = o.actiereg
        info_dict["ar_user"] = o.aruser

    info_dict['title'] = funcs.get_detail_title('project', edit, o)
    info_dict['data'] = o

    if not edit:
        # info_dict["prev"], info_dict["next"] = funcs.determine_adjacent(all_items, obj)
        info_dict['test_stats'] = funcs.get_stats_texts(proj, 'bevinding')
        info_dict['prob_stats'] = funcs.get_stats_texts(proj, 'probleem')
        info_dict['wijz_stats'] = funcs.get_stats_texts(proj, 'userwijz')
    return render(request, 'project.html', info_dict)


# "redirect" op basis van gewijzigde urlconf
def edit_project(request, proj):
    "project homepage openstellen voor wijzigingen"
    return view_project(request, proj, 'edit')


# afsplitsing van oorspronkelijke edit_item view
def update_project(request, proj):
    "wijzigingen doorvoeren en (terug) naar homepage"
    new = True if proj == 'proj' else False
    p = funcs.get_object('project', proj, new)
    to_actiereg = True if p.actiereg == "" else False
    funcs.execute_update('project', p, request.POST)

    if to_actiereg and p.actiereg != "":
        doc = "{}/addext/{}/{}/{}/".format(SITES["probreg"], p.id, p.actiereg, p.kort)
    else:
        proj = p.id
        doc = '/docs/%s/' % proj
    return HttpResponseRedirect(doc)


def view_document(request, proj, edit='', soort='', id='', srt='', verw='', meld=''):
    """toon/wijzig document
    """
    info_dict = funcs.init_infodict_for_detail(proj, soort, edit, meld)

    margins = funcs.get_margins_for_type(soort)
    info_dict["leftw"], info_dict["rightw"], info_dict["rightm"] = margins
    info_dict["lengte"] = funcs.get_fieldlengths(soort)

    info_dict['form_addr'] = '/docs' + funcs.get_update_url(proj, edit, soort, id, srt, verw)

    owner_proj = funcs.get_object('project', proj)
    info_dict["ar_proj"] = owner_proj.actiereg
    info_dict["ar_user"] = owner_proj.aruser

    if id:    # existing item
        obj = funcs.get_object(soort, id=id)
        info_dict['data'] = obj
        all_items = funcs.get_ordered_objectlist(proj, soort)
        info_dict["prev"], info_dict["next"] = funcs.determine_adjacent(all_items, obj)
        relations = funcs.GetRelations(obj, soort)  # , srt)
        info_dict['fkeys_to'] = relations.get_foreignkeys_to()
        info_dict['m2ms_to'] = relations.get_many2many_to()
        # button_lijst = [] # of button_lijst = my.rectypes[soort].from_titles.keys()
        result = relations.get_foreignkeys_from()
        buttons, info_dict['fkeys_from'], info_dict['andere'], info_dict['attrs'] = result
        more_buttons, info_dict['m2ms_from'] = relations.get_many2many_from()
        button_lijst = buttons + more_buttons
        info_dict["sect"] = '/'.join((soort, str(id)))
        if edit == 'view':
            info_dict["buttons"] = funcs.get_relation_buttons(proj, soort, id, button_lijst)
    else:
        obj = None
        info_dict['nummer'] = funcs.get_new_numberkey_for_soort(owner_proj, soort)

    info_dict['title'] = "Project {} - {}".format(owner_proj.naam,
                                                  funcs.get_detail_title(soort, edit, obj))

    naam_ev, naam_mv, sect = funcs.get_names_for_type(soort)
    if srt != '':
        info_dict['ref'] = (soort, naam_mv, verw)
    else:
        info_dict['lijstsoort'] = soort
        info_dict['lijstvan'] = naam_mv
    info_dict["sctn"] = sect

    return render(request, '{}.html'.format(soort), info_dict)


def new_document(request, proj, soort):
    "document pagina openzetten voor opvoeren (initiële waarden)"
    return view_document(request, proj, 'new', soort)


def new_from_relation(request, proj, soort, srt, verw):
    "document pagina openzetten voor opvoeren (initiële waarden) met verwijzing naar 'vanuit'"
    return view_document(request, proj, 'new', soort, srt=srt, verw=verw)


def edit_document(request, proj, soort, id):
    "document pagina openzetten voor wijzigen"
    return view_document(request, proj, 'edit', soort, id)


def update_document(request, proj='', soort='', id='', srt='', verw=''):
    """Edit a document: wijzigingen doorvoeren

    proj = projectnummer, soort = onderdeelnaam, id = item nummer of niks voor nieuw
    """
    p = funcs.get_object('project', proj)
    new = False if id else True
    o = funcs.get_object(soort, id, new)
    if new:
        o.project = p
    funcs.execute_update(soort, o, request.POST, request.FILES)
    if srt:
        funcs.update_related(soort, o, srt, verw)
    doc = '/docs/%s/%s/%s/' % (proj, soort, o.id) if proj else '/docs/%s/%s/' % (soort, o.id)
    return HttpResponseRedirect(doc)


def koppel(request, proj='', soort='', id='', arid='0', arnum=''):
    """terugkoppeling vanuit actiereg:
    neem de teruggegeven actiegegevens op in het huidige item
    """
    doc = '/docs/%s/%s/%s/' % (proj, soort, id)
    if arid == '0':
        return HttpResponseRedirect(doc + 'msg/{}/'.format(arnum))
    funcs.update_link_from_actiereg(funcs.get_object(soort, id), arid, arnum)
    return HttpResponseRedirect(doc)


def meld(request, proj='', soort='', id='', arstat='', arfrom='', arid=''):
    """terugkoppeling vanuit actiereg:
    de actie is gearchiveerd of herleefd
    """
    funcs.update_status_from_actiereg(funcs.get_object(soort, id), arstat)
    meld = _('Actie gearchiveerd') if arstat == 'arch' else _('Actie herleefd')
    doc = '/'.join((SITES["probreg"], arfrom, arid, 'mld', meld))
    return HttpResponseRedirect(doc)


def maak_rel(request, proj='', srt='', id='', soort='', verw='', rel=''):
    """associate documents
    """
    o = funcs.get_object(srt, id)
    r = funcs.get_object(soort, verw)
    funcs.set_relation(o, srt, r, soort)
    if rel == 'naar':
        srt, id = soort, verw
    doc = '/docs/{}/{}/{}/'.format(proj, srt, id) if proj else '/docs/{}/{}/'.format(srt, id)
    return HttpResponseRedirect(doc)


def unrelate(request, proj='', srt='', id='', soort='', verw='', rel=''):
    """sever an association between documents
    """
    o = funcs.get_object(srt, id)
    r = funcs.get_object(soort, verw)
    funcs.remove_relation(o, srt, r, soort)
    if rel == 'naar':
        srt, id = soort, verw
    doc = '/docs/{}/{}/{}/'.format(proj, srt, id) if proj else '/docs/{}/{}/'.format(srt, id)
    return HttpResponseRedirect(doc)


def edit_sub(request, proj='', srt1='', id1='', srt2='', id2=''):
    """Edit subitem - let op: theoretisch kan dit bij edit_item() in
    """
    # try:  # do we have form data?
    data = request.POST
    # except AttributeError:
    #     data = {}
    obj1 = funcs.get_object(srt1, id1)  # my.rectypes[srt1].objects.get(pk=id1)
    new = True if not id2 else False
    obj2 = funcs.get_object(srt2, id2, new)  # my.rectypes[srt2].objects.get(pk=id2)
    funcs.update_subitem(srt1, obj1, srt2, obj2, new, data)
    doc = '/docs/%s/%s/%s/edit/' % (proj, srt1, id1) if proj else '/docs/%s/%s/edit/' % (srt1, id1)
    return HttpResponseRedirect(doc)


def viewdoc(request):
    """display an uploaded document
    """
    parts = request.path.split('files/')
    return render(request, MEDIA_ROOT + parts[1], {})
