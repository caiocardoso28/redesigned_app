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


def gather_activity_metrics(client_objects=None, all_clients=None):
    client_dictionary = {}
    df = pd.read_csv('client_actions.csv')
    total = df.shape[0]
    ae_outreach_total = 0
    bi_sent_total = 0
    email_sent_total = 0
    ae_ages = []
    bi_ages = []
    email_ages = []
    for index, row in df.iterrows():
        client_dictionary[row['client_name']] = {'emails_sent': int(row['email_sent']),
                                                 'ae_outreaches': int(row['ae_outreach']),
                                                 'bis_sent': int(row['bi_sent'])}
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
    print()
    # print(client_dictionary)
    plan_dictionary = {}
    try:
        for client in client_objects:
            if client_dictionary.get(client.name):
                actions = client_dictionary.get(client.name)
                if not plan_dictionary.get(client.price_plan):
                    plan_dictionary[client.price_plan] = actions
                else:
                    plan_dictionary[client.price_plan]['emails_sent'] += actions['emails_sent']
                    plan_dictionary[client.price_plan]['bis_sent'] += actions['bis_sent']
                    plan_dictionary[client.price_plan]['ae_outreaches'] += actions['ae_outreaches']
    except Exception as e:
        print(e)
    # Write to another csv file (eventually database) so that total numbers can be aggregated
    print(plan_dictionary)
    count_product_activity(product_count=plan_dictionary, clients=all_clients)
    return [bi_average_age, ae_average_age, bi_per_client, ae_per_client]


def count_product_activity(product_count, clients=None):
    df = pd.read_csv('product_list.csv')

    gbs = {item: True for item in df.GBS if isinstance(item, str)}
    gbs_grand_total = 0
    gbs_bi = 0
    gbs_ae = 0

    eu = {item: True for item in df.EU if isinstance(item, str)}
    eu_grand_total = 0
    eu_bi = 0
    eu_ae = 0

    ht = {item: True for item in df.HT if isinstance(item, str)}
    ht_grand_total = 0
    ht_bi = 0
    ht_ae = 0

    other = {item: True for item in df.OTHER if isinstance(item, str)}
    other_grand_total = 0
    other_bi = 0
    other_ae = 0

    for key in product_count:
        if gbs.get(key):
            # gbs_total += 1
            gbs_bi += product_count[key]['bis_sent']
            gbs_ae += product_count[key]['ae_outreaches']
        elif eu.get(key):
            # eu_total += 1
            eu_bi += product_count[key]['bis_sent']
            eu_ae += product_count[key]['ae_outreaches']
        elif ht.get(key):
            # ht_total += 1
            ht_bi += product_count[key]['bis_sent']
            ht_ae += product_count[key]['ae_outreaches']
        elif other.get(key):
            # other_total += 1
            other_bi += product_count[key]['bis_sent']
            other_ae += product_count[key]['ae_outreaches']
        else:
            # other_total += 1
            other_bi += product_count[key]['bis_sent']
            other_ae += product_count[key]['ae_outreaches']

    all_client_products = [client.price_plan for client in clients]

    for product in all_client_products:
        if gbs.get(product):
            gbs_grand_total += 1
        elif eu.get(product):
            eu_grand_total += 1
        elif ht.get(product):
            ht_grand_total += 1
        elif other.get(product):
            other_grand_total += 1
        else:
            other_grand_total += 1

    gbs_total = gbs_ae + gbs_bi
    eu_total = eu_ae + eu_bi
    ht_total = ht_bi + ht_ae
    other_total = other_bi + other_ae

    total_list = [gbs_grand_total, eu_grand_total, ht_grand_total, other_grand_total]
    denominator = max(total_list)
    print(eu_total / eu_grand_total)
    print(ht_total / ht_grand_total)
    final = {"GBS": {'GRAND_TOTAL': gbs_grand_total, 'TOTAL': gbs_total, 'BI': gbs_bi, 'AE': gbs_ae},
             'EU': {'GRAND_TOTAL': eu_grand_total, 'TOTAL': eu_total, 'BI': eu_bi, 'AE': eu_ae},
             'HT': {'GRAND_TOTAL': ht_grand_total, 'TOTAL': ht_total, 'BI': ht_bi, 'AE': ht_ae},
             'OTHER': {'GRAND_TOTAL': other_grand_total, 'TOTAL': other_total, 'BI': other_bi, 'AE': other_ae}
             }

    print(final)

