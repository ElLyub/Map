from mymapapi import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton 
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
 
W = 400
H = 580
dMenu = 20 #для кнопок setDisable(True)
m = 10 #отступ
map_w, map_h = W -2 * m, H - dMenu - 2 * m


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setGeometry(100, 100, W, H) #(положение на экране,..,..)
        self.setWindowTitle('Карта')

        self.maps = "one.png"
         
        self.btn = QPushButton('Отобразить', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(W //3 * 2, 30)
        self.btn.clicked.connect(self.show_map_file)
 
        self.label = QLabel(self)
        self.label.setText("Введите координаты центра карты или название объекта:")
        self.label.move(10, 10)

        self.label_2 = QLabel(self)
        self.label_2.setText("Адрес объекта")
        self.label_2.resize(map_w, 25)
        self.label_2.move(10, 88)

        self.label_3 = QLabel(self)
        self.label_3.setText("")
        self.label_3.resize(map_w, 25)
        self.label_3.move(10, 105)
 
        self.lat_input = QLineEdit(self)
        self.lat_input.resize(80,25)
        self.lat_input.move(m, 30)
        self.lat_input.setText("55.7507")
        self.lon_input = QLineEdit(self)
        self.lon_input.resize(80,25)
        self.lon_input.move(100, 30)
        self.lon_input.setText("37.6256")

        #строка поиска
        self.search_input = QLineEdit(self)
        self.search_input.resize(W // 4 * 2.5,25)
        self.search_input.move(m, 60)
        self.search_input.textChanged[str].connect(self.onChanged)
        self.search_btn = QPushButton('Искать', self)
        self.search_btn.resize(W // 5 - 30, 25)
        self.search_btn.move(W // 4 * 2.6 + 20, 60)
        self.search_btn.clicked.connect(self.search_address)
        self.search_btn.setDisabled(True)

        self.pixmap = QPixmap(self.maps)
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.setGeometry(m , m + dMenu, map_w, map_h)
        self.lbl.move(10, 85)

        self.btn_2 = QPushButton('+', self)
        self.btn_2.resize(30,30)
        self.btn_2.move(W - 40 ,  H // 6 - 75)
        self.btn_2.clicked.connect(self.button_clicked_plus)

        self.btn_3 = QPushButton('-', self)
        self.btn_3.resize(30, 30)
        self.btn_3.move(W - 40 ,  H // 6 - 45)
        self.btn_3.clicked.connect(self.button_clicked_min)

        self.btn_5 = QPushButton('Сброс поискового результата', self)
        self.btn_5.resize(W // 4 * 2.5, 20)
        self.btn_5.move(m, 130)
        self.btn_5.clicked.connect(self.del_point)
        self.btn_5.setDisabled(True)

        self.combo = QComboBox(self)
        self.combo.resize(60, 25)
        self.combo.addItems(["map", "sat", "sat,skl"])
        self.combo.move(W // 2 - 10, 30)
        self.combo.activated[str].connect(self.onActivated)

        self.combo_ind = QComboBox(self)
        self.combo_ind.resize(85, 20)
        self.combo_ind.addItems(["без индекса", "с индексом"])
        self.combo_ind.move(98, 90)
        self.combo_ind.activated[str].connect(self.onActivated_2)
         
        self.count = 0
        self.z = 8
        self.map_type = "map"
        self.point = ""
        self.SF = ""
        self.index = ""
        self.flag = False
        #setText

    def onChanged(self, text):
        if text:
            self.search_btn.setDisabled(False)
            

    def search_address(self):
        address = self.search_input.text()
        #self.SF = get_fullAdr(address)
        lon, lat = get_coordinates(address)
        org_point = "{0},{1}".format(lon, lat)
        self.point = "&pt={0},pm2dgl".format(org_point)
        self.btn_5.setDisabled(False)
        
        self.lon_input.setText(str(lon))
        self.lat_input.setText(str(lat))
        self.show_map_file()

    def del_point(self):
        self.point = ""
        self.show_map_file()
        self.label_3.setText("")
            
    def button_clicked_plus(self):
        if self.z < 19:
            self.z += 1
            self.show_map_file()
        
    def button_clicked_min(self):
        if self.z > 0:
            self.z -= 1
            self.show_map_file()

    def onActivated(self, text):
        self.map_type = text
        self.show_map_file()

    def onActivated_2(self, text):
        if text == "с индексом":
            self.flag = True
        else:
            self.flag = False
        self.show_map_file()
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_PageUp:
            self.button_clicked_plus()
        elif e.key() == Qt.Key_PageDown:
            self.button_clicked_min()
        elif e.key() == Qt.Key_Up:
            dy = 180 / 2**(self.z) * (map_h / 256)
            lat = float(self.lat_input.text())
            if lat < (90 - dy):
                lat += dy
            self.lat_input.setText(str(lat))
            self.show_map_file()
        elif e.key() == Qt.Key_Down:
            dy = 180 / 2**(self.z) * (map_h / 256)
            lat = float(self.lat_input.text())
            if lat > (-90 + dy):
                lat -= dy
            self.lat_input.setText(str(lat))
            self.show_map_file()
        elif e.key() == Qt.Key_Right:
            dy = 360 / 2**(self.z) * (map_w / 256)
            lon = float(self.lon_input.text())
            if lon < (180 + dy):
                lon += dy
            self.lon_input.setText(str(lon))
            self.show_map_file()
        elif e.key() == Qt.Key_Left:
            dy = 360 / 2**(self.z) * (map_w / 256)
            lon = float(self.lon_input.text())
            if lon > (-180 + dy):
                lon -= dy
            self.lon_input.setText(str(lon))
            self.show_map_file()
        
 
    def show_map_file(self):
        # Показать карту
        lon = self.lon_input.text()
        lat = self.lat_input.text()
        for_req = ",".join([lon,lat])
        self.SF = get_fullAdr(for_req)
        if self.flag:
            try:
                self.index = get_index(for_req)
            except:
                self.index = ""
        else:
            self.index = ""
        
        map_locations = "ll=" + ",".join([lon,lat])# + "&spn=1.0,1.0"
        map_type = self.map_type
        map_param = "z={0}&size=400,400{1}".format(str(self.z), self.point)
        f_name = get_file_map(map_locations, map_type,map_param)
        if f_name:
            self.maps = f_name
        
        self.pixmap.load(self.maps)
        self.lbl.setPixmap(self.pixmap)
        
     
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
