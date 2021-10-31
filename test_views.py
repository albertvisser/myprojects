import os
import types
import pytest

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myprojects.settings")
django.setup()

import myprojects.views as views

class MockRequest(django.http.request.HttpRequest):
    pass


def test_index(monkeypatch):
    class MockQuerySet:
        data = [{'naam': 'y'}, {'naam': 'x'}]
        def order_by(self, key):
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
    class MockQuerySet1:
        data = ['item 1', 'item 2']
        def __iter__(self):
            return (x for x in self.data)
        def count(self):
            return len(self.data)
    class MockQuerySet2:
        data = []
        def __iter__(self):
            return (x for x in self.data)
        def count(self):
            return len(self.data)
    def mock_get_attrs(*args):
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
    assert response[2] == {'id': '', 'lijstitem': 'name', 'lijstvan': 'plural', 'meld': '', 'notnw': 'new',
                           'orient': 'naar', 'proj': 1, 'projecten': [{'naam': 'x'}, {'naam': 'y'}],
                           'ref': ('', 'plural', ''), 'sctn': 'section', 'soort': '', 'srt': '',
                           'title': 'title'}
    assert [x for x in lijst] == ['item 1', 'item 2']

    monkeypatch.setattr(views.funcs, 'get_ordered_objectlist', lambda x, y: MockQuerySet2())
    response = views.lijst(request, 1)
    lijst = response[2].pop('lijst')
    assert response[2] == {'id': '', 'lijstitem': 'name', 'lijstvan': 'plural',
                           'meld': 'Geen plural aanwezig bij dit project', 'notnw': 'new',
                           'orient': 'naar', 'proj': 1, 'projecten': [{'naam': 'x'}, {'naam': 'y'}],
                           'ref': ('', 'plural', ''), 'sctn': 'section', 'soort': '', 'srt': '',
                           'title': 'title'}
    assert [x for x in lijst] == []

    monkeypatch.setattr(views.funcs, 'get_ordered_objectlist', lambda x, y: MockQuerySet1())
    response = views.lijst(request, 1, 'soort', 'id', 'from', 'srt')
    lijst = response[2].pop('lijst')
    assert response[2] == {'id': 'id', 'lijstitem': 'name', 'lijstvan': 'plural', 'meld': '', 'notnw': 'new',
                           'orient': 'van', 'proj': 1, 'projecten': [{'naam': 'x'}, {'naam': 'y'}],
                           'ref': ('srt', 'plural', 'id'), 'sctn': 'section', 'soort': 'soort', 'srt': 'srt',
                           'start': 'x', 'title': 'title'}
    assert [x for x in lijst] == ['item 1', 'item 2']


def test_new_project(monkeypatch, capsys):
    def mock_view_project(*args, **kwargs):
        return 'called view_project with args {} and kwargs {}'.format(args, kwargs)
    monkeypatch.setattr(views, 'view_project', mock_view_project)
    assert views.new_project('request') == ("called view_project with args ('request',)"
                                            " and kwargs {'edit': 'new'}")


def test_add_new_proj(monkeypatch, capsys):
    def mock_update_project(*args, **kwargs):
        return 'called update_project with args {} and kwargs {}'.format(args, kwargs)
    monkeypatch.setattr(views, 'update_project', mock_update_project)
    assert views.add_new_proj('request') == ("called update_project with args ('request',)"
                                             " and kwargs {'proj': 'proj'}")


def test_view_project(monkeypatch, capsys):
    def mock_init_infodict(*args):
        return {'arg{}'.format(i): x for i, x in enumerate(args)}
    def mock_get_margins(*args):
        return 'x', 'y', 'z'
    def mock_get_update_url(*args):
        return '/{}/{}/'.format(*args)
    def mock_get_fieldlengths(*args):
        return 'q'
    def mock_get_object(srt, id):
        obj = types.SimpleNamespace(soort=srt, id=id)
        obj.actiereg = 'arproj'
        obj.aruser = 'aruser'
        return obj
    def mock_get_detail_title(*args):
        obj ='{} {}'.format(args[2].soort, args[2].id) if args[2] is not None else 'None'
        title = 'title for (`{}`, `{}`, `{}`)'.format(args[0], args[1], obj)
        return title
    def mock_get_stats_texts(*args):
        return 'stats_text for {}'.format(args)
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
    data = response[2].pop('data')
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'arg0': '',
                           'arg1': 'project', 'arg2': '', 'arg3': '',
                           'form_addr': '///', 'leftw': 'x', 'lengte': 'q',
                           'prob_stats': "stats_text for ('', 'probleem')", 'rightm': 'z',
                           'rightw': 'y', 'test_stats': "stats_text for ('', 'bevinding')",
                           'title': 'title for (`project`, ``, `project `)',
                           'wijz_stats': "stats_text for ('', 'userwijz')"}
    assert '{} {}'.format(data.soort, data.id) == 'project '

    response = views.view_project('request', 'proj', 'new', 'meld')
    assert response[2] == {'arg0': 'proj', 'arg1': 'project', 'arg2': 'new', 'arg3': 'meld',
                           'form_addr': '/proj/new/', 'leftw': 'x', 'lengte': 'q',
                           'rightm': 'z', 'rightw': 'y',
                           'title': 'title for (`project`, `new`, `None`)'}

    response = views.view_project('request', 'proj', 'edit', 'meld')
    data = response[2].pop('data')
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'arg0': 'proj',
                           'arg1': 'project', 'arg2': 'edit', 'arg3': 'meld',
                           'form_addr': '/proj/edit/', 'leftw': 'x', 'lengte': 'q',
                           'rightm': 'z', 'rightw': 'y',
                           'title': 'title for (`project`, `edit`, `project proj`)'}
    assert '{} {}'.format(data.soort, data.id) == 'project proj'


def test_edit_project(monkeypatch, capsys):
    def mock_view_project(*args):
        return 'called view_project with args {}'.format(args)
    monkeypatch.setattr(views, 'view_project', mock_view_project)
    assert views.edit_project('request', 'proj') == ("called view_project with args ('request',"
                                                     " 'proj', 'edit')")


def test_update_project(monkeypatch, capsys):
    def mock_get_object(srt, id, new=False):
        obj = types.SimpleNamespace(soort=srt)
        obj.id = 'new_id' if new else id
        obj.actiereg = '' if new else '1'
        return obj
    def mock_execute_update(*args):
        print('called execute_update with args {} `{} {}` {}'.format(args[0],
                                                                     args[1].soort, args[1].id,
                                                                     args[2]))
    def mock_get_object_2(srt, id, new=False):
        obj = types.SimpleNamespace(soort=srt, id=1, kort='kort', actiereg = '')
        return obj
    def mock_execute_update_2(project, p, postdict):
        p.actiereg = 1
        print('called execute_update with args {} `{} {}` {}'.format(project, p.soort, p.id,
                                                                     postdict))
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'execute_update', mock_execute_update)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    req = MockRequest()
    req.POST = 'postdict'
    assert views.update_project(req, 'proj') == '/new_id/'
    assert capsys.readouterr().out == ('called execute_update with args project `project new_id` '
                                       'postdict\n')
    assert views.update_project(req, 1) == '/1/'
    assert capsys.readouterr().out == ('called execute_update with args project `project 1` '
                                       'postdict\n')
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object_2)
    monkeypatch.setattr(views.funcs, 'execute_update', mock_execute_update_2)
    assert views.update_project(req, 1) == 'http://actiereg.lemoncurry.nl/addext/1/1/kort/'
    assert capsys.readouterr().out == ('called execute_update with args project `project 1` '
                                       'postdict\n')


def test_view_document(monkeypatch, capsys):
    def mock_init_infodict(*args):
        return {'arg{}'.format(i): x for i, x in enumerate(args)}
    def mock_get_margins(*args):
        return 'x', 'y', 'z'
    def mock_get_fieldlengths(*args):
        return 'q'
    def mock_get_update_url(*args):
        return '/{}/{}/{}/{}/{}/'.format(*args)
    def mock_get_object(srt, id):
        obj = types.SimpleNamespace(soort=srt, id=id)
        if srt == 'project':
            obj.naam = 'projectnaam'
            obj.actiereg = 'arproj'
            obj.aruser = 'aruser'
        return obj
    def mock_get_objectlist(proj, soort):
        return 'prev_item', 'this_item', 'next_item'
    def mock_determine_adjacent(*args):
        return args[0][0], args[0][2]
    class MockGetRelations:
        def __init__(self, obj, soort):
            self.obj = obj
            self.soort = soort
        def get_foreignkeys_to(self):
            return 'foreignkeys to {} {}'.format(self.soort, self.obj.id)
        def get_many2many_to(self):
            return 'many to many relations to {} {}'.format(self.soort, self.obj.id)
        def get_foreignkeys_from(self):
            return (['fkey buttons'], 'foreignkeys from {} {}'.format(self.soort, self.obj.id),
                     'andere fkeys', 'fkey attrs')
        def get_many2many_from(self):
            return ['m2m buttons'], 'm2m relations from {} {}'.format(self.soort, self.obj.id)
    def mock_get_relation_buttons(*args):
        return 'relation buttons for {}'.format(args)
    def mock_get_new_numberkey(proj, soort):
        return 'new_numberkey'
    def mock_get_detail_title(*args):
        obj ='{} {}'.format(args[2].soort, args[2].id) if args[2] is not None else 'None'
        title = 'title for (`{}`, `{}`, `{}`)'.format(args[0], args[1], obj)
        return title
    def mock_get_names_for_type(soort):
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
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'arg0': 'proj',
                           'arg1': '', 'arg2': '', 'arg3': 'melding', 'form_addr': '/proj/////',
                           'leftw': 'x', 'lengte': 'q', 'lijst': '', 'lijstvan': 'soort_mv',
                           'nummer': 'new_numberkey', 'rightm': 'z', 'rightw': 'y',
                           'sctn': 'sectnaam',
                           'title': 'Project projectnaam - title for (``, ``, `None`)'}
    response = views.view_document('request', 'proj', 'view', 'soort', 'id')
    assert response[0] == 'request'
    assert response[1] == 'soort.html'
    data = response[2].pop('data')
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'arg0': 'proj',
                           'arg1': 'soort', 'arg2': 'view', 'arg3': '',
                           'form_addr': '/proj/view/soort///',
                           'leftw': 'x', 'lengte': 'q', 'lijst': 'soort', 'lijstvan': 'soort_mv',
                           'rightm': 'z', 'rightw': 'y',
                           'sctn': 'sectnaam', 'sect': 'soort/id',
                           'title': 'Project projectnaam - title for (`soort`, `view`, `soort id`)',
                           'andere': 'andere fkeys', 'attrs': 'fkey attrs',
                           'buttons': "relation buttons for ('proj', 'soort', 'id', "
                           "['fkey buttons', 'm2m buttons'])",
                           'fkeys_from': 'foreignkeys from soort id',
                           'fkeys_to': 'foreignkeys to soort id',
                           'm2ms_from': 'm2m relations from soort id',
                           'm2ms_to': 'many to many relations to soort id',
                           'next': 'next_item', 'prev': 'prev_item'}
    assert data.id, data.soort == ('id', 'soort')
    response = views.view_document('request', 'proj', 'view', 'soort', 'id', 'srt', 'ref')
    assert response[0] == 'request'
    assert response[1] == 'soort.html'
    data = response[2].pop('data')
    assert response[2] == {'ar_proj': 'arproj', 'ar_user': 'aruser', 'arg0': 'proj',
                           'arg1': 'soort', 'arg2': 'view', 'arg3': '',
                           'form_addr': '/proj/view/soort/srt/ref/',
                           'leftw': 'x', 'lengte': 'q',
                           'rightm': 'z', 'rightw': 'y',
                           'sctn': 'sectnaam', 'sect': 'soort/id',
                           'title': 'Project projectnaam - title for (`soort`, `view`, `soort id`)',
                           'andere': 'andere fkeys', 'attrs': 'fkey attrs',
                           'buttons': "relation buttons for ('proj', 'soort', 'id', "
                           "['fkey buttons', 'm2m buttons'])",
                           'fkeys_from': 'foreignkeys from soort id',
                           'fkeys_to': 'foreignkeys to soort id',
                           'm2ms_from': 'm2m relations from soort id',
                           'm2ms_to': 'many to many relations to soort id',
                           'next': 'next_item', 'prev': 'prev_item',
                           'ref': ('soort', 'soort_mv', 'ref')}
    assert data.id, data.soort == ('id', 'soort')


def test_new_document(monkeypatch, capsys):
    def mock_view_document(*args, **kwargs):
        return 'called view_document with args {}'.format(args)
    monkeypatch.setattr(views, 'view_document', mock_view_document)
    assert views.new_document('request', 'proj', 'soort') == (
            "called view_document with args ('request', 'proj', 'new', 'soort')")


def test_new_from_relation(monkeypatch, capsys):
    def mock_view_document(*args, **kwargs):
        return 'called view_document with args {} and kwargs {}'.format(args, kwargs)
    monkeypatch.setattr(views, 'view_document', mock_view_document)
    assert views.new_from_relation('request', 'proj', 'soort', 'srt', 'verw') == (
            "called view_document with args ('request', 'proj', 'new', 'soort')"
            " and kwargs {'srt': 'srt', 'verw': 'verw'}")


def test_edit_document(monkeypatch, capsys):
    def mock_view_document(*args, **kwargs):
        return 'called view_document with args {}'.format(args)
    monkeypatch.setattr(views, 'view_document', mock_view_document)
    assert views.edit_document('request', 'proj', 'soort', 'id') == (
            "called view_document with args ('request', 'proj', 'edit', 'soort', 'id')")


def mock_get_object(srt, id, new=False):
    obj = "new " if new else ''
    return '{}{} {}'.format(obj, srt, id)


def test_update_document(monkeypatch, capsys):
    def mock_get_object(srt, id, new=False):
        import types
        obj = types.SimpleNamespace(soort=srt)
        obj.id = 0 if new else id
        return obj
    def mock_execute_update(*args):
        print('called execute_update with args {} `{} {}` {} {}'.format(args[0],
                                                                        args[1].soort, args[1].id,
                                                                        args[2], args[3]))
    def mock_update_related(*args):
        print('called update_related with args {} `{} {}` {} {}'.format(args[0],
                                                                        args[1].soort, args[1].id,
                                                                        args[2], args[3]))
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'execute_update', mock_execute_update)
    monkeypatch.setattr(views.funcs, 'update_related', mock_update_related)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    req = MockRequest()
    req.POST = 'postdict'
    req.FILES = 'filesdict'
    assert views.update_document(req) == '//0/'
    assert capsys.readouterr().out == ('called execute_update with args  ` 0` postdict filesdict\n'
                                       'called update_related with args  ` 0`  \n')
    assert views.update_document(req, 'proj', 'soort') == '/proj/soort/0/'
    assert capsys.readouterr().out == ('called execute_update with args soort `soort 0` '
                                       'postdict filesdict\n'
                                       'called update_related with args soort `soort 0`  \n')
    assert views.update_document(req, 'proj', 'soort', 'id') == '/proj/soort/id/'
    assert capsys.readouterr().out == ('called execute_update with args soort `soort id` '
                                        'postdict filesdict\n'
                                       'called update_related with args soort `soort id`  \n')
    assert views.update_document(req, 'proj', 'soort', 'id', 'srt', 'verw') == '/proj/soort/id/'
    assert capsys.readouterr().out == ('called execute_update with args soort `soort id` '
                                       'postdict filesdict\n'
                                       'called update_related with args soort `soort id` srt '
                                       'verw\n')


def test_koppel(monkeypatch, capsys):
    def mock_update_link(*args):
        print('called update_link_from_actiereg with args: {}'.format(args))
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'update_link_from_actiereg', mock_update_link)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.koppel('request') == '////msg//'
    assert capsys.readouterr().out == ''
    assert views.koppel('request', 'proj', 'soort', 'id') == '/proj/soort/id/msg//'
    assert capsys.readouterr().out == ''
    assert views.koppel('request', 'proj', 'soort', 'id', 'arid', 'arnum') == '/proj/soort/id/'
    assert capsys.readouterr().out == ("called update_link_from_actiereg with args:"
                                       " ('soort id', 'arid', 'arnum')\n")
    assert views.koppel('request', 'pr', 'srt', 'id', arnum='arnum') == '/pr/srt/id/msg/arnum/'
    assert capsys.readouterr().out == ''


def test_meld(monkeypatch, capsys):
    def mock_update_status(*args):
        print('called update_status_from_actiereg with args: {}'.format(args))
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
    def mock_set_relation(*args):
        print('called set_relation with args: {}'.format(args))
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'set_relation', mock_set_relation)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.maak_rel('request', 'proj') == '/proj///'
    assert capsys.readouterr().out ==  "called set_relation with args: (' ', '', ' ', '')\n"
    assert views.maak_rel('request', 'proj', 'srt', 'id') == '/proj/srt/id/'
    assert capsys.readouterr().out ==  "called set_relation with args: ('srt id', 'srt', ' ', '')\n"
    assert views.maak_rel('request', 'proj', 'srt', 'id', 'soort', 'verw', 'naar') == (
            '/proj/soort/verw/')
    assert capsys.readouterr().out == ("called set_relation with args: ('srt id', 'srt',"
                                       " 'soort verw', 'soort')\n")
    assert views.maak_rel('request', '', 'srt', 'id', 'soort', 'verw', 'naar') == (
            '/soort/verw/')
    assert capsys.readouterr().out == ("called set_relation with args: ('srt id', 'srt',"
                                       " 'soort verw', 'soort')\n")


def test_unrelate(monkeypatch, capsys):
    def mock_remove_relation(*args):
        print('called remove_relation with args: {}'.format(args))
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'remove_relation', mock_remove_relation)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.unrelate('request', 'proj') == '/proj///'
    assert capsys.readouterr().out == "called remove_relation with args: (' ', '', ' ', '')\n"
    assert views.unrelate('request', 'proj', 'srt', 'id') == '/proj/srt/id/'
    assert capsys.readouterr().out == ("called remove_relation with args: ('srt id', 'srt', ' ',"
                                       " '')\n")
    assert views.unrelate('request', 'proj', 'srt', 'id', 'soort', 'verw', 'naar') == (
            '/proj/soort/verw/')
    assert capsys.readouterr().out == ("called remove_relation with args: ('srt id', 'srt',"
                                       " 'soort verw', 'soort')\n")
    assert views.unrelate('request', '', 'srt', 'id', 'soort', 'verw', 'naar') == (
            '/soort/verw/')
    assert capsys.readouterr().out == ("called remove_relation with args: ('srt id', 'srt',"
                                       " 'soort verw', 'soort')\n")


def test_edit_sub(monkeypatch, capsys):
    def mock_update_subitem(*args):
        print('called update_subitem with args: {}'.format(args))
    req = MockRequest()
    req.POST = {}
    monkeypatch.setattr(views.funcs, 'get_object', mock_get_object)
    monkeypatch.setattr(views.funcs, 'update_subitem', mock_update_subitem)
    monkeypatch.setattr(views, 'HttpResponseRedirect', lambda x: x)
    assert views.edit_sub(req) == '///edit/'
    assert capsys.readouterr().out == ("called update_subitem with args: ('', ' ', '', 'new  ', "
                                       "True, {})\n")
    assert views.edit_sub(req, 'proj', 'srt1', 'id1', 'srt2', 'id2') == '/proj/srt1/id1/edit/'
    assert capsys.readouterr().out == ("called update_subitem with args: ('srt1', 'srt1 id1',"
                                       " 'srt2', 'srt2 id2', False, {})\n")
    req = MockRequest()
    req.POST = {'x': 'y'}
    assert views.edit_sub(req, 'proj', 'srt1', 'id1', 'srt2', 'id2') == '/proj/srt1/id1/edit/'
    assert capsys.readouterr().out == ("called update_subitem with args: ('srt1', 'srt1 id1',"
                                       " 'srt2', 'srt2 id2', False, {'x': 'y'})\n")


def test_viewdoc(monkeypatch):
    monkeypatch.setattr(views, 'render', lambda x, y, z: (x, y, z))
    request = MockRequest()
    request.path = "domain_name/files/filename"
    assert views.viewdoc(request) == (request, views.MEDIA_ROOT + 'filename', {})
