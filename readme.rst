===========
My Projects
===========

This is the web framework version of a software documentation system I once built
using Python and plain CGI communication (`DocTool </albertvisser/doctool/>`_).

It consists of four parts: user specification, functional design, technical design
and realisation, and testing - five parts: user specification, functional design,
technical design, realisation, and testing; and a main section holding the
various projects that the other stuff belongs to - six parts, "and an almost
fanatical dedication to the pope".

Except for the project section which contains only the project definitions,
each part is subdivided according to the type of documents involved. For
each type, a list of documents can be created and each document can of course be
individually viewed or edited.

The power of this system lies in the interrelation between documents of different
categories and the fact that when you define a relation one way, the other way is
automatically created as well.
For now, the kinds of relations that are possible are predefined -
a newer version of this app might have these configurable (Then again, I might
also make the types of documents in the various sections configurable - this is
only a reflection of the ideas about this stuff a couple of years ago)

A further feature is that this app can be used as the portal to my ticketing system
`ActieReg </albertvisser/actiereg/>`_. As such, you can do the intake here and only move
activities to the other system when they are actually going to be worked on.


Usage
-----

Use manage.py or the provided fcgi or wsgi script to start the django app, and
configure your web server to communicate with it (see the examples included).


Requirements
------------

- Python
- Django
