import pandas as pd
from datetime import datetime, timedelta
td = datetime.today()


def track_actions(act, data):
    """Takes in a specific type of task as a string i.e. 'bi_sent'. also takes in a list of client dictionaries
    to write to a csv file and update actions taken on clients"""
    action_selected = act
    # create sample array of dictionaries
    clients = data

    actions = []
    for i in range(len(clients)):
        print('hit this')
        if clients[i].get('Name'):
            action = {'client_name': f'{clients[i]["Name"]}',
                      'action_taken': action_selected,
                      'age': f'{clients[i]["Age"]}'}
        else:
            action = {'client_name': f'{clients[i]["Client"]}',
                      'action_taken': action_selected,
                      'age': f'{clients[i]["Age"]}'}
        actions.append(action)
    # create or read existing csv as pandas dataframe
    try:
        df = pd.read_csv('client_actions.csv', index_col=0)

    except FileNotFoundError:
        df = pd.DataFrame(columns=['client_name', 'days_aged', 'email_sent', 'bi_sent', 'ae_outreach', 'last',
                                   'last_action_date'])
        df.set_index('client_name', inplace=True)

    # iterate through each action in the array
    for action in actions:
        name = action['client_name']
        typ = action['action_taken']
        age = action['age']

        # if client name not yet in dataframe, add new row
        if name not in df.index:
            df.loc[name] = [0] * len(df.columns)
            df.loc[name, typ] += 1
            df.loc[name, 'last_action_date'] = td.strftime('%m/%d/%Y %H:%M %p')
            df.loc[name, 'last'] = typ
            df.loc[name, 'days_aged'] = age

        # if client name already in dataframe, increment appropriate column
        else:
            if typ == 'bi_sent':
                df.loc[name, typ] += 1
                df.loc[name, 'last_action_date'] = td.strftime('%m/%d/%Y %H:%M %p')
                df.loc[name, 'last'] = typ
                df.loc[name, 'days_aged'] = age
            elif typ == 'ae_outreach':
                df.loc[name, typ] += 1
                df.loc[name, 'last_action_date'] = td.strftime('%m/%d/%Y %H:%M %p')
                df.loc[name, 'last'] = typ
                df.loc[name, 'days_aged'] = age
            elif typ == 'email_sent':
                df.loc[name, typ] += 1
                df.loc[name, 'last_action_date'] = td.strftime('%m/%d/%Y %H:%M %p')
                df.loc[name, 'last'] = typ
                df.loc[name, 'days_aged'] = age



    # save updated dataframe to csv
    df.to_csv('client_actions.csv')
    clean_actions()


def clean_actions():
    df = pd.read_csv('client_actions.csv', index_col=0)
    print(df.count())
    for index, row in df.iterrows():
        date = datetime.strptime(row['last_action_date'], '%m/%d/%Y %H:%M %p')
        age = int(row['days_aged'])

        # print(f"{row['days_aged']} {row['last_action_date']}")
        today = datetime.today()
        days_passed = (today - date).days
        if age + days_passed >= 60:
            df.drop(index, axis=0, inplace=True)
    print(df.count())
    df.to_csv('client_actions.csv')


def gather_metrics():
    df = pd.read_csv('client_actions.csv')
    total = df.shape[0]
    ae_outreach_total = 0
    bi_sent_total = 0
    email_sent_total = 0
    ae_ages = []
    bi_ages = []
    email_ages = []
    for index, row in df.iterrows():
        client_age = row['days_aged']
        ae_outreach_total += int(row['ae_outreach'])
        bi_sent_total += int(row['bi_sent'])
        email_sent_total += int(row['email_sent'])
        last_action = row['last']
        if last_action == 'ae_outreach':
            ae_ages.append(int(client_age))
        elif last_action == 'bi_sent':
            bi_ages.append(int(client_age))
        elif last_action == 'email_sent':
            email_ages.append(int(client_age))

    ae_average_age = sum(ae_ages) / len(ae_ages)
    print('Average Days Aged @ AE Outreach')
    print(round(ae_average_age, 1))

    bi_average_age = sum(bi_ages) / len(bi_ages)
    print('Average Days Aged @ BI Sent')
    print(round(bi_average_age, 1))

    bi_per_client = bi_sent_total / total
    print(f"BIs Per Client: {round(bi_per_client, 1)}")

    ae_per_client = ae_outreach_total / total
    print(f"AE Outreaches Per Client: {round(ae_per_client, 1)}")


gather_metrics()

