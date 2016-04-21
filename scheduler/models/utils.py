from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string


#The following three classes allow:
# * All Event Subclasses to share the EventManager (abstract classes pass on Managers!)
# * All Subclasses to be recognised by [SubClass].objects.get_for_object()
# * And all of them be returned in their corresponding type.

# Subclassing approach based on
# http://www.djangosnippets.org/snippets/1034/
class SubclassingQuerySet(models.QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, BaseEvent) :
            return result.as_leaf_class()
        else :
            return result

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()

def get_model_bases():
    baseStrings = getattr(settings, 'SCHEDULER_BASE_CLASSES', None)
    if baseStrings is None:
        return [models.Model]
    else:
        return [import_string(x) for x in baseStrings]

class OccurrenceReplacer(object):

    def __init__(self, persisted_occurrences):
        lookup = [((occ.event, occ.original_start, occ.original_end), occ) for occ in persisted_occurrences]
        self.lookup = dict(lookup)

    def get_occurrence(self, occ):
        return self.lookup.pop((occ.event, occ.original_start, occ.original_end), occ)

    def has_occurrence(self, occ):
        try:
            return (occ.event, occ.original_start, occ.original_end) in self.lookup
        except TypeError:
            if not self.lookup:
                return False
            else:
                raise TypeError('A problem during lookup of a persisted occurrence has occurred!')

    def get_additional_occurrences(self, start, end):
        return [occ for occ in list(self.lookup.values()) if (occ.start < end and occ.end >= start and not occ.cancelled)]