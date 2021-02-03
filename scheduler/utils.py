from django.test import TestCase
from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Event


class EventCalendar(HTMLCalendar):
    user = ""
    def __init__(self, user, events=None):
        super(EventCalendar, self).__init__()
        self.events = events
        self.user = user

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(day__day=day)
        events_html = "<ul style='background-color:#35ACF2' >"
        for event in events_from_day:
            eventsObj = Event.objects.get(notes=str(event.notes))
            val = str(eventsObj.invites).split(",")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(val)
            print(self.user)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            if str(self.user) not in val:
                continue
            
            print("-----------------------------------------------------")
            print("Events Day: ",event.notes)
            print("-----------------------------------------------------")
            events_html += "<br><center><form action='http://127.0.0.1:8000/viewVal/' method='GET'> <input type='text' name='notes' style='display:none;' value='"+str(event.notes)+"'> <input type='text' name='user' style='display:none;' value='"+str(event.username)+"'><input type='submit' value='View Event'> </form></center><br>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td style="background-color:#C2F2F2" class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Event.objects.filter(day__month=themonth)

        v = []
        a = v.append
        a('<style>table {  font-family: arial, sans-serif;  border-collapse: collapse;  width: 100%;}')
        a('td, th {  border: 1px solid #dddddd;  text-align: left;  padding: 8px;}')
        a('tr {  background-color: #F2E7F2;}</style>')
        a('<table style="tr:first-child{ background-color: #C2F2F2;}" border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
