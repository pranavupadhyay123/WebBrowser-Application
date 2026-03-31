import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTabWidget, 
                             QProgressBar, QShortcut, QMenu, QAction, QFileDialog, 
                             QInputDialog)
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEngineSettings, 
                                      QWebEngineProfile)
from PyQt5.QtGui import QKeySequence, QFont, QDesktopServices

# Enable High DPI scaling for sharp text on your Predator's high-resolution screen
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class PrawserTab(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Optimize engine for extreme speed and RTX 4050 hardware acceleration
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        
        # Accept fullscreen requests automatically (e.g., YouTube)
        self.page().fullScreenRequested.connect(lambda req: req.accept())

class Prawser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prawser - Ultra Fast")
        self.setMinimumSize(1100, 800)

        # Apply a highly professional, modern Dark UI theme
        self.setStyleSheet("""
            QMainWindow { background-color: #0d0d0d; }
            #NavBar { background-color: #1a1a1a; border-bottom: 1px solid #2d2d2d; }
            QLineEdit {
                background-color: #262626; color: #ffffff;
                border: 1px solid #3d3d3d; border-radius: 18px;
                padding: 8px 20px; font-size: 14px;
                selection-background-color: #3b82f6;
            }
            QLineEdit:focus { border: 1px solid #3b82f6; background-color: #1f1f1f; }
            QPushButton {
                background-color: transparent; color: #a3a3a3;
                font-size: 18px; font-weight: bold; border: none;
                border-radius: 18px; min-width: 36px; max-width: 36px; min-height: 36px;
            }
            QPushButton:hover { background-color: #333333; color: #ffffff; }
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                background-color: #1a1a1a; color: #737373;
                padding: 10px 25px; border-top-left-radius: 10px;
                border-top-right-radius: 10px; margin-top: 5px;
                font-size: 13px; min-width: 120px; max-width: 250px;
            }
            QTabBar::tab:selected { background-color: #262626; color: #ffffff; }
            QTabBar::tab:hover:!selected { background-color: #202020; }
            QProgressBar { background-color: transparent; border: none; max-height: 2px; }
            QProgressBar::chunk { background-color: #3b82f6; }
            QMenu { background-color: #1a1a1a; color: white; border: 1px solid #333; }
            QMenu::item:selected { background-color: #3b82f6; }
        """)

        # Main Layout Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Custom Navigation Bar
        navbar_widget = QWidget()
        navbar_widget.setObjectName("NavBar")
        navbar_layout = QHBoxLayout(navbar_widget)
        navbar_layout.setContentsMargins(15, 10, 15, 10)
        navbar_layout.setSpacing(10)

        # Basic Nav Buttons
        self.back_btn = QPushButton("⮜")
        self.back_btn.clicked.connect(self.go_back)
        
        self.forward_btn = QPushButton("⮞")
        self.forward_btn.clicked.connect(self.go_forward)
        
        self.reload_btn = QPushButton("⟳")
        self.reload_btn.clicked.connect(self.reload_page)

        self.home_btn = QPushButton("🏠")
        self.home_btn.clicked.connect(self.go_home)

        # URL Bar
        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText("Search Google or enter a website...")
        self.urlbar.returnPressed.connect(self.navigate)
        self.urlbar.mousePressEvent = lambda _: self.urlbar.selectAll()

        # Add Tab & Menu Buttons
        self.new_tab_btn = QPushButton("＋")
        self.new_tab_btn.clicked.connect(lambda: self.add_tab())
        
        self.menu_btn = QPushButton("⋮")
        self.menu_btn.clicked.connect(self.show_menu)

        # Add elements to Navbar
        navbar_layout.addWidget(self.back_btn)
        navbar_layout.addWidget(self.forward_btn)
        navbar_layout.addWidget(self.reload_btn)
        navbar_layout.addWidget(self.home_btn)
        navbar_layout.addWidget(self.urlbar)
        navbar_layout.addWidget(self.new_tab_btn)
        navbar_layout.addWidget(self.menu_btn)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)

        # Assemble Main Layout
        main_layout.addWidget(navbar_widget)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.tabs)

        # Enable Downloads
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self.handle_download)

        # Keyboard Shortcuts
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(lambda: self.add_tab())
        QShortcut(QKeySequence("Ctrl+W"), self).activated.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        QShortcut(QKeySequence("Ctrl+R"), self).activated.connect(self.reload_page)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.find_in_page)
        QShortcut(QKeySequence("Ctrl+="), self).activated.connect(self.zoom_in)
        QShortcut(QKeySequence("Ctrl+-"), self).activated.connect(self.zoom_out)
        QShortcut(QKeySequence("Ctrl+0"), self).activated.connect(self.zoom_reset)

        # Open default tab
        self.add_tab(QUrl("https://www.google.com"), "New Tab")
        self.showMaximized()

    # --- Core Functions ---
    def add_tab(self, qurl=None, label="Loading..."):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = PrawserTab()
        browser.setUrl(qurl)
        
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

        # Signals
        browser.urlChanged.connect(lambda q, b=browser: self.update_urlbar(q, b))
        browser.loadFinished.connect(lambda _, i=index, b=browser: self.update_title(i, b))
        browser.loadProgress.connect(self.update_progress)

    def close_tab(self, index):
        if self.tabs.count() < 2:
            self.close()
            return
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        widget.deleteLater()

    def get_current_browser(self):
        return self.tabs.currentWidget()

    # --- Navigation & Actions ---
    def go_back(self):
        if self.get_current_browser(): self.get_current_browser().back()

    def go_forward(self):
        if self.get_current_browser(): self.get_current_browser().forward()

    def reload_page(self):
        if self.get_current_browser(): self.get_current_browser().reload()

    def go_home(self):
        if self.get_current_browser(): self.get_current_browser().setUrl(QUrl("https://www.google.com"))

    def navigate(self):
        text = self.urlbar.text().strip()
        if not text: return
        
        if " " in text and "." not in text:
            qurl = QUrl(f"https://www.google.com/search?q={text}")
        elif not text.startswith("http"):
            qurl = QUrl("https://" + text)
        else:
            qurl = QUrl(text)
            
        if self.get_current_browser():
            self.get_current_browser().setUrl(qurl)

    # --- New Advanced Features ---
    def handle_download(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if path:
            download.setPath(path)
            download.accept()

    def show_menu(self):
        menu = QMenu(self)
        
        find_action = QAction("🔍 Find in Page", self)
        find_action.triggered.connect(self.find_in_page)
        menu.addAction(find_action)
        
        zoom_in_action = QAction("➕ Zoom In", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("➖ Zoom Out", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        menu.addAction(zoom_out_action)
        
        zoom_reset_action = QAction("🔄 Reset Zoom", self)
        zoom_reset_action.triggered.connect(self.zoom_reset)
        menu.addAction(zoom_reset_action)
        
        menu.addSeparator()
        
        print_action = QAction("🖨️ Print to PDF", self)
        print_action.triggered.connect(self.print_to_pdf)
        menu.addAction(print_action)
        
        open_default_action = QAction("🌐 Open in System Browser", self)
        open_default_action.triggered.connect(self.open_in_default)
        menu.addAction(open_default_action)

        # Show menu under the button
        menu.exec_(self.menu_btn.mapToGlobal(self.menu_btn.rect().bottomLeft()))

    def find_in_page(self):
        browser = self.get_current_browser()
        if browser:
            text, ok = QInputDialog.getText(self, "Find", "Enter text to find:")
            if ok and text:
                browser.page().findText(text)

    def print_to_pdf(self):
        browser = self.get_current_browser()
        if browser:
            path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
            if path:
                browser.page().printToPdf(path)

    def open_in_default(self):
        browser = self.get_current_browser()
        if browser:
            QDesktopServices.openUrl(browser.url())

    def zoom_in(self):
        b = self.get_current_browser()
        if b: b.setZoomFactor(b.zoomFactor() + 0.1)

    def zoom_out(self):
        b = self.get_current_browser()
        if b: b.setZoomFactor(b.zoomFactor() - 0.1)

    def zoom_reset(self):
        b = self.get_current_browser()
        if b: b.setZoomFactor(1.0)

    # --- UI Update Functions ---
    def tab_changed(self, index):
        browser = self.get_current_browser()
        if browser:
            self.update_urlbar(browser.url(), browser)
            self.progress_bar.setValue(0)

    def update_urlbar(self, q, browser):
        if browser == self.get_current_browser():
            self.urlbar.setText(q.toString())

    def update_title(self, index, browser):
        title = browser.page().title()
        short_title = title[:15] + "..." if len(title) > 15 else title
        
        actual_index = self.tabs.indexOf(browser)
        if actual_index != -1:
            self.tabs.setTabText(actual_index, short_title)
            
        if browser == self.get_current_browser():
            self.setWindowTitle(f"{title} - Prawser")

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress == 100:
            self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = Prawser()
    sys.exit(app.exec_())