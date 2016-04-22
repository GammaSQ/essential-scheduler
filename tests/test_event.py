import datetime

from django.utils import timezone

from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User

from scheduler.models import Event, Rule, Calendar, EventRelation, TestSubEvent
from scheduler.models.occurrences import TestInheritOccurrence
from scheduler.models.events import BaseEvent


class TestEvent(TestCase):

    def setUp(self):
        cal = Calendar(name="MyCal")
        cal.save()

    def __create_event(self, start, end, cal):
        return Event(**{
            'start':start,
            'end':end,
            'calendar':cal
        })

    def __create_recurring_event(self, start, end, end_recurring, rule, cal):
        return Event(**{

                'start': start,
                'end': end,
                'end_recurring_period': end_recurring,
                'rule': rule,
                'calendar': cal
        })

    def test_edge_case_events(self):
        cal = Calendar(name="MyCal")
        cal.save()

        data_1 = {
            'start': datetime.datetime(2013, 1, 5, 8, 0, tzinfo=timezone.utc),
            'end': datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
            'calendar': cal,
        }

        data_2 = {
            'start': datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
            'end': datetime.datetime(2013, 1, 5, 12, 0, tzinfo=timezone.utc),

            'calendar': cal
        }
        event_one = Event(**data_1)
        event_two = Event(**data_2)
        event_one.save()
        event_two.save()

        occurrences_two = event_two.get_occurrences(datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
                                                    datetime.datetime(2013, 1, 5, 12, 0, tzinfo=timezone.utc))
        self.assertEqual(1, len(occurrences_two))

        occurrences_one = event_one.get_occurrences(datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
                                                    datetime.datetime(2013, 1, 5, 12, 0, tzinfo=timezone.utc))

        self.assertEqual(0, len(occurrences_one))

    def test_recurring_event_get_occurrences(self):

        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()

        recurring_event = self.__create_recurring_event(

                    datetime.datetime(2008, 1, 5, 8, 0, tzinfo=timezone.utc),
                    datetime.datetime(2008, 1, 5, 9, 0, tzinfo=timezone.utc),
                    datetime.datetime(2008, 5, 5, 0, 0, tzinfo=timezone.utc),

                    rule,
                    cal,
                    )
        recurring_event.save()

        occurrences = recurring_event.get_occurrences(start=datetime.datetime(2008, 1, 12, 0, 0, tzinfo=timezone.utc),
                                                      end=datetime.datetime(2008, 1, 20, 0, 0, tzinfo=timezone.utc))

        self.assertEqual(["%s to %s" % (o.start, o.end) for o in occurrences],
                          ['2008-01-12 08:00:00+00:00 to 2008-01-12 09:00:00+00:00',
                           '2008-01-19 08:00:00+00:00 to 2008-01-19 09:00:00+00:00'])


    def test_recurring_event_get_occurrences_2(self):
        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()

        recurring_event = self.__create_recurring_event(
                                    datetime.datetime(2008, 1, 5, 8, 0, tzinfo=timezone.utc),
                                    datetime.datetime(2008, 1, 5, 9, 0, tzinfo=timezone.utc),
                                    datetime.datetime(2008, 5, 5, 0, 0, tzinfo=timezone.utc),
                                    rule,
                                    cal
                )
        recurring_event.save()
        occurrences = recurring_event.get_occurrences(
                                    start=datetime.datetime(2008, 1, 12, 0, 0, tzinfo=timezone.utc),
                                    end=datetime.datetime(2008, 1, 20, 0, 0, tzinfo=timezone.utc))

        self.assertEqual(["%s to %s" %(o.start, o.end) for o in occurrences],
                ['2008-01-12 08:00:00+00:00 to 2008-01-12 09:00:00+00:00', '2008-01-19 08:00:00+00:00 to 2008-01-19 09:00:00+00:00'])

    def test_event_get_occurrences_after(self):

        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()

        self.__create_recurring_event(

                    datetime.datetime(2008, 1, 5, 8, 0, tzinfo=timezone.utc),
                    datetime.datetime(2008, 1, 5, 9, 0, tzinfo=timezone.utc),
                    datetime.datetime(2008, 5, 5, 0, 0, tzinfo=timezone.utc),

                    rule,
                    cal,
                    )
        event_one = self.__create_event(

                datetime.datetime(2013, 1, 5, 8, 0, tzinfo=timezone.utc),
                datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
                cal
        )
        event_two = self.__create_event(
                datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
                datetime.datetime(2013, 1, 5, 12, 0, tzinfo=timezone.utc),

                cal
        )
        event_one.save()
        event_two.save()
        occurrences_two = event_two.get_occurrences(

                                    datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
                                    datetime.datetime(2013, 1, 5, 12, 0, tzinfo=timezone.utc))


        self.assertEqual(1, len(occurrences_two))

        occurrences_one = event_one.get_occurrences(

                                    datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
                                    datetime.datetime(2013, 1, 5, 12, 0, tzinfo=timezone.utc))

        self.assertEqual(0, len(occurrences_one))

    def test_recurring_event_get_occurrences_after(self):

        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()
        recurring_event= self.__create_recurring_event(
                    datetime.datetime(2008, 1, 5, 8, 0, tzinfo=timezone.utc),
                    datetime.datetime(2008, 1, 5, 9, 0, tzinfo=timezone.utc),
                    datetime.datetime(2008, 5, 5, 0, 0, tzinfo=timezone.utc),
                    rule,
                    cal,
                    )

        recurring_event.save()
        occurrences = recurring_event.get_occurrences(start=datetime.datetime(2008, 1, 5, tzinfo=timezone.utc),
            end = datetime.datetime(2008, 1, 6, tzinfo=timezone.utc))
        occurrence = occurrences[0]
        occurrence2 = next(recurring_event.occurrences_after(datetime.datetime(2008, 1, 5, tzinfo=timezone.utc)))
        self.assertEqual(occurrence, occurrence2)

    def test_recurring_event_get_occurrences_after_with_moved_occ(self):


        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()
        recurring_event= self.__create_recurring_event(

                    datetime.datetime(2008, 1, 5, 2, 0, tzinfo=timezone.utc),
                    datetime.datetime(2008, 1, 5, 3, 0, tzinfo=timezone.utc),
                    datetime.datetime(2008, 5, 5, 0, 0, tzinfo=timezone.utc),

                    rule,
                    cal,
                    )

        recurring_event.save()
        occurrence = recurring_event.get_occurrence(datetime.datetime(2008, 1, 12, 2, 0, tzinfo=timezone.utc), True)
        occurrence.move(
          datetime.datetime(2008, 1, 15, 8, 0, tzinfo=timezone.utc),
          datetime.datetime(2008, 1, 15, 9, 0, tzinfo=timezone.utc))
        occurrence2 = recurring_event.get_occurrence(
          datetime.datetime(2008, 1, 14, 8, 0, tzinfo=timezone.utc))
        self.assertEqual(occurrence, occurrence2)
        self.assertEqual(datetime.datetime(2008, 1, 15, 8, 0, tzinfo=timezone.utc), occurrence2.start)

    def test_recurring_event_get_occurrence(self):

        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()

        event = self.__create_recurring_event(
                datetime.datetime(2008, 1, 5, 8, 0, tzinfo=timezone.utc),
                datetime.datetime(2008, 1, 5, 9, 0, tzinfo=timezone.utc),
                datetime.datetime(2008, 5, 5, 0, 0, tzinfo=timezone.utc),
                rule,
                cal,
            )
        event.save()

        occurrence = event.get_occurrence(datetime.datetime(2008, 1, 5, 8, 0, tzinfo=timezone.utc))
        self.assertEqual(occurrence.start, datetime.datetime(2008, 1, 5, 8, tzinfo=timezone.utc))
        occurrence.save()
        occurrence = event.get_occurrence(datetime.datetime(2008, 1, 5, 8, 0, tzinfo=timezone.utc))
        self.assertTrue(occurrence.pk is not None)

    @override_settings(HIDE_NAIVE_AWARE_TYPE_ERROR=True)
    def test_prevent_TypeError_when_comparing_naive_w_aware_dates(self):
        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()

        event = self.__create_recurring_event(
                datetime.datetime(2008, 1, 5, 8, 0, tzinfo=timezone.utc),
                datetime.datetime(2008, 1, 5, 9, 0, tzinfo=timezone.utc),
                datetime.datetime(2008, 5, 5, 0, 0, tzinfo=timezone.utc),
                rule,
                cal,
            )

        naive_date = datetime.datetime(2008, 1, 20, 0, 0)
        self.assertIsNone(event.get_occurrence(naive_date, True))

    @override_settings(USE_TZ=False)
    def test_prevent_TypeError_when_comparing_dates_when_tz_off(self):
        cal = Calendar(name="MyCal")
        cal.save()
        rule = Rule(frequency="WEEKLY")
        rule.save()

        event = self.__create_recurring_event(
                    datetime.datetime(2008, 1, 5, 8, 0),
                    datetime.datetime(2008, 1, 5, 9, 0),
                    datetime.datetime(2008, 5, 5, 0, 0),
                    rule,
                    cal,
                    )
        naive_date = datetime.datetime(2008, 1, 20, 0, 0)
        self.assertIsNone(event.get_occurrence(naive_date, True))

    def test_event_get_ocurrence(self):

        cal = Calendar(name='MyCal')
        cal.save()
        start = timezone.now() + datetime.timedelta(days=1)
        event = self.__create_event(
                            start,
                            start + datetime.timedelta(hours=1),
                            cal)
        event.save()
        occurrence = event.get_occurrence(start)
        self.assertEqual(occurrence.start, start)

    def test_occurences_after_with_no_params(self):

        cal = Calendar(name='MyCal')
        cal.save()
        start = timezone.now() + datetime.timedelta(days=1)
        event = self.__create_event(
                            start,
                            start + datetime.timedelta(hours=1),
                            cal)
        event.save()
        occurrences = list(event.occurrences_after())
        self.assertEqual(len(occurrences), 1)
        self.assertEqual(occurrences[0].start, start)
        self.assertEqual(occurrences[0].end, start + datetime.timedelta(hours=1))

    def test_occurences_with_recurrent_event_end_recurring_period_edge_case(self):

        cal = Calendar(name='MyCal')
        cal.save()
        rule = Rule(frequency="DAILY")
        rule.save()
        start = timezone.now() + datetime.timedelta(days=1)
        event = self.__create_recurring_event(
                            start,
                            start + datetime.timedelta(hours=1),
                            start + datetime.timedelta(days=10),
                            rule,
                            cal)
        event.save()
        occurrences = list(event.occurrences_after())
        self.assertEqual(len(occurrences), 11)

    def test_get_for_object(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        event_relations = list(Event.objects.get_for_object(user, 'owner'))
        self.assertEqual(len(event_relations), 0)

        rule = Rule(frequency="DAILY")
        rule.save()
        cal = Calendar(name='MyCal')
        cal.save()
        event = self.__create_event(
                datetime.datetime(2013, 1, 5, 8, 0, tzinfo=timezone.utc),
                datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
                cal
        )
        event.save()
        events = list(Event.objects.get_for_object(user, 'owner'))
        self.assertEqual(len(events), 0)
        EventRelation.objects.save_relation(event, user, 'owner')

        events = list(Event.objects.get_for_object(user, 'owner'))
        self.assertEqual(len(events), 1)
        self.assertEqual(event, events[0])

class TestEventInheritance(TestEvent):

    BaseEvent.occurrence_class=TestInheritOccurrence

    def __create_event(self, title, start, end, cal):
        return TestSubEvent(**{
                'title': title,
                'start': start,
                'end': end,
                'calendar': cal
        })

    def __create_recurring_event(self, title, start, end, end_recurring, rule, cal):
        return TestSubEvent(**{
                'title': title,
                'start': start,
                'end': end,
                'end_recurring_period': end_recurring,
                'rule': rule,
                'calendar': cal
        })

    def test_event_inheritence(self):
        cal = Calendar(name="MyCal")
        cal.save()
        event = self.__create_event(
            "Heeello!",
            datetime.datetime(2013, 1, 5, 8, 0, tzinfo=timezone.utc),
            datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
            cal
        )
        event.save()
        occ = event.get_occurrences(
            datetime.datetime(2013, 1, 5, 8, 0, tzinfo=timezone.utc),
            datetime.datetime(2014, 1, 5, 8, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(1, len(occ))

    def test_get_for_object(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        event_relations = list(Event.objects.get_for_object(user, 'owner'))
        self.assertEqual(len(event_relations), 0)

        rule = Rule(frequency="DAILY")
        rule.save()
        cal = Calendar(name='MyCal')
        cal.save()
        event = self.__create_event(
                'event test',
                datetime.datetime(2013, 1, 5, 8, 0, tzinfo=timezone.utc),
                datetime.datetime(2013, 1, 5, 9, 0, tzinfo=timezone.utc),
                cal
        )
        event.save()
        events = list(Event.objects.get_for_object(user, 'owner'))
        self.assertEqual(len(events), 0)
        EventRelation.objects.save_relation(event, user, 'owner')

        self.assertEqual(len(list(event.eventrelation_set.all())), 1)

        events = list(Event.objects.get_for_object(user, 'owner'))
        self.assertEqual(len(events), 1)
        self.assertEqual(type(events[0]), TestSubEvent)
        self.assertEqual(event, events[0])
