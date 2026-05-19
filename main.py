#!/usr/bin/env python3
"""
Email Scanner - A professional PySide6 desktop application
Scans and analyzes emails with AI-powered prioritization
"""

import sys
import os
import json
import imaplib
import email
import email.header
import email.utils
import threading
import re
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from typing import Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QSpinBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QSplitter, QTextEdit,
    QProgressBar, QStackedWidget, QScrollArea, QMessageBox, QDialog,
    QFormLayout, QCheckBox, QSlider, QStatusBar, QToolBar, QSizePolicy,
    QAbstractItemView, QMenu, QGraphicsDropShadowEffect, QTabWidget
)
from PySide6.QtCore import (
    Qt, QThread, QObject, Signal, QTimer, QPropertyAnimation,
    QEasingCurve, QRect, QSize, QPoint, QRunnable, QThreadPool,
    Slot, Property
)
from PySide6.QtGui import (
    QFont, QColor, QPalette, QLinearGradient, QBrush, QPainter,
    QPixmap, QIcon, QPen, QFontDatabase, QCursor, QAction,
    QKeySequence, QTextCharFormat, QTextCursor
)


# ─── COLOR PALETTE ──────────────────────────────────────────────────────────
COLORS = {
    "bg_primary":      "#0D1117",
    "bg_secondary":    "#161B22",
    "bg_card":         "#1C2128",
    "bg_hover":        "#21262D",
    "bg_input":        "#0D1117",
    "accent_blue":     "#388BFD",
    "accent_cyan":     "#39D5FF",
    "accent_green":    "#3FB950",
    "accent_yellow":   "#D29922",
    "accent_red":      "#F85149",
    "accent_purple":   "#BC8CFF",
    "accent_orange":   "#F0883E",
    "text_primary":    "#E6EDF3",
    "text_secondary":  "#8B949E",
    "text_muted":      "#484F58",
    "border":          "#30363D",
    "border_focus":    "#388BFD",
    "critical":        "#F85149",
    "high":            "#F0883E",
    "medium":          "#D29922",
    "low":             "#3FB950",
    "info":            "#388BFD",
}


STYLESHEET = f"""
/* ── Global ── */
QMainWindow, QWidget {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['text_primary']};
    font-family: "Segoe UI", "SF Pro Display", sans-serif;
    font-size: 13px;
}}

QScrollBar:vertical {{
    background: {COLORS['bg_secondary']};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border']};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS['text_secondary']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

QScrollBar:horizontal {{
    background: {COLORS['bg_secondary']};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: {COLORS['border']};
    border-radius: 4px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

/* ── Tooltip ── */
QToolTip {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}}

/* ── LineEdit ── */
QLineEdit {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    color: {COLORS['text_primary']};
    font-size: 13px;
    selection-background-color: {COLORS['accent_blue']};
}}
QLineEdit:focus {{
    border-color: {COLORS['border_focus']};
    background-color: {COLORS['bg_secondary']};
}}
QLineEdit:hover {{
    border-color: {COLORS['text_muted']};
}}
QLineEdit[echoMode="2"] {{
    lineedit-password-character: 9679;
}}

/* ── ComboBox ── */
QComboBox {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    color: {COLORS['text_primary']};
    font-size: 13px;
    min-width: 140px;
}}
QComboBox:focus, QComboBox:on {{
    border-color: {COLORS['border_focus']};
}}
QComboBox::drop-down {{
    border: none;
    width: 30px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {COLORS['text_secondary']};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['accent_blue']}33;
    selection-color: {COLORS['accent_blue']};
    outline: none;
    padding: 4px;
}}
QComboBox QAbstractItemView::item {{
    padding: 8px 12px;
    border-radius: 6px;
    min-height: 32px;
}}

/* ── SpinBox ── */
QSpinBox {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    color: {COLORS['text_primary']};
    font-size: 13px;
}}
QSpinBox:focus {{ border-color: {COLORS['border_focus']}; }}
QSpinBox::up-button, QSpinBox::down-button {{
    background: {COLORS['bg_card']};
    border: none;
    width: 22px;
    border-radius: 4px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background: {COLORS['bg_hover']};
}}

/* ── QPushButton base ── */
QPushButton {{
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
    border: none;
    cursor: pointer;
}}
QPushButton:disabled {{
    opacity: 0.4;
}}

/* ── Table ── */
QTableWidget {{
    background-color: transparent;
    border: none;
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['accent_blue']}22;
    selection-color: {COLORS['text_primary']};
    border-radius: 10px;
    outline: none;
}}
QTableWidget::item {{
    padding: 10px 14px;
    border-bottom: 1px solid {COLORS['border']};
}}
QTableWidget::item:selected {{
    background-color: {COLORS['accent_blue']}22;
    color: {COLORS['text_primary']};
}}
QTableWidget::item:hover {{
    background-color: {COLORS['bg_hover']};
}}
QHeaderView::section {{
    background-color: {COLORS['bg_secondary']};
    color: {COLORS['text_secondary']};
    padding: 12px 14px;
    border: none;
    border-bottom: 2px solid {COLORS['border']};
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
QHeaderView::section:first {{
    border-top-left-radius: 10px;
}}
QHeaderView::section:last {{
    border-top-right-radius: 10px;
}}

/* ── ProgressBar ── */
QProgressBar {{
    background-color: {COLORS['bg_secondary']};
    border: none;
    border-radius: 6px;
    height: 8px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['accent_blue']}, stop:1 {COLORS['accent_cyan']});
    border-radius: 6px;
}}

/* ── TextEdit ── */
QTextEdit {{
    background-color: {COLORS['bg_secondary']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    color: {COLORS['text_primary']};
    padding: 14px;
    font-size: 13px;
    line-height: 1.6;
    selection-background-color: {COLORS['accent_blue']}44;
}}

/* ── Tab Widget ── */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    background-color: {COLORS['bg_secondary']};
    top: -1px;
}}
QTabBar::tab {{
    background: transparent;
    color: {COLORS['text_secondary']};
    padding: 10px 20px;
    border: none;
    font-size: 13px;
    font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-right: 4px;
}}
QTabBar::tab:selected {{
    color: {COLORS['accent_blue']};
    border-bottom: 2px solid {COLORS['accent_blue']};
}}
QTabBar::tab:hover:!selected {{
    color: {COLORS['text_primary']};
}}

/* ── Splitter ── */
QSplitter::handle {{
    background-color: {COLORS['border']};
    width: 2px;
}}
QSplitter::handle:hover {{
    background-color: {COLORS['accent_blue']};
}}

/* ── Menu ── */
QMenu {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 6px;
    color: {COLORS['text_primary']};
}}
QMenu::item {{
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 13px;
}}
QMenu::item:selected {{
    background-color: {COLORS['bg_hover']};
}}
QMenu::separator {{
    height: 1px;
    background: {COLORS['border']};
    margin: 4px 8px;
}}

/* ── CheckBox ── */
QCheckBox {{
    color: {COLORS['text_primary']};
    spacing: 8px;
    font-size: 13px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 2px solid {COLORS['border']};
    background: {COLORS['bg_input']};
}}
QCheckBox::indicator:checked {{
    background: {COLORS['accent_blue']};
    border-color: {COLORS['accent_blue']};
}}

/* ── StatusBar ── */
QStatusBar {{
    background-color: {COLORS['bg_secondary']};
    border-top: 1px solid {COLORS['border']};
    color: {COLORS['text_secondary']};
    font-size: 12px;
    padding: 4px 12px;
}}
"""


# ─── IMAP PROVIDERS ─────────────────────────────────────────────────────────
IMAP_PROVIDERS = {
    "Gmail":        ("imap.gmail.com",   993),
    "Outlook/Hotmail": ("imap-mail.outlook.com", 993),
    "Yahoo Mail":   ("imap.mail.yahoo.com", 993),
    "iCloud":       ("imap.mail.me.com", 993),
    "Zoho Mail":    ("imap.zoho.com",    993),
    "ProtonMail (Bridge)": ("127.0.0.1", 1143),
    "Custom IMAP":  ("",                 993),
}

PRIORITY_KEYWORDS = {
    "critical": ["urgent", "asap", "immediately", "critical", "emergency", "alert",
                 "deadline", "overdue", "action required", "final notice", "last chance"],
    "high":     ["important", "priority", "attention", "follow up", "reminder",
                 "meeting", "interview", "offer", "invoice", "payment", "security",
                 "verify", "account", "password", "reset", "confirm"],
    "medium":   ["update", "review", "request", "question", "feedback", "scheduled",
                 "subscription", "report", "news", "weekly", "monthly"],
    "low":      ["newsletter", "promo", "sale", "discount", "offer", "unsubscribe",
                 "marketing", "notification", "social", "digest"],
}

PRIORITY_COLORS = {
    "critical": COLORS["critical"],
    "high":     COLORS["high"],
    "medium":   COLORS["medium"],
    "low":      COLORS["low"],
    "unknown":  COLORS["info"],
}


# ─── WORKER SIGNALS ──────────────────────────────────────────────────────────
class ScannerSignals(QObject):
    progress      = Signal(int, str)      # percent, message
    email_found   = Signal(dict)          # email data dict
    finished      = Signal(list)          # all emails list
    error         = Signal(str)
    stats_update  = Signal(dict)


# ─── EMAIL SCANNER WORKER ────────────────────────────────────────────────────
class EmailScannerWorker(QThread):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.signals = ScannerSignals()
        self._stop = False

    def stop(self):
        self._stop = True

    def decode_header_value(self, value):
        if not value:
            return ""
        parts = email.header.decode_header(value)
        decoded = []
        for part, enc in parts:
            if isinstance(part, bytes):
                try:
                    decoded.append(part.decode(enc or "utf-8", errors="replace"))
                except Exception:
                    decoded.append(part.decode("latin-1", errors="replace"))
            else:
                decoded.append(str(part))
        return " ".join(decoded).strip()

    def get_body(self, msg):
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp  = str(part.get("Content-Disposition", ""))
                if ctype == "text/plain" and "attachment" not in disp:
                    try:
                        charset = part.get_content_charset() or "utf-8"
                        body = part.get_payload(decode=True).decode(charset, errors="replace")
                        break
                    except Exception:
                        pass
        else:
            try:
                charset = msg.get_content_charset() or "utf-8"
                body = msg.get_payload(decode=True).decode(charset, errors="replace")
            except Exception:
                body = ""
        return body[:2000]

    def assign_priority(self, subject, body, sender):
        text = (subject + " " + body[:500] + " " + sender).lower()
        for level in ["critical", "high", "medium", "low"]:
            for kw in PRIORITY_KEYWORDS[level]:
                if kw in text:
                    return level
        return "unknown"

    def compute_score(self, priority, date_str, has_attachment):
        score = {"critical": 100, "high": 75, "medium": 50, "low": 25, "unknown": 35}[priority]
        try:
            dt = email.utils.parsedate_to_datetime(date_str)
            age_hours = (datetime.now(dt.tzinfo) - dt).total_seconds() / 3600
            recency = max(0, 50 - age_hours * 0.1)
            score += recency
        except Exception:
            pass
        if has_attachment:
            score += 10
        return round(score, 1)

    def run(self):
        try:
            cfg = self.config
            imap_host = cfg["imap_host"]
            imap_port = int(cfg["imap_port"])
            username  = cfg["username"]
            password  = cfg["password"]
            days      = int(cfg["days"])
            folder    = cfg.get("folder", "INBOX")

            self.signals.progress.emit(5, "Connecting to mail server…")
            mail = imaplib.IMAP4_SSL(imap_host, imap_port)

            self.signals.progress.emit(15, "Authenticating…")
            mail.login(username, password)

            self.signals.progress.emit(25, f"Opening folder: {folder}")
            mail.select(folder)

            since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
            self.signals.progress.emit(30, f"Searching emails since {since_date}…")

            _, data = mail.search(None, f'(SINCE "{since_date}")')
            msg_ids = data[0].split()
            total   = len(msg_ids)

            if total == 0:
                self.signals.finished.emit([])
                mail.logout()
                return

            self.signals.progress.emit(35, f"Found {total} emails. Analyzing…")

            results = []
            for i, mid in enumerate(reversed(msg_ids)):
                if self._stop:
                    break

                pct = 35 + int((i / total) * 60)
                self.signals.progress.emit(pct, f"Processing email {i+1} of {total}…")

                try:
                    _, msg_data = mail.fetch(mid, "(RFC822)")
                    raw = msg_data[0][1]
                    msg = email.message_from_bytes(raw)

                    subject     = self.decode_header_value(msg.get("Subject", "(No Subject)"))
                    sender      = self.decode_header_value(msg.get("From", ""))
                    date_str    = msg.get("Date", "")
                    msg_id      = msg.get("Message-ID", str(mid))
                    has_attach  = any(
                        part.get_filename() for part in msg.walk() if part.get_filename()
                    )
                    body        = self.get_body(msg)
                    priority    = self.assign_priority(subject, body, sender)
                    score       = self.compute_score(priority, date_str, has_attach)

                    try:
                        parsed_date = email.utils.parsedate_to_datetime(date_str)
                        display_date = parsed_date.strftime("%b %d, %Y  %H:%M")
                    except Exception:
                        display_date = date_str[:20] if date_str else "Unknown"

                    entry = {
                        "id":          str(mid.decode()),
                        "subject":     subject,
                        "sender":      sender,
                        "date":        display_date,
                        "raw_date":    date_str,
                        "priority":    priority,
                        "score":       score,
                        "has_attach":  has_attach,
                        "body":        body,
                        "read":        False,
                    }
                    results.append(entry)
                    self.signals.email_found.emit(entry)

                except Exception as e:
                    pass  # skip broken messages

            self.signals.progress.emit(98, "Sorting by priority…")
            results.sort(key=lambda x: x["score"], reverse=True)

            mail.logout()
            self.signals.progress.emit(100, f"Done! Scanned {len(results)} emails.")
            self.signals.finished.emit(results)

        except imaplib.IMAP4.error as e:
            self.signals.error.emit(f"IMAP Error: {str(e)}\n\nCheck credentials or enable IMAP access in your email settings.")
        except ConnectionRefusedError:
            self.signals.error.emit("Connection refused. Check the IMAP server address and port.")
        except Exception as e:
            self.signals.error.emit(f"Unexpected error: {str(e)}")


# ─── CUSTOM WIDGETS ──────────────────────────────────────────────────────────
class GlowButton(QPushButton):
    """Animated button with glow effect."""
    def __init__(self, text, color=COLORS["accent_blue"], parent=None):
        super().__init__(text, parent)
        self._color = color
        self._base_style = f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {color}CC);
                color: white;
                border-radius: 9px;
                padding: 11px 26px;
                font-size: 13px;
                font-weight: 700;
                border: none;
                letter-spacing: 0.3px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}EE, stop:1 {color});
            }}
            QPushButton:pressed {{
                background: {color}AA;
            }}
            QPushButton:disabled {{
                background: {COLORS['bg_card']};
                color: {COLORS['text_muted']};
            }}
        """
        self.setStyleSheet(self._base_style)
        self.setCursor(QCursor(Qt.PointingHandCursor))


class OutlineButton(QPushButton):
    def __init__(self, text, color=COLORS["accent_blue"], parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {color};
                border: 1.5px solid {color};
                border-radius: 9px;
                padding: 10px 22px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {color}18;
            }}
            QPushButton:pressed {{
                background: {color}30;
            }}
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))


class StatCard(QFrame):
    def __init__(self, title, value, color, icon="", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 14px;
                padding: 6px;
            }}
            QFrame#statCard:hover {{
                border-color: {color}66;
                background-color: {COLORS['bg_hover']};
            }}
        """)
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(4)

        top = QHBoxLayout()
        lbl_title = QLabel(f"{icon}  {title}" if icon else title)
        lbl_title.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 500; background: transparent; border: none;")
        top.addWidget(lbl_title)
        top.addStretch()
        layout.addLayout(top)

        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: 800; background: transparent; border: none;")
        layout.addWidget(self.value_label)

        bar = QFrame()
        bar.setFixedHeight(3)
        bar.setStyleSheet(f"background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 {color}, stop:1 {color}44); border-radius: 2px;")
        layout.addWidget(bar)

    def update_value(self, v):
        self.value_label.setText(str(v))


class PriorityBadge(QLabel):
    def __init__(self, priority, parent=None):
        super().__init__(parent)
        color  = PRIORITY_COLORS.get(priority, COLORS["info"])
        labels = {"critical": "⚡ CRITICAL", "high": "▲ HIGH",
                  "medium": "● MEDIUM", "low": "▼ LOW", "unknown": "○ NORMAL"}
        self.setText(labels.get(priority, priority.upper()))
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color}22;
                color: {color};
                border: 1px solid {color}55;
                border-radius: 6px;
                padding: 3px 10px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}
        """)
        self.setAlignment(Qt.AlignCenter)


class SectionHeader(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 0 2px;
        """)


class Divider(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFixedHeight(1)
        self.setStyleSheet(f"background-color: {COLORS['border']}; border: none;")


# ─── LOGIN / CONFIG PANEL ────────────────────────────────────────────────────
class ConfigPanel(QWidget):
    scan_requested = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Left decorative panel
        left = QFrame()
        left.setFixedWidth(380)
        left.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['bg_secondary']}, stop:1 #111827);
                border-right: 1px solid {COLORS['border']};
            }}
        """)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(40, 60, 40, 40)
        left_layout.setSpacing(20)

        # Logo / branding
        logo_lbl = QLabel("📧")
        logo_lbl.setStyleSheet("font-size: 56px; background: transparent; border: none;")
        logo_lbl.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(logo_lbl)

        app_name = QLabel("Email Scanner")
        app_name.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: transparent;
            border: none;
        """)
        app_name.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(app_name)

        tagline = QLabel("Intelligent inbox analysis\nwith AI-powered prioritization")
        tagline.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; line-height: 1.6; background: transparent; border: none;")
        tagline.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(tagline)

        left_layout.addSpacing(30)

        features = [
            ("🔍", "Deep Scan", "Analyzes subject, sender & content"),
            ("⚡", "Smart Priority", "5-level intelligent prioritization"),
            ("📊", "Live Stats", "Real-time analytics dashboard"),
            ("🔒", "Secure", "Local processing, no data stored"),
        ]
        for icon, title, desc in features:
            feat = QFrame()
            feat.setStyleSheet(f"""
                QFrame {{
                    background: {COLORS['bg_card']}88;
                    border: 1px solid {COLORS['border']};
                    border-radius: 10px;
                    padding: 2px;
                }}
            """)
            fl = QHBoxLayout(feat)
            fl.setContentsMargins(14, 10, 14, 10)
            fl.setSpacing(12)

            ico = QLabel(icon)
            ico.setStyleSheet("font-size: 22px; background: transparent; border: none;")
            ico.setFixedWidth(34)
            fl.addWidget(ico)

            txt = QVBoxLayout()
            t1 = QLabel(title)
            t1.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px; font-weight: 600; background: transparent; border: none;")
            t2 = QLabel(desc)
            t2.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px; background: transparent; border: none;")
            txt.addWidget(t1)
            txt.addWidget(t2)
            fl.addLayout(txt)
            left_layout.addWidget(feat)

        left_layout.addStretch()

        version = QLabel("v1.0.0  •  Built with PySide6")
        version.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; background: transparent; border: none;")
        version.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(version)

        root.addWidget(left)

        # Right form panel
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(QFrame.NoFrame)
        right_scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        right = QWidget()
        right.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setSpacing(0)

        title = QLabel("Connect Your Mailbox")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 24px; font-weight: 800; letter-spacing: -0.5px; background: transparent; border: none;")
        right_layout.addWidget(title)

        subtitle = QLabel("Enter your email credentials to start scanning")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; margin-top: 4px; background: transparent; border: none;")
        right_layout.addWidget(subtitle)

        right_layout.addSpacing(32)

        # Provider
        right_layout.addWidget(SectionHeader("EMAIL PROVIDER"))
        right_layout.addSpacing(8)
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(list(IMAP_PROVIDERS.keys()))
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)
        right_layout.addWidget(self.provider_combo)

        right_layout.addSpacing(20)

        # Custom host (hidden by default)
        self.custom_host_widget = QWidget()
        self.custom_host_widget.setStyleSheet("background: transparent;")
        ch_layout = QVBoxLayout(self.custom_host_widget)
        ch_layout.setContentsMargins(0, 0, 0, 0)
        ch_layout.setSpacing(8)
        ch_layout.addWidget(SectionHeader("IMAP SERVER"))
        host_row = QHBoxLayout()
        self.host_edit = QLineEdit()
        self.host_edit.setPlaceholderText("imap.example.com")
        self.port_edit = QSpinBox()
        self.port_edit.setRange(1, 65535)
        self.port_edit.setValue(993)
        self.port_edit.setFixedWidth(100)
        host_row.addWidget(self.host_edit, 3)
        host_row.addWidget(QLabel("Port:"), 0)
        host_row.addWidget(self.port_edit, 1)
        ch_layout.addLayout(host_row)
        self.custom_host_widget.hide()
        right_layout.addWidget(self.custom_host_widget)

        # Email
        right_layout.addWidget(SectionHeader("EMAIL ADDRESS"))
        right_layout.addSpacing(8)
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("your@email.com")
        right_layout.addWidget(self.email_edit)

        right_layout.addSpacing(20)

        # Password
        right_layout.addWidget(SectionHeader("PASSWORD / APP PASSWORD"))
        right_layout.addSpacing(8)
        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("••••••••••••")
        self.pass_edit.setEchoMode(QLineEdit.Password)
        right_layout.addWidget(self.pass_edit)

        hint = QLabel("💡 Gmail/Yahoo users: Use App Password (not your regular password)")
        hint.setStyleSheet(f"color: {COLORS['accent_yellow']}; font-size: 11px; margin-top: 6px; background: transparent; border: none;")
        hint.setWordWrap(True)
        right_layout.addWidget(hint)

        right_layout.addSpacing(20)

        # Scan settings row
        scan_row = QHBoxLayout()
        scan_row.setSpacing(16)

        col1 = QVBoxLayout()
        col1.addWidget(SectionHeader("SCAN PERIOD"))
        col1.addSpacing(8)
        self.days_spin = QSpinBox()
        self.days_spin.setRange(1, 365)
        self.days_spin.setValue(7)
        self.days_spin.setSuffix("  days")
        col1.addWidget(self.days_spin)
        scan_row.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(SectionHeader("FOLDER"))
        col2.addSpacing(8)
        self.folder_combo = QComboBox()
        self.folder_combo.addItems(["INBOX", "Sent", "All Mail", "Spam", "[Gmail]/All Mail"])
        col2.addWidget(self.folder_combo)
        scan_row.addLayout(col2)

        right_layout.addLayout(scan_row)
        right_layout.addSpacing(32)

        # Scan button
        self.scan_btn = GlowButton("  🔍  Start Scanning", COLORS["accent_blue"])
        self.scan_btn.setMinimumHeight(52)
        self.scan_btn.clicked.connect(self._on_scan)
        right_layout.addWidget(self.scan_btn)

        right_layout.addSpacing(16)
        demo_btn = OutlineButton("  ⚡  Load Demo Data", COLORS["accent_purple"])
        demo_btn.setMinimumHeight(44)
        demo_btn.clicked.connect(self._load_demo)
        right_layout.addWidget(demo_btn)

        right_layout.addStretch()

        right_scroll.setWidget(right)
        root.addWidget(right_scroll, 1)

    def _on_provider_changed(self, provider):
        self.custom_host_widget.setVisible(provider == "Custom IMAP")

    def _on_scan(self):
        provider = self.provider_combo.currentText()
        email_val = self.email_edit.text().strip()
        password  = self.pass_edit.text()

        if not email_val or not password:
            QMessageBox.warning(self, "Missing Fields", "Please enter your email address and password.")
            return

        if provider == "Custom IMAP":
            host = self.host_edit.text().strip()
            port = self.port_edit.value()
            if not host:
                QMessageBox.warning(self, "Missing Host", "Please enter the IMAP server address.")
                return
        else:
            host, port = IMAP_PROVIDERS[provider]

        cfg = {
            "imap_host": host,
            "imap_port": port,
            "username":  email_val,
            "password":  password,
            "days":      self.days_spin.value(),
            "folder":    self.folder_combo.currentText(),
        }
        self.scan_requested.emit(cfg)

    def _load_demo(self):
        self.scan_requested.emit({"demo": True, "days": 7})


# ─── SCANNING PROGRESS PANEL ─────────────────────────────────────────────────
class ScanningPanel(QWidget):
    cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 60, 80, 60)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignCenter)

        self.icon_lbl = QLabel("📡")
        self.icon_lbl.setStyleSheet("font-size: 64px; background: transparent; border: none;")
        self.icon_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_lbl)

        self.title_lbl = QLabel("Scanning Your Mailbox")
        self.title_lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 24px; font-weight: 800; background: transparent; border: none;")
        self.title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_lbl)

        self.status_lbl = QLabel("Connecting…")
        self.status_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; background: transparent; border: none;")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_lbl)

        layout.addSpacing(20)

        self.progress = QProgressBar()
        self.progress.setMinimumWidth(500)
        self.progress.setFixedHeight(10)
        self.progress.setRange(0, 100)
        layout.addWidget(self.progress, 0, Qt.AlignCenter)

        self.pct_lbl = QLabel("0%")
        self.pct_lbl.setStyleSheet(f"color: {COLORS['accent_blue']}; font-size: 18px; font-weight: 700; background: transparent; border: none;")
        self.pct_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pct_lbl)

        layout.addSpacing(16)
        self.found_lbl = QLabel("Emails found: 0")
        self.found_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px; background: transparent; border: none;")
        self.found_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.found_lbl)

        layout.addSpacing(32)
        cancel_btn = OutlineButton("Cancel Scan", COLORS["accent_red"])
        cancel_btn.setFixedWidth(200)
        cancel_btn.clicked.connect(self.cancelled.emit)
        layout.addWidget(cancel_btn, 0, Qt.AlignCenter)

        layout.addStretch()

    def update_progress(self, pct, msg):
        self.progress.setValue(pct)
        self.pct_lbl.setText(f"{pct}%")
        self.status_lbl.setText(msg)

    def update_found(self, n):
        self.found_lbl.setText(f"Emails found: {n}")


# ─── EMAIL DETAIL PANEL ───────────────────────────────────────────────────────
class EmailDetailPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background: {COLORS['bg_secondary']}; border-left: 1px solid {COLORS['border']};")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.header = QFrame()
        self.header.setStyleSheet(f"background: {COLORS['bg_card']}; border-bottom: 1px solid {COLORS['border']};")
        h_layout = QVBoxLayout(self.header)
        h_layout.setContentsMargins(24, 20, 24, 20)
        h_layout.setSpacing(8)

        self.subject_lbl = QLabel("Select an email to preview")
        self.subject_lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 16px; font-weight: 700; background: transparent; border: none;")
        self.subject_lbl.setWordWrap(True)
        h_layout.addWidget(self.subject_lbl)

        meta_row = QHBoxLayout()
        self.sender_lbl  = QLabel("")
        self.date_lbl    = QLabel("")
        self.priority_badge = QLabel("")

        for lbl in [self.sender_lbl, self.date_lbl]:
            lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; background: transparent; border: none;")

        meta_row.addWidget(self.sender_lbl)
        meta_row.addWidget(QLabel("·"))
        meta_row.addWidget(self.date_lbl)
        meta_row.addStretch()
        meta_row.addWidget(self.priority_badge)
        h_layout.addLayout(meta_row)

        layout.addWidget(self.header)

        # Body
        self.body_edit = QTextEdit()
        self.body_edit.setReadOnly(True)
        self.body_edit.setStyleSheet(f"""
            QTextEdit {{
                background: {COLORS['bg_secondary']};
                border: none;
                color: {COLORS['text_primary']};
                padding: 24px;
                font-size: 13px;
                line-height: 1.8;
            }}
        """)
        layout.addWidget(self.body_edit, 1)

    def show_email(self, data: dict):
        self.subject_lbl.setText(data.get("subject", ""))
        self.sender_lbl.setText(data.get("sender", ""))
        self.date_lbl.setText(data.get("date", ""))

        priority = data.get("priority", "unknown")
        color    = PRIORITY_COLORS.get(priority, COLORS["info"])
        labels   = {"critical": "⚡ CRITICAL", "high": "▲ HIGH",
                    "medium": "● MEDIUM", "low": "▼ LOW", "unknown": "○ NORMAL"}
        self.priority_badge.setText(labels.get(priority, ""))
        self.priority_badge.setStyleSheet(f"""
            QLabel {{
                background: {color}22;
                color: {color};
                border: 1px solid {color}55;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}
        """)

        body = data.get("body", "")
        if not body.strip():
            body = "(No content to preview)"
        self.body_edit.setPlainText(body)


# ─── MAIN RESULTS DASHBOARD ──────────────────────────────────────────────────
class ResultsDashboard(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_emails = []
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top bar ──
        topbar = QFrame()
        topbar.setFixedHeight(64)
        topbar.setStyleSheet(f"background: {COLORS['bg_secondary']}; border-bottom: 1px solid {COLORS['border']};")
        tb_layout = QHBoxLayout(topbar)
        tb_layout.setContentsMargins(20, 0, 20, 0)
        tb_layout.setSpacing(16)

        back_btn = OutlineButton("← Back", COLORS["text_secondary"])
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.back_requested.emit)
        tb_layout.addWidget(back_btn)

        title = QLabel("📧  Email Scanner  —  Results")
        title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 16px; font-weight: 700; background: transparent; border: none;")
        tb_layout.addWidget(title)

        tb_layout.addStretch()

        # Search
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔍  Search emails…")
        self.search_edit.setFixedWidth(280)
        self.search_edit.textChanged.connect(self._filter_table)
        tb_layout.addWidget(self.search_edit)

        # Filter
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Priorities", "Critical", "High", "Medium", "Low", "Normal"])
        self.filter_combo.setFixedWidth(160)
        self.filter_combo.currentTextChanged.connect(self._filter_table)
        tb_layout.addWidget(self.filter_combo)

        self.export_btn = OutlineButton("⬇ Export CSV", COLORS["accent_green"])
        self.export_btn.setFixedWidth(140)
        self.export_btn.clicked.connect(self._export_csv)
        tb_layout.addWidget(self.export_btn)

        root.addWidget(topbar)

        # ── Stats row ──
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"background: {COLORS['bg_primary']}; border-bottom: 1px solid {COLORS['border']};")
        sf_layout = QHBoxLayout(stats_frame)
        sf_layout.setContentsMargins(20, 16, 20, 16)
        sf_layout.setSpacing(14)

        self.stat_total    = StatCard("Total Emails", "0", COLORS["accent_blue"],    "📨")
        self.stat_critical = StatCard("Critical",     "0", COLORS["critical"],       "⚡")
        self.stat_high     = StatCard("High Priority","0", COLORS["high"],           "▲")
        self.stat_medium   = StatCard("Medium",       "0", COLORS["medium"],         "●")
        self.stat_low      = StatCard("Low / Normal", "0", COLORS["low"],            "▼")
        self.stat_attach   = StatCard("With Attachments", "0", COLORS["accent_purple"], "📎")

        for s in [self.stat_total, self.stat_critical, self.stat_high,
                  self.stat_medium, self.stat_low, self.stat_attach]:
            sf_layout.addWidget(s)

        root.addWidget(stats_frame)

        # ── Main splitter ──
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        # Email table side
        table_widget = QWidget()
        table_widget.setStyleSheet(f"background: {COLORS['bg_primary']};")
        tw_layout = QVBoxLayout(table_widget)
        tw_layout.setContentsMargins(20, 16, 0, 20)
        tw_layout.setSpacing(12)

        self.result_count_lbl = QLabel("0 emails")
        self.result_count_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; background: transparent; border: none;")
        tw_layout.addWidget(self.result_count_lbl)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Priority", "Subject", "From", "Date", "Score", "📎"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 160)
        self.table.setColumnWidth(4, 70)
        self.table.setColumnWidth(5, 40)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setDefaultSectionSize(52)
        self.table.setSortingEnabled(True)
        self.table.itemSelectionChanged.connect(self._on_row_select)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._context_menu)
        self.table.setStyleSheet(STYLESHEET)
        tw_layout.addWidget(self.table)

        splitter.addWidget(table_widget)

        # Email detail panel
        self.detail = EmailDetailPanel()
        splitter.addWidget(self.detail)

        splitter.setSizes([700, 450])
        root.addWidget(splitter, 1)

        # ── Status bar ──
        self.status_bar = QStatusBar()
        self.status_bar.setFixedHeight(28)
        root.addWidget(self.status_bar)
        self.status_bar.showMessage("Ready")

    def load_emails(self, emails: list):
        self._all_emails = emails
        self._update_stats(emails)
        self._populate_table(emails)

    def add_email_live(self, entry: dict):
        """Add a single email during live scanning."""
        self._all_emails.append(entry)
        self.stat_total.update_value(len(self._all_emails))

    def _update_stats(self, emails):
        by_prio = {"critical": 0, "high": 0, "medium": 0, "low": 0, "unknown": 0}
        attach_count = 0
        for e in emails:
            by_prio[e.get("priority", "unknown")] = by_prio.get(e.get("priority", "unknown"), 0) + 1
            if e.get("has_attach"):
                attach_count += 1

        self.stat_total.update_value(len(emails))
        self.stat_critical.update_value(by_prio["critical"])
        self.stat_high.update_value(by_prio["high"])
        self.stat_medium.update_value(by_prio["medium"])
        self.stat_low.update_value(by_prio["low"] + by_prio["unknown"])
        self.stat_attach.update_value(attach_count)

    def _populate_table(self, emails):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for row, e in enumerate(emails):
            self.table.insertRow(row)
            priority = e.get("priority", "unknown")
            color    = PRIORITY_COLORS.get(priority, COLORS["info"])
            labels   = {"critical": "⚡ CRITICAL", "high": "▲ HIGH",
                        "medium":   "● MEDIUM",   "low":  "▼ LOW", "unknown": "○ NORMAL"}

            # Priority cell
            p_item = QTableWidgetItem(labels.get(priority, priority.upper()))
            p_item.setForeground(QColor(color))
            p_item.setData(Qt.UserRole, e)
            p_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(row, 0, p_item)

            # Subject
            subj = QTableWidgetItem(e.get("subject", ""))
            subj.setForeground(QColor(COLORS["text_primary"]))
            self.table.setItem(row, 1, subj)

            # Sender
            sender_text = e.get("sender", "")
            if "<" in sender_text:
                sender_text = sender_text.split("<")[0].strip().strip('"')
            s_item = QTableWidgetItem(sender_text)
            s_item.setForeground(QColor(COLORS["text_secondary"]))
            self.table.setItem(row, 2, s_item)

            # Date
            d_item = QTableWidgetItem(e.get("date", ""))
            d_item.setForeground(QColor(COLORS["text_secondary"]))
            self.table.setItem(row, 3, d_item)

            # Score
            sc_item = QTableWidgetItem(f"{e.get('score', 0):.0f}")
            sc_item.setForeground(QColor(color))
            sc_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            sc_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.table.setItem(row, 4, sc_item)

            # Attachment
            att = QTableWidgetItem("📎" if e.get("has_attach") else "")
            att.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(row, 5, att)

        self.table.setSortingEnabled(True)
        self.result_count_lbl.setText(f"{len(emails)} emails")
        self.status_bar.showMessage(f"Showing {len(emails)} emails sorted by priority score")

    def _filter_table(self):
        query    = self.search_edit.text().strip().lower()
        prio_map = {
            "All Priorities": None, "Critical": "critical",
            "High": "high",        "Medium":   "medium",
            "Low": "low",          "Normal":   "unknown",
        }
        prio_filter = prio_map.get(self.filter_combo.currentText())

        filtered = []
        for e in self._all_emails:
            if prio_filter and e.get("priority") != prio_filter:
                continue
            if query:
                haystack = (e.get("subject","") + e.get("sender","") + e.get("body","")).lower()
                if query not in haystack:
                    continue
            filtered.append(e)

        self._populate_table(filtered)

    def _on_row_select(self):
        rows = self.table.selectedItems()
        if rows:
            data = self.table.item(rows[0].row(), 0).data(Qt.UserRole)
            if data:
                self.detail.show_email(data)

    def _context_menu(self, pos):
        idx = self.table.indexAt(pos)
        if not idx.isValid():
            return
        menu = QMenu(self)
        menu.addAction("📋  Copy Subject").triggered.connect(
            lambda: QApplication.clipboard().setText(
                self.table.item(idx.row(), 1).text()))
        menu.addAction("👤  Copy Sender").triggered.connect(
            lambda: QApplication.clipboard().setText(
                self.table.item(idx.row(), 2).text()))
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _export_csv(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", "emails_export.csv", "CSV Files (*.csv)")
        if not path:
            return
        import csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Priority", "Score", "Subject", "Sender", "Date", "Has Attachment"])
            for e in self._all_emails:
                writer.writerow([
                    e.get("priority"), e.get("score"),
                    e.get("subject"),  e.get("sender"),
                    e.get("date"),     e.get("has_attach"),
                ])
        QMessageBox.information(self, "Export Complete", f"Saved to:\n{path}")


# ─── DEMO DATA ────────────────────────────────────────────────────────────────
def generate_demo_emails():
    import random
    entries = [
        ("URGENT: Your account has been compromised - immediate action required",
         "security@banknotify.com", "critical", True,
         "Dear Customer, We've detected suspicious activity on your account. Please verify your identity immediately to prevent unauthorized access."),
        ("Interview Confirmation - Senior Software Engineer - TechCorp",
         "hr@techcorp.com", "high", True,
         "Dear Candidate, We're pleased to confirm your interview scheduled for next Monday at 10 AM. Please bring two forms of ID."),
        ("Invoice #INV-2024-0892 Due in 3 Days",
         "billing@services.io", "high", True,
         "Please find attached invoice #INV-2024-0892 for $1,250.00 due on the 20th. Late fees apply after the due date."),
        ("Project deadline reminder: Q4 Report submission",
         "pm@company.org", "critical", False,
         "This is a reminder that the Q4 annual report is due in 48 hours. Please ensure all sections are completed."),
        ("Your weekly digest: Top stories this week",
         "digest@newsservice.com", "low", False,
         "Here are the top stories curated for you this week. Click to read more about technology, business, and world news."),
        ("Re: Contract renewal discussion",
         "legal@partner.com", "high", True,
         "Further to our call yesterday, please review the attached updated contract terms. We need a decision by Friday."),
        ("Password reset request",
         "noreply@app.com", "high", False,
         "Someone requested a password reset for your account. If this was you, click the link to create a new password."),
        ("Team meeting - Thursday 3PM",
         "manager@company.com", "medium", False,
         "Hi team, We're meeting Thursday at 3PM to discuss Q1 planning. Agenda attached. Please confirm attendance."),
        ("50% OFF - Weekend Sale Ends Tonight!",
         "promo@shop.com", "low", False,
         "Don't miss our biggest sale of the year! Use code WEEKEND50 for 50% off everything in our store."),
        ("AWS Bill for October: $342.17",
         "billing@aws.amazon.com", "medium", True,
         "Your AWS statement for October is available. Total charges: $342.17. Breakdown: EC2 $180, S3 $62, Lambda $100."),
        ("GitHub: Action required — Dependabot security alert",
         "noreply@github.com", "high", False,
         "A critical vulnerability was found in one of your dependencies. Please review and merge the automated fix PR."),
        ("LinkedIn: John Smith accepted your connection",
         "notifications@linkedin.com", "low", False,
         "Your connection request was accepted. Start a conversation with John Smith to grow your professional network."),
        ("Flight confirmation: NYC → LON — Dec 15",
         "bookings@airtravel.com", "medium", True,
         "Your booking is confirmed. Flight AA101, departing JFK December 15th at 18:45, arriving LHR December 16th at 06:30."),
        ("RE: Proposal Review — Feedback needed",
         "client@bigfirm.com", "high", False,
         "Thanks for sending the proposal. I've reviewed it and have a few questions on sections 3 and 5. Can we schedule a call?"),
        ("Newsletter: October Tech Roundup",
         "editor@techdigest.io", "low", False,
         "This month: AI breakthroughs, new Apple announcements, open-source highlights, and developer tips."),
    ]

    results = []
    base = datetime.now()
    for i, (subj, sender, prio, attach, body) in enumerate(entries):
        dt = base - timedelta(hours=i * 8 + random.randint(0, 5))
        score_base = {"critical": 100, "high": 75, "medium": 50, "low": 25}[prio]
        score = score_base + random.uniform(-5, 10) + (10 if attach else 0)
        results.append({
            "id":         str(i),
            "subject":    subj,
            "sender":     sender,
            "date":       dt.strftime("%b %d, %Y  %H:%M"),
            "raw_date":   "",
            "priority":   prio,
            "score":      round(score, 1),
            "has_attach": attach,
            "body":       body,
            "read":       False,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ─── MAIN WINDOW ──────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Scanner")
        self.setMinimumSize(1200, 750)
        self.resize(1440, 880)
        self._worker = None

        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.config_panel    = ConfigPanel()
        self.scanning_panel  = ScanningPanel()
        self.results_panel   = ResultsDashboard()

        self.stack.addWidget(self.config_panel)    # 0
        self.stack.addWidget(self.scanning_panel)  # 1
        self.stack.addWidget(self.results_panel)   # 2

        self.config_panel.scan_requested.connect(self._start_scan)
        self.scanning_panel.cancelled.connect(self._cancel_scan)
        self.results_panel.back_requested.connect(self._go_home)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready  •  Email Scanner v1.0")

    def _apply_styles(self):
        self.setStyleSheet(STYLESHEET)

    def _go_home(self):
        if self._worker and self._worker.isRunning():
            self._worker.stop()
            self._worker.wait()
        self.stack.setCurrentIndex(0)

    def _start_scan(self, config):
        if config.get("demo"):
            self.stack.setCurrentIndex(1)
            self.scanning_panel.update_progress(50, "Loading demo data…")
            QTimer.singleShot(900, self._load_demo)
            return

        self.stack.setCurrentIndex(1)
        self.scanning_panel.update_progress(0, "Starting…")
        self._found_count = 0

        self._worker = EmailScannerWorker(config)
        self._worker.signals.progress.connect(self._on_progress)
        self._worker.signals.email_found.connect(self._on_email_found)
        self._worker.signals.finished.connect(self._on_finished)
        self._worker.signals.error.connect(self._on_error)
        self._worker.start()

    def _load_demo(self):
        emails = generate_demo_emails()
        self.scanning_panel.update_progress(100, "Demo data loaded!")
        QTimer.singleShot(600, lambda: self._on_finished(emails))

    @Slot(int, str)
    def _on_progress(self, pct, msg):
        self.scanning_panel.update_progress(pct, msg)

    @Slot(dict)
    def _on_email_found(self, entry):
        self._found_count = getattr(self, "_found_count", 0) + 1
        self.scanning_panel.update_found(self._found_count)

    @Slot(list)
    def _on_finished(self, emails):
        self.results_panel.load_emails(emails)
        self.stack.setCurrentIndex(2)
        self.statusBar().showMessage(f"Scan complete  •  {len(emails)} emails analyzed")

    @Slot(str)
    def _on_error(self, msg):
        self.stack.setCurrentIndex(0)
        QMessageBox.critical(self, "Scan Error", msg)

    def _cancel_scan(self):
        if self._worker:
            self._worker.stop()
        self.stack.setCurrentIndex(0)

    def closeEvent(self, event):
        if self._worker and self._worker.isRunning():
            self._worker.stop()
            self._worker.wait()
        event.accept()


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Email Scanner")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("EmailScanner")

    # High-DPI
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
