<<<<<<< HEAD
Essential Scheduler
===================

A Django calendar app.
This is a fork of llazzaro's [django-scheduler](https://github.com/llazzaro/django-scheduler)

Installation
============

download (e.g. git clone) into your project directory as just another app.
=======
Django Scheduler
========

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/llazzaro/django-scheduler?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[<img src="https://img.shields.io/travis/llazzaro/django-scheduler.svg">](https://travis-ci.org/llazzaro/django-scheduler)
[![Code Health](https://landscape.io/github/llazzaro/django-scheduler/master/landscape.svg?style=flat)](https://landscape.io/github/llazzaro/django-scheduler/master)
[<img src="https://img.shields.io/coveralls/llazzaro/django-scheduler.svg">](https://coveralls.io/r/llazzaro/django-scheduler)
[<img src="https://img.shields.io/pypi/v/django-scheduler.svg">](https://pypi.python.org/pypi/django-scheduler)
[<img src="https://pypip.in/d/django-scheduler/badge.png">](https://pypi.python.org/pypi/django-scheduler)
[<img src="https://pypip.in/license/django-scheduler/badge.png">](https://github.com/llazzaro/django-scheduler/blob/master/LICENSE.txt)


A calendar app for Django

Donate bitcoins to this project.

        BTC: 13BeXBBjM3PPtp8YvKFvgfXdqgZC19YX23


Information
========

* [Documentation](http://django-scheduler.readthedocs.org/en/latest/)
* [Wiki](https://github.com/llazzaro/django-scheduler/wiki)
* [Sample Project](https://github.com/llazzaro/django-scheduler-sample)


Installation
========

```bash
npm install -g bower
pip install django-scheduler
```

edit your `settings.py`
>>>>>>> 83706182c8f65960d833999053d214ae45ffaec3

add to `INSTALLED_APPS`:

```python
<<<<<<< HEAD
'scheduler',
```
(If you want to use automatic Occurrence discovery, make sure to add it AFTER any app that wants to use it!)

Usage
=====
 * subclass the Event - Model from scheduler.models (it only saves START and END time!)
 * Access all the functionallity through Event - subclasses (or the Event-Class itself) or their instances.

Theory of Operation
===================
The main feature of this library is to keep track of Events. An Event has a time and exoses methods to allow simple selection of any occurence of the events within a given time range. An Occurrence is an instance of a recurring event (or the only instance of a non-recurring event), which can be manipulated without changing the source Event. (Main purpose: moving, cancelling)

WARNING
=======
Since Event and Occurrences should expose similar functionallity (mainly, the same fields of any subclass), any Event - Subclass is used during the initialisation of essential-scheduler to be REBASED with the Occurrence - Model!
This is HIGHLY experimental! It should NOT be used in production this way! It's mainly implemented for convenience!

In Production, any Event-Subclass should be replicated as Occurrence-Subclass. This Subclass then has to be registered with the BaseEvent class and it's attribute "occurrence_subclasses". Sample-Code:
```python
from scheduler.models import Event, BaseEvent
from scheduler.models.occurrences import Occurrence

class MyEvents(Event):
    title = models.CharField()

class MyEvent_Occurrence(Occurrence):
    title = models.CharField() #has to have same fields as the Event-Subclass!

BaseEvent.occurrence_sublcasses[MyEvent.__name__] = MyEvent_Occurrence
```
If subclasses are defined manually, they ALL have to be defined manually! Defining some and leaving others for autmatic detaction WILL cause errors!
=======
'schedule',
'djangobower',
```

add to `TEMPLATE_CONTEXT_PROCESSORS`:

```python
"django.core.context_processors.request"
```

Add staticfinder to STATICFILES_FINDERS:

```
'djangobower.finders.BowerFinder',
```

Specify path to components root (you need to use absolute path):
```
BOWER_COMPONENTS_ROOT = '/PROJECT_ROOT/components/'
```

Add the following required Bower dependencies for scheduler:

```
BOWER_INSTALLED_APPS = (
    'jquery',
    'bootstrap'
)
```

Last step, install bower dependencies with:

```
./manage.py bower install
```


Features
========

 * one-time and recurring events
 * calendar exceptions (occurrences changed or cancelled)
 * occurrences accessible through Event API and Period API
 * relations of events to generic objects
 * ready to use, nice user interface
 * view day, week, month, three months and year

Configuration
========

Full Calendar examples
======

![Full calendar](https://raw.githubusercontent.com/llazzaro/django-scheduler-sample/master/scheduler.png)

![Monthly view (static)](https://raw.githubusercontent.com/llazzaro/django-scheduler-sample/master/monthly_view.png)

![Daily view (static)](https://raw.githubusercontent.com/llazzaro/django-scheduler-sample/master/daily.png)


Optional Settings
========

### FIRST_DAY_OF_WEEK

This setting determines which day of the week your calendar begins on if your locale doesn't already set it. Default is 0, which is Sunday.

### OCCURRENCE_CANCEL_REDIRECT

This setting controls the behavior of `Views.get_next_url`. If set, all calendar modifications will redirect here (unless there is a `next` set in the request.)

### SHOW_CANCELLED_OCCURRENCES

This setting controls the behavior of `Period.classify_occurence`. If True, then occurences that have been cancelled will be displayed with a css class of canceled, otherwise they won't appear at all.

Defaults to False

### CHECK_PERMISSION_FUNC

_deprecated_

Should be replaced with `CHECK_EVENT_PERM_FUNC`

### CHECK_EVENT_PERM_FUNC

This setting controls the callable used to determine if a user has permission to edit an event or occurrence. The callable must take the object (event) and the user and return a boolean.

Default:
```python
    check_edit_permission(ob, user):
        return user.is_authenticated()
```

If ob is None, then the function is checking for permission to add new events

### CHECK_CALENDAR_PERM_FUNC

This setting controls the callable used to determine if a user has permission to add, update or delete an events in specific calendar. The callable must take the object (calendar) and the user and return a boolean.

Default:
```python
    check_edit_permission(ob, user):
        return user.is_authenticated()
```

### GET_EVENTS_FUNC

This setting controls the callable that gets all events for calendar display. The callable must take the request and the calendar and return a `QuerySet` of events. Modifying this setting allows you to pull events from multiple calendars or to filter events based on permissions

Default:
```python
    get_events(request, calendar):
        return calendar.event_set.all()
```

### SCHEDULER_BASE_CLASSES

This setting allows for custom base classes to be used on all models. Useful for adding fields, managers, or other elements.

Defaults to django.db.models.Model


### SCHEDULER_PREVNEXT_LIMIT_SECONDS

This settings allows to set the upper and lower limit in calendars navigation.
Value is in seconds.

Default (two years):
62208000
>>>>>>> 83706182c8f65960d833999053d214ae45ffaec3
