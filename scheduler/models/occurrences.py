from __future__ import unicode_literals
from django.utils.six import with_metaclass
# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.utils.formats import date_format
from django.utils.encoding import python_2_unicode_compatible

from scheduler.models.utils import get_model_bases, OccurrenceReplacer
from scheduler.models.events import Event, BaseEvent

class RebasingQueryset(models.QuerySet):
    def __getitem__(self, k):
        result = super(RebasingQueryset, self).__getitem__(k)
        if isinstance(result, BaseEvent) :
            return result.as_leaf_class()
        else:
            return result

    def __iter__(self):
        for item in super(RebasingQueryset, self).__iter__():
            yield item.as_leaf_class()

@python_2_unicode_compatible
class Occurrence(with_metaclass(models.base.ModelBase, *get_model_bases())):
    event = models.ForeignKey(Event)
    start = models.DateTimeField()
    end = models.DateTimeField()
    cancelled = models.BooleanField(default=False)
    original_start = models.DateTimeField()
    original_end = models.DateTimeField()
    #TRACKING
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __init__(self, *args, **kwargs):
        super(Occurrence, self).__init__(*args, **kwargs)
        if self.original_start is None and self.start:
            self.original_start = self.start
        if self.original_end is None and self.end:
            self.original_end = self.end

    @property
    def moved(self):
        return self.original_start != self.start or self.original_end != self.end

    def move(self, new_start, new_end = None):
        if type(new_start) == datetime.timedelta:
            new_end = self.end + new_start
            new_start = self.start + new_start
        self.end = new_end or new_start + (self.end - self.start)
        self.start = new_start
        self.save()

    def cancel(self):
        self.cancelled = True
        self.save()

    def uncancel(self):
        self.cancelled = False
        self.save()

    def __str__(self):
        return "%s to %s" %( date_format(self.start), date_format(self.end) )
    def __lt__(self, other):
        return self.end < other.end

    def __gt__(self, other):
        return self.start > other.start

    #Need this WHAT FOR exactly?
    def __eq__(self, other):
        #Check weather same timeslot is occupied!
        return isinstance(other, Occurrence) and self.start == other.start and self.end == other.end

class TestInheritOccurrence(Occurrence):
    participant = models.CharField(max_length=200)

def all_subclasses(cls):
    return cls.__subclasses__() + [classes for subsub in cls.__subclasses__() for classes in all_subclasses(subsub)]

bases = {}
OccurrenceSubclasses = {'Event':Occurrence}
for cls in all_subclasses(Event):
    methods = dict(cls.__dict__)
    bases[cls.__name__] = []
    for base in cls.__bases__[::-1]:
        if base.__name__ in OccurrenceSubclasses:
            bases[cls.__name__].append(OccurrenceSubclasses[base.__name__])
        elif not issubclass(cls, Event) or base == Event:
            continue
        else:
            bases[cls.__name__].append(base)

    methods = dict(cls.__dict__)
    for method in cls.__dict__:
        if '__module__' != method and (method.endswith('_ptr') or hasattr(Event, method)):
            del methods[method]

    OccurrenceSubclasses[cls.__name__]=type(
        'Occurrence_'+cls.__name__,
        tuple(bases[cls.__name__]),
        dict(methods)
    )
