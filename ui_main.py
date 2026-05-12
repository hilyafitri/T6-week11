"""
Nama  : Hilya Fitri
NIM   : F1D02310009
Kelas : C

"""

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import QApplication

from api_worker import ApiWorker
from api_service import ApiService


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Post Manager REST API")
        self.resize(1200, 700)

        self.threadpool = QThreadPool()
        self.selected_post_id = None

        self.setup_ui()
        self.load_posts()

    # =========================
    # UI
    # =========================
    def setup_ui(self):

        # =========================
        # STYLE
        # =========================
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fb;
            }

            QWidget {
                color: #1f2937;
                font-size: 13px;
            }

            QLabel {
                color: #374151;
                font-size: 13px;
            }

            QPushButton {
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
            }

            QPushButton:hover {
                opacity: 0.9;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: white;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                selection-background-color: #93c5fd;
            }
                           
            QComboBox {
                background-color: white;
                color: #111827;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                color: #111827;
                border: 1px solid #d1d5db;
                selection-background-color: #bfdbfe;
                selection-color: #111827;
                padding: 5px;
                outline: 0;
                
            }

            QTableWidget {
                background-color: white;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                gridline-color: #e5e7eb;
                alternate-background-color: #f9fafb;
                selection-background-color: #bfdbfe;
                selection-color: #111827;
            }

            QTableWidget::item {
                padding: 6px;
                color: #111827;
            }

            QHeaderView::section {
                background-color: #dbeafe;
                color: #1e3a8a;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }

            QGroupBox {
                background-color: white;
                border: 2px solid #e5e7eb;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: bold;
                color: #4338ca;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }

            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 5px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }

            QMessageBox {
                background-color: white;
            }
            
            QMessageBox QLabel {
                color: #111827;
                font-size: 13px;
            }

            QMessageBox QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 6px;
                padding: 6px 14px;
                min-width: 70px;
                min-height: 28px;
                font-weight: bold;
            }

            QMessageBox QPushButton:hover {
                background-color: #2563eb;
            }
                           
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)

        # =========================
        # HEADER
        # =========================
        title = QLabel("📘 Post Manager REST API")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #1e3a8a;
        """)

        subtitle = QLabel("Aplikasi CRUD REST API menggunakan PySide6 + Threading")
        subtitle.setStyleSheet("""
            color: gray;
            font-size: 13px;
        """)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # =========================
        # STATUS
        # =========================
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            background: #dbeafe;
            color: #1e40af;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        """)

        main_layout.addWidget(self.status_label)

        # =========================
        # BUTTONS
        # =========================
        button_layout = QHBoxLayout()

        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.setStyleSheet("""
            background-color: #3b82f6;
        """)

        self.btn_add = QPushButton("➕ Tambah")
        self.btn_add.setStyleSheet("""
            background-color: #22c55e;
        """)

        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_edit.setStyleSheet("""
            background-color: #f59e0b;
        """)

        self.btn_delete = QPushButton("🗑 Hapus")
        self.btn_delete.setStyleSheet("""
            background-color: #ef4444;
        """)

        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)

        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_edit)
        button_layout.addWidget(self.btn_delete)

        main_layout.addLayout(button_layout)

        content_layout = QHBoxLayout()

        # =========================
        # LEFT PANEL
        # =========================
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        table_title = QLabel("📋 Daftar Posts")
        table_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #4338ca;
        """)

        left_layout.addWidget(table_title)

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Title",
            "Author",
            "Status"
        ])

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 320)
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 150)

        left_layout.addWidget(self.table)

        content_layout.addWidget(left_widget, 2)

        # =========================
        # RIGHT PANEL
        # =========================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }

            QWidget {
                background: transparent;
            }
        """)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(15)

        scroll.setWidget(right_widget)

        right_widget.setStyleSheet("""
            background: transparent;
        """)

        # =========================
        # FORM POST
        # =========================
        form_group = QGroupBox("✏️ Form Post")

        form_layout = QFormLayout()

        self.input_title = QLineEdit()

        self.input_body = QTextEdit()
        self.input_body.setFixedHeight(100)

        self.input_author = QLineEdit()

        self.input_slug = QLineEdit()

        self.input_status = QComboBox()
        self.input_status.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 8px;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                color: #111827;
                border: 1px solid #d1d5db;
                selection-background-color: #bfdbfe;
                selection-color: #111827;
                outline: 0;
            }
        """)

        self.input_status.view().setStyleSheet("""
            background-color: white;
            color: #111827;
            selection-background-color: #bfdbfe;
            selection-color: #111827;
        """)

        self.input_status.addItems([
            "draft",
            "published"
        ])

        form_layout.addRow("Title", self.input_title)
        form_layout.addRow("Body", self.input_body)
        form_layout.addRow("Author", self.input_author)
        form_layout.addRow("Slug", self.input_slug)
        form_layout.addRow("Status", self.input_status)

        form_group.setLayout(form_layout)

        # =========================
        # DETAIL POST
        # =========================
        detail_group = QGroupBox("📄 Detail Post")

        detail_layout = QFormLayout()

        self.detail_title = QLabel("-")
        self.detail_author = QLabel("-")
        self.detail_slug = QLabel("-")
        self.detail_status = QLabel("-")

        self.detail_body = QTextEdit()
        self.detail_body.setReadOnly(True)
        self.detail_body.setFixedHeight(100)

        self.detail_comments = QTextEdit()
        self.detail_comments.setReadOnly(True)
        self.detail_comments.setFixedHeight(100)

        detail_layout.addRow("Title", self.detail_title)
        detail_layout.addRow("Author", self.detail_author)
        detail_layout.addRow("Slug", self.detail_slug)
        detail_layout.addRow("Status", self.detail_status)
        detail_layout.addRow("Body", self.detail_body)
        detail_layout.addRow("Comments", self.detail_comments)

        detail_group.setLayout(detail_layout)

        right_layout.addWidget(detail_group)

        right_layout.addWidget(form_group)

        content_layout.addWidget(scroll, 1)

        main_layout.addLayout(content_layout)

        # =========================
        # SIGNAL
        # =========================
        self.btn_refresh.clicked.connect(self.load_posts)
        self.btn_add.clicked.connect(self.add_post)
        self.btn_edit.clicked.connect(self.edit_post)
        self.btn_delete.clicked.connect(self.delete_post)

        self.table.cellClicked.connect(self.row_selected)

    # =========================
    # STATUS
    # =========================
    def set_loading(self, text):
        self.status_label.setText(text)

    # =========================
    # LOAD POSTS
    # =========================
    def load_posts(self):

        self.set_loading("Loading posts...")

        worker = ApiWorker(ApiService.get_posts)

        worker.signals.finished.connect(
            self.load_posts_success
        )

        worker.signals.error.connect(
            self.show_error
        )

        self.threadpool.start(worker)

    def load_posts_success(self, data):

        posts = data.get("data", data)

        self.table.setRowCount(0)

        for row, post in enumerate(posts):

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(post.get("id")))
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(post.get("title", ""))
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(post.get("author", ""))
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(post.get("status", ""))
            )

        self.status_label.setText(
            f"Berhasil load {len(posts)} posts"
        )

    # =========================
    # SELECT ROW
    # =========================
    def row_selected(self, row):

        self.selected_post_id = self.table.item(
            row,
            0
        ).text()

        self.btn_edit.setEnabled(True)
        self.btn_delete.setEnabled(True)

        self.load_post_detail(self.selected_post_id)

    # =========================
    # DETAIL
    # =========================
    def load_post_detail(self, post_id):

        self.set_loading("Loading detail post...")

        worker = ApiWorker(
            lambda: ApiService.get_post_detail(post_id)
        )

        worker.signals.finished.connect(
            self.load_detail_success
        )

        worker.signals.error.connect(
            self.show_error
        )

        self.threadpool.start(worker)

    def load_detail_success(self, data):

        post = data.get("data", data)

        self.detail_title.setText(
            post.get("title", "-")
        )

        self.detail_author.setText(
            post.get("author", "-")
        )

        self.detail_slug.setText(
            post.get("slug", "-")
        )

        self.detail_status.setText(
            post.get("status", "-")
        )

        self.detail_body.setPlainText(
            post.get("body", "")
        )

        # COMMENTS
        comments = post.get("comments", [])

        comments_text = ""

        if comments:

            for comment in comments:

                comments_text += (
                    f"ID: {comment.get('id')}\n"
                    f"Name: {comment.get('name')}\n"
                    f"Comment: {comment.get('body')}\n"
                    "-----------------------\n"
                )

        else:
            comments_text = "Tidak ada komentar"

        self.detail_comments.setPlainText(
            comments_text
        )

        # FILL FORM
        self.input_title.setText(
            post.get("title", "")
        )

        self.input_body.setPlainText(
            post.get("body", "")
        )

        self.input_author.setText(
            post.get("author", "")
        )

        self.input_slug.setText(
            post.get("slug", "")
        )

        index = self.input_status.findText(
            post.get("status", "draft")
        )

        self.input_status.setCurrentIndex(index)

        self.status_label.setText(
            "Detail post berhasil dimuat"
        )

    # =========================
    # FORM DATA
    # =========================
    def get_form_data(self):

        return {
            "title": self.input_title.text(),
            "body": self.input_body.toPlainText(),
            "author": self.input_author.text(),
            "slug": self.input_slug.text(),
            "status": self.input_status.currentText(),
        }

    # =========================
    # VALIDATION
    # =========================
    def validate_form(self):

        if not self.input_title.text():
            QMessageBox.warning(
                self,
                "Warning",
                "Title wajib diisi"
            )
            return False

        if not self.input_body.toPlainText():
            QMessageBox.warning(
                self,
                "Warning",
                "Body wajib diisi"
            )
            return False

        if not self.input_author.text():
            QMessageBox.warning(
                self,
                "Warning",
                "Author wajib diisi"
            )
            return False

        if not self.input_slug.text():
            QMessageBox.warning(
                self,
                "Warning",
                "Slug wajib diisi"
            )
            return False

        return True

    # =========================
    # ADD POST
    # =========================
    def add_post(self):

        if not self.validate_form():
            return

        data = self.get_form_data()

        self.set_loading("Menambahkan post...")

        worker = ApiWorker(
            lambda: ApiService.create_post(data)
        )

        worker.signals.finished.connect(
            self.add_success
        )

        worker.signals.error.connect(
            self.show_error
        )

        self.threadpool.start(worker)

    def add_success(self, data):

        post = data.get("data", data)

        QMessageBox.information(
            self,
            "Sukses",
            f"Post berhasil ditambahkan\n"
            f"ID: {post.get('id')}"
        )

        self.load_posts()

    # =========================
    # EDIT POST
    # =========================
    def edit_post(self):

        if not self.selected_post_id:
            return

        if not self.validate_form():
            return

        data = self.get_form_data()

        self.set_loading("Mengupdate post...")

        worker = ApiWorker(
            lambda: ApiService.update_post(
                self.selected_post_id,
                data
            )
        )

        worker.signals.finished.connect(
            self.edit_success
        )

        worker.signals.error.connect(
            self.show_error
        )

        self.threadpool.start(worker)

    def edit_success(self, data):

        QMessageBox.information(
            self,
            "Sukses",
            "Post berhasil diupdate"
        )

        self.load_posts()

    # =========================
    # DELETE
    # =========================
    def delete_post(self):

        if not self.selected_post_id:
            return

        msg = QMessageBox(self)

        msg.setWindowTitle("Konfirmasi")

        msg.setText(
            "Yakin ingin menghapus post?\n"
            "Semua comments juga ikut terhapus."
        )

        msg.setIcon(QMessageBox.Question)

        # BUTTON
        btn_yes = msg.addButton("Ya", QMessageBox.YesRole)
        btn_no = msg.addButton("Tidak", QMessageBox.NoRole)

        btn_yes.setStyleSheet("""
            background-color: #22c55e;
            color: white;
            padding: 6px 15px;
            border-radius: 6px;
            font-weight: bold;
        """)

        btn_no.setStyleSheet("""
            background-color: #ef4444;
            color: white;
            padding: 6px 15px;
            border-radius: 6px;
            font-weight: bold;
        """)

        msg.exec()

        if msg.clickedButton() != btn_yes:
            return

        self.set_loading("Menghapus post...")

        worker = ApiWorker(
            lambda: ApiService.delete_post(
                self.selected_post_id
            )
        )

        worker.signals.finished.connect(
            self.delete_success
        )

        worker.signals.error.connect(
            self.show_error
        )

        self.threadpool.start(worker)

    # =========================
    # CLEAR FORM & DETAIL
    # =========================
    def clear_fields(self):

        self.detail_title.setText("-")
        self.detail_author.setText("-")
        self.detail_slug.setText("-")
        self.detail_status.setText("-")

        self.detail_body.clear()
        self.detail_comments.clear()

        self.input_title.clear()
        self.input_body.clear()
        self.input_author.clear()
        self.input_slug.clear()

        self.input_status.setCurrentIndex(0)
    # =========================
    # ERROR
    # =========================
    def show_error(self, message):

        if "422" in message:

            QMessageBox.warning(
                self,
                "Validasi Gagal",
                "Slug sudah digunakan.\n"
                "Gunakan slug lain."
            )

        else:

            QMessageBox.critical(
                self,
                "Error",
                message
            )

        self.status_label.setText("Terjadi error")