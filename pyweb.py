import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class PyWeb(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyWeb")

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.create_new_tab()

        self.nav_bar = QToolBar(self)
        self.addToolBar(self.nav_bar)

        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        self.home_button = QAction("Home", self)
        self.home_button.triggered.connect(self.navigate_home)
        self.nav_bar.addAction(self.home_button)

        self.new_tab_button = QAction("New Tab", self)
        self.new_tab_button.triggered.connect(self.create_new_tab)
        self.nav_bar.addAction(self.new_tab_button)

        self.show()

        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(self.close_current_tab)

        self.shortcut_refresh = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut_refresh.activated.connect(self.refresh_current_tab)

    def create_new_tab(self):
        new_tab = QWebEngineView(self)
        new_tab.setUrl(QUrl("http://www.google.com"))
        new_tab.urlChanged.connect(self.handle_url_change)
        new_tab.loadFinished.connect(self.update_tab_title)

        tab_index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(tab_index)

        self.tabs.tabCloseRequested.connect(self.close_tab)

    def handle_url_change(self, url):
        self.update_url_bar(url)

    def update_url_bar(self, url):
        current_index = self.tabs.currentIndex()
        current_tab = self.tabs.widget(current_index)
        self.url_bar.setText(current_tab.url().toString())

    def update_tab_title(self):
        current_index = self.tabs.currentIndex()
        current_tab = self.tabs.widget(current_index)
        title = current_tab.page().title()
    
        self.tabs.setTabText(current_index, title)

    def navigate_home(self):
        current_index = self.tabs.currentIndex()
        current_tab = self.tabs.widget(current_index)
        current_tab.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        url_text = self.url_bar.text()
        if url_text:
            current_index = self.tabs.currentIndex()
            current_tab = self.tabs.widget(current_index)
            current_tab.setUrl(QUrl(url_text))

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        self.close_tab(current_index)

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        if widget:
            widget.deleteLater()
        self.tabs.removeTab(index)

    def refresh_current_tab(self):
        current_index = self.tabs.currentIndex()
        current_tab = self.tabs.widget(current_index)
        current_tab.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyWeb()
    sys.exit(app.exec_())