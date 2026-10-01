"""
Shill.Money Campaign Image Generator
Menghasilkan gambar promosi ultra-unik, kreatif, dan profesional dengan:
- 6 Layout Arsitektur Desain Visual yang Sepenuhnya Berbeda (Cyber HUD, Payroll Invoice, ID Badge, Market Chart, Validator Dossier, Glassmorphism Ledger)
- Palet Warna & Background Berbeda (Cyan Neon, Gold Onyx, Hologram Purple, Emerald Green, Solar Amber, Oceanic Aqua)
- Elemen Grafis Kreatif: Grafik Candlestick/Sparkline, Barcode Prosedural, Radar Gauge, Tabel Rincian Upah, Stempel Terverifikasi
- Tipografi TrueType Berkualitas Tinggi (Consolas / Arial)
- Resolusi Optimal Twitter: 1200 x 675 px (16:9)
"""

import os
import sys
import time
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from config import RESULTS_DIR, ACCOUNTS_FILE
from accounts_manager import load_accounts

OUT_DIR = RESULTS_DIR / "shill_images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CA = "0x93cfF6Dc0cf59680b8d85b9F3312a24bF1a7c1D8"
TAG = "@shillmoneyrh"
TICKER = "$SHILL"
URL = "https://shill.money/clock-in"


def get_font(font_name: str, size: int):
    """Mendapatkan font TrueType dengan fallback aman."""
    try:
        return ImageFont.truetype(font_name, size)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            return ImageFont.load_default()


# =============================================================================
# LAYOUT 1: CYBERPUNK HUD TERMINAL (Cyan Neon & Deep Navy)
# =============================================================================
def render_cyber_terminal(draw: ImageDraw.ImageDraw, w: int, h: int, handle: str, shift_id: int):
    # Background Grid
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(10, 25, 40), width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=(10, 25, 40), width=1)

    cyan = (0, 240, 255)
    dark_cyan = (0, 100, 140)
    white = (255, 255, 255)
    muted = (160, 190, 210)

    # Corner Brackets
    L = 35
    for (cx, cy) in [(30, 30), (w - 30, 30), (30, h - 30), (w - 30, h - 30)]:
        dx = L if cx == 30 else -L
        dy = L if cy == 30 else -L
        draw.line([(cx, cy), (cx + dx, cy)], fill=cyan, width=4)
        draw.line([(cx, cy), (cx, cy + dy)], fill=cyan, width=4)

    # Top Status Bar
    draw.rectangle([(50, 45), (w - 50, 85)], fill=(10, 20, 35), outline=dark_cyan, width=1)
    draw.text((70, 55), "SYS://SHILL-NODE-01", fill=cyan, font=get_font("consola.ttf", 16))
    draw.text((320, 55), "● CONSENSUS: 100% ONLINE", fill=(0, 255, 150), font=get_font("consola.ttf", 16))
    draw.text((w - 280, 55), f"PROTOCOL: {TAG}", fill=white, font=get_font("consola.ttf", 16))

    # Main Headline
    draw.text((70, 115), "AUTOMATED SOCIALFI MINING TERMINAL", fill=white, font=get_font("arial.ttf", 32))
    draw.text((70, 160), "Proof-of-Work Creator Attention Ledger • Direct Smart Contract Yield", fill=muted, font=get_font("arial.ttf", 18))

    # Central Terminal Window
    draw.rectangle([(70, 205), (w - 70, 470)], fill=(8, 16, 28), outline=cyan, width=2)
    draw.rectangle([(70, 205), (w - 70, 240)], fill=(16, 32, 54))
    draw.text((85, 213), "● ● ●  TERMINAL_SESSION: ACTIVE_CLOCKIN.EXE", fill=cyan, font=get_font("consola.ttf", 15))

    # Terminal Stats Columns
    draw.text((95, 260), f"OPERATOR HANDLE   : @{handle}", fill=white, font=get_font("consola.ttf", 20))
    draw.text((95, 295), f"SHIFT REGISTRATION: #SHILL-{shift_id}", fill=cyan, font=get_font("consola.ttf", 20))
    draw.text((95, 330), "WORKLOAD MULTIPLIER: 5.0x FULL BOOST", fill=(0, 255, 180), font=get_font("consola.ttf", 20))
    draw.text((95, 365), f"PORTAL URL        : {URL}", fill=muted, font=get_font("consola.ttf", 18))

    # Telemetry Mini Waveform Box
    chart_x, chart_y, chart_w, chart_h = w - 380, 260, 280, 120
    draw.rectangle([(chart_x, chart_y), (chart_x + chart_w, chart_y + chart_h)], fill=(5, 12, 22), outline=dark_cyan, width=1)
    draw.text((chart_x + 10, chart_y + 8), "ATTENTION TELEMETRY", fill=cyan, font=get_font("consola.ttf", 12))
    # Procedural wave line
    points = []
    for px in range(chart_x + 10, chart_x + chart_w - 10, 12):
        py = chart_y + 65 + int(25 * random.uniform(-0.8, 0.8))
        points.append((px, py))
    if len(points) > 1:
        draw.line(points, fill=cyan, width=2)

    # Multiplier metrics bar inside terminal
    draw.rectangle([(95, 415), (w - 95, 450)], fill=(12, 24, 40), outline=dark_cyan, width=1)
    draw.text((115, 423), "REWARD RATES:   [ LIKE: +1 ]   [ RETWEET: +3 ]   [ REPLY: +2 ]   [ MEDIA: +10 ]   [ IDENTIFIER: +30 ]", fill=(200, 230, 255), font=get_font("consola.ttf", 14))

    # Bottom CA Footer
    draw.rectangle([(70, 495), (w - 70, 630)], fill=(12, 22, 36), outline=cyan, width=2)
    draw.text((95, 515), f"OFFICIAL ASSET: {TICKER} (EVM CONTRACT)", fill=cyan, font=get_font("consola.ttf", 16))
    draw.text((95, 545), CA, fill=white, font=get_font("consola.ttf", 22))
    draw.text((95, 585), "VERIFIED ON-CHAIN PROTOCOL DECENTRALIZED REWARD POOL", fill=(140, 175, 200), font=get_font("consola.ttf", 13))

    # Certified Stamp
    draw.rectangle([(w - 230, 515), (w - 95, 605)], fill=cyan)
    draw.text((w - 215, 545), "VERIFIED\nCLOCK-IN", fill=(0, 0, 0), font=get_font("arial.ttf", 18))


# =============================================================================
# LAYOUT 2: DECENTRALIZED PAYROLL INVOICE (Gold & Onyx Black)
# =============================================================================
def render_payroll_invoice(draw: ImageDraw.ImageDraw, w: int, h: int, handle: str, shift_id: int):
    gold = (255, 215, 0)
    dark_gold = (160, 130, 20)
    white = (255, 255, 255)
    gray = (180, 180, 180)

    # Outer Document Frame
    draw.rectangle([(40, 30), (w - 40, h - 30)], outline=dark_gold, width=2)
    draw.rectangle([(48, 38), (w - 48, h - 38)], outline=(40, 40, 40), width=1)

    # Document Header
    draw.text((65, 55), "SHILL.MONEY PROTOCOL // WAGE & PAYCHECK STATEMENT", fill=gold, font=get_font("arial.ttf", 24))
    draw.text((65, 90), f"ISSUED FOR OPERATOR: @{handle} • ASSIGNMENT #{shift_id}", fill=white, font=get_font("consola.ttf", 16))
    draw.text((w - 270, 55), f"VALIDATOR: {TAG}", fill=gray, font=get_font("consola.ttf", 16))

    draw.line([(65, 125), (w - 65, 125)], fill=gold, width=2)

    # Itemized Payroll Table
    table_top = 145
    draw.rectangle([(65, table_top), (w - 65, table_top + 40)], fill=(30, 28, 20))
    draw.text((80, table_top + 10), "WORKFLOW TASK", fill=gold, font=get_font("consola.ttf", 15))
    draw.text((360, table_top + 10), "WEIGHT", fill=gold, font=get_font("consola.ttf", 15))
    draw.text((540, table_top + 10), "REWARD UNIT", fill=gold, font=get_font("consola.ttf", 15))
    draw.text((w - 240, table_top + 10), "SETTLEMENT STATUS", fill=gold, font=get_font("consola.ttf", 15))

    rows = [
        ("Proof-of-Work Clock-In Shift", "10.0x Base", f"1,000 {TICKER}", "SETTLED ON-CHAIN"),
        ("Social Squad Retweet Multiplier", "3.0x Multi", f"300 {TICKER}", "VERIFIED BY POOL"),
        ("Contextual Creator Discussions", "2.0x Multi", f"200 {TICKER}", "SYNCED TO LEDGER"),
        ("Graphic Media Shift Badge Proof", "5.0x Bonus", f"500 {TICKER}", "CONFIRMED VALID")
    ]

    curr_y = table_top + 40
    for idx, (task, weight, amt, status) in enumerate(rows):
        bg = (18, 18, 22) if idx % 2 == 0 else (12, 12, 16)
        draw.rectangle([(65, curr_y), (w - 65, curr_y + 45)], fill=bg, outline=(35, 35, 40), width=1)
        draw.text((80, curr_y + 12), task, fill=white, font=get_font("consola.ttf", 15))
        draw.text((360, curr_y + 12), weight, fill=(255, 230, 120), font=get_font("consola.ttf", 15))
        draw.text((540, curr_y + 12), amt, fill=gold, font=get_font("consola.ttf", 15))
        draw.text((w - 240, curr_y + 12), f"✓ {status}", fill=(0, 255, 140), font=get_font("consola.ttf", 14))
        curr_y += 45

    # Barcode & Total Block
    bottom_box_y = curr_y + 20
    draw.rectangle([(65, bottom_box_y), (w - 65, bottom_box_y + 90)], fill=(20, 20, 25), outline=dark_gold, width=1)

    # Procedural Barcode
    bx = 85
    for _ in range(45):
        bw = random.choice([2, 4, 6])
        draw.rectangle([(bx, bottom_box_y + 15), (bx + bw, bottom_box_y + 65)], fill=gold)
        bx += bw + random.choice([2, 3, 5])
        if bx > 380:
            break
    draw.text((85, bottom_box_y + 70), f"*SHILL-VERIFIED-SHIFT-{shift_id}*", fill=gray, font=get_font("consola.ttf", 11))

    # Total Payout Box
    draw.text((420, bottom_box_y + 20), "TOTAL LIQUID ALLOCATION:", fill=gray, font=get_font("arial.ttf", 16))
    draw.text((420, bottom_box_y + 45), f"2,000+ {TICKER} (MAX QUADRATIC YIELD)", fill=gold, font=get_font("arial.ttf", 22))

    # Big Stamp
    stamp_x, stamp_y = w - 240, bottom_box_y + 12
    draw.rectangle([(stamp_x, stamp_y), (stamp_x + 155, stamp_y + 65)], outline=(0, 255, 140), width=3)
    draw.text((stamp_x + 18, stamp_y + 12), "SETTLED", fill=(0, 255, 140), font=get_font("arial.ttf", 20))
    draw.text((stamp_x + 15, stamp_y + 38), "ON-CHAIN", fill=(0, 255, 140), font=get_font("arial.ttf", 15))

    # Contract Address Banner
    footer_y = bottom_box_y + 105
    draw.rectangle([(65, footer_y), (w - 65, footer_y + 65)], fill=(12, 10, 5), outline=gold, width=2)
    draw.text((85, footer_y + 10), f"OFFICIAL SMART CONTRACT ({TICKER}) :", fill=gold, font=get_font("consola.ttf", 14))
    draw.text((85, footer_y + 32), CA, fill=white, font=get_font("consola.ttf", 20))


# =============================================================================
# LAYOUT 3: OPERATOR ACCESS PASS / ID CARD (Purple Hologram & Violet)
# =============================================================================
def render_security_pass(draw: ImageDraw.ImageDraw, w: int, h: int, handle: str, shift_id: int):
    purple = (190, 70, 255)
    neon_pink = (255, 40, 160)
    white = (255, 255, 255)
    gray = (175, 160, 200)

    # Diagonal Holographic Accent Lines
    for d in range(-100, w + 200, 70):
        draw.line([(d, 0), (d - 180, h)], fill=(25, 12, 45), width=1)

    # LEFT PANEL: Vertical Operator Pass
    card_w = 340
    draw.rectangle([(50, 40), (50 + card_w, h - 40)], fill=(18, 10, 36), outline=purple, width=2)

    # Lanyard slot
    draw.rectangle([(50 + card_w // 2 - 35, 52), (50 + card_w // 2 + 35, 62)], fill=(40, 25, 75))

    # Avatar box
    draw.rectangle([(90, 90), (50 + card_w - 40, 240)], fill=(30, 16, 58), outline=neon_pink, width=1)
    draw.text((120, 145), "[ VERIFIED ]\n[ CREATOR ]", fill=purple, font=get_font("consola.ttf", 18))

    # Handle & Clearance
    draw.text((75, 260), f"@{handle}", fill=white, font=get_font("arial.ttf", 24))
    draw.text((75, 295), f"ID: #SHILL-{shift_id}", fill=purple, font=get_font("consola.ttf", 18))

    draw.rectangle([(75, 335), (50 + card_w - 25, 385)], fill=(35, 14, 65), outline=neon_pink, width=1)
    draw.text((90, 348), "RANK: SQUAD ALPHA", fill=neon_pink, font=get_font("consola.ttf", 16))

    # Holographic Barcode on Left Card
    bx = 75
    for _ in range(30):
        bw = random.choice([2, 4, 5])
        draw.rectangle([(bx, 410), (bx + bw, 460)], fill=purple)
        bx += bw + random.choice([2, 3])
        if bx > 50 + card_w - 30:
            break
    draw.text((75, 470), "SECURITY PASS VERIFIED", fill=gray, font=get_font("consola.ttf", 12))

    # Clock in link on card
    draw.text((75, 550), "PORTAL ACCESS:", fill=gray, font=get_font("consola.ttf", 13))
    draw.text((75, 570), "shill.money/clock-in", fill=purple, font=get_font("consola.ttf", 14))

    # RIGHT PANEL: Shift Credentials & On-Chain Metrics
    rx = 50 + card_w + 35
    rw = w - rx - 50

    # Header Bar
    draw.rectangle([(rx, 40), (rx + rw, 95)], fill=(22, 12, 42), outline=purple, width=1)
    draw.text((rx + 20, 55), "SHILL NETWORK // ATTENTION MINING PASS", fill=purple, font=get_font("arial.ttf", 22))
    draw.text((rx + rw - 180, 58), f"TAG: {TAG}", fill=white, font=get_font("consola.ttf", 15))

    # Metric Cards Grid (2x2)
    cards = [
        ("CONSENSUS METRIC", "PROOF-OF-WORK VERIFIED", (0, 255, 160)),
        ("DAILY ALLOCATION", "+500 LEADERBOARD PTS", neon_pink),
        ("LIQUID PROTOCOL", "$SHILL EVM CONTRACT", purple),
        ("SQUAD MULTIPLIER", "MAX 5.0x ACTIVE", (255, 220, 0))
    ]

    for i, (label, val, col) in enumerate(cards):
        cx = rx + (i % 2) * (rw // 2 + 10)
        cy = 120 + (i // 2) * 115
        cw = rw // 2 - 15
        draw.rectangle([(cx, cy), (cx + cw, cy + 95)], fill=(16, 8, 32), outline=purple, width=1)
        draw.text((cx + 15, cy + 18), label, fill=gray, font=get_font("consola.ttf", 13))
        draw.text((cx + 15, cy + 45), val, fill=col, font=get_font("consola.ttf", 16))

    # Bottom CA Box
    ca_y = 375
    draw.rectangle([(rx, ca_y), (rx + rw, ca_y + 130)], fill=(24, 12, 48), outline=neon_pink, width=2)
    draw.text((rx + 20, ca_y + 18), f"OFFICIAL {TICKER} CONTRACT ADDRESS:", fill=purple, font=get_font("consola.ttf", 16))
    draw.text((rx + 20, ca_y + 48), CA, fill=white, font=get_font("consola.ttf", 20))
    draw.text((rx + 20, ca_y + 88), "EVM ON-CHAIN VERIFICATION • ZERO INTERMEDIARIES", fill=gray, font=get_font("consola.ttf", 14))

    # Footer note
    draw.text((rx + 10, h - 70), "Clock in daily to maintain multiplier continuity & maximize payout.", fill=gray, font=get_font("arial.ttf", 15))


# =============================================================================
# LAYOUT 4: MARKET ANALYTICS & YIELD CHART (Emerald Green & Charcoal)
# =============================================================================
def render_market_analytics(draw: ImageDraw.ImageDraw, w: int, h: int, handle: str, shift_id: int):
    emerald = (0, 255, 140)
    dark_green = (0, 100, 60)
    white = (255, 255, 255)
    gray = (160, 185, 175)

    # Dark Matrix Dotted Background
    for x in range(0, w, 50):
        for y in range(0, h, 50):
            draw.point((x, y), fill=(0, 60, 40))

    # Header
    draw.rectangle([(50, 40), (w - 50, 95)], fill=(6, 24, 16), outline=emerald, width=1)
    draw.text((70, 52), "SHILL.MONEY SOCIAL-FI ANALYTICS // ON-CHAIN YIELD INDEX", fill=emerald, font=get_font("arial.ttf", 22))
    draw.text((w - 260, 55), f"OFFICIAL: {TAG}", fill=white, font=get_font("consola.ttf", 16))

    # Main Chart Box (Candlestick / Sparkline)
    chart_x, chart_y, chart_w, chart_h = 50, 120, w - 420, 240
    draw.rectangle([(chart_x, chart_y), (chart_x + chart_w, chart_y + chart_h)], fill=(4, 16, 12), outline=dark_green, width=1)
    draw.text((chart_x + 15, chart_y + 12), "DAILY CREATOR ATTENTION METRIC ($SHILL SHIFT INDEX)", fill=emerald, font=get_font("consola.ttf", 14))

    # Procedural Green Candlesticks
    cx = chart_x + 35
    base_price = 140
    while cx < chart_x + chart_w - 40:
        delta = random.randint(-15, 25)
        open_p = chart_y + base_price
        close_p = open_p - delta
        high_p = min(open_p, close_p) - random.randint(5, 15)
        low_p = max(open_p, close_p) + random.randint(5, 15)

        color = emerald if close_p <= open_p else (255, 70, 70)
        draw.line([(cx + 8, high_p), (cx + 8, low_p)], fill=color, width=1)
        top_b, bot_b = min(open_p, close_p), max(open_p, close_p)
        draw.rectangle([(cx, top_b), (cx + 16, max(bot_b, top_b + 3))], fill=color)

        base_price = max(40, min(180, base_price - delta))
        cx += 32

    # RIGHT STATS BOX
    rx = chart_x + chart_w + 25
    rw = w - rx - 50
    draw.rectangle([(rx, chart_y), (rx + rw, chart_y + chart_h)], fill=(6, 20, 15), outline=emerald, width=1)
    draw.text((rx + 20, chart_y + 20), "SHIFT YIELD BOOST", fill=gray, font=get_font("consola.ttf", 14))
    draw.text((rx + 20, chart_y + 45), "+420%", fill=emerald, font=get_font("arial.ttf", 36))

    draw.text((rx + 20, chart_y + 110), f"OPERATOR: @{handle}", fill=white, font=get_font("consola.ttf", 16))
    draw.text((rx + 20, chart_y + 140), f"SHIFT NO: #{shift_id}", fill=emerald, font=get_font("consola.ttf", 16))
    draw.text((rx + 20, chart_y + 175), "PROOF STATUS: VERIFIED", fill=(0, 255, 200), font=get_font("consola.ttf", 16))

    # Bottom Progress Bar
    draw.rectangle([(50, 385), (w - 50, 450)], fill=(8, 22, 16), outline=dark_green, width=1)
    draw.text((70, 400), "SHIFT COMPLETION GOAL:", fill=gray, font=get_font("consola.ttf", 14))
    draw.rectangle([(260, 405), (w - 180, 430)], fill=(12, 35, 25), outline=dark_green, width=1)
    draw.rectangle([(260, 405), (w - 180, 430)], fill=emerald)
    draw.text((w - 150, 405), "100% DONE", fill=emerald, font=get_font("consola.ttf", 16))

    # Contract Address Box
    ca_y = 475
    draw.rectangle([(50, ca_y), (w - 50, ca_y + 135)], fill=(4, 18, 12), outline=emerald, width=2)
    draw.text((75, ca_y + 18), f"SMART CONTRACT IDENTIFIER ({TICKER}) :", fill=emerald, font=get_font("consola.ttf", 16))
    draw.text((75, ca_y + 48), CA, fill=white, font=get_font("consola.ttf", 22))
    draw.text((75, ca_y + 90), f"CLOCK-IN PORTAL: {URL} • TRANSPARENT SOCIALFI LEDGER", fill=gray, font=get_font("consola.ttf", 15))


# =============================================================================
# LAYOUT 5: SOLAR AMBER VALIDATOR DOSSIER (Amber Orange & Charcoal)
# =============================================================================
def render_validator_dossier(draw: ImageDraw.ImageDraw, w: int, h: int, handle: str, shift_id: int):
    amber = (255, 160, 0)
    dark_amber = (150, 90, 0)
    white = (255, 255, 255)
    gray = (190, 180, 165)

    # Geometric Diagonal Framing
    draw.rectangle([(40, 30), (w - 40, h - 30)], outline=dark_amber, width=2)
    draw.polygon([(40, 30), (160, 30), (40, 150)], fill=(40, 24, 0))
    draw.polygon([(w - 40, h - 30), (w - 160, h - 30), (w - 40, h - 150)], fill=(40, 24, 0))

    # Dossier Title Header
    draw.text((70, 50), "SHILL PROTOCOL // VALIDATOR DOSSIER & SHIFT RECORD", fill=amber, font=get_font("arial.ttf", 24))
    draw.text((70, 85), f"OFFICIAL SHIFT STATEMENT FOR OPERATOR @{handle}", fill=white, font=get_font("consola.ttf", 16))
    draw.text((w - 260, 50), f"CONSENSUS: {TAG}", fill=gray, font=get_font("consola.ttf", 15))

    draw.line([(70, 120), (w - 70, 120)], fill=amber, width=2)

    # Radar Circle Gauge on the Left
    center_x, center_y, radius = 175, 260, 100
    for r in range(25, radius + 1, 25):
        draw.ellipse([(center_x - r, center_y - r), (center_x + r, center_y + r)], outline=dark_amber, width=1)
    draw.line([(center_x - radius, center_y), (center_x + radius, center_y)], fill=dark_amber, width=1)
    draw.line([(center_x, center_y - radius), (center_x, center_y + radius)], fill=dark_amber, width=1)
    # Rotating radar beam
    draw.line([(center_x, center_y), (center_x + 70, center_y - 65)], fill=amber, width=3)
    draw.text((center_x - 65, center_y + radius + 15), "VALIDATOR RADAR", fill=amber, font=get_font("consola.ttf", 14))

    # Checklist & Metrics Box on the Right
    rx = 320
    draw.rectangle([(rx, 145), (w - 70, 395)], fill=(20, 14, 4), outline=dark_amber, width=1)
    draw.text((rx + 20, 165), f"RECORD ID         : #SHILL-{shift_id}", fill=amber, font=get_font("consola.ttf", 18))
    draw.text((rx + 20, 200), f"OPERATOR HANDLE   : @{handle}", fill=white, font=get_font("consola.ttf", 18))
    draw.text((rx + 20, 235), "CONSENSUS TIER    : LEVEL 5 (MAX MULTIPLIER)", fill=(255, 220, 0), font=get_font("consola.ttf", 18))

    checklist = [
        "[X] Daily Proof-of-Work Clock-In Registered",
        "[X] Cross-Squad Social Interaction Multiplied",
        "[X] Verified Smart Contract Attribution Confirmed",
        "[X] Decentralized Payroll Allocation Staked"
    ]
    cy = 275
    for item in checklist:
        draw.text((rx + 20, cy), item, fill=(0, 255, 160), font=get_font("consola.ttf", 14))
        cy += 25

    # Bottom CA Section
    footer_y = 425
    draw.rectangle([(70, footer_y), (w - 70, footer_y + 170)], fill=(28, 18, 5), outline=amber, width=2)
    draw.text((95, footer_y + 20), f"OFFICIAL {TICKER} SMART CONTRACT ADDRESS:", fill=amber, font=get_font("consola.ttf", 16))
    draw.text((95, footer_y + 55), CA, fill=white, font=get_font("consola.ttf", 22))
    draw.text((95, footer_y + 105), f"CLOCK-IN NOW: {URL} • 100% VERIFIED EVM TRANSACTION", fill=gray, font=get_font("consola.ttf", 16))

    # Watermark Stamp
    draw.rectangle([(w - 260, footer_y + 30), (w - 95, footer_y + 120)], outline=amber, width=2)
    draw.text((w - 245, footer_y + 55), "CONFIDENTIAL\nON-CHAIN PROOF", fill=amber, font=get_font("consola.ttf", 14))


# =============================================================================
# LAYOUT 6: OCEANIC AQUA GLASSMORPHISM (Aqua Teal & Deep Indigo)
# =============================================================================
def render_glassmorphism(draw: ImageDraw.ImageDraw, w: int, h: int, handle: str, shift_id: int):
    aqua = (0, 245, 220)
    deep_aqua = (0, 120, 140)
    white = (255, 255, 255)
    gray = (170, 205, 220)

    # Sleek Gradient Line Accents
    for y in range(0, h, 35):
        draw.line([(0, y), (w, y)], fill=(6, 18, 30), width=1)

    # Top Pill Header
    draw.rectangle([(60, 40), (w - 60, 95)], fill=(8, 28, 44), outline=aqua, width=1)
    draw.text((85, 52), "SHILL.MONEY // DECENTRALIZED ATTENTION LEDGER", fill=aqua, font=get_font("arial.ttf", 22))
    draw.text((w - 260, 55), f"PROTOCOL: {TAG}", fill=white, font=get_font("consola.ttf", 16))

    # Glass Card 1 (Left): Operator Profile
    c1_w = (w - 150) // 2
    draw.rectangle([(60, 125), (60 + c1_w, 375)], fill=(10, 32, 50), outline=deep_aqua, width=1)
    draw.text((85, 145), "OPERATOR CREDENTIALS", fill=aqua, font=get_font("consola.ttf", 15))
    draw.text((85, 185), f"@{handle}", fill=white, font=get_font("arial.ttf", 26))
    draw.text((85, 230), f"SHIFT NO: #SHILL-{shift_id}", fill=aqua, font=get_font("consola.ttf", 18))
    draw.text((85, 270), "STATUS  : CLOCKED-IN & VALIDATED", fill=(0, 255, 180), font=get_font("consola.ttf", 16))
    draw.text((85, 310), f"PORTAL  : {URL}", fill=gray, font=get_font("consola.ttf", 14))

    # Glass Card 2 (Right): Multiplier Metrics
    c2_x = 60 + c1_w + 30
    draw.rectangle([(c2_x, 125), (w - 60, 375)], fill=(10, 32, 50), outline=deep_aqua, width=1)
    draw.text((c2_x + 25, 145), "ATTENTION MULTIPLIER MATRIX", fill=aqua, font=get_font("consola.ttf", 15))

    metrics = [
        ("Base Shift Clock-in", "+10 Pts"),
        ("Like Interaction", "+1 Pt"),
        ("Retweet Amplification", "+3 Pts"),
        ("Discussion Comments", "+2 Pts"),
        ("Verified EVM Identifiers", "+30 Pts")
    ]
    my = 185
    for m_label, m_val in metrics:
        draw.text((c2_x + 25, my), m_label, fill=white, font=get_font("consola.ttf", 15))
        draw.text((w - 180, my), m_val, fill=aqua, font=get_font("consola.ttf", 15))
        my += 32

    # Bottom Glass Card (Full Width): CA Banner
    draw.rectangle([(60, 410), (w - 60, 615)], fill=(8, 24, 40), outline=aqua, width=2)
    draw.text((85, 435), f"OFFICIAL {TICKER} SMART CONTRACT IDENTIFIER (EVM):", fill=aqua, font=get_font("consola.ttf", 16))
    draw.text((85, 475), CA, fill=white, font=get_font("consola.ttf", 24))
    draw.text((85, 535), "100% VERIFIED ON-CHAIN PAYROLL • DIRECT REWARD DISTRIBUTION", fill=gray, font=get_font("consola.ttf", 16))

    # Floating Verified Badge
    draw.rectangle([(w - 240, 435), (w - 85, 505)], fill=aqua)
    draw.text((w - 220, 458), "VERIFIED PASS", fill=(0, 0, 0), font=get_font("arial.ttf", 16))


# =============================================================================
# MAIN IMAGE GENERATOR DISPATCHER
# =============================================================================
LAYOUT_FUNCTIONS = [
    render_cyber_terminal,       # Layout 1: Cyan Terminal HUD
    render_payroll_invoice,      # Layout 2: Gold Payroll Statement
    render_security_pass,        # Layout 3: Purple Holographic Pass
    render_market_analytics,     # Layout 4: Emerald Analytics Dashboard
    render_validator_dossier,    # Layout 5: Solar Amber Validator Dossier
    render_glassmorphism         # Layout 6: Oceanic Aqua Glassmorphism
]
THEME_PRESETS = LAYOUT_FUNCTIONS

BACKGROUND_COLORS = [
    (7, 10, 16),    # Deep Cyan Black
    (12, 10, 8),    # Onyx Charcoal
    (10, 6, 22),    # Deep Obsidian Violet
    (4, 12, 8),     # Forest Matrix Black
    (16, 10, 4),    # Amber Night
    (4, 14, 24)     # Oceanic Indigo
]


def generate_image_for_account(account_handle: str, layout_idx: int = 0, cycle_num: int = 1) -> str:
    """Menghasilkan satu gambar kreatif & ultra-unik untuk akun dengan salah satu dari 6 layout berbeda."""
    w, h = 1200, 675
    clean_handle = account_handle.lstrip("@").strip()

    selected_idx = layout_idx % len(LAYOUT_FUNCTIONS)
    bg_color = BACKGROUND_COLORS[selected_idx]
    render_func = LAYOUT_FUNCTIONS[selected_idx]

    img = Image.new("RGB", (w, h), color=bg_color)
    draw = ImageDraw.Draw(img)

    shift_num = abs(hash(f"{clean_handle}_{cycle_num}_{time.time()}")) % 9000 + 1000

    # Panggil fungsi layout yang dipilih
    render_func(draw, w, h, clean_handle, shift_num)

    out_file = OUT_DIR / f"shill_{clean_handle}_c{cycle_num}.png"
    img.save(out_file, format="PNG", quality=95)
    return str(out_file.resolve())


def generate_all_images():
    """Menghasilkan gambar unik untuk semua akun yang ada di accounts.json atau akun dummy."""
    results = {}
    handles = []

    if ACCOUNTS_FILE.exists():
        try:
            acc_data = load_accounts()
            for v in acc_data.get("accounts", {}).values():
                h = v.get("screen_name")
                if h:
                    handles.append(h)
        except Exception:
            pass

    if not handles:
        handles = [f"operator_{i}" for i in range(1, 9)]

    layout_names = [
        "Cyberpunk HUD Terminal",
        "Decentralized Payroll Statement",
        "Operator Security Pass",
        "Market Analytics & Yield Chart",
        "Solar Amber Validator Dossier",
        "Oceanic Aqua Glassmorphism"
    ]

    for idx, handle in enumerate(handles):
        out_path = generate_image_for_account(handle, idx)
        results[handle] = out_path
        l_name = layout_names[idx % len(layout_names)]
        print(f"✓ Generated creative graphic for @{handle} [{l_name}] -> {Path(out_path).name}")

    return results


if __name__ == "__main__":
    generate_all_images()
