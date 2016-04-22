Essential Scheduler
===================

A Django calendar app.
This is a fork of llazzaro's [django-scheduler](https://github.com/llazzaro/django-scheduler)

Installation
============

download (e.g. git clone) into your project directory as just another app.

add to `INSTALLED_APPS`:

```python
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
