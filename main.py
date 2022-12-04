from random import choice
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QFont

import sqlite3
import pygame
import sys
pygame.init()


class Minesweeper(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_table.ui', self)
        self.setFixedSize(QSize(494, 690))
        self.song = pygame.mixer.Sound('music/Jesper Kyd - Home in Florence.mp3')

        self.pixmap = QPixmap('images/ico_main.jpg')
        # Стили кнопок
        self.style = 'font: 20pt "Times New Roman";\n' \
                     '\ncolor: rgb(170, 170, 102);\nbackground-color: rgb(116, 0, 0);'
        self.style_2 = 'font: 20pt "Times New Roman";' \
                       '\nbackground-color: rgb(168, 168, 168);\ncolor: rgb(118, 0, 0);\n'

        self.music_key = 0  # Флаг музыки
        self.pixmap = self.pixmap.scaled(121, 121, Qt.KeepAspectRatio)  # Установка изображения в главном меню
        self.label_2.setPixmap(self.pixmap)

        self.pushButton = HoverButton(self)  # Кнопка входа в профиль
        self.pushButton.setStyleSheet(self.style)
        self.pushButton.setGeometry(140, 310, 211, 41)
        self.pushButton.setText('Войти в профиль')

        self.pushButton_2 = HoverButton(self)  # Кнопка перехода на регистрацию
        self.pushButton_2.setStyleSheet(self.style)
        self.pushButton_2.setGeometry(140, 370, 211, 41)
        self.pushButton_2.setText('Регистрация')

        self.pushButton_3 = HoverButton(self)  # Кнопка входа в статистику
        self.pushButton_3.setDisabled(True)
        self.pushButton_3.setStyleSheet(self.style_2)
        self.pushButton_3.setGeometry(140, 430, 211, 41)
        self.pushButton_3.setText('Статистика')
        self.pushButton_3.clicked.connect(self.statistic)

        self.pushButton_4 = HoverButton(self)  # Кнопка входа в список правил
        self.pushButton_4.setStyleSheet(self.style)
        self.pushButton_4.setGeometry(140, 490, 211, 41)
        self.pushButton_4.setText('Правила')

        self.pushButton_5 = HoverButton(self)  # Кнопка включения\отключения музыки
        self.pushButton_5.setStyleSheet('''font: 12pt "Times New Roman";
                                    color: rgb(170, 170, 102);
                                    background-color: rgb(116, 0, 0);''')
        self.pushButton_5.setGeometry(330, 610, 141, 31)
        self.music()

        self.pushButton_6 = HoverButton(self)  # Кнопка выхода
        self.pushButton_6.setStyleSheet(self.style)
        self.pushButton_6.setGeometry(140, 550, 211, 41)
        self.pushButton_6.setText('Выход')

        self.pushButton_7 = HoverButton(self)  # Кнопка входа в игровое меню
        self.pushButton_7.setDisabled(True)
        self.pushButton_7.setStyleSheet(self.style_2)
        self.pushButton_7.setGeometry(140, 250, 211, 41)
        self.pushButton_7.setText('Играть')
        self.pushButton_7.clicked.connect(self.played)

        self.list_btns_in_menu = [self.pushButton, self.pushButton_2,
                                  self.pushButton_4, self.pushButton_5,
                                  self.pushButton_6]

        for i in self.list_btns_in_menu:
            i.setCursor(QtCore.Qt.PointingHandCursor)

        # ON/OFF музыка
        self.pushButton_5.clicked.connect(self.music)
        # Регистрация
        self.pushButton_2.clicked.connect(self.global_registration)
        # Статистика

        # Вход в профиль
        self.pushButton.clicked.connect(self.sign)
        # Выход из приложения
        self.pushButton_6.clicked.connect(self.exit)

        # Правила игры
        self.pushButton_4.clicked.connect(self.rules)

    def sign(self):  # Переход в профиль (переход)
        self.sign_in = Sign()
        self.sign_in.show()

    def rules(self):  # Правила (переход)
        self.rls = Rules()
        self.rls.show()

    def statistic(self):  # Переход на статистику
        self.stat = Statistics(self.name)
        self.stat.show()

    def music(self):  # Включение\выключение музыки
        self.music_key += 1
        if self.music_key % 2 != 0:
            self.song.play()
            self.song.set_volume(0.4)
            self.pushButton_5.setText('Музыка: ON')
        else:
            self.song.stop()
            self.pushButton_5.setText('Музыка: OFF')

    def signer(self, name):  # Разблокировка статистики и игры (переход)
        self.name = name
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setStyleSheet(self.style)
        self.pushButton_3.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_7.setEnabled(True)
        self.pushButton_7.setStyleSheet(self.style)
        self.pushButton_7.setCursor(QtCore.Qt.PointingHandCursor)
        self.label_4.setText('Пользователь:  ' + self.name)

    def global_registration(self):  # Регистрация (переход)
        self.reg_in = Registration()
        self.reg_in.show()

    def played(self):  # Запуск игрового меню (переход)
        self.game_overlay = Overlay(self.name)
        self.game_overlay.show()

    def exit(self):  # Выход
        self.song.stop()
        sys.exit()


class HoverButton(QPushButton):  # Работа с эффектом наведения курсора на кнопку
    mouseHover = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):  # При наводке на кнопку
        if self.isEnabled():
            geom = str(self.geometry())
            geom = geom.split('(')
            geom = list(geom[1][:-1].split(', '))
            self.mouseHover.emit(True)
            # Далее идет проверка, на принадлежность кнопки к какому типу стиля по ее геометрии
            # Во второй функции точно также
            if geom[3] == '40':
                self.setStyleSheet('''font: italic 10pt "Times New Roman";
                    color: rgb(245, 245, 142);
                    background-color: rgb(116, 0, 0);''')
            elif geom[0] == '140' or geom[2] == '591' or geom[2] == '161' or geom[1] == '350':
                self.setStyleSheet('''font: 20pt "Times New Roman";
                color: rgb(245, 245, 142);
                background-color: rgb(116, 0, 0);''')
            elif geom[0] == '330' or geom[1] == '230' or geom[1] == '240':
                self.setStyleSheet('''font: 12pt "Times New Roman";
                color: rgb(245, 245, 142);
                background-color: rgb(116, 0, 0);''')
        else:
            self.setStyleSheet('''font: 20pt "Times New Roman";
                background-color: rgb(168, 168, 168);
                color: rgb(118, 0, 0)''')

    def leaveEvent(self, event):  # В пассивном режиме
        if self.isEnabled():
            geom = str(self.geometry())
            geom = geom.split('(')
            geom = list(geom[1][:-1].split(', '))
            self.mouseHover.emit(False)
            if geom[3] == '40':
                self.setStyleSheet('''font: italic 10pt "Times New Roman";
                    color: rgb(170, 170, 102);
                    background-color: rgb(116, 0, 0);''')
            elif geom[0] == '140' or geom[2] == '591' or geom[2] == '161' or geom[1] == '350':
                self.setStyleSheet('''font: 20pt "Times New Roman";
                color: rgb(170, 170, 102);
                background-color: rgb(116, 0, 0);''')
            elif geom[0] == '330' or geom[1] == '230' or geom[1] == '240':
                self.setStyleSheet('''font: 12pt "Times New Roman";
                color: rgb(170, 170, 102);
                background-color: rgb(116, 0, 0);''')
        else:
            self.setStyleSheet('''font: 20pt "Times New Roman";
                background-color: rgb(168, 168, 168);
                color: rgb(118, 0, 0)''')


class Registration(QMainWindow):  # Регистрация
    def __init__(self):
        super().__init__()
        uic.loadUi('registration_table.ui', self)
        self.setFixedSize(QSize(303, 294))
        self.connection = sqlite3.connect("sign_in.db")
        self.style = '''font: 12pt "Times New Roman";
                color: rgb(170, 170, 102);
                background-color: rgb(116, 0, 0);'''

        self.pushButton_6 = HoverButton(self)
        self.pushButton_6.clicked.connect(self.close)
        self.pushButton_6.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_6.setStyleSheet(self.style)
        self.pushButton_6.setGeometry(20, 240, 101, 31)
        self.pushButton_6.setText('Назад')

        self.pushButton_5 = HoverButton(self)
        self.pushButton_5.setStyleSheet(self.style)
        self.pushButton_5.setGeometry(180, 240, 101, 31)
        self.pushButton_5.setText('Подтвердить')
        self.pushButton_5.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_5.clicked.connect(self.confirm)

    def confirm(self):  # Ввод данных
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        password_2 = self.lineEdit_3.text()
        # Проверка пароля и на совпадение логинов
        if name != '' and password != '' and password_2 != '':
            res = self.connection.cursor().execute('''SELECT id from users
                WHERE name=?''', (name,)).fetchall()
            if password == password_2:
                if not res:
                    con = sqlite3.connect('sign_in.db')
                    cur = con.cursor()
                    cur.execute(f'''INSERT INTO users(name, password) 
                    VALUES(?, ?)''', (name, password))
                    con.commit()
                    self.close()
                    ex.signer(name)
                else:
                    self.label_6.setText('Аккаунт с таким именем уже существует')
            else:
                self.label_6.setText('Ваши пароли не совпадают')
        else:
            self.label_6.setText('Введите данные')


class Sign(QMainWindow):  # Вход в профиль
    def __init__(self):
        super().__init__()
        uic.loadUi('sign.ui', self)
        self.style = '''font: 12pt "Times New Roman";
                color: rgb(170, 170, 102);
                background-color: rgb(116, 0, 0);'''
        self.setFixedSize(QSize(301, 310))
        self.connection = sqlite3.connect("sign_in.db")
        self.pushButton_6 = HoverButton(self)
        self.pushButton_6.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_6.setStyleSheet(self.style)
        self.pushButton_6.setGeometry(20, 230, 101, 31)
        self.pushButton_6.setText('Назад')
        self.pushButton_6.clicked.connect(self.close)

        self.pushButton_5 = HoverButton(self)
        self.pushButton_5.setStyleSheet(self.style)
        self.pushButton_5.setGeometry(180, 230, 101, 31)
        self.pushButton_5.setText('Подтвердить')
        self.pushButton_5.clicked.connect(self.confirming)
        self.pushButton_5.setCursor(QtCore.Qt.PointingHandCursor)

    def confirming(self):  # Проверка
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if password != '' and name != '':
            res = self.connection.cursor().execute('''SELECT password from users
                WHERE name=?''', (name,)).fetchall()
            if res:
                if password == str(res[0][0]):
                    self.close()
                    ex.signer(name)
                else:
                    self.label_4.setText('Неверный пароль')
            else:
                self.label_4.setText('Пользователя с таким логином не существует')
        else:
            self.label_4.setText('Введите данные')


class Rules(QMainWindow):  # Правила
    def __init__(self):
        super().__init__()
        uic.loadUi('rules.ui', self)
        self.setFixedSize(QSize(510, 676))

        self.style = 'font: 20pt "Times New Roman";\n' \
                     '\ncolor: rgb(170, 170, 102);\nbackground-color: rgb(116, 0, 0);'

        self.pixmap = QPixmap("images/bomb_grey.jpg")
        self.pixmap_2 = QPixmap("images/bomb_red.jpg")
        self.pixmap_3 = QPixmap("images/bomb_green.jpg")
        self.pixmap_4 = QPixmap("images/Flajock.png")

        # Установка изображений
        self.pixmap = self.pixmap.scaled(41, 41, Qt.KeepAspectRatio)
        self.label_4.setPixmap(self.pixmap)

        self.pixmap_2 = self.pixmap_2.scaled(41, 41, Qt.KeepAspectRatio)
        self.label_7.setPixmap(self.pixmap_2)

        self.pixmap_3 = self.pixmap_3.scaled(41, 41, Qt.KeepAspectRatio)
        self.label_9.setPixmap(self.pixmap_3)

        self.pixmap_4 = self.pixmap_4.scaled(41, 41, Qt.KeepAspectRatio)
        self.label_11.setPixmap(self.pixmap_4)

        self.pushButton_6 = HoverButton(self)
        self.pushButton_6.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_6.setStyleSheet(self.style)
        self.pushButton_6.setGeometry(140, 590, 221, 41)
        self.pushButton_6.setText('Назад')
        self.pushButton_6.clicked.connect(self.close)


class Statistics(QMainWindow):  # Статистика
    def __init__(self, name):
        super().__init__()
        uic.loadUi('statistic_table.ui', self)
        self.setFixedSize(QSize(610, 604))
        self.name = name
        self.style = 'font: 20pt "Times New Roman";\n' \
                     '\ncolor: rgb(170, 170, 102);\nbackground-color: rgb(116, 0, 0);'
        self.pushButton_6 = HoverButton(self)
        self.pushButton_6.clicked.connect(self.close)
        self.pushButton_6.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_6.setStyleSheet(self.style)
        self.pushButton_6.setGeometry(10, 550, 591, 31)
        self.pushButton_6.setText('Выход')
        self.connection = sqlite3.connect("sign_in.db")
        self.sortable = 2
        self.label_2.setText(self.name)
        self.main()
        self.standard()
        self.normale()
        self.big()
        self.pushButton.clicked.connect(self.standard)
        self.pushButton_2.clicked.connect(self.normale)
        self.pushButton_3.clicked.connect(self.big)
        self.event = ['Количеству мин', 'Времени', 'Уровню сложности']
        self.comboBox.addItems(self.event)
        self.comboBox.activated[str].connect(self.onActivated)
        self.comboBox_2.addItems(self.event)
        self.comboBox_2.activated[str].connect(self.onActivated)
        self.comboBox_3.addItems(self.event)
        self.comboBox_3.activated[str].connect(self.onActivated)

    def onActivated(self, text):  # Выбор пользователем сортировки
        title_sort = text
        if title_sort == self.event[0]:
            self.sortable = 2
        elif title_sort == self.event[1]:
            self.sortable = 3
        elif title_sort == self.event[2]:
            self.sortable = 4

    def main(self):  # Раздел личной статистики
        res_1 = self.connection.cursor().execute(f'''SELECT *
            FROM stats JOIN game_mods
            ON stats.game_mode_id = game_mods.game_mod_id
            ORDER BY game_mode_id DESC''').fetchall()
        res_main = self.connection.cursor().execute('''SELECT id from users
                WHERE name=?''', (self.name,)).fetchall()
        name_id = res_main[0][0]
        main_stats = []
        for i, row in enumerate(res_1):
            res_1[i] = list(res_1[i])
            if res_1[i][1] == name_id:
                main_stats.append([res_1[i][2], res_1[i][3], res_1[i][5],
                                   res_1[i][7]])
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Площадь', 'Мины', 'Время', 'Уровень сложности'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(main_stats):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def standard(self):  # Раздел общей статистики поля стандартного размера
        res_2 = self.connection.cursor().execute(f'''SELECT *
            FROM stats JOIN users
            ON stats.name_id = users.id
            ORDER BY time DESC''').fetchall()
        standard_stats = []
        for i, row in enumerate(res_2):
            res_2[i] = list(res_2[i])
            if res_2[i][2] == 400 and (res_2[i][3] == 28 or
                                       res_2[i][3] == 52 or res_2[i][3] == 80):
                standard_stats.append([res_2[i][7], res_2[i][2], res_2[i][3],
                                       res_2[i][5], res_2[i][4]])
        standard_stats.sort(key=lambda x: x[self.sortable])
        if self.sortable == 4 or self.sortable == 2:
            standard_stats.reverse()
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(['Имя', 'Площадь', 'Мины', 'Время', 'Уровень сложности'])
        self.tableWidget_2.setRowCount(0)
        for i, row in enumerate(standard_stats):
            self.tableWidget_2.setRowCount(
                self.tableWidget_2.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_2.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.show()

    def normale(self):  # Раздел общей статистики поля среднего размера
        res_3 = self.connection.cursor().execute(f'''SELECT *
            FROM stats JOIN users
            ON stats.name_id = users.id
            ORDER BY time DESC''').fetchall()
        normal_stats = []
        for i, row in enumerate(res_3):
            res_3[i] = list(res_3[i])
            if res_3[i][2] == 625 and (res_3[i][3] == 44 or
                                       res_3[i][3] == 81 or res_3[i][3] == 125):
                normal_stats.append([res_3[i][7], res_3[i][2], res_3[i][3],
                                     res_3[i][5], res_3[i][4]])
        normal_stats.sort(key=lambda x: x[self.sortable])
        if self.sortable == 4:
            normal_stats.reverse()
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setHorizontalHeaderLabels(['Имя', 'Площадь', 'Мины', 'Время',
                                                      'Уровень сложности'])
        self.tableWidget_3.setRowCount(0)
        for i, row in enumerate(normal_stats):
            self.tableWidget_3.setRowCount(
                self.tableWidget_3.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_3.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.show()

    def big(self):  # Раздел общей статистики поля большого размера
        res_4 = self.connection.cursor().execute(f'''SELECT *
            FROM stats JOIN users
            ON stats.name_id = users.id
            ORDER BY time DESC''').fetchall()
        big_stats = []
        for i, row in enumerate(res_4):
            res_4[i] = list(res_4[i])
            if res_4[i][2] == 1225 and (res_4[i][3] == 86 or
                                        res_4[i][3] == 159 or res_4[i][3] == 245):
                big_stats.append([res_4[i][7], res_4[i][2], res_4[i][3],
                                  res_4[i][5], res_4[i][4]])
        big_stats.sort(key=lambda x: x[self.sortable])
        if self.sortable == 4:
            big_stats.reverse()
        self.tableWidget_4.setColumnCount(5)
        self.tableWidget_4.setHorizontalHeaderLabels(['Имя', 'Площадь', 'Мины', 'Время',
                                                      'Уровень сложности'])
        self.tableWidget_4.setRowCount(0)
        for i, row in enumerate(big_stats):
            self.tableWidget_4.setRowCount(
                self.tableWidget_4.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_4.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.show()


class Overlay(QMainWindow):  # Предыгровое меню
    def __init__(self, name):
        super().__init__()
        self.name = name
        uic.loadUi('game_overlay.ui', self)
        self.setFixedSize(QSize(420, 438))
        self.style = 'font: 20pt "Times New Roman";\n' \
                     '\ncolor: rgb(170, 170, 102);\nbackground-color: rgb(116, 0, 0);'

        self.pushButton = HoverButton(self)
        self.pushButton.clicked.connect(self.run_level)
        self.pushButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton.setStyleSheet(self.style)
        self.pushButton.setGeometry(250, 350, 151, 41)
        self.pushButton.setText('Играть')

        self.pushButton_2 = HoverButton(self)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_2.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_2.setStyleSheet(self.style)
        self.pushButton_2.setGeometry(20, 350, 151, 41)
        self.pushButton_2.setText('Назад')

        self.pixmap = QPixmap('images/bomb_grey.jpg')
        self.pixmap = self.pixmap.scaled(71, 71, Qt.KeepAspectRatio)
        self.label_7.setPixmap(self.pixmap)
        self.pixmap_2 = QPixmap('images/bomb_green.jpg')
        self.pixmap_2 = self.pixmap_2.scaled(71, 71, Qt.KeepAspectRatio)
        self.label_9.setPixmap(self.pixmap_2)
        self.pixmap_3 = QPixmap('images/bomb_red.jpg')
        self.pixmap_3 = self.pixmap_3.scaled(71, 71, Qt.KeepAspectRatio)
        self.label_8.setPixmap(self.pixmap_3)
        self.list_plain = ['Стандарт(20 х 20)', 'Средний(25 х 25)', 'Большой(35 х 35)',
                           'Свой размер']
        self.comboBox.addItems(self.list_plain)
        self.comboBox.activated[str].connect(self.onActivated)
        self.list_complexity = ['Легкая', 'Нормальная', 'Сложная', 'Своя сложность']
        self.complexity = self.list_complexity[0]
        self.comboBox_2.addItems(self.list_complexity)
        self.comboBox_2.activated[str].connect(self.onActivated_2)
        self.lineEdit.setText('20')
        self.lineEdit_2.setText('20')
        self.koeff = 0.07
        self.game_mod_id = 1
        self.lineEdit_3.setText(str(
            round(int(self.lineEdit.text()) * int(self.lineEdit_2.text()) * self.koeff)))

    def run_level(self):  # Запуск самого уровня с выбранными параметрами
        if self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and \
                self.lineEdit_3.text() != '' and self.lineEdit_3.text() != '0' and \
                int(self.lineEdit.text()) >= 10 and int(self.lineEdit_2.text()) >= 10:
            self.grang_game = Level(int(self.lineEdit.text()), int(self.lineEdit_2.text()),
                                    int(self.lineEdit_3.text()), self.name, self.game_mod_id)
            self.grang_game.show()
            ex.hide()
            self.close()

    def onActivated(self, text):  # Выбор размера поля
        size_plain_str = text
        if size_plain_str != self.list_plain[-1]:
            if size_plain_str == self.list_plain[0]:
                self.lineEdit.setText('20')
                self.lineEdit_2.setText('20')

            elif size_plain_str == self.list_plain[1]:
                self.lineEdit.setText('25')
                self.lineEdit_2.setText('25')

            elif size_plain_str == self.list_plain[2]:
                self.lineEdit.setText('35')
                self.lineEdit_2.setText('35')

            self.lineEdit.setDisabled(True)
            self.lineEdit_2.setDisabled(True)
            if self.complexity != self.list_complexity[-1]:
                self.lineEdit_3.setText(str(
                    round(int(self.lineEdit.text()) * int(self.lineEdit_2.text()) * self.koeff)))
        else:
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.lineEdit_3.setText('')

    def onActivated_2(self, text):  # Выбор уровня сложности
        self.complexity = text
        if self.complexity != self.list_complexity[-1]:
            if self.complexity == self.list_complexity[0]:
                self.koeff = 0.07
                self.game_mod_id = 1
            elif self.complexity == self.list_complexity[1]:
                self.koeff = 0.13
                self.game_mod_id = 2
            elif self.complexity == self.list_complexity[2]:
                self.koeff = 0.2
                self.game_mod_id = 3
            if self.lineEdit.text() != '' and self.lineEdit_2.text() != '':
                self.lineEdit_3.setText(str(
                    round(int(self.lineEdit.text()) * int(self.lineEdit_2.text()) * self.koeff)))
                self.lineEdit_3.setDisabled(True)
        else:
            self.lineEdit_3.setText('')
            self.lineEdit_3.setEnabled(True)
            self.game_mod_id = 4


class Level(QMainWindow):  # Игра
    # На вход принимает параметры из класса "Overlay"
    def __init__(self, x_eternal, y_eternal, bomb, name, game_mod):

        """Сам уровень имеет такую схему:
        сначала создается карта поля в массиве,
        потом по ней заполняются Label,
        а сверху, на них накладываются кнопки PushButton.
        То есть кнопки скрывают поле от игрока"""

        super().__init__()
        uic.loadUi('level.ui', self)
        self.style = '''font: italic 10pt "Times New Roman";
                    color: rgb(170, 170, 102);
                    background-color: rgb(116, 0, 0);'''
        self.pinponging_musik = pygame.mixer.Sound('music/pinponging.mp3')
        self.pinponging_musik.set_volume(0.5)

        self.explosion_musik = pygame.mixer.Sound('music/explosion.mp3')
        self.explosion_musik.set_volume(0.5)

        self.casino_final = pygame.mixer.Sound('music/casino_final.mp3')
        self.casino_final.set_volume(0.5)

        self.win_sound = pygame.mixer.Sound('music/win_sound.mp3')
        self.flag_sound = pygame.mixer.Sound('music/flag_1.mp3')


        self.timeInterval = 1000  # Интервал времени - 1 секунда
        self.name = name
        self.count_bomb = bomb
        self.game_mod_id = game_mod
        self.setFixedSize(QSize((x_eternal * 20) + 40, (y_eternal * 20) + 105))
        self.widget.setGeometry(20, 20, x_eternal * 20, y_eternal * 20)
        self.plain = (x_eternal * y_eternal)
        self.x_eternal = x_eternal
        self.y_eternal = y_eternal
        # Высчитывается геометрия кнопок, таймера и счетчика флагов
        self.LCD_count_flag.setGeometry(20, ((y_eternal * 20) + 30),
                                        (x_eternal * 5), 40)
        self.lcdNumber_2.setGeometry(((x_eternal * 20) + 20 - (x_eternal * 5)),
                                     ((y_eternal * 20) + 30),
                                     (x_eternal * 5), 40)
        self.replay = HoverButton(self)
        self.replay.setCursor(QtCore.Qt.PointingHandCursor)
        self.replay.setStyleSheet(self.style)
        self.replay.setText('Заново')
        self.replay.setGeometry((x_eternal * 5) + 21, ((y_eternal * 20) + 30),
                                round(4.55 * x_eternal), 40)
        self.replay.clicked.connect(self.will_row)  # Перезапуск уровня

        self.replay_2 = HoverButton(self)
        self.replay_2.setCursor(QtCore.Qt.PointingHandCursor)
        self.replay_2.setStyleSheet(self.style)
        self.replay_2.setText('Выйти')
        self.replay_2.setGeometry(((x_eternal * 20) + 19 - (x_eternal * 5)) - round(4.55 * x_eternal),
                                  (y_eternal * 20) + 30, round(4.55 * x_eternal), 40)
        self.replay_2.clicked.connect(self.exited)
        # Изображения видов мин
        self.pixmap = QPixmap('images/bomb_light_theme.jpg')
        self.neutral_pixmap = QPixmap('images/bomb_green_theme.jpg')
        self.danger_pixmap = QPixmap('images/bomb_red_theme.jpg')
        self.flajock = QIcon('images/Flajock.png')
        self.pixmap = self.pixmap.scaled(20, 20, Qt.KeepAspectRatio)
        self.neutral_pixmap = self.neutral_pixmap.scaled(20, 20, Qt.KeepAspectRatio)
        self.danger_pixmap = self.danger_pixmap.scaled(20, 20, Qt.KeepAspectRatio)

        # Объявление таймера
        self.timerUp = QTimer()
        self.time = 0
        # Запуск основного процесса
        self.engine()

    def engine(self):  # Объявляет переменные
        self.LCD_count_flag.display(self.count_bomb)
        self.count_red_flag = self.count_bomb
        self.count_flag = []
        self.flag_list = []
        self.list_btn = []
        self.list_lbl = []

        # Переход на функцию, создающую карту будущей игры
        self.get_map_mines()

        # Заполнение карты соответствующими объектами
        y = 20
        numeric = 0
        for i in range(self.y_eternal):
            x = 20
            for u in range(self.x_eternal):
                numeric += 1
                self.label = QLabel(self)
                self.label.move(x, y)
                self.label.resize(19, 19)

                # Переход на функцию, которая ставит и красит цифры, устанавливает изображения и иконки
                # Принимает на вход объект и соответсвующую ему координату на карте
                self.set_text_on_label(self.label, self.reader[i][u])

                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setObjectName(f'label_{str(numeric)}')
                self.pushButton = QPushButton(self)
                self.pushButton.move(x, y)
                self.pushButton.setText('')
                self.pushButton.resize(19, 19)
                self.pushButton.clicked.connect(self.push)
                self.pushButton.setStyleSheet('background-color: rgb(235, 235, 235);')
                self.pushButton.setCursor(QtCore.Qt.PointingHandCursor)
                self.pushButton.setObjectName(f'pushButton_{str(numeric)}')
                self.list_btn.append(self.pushButton)
                self.list_lbl.append(self.label)
                x += 20
            y += 20

    def set_text_on_label(self, object, elem):

        """
        Функция для каждого Label-виджета зыполняет его цифрой и стилем.
        Чтобы не путать пустые клетки и мины,
        мы заполняем пустые клетки пробелом в "label."
        """

        if elem == 'b':
            object.setPixmap(self.pixmap)
            object.setText('')
        elif elem == '1':
            object.setText('1')
            object.setStyleSheet('''color: rgb(0, 85, 255);
                \nbackground-color: rgb(200, 200, 200);''')
            object.setFont(QFont("Areal", 10, QFont.Bold))
        elif elem == '2':
            object.setText('2')
            object.setStyleSheet('''color: rgb(0, 170, 0);
                \nbackground-color: rgb(200, 200, 200);''')
            object.setFont(QFont("Areal", 10, QFont.Bold))
        elif elem == '3':
            object.setText('3')
            object.setStyleSheet('''color: rgb(255, 0, 0);
                \nbackground-color: rgb(200, 200, 200);''')
            object.setFont(QFont("Areal", 10, QFont.Bold))
        elif elem == '4':
            object.setText('4')
            object.setStyleSheet('''color: rgb(0, 0, 127);
                \nbackground-color: rgb(200, 200, 200);''')
            object.setFont(QFont("Areal", 10, QFont.Bold))
        elif elem == '5':
            object.setText('5')
            object.setStyleSheet('''color: rgb(170, 0, 0);
                \nbackground-color: rgb(200, 200, 200);''')
            object.setFont(QFont("Areal", 10, QFont.Bold))
        elif elem == '6':
            object.setText('6')
            object.setStyleSheet('''color: rgb(0, 255, 255);
                \nbackground-color: rgb(200, 200, 200);''')
            object.setFont(QFont("Areal", 10, QFont.Bold))
        elif elem == '7':
            object.setText('7')
            object.setStyleSheet('''color: rgb(0, 0, 0);
                \nbackground-color: rgb(200, 200, 200);''')
            object.setFont(QFont("Areal", 10, QFont.Bold))
        elif elem == '8':
            object.setText('8')
            object.setStyleSheet('''color: rgb(132, 132, 132);
                \nbackground-color: rgb(200, 200, 200);''')
            object.setFont(QFont("Areal", 10, QFont.Bold))
        else:
            object.setText(' ')
            object.setStyleSheet('background-color: rgb(200, 200, 200);')
            object.setFont(QFont("Areal", 10, QFont.Bold))

    def get_map_mines(self, key=-1):

        """Сначала для получения карты, мы  находим случайно номера элементов,
        в которых будут мины. Далее мы заполняем прилегающие с минами клетки цифрами.
        Функция имеет необязательный параметр key,
        равный -1 по умолчанию. С помощью него мы сможем вернуться сюда в случае,
        если игрок нажмет в первый раз на мину. При этом параметр key будет равен номеру ячейки,
        в которой не должно оказаться бомбы"""

        self.touch = 0
        self.ihner_bomb = []
        self.global_list = []

        # Карта мин
        for t in range(self.count_bomb):
            change = choice(list(i for i in range(self.x_eternal * self.y_eternal)))
            if key == -1:
                while change in self.ihner_bomb:
                    change = choice(list(i for i in range(self.x_eternal * self.y_eternal)))
            else:
                while change in self.ihner_bomb or change == key:
                    change = choice(list(i for i in range(self.x_eternal * self.y_eternal)))
            self.ihner_bomb.append(change)

        # Мины обозначем буквой "b"
        self.reader = []
        num = 0
        for s in range(self.y_eternal):
            a = []
            for n in range(self.x_eternal):
                num += 1
                if num in self.ihner_bomb:
                    a.append('b')
                else:
                    a.append('')
            self.reader.append(a)

        # По карте бомб заполняем ячейки
        for i in range(self.y_eternal):
            for u in range(self.x_eternal):
                koeff = 0
                if i == 0 and u == 0:  # Инструкция для ячейки левого верхнего угла
                    if self.reader[i][u + 1] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u + 1] == 'b':
                        koeff += 1
                elif i == 0 and u != self.x_eternal - 1:  # Инструкция для ячейки, прилигающей к верхней границе
                    if self.reader[i][u + 1] == 'b':
                        koeff += 1
                    if self.reader[i][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u + 1] == 'b':
                        koeff += 1
                elif i == 0 and u == self.x_eternal - 1:  # Инструкция для ячейки правого верхнего угла
                    if self.reader[i][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u - 1] == 'b':
                        koeff += 1
                elif u == 0 and i != self.y_eternal - 1:  # Инструкция для ячейки, прилигающей к левой границе
                    if self.reader[i][u + 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u + 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u + 1] == 'b':
                        koeff += 1
                elif u == 0 and i == self.y_eternal - 1:  # Инструкция для ячейки левого нижнего угла
                    if self.reader[i][u + 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u + 1] == 'b':
                        koeff += 1
                elif i == self.y_eternal - 1 and u != 0 and u != self.x_eternal - 1:  # Инструкция для ячейки, прилигающей к нижней границе
                    if self.reader[i][u + 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u + 1] == 'b':
                        koeff += 1
                elif u == self.x_eternal - 1 and i != self.y_eternal - 1 and i != 0:  # Инструкция для ячейки, прилигающей к правой границе
                    if self.reader[i - 1][u] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u] == 'b':
                        koeff += 1
                    if self.reader[i][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u - 1] == 'b':
                        koeff += 1
                elif u == self.x_eternal - 1 and i == self.y_eternal - 1:  # Инструкция для ячейки правого нижнего угла
                    if self.reader[i][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u - 1] == 'b':
                        koeff += 1
                elif i != 0 and i != self.y_eternal - 1 and u != 0 and u != self.x_eternal - 1:
                    # Инструкции для всех остальных, непограничных ячеек
                    if self.reader[i][u + 1] == 'b':
                        koeff += 1
                    if self.reader[i][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i + 1][u + 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u - 1] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u] == 'b':
                        koeff += 1
                    if self.reader[i - 1][u + 1] == 'b':
                        koeff += 1
                if self.reader[i][u] != 'b':
                    self.reader[i][u] = str(koeff)

    def will_row(self):
        """
        Перезапуск от пользователя (оптимизированная версия функции engine,
        только без создания объектов, а с их изменениями)
        """
        # Очищаем переменные
        self.time = 0
        self.spisok_map = []
        self.count_flag = []
        self.flag_list = []
        self.LCD_count_flag.display(self.count_bomb)
        self.count_red_flag = self.count_bomb

        # Скрыть все кнопки и очистить label
        for i in self.list_btn:
            i.setIcon(self.flajock)
            i.setIconSize(QSize(0, 0))
        for u in self.list_lbl:
            u.hide()
        self.get_map_mines()
        for u in self.reader:
            for i in u:
                self.spisok_map.append(i)
        i = 0
        for elem in self.spisok_map:
            # Заполнение
            self.set_text_on_label(self.list_lbl[i], elem)

            self.list_lbl[i].show()
            self.list_lbl[i].setAlignment(QtCore.Qt.AlignCenter)
            i += 1
        # Показать все кнопки
        for u in self.list_btn:
            u.show()
        self.pinponging_musik.play()

    def first_touch_is_bomb(self, total):

        """В случае, если первое касание выпадает на мину,
        карта заново генерируется и открывается та ячейка,
        которую нажал игрок.
        Функция принимает параметр total - номер ячейки, на
        которую нажал игрок"""

        self.spisok_map = []
        self.count_flag = []
        self.flag_list = []
        self.count_red_flag = self.count_bomb
        self.get_map_mines(key=total)
        for u in self.reader:
            for i in u:
                self.spisok_map.append(i)
        i = 0
        for elem in self.spisok_map:
            self.set_text_on_label(self.list_lbl[i], elem)
            self.list_lbl[i].show()
            self.list_lbl[i].setAlignment(QtCore.Qt.AlignCenter)
            i += 1
        child = self.findChild(QPushButton, f'pushButton_{total}')
        # Имитируем нажатие
        child.animateClick()

    def mousePressEvent(self, event):
        """Инициализирует нажатие правой клавиши и
        передает координату места ее нажатия в функцию флага"""
        if event.button() == Qt.RightButton:
            self.flag(event.x(), event.y())

    def none_label_cheat(self):

        """Функция, отвечающая за открытие всех смежных ячеек,
        в случае открытия пустой ячейки.
        Чтобы избежать сбоя и нечестно отобранного времени, то
        пока работает эта функция - таймер выключен"""

        self.timerUp.stop()
        flag = True
        while flag:
            k = 0
            for num in range(len(self.list_lbl)):
                # Инструкции для элементов
                parameters = [num + 1, num - 1, num - self.x_eternal, num - self.x_eternal + 1,
                              num - self.x_eternal - 1, num + self.x_eternal, num + self.x_eternal + 1,
                              num + self.x_eternal - 1]
                if self.list_lbl[num].text() == ' ' and self.list_btn[num].isHidden() and \
                        num not in self.global_list:
                    for i in parameters:
                        if 0 < i + 1 <= (self.x_eternal * self.y_eternal):
                            # Инструкции для крайних элементов
                            if (num + 1) % self.x_eternal == 0:
                                if i != parameters[0] and i != parameters[3] and i != parameters[6]:
                                    if not self.list_btn[i].isHidden():
                                        if (i + 1) not in self.flag_list:
                                            self.list_btn[i].hide()
                                    k = 1
                            elif (num + 1) % self.x_eternal == 1:
                                if i != parameters[1] and i != parameters[4] and i != parameters[7]:
                                    if not self.list_btn[i].isHidden():
                                        if (i + 1) not in self.flag_list:
                                            self.list_btn[i].hide()
                                    k = 1
                            else:
                                k = 1
                                if (i + 1) not in self.flag_list:
                                    self.list_btn[i].hide()
                    self.global_list.append(num)
                    break
            if k == 0:
                flag = False
            # *Продолжает работать таймер*
            self.run_time()

    def push(self):

        """Нажатие левой кнопки мыши по PushButton,
        провоцирует скрытие этого PushButton"""

        self.touch += 1
        coord = str(self.sender().geometry())
        # Находим по координатам нажатой кнопки порядковое число его на карте
        coordination = ((coord.split('(')[1])[:-1]).split(', ')
        x1 = int(coordination[0])
        y1 = int(coordination[1])
        x_main = (x1 // 20)
        y_main = ((y1 // 20) - 1) * self.x_eternal
        if x_main == 0:
            x_main = 1
        total = str(x_main + y_main)
        # Находим Label по его номеру в названии объекта
        child_2 = self.findChild(QLabel, f'label_{total}')
        if int(total) not in self.flag_list:
            if child_2.text() == '' and self.touch == 1:  # Если первое касание - выпадает на мину
                self.first_touch_is_bomb(total)
            else:
                if self.touch == 1:  # Если нажал в первый раз, запуск таймера
                    self.run_time()
                self.sender().hide()
                if child_2.text() == '':  # Если нажатие(не первое) выпадает на мину
                    # Останавливаем таймер
                    self.timerUp.stop()
                    child_2.setPixmap(self.danger_pixmap)
                    child_2.setText('')
                    child_2.setAlignment(QtCore.Qt.AlignCenter)
                    for i in self.list_btn:
                        i.hide()
                    self.explosion_musik.play()
                else:
                    if child_2.text() == ' ':  # Если нажатие на пустое поле, переходим в соответствующую функцию
                        self.none_label_cheat()
                    self.casino_final.play()

    def flag(self, x, y):

        """Отвечает за поставление на PushButton иконки флажка.
        При закрытии всех бомб флажками игра закончится.
        Все номера флажков добавляем в список"""

        # Находим номер ячейки по координатам от MouseEvent
        x1 = (x // 20)
        y1 = ((y // 20) - 1) * self.x_eternal
        if x1 == 0:
            x1 = 1
        total = str(x1 + y1)

        # Находим объекты по их названию
        child = self.findChild(QPushButton, f'pushButton_{total}')
        child_2 = self.findChild(QLabel, f'label_{total}')
        total = int(total)

        # Проверка на то, что такие объекты вообще существуют и уже не скрыты
        if child is not None and child_2 is not None and not child.isHidden():
            # Если флага на этом месте еще нет
            if total not in self.flag_list:  # Если такого порядкого номера еще нет в списке флагов
                if self.count_red_flag > 0:  # Если у игрока еще есть в наличии флаги
                    # Устанавливаем иконку в кнопку
                    child.setIcon(self.flajock)
                    child.setIconSize(QSize(19, 19))
                    # Добавляем в список флагов порядковое число нового флага
                    self.flag_list.append(total)
                    if total in self.ihner_bomb:  # Устанавливаем зеленую картинку бомбы, если флаг стоит над бомбой
                        child_2.setPixmap(self.neutral_pixmap)
                        child_2.setAlignment(QtCore.Qt.AlignCenter)
                    # Отображаем на табло количество флажков в наличии у игрока
                    self.count_red_flag = self.count_bomb - len(self.flag_list)
                    self.LCD_count_flag.display(self.count_red_flag)

            else:  # Если флаг уже стоит, то мы его убираем
                child.setIcon(self.flajock)
                child.setIconSize(QSize(0, 0))
                self.flag_list.remove(total)
                if total in self.ihner_bomb:  # Убираем зеленую картинку бомбы, если флаг стоял над бомбой
                    child_2.setPixmap(self.pixmap)
                    child_2.setText('')
                    child_2.setAlignment(QtCore.Qt.AlignCenter)
                # Отображаем на табло количество флажков в наличии у игрока
                self.count_red_flag = self.count_bomb - len(self.flag_list)
                self.LCD_count_flag.display(self.count_red_flag)

            # Если список расставленных флагов совпадает с списком мин
            if sorted(self.flag_list) == sorted(self.ihner_bomb):
                # При победе все кнопки скрываются, открывается окно с итогами игры
                self.timerUp.stop()
                self.win_sound.play()
                for i in self.list_btn:
                    i.hide()
                self.present = Congratulations(self.count_bomb, self.plain, self.time, self.name,
                                          self.game_mod_id)


            else:
                self.flag_sound.play()

    def run_time(self):
        """Эта и последующие 2 функции
        отвечают за работу таймера"""
        self.timerUp = QTimer()
        self.settimer(self.time)
        self.timerUp.setInterval(self.timeInterval)
        self.timerUp.timeout.connect(self.updateUptime)
        self.timerUp.start()

    def updateUptime(self):
        self.time += 1
        self.settimer(self.time)

    def settimer(self, int):
        self.lcdNumber_2.display(int)

    def exited(self):
        self.close()
        ex.show()


class Congratulations(QMainWindow):
    def __init__(self, mines, count_plain, time, name, game_mod):
        """Поздравления,
        запись результатов в БД"""
        super().__init__()
        uic.loadUi('congratulations.ui', self)
        self.connection = sqlite3.connect("sign_in.db")
        self.style = 'font: 20pt "Times New Roman";\n' \
                     '\ncolor: rgb(170, 170, 102);\nbackground-color: rgb(116, 0, 0);'
        self.setFixedSize(QSize(350, 368))
        self.pushButton = HoverButton(self)
        self.pushButton.clicked.connect(self.close)
        self.pushButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton.setStyleSheet(self.style)
        self.pushButton.setGeometry(100, 280, 161, 41)
        self.pushButton.setText('Назад')
        self.name = name
        self.mines = mines
        self.count_plain = count_plain
        self.time = time
        self.game_mod = game_mod
        self.result()

    def result(self):
        self.label_9.setText(str(self.name))
        self.label_6.setText(str(self.mines))
        self.label_7.setText(str(self.count_plain))
        self.label_8.setText(str(self.time))
        # Запись в базу данных
        self.res = self.connection.cursor().execute('''SELECT id from users
                WHERE name=?''', (self.name,)).fetchall()
        name_id = self.res[0][0]
        con = sqlite3.connect('sign_in.db')
        cur = con.cursor()
        cur.execute(f'''INSERT INTO stats(name_id, size, bombs, game_mode_id, time) 
        VALUES(?, ?, ?, ?, ?)''', (name_id, self.count_plain, self.mines,
                                   self.game_mod, self.time))
        con.commit()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Minesweeper()
    ex.show()
    sys.exit(app.exec())
