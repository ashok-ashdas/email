# 📧 Email Scanner — Desktop Application

A professional PySide6 desktop app that connects to your email via IMAP,
scans your inbox, and presents emails ranked by AI-powered priority scoring.

---

## 🚀 Quick Start

### 1. Install Python 3.10+
Download from https://python.org

### 2. Install dependencies
```bash
pip install PySide6
```

### 3. Run the app
```bash
python main.py
```

---

## 📋 Features

| Feature | Description |
|---|---|
| **Multi-provider support** | Gmail, Outlook, Yahoo, iCloud, Zoho, and custom IMAP |
| **Smart prioritization** | 5-level priority: Critical / High / Medium / Low / Normal |
| **Custom scan range** | Scan from last 1 day to 365 days |
| **Live stats dashboard** | Real-time counts for each priority level |
| **Email preview panel** | Click any email to read sender, date, body preview |
| **Search & filter** | Filter by keyword or priority level |
| **CSV export** | Export all results to spreadsheet |


---

## 🔐 Provider Setup

### Gmail
1. Enable IMAP: Gmail Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP
2. Create App Password:
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification (required)
   - Go to "App Passwords" → Select app: Mail → Generate
3. Use your Gmail address + the 16-character App Password in the app

### Outlook / Hotmail
1. Enable IMAP: Settings → View all Outlook settings → Mail → Sync email → Enable IMAP
2. Use your full email address and regular password
   (If 2FA is on, generate App Password at https://account.microsoft.com/security)

### Yahoo Mail
1. Enable IMAP: Settings → More Settings → Mailboxes → your account → IMAP
2. Create App Password at: https://login.yahoo.com/account/security

---

## ⚡ Priority Algorithm

Emails are scored (0–150+) using:
- **Keyword matching** — subject + body scanned for urgency signals
- **Recency** — newer emails get a recency bonus
- **Attachment flag** — emails with attachments score +10

| Priority | Keywords (examples) |
|---|---|
| ⚡ Critical | urgent, asap, emergency, deadline, action required |
| ▲ High | important, meeting, invoice, security, verify |
| ● Medium | update, review, request, report, scheduled |
| ▼ Low | newsletter, promo, sale, marketing, unsubscribe |

---

## 🛡️ Privacy

- Your credentials are **never stored to disk**
- All processing is **100% local** — no data is sent to any external server
- Passwords exist only in memory during the session

---

## 🖥️ System Requirements

- Python 3.10 or higher
- PySide6 6.5+
- macOS 12+, Windows 10+, or Linux (X11/Wayland)
- Active internet connection (for IMAP access)
