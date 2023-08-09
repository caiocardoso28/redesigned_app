from datetime import datetime, timedelta, date, time
import win32com.client
import time as gn
import win32com.client
import pandas
from datetime import datetime


def get_meeting_dict():
    df = pandas.read_csv("recurring_events.csv", index_col="Meeting Name")

    # Convert the DataFrame to a dictionary
    meeting_dict = df.to_dict(orient="index")

    # Convert the dictionary values to a list
    for key, value in meeting_dict.items():
        meeting_dict[key] = [value['Meeting Time'], value['Meeting Duration'], value['Recurrence Pattern']]
    print(meeting_dict)
    return meeting_dict


def recurrence_conflict(selection, dic):
    """This function ensures no conflict occurs with user-defined recurrence blocks (recurring appointments
    captured by the get_conflicts() function have different time data that can interfere with find_times() function.
    This is a minor work-around for the issue)"""
    work_week = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
    }
    selection_date = selection.date()
    for meeting in dic:
        if dic[meeting][2] != 'Daily':
            if selection.weekday() == work_week[dic[meeting][2]]:
                if selection.time().strftime("%H:%M:%S") == dic[meeting][0]:
                    print(dic[meeting][0])
                    print('hitting true')
                    return True
        else:
            if selection.time().strftime("%H:%M:%S") == dic[meeting][0]:
                print(dic[meeting][0])
                print('hitting true')
                return True
    print('hitting False')
    return False


today = datetime.today()
# encapsulate below as get_conflicts(start, end) this will return list of conflicts, date_range in days (int), and start
# as tuple return (conflicts, day_range, begin)

test_emails = ['rebecca.probus@brightspringhealth.com',
               'leo.merle@blaize.com',
               'rogerio.gallo@sefaz.mt.gov.br',
               'ALSMITH1@ARKBLUECROSS.COM',
               'steve.benni@oakstreethealth.com',
               'rohit.juneja@newgold.com',
               'john.wheeler@cognizant.com']


def get_conflicts(start_date=None, end_date=None, cal_view=False):
    """This function searches and sorts through user's local Outlook calendar items. If cal_view is set to True,
    then the function will specifically search for calendar items for the specified week to populate the
    clients on the calendar widget. Otherwise, the range will be based on user input or default to 21 days."""
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    appointments = outlook.GetDefaultFolder(9).Items
    appointments.IncludeRecurrences = True

    now = datetime.now()
    # begin will be equal to start
    if start_date:
        begin_date = start_date.date()
    else:
        begin_date = today.date()
    begin_time = time(8, 0, 0)
    begin = datetime.combine(begin_date, begin_time)
    # will be equal to tdelta end - start
    if not cal_view:
        day_range = 21
    else:
        day_range = 5
    # will be equal to end argument from function call
    if end_date:
        ending_date = end_date.date()
    else:
        ending_date = begin_date + timedelta(days=day_range)
    ending_time = time(17, 0, 0)

    end = datetime.combine(ending_date, ending_time)
    #print(begin)
    # restrict range of appointments to read

    restriction = "[Start] >= '" + begin.strftime("%m/%d/%Y %I:%M %p") + "' AND [END] <= '" + end.strftime("%m/%d/%Y %I:%M %p") + "'"
    appointments = appointments.Restrict(restriction)
    recurring_appointments = []

    sorted_list = sorted(appointments, key=lambda x: x.Start.date())

    mon = {}
    tues = {}
    wed = {}
    thur = {}
    fri = {}

    # capture and categorize calendar events by weekday
    for item in sorted_list:

        if item.meetingstatus != 7 and 120 > item.Duration >= 15:
            if item.RecurrenceState < 1:
                # print(item.Subject)
                if item.Start.weekday() == 0:
                    mon[(item.Start.strftime("%m/%d/%Y %I:%M %p"))] = item
                elif item.Start.weekday() == 1:
                    tues[(item.Start.strftime("%m/%d/%Y %I:%M %p"))] = item
                elif item.Start.weekday() == 2:
                    wed[(item.Start.strftime("%m/%d/%Y %I:%M %p"))] = item
                elif item.Start.weekday() == 3:
                    thur[(item.Start.strftime("%m/%d/%Y %I:%M %p"))] = item
                elif item.Start.weekday() == 4:
                    fri[(item.Start.strftime("%m/%d/%Y %I:%M %p"))] = item

            else:
                # print(f'{item.Subject}: {item.Start.weekday()} Type: {item.GetRecurrencePattern().RecurrenceType}')
                recurring_appointments.append(item)
        # print(f"{item.Start.weekday()} {item.Subject}")
        else:
            pass

    conflicts = [mon, tues, wed, thur, fri]
    return conflicts


def get_meetings_week(week):
    if week == 'This Week':
        today = datetime.today().weekday()
        week_start = datetime.today() - timedelta(days=today)
        meetings = get_conflicts(start_date=week_start, cal_view=True)
        print(meetings)

        return meetings
    elif week == 'Next Week':
        today = datetime.today().weekday()
        week_next = datetime.today() + timedelta(weeks=1)
        week_start = week_next - timedelta(days=today)
        meetings = get_conflicts(start_date=week_start, cal_view=True)
        print(meetings)

        return meetings
        pass
    elif week == 'Last Week':
        today = datetime.today().weekday()
        week_last = datetime.today() - timedelta(weeks=1)
        week_start = week_last - timedelta(days=today)
        meetings = get_conflicts(start_date=week_start, cal_view=True)
        print(meetings)

        return meetings
        pass


def get_meetings_today(array):
    meetings = []
    td = datetime.today()
    td_day = td.weekday()
    td_string = td.strftime("%m/%d/%Y")

    for key in array[td_day]:
        appointment = array[td_day].get(key)
        appointment_date = appointment.Start.strftime("%m/%d/%Y")
        if appointment_date == td_string:
            if 'Your Gartner Call' in appointment.Subject or 'Accept or Reschedule' in appointment.Subject or 'Seu' in appointment.Subject:
                meetings.append(appointment)

    clients = []
    i = 0
    for item in meetings:
        # print(i)
        for recipient in item.Recipients:
            if ',' not in recipient.Name:
                clients.append(recipient.Address)
                # print(f"Recipient: {recipient.Name}")

        i += 1
    return clients


def find_times(item_list, meeting_duration, date_range=30, length=None):
    """ Algorithm for finding open slots on calendar -> returns array of datetime objects to fill Invite Table.
        IF not enough times are found in the default range of 30 days, the function recursively extends date range until
        enough
        times are found.
    """
    user_events = get_meeting_dict()
    time_output = []
    conflicts = item_list

    def reset_time(date_time):
        if date_time.weekday() == 4:
            d = date_time.date() + timedelta(days=3)
        else:
            d = date_time.date() + timedelta(days=1)
        hour = 9
        minute = 0
        t = time(hour=hour, minute=minute)
        return datetime.combine(d, t)

    dt = date.today()
    hour = 9
    minute = 0
    t = time(hour=hour, minute=minute)
    # this is a pointer that moves through weekdays then traverses each day's timeslots (30 or 15 min intervals)
    selection = datetime.combine(dt, t)

    # loop through weekdays
    for i in range(date_range):
        # checking if selection is same-day, then pushing the selection date accordingly
        if selection.date() == datetime.today().date():
            if selection.weekday() == 4:
                selection = selection + timedelta(days=3)
            elif selection.weekday() == 5:
                selection = selection + timedelta(days=2)

            else:
                selection = selection + timedelta(days=1)

        # Just in case algorithm tries to push selection date to weekend (Friday '4' is ok)
        if selection.weekday() == 4:
            pass
        elif selection.weekday() == 5:
            selection = selection + timedelta(days=2)
        elif selection.weekday() == 6:
            selection = selection + timedelta(days=1)

        # time_key is used to check for conflicts in conflicts dictionary using constant O(1) time
        time_key = selection.strftime("%m/%d/%Y %I:%M %p")
        duration = meeting_duration
        # BI Duration (30min or 15min) is used to determine how many time slots to check for each day
        if duration == 30:
            time_slot_count = 16
        else:
            time_slot_count = 26
        print(time_slot_count)
        # loop through timeslots and check conflicts using weekday index
        for j in range(time_slot_count):
            # print(f"{selection.weekday()} {selection.date()} {selection.time()}")
            try:
                if conflicts[selection.weekday()].get(time_key):
                    conflict = conflicts[selection.weekday()].get(time_key)
                    # print(f'Conflict: {conflicts[selection.weekday()].get(time_key).Subject} at {selection.time()}')
                    # Determining time to push the selection pointer forward in the day using conflict duration
                    if duration == 30:
                        if conflict.Duration % 2 != 0:
                            if conflict.Duration < 30:
                                selection = selection + timedelta(minutes=duration)
                            else:
                                selection = selection + timedelta(minutes=90)
                        else:
                            selection = selection + timedelta(minutes=conflict.Duration)
                    else:
                        selection = selection + timedelta(minutes=conflict.Duration)

                    time_key = selection.strftime("%m/%d/%Y %I:%M %p")
                else:
                    if j < time_slot_count - 1:
                        # user variable parameters (lunchtime object and other recurrences times will be considered here
                        bod = datetime.combine(date=selection.date(), time=time(hour=8, minute=0))
                        eod = datetime.combine(date=selection.date(), time=time(hour=16, minute=0))
                        lunch = datetime.combine(date=selection.date(), time=time(hour=12, minute=0))
                        break_1 = datetime.combine(date=selection.date(), time=time(hour=10, minute=0))
                        # Solution for team meetings for right now
                        if selection.weekday() == 0:
                            team_meeting = datetime.combine(date=selection.date(), time=time(hour=11, minute=0))
                        else:
                            team_meeting = None
                        if selection.weekday() == 4:
                            team_eow = datetime.combine(date=selection.date(), time=time(hour=11, minute=0))
                        else:
                            team_eow = None
                        # ensuring no time outside work hours gets included
                        if bod.time() < selection.time() < eod.time():
                            if not recurrence_conflict(selection, user_events):
                                time_output.append(selection)
                            else:
                                selection = selection + timedelta(minutes=60)
                                time_key = selection.strftime("%m/%d/%Y %I:%M %p")
                                continue
                        selection = selection + timedelta(minutes=duration)
                        time_key = selection.strftime("%m/%d/%Y %I:%M %p")
                    else:
                        selection = reset_time(selection)
                        time_key = selection.strftime("%m/%d/%Y %I:%M %p")
            except:
                pass
    final_output = []
    i = 0
    last_time = None
    import random
    for slot in time_output:
        if slot.date() - today.date() < timedelta(days=2):
            continue
        # randomize times to avoid only capturing earlier times for each day
        if random.randint(0, 10) % 2 != 0:
            continue
        # print(slot.date())
        if not last_time:
            i += 1
            final_output.append(slot)
            last_time = slot
        else:
            if last_time.date() == slot.date():
                if i < 3:
                    final_output.append(slot)
                    last_time = slot
                    i += 1
                else:
                    continue
            else:
                i = 1
                final_output.append(slot)
                last_time = slot

    print(len(time_output))
    print(len(final_output))

    if len(final_output) >= length:
        return final_output
    else:
        date_range += 1
        return find_times(conflicts, meeting_duration, date_range, length=length)


def get_most_recent_email_from_sender(email_address):
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 refers to the index of the Inbox folder
    invite_responses = inbox.Folders["Invite Responses"]
    print('that was ok')
    start_of_year = today - timedelta(weeks=4)
    # Retrieve all emails in the inbox folder
    messages = inbox.Items.Restrict("[ReceivedTime] >= '" + start_of_year.strftime('%m/%d/%Y %H:%M %p') + "'")
    invite_responses = invite_responses.Items.Restrict("[ReceivedTime] >= '" + start_of_year.strftime('%m/%d/%Y %H:%M %p') + "'")

    # Create a list of emails that match the given email address
    email_list = []
    response_list = []
    i = 0
    try:

        for message in messages:
            if message.Class != 43:
                continue
            if message.SenderEmailType == 'EX':
                continue
            if i < 1000:
                try:
                    print(message.ReceivedTime)
                    print('working')
                    if message.SenderEmailAddress.lower() == email_address.lower():
                        print('found')
                        email_list.append(message)
                        break
                except:
                    pass
                i += 1
            else:
                break

        for response in invite_responses:
            print('response')

            meeting_request = response
            print(meeting_request.Class)
            print("Meeting Subject:", meeting_request.Subject)
            if meeting_request.SenderEmailAddress.lower() == email_address.lower():
                email_list.append(meeting_request)

        print(invite_responses)
        i = 0

    except Exception as e:
        print(f"An error occurred:", str(e))

    # Sort the emails by received time and get the most recent one

    email_list.sort(key=lambda x: x.ReceivedTime, reverse=True)
    try:
        most_recent_email = email_list[0]
        most_recent_email.Display()
    except:
        if len(response_list) > 0:
            most_recent_email = response_list[0]
            most_recent_email.Display()
        else:
            most_recent_email = None

    return most_recent_email
# testing = get_conflicts()



