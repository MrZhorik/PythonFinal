from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
import sys
import MySQLdb

from PyQt5.uic import loadUiType

ui, _ = loadUiType('library.ui')

login, _ = loadUiType('login.ui')


class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.window2 = None
        self.db = None
        self.cur = None
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handel_login)

    def handel_login(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()

        for row in data:
            if username == row[1] and password == row[3]:

                self.window2 = MainApp()
                self.close()
                self.window2.show()
                break

        else:
            QMessageBox.warning(self, "Delete Book", "Are You Sure?", QMessageBox.Ok)


# Connect UI to PyCharm
class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.cur = None
        self.db = None
        self.setupUi(self)
        self.handle_ui_changes()
        self.handle_buttons()

        self.show_category()
        self.show_author()
        self.show_publisher()

        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()

        self.show_all_books_ui()
        self.show_all_clients_ui()
        self.show_all_operations_ui()

    def handle_ui_changes(self):
        self.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):

        self.pushButton.clicked.connect(self.open_day_to_day_tab)
        self.pushButton_2.clicked.connect(self.open_books_tab)
        self.pushButton_3.clicked.connect(self.open_users_tab)
        self.pushButton_4.clicked.connect(self.open_settings_tab)
        self.pushButton_5.clicked.connect(self.open_clients_tab)

        self.pushButton_6.clicked.connect(self.handel_day_operations)

        self.pushButton_7.clicked.connect(self.add_new_book)
        self.pushButton_10.clicked.connect(self.search_book)
        self.pushButton_9.clicked.connect(self.edit_book)
        self.pushButton_11.clicked.connect(self.delete_book)

        self.pushButton_12.clicked.connect(self.add_new_user)
        self.pushButton_16.clicked.connect(self.login_user)
        self.pushButton_15.clicked.connect(self.edit_user)
        self.pushButton_23.clicked.connect(self.delete_user)

        self.pushButton_8.clicked.connect(self.add_new_client)
        self.pushButton_13.clicked.connect(self.search_client)
        self.pushButton_22.clicked.connect(self.edit_client)
        self.pushButton_21.clicked.connect(self.delete_client)

        self.pushButton_14.clicked.connect(self.add_category)
        self.pushButton_17.clicked.connect(self.add_author)
        self.pushButton_18.clicked.connect(self.add_publisher)

    # Opening Tabs
    def open_day_to_day_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_clients_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(4)

    # Day operations
    def handel_day_operations(self):
        book_title = self.lineEdit.text()
        client = self.lineEdit_23.text()
        type_book = self.comboBox.currentText()
        duration = self.comboBox_2.currentIndex() + 1
        today_date = datetime.date.today()
        to_date = today_date + datetime.timedelta(days=duration)

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO day_operations(book_name, client, type, days_number, day, to_day)
            VALUES (%s, %s, %s, %s, %s, %s) 
        ''', (book_title, client, type_book, duration, today_date, to_date))

        self.db.commit()
        self.statusBar().showMessage('New Book Retrieve Or Rent')
        self.lineEdit.setText('')
        self.lineEdit_23.setText('')
        self.comboBox_2.setCurrentIndex(0)
        self.show_all_operations_ui()

    def show_all_operations_ui(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            SELECT book_name, client, type, day, to_day FROM day_operations
        ''')

        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    # Operations With Books DB
    def add_new_book(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_7.currentText()
        book_price = self.lineEdit_6.text()
        book_description = self.plainTextEdit.toPlainText()

        self.cur.execute('''
            INSERT INTO book(book_name, book_description, book_code, book_category, book_author, 
            book_publisher, book_price) VALUES (%s, %s, %s, %s, %s, %s, %s) 
            ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))

        self.db.commit()
        self.statusBar().showMessage("New Book Added")

        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_6.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.plainTextEdit.setPlainText('')
        self.show_all_books_ui()

    def show_all_books_ui(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT book_code, book_name, book_description, book_author, book_publisher, 
        book_category, book_price FROM book''')
        data = self.cur.fetchall()

        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)

        if data:
            self.tableWidget_6.setRowCount(0)
            self.tableWidget_6.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_6.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_6.rowCount()
                self.tableWidget_6.insertRow(row_position)

            self.db.close()

    def search_book(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_13.text()
        query = ("SELECT book_name, book_description, book_code, book_category, book_author, book_publisher, "
                 "book_price FROM book WHERE book_name = %s")
        self.cur.execute(query, (book_title,))

        data = self.cur.fetchall()

        for book_info in data:
            self.lineEdit_12.setText(book_info[0])
            self.plainTextEdit_4.setPlainText(book_info[1])
            self.lineEdit_10.setText(book_info[2])
            self.comboBox_13.setCurrentText(book_info[3])
            self.comboBox_11.setCurrentText(book_info[4])
            self.comboBox_12.setCurrentText(book_info[5])
            self.lineEdit_11.setText(book_info[6])

        self.statusBar().showMessage("Searching Book")

    def edit_book(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_12.text()
        book_description = self.plainTextEdit_4.toPlainText()
        book_code = self.lineEdit_10.text()
        book_category = self.comboBox_13.currentText()
        book_author = self.comboBox_11.currentText()
        book_publisher = self.comboBox_12.currentText()
        book_price = self.lineEdit_11.text()

        search_book_title = self.lineEdit_13.text()

        self.cur.execute('''
                    UPDATE book SET book_name=%s ,book_description=%s ,book_code=%s ,book_category=%s ,book_author=%s ,
                    book_publisher=%s ,book_price=%s WHERE book_name = %s            
                ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price,
                      search_book_title))

        self.db.commit()
        self.statusBar().showMessage("Book Updated")
        self.show_all_books_ui()

    def delete_book(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_13.text()

        warning = QMessageBox.warning(self, "Delete Book", "Are You Sure?",
                                      QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = '''DELETE FROM book WHERE book_name = %s'''
            self.cur.execute(sql, (book_title,))
            self.db.commit()
            self.statusBar().showMessage('Book Deleted')

            self.show_all_books_ui()

            self.lineEdit_12.setText('')
            self.plainTextEdit_4.setPlainText('')
            self.lineEdit_10.setText('')
            self.comboBox_13.setCurrentText('')
            self.comboBox_11.setCurrentText('')
            self.comboBox_12.setCurrentText('')
            self.lineEdit_11.setText('')

    # Clients
    def add_new_client(self):
        client_name = self.lineEdit_4.text()
        client_email = self.lineEdit_5.text()
        client_id = self.lineEdit_7.text()

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
               INSERT INTO client(client_name, client_email, client_id)
               Values (%s, %s, %s)
           ''', (client_name, client_email, client_id))

        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New Client Added')

        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_7.setText('')

        self.show_all_clients_ui()

    def search_client(self):
        client_id = self.lineEdit_8.text()

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        query = '''SELECT client_name, client_email, client_ID FROM client WHERE client_ID = %s'''
        self.cur.execute(query, (client_id,))

        data = self.cur.fetchall()

        for client_data in data:
            self.lineEdit_22.setText(client_data[0])
            self.lineEdit_18.setText(client_data[1])
            self.lineEdit_9.setText(client_data[2])

        self.statusBar().showMessage("Searching Book")

    def edit_client(self):

        client_name = self.lineEdit_22.text()
        client_email = self.lineEdit_18.text()
        client_id = self.lineEdit_9.text()
        client_original_id = self.lineEdit_8.text()

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        query = '''UPDATE client SET client_name = %s, client_email = %s, client_ID = %s WHERE client_ID = %s'''
        self.cur.execute(query, (client_name, client_email, client_id, client_original_id))

        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('Client Edited')

        self.lineEdit_22.setText('')
        self.lineEdit_18.setText('')
        self.lineEdit_9.setText('')
        self.lineEdit_8.setText('')

        self.show_all_clients_ui()

    def delete_client(self):

        client_original_id = self.lineEdit_8.text()

        warning_message = QMessageBox.warning(self, "Delete Client", "Are you sure?",
                                              QMessageBox.Yes | QMessageBox.No)
        if warning_message == QMessageBox.Yes:
            self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
            self.cur = self.db.cursor()

            self.cur.execute('''DELETE FROM client WHERE client_ID = %s''', (client_original_id,))

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('Delete Client')

            self.lineEdit_22.setText('')
            self.lineEdit_18.setText('')
            self.lineEdit_9.setText('')
            self.lineEdit_8.setText('')

            self.show_all_clients_ui()

    def show_all_clients_ui(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT client_name, client_email, client_ID from client''')
        data = self.cur.fetchall()

        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

            self.db.close()

    # Operations With Users DB
    def add_new_user(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_14.text()
        email = self.lineEdit_17.text()
        password = self.lineEdit_15.text()
        password_again = self.lineEdit_16.text()

        if password == password_again:
            self.cur.execute('''
                INSERT INTO users(user_name , user_email , user_password)
                VALUES (%s , %s , %s)
            ''', (username, email, password))

            self.db.commit()
            self.statusBar().showMessage('New User Added')

        elif email == '' or username == '':
            self.statusBar().showMessage('Check Your Credentials')

        else:
            self.statusBar().showMessage('Check Your Credentials')

        self.lineEdit_14.setText('')
        self.lineEdit_17.setText('')
        self.lineEdit_15.setText('')
        self.lineEdit_16.setText('')

    def login_user(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_31.text()
        password = self.lineEdit_30.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()

        for user_data in data:
            if username == user_data[1] and password == user_data[3]:
                self.groupBox_5.setEnabled(True)

                self.lineEdit_26.setText(user_data[1])
                self.lineEdit_29.setText(user_data[2])

                self.statusBar().showMessage('Valid Username & Password')
        else:
            self.statusBar().showMessage('Invalid Username & Password')

    def edit_user(self):

        username = self.lineEdit_26.text()
        password = self.lineEdit_27.text()
        password_again = self.lineEdit_28.text()
        email = self.lineEdit_29.text()

        original_username = self.lineEdit_31.text()

        if password != password_again or username == '' or email == '' or password == '' or password_again == '':
            self.statusBar().showMessage('Invalid Credentials')

        else:
            self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
            self.cur = self.db.cursor()

            self.cur.execute('''
                UPDATE users SET user_name = %s, user_password = %s, user_email = %s WHERE user_name = %s
            ''', (username, password, email, original_username))

            self.db.commit()
            self.statusBar().showMessage('User Data Edited')

            self.lineEdit_26.setText('')
            self.lineEdit_27.setText('')
            self.lineEdit_28.setText('')
            self.lineEdit_29.setText('')
            self.groupBox_5.setEnabled(False)

    def delete_user(self):

        user_name_original = self.lineEdit_31.text()

        warning = QMessageBox.warning(self, "Delete Book", "Are You Sure?",
                                      QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:
            self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
            self.cur = self.db.cursor()

            self.cur.execute('''DELETE FROM users WHERE user_name = %s''', (user_name_original,))

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('Delete User')

            self.lineEdit_26.setText('')
            self.lineEdit_27.setText('')
            self.lineEdit_28.setText('')
            self.lineEdit_29.setText('')
            self.groupBox_5.setEnabled(False)

    # Operations With Settings DB
    def add_category(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_19.text()

        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
        ''', (category_name,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added')
        self.lineEdit_19.setText('')
        self.show_category()
        self.show_category_combobox()

    def add_author(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        author_name = self.lineEdit_20.text()

        self.cur.execute('''
            INSERT INTO author (author_name) VALUES (%s)
        ''', (author_name,))

        self.db.commit()
        self.statusBar().showMessage('New Author Added')
        self.lineEdit_20.setText('')
        self.show_author()
        self.show_author_combobox()

    def add_publisher(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_21.text()

        self.cur.execute('''
            INSERT INTO publisher (publisher_name) VALUES (%s)
        ''', (publisher_name,))

        self.db.commit()
        self.statusBar().showMessage('New Publisher Added')
        self.lineEdit_21.setText('')
        self.show_publisher()
        self.show_publisher_combobox()

    # Showing Data In UI Settings
    def show_category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def show_author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM author''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    def show_publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)

    # Show Settings Data In UI ComboBox
    def show_category_combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category''')
        data = self.cur.fetchall()

        self.comboBox_3.clear()
        self.comboBox_13.clear()

        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_13.addItem(category[0])

    def show_author_combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM author''')
        data = self.cur.fetchall()

        self.comboBox_4.clear()
        self.comboBox_11.clear()

        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_11.addItem(author[0])

    def show_publisher_combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='AboOgy2222@', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        self.comboBox_7.clear()
        self.comboBox_12.clear()

        for publisher in data:
            self.comboBox_7.addItem(publisher[0])
            self.comboBox_12.addItem(publisher[0])


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
