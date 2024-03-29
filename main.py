import csv
from langdetect import detect
from monthly import all_months
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTime, QDate, QDateTime, QEvent
from PyQt5 import uic, QtGui
import pandas
from datetime import datetime, timedelta
from communications import show_invites, send_emails, send_emails_ae, send_emails_ae_unified
from ui_functions import *
from calstuff import get_meeting_dict
USER = None
SELECTION = None
SELECTION_NAME = None
ACTIVITIES = []
ACTIONS_TAKEN = {}
IDIOMS = {'en': 'English',
          'pt': 'Portuguese',
          'es': 'Spanish',
          'fr': 'French'
          }

custom_meeting_subjects = {}
auto_meeting_subjects = {'Su llamada con Gartner': True,
                         'Your Gartner Call': True}

ICONS = ['iconz\\test_icon_disabled.png', 'iconz\\cal_reg.png', 'iconz\\hand_reg.png', 'iconz\\plane_reg.png',
         'iconz\\profile_reg.png']

DISABLED = ['iconz_disabled\\test_icon.png', 'iconz_disabled\\cal_dis.png', 'iconz_disabled\\hand_dis.png',
            'iconz_disabled\\plane_dis.png',
            'iconz_disabled\\profile_dis.png']

today = datetime.today()


def load_activity():
    global ACTIVITIES
    file = 'client_actions.csv'
    try:
        df = pandas.read_csv(file)
        for index, row in df.iterrows():
            # create an instance of the class and append it to the list

            activity = Activity(name=row['client_name'],
                                action_age=row['days_aged'],
                                emails_sent=row['email_sent'],
                                bi_sent=row['bi_sent'],
                                ae_outreaches=row['ae_outreach'],
                                last_action=row['last'],
                                lad=row['last_action_date'])
            ACTIONS_TAKEN[activity.name] = activity.last_action
            ACTIVITIES.append(activity)
            # print(activity.name, activity.last_action)
        return True
    except:

        return False


def load_user():
    try:
        file = 'catcher2.csv'
        df = pandas.read_csv(file)
        for index, row in df.iterrows():
            # create an instance of the class and append it to the list
            # global USER
            first_name,last_name,manager,scheduling = row['First'], row['Last'], row['Manager'], row['Scheduling']
            print(first_name,last_name,manager,scheduling)
            break
            # return True
        user_languages = []
        file = 'language_selection.csv'
        df = pandas.read_csv(file)
        for index, row in df.iterrows():
            language = row['Languages']
            user_languages.append(language)
        user_recurrences = get_meeting_dict()
        user_subjects = {}
        file = 'user_subjects.csv'
        df = pandas.read_csv(file)
        for index, row in df.iterrows():
            subject = row['Subjects']
            custom_meeting_subjects[subject] = True
            language = detect(subject)
            try:
                language = IDIOMS[language]
            except Exception as e:
                print(e)
                pass
            user_subjects[language] = subject
        global USER
        USER = Person(name=first_name,
                      last=last_name,
                      manager=manager,
                      scheduling=scheduling,
                      languages=user_languages,
                      recurrences=user_recurrences,
                      subjects=user_subjects)
        print(USER.subjects)
        return True

    except Exception as e:
        print(e)
        return False


class Activity:
    def __init__(self, name, action_age, emails_sent, bi_sent, ae_outreaches, last_action, lad):
        self.name = name
        self.action_age = action_age
        self.emails_sent = emails_sent
        self.bi_sent = bi_sent
        self.ae_outreaches = ae_outreaches
        self.last_action = last_action
        self.lad = lad


class Event:
    def __init__(self, event_name, event_time, event_duration, event_pattern):
        self.event_name = event_name
        self.event_time = event_time
        self.event_duration = event_duration
        self.event_pattern = event_pattern


class Person:
    def __init__(self, name, last, manager, scheduling, languages, recurrences=None, subjects=None):
        self.name = name
        self.last = last
        self.manager = manager
        self.scheduling = scheduling
        self.languages = languages
        self.recurrences = recurrences
        self.subjects = subjects


class Client:
    def __init__(self,
                 date=None,
                 name=None,
                 email=None,
                 status=None,
                 ae=None,
                 age=None,
                 ppl_code=None,
                 stage=None,
                 country=None,
                 cpv=None,
                 dpv=None,
                 event_act=None,
                 inq=None,
                 org_name=None,
                 eng_lad=None,
                 eng_age=None,
                 extra=None,
                 mem_status=None,
                 meeting_status=None,
                 meeting=None,
                 price_plan=None):
        self.date = date
        self.name = name
        self.email = email
        self.status = status
        self.ae = ae
        self.age = age
        self.stage = stage
        self.ppl_code = ppl_code
        self.country = country
        self.cpv = cpv
        self.dpv = dpv
        self.event_act = event_act
        self.inq = inq
        self.org_name = org_name
        self.eng_lad = eng_lad
        self.eng_age = eng_age
        self.extra = extra
        self.mem_status = mem_status
        self.meeting_status = meeting_status
        self.meeting = meeting
        self.price_plan = price_plan

    close_date = None
    to_send = True
    mobile = None


    def is_engaged(self):
        engagement = [self.cpv, self.dpv, self.event_act, self.inq]
        for metric in engagement:
            if metric != 0:
                return True
        return False

    def is_over(self):
        return 13 <= self.age < 60

    def __repr__(self):
        return repr(f"Client Object: {self.name}")


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('home.ui', self)
        self.fname = None


        self.buttons = []
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.page_1 = self.findChild(QWidget, 'page_1')
        self.page_2 = self.findChild(QWidget, 'page_2')
        self.page_3 = self.findChild(QWidget, 'page_3')
        self.page_4 = self.findChild(QWidget, 'page_4')
        self.page_5 = self.findChild(QWidget, 'page_5')
        self.verticalLayoutBi = self.findChild(QVBoxLayout, 'verticalLayout_6')
        self.verticalLayoutAe = self.findChild(QVBoxLayout, 'verticalLayoutAE')
        self.VerticalLayoutOutreach = self.findChild(QVBoxLayout, 'verticalLayout_9')
        self.VerticalLayoutMetrics = self.findChild(QVBoxLayout, 'verticalLayout_2')
        self.Btn_Toggle = self.findChild(QPushButton, 'Btn_Toggle')
        self.Btn_Toggle.setIcon(QIcon('iconz\\menu_reg.png'))
        self.btn_page_1 = self.findChild(QPushButton, 'btn_page_1')
        self.buttons.append(self.btn_page_1)
        self.btn_page_2 = self.findChild(QPushButton, 'btn_page_2')
        self.btn_page_2.setEnabled(False)

        self.buttons.append(self.btn_page_2)
        self.btn_page_3 = self.findChild(QPushButton, 'btn_page_3')
        self.btn_page_3.setEnabled(False)
        self.buttons.append(self.btn_page_3)
        self.btn_page_4 = self.findChild(QPushButton, 'btn_page_4')
        self.btn_page_4.setEnabled(False)
        self.buttons.append(self.btn_page_4)
        self.btn_page_5 = self.findChild(QPushButton, 'btn_page_5')
        self.btn_page_5.setEnabled(False)
        self.buttons.append(self.btn_page_5)
        self.adjust_text()
        self.frame_left_menu = self.findChild(QFrame, 'frame_left_menu')
        self.loadButton = self.findChild(QPushButton, 'loadButton')
        self.loadButton.clicked.connect(self.open_file)
        self.stackedWidget.setCurrentWidget(self.page_1)
        self.selected(self.btn_page_1)
        # TOGGLE/BURGER MENU

        self.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))

        # PAGES
        ########################################################################

        # PAGE 1
        self.btn_page_1.clicked.connect(lambda: self.load_home())

        # PAGE 2
        self.btn_page_2.clicked.connect(lambda: self.load_data_bi())

        # PAGE 3
        self.btn_page_3.clicked.connect(lambda: self.load_data_ae())

        # PAGE 4
        self.btn_page_4.clicked.connect(lambda: self.load_data_outreach())

        # PAGE 5
        self.btn_page_5.clicked.connect(lambda: self.testing())

        # SHOW ==> MAIN WINDOW
        ########################################################################

        self.show()

        # ==> END ##

    months = {'1': [],
              '2': [],
              '3': [],
              '4': [],
              '5': [],
              '6': [],
              '7': [],
              '8': [],
              '9': [],
              '10': [],
              '11': [],
              '12': [],
              }
    object_list = []
    client_list = []
    selected_tab = None
    loaded_file = None
    people = []
    email_list = []

    def testing(self):
        self.selected(self.btn_page_5)
        if self.VerticalLayoutMetrics.isEmpty():
            window = MetricWindow()
            self.VerticalLayoutMetrics.addWidget(window)
            self.stackedWidget.setCurrentWidget(self.page_5)
        else:

            self.stackedWidget.setCurrentWidget(self.page_5)

    def load_home(self):
        self.selected(self.btn_page_1)
        self.stackedWidget.setCurrentWidget(self.page_1)

    def load_data_outreach(self):
        self.selected(self.btn_page_4)
        if self.VerticalLayoutOutreach.isEmpty():
            table_window = OutreachWindow()
            self.VerticalLayoutOutreach.addWidget(table_window)
            self.stackedWidget.setCurrentWidget(self.page_4)
        else:

            self.stackedWidget.setCurrentWidget(self.page_4)

    def load_data_ae(self):
        self.selected(self.btn_page_3)
        if self.verticalLayoutAe.isEmpty():
            table_window = AeWindow()
            self.verticalLayoutAe.addWidget(table_window)
            self.stackedWidget.setCurrentWidget(self.page_3)
        else:

            self.stackedWidget.setCurrentWidget(self.page_3)

    def open_file(self):
        self.client_list.clear()
        self.object_list.clear()
        try:
            self.fname = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Excel Files (*.xlsx)")

            sheet = pandas.read_excel(self.fname[0])
            self.loadButton.setText(f'File Selected: {self.fname[0].split("/")[-1]}')
            self.loaded_file = True
            status = QLabel(f'Working With - {self.fname[0].split("/")[-1]}')

            status.setStyleSheet('QLabel{color:gray; font: Arial; border:none} QStatusBar::item{border:none}')
            self.setStatusBar(QStatusBar(self))
            self.statusBar().addWidget(status)


        except:
            return False

        # Create a list of objects

        for index, row in sheet.iterrows():
            try:
                age = self.calculate_age(row['ACT_CREATE_DT'])
                eng_age = self.calculate_age(row['ENGAGEMENT_LAD'])
                client = Client(name=str(row['CLIENT_NAME']),
                                ae=str(row['AE_NAME']),
                                date=row['ACT_CREATE_DT'],
                                email=str(row['CLIENT_PRIMARY_EMAIL']),
                                status=row['OB_60_achieved'],
                                age=age,
                                ppl_code=row['PPL_CODE'],
                                stage=str(row['ACT_STATUS']),
                                country=str(row['ORG_COUNTRY']),
                                cpv=row['Cpv_In_30D_Post_Ob'],
                                dpv=row['Dpv_In_30D_Post_Ob'],
                                event_act=row['Event_Act_In_30D_Post_Ob'],
                                inq=row['Inq_In_30D_Post_Ob'],
                                org_name=row['ORG_NAME'],
                                eng_lad=row['ENGAGEMENT_LAD'],
                                eng_age=eng_age,
                                extra=row['ACT_REASON'],
                                mem_status=row['MEMBER_STATUS'],
                                price_plan=row['PRICE_PLAN_NAME']
                                )
            except Exception as e:
                print(e)
                break
            # print(f"{client.eng_age}{client.is_engaged()}")

            self.client_list.append(client)
            if client.age < 95:
                if client.stage == 'Closed Not Onboarded':
                    if client.extra == 'Placeholder/Seat Swap' or client.extra == 'Ineligible-Binder Changes' or client.extra == 'Ineligible-Renewal' or client.extra == 'Dual Service' or client.extra == 'Ineligible-Language Support':
                        pass
                    else:
                        self.months[str(client.date.month)].append(client)
                else:
                    if client.mem_status != 'INACTIVE':
                        self.months[str(client.date.month)].append(client)

        for j in range(len(self.client_list)):
            if self.client_list[j].is_over() and self.client_list[j].status == 0:
                self.object_list.append(self.client_list[j])
                self.email_list.append(self.client_list[j].email)
        i = 0
        for button in self.buttons:
            if not button.isEnabled():
                button.setEnabled(True)
                if self.frame_left_menu.width() == 100:
                    button.setIcon(QIcon(ICONS[i]))
            i += 1

    def load_data_bi(self):

        self.selected(self.btn_page_2)
        try:
            if self.verticalLayoutBi.isEmpty():
                table_window = BiWindow()
                self.verticalLayoutBi.addWidget(table_window)
                self.stackedWidget.setCurrentWidget(self.page_2)
            else:
                self.stackedWidget.setCurrentWidget(self.page_2)
        except Exception as e:
            print(e)

    def selected(self, button):
        if self.selected_tab:
            self.selected_tab.setStyleSheet('QPushButton {color: rgb(154, 154, 154);background-color: rgb(35, 35, 35);'
                                            'border: 0px solid;}'
                                            'QPushButton:hover {background-color: rgb(113, 113, 113);color: #ffffff;}')
        button.setStyleSheet('background-color: rgb(113, 113, 113); color: #7fcde1; border: 0px solid;')
        self.selected_tab = button

    def adjust_text(self):
        if self.frame_left_menu.width() == 100:
            i = 0
            for button in self.buttons:
                if len(button.text()) >= 8:
                    if button.isEnabled():
                        button.setText('')
                        button.setIcon(QIcon(ICONS[i]))
                    else:
                        button.setText('')
                        button.setIcon(QIcon(DISABLED[i]))
                i += 1

    @staticmethod
    def calculate_age(date):
        days = (today - date).days
        return days


class OutreachWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('outreach.ui', self)
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.table.cellDoubleClicked.connect(self.show_item_info)
        self.loadButton = self.findChild(QPushButton, 'pushButton_2')
        self.customize = self.findChild(QPushButton, 'pushButton_3')
        self.checkboxes = []
        self.dialog = TemplateEdit(self)
        # self.text_edit = self.dialog.findChild(QTextEdit, 'textEdit')
        # self.line = self.dialog.findChild(QLineEdit, 'lineEdit_2')
        # self.template_ok = self.dialog.findChild(QPushButton, 'pushButton')
        self.custom_check = self.findChild(QCheckBox, 'checkBox')
        self.pushButton.clicked.connect(lambda: self.create_list())
        self.loadButton.clicked.connect(lambda: self.load_table())
        self.customize.clicked.connect(lambda: self.open_editor())
        self.custom_check.clicked.connect(lambda: self.customize_template())

        self.object_list = MainWindow.object_list
        self.list = []
        for i in range(len(self.object_list)):
            if self.object_list[i].stage != 'Closed Not Onboarded':
                self.list.append(self.object_list[i])
        # sort and filter the list for client stages/status (specific to blind invite window will vary for AE
        self.sorted_list = sorted(self.list, key=lambda x: x.ae)

        self.show()

    change_template = False
    template = None
    subject = None
    info = None

    def show_item_info(self, row, col):
        item = self.table.item(row, col)
        if item and '@' not in item.text():
            self.info = self.get_item_info(item.text())
            if self.info:
                client_card = ClientView(self)
                client_card.show()
        else:
            pass

    def get_item_info(self, name):
        if name:
            try:
                for client in MainWindow.client_list:
                    if name == client.name:
                        return [client.name, client.email, client.ae, client.age, client.stage, client.ppl_code, client.meeting_status, client.meeting]
            except:
                return False

    def open_editor(self):
        if self.dialog.isHidden():
            self.dialog.show()

    def checkbox_toggled(self, state):
        print(f'toggled: {state}')
        print(self.windowOpacity())

    def see_through(self):
        pass

    def customize_template(self):
        
        if self.custom_check.isChecked():
            print('checked')
            if self.subject:
                self.custom_check.setText(f'Template Selected: {self.subject}')
                self.customize.setEnabled(False)
                self.change_template = True
            else:
                print('Unchecked')
                self.custom_check.setChecked(False)
        else:
            print('Unchecked')
            self.custom_check.setText(f'Use Custom Template')
            self.change_template = False
            self.customize.setEnabled(True)

    # function called when return statement hits needs to take in template parameter if checkbox marked
    def create_list(self):
        data = []
        header_labels = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        for i in range(self.table.rowCount()):
            # checkbox_outer_widget = self.table.cellWidget(i, 0)
            checkbox = self.table.cellWidget(i, 0)
            if checkbox.isChecked():
                row_data = {}
                for j in range(1, self.table.columnCount()):
                    if j != 6:
                        item = self.table.item(i, j)
                    else:
                        item = self.table.cellWidget(i, j)

                    if item is not None:
                        row_data[header_labels[j]] = item.text()
                # updating last_action dictionary
                if ACTIONS_TAKEN.get(row_data['Name']):
                    ACTIONS_TAKEN[row_data['Name']] = 'email_sent'
                else:
                    ACTIONS_TAKEN[row_data['Name']] = 'email_sent'
                data.append(row_data)
        print(data)
        from tracking import track_actions
        track_actions(act='email_sent', data=data)
        if self.change_template:
            return send_emails(data, self.template, self.subject, user=USER)
        return send_emails(data, user=USER)

    def load_table(self):
        if self.table.columnCount() > 1:
            self.table.clear()
            self.table.setColumnCount(0)
            self.table.setRowCount(0)
            print('Already Loaded')

            return self.load_table()

        # Set the column headers to be the object's attributes
        attributes = ['', "Name", 'Email', "Age", "Status", "AE", 'Country']
        self.table.setColumnCount(len(attributes))
        self.table.setHorizontalHeaderLabels(attributes)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Add the objects' data to the table
        for i, obj in enumerate(self.sorted_list):
            # print(i)
            self.table.insertRow(i)
            # insert row checkbox
            checkbox_item = QCheckBox()
            checkbox_item.setChecked(False)
            checkbox_item.stateChanged.connect(self.checkbox_toggled)
            self.checkboxes.append(checkbox_item)

            self.table.setCellWidget(i, 0, checkbox_item)
            # print('item 1')
            self.table.setItem(i, 1, QTableWidgetItem(obj.name))
            # print('item 2')
            self.table.setItem(i, 2, QTableWidgetItem(obj.email))
            # print('item 3')
            self.table.setItem(i, 3, QTableWidgetItem(str(obj.age)))
            self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)

            # color of aging clients
            if obj.age >= 35:
                self.table.item(i, 3).setForeground(Qt.red)
            elif obj.age >= 20:
                self.table.item(i, 3).setForeground(Qt.darkYellow)
            else:
                self.table.item(i, 3).setForeground(Qt.darkGreen)
            # print('item 4')
            if ACTIONS_TAKEN.get(obj.name):
                if ACTIONS_TAKEN[obj.name] == 'bi_sent':
                    self.table.setItem(i, 4, QTableWidgetItem(f"BI - {obj.stage}"))
                elif ACTIONS_TAKEN[obj.name] == 'email_sent':
                    self.table.setItem(i, 4, QTableWidgetItem(f"Emailed - {obj.stage}"))
                elif ACTIONS_TAKEN[obj.name] == 'ae_outreach':
                    self.table.setItem(i, 4, QTableWidgetItem(f"RTS - {obj.stage}"))
            else:
                self.table.setItem(i, 4, QTableWidgetItem(obj.stage))
            # print('item 5')
            self.table.setItem(i, 5, QTableWidgetItem(obj.ae))
            # print('item 6')

            self.table.setItem(i, 6, QTableWidgetItem(str(obj.country)))
            self.table.item(i, 6).setTextAlignment(Qt.AlignCenter)
            # print('item 7')

        self.table.resizeColumnsToContents()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.adjustSize()


class AeWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ae_window.ui', self)
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.table.cellDoubleClicked.connect(self.show_item_info)
        self.loadButton = self.findChild(QPushButton, 'pushButton_2')
        self.sendUnifiedButton = self.findChild(QPushButton, 'pushButton_3')
        self.customize = self.findChild(QPushButton, 'pushButton_4')
        self.dialog = TemplateEdit(self)
        self.custom_check = self.findChild(QCheckBox, 'checkBox')
        self.checkboxes = []
        self.pushButton.clicked.connect(lambda: self.create_list())
        self.loadButton.clicked.connect(lambda: self.load_table())
        self.sendUnifiedButton.clicked.connect(lambda: self.create_unified_list())
        self.customize.clicked.connect(lambda: self.open_editor())
        self.custom_check.clicked.connect(lambda: self.customize_template())

        # algorithmically suggest times from outlook
        # self.pyt = find_times(self.calendar[0], duration=30, date_range=self.calendar[1], start=self.calendar[2])

        self.object_list = MainWindow.object_list
        self.list = []
        for i in range(len(self.object_list)):
            if self.object_list[i].stage != 'Closed Not Onboarded':
                if type(self.object_list[i].eng_age) != type(3):
                    self.object_list[i].eng_age = 'Not Engaged'
                    self.list.append(self.object_list[i])
                elif self.object_list[i].eng_age < 60:
                    self.list.append(self.object_list[i])
                else:
                    self.object_list[i].eng_age = 'Not Engaged'
                    self.list.append(self.object_list[i])
        # sort and filter the list for client stages/status (specific to blind invite window will vary for AE
        self.sorted_list = sorted(self.list, key=lambda x: x.ae)

        self.show()

    change_template = False
    template = None
    subject = None

    info = None

    def show_item_info(self, row, col):
        item = self.table.item(row, col)
        if item and '@' not in item.text():
            self.info = self.get_item_info(item.text())
            if self.info:
                client_card = ClientView(self)
                client_card.show()
        else:
            pass

    def get_item_info(self, name):
        if name:
            try:
                for client in MainWindow.client_list:
                    if name == client.name:
                        return [client.name, client.email, client.ae, client.age, client.stage, client.ppl_code, client.meeting_status, client.meeting]
            except:
                return False

    def customize_template(self):

        if self.custom_check.isChecked():
            print('checked')
            if self.subject:
                self.custom_check.setText(f'Template Selected: {self.subject}')
                self.customize.setEnabled(False)
                self.change_template = True
            else:
                print('Unchecked')
                self.custom_check.setChecked(False)
        else:
            print('Unchecked')
            self.custom_check.setText(f'Use Custom Template')
            self.change_template = False
            self.customize.setEnabled(True)

    def open_editor(self):
        if self.dialog.isHidden():
            self.dialog.show()

    def checkbox_toggled(self, state):
        print(f'toggled: {state}')
        print(self.windowOpacity())

    def see_through(self):
        pass

    def create_unified_list(self):
        data = []
        header_labels = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        for i in range(self.table.rowCount()):
            # checkbox_outer_widget = self.table.cellWidget(i, 0)
            checkbox = self.table.cellWidget(i, 0)
            if checkbox.isChecked():
                row_data = {}
                for j in range(1, self.table.columnCount()):
                    if j != 6:
                        item = self.table.item(i, j)
                    else:
                        item = self.table.cellWidget(i, j)

                    if item is not None:
                        row_data[header_labels[j]] = item.text()
                data.append(row_data)
                if ACTIONS_TAKEN.get(row_data['Client']):
                    ACTIONS_TAKEN[row_data['Client']] = 'ae_outreach'
                else:
                    ACTIONS_TAKEN[row_data['Client']] = 'ae_outreach'
        print(data)
        if data:
            from tracking import track_actions
            track_actions(act='ae_outreach', data=data)
            return send_emails_ae_unified(data, user=USER)
        return False

    def create_list(self):
        data = []
        header_labels = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        for i in range(self.table.rowCount()):
            # checkbox_outer_widget = self.table.cellWidget(i, 0)
            checkbox = self.table.cellWidget(i, 0)
            if checkbox.isChecked():
                row_data = {}
                for j in range(1, self.table.columnCount()):
                    if j != 6:
                        item = self.table.item(i, j)
                    else:
                        item = self.table.cellWidget(i, j)

                    if item is not None:
                        row_data[header_labels[j]] = item.text()
                if ACTIONS_TAKEN.get(row_data['Client']):
                    ACTIONS_TAKEN[row_data['Client']] = 'ae_outreach'
                else:
                    ACTIONS_TAKEN[row_data['Client']] = 'ae_outreach'
                data.append(row_data)
        print(data)
        from tracking import track_actions
        track_actions(act='ae_outreach', data=data)
        if self.change_template:
            return send_emails_ae(data, self.template, self.subject, user=USER)
        return send_emails_ae(data, user=USER)

    # Connect the date time changed signal to the slot function and pass the row number
    def update_table(self, date_time, row_number):
        pass

    def load_table(self):
        if self.table.columnCount() > 1:
            self.table.clear()
            self.table.setColumnCount(0)
            self.table.setRowCount(0)
            print('Already Loaded')

            return self.load_table()

        # Set the column headers to be the object's attributes
        attributes = ['', "AE", 'Client', "Age", "Status", "Account", "Last Engaged", 'Country']
        self.table.setColumnCount(len(attributes))
        self.table.setHorizontalHeaderLabels(attributes)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Add the objects' data to the table
        for i, obj in enumerate(self.sorted_list):

            self.table.insertRow(i)
            # insert row checkbox
            checkbox_item = QCheckBox()
            checkbox_item.setChecked(False)
            checkbox_item.stateChanged.connect(self.checkbox_toggled)
            self.checkboxes.append(checkbox_item)

            self.table.setCellWidget(i, 0, checkbox_item)
            # print('item 1')
            self.table.setItem(i, 1, QTableWidgetItem(obj.ae))
            # print('item 2')
            self.table.setItem(i, 2, QTableWidgetItem(obj.name))
            # print('item 3')
            self.table.setItem(i, 3, QTableWidgetItem(str(obj.age)))
            self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)

            # color of aging clients
            if obj.age >= 35:
                self.table.item(i, 3).setForeground(Qt.red)
            elif obj.age >= 20:
                self.table.item(i, 3).setForeground(Qt.darkYellow)
            else:
                self.table.item(i, 3).setForeground(Qt.darkGreen)
            # print('item 4')
            if ACTIONS_TAKEN.get(obj.name):
                if ACTIONS_TAKEN[obj.name] == 'bi_sent':
                    self.table.setItem(i, 4, QTableWidgetItem(f"BI - {obj.stage}"))
                elif ACTIONS_TAKEN[obj.name] == 'email_sent':
                    self.table.setItem(i, 4, QTableWidgetItem(f"Emailed - {obj.stage}"))
                elif ACTIONS_TAKEN[obj.name] == 'ae_outreach':
                    self.table.setItem(i, 4, QTableWidgetItem(f"RTS - {obj.stage}"))
            else:
                self.table.setItem(i, 4, QTableWidgetItem(obj.stage))
            # print('item 5')
            self.table.setItem(i, 5, QTableWidgetItem(obj.org_name))
            # print('item 6')

            self.table.setItem(i, 6, QTableWidgetItem(str(obj.eng_age)))
            self.table.item(i, 6).setTextAlignment(Qt.AlignCenter)
            # print('item 7')
            self.table.setItem(i, 7, QTableWidgetItem(obj.country))
            self.table.item(i, 7).setTextAlignment(Qt.AlignCenter)
            # print('item 8')
        self.table.resizeColumnsToContents()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.adjustSize()


class BiWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('blind_invite.ui', self)
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.table.cellDoubleClicked.connect(self.show_item_info)
        self.loadButton = self.findChild(QPushButton, 'pushButton_2')
        self.checkboxes = []
        self.pushButton.clicked.connect(lambda: self.create_list())
        self.loadButton.clicked.connect(lambda: self.load_table())

        # algorithmically suggest times from outlook
        # self.pyt = find_times(self.calendar[0], duration=30, date_range=self.calendar[1], start=self.calendar[2])
        self.pyt = None
        self.object_list = MainWindow.object_list

        # sort and filter the list for client stages/status (specific to blind invite window will vary for AE
        self.sorted_list = sorted([self.object_list[i] for i in range(len(self.object_list))
                                   if self.object_list[i].stage != 'Webtour Scheduled' and self.object_list[i].stage !=
                                   'Closed Not Onboarded'],
                                  key=lambda x: x.age, reverse=True
                                  )

        self.show()

    bi_list = []
    info = None

    def show_item_info(self, row, col):
        item = self.table.item(row, col)
        if item:
            self.info = self.get_item_info(item.text())
            if self.info:
                client_card = ClientView(self)
                client_card.show()
        else:
            pass

    def get_item_info(self, name):
        if name:
            try:
                for client in MainWindow.client_list:
                    if name == client.name:
                        return [client.name, client.email, client.ae, client.age, client.stage, client.ppl_code, client.meeting_status, client.meeting]
            except:
                return False

    def checkbox_toggled(self, state):
        print(f'toggled: {state}')
        print(self.windowOpacity())

    def see_through(self):
        pass

    def create_list(self):
        data = []
        header_labels = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        for i in range(self.table.rowCount()):
            # checkbox_outer_widget = self.table.cellWidget(i, 0)
            checkbox = self.table.cellWidget(i, 0)
            if checkbox.isChecked():
                row_data = {}
                for j in range(1, self.table.columnCount()):
                    if j != 6:
                        item = self.table.item(i, j)
                    else:
                        item = self.table.cellWidget(i, j)

                    if item is not None:
                        row_data[header_labels[j]] = item.text()
                if ACTIONS_TAKEN.get(row_data['Name']):
                    ACTIONS_TAKEN[row_data['Name']] = 'bi_sent'
                else:
                    ACTIONS_TAKEN[row_data['Name']] = 'bi_sent'
                data.append(row_data)
        print(data)
        from tracking import track_actions
        track_actions(act='bi_sent', data=data)
        return show_invites(data, user=USER)

    # Connect the date time changed signal to the slot function and pass the row number
    def update_table(self, date_time, row_number):
        print(type(date_time))
        selected_date = date_time.toPyDateTime()
        self.table.setItem(row_number, 7, QTableWidgetItem(selected_date.strftime("%m/%d/%Y %I:%M %p")))
        self.table.item(row_number, 7).setTextAlignment(Qt.AlignCenter)

    def load_table(self):
        if self.table.columnCount() > 1:
            self.table.clear()
            self.table.setColumnCount(0)
            self.table.setRowCount(0)
            print('Already Loaded')

            return self.load_table()

        from calstuff import get_conflicts, find_times
        self.pyt = find_times(get_conflicts(), 30, 30, length=len(self.sorted_list))
        # Set the column headers to be the object's attributes
        attributes = ['', "Name", 'Status', "Age", 'AE', "Email", 'Suggested Time', 'Edited Time', 'Country']
        self.table.setColumnCount(len(attributes))
        self.table.setHorizontalHeaderLabels(attributes)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Add the objects' data to the table
        for i, obj in enumerate(self.sorted_list):
            # print(i)
            self.table.insertRow(i)
            # insert row checkbox
            checkbox_item = QCheckBox()
            checkbox_item.setChecked(False)
            checkbox_item.stateChanged.connect(self.checkbox_toggled)
            self.checkboxes.append(checkbox_item)

            self.table.setCellWidget(i, 0, checkbox_item)

            self.table.setItem(i, 1, QTableWidgetItem(obj.name))

            if ACTIONS_TAKEN.get(obj.name):
                if ACTIONS_TAKEN[obj.name] == 'bi_sent':
                    self.table.setItem(i, 2, QTableWidgetItem(f"BI - {obj.stage}"))
                elif ACTIONS_TAKEN[obj.name] == 'email_sent':
                    self.table.setItem(i, 2, QTableWidgetItem(f"Emailed - {obj.stage}"))
                elif ACTIONS_TAKEN[obj.name] == 'ae_outreach':
                    self.table.setItem(i, 2, QTableWidgetItem(f"RTS - {obj.stage}"))
            else:
                self.table.setItem(i, 2, QTableWidgetItem(obj.stage))

            self.table.setItem(i, 3, QTableWidgetItem(str(obj.age)))
            self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)
            # color of aging clients
            if obj.age >= 35:
                self.table.item(i, 3).setForeground(Qt.red)
            elif obj.age >= 20:
                self.table.item(i, 3).setForeground(Qt.darkYellow)
            else:
                self.table.item(i, 3).setForeground(Qt.darkGreen)

            self.table.setItem(i, 4, QTableWidgetItem(str(obj.ae)))

            self.table.setItem(i, 5, QTableWidgetItem(obj.email))
            # insert date time edit
            self.date_time_picker = QDateTimeEdit()
            # suggesting most recent times for most aged clients
            date = QDateTime(QDate(self.pyt[i].year, self.pyt[i].month, self.pyt[i].day),
                             QTime(self.pyt[i].hour, self.pyt[i].minute, self.pyt[i].second))

            self.date_time_picker.setDateTime(date)
            self.date_time_picker.dateTimeChanged.connect(lambda date_time, row=i: self.update_table(date_time, row))
            self.table.setCellWidget(i, 6, self.date_time_picker)

            self.table.setItem(i, 8, QTableWidgetItem(obj.country))
            self.table.item(i, 8).setTextAlignment(Qt.AlignCenter)
        self.table.resizeColumnsToContents()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.adjustSize()


class BiMonth(BiWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('blind_invite.ui', self)
        self.label = self.findChild(QLabel, 'label')
        self.label.setText(f'{SELECTION_NAME} BI Workspace')

        self.list = []
        for item in SELECTION:
            if item.stage != 'Closed Onboarded':
                if item.stage == 'Waiting For Client' or item.stage == 'Holding' or item.stage == 'Webtour Scheduled':
                    if 14 <= item.age < 60:
                        self.list.append(item)

        self.sorted_list = sorted(self.list, key=lambda x: x.age, reverse=True)
        self.show()


class AeMonth(AeWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ae_window.ui', self)
        self.label = self.findChild(QLabel, 'label')
        self.label.setText(f'{SELECTION_NAME} AE Workspace')
        self.list = []
        for item in SELECTION:
            if 60 > item.age > 11 and item.stage != 'Closed Onboarded':
                if type(item.eng_age) != type(3):
                    item.eng_age = 'Not Engaged'
                    self.list.append(item)
                else:
                    self.list.append(item)
        self.sorted_list = sorted(self.list, key=lambda x: x.ae)
        print(self.sorted_list)
        self.show()


class OutreachMonth(OutreachWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('outreach.ui', self)
        self.label = self.findChild(QLabel, 'label')
        self.label.setText(f'{SELECTION_NAME} Outreaches')
        self.list = []
        for item in SELECTION:
            if item.stage != 'Closed Onboarded':
                if item.stage == 'Waiting For Client' or item.stage == 'Webtour Scheduled' or item.stage == 'Holding':
                    if 11 < item.age < 60:
                        self.list.append(item)
        self.sorted_list = sorted(self.list, key=lambda x: x.age)
        self.show()


class ClientView(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('client_info.ui', self)


        # self.dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.name_label = self.findChild(QLabel, 'name_label')
        self.name_label.setText(self.parentWidget().info[0])
        self.activity_label = self.findChild(QLabel, 'label_2')
        self.find_activity()
        self.meeting_status_label = self.findChild(QLabel, 'label_3')
        try:
            if self.parentWidget().info[6] == 3:
                self.meeting_status_label.setText(f"Accepted")
                self.meeting_status_label.setStyleSheet('color:#009933; font: 9pt Arial;')
            elif self.parentWidget().info[6] == 4:
                self.meeting_status_label.setText(f"Declined")
                self.meeting_status_label.setStyleSheet('color:#cc0000; font: 9pt Arial;')
            elif self.parentWidget().info[6] == 2:
                self.meeting_status_label.setText(f"Tentative")
                self.meeting_status_label.setStyleSheet('color:#e6e600; font: 9pt Arial;')
            elif self.parentWidget().info[6] == 0:
                self.meeting_status_label.setText(f"No Response")
            else:
                self.meeting_status_label.setText(f"")
        except:
            self.meeting_status_label.setText(f"")
        self.email_label = self.findChild(QLabel, 'email_label')
        self.email_label.setText(self.parentWidget().info[1])
        self.ae_label = self.findChild(QLabel, 'ae_label')
        self.ae_label.setText(self.parentWidget().info[2])
        self.age_label = self.findChild(QLabel, 'age_label')
        self.age_label.setText(str(self.parentWidget().info[3]))
        self.status_label = self.findChild(QLabel, 'status_label')
        self.status_label.setText(self.parentWidget().info[4])

        # self.doubleClicked.connect(self.dialog_double_clicked)
        self.reschedule = self.findChild(QPushButton, 'pushButton_4')
        self.reschedule.clicked.connect(lambda: self.reschedule_meeting())
        self.clip = self.findChild(QPushButton, 'pushButton_5')
        self.clip.clicked.connect(lambda: self.open_clip())
        self.ae_button = self.findChild(QPushButton, 'pushButton_2')
        self.ae_button.clicked.connect(lambda: self.message_ae())
        self.outreach_button = self.findChild(QPushButton, 'pushButton')
        self.outreach_button.clicked.connect(lambda: self.open_invite())

    def find_activity(self):
        for activity in ACTIVITIES:
            if self.name_label.text() == activity.name:
                print('good here')
                self.activity_label.setText(f"Last Action: {activity.last_action} {self.parentWidget().info[3] - activity.action_age} days ago")
                return True
        self.activity_label.setText('No Actions Yet')
        return False

    def message_ae(self):
        from communications import send_email
        send_email(client=self.parentWidget().info, to='partner', purpose=None, user=USER)
        from tracking import track_actions
        track_actions(act='ae_outreach', data=[{"Client": self.parentWidget().info[0],
                                                "Age": self.parentWidget().info[3]}])

    def reschedule_meeting(self):
        from communications import send_email
        send_email(client=self.parentWidget().info, to='client', purpose='reschedule', user=USER)
        if self.parentWidget().info[7]:
            self.parentWidget().info[7].Display()

    def open_invite(self):
        if self.parentWidget().info[7]:
            self.parentWidget().info[7].Display()
            from tracking import track_actions
            track_actions(act='bi_sent', data=[{"Client": self.parentWidget().info[0],
                                                "Age": self.parentWidget().info[3]}])

    def open_clip(self):
        import webbrowser
        webbrowser.open(f"https://scp.ssd.aws.gartner.com/#/{self.parentWidget().info[5]}")


class WeekView(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('week_table.ui', self)
        self.week_select = self.findChild(QComboBox, 'comboBox')
        self.load_button = self.findChild(QPushButton, 'pushButton')
        self.span_label = self.findChild(QLabel, 'label_2')
        self.table = self.findChild(QTableWidget, 'tableWidget')
        self.table.cellDoubleClicked.connect(self.show_item_info)
        self.clients = self.parentWidget().current_clients

        self.week_selection = self.week_select.currentText()
        self.week_select.activated[str].connect(self.on_activated)
        self.load_button.clicked.connect(lambda: self.load_table(self.week_selection))

    month_1 = None
    month_1_count = 0
    month_2 = None
    month_2_count = 0
    month_3 = None
    month_3_count = 0
    mon = []
    tues = []
    wed = []
    thurs = []
    fri = []
    weekly_clients = []
    info = None

    def show_item_info(self, row, col):
        item = self.table.item(row, col)
        if item and '@' not in item.text():
            self.info = self.get_item_info(item.text())
            client_card = ClientView(self)
            client_card.show()
        else:
            pass

    def discover_email(self, email):
        for client in MainWindow.client_list:
            if email.lower() == client.email.lower():
                return client
        return 'Unknown'

    def discover_exchange_name(self, name):
        try:
            if ',' in name:

                first_name = name.split(',')[1]

                if ' ' == first_name[0]:
                    first_name = first_name.split(' ')[1]
                    fixed_name = first_name + ' ' + name.split(',')[0]
                elif len(first_name.split(' ')) == 2:
                    first_name = first_name.split(' ')[0]
                    fixed_name = first_name + ' ' + name.split(',')[0]
                else:
                    fixed_name = name.split(',')[1] + ' ' + name.split(',')[0]
                # print(fixed_name)
            else:
                fixed_name = name

            for client in MainWindow.client_list:
                if client.name.lower() == fixed_name.lower():
                    return client
            return False
        except Exception as e:
            print(Exception)
            return False

    def get_item_info(self, name):
        if name:
            if name[0] == '✓' or name[3] == '-':
                if name[3] == '-':
                    name = name[5:]
                    print(name)
                else:
                    name = name[1:]
            elif 'SKO' in name:
                name = name[6:]

            for client in MainWindow.client_list:
                if name == client.name:
                    return [client.name, client.email, client.ae, client.age, client.stage, client.ppl_code, client.meeting_status, client.meeting]
            return 'NA'

    def on_activated(self, text):
        self.week_selection = text
        self.load_table(self.week_selection)
        print(self.week_selection)
        print(self.clients)

    def verify_meeting(self, attendee_list):
        try:
            for person in attendee_list:
                if '@' in person.Name:
                    if person.Name in MainWindow.email_list:
                        return True
                else:
                    ex_user = person.AddressEntry.GetExchangeUser()
                    # print(ex_user)
            return False
        except Exception as e:
            print(e)
            return False

    def load_table(self, text):
        self.table.clearContents()
        self.weekly_clients.clear()
        self.mon.clear()
        self.tues.clear()
        self.wed.clear()
        self.thurs.clear()
        self.fri.clear()
        self.span_label.setText('')
        from calstuff import get_meetings_week
        meetings = get_meetings_week(text)

        i = 0
        for meeting in meetings:
            # FILTERING FOR RELEVANT CLIENT MEETINGS COULD BE IMPROVED & ENCAPSULATED
            j = 0
            for key in meeting:
                if meeting[key].Subject in custom_meeting_subjects:
                    if i == 0:
                        self.mon.append(meeting[key])
                    elif i == 1:
                        self.tues.append(meeting[key])
                    elif i == 2:
                        self.wed.append(meeting[key])
                    elif i == 3:
                        self.thurs.append(meeting[key])
                    elif i == 4:
                        self.fri.append(meeting[key])

                elif 'Your Gartner Call' in meeting[key].Subject or 'Su llamada con Gartner' in meeting[key].Subject:
                    if i == 0:
                        self.mon.append(meeting[key])
                    elif i == 1:
                        self.tues.append(meeting[key])
                    elif i == 2:
                        self.wed.append(meeting[key])
                    elif i == 3:
                        self.thurs.append(meeting[key])
                    elif i == 4:
                        self.fri.append(meeting[key])

                else:
                    if self.verify_meeting(meeting[key].Recipients):

                        if i == 0:
                            self.mon.append(meeting[key])
                        elif i == 1:
                            self.tues.append(meeting[key])
                        elif i == 2:
                            self.wed.append(meeting[key])
                        elif i == 3:
                            self.thurs.append(meeting[key])
                        elif i == 4:
                            self.fri.append(meeting[key])

                j += 1
            i += 1
        self.weekly_clients = [sorted(self.mon, key=lambda x: x.Start.time()),
                               sorted(self.tues, key=lambda x: x.Start.time()),
                               sorted(self.wed, key=lambda x: x.Start.time()),
                               sorted(self.thurs, key=lambda x: x.Start.time()),
                               sorted(self.fri, key=lambda x: x.Start.time())]
        print(self.weekly_clients)
        try:
            span = f"Viewing: {self.weekly_clients[0][0].Start.date().strftime('%m/%d/%Y')} - {self.weekly_clients[-1][0].Start.date().strftime('%m/%d/%Y')}"
        except:
            span = 'Viewing: Next Week'
        self.span_label.setText(span)
        self.span_label.setStyleSheet('font: 12pt Arial')
        # loading table
        try:
            for col_index, day in enumerate(self.weekly_clients):
                meetings = self.weekly_clients[col_index]

                for row_index, meeting in enumerate(meetings):

                    client_email = 'emailnotfound@gartner.com'
                    meeting_type = None
                    # determining which email belongs to client to populate weekly table
                    for recipient in meeting.Recipients:
                        # checking if address is exchange address or regular smtp address
                        if recipient.AddressEntry.GetExchangeUser() is not None:
                            exchange_user = recipient.AddressEntry.GetExchangeUser()
                            if len(exchange_user.PrimarySmtpAddress) > 1:
                                continue
                            if self.discover_exchange_name(exchange_user.Name):
                                middle_man = self.discover_exchange_name(exchange_user.Name)
                                client_email = middle_man.email
                                middle_man.meeting_status = recipient.MeetingResponseStatus
                                middle_man.meeting = meeting
                            else:
                                continue
                            meeting_type = meeting.Subject
                        # EXTRA check to verify actual client email and not associate email
                        elif ',' not in recipient.Name and recipient.Type == 1:
                            client_email = recipient.Address
                            middle_man = self.discover_email(client_email)
                            if not isinstance(middle_man, str):
                                middle_man.meeting_status = recipient.MeetingResponseStatus
                                middle_man.meeting = meeting
                            meeting_type = meeting.Subject

                    match_found = False
                    # looping through clients in 'oldest' month
                    for client in self.clients[0]:
                        if client_email.lower() == client.email.lower():

                            self.month_1 = self.parentWidget().month_names[0]
                            self.month_1_count += 1
                            if client.stage == 'Closed Onboarded':
                                self.table.setItem(row_index, col_index, QTableWidgetItem(f"✓{client.name}"))
                            elif "Your Gartner Call" not in meeting_type:
                                if meeting_type in custom_meeting_subjects:
                                    self.table.setItem(row_index, col_index, QTableWidgetItem(f"BI - {client.name}"))
                                else:
                                    self.table.setItem(row_index, col_index, QTableWidgetItem(f"SKO - {client.name}"))
                            else:
                                self.table.setItem(row_index, col_index, QTableWidgetItem(client.name))
                            self.table.item(row_index, col_index).setForeground(Qt.red)
                            self.table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
                            match_found = True
                            break
                    # looping through clients in 'middle' month
                    for client in self.clients[1]:
                        if client_email.lower() == client.email.lower():

                            self.month_2 = self.parentWidget().month_names[1]
                            self.month_2_count += 1
                            if client.stage == 'Closed Onboarded':
                                self.table.setItem(row_index, col_index, QTableWidgetItem(f"✓{client.name}"))
                            elif "Your Gartner Call" not in meeting_type:
                                if meeting_type in custom_meeting_subjects:
                                    self.table.setItem(row_index, col_index, QTableWidgetItem(f"BI - {client.name}"))
                                else:
                                    self.table.setItem(row_index, col_index, QTableWidgetItem(f"SKO - {client.name}"))
                            else:
                                self.table.setItem(row_index, col_index, QTableWidgetItem(client.name))
                            self.table.item(row_index, col_index).setForeground(Qt.darkYellow)
                            self.table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
                            match_found = True
                            break
                    # looping through clients in 'newest' month
                    for client in self.clients[2]:
                        if client_email.lower() == client.email.lower():

                            self.month_3 = self.parentWidget().month_names[2]
                            self.month_3_count += 1
                            if client.stage == 'Closed Onboarded':
                                self.table.setItem(row_index, col_index, QTableWidgetItem(f"✓{client.name}"))
                            elif "Your Gartner Call" not in meeting_type:
                                if meeting_type in custom_meeting_subjects:
                                    self.table.setItem(row_index, col_index, QTableWidgetItem(f"BI - {client.name}"))
                                else:
                                    self.table.setItem(row_index, col_index, QTableWidgetItem(f"SKO - {client.name}"))
                            else:
                                self.table.setItem(row_index, col_index, QTableWidgetItem(client.name))
                            self.table.item(row_index, col_index).setForeground(Qt.darkGreen)
                            self.table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
                            match_found = True
                            break
                    if not match_found:
                        # searches entire client list for client email (usually wrong email or out of OB60 range)
                        response = self.discover_email(client_email)
                        if response != 'Unknown':

                            if response.stage == 'Closed Onboarded':
                                self.table.setItem(row_index, col_index, QTableWidgetItem(f"✓{response.name}"))
                            elif "Your Gartner Call" not in meeting_type:
                                if meeting_type in custom_meeting_subjects:
                                    self.table.setItem(row_index, col_index, QTableWidgetItem(f"BI - {response.name}"))
                                else:
                                    self.table.setItem(row_index, col_index, QTableWidgetItem(f"SKO - {response.name}"))
                            else:
                                self.table.setItem(row_index, col_index, QTableWidgetItem(response.name))

                            if self.month_1 == all_months[response.date.month]:
                                self.table.item(row_index, col_index).setForeground(Qt.red)
                                self.table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
                            elif self.month_2 == all_months[response.date.month]:
                                self.table.item(row_index, col_index).setForeground(Qt.darkYellow)
                                self.table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
                            elif self.month_3 == all_months[response.date.month]:
                                self.table.item(row_index, col_index).setForeground(Qt.darkGreen)
                                self.table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
                            else:
                                self.table.item(row_index, col_index).setForeground(Qt.gray)
                                self.table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
                        else:
                            self.table.setItem(row_index, col_index, QTableWidgetItem(client_email))
                            self.table.item(row_index, col_index).setForeground(Qt.gray)
                            self.table.item(row_index, col_index).setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            print(e)


class MetricWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('metrics.ui', self)
        self.frame_1 = self.findChild(QFrame, 'frame_1')
        self.frame_2 = self.findChild(QFrame, 'frame_2')
        self.frame_3 = self.findChild(QFrame, 'frame_3')
        # grab labels
        self.totalLabel_1 = self.findChild(QLabel, 'totalLabel_1')
        self.totalLabel_2 = self.findChild(QLabel, 'totalLabel_2')
        self.totalLabel_3 = self.findChild(QLabel, 'totalLabel_3')

        self.monthLabel_1 = self.findChild(QLabel, 'monthLabel_1')
        self.monthLabel_2 = self.findChild(QLabel, 'monthLabel_2')
        self.monthLabel_3 = self.findChild(QLabel, 'monthLabel_3')

        self.obLabel_1 = self.findChild(QLabel, 'obLabel_1')
        self.obLabel_2 = self.findChild(QLabel, 'obLabel_2')
        self.obLabel_3 = self.findChild(QLabel, 'obLabel_3')

        self.oppLabel_1 = self.findChild(QLabel, 'oppLabel_1')
        self.oppLabel_2 = self.findChild(QLabel, 'oppLabel_2')
        self.oppLabel_3 = self.findChild(QLabel, 'oppLabel_3')

        self.maxLabel_1 = self.findChild(QLabel, 'maxLabel_1')
        self.maxLabel_2 = self.findChild(QLabel, 'maxLabel_2')
        self.maxLabel_3 = self.findChild(QLabel, 'maxLabel_3')

        # identify buttons
        self.weekButton = self.findChild(QPushButton, 'weekButton')
        self.weekButton.clicked.connect(lambda: self.open_calendar())
        self.select_1 = self.findChild(QPushButton, 'select_1')
        self.select_1.clicked.connect(lambda: self.selection(1))
        self.select_2 = self.findChild(QPushButton, 'select_2')
        self.select_2.clicked.connect(lambda: self.selection(2))
        self.select_3 = self.findChild(QPushButton, 'select_3')
        self.select_3.clicked.connect(lambda: self.selection(3))

        self.aeButton = self.findChild(QPushButton, 'aeButton')
        self.aeButton.clicked.connect(lambda: self.open_ae())
        self.biButton = self.findChild(QPushButton, 'biButton')
        self.biButton.clicked.connect(lambda: self.open_bi())
        self.outreachButton = self.findChild(QPushButton, 'outreachButton')
        self.outreachButton.clicked.connect(lambda: self.open_outreach())

        self.current_months = self.find_months(today)
        self.month_names = []

        for month in self.current_months:
            self.month_names.append(all_months[month])

        # set month titles
        self.monthLabel_1.setText(self.month_names[0])
        self.monthLabel_2.setText(self.month_names[1])
        self.monthLabel_3.setText(self.month_names[2])

        self.monthly_clients = self.get_monthly_clients(self.current_months)
        print(self.monthly_clients)
        # grab and set totals
        self.first_month_total = len(self.monthly_clients[0])
        self.totalLabel_1.setText(str(len(self.monthly_clients[0])))
        self.second_month_total = len(self.monthly_clients[1])
        self.totalLabel_2.setText(str(len(self.monthly_clients[1])))
        self.third_month_total = len(self.monthly_clients[2])
        self.totalLabel_3.setText(str(len(self.monthly_clients[2])))

        self.quick_maths(self.monthly_clients)

        self.activity_button = self.findChild(QPushButton, 'activity_button')
        self.activity_button.clicked.connect(lambda: self.show_activities())
        self.show()

    active_month = None
    window_list = []
    current_clients = []
    activity_list = []

    def show_activities(self):
        activity_window = ActivityWindow(self)
        activity_window.show()

    def open_calendar(self):
        self.current_clients = self.monthly_clients
        print(self.current_clients)
        calendar = WeekView(self)
        calendar.show()

    def open_outreach(self):
        global SELECTION
        if SELECTION:
            outreach_window = OutreachMonth()

    def open_bi(self):
        global SELECTION
        if SELECTION:
            bi_window = BiMonth()

    def open_ae(self):
        global SELECTION
        if SELECTION:
            ae_window = AeMonth()

    def selection(self, selection):
        global SELECTION, SELECTION_NAME
        if selection == 1:
            if selection == self.active_month:
                return True
            self.frame_1.setStyleSheet('QLabel{border: 1px solid #7fcde1;'
                                       'border-radius: 4px}'
                                       )
            if self.active_month:
                self.deselection(self.active_month)

            SELECTION = self.monthly_clients[0]
            SELECTION_NAME = self.month_names[0]
            self.active_month = 1
        elif selection == 2:
            if selection == self.active_month:
                return True
            self.frame_2.setStyleSheet('QLabel{border: 1px solid #7fcde1;'
                                       'border-radius: 4px}')
            if self.active_month:
                self.deselection(self.active_month)

            SELECTION = self.monthly_clients[1]
            SELECTION_NAME = self.month_names[1]
            self.active_month = 2
        elif selection == 3:
            if selection == self.active_month:
                return True
            self.frame_3.setStyleSheet('QLabel{border: 1px solid #7fcde1;'
                                       'border-radius: 4px}')
            if self.active_month:
                self.deselection(self.active_month)

            SELECTION = self.monthly_clients[2]
            SELECTION_NAME = self.month_names[2]
            self.active_month = 3
        print(self.active_month)
        print(self.window_list)

    def deselection(self, frame):
        if frame == 1:
            self.frame_1.setStyleSheet('QFrame{background-color: rgb(38, 38, 38);}'
                                       'QLabel{border:none}')
        if frame == 2:
            self.frame_2.setStyleSheet('QFrame{background-color: rgb(38, 38, 38);}'
                                       'QLabel{border:none}')
        if frame == 3:
            self.frame_3.setStyleSheet('QFrame{background-color: rgb(38, 38, 38);}'
                                       'QLabel{border:none}')

    def quick_maths(self, clients):
        total_closed = []

        for month in clients:
            closed = 0
            for j in range(len(month)):
                if month[j].stage == 'Closed Onboarded':
                    closed += 1
            total_closed.append(closed)
            print(total_closed)
        ob_1 = total_closed[0]/int(self.totalLabel_1.text())
        self.findChild(QLabel, 'goal_1').setText(f"{int(round((.82 - ob_1) * int(self.totalLabel_1.text()), 0))}")
        self.obLabel_1.setText(f'{str(ob_1 * 100)[:4]}%')

        ob_2 = total_closed[1] / int(self.totalLabel_2.text())
        self.findChild(QLabel, 'goal_2').setText(f"{int(round((.82 - ob_2) * int(self.totalLabel_2.text()), 0))}")
        self.obLabel_2.setText(f'{str(ob_2 * 100)[:4]}%')

        # check if month has clients before dividing by 0
        if int(self.totalLabel_3.text()) != 0:
            ob_3 = total_closed[2] / int(self.totalLabel_3.text())
            self.findChild(QLabel, 'goal_3').setText(f"{int(round((.82 - ob_3) * int(self.totalLabel_3.text()), 0))}")
            self.obLabel_3.setText(f'{str(ob_3 * 100)[:4]}%')
        else:
            ob_3 = 0
            self.obLabel_3.setText(f'{str(ob_3)}%')
            self.findChild(QLabel, 'goal_3').setText("NA")
        opportunities = []

        for month in clients:
            opportunity_total = 0
            print(month)
            for j in range(len(month)):
                if month[j].stage != 'Closed Onboarded':
                    if month[j].age < 53 and month[j].stage != 'Closed Not Onboarded':
                        print(f"{month[j].stage} {month[j].age}")
                        opportunity_total += 1

            opportunities.append(opportunity_total)

        opp_1 = opportunities[0]
        self.oppLabel_1.setText(str(opp_1))
        print(opp_1)

        opp_2 = opportunities[1]
        self.oppLabel_2.setText(str(opp_2))
        print(opp_2)
        opp_3 = opportunities[2]
        self.oppLabel_3.setText(str(opp_3))

        rem_1 = (total_closed[0] + opp_1) / int(self.totalLabel_1.text())
        if rem_1 < .82:
            self.maxLabel_1.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: yellow;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        if rem_1 < .70:
            self.maxLabel_1.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: red;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        else:
            self.maxLabel_1.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: green;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        self.maxLabel_1.setText(f"{str(rem_1 * 100)[:4]}%")
        rem_2 = (total_closed[1] + opp_2) / int(self.totalLabel_2.text())
        if rem_2 < .82:
            self.maxLabel_2.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: yellow;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        elif rem_2 < .70:
            self.maxLabel_2.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: red;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        else:
            self.maxLabel_2.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: green;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        if rem_2 == 1:
            self.maxLabel_2.setText(f"{str(rem_2 * 100)[:3]}%")
        else:
            self.maxLabel_2.setText(f"{str(rem_2 * 100)[:4]}%")
        # check if month has clients before dividing by 0
        if int(self.totalLabel_3.text()) != 0:
            rem_3 = (total_closed[2] + opp_3) / int(self.totalLabel_3.text())
        else:
            rem_3 = 0
        if rem_3 < .70:
            self.maxLabel_3.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: red;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        elif rem_3 < .82:
            self.maxLabel_3.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: yellow;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        else:
            self.maxLabel_3.setStyleSheet('''font: 12pt Arial;
                                        font-weight: bold;
                                        color: green;
                                        background-color: rgb(79, 79, 79);
                                        border: 1px solid rgb(79, 79, 79);
                                        border-radius: 2px'''
                                          )
        if rem_3 == 1:
            self.maxLabel_3.setText(f"{str(rem_3 * 100)[:3]}%")
        elif rem_3 == 0:
            self.maxLabel_3.setText(f"NA")
        else:
            self.maxLabel_3.setText(f"{str(rem_3 * 100)[:4]}%")

    def find_months(self, td):
        first = td.month - 2
        second = td.month - 1
        if first == -1:
            first = 11
        elif first == 0:
            first = 12
        if second == 0:
            second = 12

        return [first, second, td.month]

    def get_monthly_clients(self, current_months):
        clients = []
        for month in current_months:

            clients.append(MainWindow.months.get(str(month)))
        return clients


class ActivityWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('activity_tracker.ui', self)
        from tracking import gather_activity_metrics
        activity_list = gather_activity_metrics(MainWindow.object_list, MainWindow.client_list)
        self.average_bi = self.findChild(QLabel, 'averageBI_number')
        self.average_bi.setText(str(round(activity_list[0], 1)))
        self.average_ae = self.findChild(QLabel, 'averageAE_number')
        self.average_ae.setText(str(round(activity_list[1], 1)))
        self.bi_per_client = self.findChild(QLabel, 'bi_per_client_number')
        self.bi_per_client.setText(str(round(activity_list[2], 1)))
        self.ae_per_client = self.findChild(QLabel, 'ae_per_client_number')
        self.ae_per_client.setText(str(round(activity_list[3], 1)))
        self.show()


class TestBox(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('register.ui', self)
        self.pages = []
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')

        self.welcome = self.findChild(QWidget, 'welcome')
        self.pages.append(self.welcome)
        self.stackedWidget.setCurrentWidget(self.welcome)
        self.nameEdit = self.welcome.findChild(QLineEdit, 'nameEdit')
        self.lastEdit = self.welcome.findChild(QLineEdit, 'lastEdit')
        self.managerEdit = self.welcome.findChild(QLineEdit, 'lineEdit')
        self.schedulingEdit = self.welcome.findChild(QLineEdit, 'schedulingEdit')
        self.errorLabel = self.welcome.findChild(QLabel, 'errorLabel')

        self.language_select = self.findChild(QWidget, 'language_select')
        self.spanish = self.language_select.findChild(QPushButton, 'spanish')
        self.spanish.clicked.connect(lambda: self.select_language(self.spanish))
        self.english = self.language_select.findChild(QPushButton, 'english')
        self.english.clicked.connect(lambda: self.select_language(self.english))
        self.portuguese = self.language_select.findChild(QPushButton, 'portuguese')
        self.portuguese.clicked.connect(lambda: self.select_language(self.portuguese))
        self.french = self.language_select.findChild(QPushButton, 'french')
        self.french.clicked.connect(lambda: self.select_language(self.french))
        self.japanese = self.language_select.findChild(QPushButton, 'japanese')
        self.japanese.clicked.connect(lambda: self.select_language(self.japanese))
        self.mandarin = self.language_select.findChild(QPushButton, 'mandarin')
        self.mandarin.clicked.connect(lambda: self.select_language(self.mandarin))
        self.pages.append(self.language_select)

        self.daily_recurrences = self.findChild(QWidget, 'daily_recurrences')
        self.eventEdit = self.daily_recurrences.findChild(QLineEdit, 'eventEdit')
        self.timeEdit = self.daily_recurrences.findChild(QTimeEdit, 'timeEdit')
        self.durationEdit = self.daily_recurrences.findChild(QSpinBox, 'durationEdit')
        self.addDaily = self.daily_recurrences.findChild(QPushButton, 'addDaily')
        self.addDaily.clicked.connect(self.add_daily_event)
        self.pages.append(self.daily_recurrences)

        self.weekly_recurrences = self.findChild(QWidget, 'weekly_recurrences')
        self.eventEdit_2 = self.weekly_recurrences.findChild(QLineEdit, 'eventEdit_2')
        self.weekSelect = self.weekly_recurrences.findChild(QComboBox, 'weekSelect')
        self.timeEdit_2 = self.weekly_recurrences.findChild(QTimeEdit, 'timeEdit_2')
        self.durationEdit_2 = self.weekly_recurrences.findChild(QSpinBox, 'durationEdit_2')
        self.addWeekly = self.weekly_recurrences.findChild(QPushButton, 'addWeekly')
        self.addWeekly.clicked.connect(self.add_weekly_event)
        self.pages.append(self.weekly_recurrences)

        self.subject = self.findChild(QWidget, 'subject')
        self.subjectEdit = self.subject.findChild(QLineEdit, 'subjectEdit')
        self.addSubject = self.subject.findChild(QPushButton, 'addSubject')
        self.addSubject.clicked.connect(self.add_subject)
        self.pages.append(self.subject)

        self.continue_1 = self.welcome.findChild(QPushButton, 'continue_1')
        self.continue_2 = self.language_select.findChild(QPushButton, 'continue_2')
        self.continue_3 = self.daily_recurrences.findChild(QPushButton, 'saveDaily')
        self.continue_4 = self.weekly_recurrences.findChild(QPushButton, 'saveWeekly')
        self.finalize = self.subject.findChild(QPushButton, 'finalizeButton')

        self.continue_1.clicked.connect(lambda: self.save_user())
        self.continue_2.clicked.connect(lambda: self.save_languages())
        self.continue_3.clicked.connect(self.next_page)
        self.continue_4.clicked.connect(lambda: self.save_events())
        self.finalize.clicked.connect(lambda: self.finalize_all())

        self.show()

    idx = 0
    user_languages = []
    user_events = []
    user_subjects = []

    def select_language(self, language):
        if language.isChecked():
            language.setStyleSheet('QPushButton{background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ff9d00, stop: 1 #ffb900);'
                                   'color: white;}')
            print(f'Selected: {language.text()}')
            self.user_languages.append(language.text())
            print(self.user_languages)
        else:

            language.setStyleSheet("QPushButton{background-color: rgb(217, 217, 217);"
                                   "color: rgb(222, 222, 222);"
                                   "color: rgb(125, 125, 125);"
                                   "border: 1px solid #7fcde1;"
                                   "border-radius: 2px;"
                                   "padding: 4px;"
                                   "font: 10pt 'Arial';"
                                   "height: 25px;}"
                                   "QPushButton:hover{"
                                   "background: rgb(241, 241, 241);"
                                   "font: rgb(186, 186, 186);"
                                   "color: rgb(176, 176, 176);}")
            print(f'Deselected: {language.text()}')
            self.user_languages.remove(language.text())
            print(self.user_languages)

    def add_subject(self):
        try:
            self.user_subjects.append(self.subjectEdit.text())
            self.subjectEdit.clear()
        except:
            pass

    def save_events(self):
        if len(self.user_events) < 1:
            return False
        else:
            data = {"Meeting Name": [event.event_name for event in self.user_events],
                    "Meeting Time": [event.event_time for event in self.user_events],
                    "Meeting Duration": [event.event_duration for event in self.user_events],
                    "Recurrence Pattern": [event.event_pattern for event in self.user_events]}
            df = pandas.DataFrame(data).set_index('Meeting Name')
            df.to_csv('recurring_events.csv')
            self.next_page()

    def add_weekly_event(self):
        try:
            event = Event(event_name=self.eventEdit_2.text(),
                          event_time=self.timeEdit_2.time().toPyTime(),
                          event_duration=self.durationEdit_2.text(),
                          event_pattern=self.weekSelect.currentText())
            self.eventEdit_2.clear()
            self.timeEdit_2.setTime(QTime(12, 0))
            self.weekSelect.setCurrentText('Monday')
            self.user_events.append(event)
            print(f'event added: {event.event_name} {event.event_time}')
        except Exception as e:
            print(e)
            pass

    def add_daily_event(self):
        try:
            event = Event(event_name=self.eventEdit.text(),
                          event_time=self.timeEdit.time().toPyTime(),
                          event_duration=self.durationEdit.text(),
                          event_pattern='Daily')
            self.eventEdit.clear()
            self.timeEdit.setTime(QTime(12, 0))
            self.user_events.append(event)
            print('event added')
        except Exception as e:
            print(e)
            pass

    def next_page(self):
        if self.idx < 4:
            self.idx += 1
            self.stackedWidget.setCurrentWidget(self.pages[self.idx])

    def verify_user_fields(self):
        if len(self.nameEdit.text()) > 3 and len(self.lastEdit.text()) > 3 and '@' in self.managerEdit.text():
            if len(self.managerEdit.text()) > 10:
                return True
        return False

    def save_languages(self):
        if len(self.user_languages) < 1:
            pass
        else:
            data = {'Languages': self.user_languages}
            df = pandas.DataFrame(data)
            df.to_csv('language_selection.csv')
            self.next_page()

    def save_user(self):
        columns = ['First', 'Last', 'Manager', 'Scheduling']
        if self.verify_user_fields():
            try:
                data = {'First': [self.nameEdit.text()],
                        'Last': [self.lastEdit.text()],
                        'Manager': [self.managerEdit.text()],
                        'Scheduling': [self.schedulingEdit.text()],
                        }
            except Exception as e:
                print(e)
                data = {'First': [self.nameEdit.text()],
                        'Last': [self.lastEdit.text()],
                        'Manager': [self.managerEdit.text()],
                        'Scheduling': [''],
                        }
            df = pandas.DataFrame(data)
            df.to_csv(f'catcher2.csv',
                      index=False, header=True, columns=columns)
            # ACTIVATING MAIN WINDOW (WILL BE MOVED TO FINALIZE FUNCTION
            # start.setEnabled(True)
            # global USER
            # USER = True
            self.next_page()
        else:
            self.errorLabel.setText('Please make sure all required fields are filled in properly.')
        # self.close()

    def finalize_all(self):
        try:
            data = {'Subjects': self.user_subjects}
            df = pandas.DataFrame(data)
            df.to_csv('user_subjects.csv')
            start.setEnabled(True)
            global USER
            load_user()
            self.close()
        except Exception as e:
            print(e)
            pass


class TemplateEdit(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('template_editor.ui', self)
        self.parent = self.parentWidget()
        self.button = self.findChild(QPushButton, 'pushButton')

        self.textEdit = self.findChild(QTextEdit, 'textEdit')

        self.subject = self.findChild(QLineEdit, 'lineEdit_2')
        # self.subject.changeEvent(lambda: self.enable_button())
        self.subject.setFocus()
        self.button.clicked.connect(lambda: self.button_clicked())

    def button_clicked(self):
        if len(self.subject.text()) < 3:
            self.subject.setFocus()
            pass
        else:
            print('Clicked')
            self.parentWidget().template = self.textEdit.toHtml()
            self.parentWidget().subject = self.subject.text()

            self.close()


if __name__ == '__main__':
    app = QApplication([])
    if load_user():
        load_activity()
        start = MainWindow()

    else:
        start = MainWindow()
        start.setEnabled(False)
        test = TestBox()

    app.exec_()
