
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTime, QDate, QDateTime, QEvent
from PyQt5 import uic, QtGui
import pandas
from datetime import datetime
from communications import show_invites, send_emails, send_emails_ae, send_emails_ae_unified
from ui_functions import *
USER = None

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
                 eng_age=None):
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
        self.verticalLayoutBi = self.findChild(QVBoxLayout, 'verticalLayout_6')
        self.verticalLayoutAe = self.findChild(QVBoxLayout, 'verticalLayoutAE')
        self.VerticalLayoutOutreach = self.findChild(QVBoxLayout, 'verticalLayout_9')
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
        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))

        ## PAGES
        ########################################################################

        # PAGE 1
        self.btn_page_1.clicked.connect(lambda: self.load_home())

        # PAGE 2
        self.btn_page_2.clicked.connect(lambda: self.load_data_bi())

        # PAGE 3
        self.btn_page_3.clicked.connect(lambda: self.load_data_ae())

        # PAGE 4
        self.btn_page_4.clicked.connect(lambda: self.load_data_outreach())

        # SHOW ==> MAIN WINDOW
        ########################################################################

        self.show()



        # ==> END ##

    object_list = []
    client_list = []
    selected_tab = None
    loaded_file = None
    people = []

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
                            eng_age=eng_age
                            )

            print(f"{client.eng_age}{client.is_engaged()}")
            self.client_list.append(client)

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
            self.change_template = True
        else:
            print('Unchecked')
            self.change_template = False

    # function called when return statement hits needs to take in template parameter if checkbox marked
    def create_list(self):
        data = []
        header_labels = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        for i in range(self.table.rowCount()):
            # checkbox_outer_widget = self.table.cellWidget(i, 0)
            checkbox = self.table.cellWidget(i, 0)
            if self.checkboxes[i].isChecked():
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
            print(i)

            self.table.insertRow(i)
            # insert row checkbox
            checkbox_item = QCheckBox()
            checkbox_item.setChecked(False)
            checkbox_item.stateChanged.connect(self.checkbox_toggled)
            self.checkboxes.append(checkbox_item)

            self.table.setCellWidget(i, 0, checkbox_item)
            print('item 1')
            self.table.setItem(i, 1, QTableWidgetItem(obj.name))
            print('item 2')
            self.table.setItem(i, 2, QTableWidgetItem(obj.email))
            print('item 3')
            self.table.setItem(i, 3, QTableWidgetItem(str(obj.age)))
            self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)

            # color of aging clients
            if obj.age >= 35:
                self.table.item(i, 3).setForeground(Qt.red)
            elif obj.age >= 20:
                self.table.item(i, 3).setForeground(Qt.darkYellow)
            else:
                self.table.item(i, 3).setForeground(Qt.darkGreen)
            print('item 4')
            self.table.setItem(i, 4, QTableWidgetItem(str(obj.stage)))
            print('item 5')
            self.table.setItem(i, 5, QTableWidgetItem(obj.ae))
            print('item 6')

            self.table.setItem(i, 6, QTableWidgetItem(str(obj.country)))
            self.table.item(i, 6).setTextAlignment(Qt.AlignCenter)
            print('item 7')

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
        self.checkboxes = []
        self.pushButton.clicked.connect(lambda: self.create_list())
        self.loadButton.clicked.connect(lambda: self.load_table())
        self.sendUnifiedButton.clicked.connect(lambda: self.create_unified_list())

        # algorithmically suggest times from outlook
        # self.pyt = find_times(self.calendar[0], duration=30, date_range=self.calendar[1], start=self.calendar[2])

        self.object_list = MainWindow.object_list
        self.list = []
        for i in range(len(self.object_list)):
            if self.object_list[i].stage != 'Closed Not Onboarded':
                if type(self.object_list[i].eng_age) != type(3):
                    self.object_list[i].eng_age = 'N/A'
                    self.list.append(self.object_list[i])
                elif self.object_list[i].eng_age > 21:
                    self.list.append(self.object_list[i])
        # sort and filter the list for client stages/status (specific to blind invite window will vary for AE
        self.sorted_list = sorted(self.list, key=lambda x: x.ae)

        self.show()



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
            if self.checkboxes[i].isChecked():
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
        return send_emails_ae_unified(data)

    def create_list(self):

        data = []
        header_labels = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        for i in range(self.table.rowCount()):
            # checkbox_outer_widget = self.table.cellWidget(i, 0)
            checkbox = self.table.cellWidget(i, 0)
            if self.checkboxes[i].isChecked():
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
            print(i)

            self.table.insertRow(i)
            # insert row checkbox
            checkbox_item = QCheckBox()
            checkbox_item.setChecked(False)
            checkbox_item.stateChanged.connect(self.checkbox_toggled)
            self.checkboxes.append(checkbox_item)

            self.table.setCellWidget(i, 0, checkbox_item)
            print('item 1')
            self.table.setItem(i, 1, QTableWidgetItem(obj.ae))
            print('item 2')
            self.table.setItem(i, 2, QTableWidgetItem(obj.name))
            print('item 3')
            self.table.setItem(i, 3, QTableWidgetItem(str(obj.age)))
            self.table.item(i, 3).setTextAlignment(Qt.AlignCenter)

            # color of aging clients
            if obj.age >= 35:
                self.table.item(i, 3).setForeground(Qt.red)
            elif obj.age >= 20:
                self.table.item(i, 3).setForeground(Qt.darkYellow)
            else:
                self.table.item(i, 3).setForeground(Qt.darkGreen)
            print('item 4')
            self.table.setItem(i, 4, QTableWidgetItem(str(obj.stage)))
            print('item 5')
            self.table.setItem(i, 5, QTableWidgetItem(obj.org_name))
            print('item 6')

            self.table.setItem(i, 6, QTableWidgetItem(str(obj.eng_age)))
            self.table.item(i, 6).setTextAlignment(Qt.AlignCenter)
            print('item 7')
            self.table.setItem(i, 7, QTableWidgetItem(obj.country))
            self.table.item(i, 7).setTextAlignment(Qt.AlignCenter)
            print('item 8')
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
            if self.checkboxes[i].isChecked():
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

        from calstuff import conflicts, find_times, day_range
        self.pyt = find_times(conflicts, 30, day_range)
        # Set the column headers to be the object's attributes
        attributes = ['', "Name", 'Status', "Age", 'AE', "Email", 'Suggested Time', 'Edited Time', 'Country']
        self.table.setColumnCount(len(attributes))
        self.table.setHorizontalHeaderLabels(attributes)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)


        # Add the objects' data to the table
        for i, obj in enumerate(self.sorted_list):
            print(i)
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
        self.button = self.findChild(QPushButton, 'pushButton')
        self.textEdit = self.findChild(QTextEdit, 'textEdit')
        self.subject = self.findChild(QLineEdit, 'lineEdit_2')
        self.button.clicked.connect(lambda: self.button_clicked())

    def button_clicked(self):
        print('Clicked')
        OutreachWindow.template = self.textEdit.toHtml()
        OutreachWindow.subject = self.subject.text()
        print(OutreachWindow.template)
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




    #window = BiWindow()
    #window.show()
    app.exec_()

