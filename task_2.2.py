from mymapapi import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton 
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
 
W = 400
H = 520
dMenu = 50 #для кнопок setDisable(True)
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

        self.combo = QComboBox(self)
        self.combo.resize(60, 25)
        self.combo.addItems(["map", "sat", "sat,skl"])
        self.combo.move(W // 2 - 10, 30)
        self.combo.activated[str].connect(self.onActivated)
         
        self.count = 0
        self.z = 8
        self.map_type = "map"
        self.point = ""
        #setText

    def onChanged(self, text):
        if text:
            self.search_btn.setDisabled(False)

    def search_address(self):
        address = self.search_input.text()
        lon, lat = get_coordinates(address)
        org_point = "{0},{1}".format(lon, lat)
        self.point = "&pt={0},pm2dgl".format(org_point)
        
        self.lon_input.setText(str(lon))
        self.lat_input.setText(str(lat))
        self.show_map_file()
            
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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_PageUp:
            self.button_clicked_plus()
        elif e.key() == Qt.Key_PageDown:
            self.button_clicked_min()
        elif e.key() == Qt.Key_Up:
            dy = 180 / 2**(self.z)
            #if
            lat = float(self.lat_input.text()) + dy
            self.lat_input.setText(str(lat))
            self.show_map_file()
        elif e.key() == Qt.Key_Down:
            dy = 180 / 2**(self.z)
            #if
            lat = float(self.lat_input.text()) - dy
            self.lat_input.setText(str(lat))
            self.show_map_file()
        elif e.key() == Qt.Key_Right:
            dy = 360 / 2**(self.z)
            #if
            lon = float(self.lon_input.text()) + dy
            self.lon_input.setText(str(lat))
            self.show_map_file()
        elif e.key() == Qt.Key_Left:
            dy = 360 / 2**(self.z)
            #if
            lon = float(self.lon_input.text()) + dy
            self.lon_input.setText(str(lat))
            self.show_map_file()
        
 
    def show_map_file(self):
        # Показать карту
        lon = self.lon_input.text()
        lat = self.lat_input.text()
        
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
