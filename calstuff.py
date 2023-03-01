from datetime import datetime, timedelta, date, time
import win32com.client
import time as gn
import win32com.client

from datetime import datetime

today = datetime.today()
# encapsulate below as get_conflicts(start, end) this will return list of conflicts, date_range in days (int), and start
# as tuple return (conflicts, day_range, begin)


def get_conflicts(start_date=None, end_date=None, cal_view=False):
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
    print(begin)
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


# will take output from get_conflicts (conflicts, day_range, begin) and meeting duration


def find_times(item_list, meeting_duration, date_range):

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

    selection = datetime.combine(dt, t)

    # loop through weekdays
    for i in range(date_range):

        if selection.date() == datetime.today().date():
            if selection.weekday() == 4:
                selection = selection + timedelta(days=3)
            elif selection.weekday() == 5:
                selection = selection + timedelta(days=2)

            else:
                selection = selection + timedelta(days=1)

        print(f'{selection.weekday()}: {selection.date()}')
        time_key = selection.strftime("%m/%d/%Y %I:%M %p")
        duration = meeting_duration
        if duration == 30:
            time_slot_count = 16
        else:
            time_slot_count = 26

        # loop through timeslots and check conflicts using weekday index
        for j in range(time_slot_count):
            if conflicts[selection.weekday()].get(time_key):
                conflict = conflicts[selection.weekday()].get(time_key)
                print(f'Conflict: {conflicts[selection.weekday()].get(time_key).Subject} at {selection.time()}')

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
                    eod = datetime.combine(date=selection.date(), time=time(hour=16, minute=0))
                    lunch = datetime.combine(date=selection.date(), time=time(hour=12, minute=0))
                    if selection.time() <= eod.time():
                        if selection != lunch:
                            print(f'opening found at {selection.time()}')
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

    return time_output


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
# testing = find_times(conflicts, 30, day_range)



