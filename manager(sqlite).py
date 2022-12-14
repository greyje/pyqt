import os
import datetime
import time
import sys
from datetime import datetime, date
import os.path
import sqlite3
from database_query import if_not_exists
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QHeaderView, QComboBox


class ComboBoxStatus(QComboBox):
    def __init__(self):
        super().__init__()

    def currentTextChanged(self, value, index_):
        self.setItemData(index_, value, QtCore.Qt.UserRole + 1)





class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.SignUpButton = QtWidgets.QPushButton("Sign up")
        self.LogInButton = QtWidgets.QPushButton("Log in")
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        self.SignUpButton.setFixedSize(150, 25)
        self.LogInButton.setFixedSize(150, 25)
        layout.addWidget(self.SignUpButton)
        layout.addWidget(self.LogInButton)
        self.SignUpButton.clicked.connect(self.go_to_signup)
        self.LogInButton.clicked.connect(self.go_to_login)
        self.setLayout(layout)

    def go_to_login(self):
        self.LGW = LogInWindow()
        self.LGW.show()

    def go_to_signup(self):
        self.SUW = SignUpWindow()
        self.SUW.show()


class LogInWindow(QWidget):
    def __init__(self):
        super(LogInWindow, self).__init__()
        self.setWindowTitle("Log in")
        self.usernameLabel = QtWidgets.QLabel("Username")
        self.passwordLabel = QtWidgets.QLabel("Password")
        self.backButton = QtWidgets.QPushButton('Back')
        self.loginButton = QtWidgets.QPushButton('Log in')
        self.errorLabel = QtWidgets.QLabel('The email or password is incorrect.')
        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()
        # self.backButton.clicked.connect(self.go_back)
        self.errorLabel.setStyleSheet("color : 'red'")
        self.passwordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.login_function)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        # buttonLayout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.passwordLine.setFixedSize(200, 25)
        self.usernameLine.setFixedSize(200, 25)
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameLine)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordLine)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.loginButton)
        layout.addWidget(self.backButton)
        self.errorLabel.hide()
        self.setLayout(layout)

    def login_function(self):
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        if len(username) == 0 or len(password) == 0:
            self.errorLabel.setText("Please input all fields.")
            self.errorLabel.show()
        else:
            if SignUp().user_exists(username):
                print(Tasks().compare_data(username, password))
                if Tasks().compare_data(username, password):
                    # self.errorLabel.setText("Successfully logged in.")
                    # self.errorLabel.setStyleSheet("color : 'green'")
                    # self.errorLabel.show()
                    # TaskManagerUI().data_receiver(username, password)
                    username_session.append(username)
                    password_session.append(password)
                    self.go_to_task_manager()
                    self.close()
                    MW.close()

                else:
                    self.errorLabel.setText("Invalid username or password")
                    self.errorLabel.show()
            else:
                self.errorLabel.setText("User not found")
                self.errorLabel.show()

    def go_to_task_manager(self):
        self.TMUI = TaskManagerUI()
        self.TMUI.show()


class SignUpWindow(QWidget):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        self.setWindowTitle('Sign up')
        self.usernameLabel = QtWidgets.QLabel("Username")
        self.passwordLabel = QtWidgets.QLabel("Password")
        self.passwordLabel2 = QtWidgets.QLabel("Confirm password")
        self.backButton = QtWidgets.QPushButton('Back')
        self.createButton = QtWidgets.QPushButton('Create user')
        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()
        self.passwordLine2 = QtWidgets.QLineEdit()
        self.errorLabel = QtWidgets.QLabel('ERROR')
        self.errorLabel.setStyleSheet("color : 'red'")
        # self.backButton.clicked.connect(self.go_back)
        self.createButton.clicked.connect(self.create_func)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordLine.setFixedSize(200, 25)
        self.passwordLine2.setFixedSize(200, 25)
        self.usernameLine.setFixedSize(200, 25)
        layout.maximumSize()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameLine)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordLine)
        layout.addWidget(self.passwordLabel2)
        layout.addWidget(self.passwordLine2)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.createButton)
        layout.addWidget(self.backButton)
        self.errorLabel.hide()
        self.setLayout(layout)

    def create_func(self):
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        password1 = self.passwordLine2.text()
        Tasks().compare_data(username, password)
        if password != password1:
            self.errorLabel.setText("Passwords are not matching")
            self.errorLabel.show()
            QtCore.QTimer.singleShot(5, SignUpWindow.close)
            LogInWindow().go_to_task_manager()
        else:
            if SignUp().user_exists(username):
                self.errorLabel.setText("User already exists")
                self.errorLabel.show()
            else:
                DataBase().database_sign_up(username, password)
                # self.errorLabel.setText('Succesfully signed up!')
                # self.errorLabel.setStyleSheet("color : 'green'")
                # self.errorLabel.show()
                self.close()
        LogInWindow().go_to_task_manager()


class TaskManagerUI(QMainWindow):
    def __init__(self):
        super(TaskManagerUI, self).__init__()
        self.con = sqlite3.connect("database/database.db")
        self.setFixedSize(1000, 600)
        self.setWindowTitle('Task manager')

        self.menu = QtWidgets.QMenu
        self.toolbar = QtWidgets.QToolBar()

        self.cbox_items = ['Ongoing', 'Completed', 'Cancelled']

        # check number of rows in sqlite table
        cur = self.con.cursor()
        cur.execute('SELECT tid FROM userstasks')
        self.rows_number = cur.fetchall()

        self.addToolBar(self.toolbar)
        self.toolbar.setMovable(False)
        self.clear_button = QtWidgets.QPushButton('clear')
        self.button_action = QAction("All tasks", self)
        self.button_action.triggered.connect(self.all_tasks)
        self.button_action2 = QAction("Add task", self)
        self.button_action2.triggered.connect(self.add_task)
        self.button_action3 = QAction("Tasks status", self)
        self.button_action3.triggered.connect(self.tasks_status)

        self.toolbar.setStyleSheet('background-color: white;')
        self.toolbar.addAction(self.button_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.button_action2)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.button_action3)

        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()

    def load_data(self, display=None):
        cur = self.con.cursor()
        cur.execute('SELECT username, date, content, steps, status, status_time FROM userstasks')
        row = 0
        while True:
            res = cur.fetchone()
            if res is None:
                break
            for column, item in enumerate(res):
                display.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))
                if isinstance(item, str) and item.title() in self.cbox_items:
                    combo = ComboBoxStatus()
                    combo.addItems(self.cbox_items)
                    combo.setStyleSheet('QComboBox{color: #D3D3D3};')
                    combo.setStyleSheet('selection-background-color: rgb(211, 211, 211)')
                    combo.setStyleSheet('color: rgb(211, 211, 211)')
                    index_ = combo.findText(str(item).title())
                    print(combo.itemData(index_, QtCore.Qt.UserRole + 1))
                    if index_ != -1:
                        combo.setCurrentText(item.title())
                        display.setCellWidget(row, 4, combo)
            row += 1

    def all_tasks(self):
        self.all_tasks_table = QtWidgets.QTableWidget()
        all_tasks_table_header = self.all_tasks_table.horizontalHeader()
        self.all_tasks_table.setRowCount(self.rows_number[-1][0])
        self.all_tasks_table.setColumnCount(6)
        self.all_tasks_table.setStyleSheet('QTableWidget{color: #D3D3D3}')
        self.all_tasks_table.setHorizontalHeaderLabels(
                ['Username', 'Date', 'Content', 'Steps', 'Status', 'Status set time'])

        all_tasks_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        all_tasks_table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        all_tasks_table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        all_tasks_table_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        all_tasks_table_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        all_tasks_table_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

        display = self.all_tasks_table
        self.load_data(display)
        # self.all_tasks_table.setFixedSize()
        self.setCentralWidget(self.all_tasks_table)

        self.centralWidget().show()

    def add_task(self):
        dialog = DialogWindow()
        dialog.show()

    def filter_tasks(self, index):
        if index == 0:
            self.overdue_tasks()
        elif index == 1:
            self.three_days_tasks()
        elif index == 2:
            self.today_tasks()
        else:
            pass

    def overdue_tasks(self):
        username = username_session[0]
        with self.con as db:
            cur = db.cursor()
            cur.execute(
                'SELECT username, date, content, steps, status, status_time FROM userstasks WHERE username = ? ',
                (Tasks().func_username_container(username)))
            row = 0
            while True:
                res = cur.fetchone()
                if res is None:
                    break
                d = time.localtime()
                getctime = time.strftime('%Y-%m-%d', d)
                t1 = datetime.strptime(res[1], "%Y-%m-%d")
                t2 = datetime.strptime(getctime, "%Y-%m-%d")
                time_diff = abs((t1 - t2).days)
                if time_diff >= 3:
                    for column, i in enumerate(res):
                        self.tab_1.setItem(row, column, QtWidgets.QTableWidgetItem(str(i)))
                else:
                    continue
                row += 1

    def three_days_tasks(self):
        username = username_session[0]
        with self.con as db:
            cur = db.cursor()
            cur.execute(
                'SELECT username, date, content, steps, status, status_time FROM userstasks WHERE username = ? ',
                (Tasks().func_username_container(username)))
            row = 0
            while True:
                res = cur.fetchone()
                if res is None:
                    break
                for column, i in enumerate(res):
                    set_data = datetime.strptime(res[1], "%Y-%m-%d")
                    if (datetime.now() - set_data).days > 3:
                        print('overdue!!!!!!!!!!!', res)
                    else:
                        self.tab_2.setItem(row, column, QtWidgets.QTableWidgetItem(str(i)))
                #                    if now - timedelta(hours=24) <= set_data <= now + timedelta(hours=24):
                #                        self.tab_3.setItem(row, column, QtWidgets.QTableWidgetItem(str(i)))
                #                    else:
                #                        print('overdue!!!!!!!!!!!', res)
                row += 1

    def today_tasks(self):
        username = username_session[0]
        with self.con as db:
            cur = db.cursor()

            cur.execute('SELECT username, date, content, steps, status, status_time FROM userstasks WHERE username = ? '
                        , (Tasks().func_username_container(username)))
            row = 0
            while True:
                res = cur.fetchone()
                if res is None:
                    break
                for column, i in enumerate(res):
                    now = datetime.now()
                    set_data = datetime.strptime(res[1], "%Y-%m-%d")

                    if (datetime.now() - set_data).days > 1:
                        print('overdue!!!!!!!!!!!', res)
                    else:
                        self.tab_3.setItem(row, column, QtWidgets.QTableWidgetItem(str(i)))
                row += 1

    def tasks_status(self):
        tabs = QtWidgets.QTabWidget()
        overdue_table = QtWidgets.QTableWidget()
        three_days_table = QtWidgets.QTableWidget()
        today_table = QtWidgets.QTableWidget()

        overdue_table_header = overdue_table.horizontalHeader()
        three_days_table_header = three_days_table.horizontalHeader()
        today_table_header = today_table.horizontalHeader()

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab_1 = overdue_table
        self.tab_1.setFixedSize(995, 550)
        self.tab_1.setParent(self.tab1)

        self.tab_2 = three_days_table
        self.tab_2.setFixedSize(995, 550)
        self.tab_2.setParent(self.tab2)

        self.tab_3 = today_table
        self.tab_3.setFixedSize(995, 550)
        self.tab_3.setParent(self.tab3)

        tabs.addTab(self.tab1, 'Overdue tasks')
        tabs.addTab(self.tab2, 'Tasks of the 3 days')
        tabs.addTab(self.tab3, 'Tasks of the day')

        tables = [self.tab_1, self.tab_2, self.tab_3]
        table_headers = [overdue_table_header, three_days_table_header, today_table_header]

        # if len(rows_number) > 1:
        for i in tables:
            i.setRowCount(self.rows_number[-1][0])
            i.setColumnCount(6)
            i.setStyleSheet('QTableWidget{color: #D3D3D3}')
            i.setHorizontalHeaderLabels(
                ['Username', 'Date', 'Content', 'Steps', 'Status', 'Status set time'])

        for i in table_headers:
            i.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            i.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            i.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            i.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            i.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            i.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        tabs.tabBarClicked.connect(self.filter_tasks)
        self.setCentralWidget(tabs)
        self.centralWidget().show()

    def combo_box_changed(self, value):
        with self.con as db:
            rowid = self.all_tasks_table.currentRow() + 1
            cur = db.cursor()
            cur.execute('UPDATE userstasks SET status = ? WHERE tid = ?', (value, rowid))


# dialog window for add task func
class DialogWindow(QWidget):
    def __init__(self):
        super(DialogWindow, self).__init__()
        self.setWindowTitle('Add task')
        self.setFixedSize(400, 300)

        self.ask = AskUser()

        self.add_button = QtWidgets.QPushButton('Add')
        self.date_edit = QtWidgets.QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFixedHeight(30)
        self.date_edit.setStyleSheet('QDateEdit {color: #D3D3D3}')
        self.date_edit.setDateTime(QtCore.QDateTime.currentDateTime())

        self.user_input = QtWidgets.QLineEdit()

        self.label = QtWidgets.QLabel('Input your task')
        self.label.setStyleSheet('QLabel{font-size: 15pt}')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.check_box = QtWidgets.QCheckBox()
        self.check_box.setText('Add steps ?')
        self.check_box.setStyleSheet('QCheckBox {color: #D3D3D3;}')
        self.check_box.stateChanged.connect(lambda: self.checked())

        self.error_label = QtWidgets.QLabel('Input integer')
        self.error_label.setStyleSheet('QLabel {color: red}')

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.user_input)
        layout.setSpacing(20)
        layout.addWidget(self.date_edit)
        layout.setSpacing(20)
        layout.addWidget(self.check_box)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_func)

    def checked(self):
        if self.check_box.isChecked():
            self.dialog()

    # print(self.date_edit.)

    def dialog(self):
        self.ask.show()

    def add_func(self):
        self.text = self.user_input.text()
        content_session.append(self.text)
        self.temp = self.date_edit.calendarWidget().selectedDate()
        date.append(self.temp)
        DataBase().database_add_task()
        self.hide()


class AskUser(QWidget):
    def __init__(self):
        super(AskUser, self).__init__()
        self.resize(300, 150)
        self.setWindowTitle('Steps')
        self.items = []
        self.item_count = 0

        label = QtWidgets.QLabel("Number of steps")
        self.accept_btn = QtWidgets.QPushButton('Accept')
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setRange(0, 5)
        self.spinBox.valueChanged.connect(self.set_item_count)
        self.spinBox.setStyleSheet('QSpinBox {color: #D3D3D3}')
        groupBox = QtWidgets.QGroupBox("Input steps")
        groupBox.setStyleSheet('QGroupBox{color: #D3D3D3}')
        self.item_layout = QtWidgets.QVBoxLayout(groupBox)
        self.item_layout.addStretch(2)

        g_layout = QtWidgets.QGridLayout(self)
        g_layout.addWidget(label, 0, 0, 1, 2)
        g_layout.addWidget(self.spinBox, 0, 2, 1, 1)
        g_layout.addWidget(groupBox, 2, 0, 5, 3)
        g_layout.addWidget(self.accept_btn)

    def set_item_count(self, new_count: int):
        lineEdit = QtWidgets.QLineEdit
        n_items = len(self.items)
        for i in range(n_items, new_count):
            item = lineEdit(self)
            self.items.append(item)
            self.item_layout.insertWidget(n_items, item)
        for i in range(self.item_count, new_count):
            self.item_layout.itemAt(i).widget().show()
        for i in range(new_count, self.item_count):
            self.item_layout.itemAt(i).widget().hide()
        self.item_count = new_count

        if n_items > new_count:
            self.items = self.items[:-1]

        self.accept_btn.clicked.connect(self.accept_func)

    def accept_func(self):
        steps = []
        for i in self.items:
            steps.append(i.text())
        self.steps_str = ''
        for i in steps:
            self.steps_str = ', '.join([str(item) for item in steps])
        steps_session.append(self.steps_str)
        self.close()


class SignUp:
    def __init__(self):
        self.con = sqlite3.connect("database/database.db")

    def user_exists(self, username):
        with self.con as db:
            cur = db.cursor()
            cur.execute("SELECT username FROM usersdata")
            names = {name[0] for name in cur.fetchall()}
            if username in names:
                return True
        return False


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("database/database.db")

    def database_sign_up(self, username, password):
        with self.con as db:
            cur = db.cursor()
            cur.execute('INSERT INTO usersdata(username, password) VALUES (?, ?)',
                        Tasks().func_user_info(username, password))

    def database_add_task(self):
        username = username_session[0]
        content = content_session[0]
        with self.con as db:
            status = 'ongoing'
            cur = db.cursor()
            d = date[-1].toPyDate()
            print(date)
            print(date[-1])
            date1 = time.localtime()
            getctime = time.strftime('%Y-%m-%d', date1)
            # time.ctime()
            if not steps_session:
                cur.execute(
                    'INSERT INTO userstasks(username, date, content, status, status_time) VALUES (?, ?, ?, ?, ?)',
                    (username, d, content, status, getctime))
            else:
                cur.execute(
                    'INSERT INTO userstasks(username, date, content, steps, status, status_time) VALUES (?, ?, ?, ?, ?,'
                    ' ?)',
                    (username, d, content, steps_session[0], status, getctime))

    def database_all_tasks(self, username):
        with self.con as db:
            row_list = []
            cur = db.cursor()
            execute = cur.execute('SELECT * from userstasks WHERE username = ?',
                                  (Tasks().func_username_container(username)))
            if not Tasks().tasks_exists(username):
                for row in execute:
                    row_list.append(row)
                return row_list
            else:
                print("Not a single task was found")

    def database_task_exists(self, username):
        with self.con as db:
            cur = db.cursor()
            cur.execute('SELECT * from userstasks ')
            names = {name[0] for name in cur.fetchall()}
            if username in names:
                return True

    def database_compare_data(self, username, password):
        with self.con as db:
            cur = db.cursor()
            cur.execute("SELECT username, password FROM usersdata")
            data_list = cur.fetchall()
            for i in data_list:
                if Tasks().func_user_input(username, password) == i:
                    return True
        return False


class Tasks:
    def __init__(self):
        self.con = sqlite3.connect("database/database.db")

    def tasks_exists(self, username):
        DataBase().database_task_exists(username)
        return False

    def func_username_container(self, username):
        username_container = [username]
        return username_container

    def func_user_info(self, username, password):
        user_info = (username, password)
        return user_info

    def func_user_input(self, username, password):
        user_input = (username, password)
        return user_input

    def compare_data(self, username, password):
        return DataBase().database_compare_data(username, password)

    def return_function(self, choice):
        funcctions = {
            1: self.__getattribute__("all_tasks"),
            2: self.__getattribute__("add_task"),
            3: self.__getattribute__("tasks_status"),
            4: self.__getattribute__("update_status"),
            5: TaskManager().__getattribute__("main")
        }
        return funcctions.get(int(choice))


class TaskManager:

    def __init__(self, user_name=None, db=None):
        self.username = user_name
        self.create_structure()
        self.con = sqlite3.connect("database/database.db")
        # self.cur = db.cursor()

    @staticmethod
    def create_structure():
        os.makedirs('datafiles', exist_ok=True)
        os.makedirs('database', exist_ok=True)

    def data_files(self):
        if not os.path.isdir("database"):
            os.mkdir("database")

    def data_files_tasks(self):
        with self.con as db:
            db.executescript(if_not_exists)

    def return_function_for_main(self, choice):
        funcctions = {
            1: self.__getattribute__("log_in"),
            2: SignUp().__getattribute__("sign_up"),
            3: self.__getattribute__("exitt"),
        }
        return funcctions.get(int(choice))


if __name__ == "__main__":
    TaskManager().data_files()
    TaskManager().data_files_tasks()
    app = QApplication(sys.argv)
    style = """
        QWidget{
            background: #262D37;
        }
        QLabel{
            color: #D3D3D3;
        }
        QLineEdit{
            border: 2px solid #D3D3D3;
            border-radius: 8px;
            padding: 1px;
            color: #D3D3D3;
        }
        QPushButton{
            color: #D3D3D3;
            background: #808080;
            border: 1px #DADADA solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: bold;
            font-size: 9pt;
            outline: none
        }
        
    """
    username_session = []
    password_session = []
    content_session = []
    date = []
    steps_session = []
    app.setStyleSheet(style)
    MW = MainWindow()
    MW.setWindowTitle("Task manager")
    MW.setFixedSize(400, 300)
    MW.show()
    sys.exit(app.exec_())
