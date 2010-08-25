#!/usr/bin/env python
'''
hamstered.py - Copyright 2010, Ton van den Heuvel, Ecomation
'''

from datetime import datetime, timedelta, date
import optparse
import sqlite3

class Hamstered(object):
    def __init__(self, options):
        if options.start_date:
            self.start_date = datetime.strptime(options.start_date, '%Y-%m-%d').date()
        else:
            self.start_date = date.today() - timedelta(days = int(options.days) - 1)

        if options.end_date:
            self.end_date = datetime.strptime(options.end_date, '%Y-%m-%d').date()
        else:
            self.end_date = date.today()

        self.databases = options.databases.split(',')
        self.output_file = options.output_file
        self.travel_description = options.travel_description
        self.travel_hours = options.travel_hours

    def format_duration(self, start_time, end_time):
        # for now, only report in hours rounded to quarters 
        return round((end_time - start_time).seconds / 900.) * 0.25

    def generate(self):
        # activities is a mapping from a start date to a list of tuples containing an activity name, a start time, an end time, and a duration in fractional hours
        days = {}
        for database in self.databases:
            try:
                connection = sqlite3.connect(database)
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute("select name, start_time, end_time from facts "
                        "left join activities on activities.id = activity_id "
                        "where date(start_time) >= '" + self.start_date.isoformat() + "' and date(end_time) <= '" + self.end_date.isoformat() + "' "
                        "order by start_time")
                rows = cursor.fetchall()
                for row in rows:
                    start_time = datetime.strptime(row['start_time'], '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.strptime(row['end_time'], '%Y-%m-%d %H:%M:%S')
                    day = start_time.date() #date.strftime(start_time.date(), '%d-%m-%Y')
                    if not day in days:
                        days[day] = [] if not self.travel_hours else [(self.travel_description, '', '', float(self.travel_hours))]
                    days[day].append((row['name'], datetime.strftime(start_time, '%H:%M'), datetime.strftime(end_time, '%H:%M'), self.format_duration(start_time, end_time)))
            except:
                print 'Error processing database: ' + database
                raise

        f = open(self.output_file, 'w')
        f.write('<?xml-stylesheet type="text/xsl" href="hamstered.xsl"?>\n')
        f.write('<report start_date="' + date.strftime(self.start_date, '%d-%m-%Y') + '" end_date="' + date.strftime(self.end_date, '%d-%m-%Y') + '">\n')
        last_date = None
        for day in sorted(days.items()):
            if (day[0] != last_date):
                if last_date is not None:
                    f.write('</day>\n')
                last_date = day[0]
                f.write('<day date="' + date.strftime(last_date, '%d-%m') + '" weekday="' + str(last_date.weekday()) + '">\n')

            for activity in day[1]:
                f.write('  <activity name="' + activity[0] + '" start_time="' + activity[1] + '" end_time="' + activity[2] + '" duration="' + str(activity[3]) + '" />\n')
        if last_date is not None:
            f.write('</day>\n')
        f.write('</report>\n')

if __name__ == '__main__':
    parser = optparse.OptionParser(description = 'Generate an XML report from (multiple) hamster database over a given date range.',
            version = "0.0.1",
            usage = 'usage: %prog <-d, --database=DATABASES> [options]',
            epilog = 'Copyright 2010, Ton van den Heuvel, Ecomation, see LICENSE for more details.')
    parser.add_option('-d', '--database',
            dest = 'databases',
            help = 'comma separated list of Hamster .db files')
    parser.add_option('-s', '--start',
            dest = 'start_date',
            help = 'start date for which the report should be generated (in ISO 8601 format; yyyy-mm-dd)')
    parser.add_option('-e', '--end',
            dest = 'end_date',
            help = 'end date for which the report should be generated (in ISO 8601 format; yyyy-mm-dd), default: today\'s date')
    parser.add_option('-l', '--last',
            dest = 'days',
            help = 'generate a report for the last DAYS (> 0) days including today')
    parser.add_option('-r', '--round',
            dest = 'round',
            default = 'quarter',
            help = 'format in which to report the duration per activity: quarter. Default: %default')
    parser.add_option('-t', '--travel',
            dest = 'travel_hours',
            help = 'adds a travel activity with the given number of hours (in decimal format) for each day in the range with other activity')
    parser.add_option('-a', '--travel_activity',
            dest = 'travel_description',
            default = 'Traveling',
            help = 'specify a name for the trave activity, default: %default')
    parser.add_option('-o', '--output',
            dest = 'output_file',
            default = 'hamstered.xml',
            help = 'XML report to generate, default: %default')
    (options, args) = parser.parse_args()
    if not options.databases:
        print 'Error, please provide a list of comma separated Hamster database files.\n'
    elif (not options.start_date and not options.days) or (options.days and int(options.days) < 1):
        print 'Error, please provide a valid date range.\n'
        parser.print_usage()
    else:
        Hamstered(options).generate()
