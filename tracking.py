import pandas as pd
from datetime import datetime
td = datetime.today()


def track_actions(act, data):
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



