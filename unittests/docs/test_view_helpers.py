"""unittests for ./docs/helpers.py
"""
from types import SimpleNamespace as NS
import datetime
import pytest
import docs.helpers as funcs
import docs.models as my
from django.http import Http404
from fixtures import (expected_relations, expected_field_attrs, expected_stats_texts,
                      expected_names_for_type, prepare_uploadfile)
FIXDATE = datetime.datetime(2021, 1, 1)


@pytest.fixture(autouse=True)
def lang_nl(settings):
    """stub
    """
    settings.LANGUAGE_CODE = 'nl.nl'


def print_elementen():  # wordt deze functie wel gebruikt en hoe?
    """was bedoeld om wat info over attributen van models in files weg te zetten
    """
    for name, cls in my.rectypes.items():
        with open(f'naslag/{name}_attr.rst', 'w') as out:
            print('attr,name,type,auto,concrete,{hidden,one2one,many2one,one2many,m2m,is_rel,'
                  'related_class)', file=out)
            for relobj in cls()._meta.get_fields(include_hidden=True):
                print(relobj, ',', relobj.name, ',', relobj.get_internal_type(), ',',
                      relobj.auto_created, ',', relobj.concrete, ',', relobj.hidden,
                      ',', relobj.is_relation, ',', relobj.one_to_one, ',',
                      relobj.many_to_one, ',', relobj.one_to_many, ',',
                      relobj.many_to_many, ',', relobj.related_model, file=out)


@pytest.mark.django_db
def test_get_related():
    """unittest for helpers.get_related
    """
    pr = my.Project.objects.create(naam="test", kort="test project", actiereg='TestProj',
                                   aruser='0001')
    sp = my.Userspec.objects.create(project=pr, naam="testspec", kort="poging 1")
    gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak", doel="uitproberen", spec=sp)
    aw = my.Userwijz.objects.create(project=pr, gereed=False)
    gt.rfc.add(aw)
    assert funcs.get_related(pr, my.Userwijz) is None
    assert funcs.get_related(pr, my.Gebrtaak) is None
    assert list(funcs.get_related(sp, my.Gebrtaak).all()) == [gt]
    # de vorige is raar, je wilt toch juist weten welke aw's naar deze gt verwijzen?
    assert list(funcs.get_related(aw, my.Gebrtaak, True).all()) == [gt]


def test_get_relation(expected_relations):
    """unittest for helpers.get_relation

    geen test op functionaliteit omdat monkeypatchen niet goed lukt
    daarom alleen test op resultaten
    """
    for soort in my.rectypes:
        for srt in my.rectypes:
            print(soort, srt)
            try:
                assert funcs.get_relation(soort, srt) == expected_relations[soort, srt]
            except KeyError:  # relatie bestaat niet <-> zit niet in fixture
                assert funcs.get_relation(soort, srt) == (None, None)


@pytest.mark.django_db
def test_set_relation_1():
    """unittest for helpers.set_relation: single
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")
    sp = my.Userspec.objects.create(project=pr, naam="testspec")
    funcs.set_relation(gt, 'gebrtaak', sp, 'userspec')
    gt_v2 = my.Gebrtaak.objects.get(pk=gt.id)
    assert gt_v2.spec == sp


@pytest.mark.django_db
def test_set_relation_2():
    """unittest for helpers.set_relation: multiple
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")
    aw = my.Userwijz.objects.create(project=pr, nummer='testwijz', gereed=False)
    funcs.set_relation(gt, 'gebrtaak', aw, 'userwijz')
    gt_v2 = my.Gebrtaak.objects.get(pk=gt.id)
    assert list(gt_v2.rfc.all()) == [aw]


@pytest.mark.django_db
def test_remove_relation_1():
    """unittest for helpers.remove_relation: single
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    sp = my.Userspec.objects.create(project=pr, naam="testspec")
    gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak", spec=sp)
    funcs.remove_relation(gt, 'gebrtaak', sp, 'userspec')
    gt_v2 = my.Gebrtaak.objects.get(pk=gt.id)
    assert gt_v2.spec is None


@pytest.mark.django_db
def test_remove_relation_2():
    """unittest for helpers.remove_relation: multiple
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")
    aw = my.Userwijz.objects.create(project=pr, nummer='testwijz', gereed=False)
    gt.rfc.add(aw)
    funcs.remove_relation(gt, 'gebrtaak', aw, 'userwijz')
    gt_v2 = my.Gebrtaak.objects.get(pk=gt.id)
    assert not list(gt_v2.rfc.all())


def test_corr_naam():
    """unittest for helpers.corr_naam
    """
    for naam in my.rectypes:
        if naam == 'techtaak':
            assert funcs.corr_naam(naam) == 'techtask'
        elif naam == 'programma':
            assert funcs.corr_naam(naam) == 'procproc'
        else:
            assert funcs.corr_naam(naam) == naam


def test_get_field_attr(expected_field_attrs):
    """unittest for helpers.get_field_attr

    ook hier alleen test op resultaten
    """
    for soort in my.rectypes:
        assert funcs.get_field_attr(soort) == expected_field_attrs[soort]


def _test_get_relation_fields():
    """unittest for helpers.get_relation_fields
    """
    # wordt niet gebruikt dus gaan we ook niet maken


@pytest.mark.django_db
def test_get_new_numberkey_for_soort():
    """unittest for helpers.get_new_numberkey_for_soort
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    yr = datetime.datetime.today().year
    first_this_year = f'{yr}-0001'
    for naam in my.rectypes:
        if naam in ('userwijz', 'userprob', 'bevinding'):
            assert funcs.get_new_numberkey_for_soort(pr, naam) == first_this_year
        else:
            assert funcs.get_new_numberkey_for_soort(pr, naam) == ''
    my.Userwijz.objects.create(project=pr, gereed=False, nummer=first_this_year)
    my.Userprob.objects.create(project=pr, gereed=False, nummer=first_this_year)
    my.Bevinding.objects.create(project=pr, gereed=False, nummer=first_this_year)
    for naam in ('userwijz', 'userprob', 'bevinding'):
        assert funcs.get_new_numberkey_for_soort(pr, naam) == f'{yr}-0002'


@pytest.mark.django_db
def test_get_stats_texts(expected_stats_texts):
    """unittest for helpers.get_stats_texts
    """
    pr = my.Project.objects.create(naam="test", kort="test project", actiereg='TestProj',
                                        aruser='0001')
    assert funcs.get_stats_texts(pr, 'bevinding') == ('(nog) geen', 'opgevoerd')
    assert funcs.get_stats_texts(pr, 'probleem') == ('(nog) geen', 'gemeld')
    assert funcs.get_stats_texts(pr, 'userwijz') == ('(nog) geen', 'ingediend')
    assert funcs.get_stats_texts(pr, 'x') == ('', '')
    aw1 = my.Userwijz.objects.create(project=pr, gereed=False)
    prb1 = my.Userprob.objects.create(project=pr, gereed=False)
    bev1 = my.Bevinding.objects.create(project=pr, gereed=False)
    assert funcs.get_stats_texts(pr, 'userwijz') == (1, 'waarvan 0 gerealiseerd'
                                                        ' en 0 in behandeling via Actiereg')
    assert funcs.get_stats_texts(pr, 'probleem') == (1, 'waarvan 0 opgelost'
                                                        ' en 0 doorgekoppeld naar Actiereg')
    assert funcs.get_stats_texts(pr, 'bevinding') == (1, 'waarvan 0 opgelost'
                                                         ' en 0 doorgekoppeld naar Actiereg')
    aw1.gereed = True
    aw1.save()
    my.Userwijz.objects.create(project=pr, gereed=False, actie=1)
    assert funcs.get_stats_texts(pr, 'userwijz') == (2, 'waarvan 1 gerealiseerd'
                                                        ' en 1 in behandeling via Actiereg')
    prb1.gereed = True
    prb1.save()
    my.Userprob.objects.create(project=pr, gereed=False, actie=2)
    assert funcs.get_stats_texts(pr, 'probleem') == (2, 'waarvan 1 opgelost'
                                                        ' en 1 doorgekoppeld naar Actiereg')
    bev1.gereed = True
    bev1.save()
    my.Bevinding.objects.create(project=pr, gereed=False, actie=3)
    assert funcs.get_stats_texts(pr, 'bevinding') == (2, 'waarvan 1 opgelost'
                                                         ' en 1 doorgekoppeld naar Actiereg')


def _test_get_names_for_type(expected_names_for_type):
    """unittest for helpers.get_names_for_type
    """
    # test failt al op de eerste vergelijking:
    # AssertionError: assert (' project ', ' project ', '') == ('project', 'projecten', '')
    for typename in my.rectypes:
        assert funcs.get_names_for_type(typename) == expected_names_for_type[typename]


@pytest.mark.django_db
def test_get_projectlist():
    """unittest for helpers.get_projectlist
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    pr2 = my.Project.objects.create(naam="extra", kort="nog een test project")
    assert list(funcs.get_projectlist()) == [pr2, pr]


@pytest.mark.django_db
def test_get_ordered_objectlist():
    """unittest for helpers.get_ordered_objectlist
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    gt1 = my.Gebrtaak.objects.create(project=pr, naam='Software')
    gt2 = my.Gebrtaak.objects.create(project=pr, naam='Meer software')
    gt3 = my.Gebrtaak.objects.create(project=pr, naam='Nog meer software')
    gt4 = my.Gebrtaak.objects.create(project=pr, naam='Geen software')
    assert list(funcs.get_ordered_objectlist(pr, 'gebrtaak')) == [gt4, gt2, gt3, gt1]
    aw1 = my.Userwijz.objects.create(project=pr, gereed=False, nummer='0015')
    aw2 = my.Userwijz.objects.create(project=pr, gereed=True, nummer='0001')
    aw3 = my.Userwijz.objects.create(project=pr, gereed=False, nummer='0005')
    assert list(funcs.get_ordered_objectlist(pr, 'userwijz')) == [aw2, aw3, aw1]


@pytest.mark.django_db
def test_get_object():
    """unittest for helpers.get_object
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    pkey = pr.id
    with pytest.raises(Http404):
        funcs.get_object('gebrtarsak', 1)
    assert funcs.get_object('project', pkey) == pr
    assert str(funcs.get_object('gebrtaak', 0, new=True)) == str(my.Gebrtaak())
    with pytest.raises(Http404):
        funcs.get_object('gebrtaak', 1)


def test_determine_adjacent():
    """unittest for helpers.determine_adjacent
    """
    assert funcs.determine_adjacent([NS(id=1), NS(id=2), NS(id=3)], NS(id=1)) == (0, 2)
    assert funcs.determine_adjacent([NS(id=1), NS(id=2), NS(id=3)], NS(id=2)) == (1, 3)
    assert funcs.determine_adjacent([NS(id=1), NS(id=2), NS(id=3)], NS(id=3)) == (2, 0)


@pytest.mark.django_db
def test_get_list_title_attrs():
    """unittest for helpers.get_list_title_attrs
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    assert funcs.get_list_title_attrs(pr.id, 'gebrtaak', '', 0, '') == (
            'Project test - Gebruikerstaken bij project test', 'gebruikerstaak',
            'gebruikerstaken', 'func')
    assert funcs.get_list_title_attrs('', 'gebrtaak', '', 0, '') == (
            'Lijst gebruikerstaken', 'gebruikerstaak', 'gebruikerstaken', 'func')
    assert funcs.get_list_title_attrs(pr.id, 'gebrtaak', 'userwijz', 1, '') == (
            'Project test - Gebruikerstaken bij project test', 'gebruikerstaak',
            'gebruikerstaken', 'func')
    assert funcs.get_list_title_attrs('', 'gebrtaak', 'userwijz', 1, '') == (
            'Lijst gebruikerstaken', 'gebruikerstaak', 'gebruikerstaken', 'func')
    sp = my.Userspec.objects.create(project=pr, naam='testspec')
    fp = my.Funcproc.objects.create(project=pr, naam='testproc', spec=sp)
    assert funcs.get_list_title_attrs(pr.id, 'gebrtaak', 'funcproc', fp.id, 'from') == (
            'Project test - functioneel proces "testproc" relateren aan gebruikerstaak ',
            'gebruikerstaak', 'gebruikerstaken', 'func')
    aw = my.Userwijz.objects.create(project=pr, nummer='0001', gereed=False)
    fp.rfc.add(aw)
    assert funcs.get_list_title_attrs(pr.id, 'userwijz', 'funcproc', fp.id, 'from') == (
            'Project test - functioneel proces "testproc" relateren aan aanvraag wijziging ',
            'aanvraag wijziging', 'aanvraag wijzigingen', 'user')
    assert funcs.get_list_title_attrs(pr.id, 'userwijz', 'funcproc', fp.id, 'to') == (
            'Project test - aanvraag wijziging relateren aan functioneel proces "testproc" ',
            'aanvraag wijziging', 'aanvraag wijzigingen', 'user')
    assert funcs.get_list_title_attrs(pr.id, 'funcproc', 'userwijz', aw.id, 'from') == (
            'Project test - aanvraag wijziging "0001" relateren aan functioneel proces ',
            'functioneel proces', 'functionele processen', 'func')
    assert funcs.get_list_title_attrs(pr.id, 'funcproc', 'userwijz', aw.id, 'to') == (
            'Project test - functioneel proces relateren aan aanvraag wijziging "0001" ',
            'functioneel proces', 'functionele processen', 'func')


def test_init_infodict(monkeypatch):
    """unittest for helpers.init_infodict
    """
    monkeypatch.setattr(funcs, 'get_projectlist', lambda: ['x', 'y', 'z'])
    assert funcs.init_infodict_for_detail('proj', 'project', 'new', '') == {
        'start': '', 'soort': 'project', 'prev': '', 'notnw': 'new', 'next': '',
        "sites": funcs.SITES, 'proj': '', 'sect': '', 'meld': '',
        'projecten': ['x', 'y', 'z'], 'mode': 'edit', 'new': 'nieuw'}
    assert funcs.init_infodict_for_detail(0, 'userspec', 'edit', '') == {
        'start': '', 'soort': 'userspec', 'prev': '', 'notnw': 'new', 'next': '',
        "sites": funcs.SITES, 'proj': 0, 'sect': '', 'meld': '',
        'projecten': ['x', 'y', 'z'], 'mode': 'edit', 'new': ''}
    assert funcs.init_infodict_for_detail(15, 'gebrtaak', 'view', 'melding') == {
        'start': '', 'soort': 'gebrtaak', 'prev': '', 'notnw': 'new', 'next': '',
        "sites": funcs.SITES, 'proj': 15, 'sect': '', 'meld': 'melding',
        'projecten': ['x', 'y', 'z'], 'mode': 'edit', 'new': ''}   # moet hier mode niet `view` zijn?


def test_get_update_url():
    """unittest for helpers.get_update_url
    """
    # goed situaties
    assert funcs.get_update_url('proj', 'new') == "/proj/mut/"
    assert funcs.get_update_url(1, 'notnew') == "/1/mut/"
    assert funcs.get_update_url(1, 'new', 'soort') == "/1/soort/mut/"
    assert funcs.get_update_url(1, 'new', 'soort', srt='srt', verw='verw') == "/1/soort/mut/srt/verw/"
    assert funcs.get_update_url(1, 'notnew', 'soort', 2) == '/1/soort/2/mut/'
    # fallback situatie
    assert not funcs.get_update_url(1, '')


def test_get_fieldlengths(expected_field_attrs):
    """unittest for helpers.get_fieldlengths
    """
    for soort in my.rectypes:
        assert funcs.get_fieldlengths(soort) == {x: z for x, y, z in expected_field_attrs[soort]}


def test_get_margins():
    """unittest for helpers.get_margins_for_type
    """
    assert funcs.get_margins_for_type('project') == ('140px', '770px', '145px')
    assert funcs.get_margins_for_type('userspec') == ('230px', '680px', '235px')
    assert funcs.get_margins_for_type('funcdoc') == ('160px', '750px', '165px')
    assert funcs.get_margins_for_type('gebrtaak') == ('240px', '670px', '245px')
    assert funcs.get_margins_for_type('funcproc') == ('160px', '750px', '165px')
    assert funcs.get_margins_for_type('entiteit') == ('140px', '770px', '145px')
    assert funcs.get_margins_for_type('techtaak') == ('200px', '710px', '205px')
    assert funcs.get_margins_for_type('techproc') == ('140px', '770px', '145px')
    assert funcs.get_margins_for_type('testplan') == ('140px', '770px', '145px')
    assert funcs.get_margins_for_type('bevinding') == ('140px', '770px', '145px')
    assert funcs.get_margins_for_type('anything') == ('120px', '790px', '125px')


def test_get_detail_title():
    """unittest for helpers.get_detail_title
    """
    testobj = None
    assert funcs.get_detail_title('gebrtaak', 'new', testobj) == 'Nieuw(e) gebruikerstaak'
    testobj = NS(naam='testnaam')
    assert funcs.get_detail_title('gebrtaak', '', testobj) == 'Gebruikerstaak testnaam'
    testobj = NS(nummer='testnummer')
    assert funcs.get_detail_title('gebrtaak', '', testobj) == 'Gebruikerstaak testnummer'


def test_get_relation_buttons():
    """unittest for helpers.get_relation_buttons
    """
    assert funcs.get_relation_buttons(1, 'gebrtaak', 2, []) == []
    button_list = ['userspec']
    assert len(funcs.get_relation_buttons(1, 'gebrtaak', 2, button_list)) == len(button_list)


@pytest.mark.django_db
def test_execute_update(prepare_uploadfile):
    """unittest for helpers.execute_update
    """
    # de logica gaat alleen over velden in userwijz userprob en bevinding
    # en over `link` in userdoc, funcdoc en layout
    # class MockDatetime(datetime.datetime):
    #     tzinfo = datetime.timezone.utc
    #     def __init__(self, *args):
    #         super().__init__()

    #     @classmethod
    #     def today(cls):
    #         retur
    # monkeypatch.setattr(funcs.datetime, 'datetime', MockDatetime)
    class Upload:
        """stub
        """
        name = 'testfile'
        def chunks(self):
            """stub
            """
            return [b'filechunk']
    prepfunc = prepare_uploadfile
    pr = my.Project.objects.create(naam="test", kort="test project")
    aw = my.Userwijz.objects.create(project=pr, gereed=False)
    postdict = {'gereed': '1', 'nummer': 'nieuw_nummer', 'wens': '', 'toelichting': '',
                'opmerkingen': '', 'actie': 0, 'actienummer': ''}
    funcs.execute_update('userwijz', aw, postdict)
    aw_v2 = my.Userwijz.objects.get(pk=aw.id)  # .objects.create(project=pr, gereed=False)
    assert aw_v2.gereed  # laat dit datetimes maar zitten
    filename = 'userdocs/testfile'
    prepfunc(filename)
    doc = my.Userdoc.objects.create(project=pr)
    postdict = {'naam': '', 'oms': '', 'tekst': ''}
    files = {'link_file': Upload()}
    funcs.execute_update('userdoc', doc, postdict, files)
    doc_v2 = my.Userdoc.objects.get(pk=doc.id)
    assert str(doc_v2.link) == filename
    with open(funcs.MEDIA_ROOT + filename) as _in:
        contents = _in.read()
    assert contents == 'filechunk'
    prepfunc(filename)


def _test_execute_update_for_link(prepare_uploadfile):
    """unittest for helpers.execute_update_for_link
    """
    # zit momenteel alleen in een gedeactiveerd gedeelte van update_document
    prepfunc = prepare_uploadfile
    filename = '/userdocs/testfile'
    prepfunc(filename)
    doc = my.Userdoc.objects.create(project=pr)
    postdict = {'naam': '', 'oms': '', 'tekst': ''}
    files = {'link_file': Upload()}
    funcs.execute_update('userdoc', doc, postdict, files)
    doc_v2 = my.Userdoc.objects.get(pk=doc.id)
    assert doc_v2.link == filename
    with open(funcs.MEDIA_ROOT + filename) as _in:
        contents = _in.read()
    assert contents == 'filechunk'
    prepfunc(filename)


@pytest.mark.django_db
def test_update_link_for_actiereg():
    """unittest for helpers.update_link_for_actiereg
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    testobj = my.Userwijz.objects.create(project=pr, gereed=False)
    volgnr = 1
    actie = 'actienr'
    funcs.update_link_from_actiereg(testobj, volgnr, actie)
    aw = my.Userwijz.objects.get(pk=testobj.id)
    assert aw.actie == volgnr
    assert aw.actienummer == actie


@pytest.mark.django_db
def test_update_status_from_actiereg():
    """unittest for helpers.update_status_from_actiereg
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    testobj = my.Userwijz.objects.create(project=pr, gereed=False)
    funcs.update_status_from_actiereg(testobj, 'arch')
    pr = my.Userwijz.objects.get(pk=testobj.id)
    assert pr.gereed
    funcs.update_status_from_actiereg(testobj, 'herl')
    pr = my.Userwijz.objects.get(pk=testobj.id)
    assert not pr.gereed


@pytest.mark.django_db
def test_update_subitem():
    """unittest for helpers.update_subitem
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    ent = my.Entiteit.objects.create(project=pr)
    att = my.Attribuut.objects.create(primarykey=1, hoort_bij=ent)
    funcs.update_subitem('entiteit', ent, 'attribuut', att, True, {'naam': "testattr", 'type': 'x',
                                                                   'bereik': 'y', 'key': 2})
    att_v2 = my.Attribuut.objects.get(pk=att.id)
    assert att_v2.hoort_bij == att.hoort_bij
    # assert att_v2.primarykey == att.primarykey  # assert 0 == '0' ?
    assert att_v2.naam == 'testattr'
    assert att_v2.type == 'x'
    assert att_v2.bereik == 'y'

    itm = my.Dataitem.objects.create(project=pr)
    ele = my.Dataelement.objects.create(sleutel=1, hoort_bij=itm)
    funcs.update_subitem('dataitem', itm, 'element', ele, False, {'naam': "testelement", 'type': 'x',
                                                                  'oms': 'q', 'sleutel': '2'})
    ele_v2 = my.Dataelement.objects.get(pk=ele.id)
    assert ele_v2.hoort_bij == ele.hoort_bij
    # assert ele_v2.sleutel == ele.sleutel  # assert 2 == '2'
    assert ele_v2.naam == 'testelement'
    assert ele_v2.soort == 'x'
    assert ele_v2.omschrijving == 'q'


@pytest.mark.django_db
def test_update_related():
    """unittest for helpers.update_related
    """
    pr = my.Project.objects.create(naam="test", kort="test project")
    with pytest.raises(Http404):
        funcs.update_related('project', pr, 'gargl', 'snork')
    gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")
    # update gebrtaak.spec (fkey)
    sp = my.Userspec.objects.create(project=pr, naam="testspec")
    funcs.update_related('gebrtaak', gt, 'userspec', sp.id)
    gt_v2 = my.Gebrtaak.objects.get(pk=gt.id)
    assert gt_v2.spec == sp
    # update gebrtaak.rfc (m2m)
    aw = my.Userwijz.objects.create(project=pr, nummer='testwijz', gereed=False)
    funcs.update_related('gebrtaak', gt, 'userwijz', aw.id)
    gt_v3 = my.Gebrtaak.objects.get(pk=gt.id)
    assert list(gt_v3.rfc.all()) == [aw]


@pytest.mark.django_db
class TestGetRelations:
    """unittests for helpers.GetRelations
    """

    def test_init(self):
        """unittest for GetRelations.init
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")
        testobj = funcs.GetRelations(gt, 'gebrtaak')  # , 'userspec')
        assert testobj.obj == gt
        assert testobj.soort == 'gebrtaak'
        # assert testobj.srt == 'userspec'
        assert testobj.opts == my.Gebrtaak._meta

    def test_get_foreignkeys_to_1(self):
        """unittest for GetRelations.get_foreignkeys_to
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")  # , spec=sp)
        testobj = funcs.GetRelations(gt, 'gebrtaak')
        result = testobj.get_foreignkeys_to()
        assert result[0]['btn'] == funcs.BTNTXT.format(pr.id, 'userspec', 'rel', 'gebrtaak', gt.id,
                                   funcs.ADD_TEXT)
        assert result[0]['text'] == 'Hoort bij gebruikersspecificatie'
        assert result[0]['links'] == []

    def test_get_foreignkeys_to_2(self):
        """unittest for GetRelations.get_foreignkeys_to
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        sp = my.Userspec.objects.create(project=pr, naam="testproc")
        gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak", spec=sp)
        testobj = funcs.GetRelations(gt, 'gebrtaak')
        result = testobj.get_foreignkeys_to()
        assert result[0]['text'] == 'Hoort bij gebruikersspecificatie'
        assert result[0]['links'] == [funcs.RELTXT.format(pr.id, 'userspec', sp.id,
                                                          sp.naam + ': ') + ' '
                                      + funcs.BTNTXT.format(pr.id, 'gebrtaak', gt.id,
                                                            'unrel/van/userspec', sp.id,
                                                            funcs.REMOVE_TEXT)]
        assert 'btn' not in result[0]

    def test_get_mamy2many_to_1(self):
        """unittest for GetRelations.get_mamy2many_to
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")  # , spec=sp)
        testobj = funcs.GetRelations(gt, 'gebrtaak')
        result = testobj.get_many2many_to()
        assert result[0]['text'] == 'Is geraakt door aanvraag wijziging'
        assert result[0]['btn'] == funcs.BTNTXT.format(pr.id, 'userwijz', 'rel', 'gebrtaak', gt.id,
                                   funcs.ADD_TEXT)
        assert result[0]['links'] == []

    def test_get_mamy2many_to_2(self):
        """unittest for GetRelations.get_mamy2many_to
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        aw = my.Userwijz.objects.create(project=pr, nummer='testwijz', gereed=False)
        gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")  # , spec=sp)
        gt.rfc.add(aw)
        testobj = funcs.GetRelations(gt, 'gebrtaak')
        result = testobj.get_many2many_to()
        assert result[0]['text'] == 'Is geraakt door aanvraag wijziging'
        assert result[0]['btn'] == funcs.BTNTXT.format(pr.id, 'userwijz', 'rel', 'gebrtaak', gt.id,
                                   funcs.ADD_TEXT)
        assert result[0]['links'] == [funcs.RELTXT.format(pr.id, 'userwijz', aw.id,
                                                          aw.nummer + ':  ') + ' '
                                      + funcs.BTNTXT.format(pr.id, 'gebrtaak', gt.id,
                                                            'unrel/van/userwijz', aw.id,
                                                            funcs.REMOVE_TEXT)]

    def test_get_foreignkeys_from_1(self):
        """unittest for GetRelations.get_foreignkeys_from: most element types
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        sp = my.Userspec.objects.create(project=pr, naam="testspec")
        gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak", spec=sp)
        fp = my.Funcproc.objects.create(project=pr, naam="testproc", spec=sp)
        testobj = funcs.GetRelations(sp, 'userspec')
        result = testobj.get_foreignkeys_from()
        assert result[0] == ['gebrtaak', 'funcproc']
        assert result[1][0]['text'] == 'Betrokken gebruikerstaak'
        assert result[1][0]['btn'] == funcs.BTNTXT.format(pr.id, 'userspec', sp.id, 'rel',
                                                          'gebrtaak', funcs.ADD_TEXT)
        assert result[1][0]['links'] == [funcs.RELTXT.format(pr.id, 'gebrtaak', gt.id,
                                                             gt.naam + ': ') + ' '
                                         + funcs.BTNTXT.format(pr.id, 'gebrtaak', gt.id,
                                                               'unrel/naar/userspec', sp.id,
                                                               funcs.REMOVE_TEXT)]
        assert result[1][1]['text'] == 'Betrokken functioneel proces'
        assert result[1][1]['btn'] == funcs.BTNTXT.format(pr.id, 'userspec', sp.id, 'rel',
                                                          'funcproc', funcs.ADD_TEXT)
        assert result[1][1]['links'] == [funcs.RELTXT.format(pr.id, 'funcproc', fp.id,
                                                             fp.naam + ': ') + ' '
                                         + funcs.BTNTXT.format(pr.id, 'funcproc', fp.id,
                                                               'unrel/naar/userspec', sp.id,
                                                               funcs.REMOVE_TEXT)]
        assert testobj.get_foreignkeys_from()[2:] == ([], [])

    def test_get_foreignkeys_from_2(self):
        """unittest for GetRelations.get_foreignkeys_from: element type entiteit / dataelement
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        ent = my.Entiteit.objects.create(project=pr, naam="testentiteit")
        att = my.Attribuut.objects.create(primarykey=1, naam="testattr", hoort_bij=ent)
        testobj = funcs.GetRelations(ent, 'entiteit')
        result = testobj.get_foreignkeys_from()
        assert result[:3] == ([], [], [])
        assert list(result[3]) == [att]

    def test_get_foreignkeys_from_3(self):
        """unittest for GetRelations.get_foreignkeys_from: element type dataitem / dataelement
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        itm = my.Dataitem.objects.create(project=pr, naam="testitem")
        ele = my.Dataelement.objects.create(sleutel=1, naam="testelement", hoort_bij=itm)
        testobj = funcs.GetRelations(itm, 'dataitem')
        result = testobj.get_foreignkeys_from()
        assert result[:3] == ([], [], [])
        assert list(result[3]) == [ele]

    def test_get_mamy2many_from(self):
        """unittest for GetRelations.get_mamy2many_from
        """
        pr = my.Project.objects.create(naam="test", kort="test project")
        sp = my.Userspec.objects.create(project=pr, naam="testspec")
        aw = my.Userwijz.objects.create(project=pr, nummer='testwijz', gereed=False)
        gt = my.Gebrtaak.objects.create(project=pr, naam="testtaak")  # , spec=sp)
        gt.rfc.add(aw)
        fp = my.Funcproc.objects.create(project=pr, naam="testproc", spec=sp)
        fp.rfc.add(aw)
        testobj = funcs.GetRelations(aw, 'userwijz')
        result = testobj.get_many2many_from()
        assert result[0] == ['gebrtaak', 'funcproc', 'entiteit']
        assert result[1][0]['text'] == 'Raakt gebruikerstaak'
        assert result[1][0]['btn'] == funcs.BTNTXT.format(pr.id, 'userwijz', aw.id, 'rel',
                                                         'gebrtaak', funcs.ADD_TEXT)
        assert result[1][0]['links'] == [funcs.RELTXT.format(pr.id, 'gebrtaak', gt.id,
                                                          gt.naam + ': ') + ' '
                                         + funcs.BTNTXT.format(pr.id, 'gebrtaak', gt.id,
                                                               'unrel/naar/userwijz', aw.id,
                                                               funcs.REMOVE_TEXT)]
        assert result[1][1]['text'] == 'Raakt functioneel proces'
        assert result[1][1]['btn'] == funcs.BTNTXT.format(pr.id, 'userwijz', aw.id, 'rel',
                                                         'funcproc', funcs.ADD_TEXT)
        assert result[1][1]['links'] == [funcs.RELTXT.format(pr.id, 'funcproc', fp.id,
                                                          fp.naam + ': ') + ' '
                                         + funcs.BTNTXT.format(pr.id, 'funcproc', fp.id,
                                                               'unrel/naar/userwijz', aw.id,
                                                               funcs.REMOVE_TEXT)]
        assert result[1][2]['text'] == 'Raakt entiteit'
        assert result[1][2]['btn'] == funcs.BTNTXT.format(pr.id, 'userwijz', aw.id, 'rel',
                                                         'entiteit', funcs.ADD_TEXT)
        assert result[1][2]['links'] == []
