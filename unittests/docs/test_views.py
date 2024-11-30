"""unittests for ./docs/views.py
"""
import os
import types
import pytest

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myprojects.settings")
django.setup()
from docs import views

class MockRequest(django.http.request.HttpRequest):
    """stub
    """

@pytest.fixture(autouse=True)
def lang_nl(settings):
    """stub
    """
    settings.LANGUAGE_CODE = 'nl.nl'

def test_index(monkeypatch):
    """unittest for views.index
    """
    class MockQuerySet:
        """stub
        """
        data = [{'naam': 'y'}, {'naam': 'x'}]
        def order_by(self, key):
            """stub
            """
            return sorted(self.data, key=lambda x: x['naam'])
    # include in every test?
    monkeypatch.setattr(views, 'render', lambda x, y, z: (x, y, z))
    monkeypatch.setattr(views.my.Project.objects, 'all', MockQuerySet)
    # result = views.index('request')
    request = MockRequest()
    result = views.index(request)
    # assert result[0] == 'request'
    assert result[0] == request
    assert result[1] == 'start.html'
    assert result[2] == {'title': views._('Welcome to MyProjects (formerly known as DocTool)!'),
                         'meld': '',
                         'start': True,
                         'projecten': [{'naam': 'x'}, {'naam': 'y'}],
                         'sites': views.SITES,
                         'footer': ''}


def test_lijst(monkeypatch):
    """unittest for views.lijst
    """
    class MockQuerySet1:
        """stub
        """
        data = ['item 1', 'item 2']
        def __iter__(self):
            """stub
            """
            return (x for x in self.data)
        def count(self):
            """stub
            """
            return len(self.data)
    class MockQuerySet2:
        """stub
        """
        data = []
        def __iter__(self):
            """stub
            """
            return (x for x in self.data)
        def count(self):
            """stub
            """
            return len(self.data)
    def mock_get_attrs(*args):
        """stub
        """
        return 'title', 'name', 'plural', 'section'
    monkeypatch.setattr(views, 'render', lambda x, y, z: (x, y, z))
    monkeypatch.setattr(views.funcs, 'get_projectlist', lambda: [{'naam': 'x'}, {'naam': 'y'}])
    monkeypatch.setattr(views.funcs, 'get_ordered_objectlist', lambda x, y: MockQuerySet1())
    monkeypatch.setattr(views.funcs, 'get_list_title_attrs', mock_get_attrs)
    request = MockRequest()
    response = views.lijst(request, 1)
    assert response[0] == request
    assert response[1] == 'lijst.html'
    lijst = response[2].pop('lijst')
    assert response[2] == {'id': '', 'lijstitem': 'name', 'lijstvan': 'plural', 'meld': '',
                           'notnw': 'new',
                           'orient': 'naar', 'proj': 1, 'projecten': [{'naam': 'x'}, {'naam': 'y'}],
                           'ref': (), 'sctn': 'section', 'soort': '', 'srt': '', 'title': 'title'}
    assert list(lijst) == ['item 1', 'item 2']

    monkeypatch.setattr(views.funcs, 'get_ordered_objectlist', lambda x, y: MockQuerySet2())
    response = views.lijst(request, 0)
    lijst = response[2].pop('lijst')
    assert response[2] == {'id': '', 'lijstitem': 'name', 'lijstvan': 'plural',
                           'meld': 'Geen plural aanwezig', 'notnw': 'new',
                           'orient': 'naar', 'proj': 0, 'projecten': [{'naam': 'x'}, {'naam': 'y'}],
                           'ref': (), 'sctn': 'section', 'soort': '', 'srt': '', 'title': 'title'}
    assert not list(lijst)
    monkeypatch.setattr(views.funcs, 'get_ordered_objectlist', lambda x, y: MockQuerySet2())
    response = views.lijst(request, 1)
    lijst = response[2].pop('lijst')
    assert response[2] == {'id': '', 'lijstitem': 'name', 'lijstvan': 'plural',
                           'meld': 'Geen plural aanwezig bij dit project', 'notnw': 'new',
                           'orient': 'naar', 'proj': 1, 'projecten': [{'naam': 'x'}, {'naam': 'y'}],
                           'ref': (), 'sctn': 'section', 'soort': '', 'srt': '', 'title': 'title'}
    assert not list(lijst)

    monkeypatch.setattr(views.funcs, 'get_ordered_objectlist', lambda x, y: MockQuerySet1())
    response = views.lijst(request, 1, 'soort', 'id', 'from', 'srt')
    lijst = response[2].pop('lijst')
    assert response[2] == {'id': 'id', 'lijstitem': 'name', 'lijstvan': 'plural', 'meld': '',
                           'notnw': 'new',
                           'orient': 'van', 'proj': 1, 'projecten': [{'naam': 'x'}, {'naam': 'y'}],
                           'ref': ('srt', 'plural', 'id'), 'sctn': 'section', 'soort': 'soort',
                           'srt': 'srt', 'start': 'x', 'title': 'title'}
    assert list(lijst) == ['item 1', 'item 2']


def test_new_project(monkeypatch):
    """unittest for views.new_project
    """
    def mock_view_project(*args, **kwargs):
        """stub
        """
        return f'called view_project with args {args} and kwargs {kwargs}'
    monkeypatch.setattr(views, 'view_project', mock_view_project)
    assert views.new_project('request') == ("called view_project with args ('request',)"
                                            " and kwargs {'edit': 'new'}")


def test_add_new_proj(monkeypatch):
    """unittest for views.add_new_proj
    """
    def mock_update_project(*args, **kwargs):
        """stub
        """
        return f'called update_project with args {args} and kwargs {kwargs}'
    monkeypatch.setattr(views, 'update_project', mock_update_project)
    assert views.add_new_proj('request') == ("called update_project with args ('request',)"
                                             " and kwargs {'proj': 'proj'}")


def test_view_project(monkeypatch, capsys):
    """unittest for views.view_project
    """
    def mock_init_infodict(*args):
        """stub
        """
        print('call init_infodict with args', args)
        return {}
    def mock_get_margins(*args):
        """stub
        """
        return 'x', 'y', 'z'
    def mock_get_update_url(*args):
        """stub
        """
        print('call get_update_url with args', args)
        return '/update_url'
    def mock_get_fieldlengths(*args):
        """stub
        """
        return 'q'
    def mock_get_object(srt, id):
        """stub
        """
        return types.SimpleNamespace(soort=srt, id=id, actiereg='arproj', aruser='aruser')
    def mock_get_detail_title(*args):
        """stub
        """
        print('call get_detail_title with args', args)
        return 'detail_title'
    def mock_get_stats_texts(*args):
        """stub
        """
        return f'stats_text with args {args}'
    monkeypatch.setattr(views.funcs, 'init_infodict_for_detail', mock_init_infodict)
    monkeypatch.setattr(views.funcs, 'get_margins_for_type', mock_get_margins)
    monkeypatch.setattr(views.funcs, 'get_update_url', mock_get_update_url)
    monkeypatch.setattr(views.funcs, 'get_fieldlengths', mock_get_fieldlengths)
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'get_detail_title', mock_get_detail_title)
    monkeypatch.setattr(views.funcs, 'get_stats_texts', mock_get_stats_texts)
    monkeypatch.setattr(views, 'render', lambda x, y, z: (x, y, z))
    response = views.view_project('request')
    assert response[0] == 'request'
    assert response[1] == 'project.html'
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'form_addr': '/docs/update_url',
                           'data': types.SimpleNamespace(soort='project', id='', actiereg='arproj',
                               aruser='aruser'),
                           'leftw': 'x', 'lengte': 'q', 'rightm': 'z', 'rightw': 'y',
                           'prob_stats': "stats_text with args ('', 'probleem')",
                           'test_stats': "stats_text with args ('', 'bevinding')",
                           'title': 'detail_title',
                           'wijz_stats': "stats_text with args ('', 'userwijz')"}
    assert capsys.readouterr().out == ("call init_infodict with args ('', '', '', '')\n"
                                       "call get_update_url with args ('', '')\n"
                                       "call get_detail_title with args ('project', '', namespace("
                                       "soort='project', id='', actiereg='arproj', aruser='aruser'))\n")

    response = views.view_project('request', 'proj', 'new', 'meld')
    assert response[2] == {'data': None, 'form_addr': '/docs/update_url', 'leftw': 'x', 'lengte': 'q',
                           'rightm': 'z', 'rightw': 'y', 'title': 'detail_title'}
    assert capsys.readouterr().out == ("call init_infodict with args ('proj', '', 'new', 'meld')\n"
                                       "call get_update_url with args ('proj', 'new')\n"
                                       "call get_detail_title with args ('project', 'new', None)\n")

    response = views.view_project('request', 'proj', 'edit', 'meld')
    # data = response[2].pop('data')
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'form_addr': '/docs/update_url',
                           'data': types.SimpleNamespace(soort='project', id='proj', actiereg='arproj',
                               aruser='aruser'),
                           'leftw': 'x', 'lengte': 'q', 'rightm': 'z', 'rightw': 'y',
                           'title': 'detail_title'}
    assert capsys.readouterr().out == ("call init_infodict with args ('proj', '', 'edit', 'meld')\n"
                                       "call get_update_url with args ('proj', 'edit')\n"
                                       "call get_detail_title with args ('project', 'edit',"
                                       " namespace(soort='project', id='proj', actiereg='arproj',"
                                       " aruser='aruser'))\n")


def test_edit_project(monkeypatch):
    """unittest for views.edit_project
    """
    def mock_view_project(*args):
        """stub
        """
        return f'called view_project with args {args}'
    monkeypatch.setattr(views, 'view_project', mock_view_project)
    assert views.edit_project('request', 'proj') == ("called view_project with args ('request',"
                                                     " 'proj', 'edit')")


def test_update_project(monkeypatch, capsys):
    """unittest for views.update_project
    """
    def mock_get_object(srt, id, new=False):
        """stub
        """
        obj = types.SimpleNamespace(soort=srt)
        obj.id = 'new_id' if new else id
        obj.actiereg = '' if new else '1'
        return obj
    def mock_execute_update(*args):
        """stub
        """
        print('called execute_update with args', args)
    def mock_update_related(*args):
        """stub
        """
        print('called update_related with args', args)
    def mock_get_object_2(srt, id, new=False):
        """stub
        """
        obj = types.SimpleNamespace(soort=srt, id=1, kort='kort', actiereg='')
        return obj
    def mock_execute_update_2(*args):  # project, p, postdict):
        """stub
        """
        args[1].actiereg = 1  # p.actiereg = 1
        print('called execute_update with args', args)  # ({project}, {p}, {postdict})')
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'execute_update', mock_execute_update)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    req = MockRequest()
    req.POST = 'postdict'
    assert views.update_project(req, 'proj') == '/docs/new_id/'
    assert capsys.readouterr().out == ("called execute_update with args ('project', namespace(soort="
                                       "'project', id='new_id', actiereg=''), 'postdict')\n")
    assert views.update_project(req, 1) == '/docs/1/'
    assert capsys.readouterr().out == ("called execute_update with args ('project', namespace(soort="
                                       "'project', id=1, actiereg='1'), 'postdict')\n")
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object_2)
    monkeypatch.setattr(views.funcs, 'execute_update', mock_execute_update_2)
    assert views.update_project(req, 1) == 'http://actiereg.lemoncurry.nl/addext/1/1/kort/'
    assert capsys.readouterr().out == ("called execute_update with args ('project', namespace(soort="
                                       "'project', id=1, kort='kort', actiereg=1), 'postdict')\n")


def test_view_document(monkeypatch, capsys):
    """unittest for views.view_document
    """
    def mock_init_infodict(*args):
        """stub
        """
        print('call init_infodict with args', args)
        return {}
    def mock_get_margins(*args):
        """stub
        """
        return 'x', 'y', 'z'
    def mock_get_fieldlengths(*args):
        """stub
        """
        return 'q'
    def mock_get_update_url(*args):
        """stub
        """
        print('call get_update_url with args', args)
        return '/update_url'
    def mock_get_object(srt, id):
        """stub
        """
        obj = types.SimpleNamespace(soort=srt, id=id)
        if srt == 'project':
            obj.naam = 'projectnaam'
            obj.actiereg = 'arproj'
            obj.aruser = 'aruser'
        return obj
    def mock_get_objectlist(proj, soort):
        """stub
        """
        return 'prev_item', 'this_item', 'next_item'
    def mock_determine_adjacent(*args):
        """stub
        """
        print('call determine_adjacent with args', args)
        return args[0][0], args[0][2]
    class MockGetRelations:
        """stub
        """
        def __init__(self, obj, soort):
            self.obj = obj
            self.soort = soort
        def get_foreignkeys_to(self):
            """stub
            """
            return f'foreignkeys to {self.soort} {self.obj.id}'
        def get_many2many_to(self):
            """stub
            """
            return f'many to many relations to {self.soort} {self.obj.id}'
        def get_foreignkeys_from(self):
            """stub
            """
            return (['fkey buttons'], f'foreignkeys from {self.soort} {self.obj.id}',
                    'andere fkeys', 'fkey attrs')
        def get_many2many_from(self):
            """stub
            """
            return ['m2m buttons'], f'm2m relations from {self.soort} {self.obj.id}'
    def mock_get_relation_buttons(*args):
        """stub
        """
        return f'relation buttons with args {args}'
    def mock_get_new_numberkey(proj, soort):
        """stub
        """
        return 'new_numberkey'
    def mock_get_detail_title(*args):
        """stub
        """
        print('call get_detail_title with args', args)
        return 'detail_title'
    def mock_get_names_for_type(soort):
        """stub
        """
        return 'soort_ev', 'soort_mv', 'sectnaam'
    monkeypatch.setattr(views.funcs, 'init_infodict_for_detail', mock_init_infodict)
    monkeypatch.setattr(views.funcs, 'get_margins_for_type', mock_get_margins)
    monkeypatch.setattr(views.funcs, 'get_fieldlengths', mock_get_fieldlengths)
    monkeypatch.setattr(views.funcs, 'get_update_url', mock_get_update_url)
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'get_ordered_objectlist', mock_get_objectlist)
    monkeypatch.setattr(views.funcs, 'determine_adjacent', mock_determine_adjacent)
    monkeypatch.setattr(views.funcs, 'GetRelations', MockGetRelations)
    monkeypatch.setattr(views.funcs, 'get_relation_buttons', mock_get_relation_buttons)
    monkeypatch.setattr(views.funcs, 'get_new_numberkey_for_soort', mock_get_new_numberkey)
    monkeypatch.setattr(views.funcs, 'get_detail_title', mock_get_detail_title)
    monkeypatch.setattr(views.funcs, 'get_names_for_type', mock_get_names_for_type)
    monkeypatch.setattr(views, 'render', lambda x, y, z: (x, y, z))
    response = views.view_document('request', 'proj', meld='melding')
    assert response[0] == 'request'
    assert response[1] == '.html'
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'form_addr': '/docs/update_url',
                           'leftw': 'x', 'lengte': 'q', 'lijstsoort': '', 'lijstvan': 'soort_mv',
                           'nummer': 'new_numberkey', 'rightm': 'z', 'rightw': 'y',
                           'sctn': 'sectnaam', 'title': 'Project projectnaam - detail_title'}
    assert capsys.readouterr().out == ("call init_infodict with args ('proj', '', '', 'melding')\n"
                                       "call get_update_url with args ('proj', '', '', '', '', '')\n"
                                       "call get_detail_title with args ('', '', None)\n")
    response = views.view_document('request', 'proj', 'view', 'soort', 'id')
    assert response[0] == 'request'
    assert response[1] == 'soort.html'
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'form_addr': '/docs/update_url',
                           'data': types.SimpleNamespace(soort='soort', id='id'),
                           'leftw': 'x', 'lengte': 'q', 'lijstsoort': 'soort', 'lijstvan': 'soort_mv',
                           'rightm': 'z', 'rightw': 'y', 'sctn': 'sectnaam', 'sect': 'soort/id',
                           'title': 'Project projectnaam - detail_title',
                           'buttons': "relation buttons with args ('proj', 'soort', 'id',"
                           " ['fkey buttons', 'm2m buttons'])",
                           'fkeys_from': 'foreignkeys from soort id',
                           'fkeys_to': 'foreignkeys to soort id',
                           'm2ms_from': 'm2m relations from soort id',
                           'm2ms_to': 'many to many relations to soort id',
                           'andere': 'andere fkeys', 'attrs': 'fkey attrs',
                           'next': 'next_item', 'prev': 'prev_item'}
    assert capsys.readouterr().out == ("call init_infodict with args ('proj', 'soort', 'view', '')\n"
                                       "call get_update_url with args ('proj', 'view', 'soort', 'id',"
                                       " '', '')\n"
                                       "call determine_adjacent with args (('prev_item', 'this_item',"
                                       " 'next_item'), namespace(soort='soort', id='id'))\n"
                                       "call get_detail_title with args ('soort', 'view',"
                                       " namespace(soort='soort', id='id'))\n")
    response = views.view_document('request', 'proj', 'edit', 'soort', 'id')
    assert response[0] == 'request'
    assert response[1] == 'soort.html'
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'form_addr': '/docs/update_url',
                           'data': types.SimpleNamespace(soort='soort', id='id'),
                           'leftw': 'x', 'lengte': 'q', 'lijstsoort': 'soort', 'lijstvan': 'soort_mv',
                           'rightm': 'z', 'rightw': 'y', 'sctn': 'sectnaam', 'sect': 'soort/id',
                           'title': 'Project projectnaam - detail_title',
                           'fkeys_from': 'foreignkeys from soort id',
                           'fkeys_to': 'foreignkeys to soort id',
                           'm2ms_from': 'm2m relations from soort id',
                           'm2ms_to': 'many to many relations to soort id',
                           'andere': 'andere fkeys', 'attrs': 'fkey attrs',
                           'next': 'next_item', 'prev': 'prev_item'}
    assert capsys.readouterr().out == ("call init_infodict with args ('proj', 'soort', 'edit', '')\n"
                                       "call get_update_url with args ('proj', 'edit', 'soort', 'id',"
                                       " '', '')\n"
                                       "call determine_adjacent with args (('prev_item', 'this_item',"
                                       " 'next_item'), namespace(soort='soort', id='id'))\n"
                                       "call get_detail_title with args ('soort', 'edit',"
                                       " namespace(soort='soort', id='id'))\n")
    response = views.view_document('request', 'proj', 'view', 'soort', 'id', 'srt', 'ref')
    assert response[0] == 'request'
    assert response[1] == 'soort.html'
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'form_addr': '/docs/update_url',
                           'data': types.SimpleNamespace(soort='soort', id='id'),
                           'leftw': 'x', 'lengte': 'q', 'rightm': 'z', 'rightw': 'y',
                           'sctn': 'sectnaam', 'sect': 'soort/id',
                           'title': 'Project projectnaam - detail_title',
                           'andere': 'andere fkeys', 'attrs': 'fkey attrs',
                           'buttons': "relation buttons with args ('proj', 'soort', 'id', "
                           "['fkey buttons', 'm2m buttons'])",
                           'fkeys_from': 'foreignkeys from soort id',
                           'fkeys_to': 'foreignkeys to soort id',
                           'm2ms_from': 'm2m relations from soort id',
                           'm2ms_to': 'many to many relations to soort id',
                           'next': 'next_item', 'prev': 'prev_item',
                           'ref': ('soort', 'soort_mv', 'ref')}
    assert capsys.readouterr().out == ("call init_infodict with args ('proj', 'soort', 'view', '')\n"
                                       "call get_update_url with args ('proj', 'view', 'soort', 'id',"
                                       " 'srt', 'ref')\n"
                                       "call determine_adjacent with args (('prev_item', 'this_item',"
                                       " 'next_item'), namespace(soort='soort', id='id'))\n"
                                       "call get_detail_title with args ('soort', 'view',"
                                       " namespace(soort='soort', id='id'))\n")


def test_new_document(monkeypatch):
    """unittest for views.new_document
    """
    def mock_view_document(*args, **kwargs):
        """stub
        """
        return f'called view_document with args {args}'
    monkeypatch.setattr(views, 'view_document', mock_view_document)
    assert views.new_document('request', 'proj', 'soort') == (
            "called view_document with args ('request', 'proj', 'new', 'soort')")


def test_new_from_relation(monkeypatch):
    """unittest for views.new_from_relation
    """
    def mock_view_document(*args, **kwargs):
        """stub
        """
        return f'called view_document with args {args} and kwargs {kwargs}'
    monkeypatch.setattr(views, 'view_document', mock_view_document)
    assert views.new_from_relation('request', 'proj', 'soort', 'srt', 'verw') == (
            "called view_document with args ('request', 'proj', 'new', 'soort')"
            " and kwargs {'srt': 'srt', 'verw': 'verw'}")


def test_edit_document(monkeypatch):
    """unittest for views.edit_document
    """
    def mock_view_document(*args, **kwargs):
        """stub
        """
        return f'called view_document with args {args}'
    monkeypatch.setattr(views, 'view_document', mock_view_document)
    assert views.edit_document('request', 'proj', 'soort', 'id') == (
            "called view_document with args ('request', 'proj', 'edit', 'soort', 'id')")


def mock_get_object(srt, id, new=False):
    """stub
    """
    obj = "new " if new else ''
    return f'{obj}{srt} {id}'


def test_update_document(monkeypatch, capsys):
    """unittest for views.update_document
    """
    def mock_get_object(srt, id, new=False):
        """stub
        """
        obj = types.SimpleNamespace(soort=srt)
        obj.id = 0 if new else id
        return obj
    def mock_execute_update(*args):
        """stub
        """
        print('called execute_update with args', args)
    def mock_update_related(*args):
        """stub
        """
        print('called update_related with args', args)
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'execute_update', mock_execute_update)
    monkeypatch.setattr(views.funcs, 'update_related', mock_update_related)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    req = MockRequest()
    req.POST = 'postdict'
    req.FILES = 'filesdict'
    assert views.update_document(req) == '/docs//0/'
    assert capsys.readouterr().out == ("called execute_update with args ('', namespace(soort='',"
            " id=0, project=namespace(soort='project', id='')), 'postdict', 'filesdict')\n")
    assert views.update_document(req, 'proj', 'soort') == '/docs/proj/soort/0/'
    assert capsys.readouterr().out == ("called execute_update with args ('soort', namespace(soort="
            "'soort', id=0, project=namespace(soort='project', id='proj')), 'postdict', 'filesdict')\n")
    assert views.update_document(req, 'proj', 'soort', 'id') == '/docs/proj/soort/id/'
    assert capsys.readouterr().out == ("called execute_update with args ('soort', namespace(soort="
            "'soort', id='id'), 'postdict', 'filesdict')\n")
    assert views.update_document(req, 'proj', 'soort', 'id', 'srt', 'verw') == '/docs/proj/soort/id/'
    assert capsys.readouterr().out == ("called execute_update with args ('soort', namespace(soort="
                                       "'soort', id='id'), 'postdict', 'filesdict')\n"
                                       "called update_related with args ('soort', namespace(soort="
                                       "'soort', id='id'), 'srt', 'verw')\n")


def test_koppel(monkeypatch, capsys):
    """unittest for views.koppel
    """
    def mock_update_link(*args):
        """stub
        """
        print('called update_link_from_actiereg with args', args)
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'update_link_from_actiereg', mock_update_link)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.koppel('request') == '/docs////msg//'
    assert capsys.readouterr().out == ''
    assert views.koppel('request', 'proj', 'soort', 'id') == '/docs/proj/soort/id/msg//'
    assert capsys.readouterr().out == ''
    assert views.koppel('request', 'proj', 'soort', 'id', 'arid', 'arnum') == '/docs/proj/soort/id/'
    assert capsys.readouterr().out == ("called update_link_from_actiereg with args"
                                       " ('soort id', 'arid', 'arnum')\n")
    assert views.koppel('request', 'pr', 'srt', 'id', arnum='arnum') == '/docs/pr/srt/id/msg/arnum/'
    assert capsys.readouterr().out == ''


def test_meld(monkeypatch, capsys):
    """unittest for views.meld
    """
    def mock_update_status(*args):
        """stub
        """
        print('called update_status_from_actiereg with args:', args)
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'update_status_from_actiereg', mock_update_status)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.meld('request') == 'http://actiereg.lemoncurry.nl///mld/Actie herleefd'
    assert capsys.readouterr().out == "called update_status_from_actiereg with args: (' ', '')\n"
    assert views.meld('request', 'proj', 'soort', 'id') == ('http://actiereg.lemoncurry.nl/'
                                                            '//mld/Actie herleefd')
    assert capsys.readouterr().out == ("called update_status_from_actiereg with args: ('soort id',"
                                       " '')\n")
    assert views.meld('request', 'proj', 'soort', 'id', 'arch', 'arfrom', 'arid') == (
            'http://actiereg.lemoncurry.nl/arfrom/arid/mld/Actie gearchiveerd')
    assert capsys.readouterr().out == ("called update_status_from_actiereg with args: ('soort id',"
                                       " 'arch')\n")


def test_maak_rel(monkeypatch, capsys):
    """unittest for views.maak_rel
    """
    def mock_set_relation(*args):
        """stub
        """
        print('called set_relation with args:', args)
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'set_relation', mock_set_relation)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.maak_rel('request', 'proj') == '/docs/proj///'
    assert capsys.readouterr().out == "called set_relation with args: (' ', '', ' ', '')\n"
    assert views.maak_rel('request', 'proj', 'srt', 'id') == '/docs/proj/srt/id/'
    assert capsys.readouterr().out == "called set_relation with args: ('srt id', 'srt', ' ', '')\n"
    assert views.maak_rel('request', 'proj', 'srt', 'id', 'soort', 'verw', 'naar') == (
            '/docs/proj/soort/verw/')
    assert capsys.readouterr().out == ("called set_relation with args: ('srt id', 'srt',"
                                       " 'soort verw', 'soort')\n")
    assert views.maak_rel('request', '', 'srt', 'id', 'soort', 'verw', 'naar') == (
            '/docs/soort/verw/')
    assert capsys.readouterr().out == ("called set_relation with args: ('srt id', 'srt',"
                                       " 'soort verw', 'soort')\n")


def test_unrelate(monkeypatch, capsys):
    """unittest for views.unrelate
    """
    def mock_remove_relation(*args):
        """stub
        """
        print('called remove_relation with args:', args)
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'remove_relation', mock_remove_relation)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.unrelate('request', 'proj') == '/docs/proj///'
    assert capsys.readouterr().out == "called remove_relation with args: (' ', '', ' ', '')\n"
    assert views.unrelate('request', 'proj', 'srt', 'id') == '/docs/proj/srt/id/'
    assert capsys.readouterr().out == ("called remove_relation with args: ('srt id', 'srt', ' ',"
                                       " '')\n")
    assert views.unrelate('request', 'proj', 'srt', 'id', 'soort', 'verw', 'naar') == (
            '/docs/proj/soort/verw/')
    assert capsys.readouterr().out == ("called remove_relation with args: ('srt id', 'srt',"
                                       " 'soort verw', 'soort')\n")
    assert views.unrelate('request', '', 'srt', 'id', 'soort', 'verw', 'naar') == (
            '/docs/soort/verw/')
    assert capsys.readouterr().out == ("called remove_relation with args: ('srt id', 'srt',"
                                       " 'soort verw', 'soort')\n")


def test_edit_sub(monkeypatch, capsys):
    """unittest for views.edit_sub
    """
    def mock_update_subitem(*args):
        """stub
        """
        print('called update_subitem with args:', args)
    req = MockRequest()
    req.POST = {}
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'update_subitem', mock_update_subitem)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.edit_sub(req) == '/docs///edit/'
    assert capsys.readouterr().out == ("called update_subitem with args: ('', ' ', '', 'new  ', "
                                       "True, {})\n")
    assert views.edit_sub(req, 'proj', 'srt1', 'id1', 'srt2', 'id2') == '/docs/proj/srt1/id1/edit/'
    assert capsys.readouterr().out == ("called update_subitem with args: ('srt1', 'srt1 id1',"
                                       " 'srt2', 'srt2 id2', False, {})\n")
    req = MockRequest()
    req.POST = {'x': 'y'}
    assert views.edit_sub(req, 'proj', 'srt1', 'id1', 'srt2', 'id2') == '/docs/proj/srt1/id1/edit/'
    assert capsys.readouterr().out == ("called update_subitem with args: ('srt1', 'srt1 id1',"
                                       " 'srt2', 'srt2 id2', False, {'x': 'y'})\n")


def test_viewdoc(monkeypatch):
    """unittest for views.viewdoc
    """
    monkeypatch.setattr(views, 'render', lambda x, y, z: (x, y, z))
    request = MockRequest()
    request.path = "domain_name/files/filename"
    assert views.viewdoc(request) == (request, views.MEDIA_ROOT + 'filename', {})
