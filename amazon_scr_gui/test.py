import sys
from PyQt5.QtWidgets import *
import time
from threading import *
  
class ListBox(QWidget):
  
    def __init__(self):
        super().__init__()
  
        self.Button()
  
    def Button(self):
        # Add Push Button
        clear_btn = QPushButton('Click Me', self)
        clear_btn.clicked.connect(self.thread)
  
        # Set geometry
        self.setGeometry(200, 200, 200, 200)
  
        # Display QlistWidget
        self.show()
  
    def thread(self):
        t1=Thread(target=self.Operation)
        t1.start()
  
    def Operation(self):
        print("time start")
        time.sleep(10)
        print("time stop")
  
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
      
    # Call ListBox Class
    ex = ListBox()
  
    # Close the window
    sys.exit(app.exec_())