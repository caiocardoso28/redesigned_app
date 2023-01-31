
import win32com.client
import time as gn
import win32com.client


def show_invites(clients):
    outlook = win32com.client.Dispatch("Outlook.Application")

    for client in clients:
        if client.get('Edited Time'):
            dt = client.get('Edited Time')
        else:
            dt = client.get('Suggested Time')
        cal_item = outlook.CreateItem(1)
        if client.get('Country') == 'BRAZIL':
            cal_item.subject = "Gartner | Seu call de introdução às ferramentas está disponível"
            cal_item.body = f"""Oi {client['Name'].split(' ')[0]},\n\n"""
        else:
            cal_item.subject = 'Accept or Reschedule > Your Gartner Membership'
            cal_item.body = f"""Hi {client['Name'].split(' ')[0]},\n\n"""
        cal_item.location = 'Teams Meeting'
        cal_item.start = dt
        cal_item.duration = 30
        cal_item.MeetingStatus = 1
        required = cal_item.Recipients.add(f"{client['Email']}")
        required.Type = 1
        optional = cal_item.Recipients.add(f"{client['AE']};")
        optional.Type = 2
        gn.sleep(1)
        cal_item.display()


def send_emails(clients, template=None, subject=None):
    outlook = win32com.client.Dispatch('outlook.application')
    template = template
    to_change = ['(AE)', '(AGE)', '(CLIENT)', '(ORG)']
    i = 0
    last_client = None
    for client in clients:
        mail = outlook.CreateItem(0)
        mail.To = client['Email']
        if template and subject:
            for item in to_change:
                if item == '(AE)':
                    if i == 0:
                        template = template.replace(item, f"@{client['AE'].split(',')[1]}")
                    else:
                        template = template.replace(f"@{last_client['AE'].split(',')[1]}", f"@{client['AE'].split(',')[1]}")
                elif item == '(AGE)':
                    if i == 0:
                        template = template.replace(item, client['Age'])
                    else:
                        template = template.replace(last_client['Age'], client['Age'])
                elif item == '(CLIENT)':
                    if i == 0:
                        template = template.replace(item, client['Name'].split(' ')[0])
                    else:
                        template = template.replace(last_client['Name'].split(' ')[0], client['Name'].split(' ')[0])

            last_client = client
            mail.Subject = subject
            mail.HTMLBody = template
        else:
            mail.Subject = 'Gartner Platform Overview'
            mail.HTMLBody = f"""Hello <b>{client['Name'].split(' ')[0]},</b>
        
                    <br><br>I am reaching out to schedule some time for your Gartner platform overview. This session is a 30 minute introduction to the resources you have access to on the Gartner.com portal. We do strongly encourage you to take advantage of this onboarding session as it does come as part of your service and this introductory call will allow us to customize the portal to best suit your needs.
        
                    <br><br>Please see below for my most current availability and I look forward to connecting with you soon!
        
                    <br><br><b>Scheduling:</b> {'www.scheduling.com'}
        
                    <br><br>Best,
        
                    <br><br>{'Caio'} {'Cardoso'}<br>Client Onboarding Specialist-NCE | Gartner"""
        # mail.Send()
        i += 1
        mail.Display()


def send_emails_ae(clients, template=None, subject=None):
    outlook = win32com.client.Dispatch('outlook.application')
    template = template
    to_change = ['(AGE)', '(CLIENT)', '(ORG)', '(AE)']
    i = 0
    last_client = None
    for client in clients:
        mail = outlook.CreateItem(0)
        mail.To = f'{client["AE"]};'
        mail.CC = 'Conley, Ashlee;'
        if template and subject:
            for item in to_change:
                if item == '(AE)':
                    if i == 0:
                        template = template.replace(item, client['AE'].split(',')[1])
                    else:
                        template = template.replace(last_client['AE'].split(',')[1], client['AE'].split(',')[1])
                elif item == '(AGE)':
                    if i == 0:
                        template = template.replace(item, client['Age'])
                    else:
                        template = template.replace(last_client['Age'], client['Age'])
                elif item == '(CLIENT)':
                    if i == 0:
                        template = template.replace(item, client['Client'])
                    else:
                        template = template.replace(last_client['Client'], client['Client'])
                elif item == '(ORG)':
                    if i == 0:
                        template = template.replace(item, client['Account'].title())
                    else:
                        template = template.replace(last_client['Account'].title(), client['Account'].title())
            last_client = client
            mail.Subject = subject
            mail.HTMLBody = template
        else:
            mail.Subject = 'Gartner Platform Overview'
            mail.HTMLBody = f"""Hello <b>{client['AE'].split(',')[1]},</b>
    
                    <br><br>I hope you are doing well! I am reaching out today because I have been trying to get a hold of 
                    {client['Client'].split(' ')[0]} from <b>{client['Account']}</b>. Have you been able to speak with them yet? I
                    would love to partner with you to help the client get off to a fast start with Gartner. I have also 
                    included my scheduling link below to make it easier in case you have an upcoming meeting with the client.
                    I look forward to getting {client['Client'].split(' ')[0]} up to speed. Thank you!
    
                    <br><br><b>Scheduling:</b> {'www.scheduling.com'}
    
                    <br><br>Best,
    
                    <br><br>{'Caio'} {'Cardoso'}<br>Client Onboarding Specialist-NCE | Gartner"""
        # mail.Send()
        i += 1
        mail.Display()

def send_emails_ae_unified(clients):
    outlook = win32com.client.Dispatch('outlook.application')
    last_ae = ''
    mail_list = []
    html_tags = []
    for client in clients:

        # mail.Send()
        if last_ae == '':
            mail_list.append(client)
            last_ae = client["AE"]
        elif last_ae == f'{client["AE"]}':
            mail_list.append(client)
        else:
            print('False')
            return False

    for client in mail_list:
        html_tags.append(f'<li>{client["Client"]}</li>')
    mail = outlook.CreateItem(0)
    mail.To = f'{last_ae};'
    mail.CC = 'Conley, Ashlee;'
    mail.Subject = 'Gartner Platform Overview'
    mail.HTMLBody = f"""Hello <b>{last_ae.split(',')[1]},</b>

                    <br><br>I hope you are doing well! I am reaching out today because I have been trying to get a hold of the following
                    clients from <b>{mail_list[0]['Account']}</b>:<br><br><b>{[client["Client"] for client in mail_list]}</b>
                    <br><br>Have you been able to speak with any of them yet? I
                    would love to partner with you to help the team get off to a fast start with Gartner. I have also 
                    included my scheduling link below to make it easier in case you have an upcoming meeting with the client.
                    I look forward to helping get the whole team up to speed. Thank you!

                    <br><br><b>Scheduling:</b> {'www.scheduling.com'}

                    <br><br>Best,

                    <br><br>{'Caio'} {'Cardoso'}<br>Client Onboarding Specialist-NCE | Gartner"""
    # mail.Send()
    mail.Display()



