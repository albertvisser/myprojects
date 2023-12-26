"""Fixtures for Myprojects unittests
"""
import pytest
import pathlib


@pytest.fixture
def expected_relations():
    """geeft per relatie tussen twee entiteit typen het attribuut terug waarmee de gerelateerde
    objecten kunnen worden uitgevraagd, alsmede de soort relatie (multiple of niet)

    voornamelijk bedoeld om te controleren of een en ander goed blijft werken wanneer code wordt
    aangepast in verband met een Django update
    """
    reldict = {('project', 'userspec'): ('specs', False),
               ('project', 'userdoc'): ('docs', False),
               ('project', 'userwijz'): ('rfcs', False),
               ('project', 'userprob'): ('probs', False),
               ('project', 'funcdoc'): ('fdocs', False),
               ('project', 'gebrtaak'): ('gtaken', False),
               ('project', 'funcproc'): ('fprocs', False),
               ('project', 'entiteit'): ('fdata', False),
               ('project', 'attribuut'): (None, None),
               ('project', 'techtaak'): ('ttask', False),
               ('project', 'techproc'): ('tproc', False),
               ('project', 'dataitem'): ('tdata', False),
               ('project', 'element'): (None, None),
               ('project', 'layout'): ('layout', False),
               ('project', 'programma'): ('pproc', False),
               ('project', 'testplan'): ('tplan', False),
               ('project', 'testcase'): ('tcase', False),
               ('project', 'bevinding'): ('tbev', False),
               ('userspec', 'project'): ('project', False),
               ('userspec', 'gebrtaak'): ('gtaken', False),
               ('userspec', 'funcproc'): ('fprocs', False),
               ('userdoc', 'project'): ('project', False),
               ('userwijz', 'project'): ('project', False),
               ('userwijz', 'gebrtaak'): ('gtaken', True),
               ('userwijz', 'funcproc'): ('fprocs', True),
               ('userwijz', 'entiteit'): ('fdata', True),
               ('userprob', 'project'): ('project', False),
               ('funcdoc', 'project'): ('project', False),
               ('gebrtaak', 'project'): ('project', False),
               ('gebrtaak', 'userspec'): ('spec', False),
               ('gebrtaak', 'userwijz'): ('rfc', True),
               ('gebrtaak', 'funcproc'): ('fprocs', True),
               ('gebrtaak', 'techtaak'): ('ttask', False),
               ('gebrtaak', 'layout'): ('layout', True),
               ('gebrtaak', 'testplan'): ('tplan', True),
               ('funcproc', 'project'): ('project', False),
               ('funcproc', 'userspec'): ('spec', False),
               ('funcproc', 'userwijz'): ('rfc', True),
               ('funcproc', 'gebrtaak'): ('gt', True),
               ('funcproc', 'funcproc'): ('used_by', True),
               ('funcproc', 'entiteit'): ('fdata', True),
               ('funcproc', 'techproc'): ('tproc', True),
               ('funcproc', 'testplan'): ('tplan', True),
               ('entiteit', 'project'): ('project', False),
               ('entiteit', 'userwijz'): ('rfc', True),
               ('entiteit', 'funcproc'): ('fp', True),
               ('entiteit', 'attribuut'): ('attrs', False),
               ('entiteit', 'dataitem'): ('tdata', True),
               ('entiteit', 'testplan'): ('tplan', True),
               ('attribuut', 'entiteit'): ('hoort_bij', False),
               ('techtaak', 'project'): ('project', False),
               ('techtaak', 'gebrtaak'): ('gt', False),
               ('techtaak', 'techproc'): ('tproc', True),
               ('techproc', 'project'): ('project', False),
               ('techproc', 'funcproc'): ('fp', True),
               ('techproc', 'techtaak'): ('tt', True),
               ('techproc', 'techproc'): ('used_by', True),
               ('techproc', 'dataitem'): ('tdata', True),
               ('techproc', 'layout'): ('layout', True),
               ('techproc', 'programma'): ('pproc', True),
               ('dataitem', 'project'): ('project', False),
               ('dataitem', 'entiteit'): ('ent', True),
               ('dataitem', 'techproc'): ('tp', True),
               ('element', 'dataitem'): ('hoort_bij', False),
               ('layout', 'project'): ('project', False),
               ('layout', 'gebrtaak'): ('gt', True),
               ('layout', 'techproc'): ('tp', True),
               ('programma', 'project'): ('project', False),
               ('programma', 'techproc'): ('tp', True),
               ('testplan', 'project'): ('project', False),
               ('testplan', 'gebrtaak'): ('gt', True),
               ('testplan', 'funcproc'): ('fp', True),
               ('testplan', 'entiteit'): ('ent', True),
               ('testplan', 'testcase'): ('tcase', True),
               ('testplan', 'bevinding'): ('tbev', True),
               ('testcase', 'project'): ('project', False),
               ('testcase', 'testplan'): ('tplan', True),
               ('bevinding', 'project'): ('project', False),
               ('bevinding', 'testplan'): ('tplan', True)}
    return reldict


@pytest.fixture
def expected_field_attrs():
    attrdict = {'project': [('naam', 'Char', 40), ('kort', 'Char', 80), ('oms', 'Text', None),
                            ('start', 'Char', 80), ('fysloc', 'Char', 80), ('actiereg', 'Char', 40),
                            ('aruser', 'Char', 40), ('status', 'Text', None)],
                'userspec': [('naam', 'Char', 40), ('kort', 'Char', 80), ('functie', 'Text', None),
                             ('beeld', 'Text', None), ('product', 'Text', None),
                             ('baten', 'Char', 80), ('kosten', 'Char', 80),
                             ('opmerkingen', 'Text', None)],
                'userdoc': [('naam', 'Char', 40), ('oms', 'Char', 80), ('link', 'File', 100),
                            ('tekst', 'Text', None)],
                'userwijz': [('nummer', 'Char', 10), ('datum_in', 'DateTime', None),
                             ('gereed', 'Boolean', None), ('datum_gereed', 'DateTime', None),
                             ('wens', 'Char', 80), ('toelichting', 'Text', None),
                             ('opmerkingen', 'Text', None), ('actie', 'Integer', None),
                             ('actienummer', 'Char', 10)],
                'userprob': [('nummer', 'Char', 10), ('datum_in', 'DateTime', None),
                             ('gereed', 'Boolean', None), ('datum_gereed', 'DateTime', None),
                             ('kort', 'Char', 80), ('melding', 'Text', None),
                             ('oplossing', 'Text', None), ('actie', 'Integer', None),
                             ('actienummer', 'Char', 10)],
                'funcdoc': [('naam', 'Char', 40), ('oms', 'Char', 80), ('link', 'File', 100),
                            ('tekst', 'Text', None)],
                'gebrtaak': [('naam', 'Char', 40), ('doel', 'Char', 80), ('wanneer', 'Text', None),
                             ('wie', 'Text', None), ('condities', 'Text', None),
                             ('waarvoor', 'Text', None), ('beschrijving', 'Text', None)],
                'funcproc': [('naam', 'Char', 40), ('doel', 'Char', 80), ('invoer', 'Text', None),
                             ('uitvoer', 'Text', None), ('beschrijving', 'Text', None) ],
                'entiteit': [('naam', 'Char', 40), ('kort', 'Char', 80), ('functie', 'Text', None),
                             ('levensloop', 'Text', None)],
                'attribuut': [('naam', 'Char', 40), ('type', 'Char', 10), ('bereik', 'Text', None),
                              ('primarykey', 'PositiveSmallInteger', None)],
                'techtaak': [('naam', 'Char', 40), ('kort', 'Char', 80), ('doel', 'Text', None),
                             ('periode', 'Text', None), ('verloop', 'Text', None)],
                'techproc': [('naam', 'Char', 40), ('doel', 'Char', 80), ('invoer', 'Text', None),
                             ('uitvoer', 'Text', None), ('beschrijving', 'Text', None),
                             ('omgeving', 'Text', None)],
                'dataitem': [('naam', 'Char', 40), ('functie', 'Char', 80),
                             ('levensloop', 'Text', None)],
                'element': [('naam', 'Char', 40), ('omschrijving', 'Char', 80),
                            ('soort', 'Char', 40), ('sleutel', 'PositiveSmallInteger', None)],
                'layout': [('naam', 'Char', 40), ('kort', 'Char', 80), ('data', 'Text', None),
                           ('link', 'File', 100)],
                'programma': [('naam', 'Char', 40), ('doel', 'Char', 80), ('invoer', 'Text', None),
                              ('uitvoer', 'Text', None), ('werkwijze', 'Text', None),
                              ('bijzonder', 'Text', None), ('hoetetesten', 'Text', None),
                              ('testgevallen', 'Text', None)],
                'testplan': [('naam', 'Char', 40), ('oms', 'Char', 80), ('tekst', 'Text', None)],
                'testcase': [('naam', 'Char', 40), ('oms', 'Char', 80), ('tekst', 'Text', None)],
                'bevinding': [('nummer', 'Char', 10), ('datum_in', 'DateTime', None),
                              ('gereed', 'Boolean', None), ('datum_gereed', 'DateTime', None),
                              ('kort', 'Char', 80), ('melding', 'Text', None),
                              ('oplossing', 'Text', None), ('actie', 'Integer', None),
                              ('actienummer', 'Char', 10)]}
    return attrdict


@pytest.fixture
def expected_stats_texts():
    return {(28, 'bevinding'): (7, 'waarvan 7 opgelost en 0 doorgekoppeld naar Actiereg'),
            (28, 'probleem'): (3, 'waarvan 2 opgelost en 1 doorgekoppeld naar Actiereg'),
            (28, 'userwijz'): (5, 'waarvan 4 gerealiseerd en 1 in behandeling via Actiereg'),
            (29, 'bevinding'): ('(nog) geen', 'opgevoerd'),
            (29, 'probleem'): ('(nog) geen', 'gemeld'),
            (29, 'userwijz'): ('(nog) geen', 'ingediend')}


@pytest.fixture
def expected_names_for_type():
    return {'project': ('project', 'projecten', ''),
            'userspec': ('gebruikersspecificatie', 'gebruikersspecificaties', 'user'),
            'userdoc': ('naslagdocument', 'naslagdocumenten', 'user'),
            'userwijz': ('aanvraag wijziging', 'aanvraag wijzigingen', 'user'),
            'userprob': ('incident/probleem', 'incidenten/problemen', 'user'),
            'funcdoc': ('functioneel document', 'functionele documenten', 'func'),
            'gebrtaak': ('gebruikerstaak', 'gebruikerstaken', 'func'),
            'funcproc': ('functioneel proces', 'functionele processen', 'func'),
            'entiteit': ('entiteit', 'entiteiten', 'func'),
            'attribuut': ('attribuut', 'attributen', 'func'),
            'techtaak': ('systeemtaak', 'systeemtaken', 'tech'),
            'techproc': ('technisch proces', 'technische processen', 'tech'),
            'dataitem': ('data-item', 'data-items', 'tech'),
            'element': ('data-element', 'data-elementen', 'tech'),
            'layout': ('layout', 'layouts', 'tech'),
            'programma': ('programmabeschrijving', 'programmabeschrijvingen', 'tech'),
            'testplan': ('testplan', 'testplannen', 'test'),
            'testcase': ('testgeval', 'testgevallen', 'test'),
            'bevinding': ('bevinding', 'bevindingen', 'test')}


@pytest.fixture
def prepare_uploadfile():
    "make sure file does not exist before (and after) executing test"
    def prepfunc(fname):
        filepath = pathlib.Path('/home/albert/projects/myprojects/files/{fname}')
        filepath.unlink(missing_ok=True)
    return prepfunc
