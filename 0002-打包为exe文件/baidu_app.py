import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl  # 导入QUrl

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Web Browser")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.baidu.com'))  # 使用QUrl传递网址

        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

def main():
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
