import csv
from monthly import all_months
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTime, QDate, QDateTime, QEvent
from PyQt5 import uic, QtGui
import pandas
from datetime import datetime, timedelta
from communications import show_invites, send_emails, send_emails_ae, send_emails_ae_unified
from ui_functions import *
USER = None
SELECTION = None
SELECTION_NAME = None


ICONS = ['iconz\\test_icon_disabled.png', 'iconz\\cal_reg.png', 'iconz\\hand_reg.png', 'iconz\\plane_reg.png',
         'iconz\\profile_reg.png']

DISABLED = ['iconz_disabled\\test_icon.png', 'iconz_disabled\\cal_dis.png', 'iconz_disabled\\hand_dis.png',
            'iconz_disabled\\plane_dis.png',
            'iconz_disabled\\profile_dis.png']

today = datetime.today()


def load_user():
    file = 'catcher.csv'
    try:
        df = pandas.read_csv(file)
        for index, row in df.iterrows():
            # create an instance of the class and append it to the list
            global USER
            USER = Person(row['First'], row['Last'], row['Scheduling'], row['Lunch'], row['Team Meeting'])
            return True
    except:

        return False


class Person:
    def __init__(self, name, last, scheduling, lunch, team_meeting):
        self.name = name
        self.last = last
        self.scheduling = scheduling
        self.lunch = lunch
        self.team_meeting = team_meeting


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
                 mem_status=None):
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
        return 14 <= self.age < 60


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

            age = self.calculate_age(row['ACT_CREATE_DT'])
            eng_age = self.calculate_age(row['ENGAGEMENT_LAD'])
            client = Client(name=str(row['CLIENT_NAME']),
                            ae=str(row['AE_NAME']),
                            date=row['ACT_CREATE_DT'],
                            email=str(row['CLIENT_PRIMARY_EMAIL']),
                            status=row['New_OBC_In_60_Days'],
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
                            mem_status=row['MEMBER_STATUS']
                            )

            #print(f"{client.eng_age}{client.is_engaged()}")

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
        i = 0
        for button in self.buttons:
            if not button.isEnabled():
                button.setEnabled(True)
                if self.frame_left_menu.width() == 100:
                    button.setIcon(QIcon(ICONS[i]))
            i += 1

    def load_data_bi(self):

        self.selected(self.btn_page_2)
        if self.verticalLayoutBi.isEmpty():
            table_window = BiWindow()
            self.verticalLayoutBi.addWidget(table_window)
            self.stackedWidget.setCurrentWidget(self.page_2)
        else:
            self.stackedWidget.setCurrentWidget(self.page_2)

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
        self.loadButton = self.findChild(QPushButton, 'pushButton_2')
        self.customize = self.findChild(QPushButton, 'pushButton_3')
        self.checkboxes = []
        self.dialog = TemplateEdit(self)
        #self.text_edit = self.dialog.findChild(QTextEdit, 'textEdit')
        #self.line = self.dialog.findChild(QLineEdit, 'lineEdit_2')
        #self.template_ok = self.dialog.findChild(QPushButton, 'pushButton')
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
                data.append(row_data)
        print(data)
        if self.change_template:
            return send_emails(data, self.template, self.subject)
        return send_emails(data)

    def load_table(self):
        if self.table.columnCount() > 1:
            print('Already Loaded')
            return False


        # Set the column headers to be the object's attributes
        attributes = ['', "Name", 'Email', "Age", "Status", "AE", 'Country']
        self.table.setColumnCount(len(attributes))
        self.table.setHorizontalHeaderLabels(attributes)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)


        # Add the objects' data to the table
        for i, obj in enumerate(self.sorted_list):
            #print(i)

            self.table.insertRow(i)
            # insert row checkbox
            checkbox_item = QCheckBox()
            checkbox_item.setChecked(False)
            checkbox_item.stateChanged.connect(self.checkbox_toggled)
            self.checkboxes.append(checkbox_item)

            self.table.setCellWidget(i, 0, checkbox_item)
            #print('item 1')
            self.table.setItem(i, 1, QTableWidgetItem(obj.name))
            #print('item 2')
            self.table.setItem(i, 2, QTableWidgetItem(obj.email))
            #print('item 3')
            self.table.setItem(i, 3, QTableWidgetItem(str(obj.age)))
            self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)

            # color of aging clients
            if obj.age >= 35:
                self.table.item(i, 3).setForeground(Qt.red)
            elif obj.age >= 20:
                self.table.item(i, 3).setForeground(Qt.darkYellow)
            else:
                self.table.item(i, 3).setForeground(Qt.darkGreen)
            #print('item 4')
            self.table.setItem(i, 4, QTableWidgetItem(str(obj.stage)))
            #print('item 5')
            self.table.setItem(i, 5, QTableWidgetItem(obj.ae))
            #print('item 6')

            self.table.setItem(i, 6, QTableWidgetItem(str(obj.country)))
            self.table.item(i, 6).setTextAlignment(Qt.AlignCenter)
            #print('item 7')

        self.table.resizeColumnsToContents()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.adjustSize()


class AeWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ae_window.ui', self)
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.table = self.findChild(QTableWidget, 'tableWidget')
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
        print(data)
        if data:
            return send_emails_ae_unified(data)
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
                data.append(row_data)
        print(data)
        if self.change_template:
            return send_emails_ae(data, self.template, self.subject)
        return send_emails_ae(data)

    # Connect the date time changed signal to the slot function and pass the row number
    def update_table(self, date_time, row_number):
        pass

    def load_table(self):
        if self.table.columnCount() > 1:
            print('Already Loaded')
            return False

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
            #print('item 1')
            self.table.setItem(i, 1, QTableWidgetItem(obj.ae))
            #print('item 2')
            self.table.setItem(i, 2, QTableWidgetItem(obj.name))
            #print('item 3')
            self.table.setItem(i, 3, QTableWidgetItem(str(obj.age)))
            self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)

            # color of aging clients
            if obj.age >= 35:
                self.table.item(i, 3).setForeground(Qt.red)
            elif obj.age >= 20:
                self.table.item(i, 3).setForeground(Qt.darkYellow)
            else:
                self.table.item(i, 3).setForeground(Qt.darkGreen)
            #print('item 4')
            self.table.setItem(i, 4, QTableWidgetItem(str(obj.stage)))
            #print('item 5')
            self.table.setItem(i, 5, QTableWidgetItem(obj.org_name))
            #print('item 6')

            self.table.setItem(i, 6, QTableWidgetItem(str(obj.eng_age)))
            self.table.item(i, 6).setTextAlignment(Qt.AlignCenter)
            #print('item 7')
            self.table.setItem(i, 7, QTableWidgetItem(obj.country))
            self.table.item(i, 7).setTextAlignment(Qt.AlignCenter)
            #print('item 8')
        self.table.resizeColumnsToContents()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.adjustSize()


class BiWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('blind_invite.ui', self)
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.table = self.findChild(QTableWidget, 'tableWidget')
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
                data.append(row_data)
        print(data)

        return show_invites(data)

    # Connect the date time changed signal to the slot function and pass the row number
    def update_table(self, date_time, row_number):
        print(type(date_time))
        selected_date = date_time.toPyDateTime()
        self.table.setItem(row_number, 7, QTableWidgetItem(selected_date.strftime("%m/%d/%Y %I:%M %p")))
        self.table.item(row_number, 7).setTextAlignment(Qt.AlignCenter)

    def load_table(self):
        if self.table.columnCount() > 1:
            print('Already Loaded')
            return False

        from calstuff import get_conflicts, find_times
        self.pyt = find_times(get_conflicts(), 30, 21)
        # Set the column headers to be the object's attributes
        attributes = ['', "Name", 'Status', "Age", 'AE', "Email", 'Suggested Time', 'Edited Time', 'Country']
        self.table.setColumnCount(len(attributes))
        self.table.setHorizontalHeaderLabels(attributes)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)


        # Add the objects' data to the table
        for i, obj in enumerate(self.sorted_list):
            #print(i)
            self.table.insertRow(i)
            # insert row checkbox
            checkbox_item = QCheckBox()
            checkbox_item.setChecked(False)
            checkbox_item.stateChanged.connect(self.checkbox_toggled)
            self.checkboxes.append(checkbox_item)

            self.table.setCellWidget(i, 0, checkbox_item)

            self.table.setItem(i, 1, QTableWidgetItem(obj.name))

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
                    if item.age < 60:
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


class WeekView(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('week_table.ui', self)
        self.week_select = self.findChild(QComboBox, 'comboBox')
        self.load_button = self.findChild(QPushButton, 'pushButton')
        self.table = self.findChild(QTableWidget, 'tableWidget')

        self.current_clients = MetricWindow.current_clients
        self.week_selection = self.week_select.currentText()
        self.week_select.activated[str].connect(self.on_activated)



    mon = []
    tues = []
    wed = []
    thurs = []
    fri = []
    weekly_clients = []

    def on_activated(self, text):
        print(text)
        self.week_selection = text

    def load_table(self, text):
        from calstuff import get_meetings_week
        meetings = get_meetings_week(text)
        i = 0
        for meeting in meetings:
            print(i)
            j = 0
            for key in meeting:
                if 'Your Gartner Call' in meeting[key].Subject or 'Accept or Reschedule' in meeting[key].Subject or 'Seu' in meeting[key].Subject:
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
        self.weekly_clients = [self.mon, self.tues, self.wed, self.thurs, self.fri]
        print(self.weekly_clients)






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
        #grab and set totals
        self.first_month_total = len(self.monthly_clients[0])
        self.totalLabel_1.setText(str(len(self.monthly_clients[0])))
        self.second_month_total = len(self.monthly_clients[1])
        self.totalLabel_2.setText(str(len(self.monthly_clients[1])))
        self.third_month_total = len(self.monthly_clients[2])
        self.totalLabel_3.setText(str(len(self.monthly_clients[2])))

        self.quick_maths(self.monthly_clients)


        self.show()

    active_month = None
    window_list = []
    current_clients = []


    def open_calendar(self):
        self.current_clients = self.monthly_clients
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
        self.obLabel_1.setText(f'{str(ob_1 * 100)[:4]}%')

        ob_2 = total_closed[1] / int(self.totalLabel_2.text())
        self.obLabel_2.setText(f'{str(ob_2 * 100)[:4]}%')

        # check if month has clients before dividing by 0
        if int(self.totalLabel_3.text()) != 0:
            ob_3 = total_closed[2] / int(self.totalLabel_3.text())
            self.obLabel_3.setText(f'{str(ob_3 * 100)[:4]}%')
        else:
            ob_3 = 0
            self.obLabel_3.setText(f'{str(ob_3)}%')

        opportunities = []

        for month in clients:
            opportunity_total = 0
            for j in range(len(month)):
                if month[j].stage == 'Closed Onboarded' or month[j].age > 45:
                    opportunity_total += 1
            opportunities.append(opportunity_total)

        opp_1 = int(self.totalLabel_1.text()) - opportunities[0]
        self.oppLabel_1.setText(str(opp_1))

        opp_2 = int(self.totalLabel_2.text()) - opportunities[1]
        self.oppLabel_2.setText(str(opp_2))

        opp_3 = int(self.totalLabel_3.text()) - opportunities[2]
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
        elif rem_1 < .70:
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


class TestBox(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('register.ui', self)
        self.submit = self.findChild(QPushButton, 'pushButton_2')
        self.button = self.findChild(QPushButton, 'pushButton')
        self.button.clicked.connect(self.save_user)
        self.nameEdit = self.findChild(QLineEdit, 'nameEdit')
        self.lastEdit = self.findChild(QLineEdit, 'lastEdit')
        self.timeEdit = self.findChild(QTimeEdit, 'timeEdit')
        self.dateTimeEdit = self.findChild(QDateTimeEdit, 'dateTimeEdit')
        self.schedulingEdit = self.findChild(QLineEdit, 'schedulingEdit')
        self.checkbox = self.findChild(QCheckBox, 'checkBox')
        self.logo = self.findChild(QLabel, 'label')

        self.submit.clicked.connect(self.verify_fields)

        pixmap = QtGui.QPixmap('C:\\Users\\ccardoso\\Desktop\\August Data\\Gartner_logo.svg.png')
        pixmap = pixmap.scaled(464, 200, Qt.KeepAspectRatio)
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignCenter)

        self.checkbox.setEnabled(False)
        self.timeEdit.setEnabled(False)
        self.dateTimeEdit.setEnabled(False)
        self.button.setEnabled(False)

        if len(self.nameEdit.text()) > 3 and len(self.lastEdit.text()) > 3 and len(self.schedulingEdit.text()) > 10:
            self.button.setEnabled(False)
        self.show()

    def verify_fields(self):
        if len(self.nameEdit.text()) > 3 and len(self.lastEdit.text()) > 3 and len(self.schedulingEdit.text()) > 10:
            self.checkbox.setEnabled(True)
            self.timeEdit.setEnabled(True)
            self.dateTimeEdit.setEnabled(True)
            self.button.setEnabled(True)

    def save_user(self):
        columns = ['First', 'Last', 'Scheduling', 'Lunch', 'Team Meeting']
        if self.checkbox.isChecked():
            data = {'First': [self.nameEdit.text()],
                    'Last': [self.lastEdit.text()],
                    'Scheduling': [self.schedulingEdit.text()],
                    'Lunch': [self.timeEdit.text()],
                    'Team Meeting': [self.dateTimeEdit.text()]}
        else:
            data = {'First': [self.nameEdit.text()],
                    'Last': [self.lastEdit.text()],
                    'Scheduling': [self.schedulingEdit.text()],
                    'Lunch': [''],
                    'Team Meeting': ['']}
        df = pandas.DataFrame(data)
        df.to_csv(f'catcher.csv',
                  index=False, header=True, columns=columns)
        start.setEnabled(True)
        global USER
        USER = True

        self.close()


class TemplateEdit(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('template_editor.ui', self)
        self.parent = self.parentWidget()
        self.button = self.findChild(QPushButton, 'pushButton')

        self.textEdit = self.findChild(QTextEdit, 'textEdit')

        self.subject = self.findChild(QLineEdit, 'lineEdit_2')
        #self.subject.changeEvent(lambda: self.enable_button())
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
        start = MainWindow()

    else:
        start = MainWindow()
        start.setEnabled(False)
        test = TestBox()
        load_user()

    app.exec_()
