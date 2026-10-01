"""
Shill.Money Campaign Image Generator
Menghasilkan 8 gambar promosi 100% BERBEDA dari segi:
- Background & Palet Warna (Cyan, Gold, Emerald, Purple, Crimson, Amber, Aqua, Lime)
- Layout Desain & Struktur Kartu / Tabel
- Tipografi, Judul & Badge
- Identitas Operator & Shift Unik per Akun
Resolusi: 1200 x 675 px (Optimal untuk Twitter 16:9)
"""

import os
import sys
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

THEME_PRESETS = [
    {
        "id": "cyan_terminal",
        "bg": (7, 10, 16),
        "primary": (0, 240, 255),     # Cyan
        "secondary": (0, 120, 255),
        "badge_bg": (12, 22, 36),
        "header": "SHILL.MONEY // OPERATOR TERMINAL",
        "title": "VERIFIED CLOCK-IN SHIFT",
        "subtitle": "Automated SocialFi Yield Proof & Attention Mining",
        "status": "SHIFT STATUS: ACTIVE & VERIFIED",
        "pattern": "grid"
    },
    {
        "id": "gold_paycheck",
        "bg": (5, 11, 26),
        "primary": (255, 215, 0),     # Gold
        "secondary": (255, 140, 0),
        "badge_bg": (20, 24, 40),
        "header": "DECENTRALIZED PAYCHECK SYSTEM",
        "title": "CREATOR WAGE DISTRIBUTION",
        "subtitle": "Proof-of-Work Shift • Transparent EVM Tokenomics",
        "status": "PAYCHECK MULTIPLIER: 5.0x ACTIVE",
        "pattern": "radar"
    },
    {
        "id": "emerald_matrix",
        "bg": (3, 20, 12),
        "primary": (0, 255, 136),     # Emerald
        "secondary": (32, 227, 178),
        "badge_bg": (8, 32, 20),
        "header": "PROTOCOL PROOF-OF-WORK LEDGER",
        "title": "DAILY SHIFT COMPLETED",
        "subtitle": "Turning Real Discussions Into Verifiable Yield",
        "status": "ON-CHAIN METRICS: VALIDATED",
        "pattern": "matrix"
    },
    {
        "id": "purple_pass",
        "bg": (13, 7, 30),
        "primary": (176, 38, 255),    # Purple
        "secondary": (255, 20, 147),
        "badge_bg": (26, 14, 48),
        "header": "SHILL.MONEY ATTENTION MINING",
        "title": "SOCIAL-FI PROOF OF REACH",
        "subtitle": "Smart Contract Rewards For Authentic Engagement",
        "status": "TIER: SQUAD RAID MULTIPLIER",
        "pattern": "angled"
    },
    {
        "id": "rose_crimson",
        "bg": (24, 5, 9),
        "primary": (255, 51, 102),    # Rose Crimson
        "secondary": (255, 0, 63),
        "badge_bg": (38, 12, 18),
        "header": "DECENTRALIZED CREATOR PAYSLIP",
        "title": "OFFICIAL SHIFT STATEMENT",
        "subtitle": "EVM On-Chain Wage Tracking • Zero Intermediaries",
        "status": "SETTLEMENT: LIQUID ON-CHAIN",
        "pattern": "bars"
    },
    {
        "id": "solar_amber",
        "bg": (22, 15, 3),
        "primary": (255, 153, 0),     # Solar Amber
        "secondary": (255, 230, 0),
        "badge_bg": (36, 26, 8),
        "header": "SHILL NETWORK VALIDATOR",
        "title": "COMMUNITY SQUAD SHIFT",
        "subtitle": "Collaborative Engagement Multiplier Ecosystem",
        "status": "VALIDATOR POOL: CLOCKED-IN",
        "pattern": "isometric"
    },
    {
        "id": "aqua_teal",
        "bg": (2, 22, 26),
        "primary": (0, 245, 212),     # Aqua Teal
        "secondary": (0, 187, 249),
        "badge_bg": (6, 36, 42),
        "header": "WEB3 SOCIALFI PROTOCOL",
        "title": "ON-CHAIN ATTENTION CAPITAL",
        "subtitle": "Transforming Social Reach Into Decentralized Wages",
        "status": "ATTENTION POOL: STAKED",
        "pattern": "gradient_box"
    },
    {
        "id": "cyber_lime",
        "bg": (12, 14, 18),
        "primary": (112, 255, 0),     # Cyber Lime
        "secondary": (0, 255, 170),
        "badge_bg": (20, 26, 30),
        "header": "SHILL.MONEY // PROTOCOL PROOF",
        "title": "SHIFT CLOCK-IN VERIFIED",
        "subtitle": "Transparent Creator Paychecks & Liquid Multipliers",
        "status": "CLOCK-IN: RECORDED ON LEDGER",
        "pattern": "minimal_frame"
    }
]


def draw_pattern(draw: ImageDraw.ImageDraw, pattern: str, w: int, h: int, color: tuple):
    """Menggambar latar belakang grafis geometris unik per tema."""
    faint_color = (color[0] // 5, color[1] // 5, color[2] // 5)
    fainter = (color[0] // 10, color[1] // 10, color[2] // 10)

    if pattern == "grid":
        for x in range(0, w, 50):
            draw.line([(x, 0), (x, h)], fill=fainter, width=1)
        for y in range(0, h, 50):
            draw.line([(0, y), (w, y)], fill=fainter, width=1)
        draw.rectangle([(20, 20), (w - 20, h - 20)], outline=faint_color, width=2)

    elif pattern == "radar":
        cx, cy = w // 2, h // 2
        for r in range(100, 600, 100):
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=fainter, width=1)
        draw.line([(0, cy), (w, cy)], fill=fainter, width=1)
        draw.line([(cx, 0), (cx, h)], fill=fainter, width=1)

    elif pattern == "matrix":
        for x in range(0, w, 40):
            draw.line([(x, 0), (x, h)], fill=fainter, width=1)
        for y in range(60, h, 80):
            draw.line([(0, y), (w, y)], fill=faint_color, width=1)

    elif pattern == "angled":
        for x in range(-200, w + 400, 80):
            draw.line([(x, 0), (x - 200, h)], fill=fainter, width=1)
        draw.polygon([(0, 0), (120, 0), (0, 120)], fill=faint_color)
        draw.polygon([(w, h), (w - 120, h), (w, h - 120)], fill=faint_color)

    elif pattern == "bars":
        for y in range(0, h, 25):
            draw.line([(0, y), (w, y)], fill=fainter, width=1)
        draw.rectangle([(30, 30), (w - 30, h - 30)], outline=faint_color, width=2)

    elif pattern == "isometric":
        for x in range(0, w, 90):
            for y in range(0, h, 90):
                draw.rectangle([(x, y), (x + 40, y + 40)], outline=fainter, width=1)

    elif pattern == "gradient_box":
        draw.rectangle([(15, 15), (w - 15, h - 15)], outline=faint_color, width=2)
        draw.rectangle([(30, 30), (w - 30, h - 30)], outline=fainter, width=1)
        for x in range(0, w, 60):
            draw.line([(x, 0), (x, 80)], fill=faint_color, width=1)
            draw.line([(x, h - 80), (x, h)], fill=faint_color, width=1)

    elif pattern == "minimal_frame":
        draw.rectangle([(25, 25), (w - 25, h - 25)], outline=color, width=2)
        draw.rectangle([(35, 35), (w - 35, h - 35)], outline=fainter, width=1)
        L = 40
        draw.line([(25, 25), (25 + L, 25)], fill=color, width=5)
        draw.line([(25, 25), (25, 25 + L)], fill=color, width=5)
        draw.line([(w - 25, 25), (w - 25 - L, 25)], fill=color, width=5)
        draw.line([(w - 25, 25), (w - 25, 25 + L)], fill=color, width=5)
        draw.line([(25, h - 25), (25 + L, h - 25)], fill=color, width=5)
        draw.line([(25, h - 25), (25, h - 25 - L)], fill=color, width=5)
        draw.line([(w - 25, h - 25), (w - 25 - L, h - 25)], fill=color, width=5)
        draw.line([(w - 25, h - 25), (w - 25, h - 25 - L)], fill=color, width=5)


def generate_image_for_account(account_handle: str, theme_idx: int = 0, cycle_num: int = 1) -> str:
    """Menghasilkan satu gambar unik secara dinamis untuk akun apa pun dengan tema visual spesifik."""
    import time
    w, h = 1200, 675
    theme = THEME_PRESETS[theme_idx % len(THEME_PRESETS)]
    clean_handle = account_handle.lstrip("@").strip()

    img = Image.new("RGB", (w, h), color=theme["bg"])
    draw = ImageDraw.Draw(img)

    # 1. Background Pattern
    draw_pattern(draw, theme["pattern"], w, h, theme["primary"])

    # 2. Header Bar
    draw.rectangle([(40, 40), (w - 40, 90)], fill=theme["badge_bg"], outline=theme["primary"], width=1)
    draw.text((60, 52), f"● {theme['header']}", fill=theme["primary"])
    draw.text((w - 280, 52), f"VERIFIED: {TAG}", fill=(200, 210, 225))

    # 3. Big Main Title
    draw.text((60, 120), theme["title"], fill=(255, 255, 255))
    draw.line([(60, 160), (450, 160)], fill=theme["primary"], width=3)
    draw.text((60, 175), theme["subtitle"], fill=(180, 190, 205))

    # 4. Central Operator Badge Card
    card_top = 220
    card_h = 160
    draw.rectangle([(60, card_top), (w - 60, card_top + card_h)], fill=theme["badge_bg"], outline=(40, 50, 70), width=1)
    draw.line([(60, card_top), (60, card_top + card_h)], fill=theme["primary"], width=6)

    shift_num = abs(hash(f"{clean_handle}_{cycle_num}_{time.time()}")) % 9000 + 1000
    draw.text((85, card_top + 20), f"OPERATOR HANDLE : @{clean_handle}", fill=(255, 255, 255))
    draw.text((85, card_top + 55), f"SHIFT ASSIGNMENT: #SHILL-{shift_num}", fill=theme["primary"])
    draw.text((85, card_top + 90), f"CONSENSUS STATUS: {theme['status']}", fill=theme["secondary"])

    # Metric Badges
    box_w = 260
    box_x = w - 60 - box_w - 25
    draw.rectangle([(box_x, card_top + 20), (box_x + box_w, card_top + 65)], fill=(15, 20, 32), outline=theme["primary"], width=1)
    draw.text((box_x + 15, card_top + 33), "PROOF-OF-WORK CLOCK-IN", fill=(255, 255, 255))

    draw.rectangle([(box_x, card_top + 80), (box_x + box_w, card_top + 125)], fill=(15, 20, 32), outline=theme["secondary"], width=1)
    draw.text((box_x + 35, card_top + 93), "EVM ON-CHAIN YIELD", fill=theme["secondary"])

    # 5. Engagement Multiplier Bar
    bar_top = 405
    draw.rectangle([(60, bar_top), (w - 60, bar_top + 60)], fill=(12, 16, 24), outline=(30, 40, 60), width=1)
    metrics_text = "ENGAGEMENT MULTIPLIERS:  [ LIKE: +1 ]   [ REPLY: +2 ]   [ REPOST: +3 ]   [ MEDIA: +10 ]   [ IDENTIFIERS: +30 ]"
    draw.text((85, bar_top + 20), metrics_text, fill=(220, 230, 240))

    # 6. Bottom Identifiers Footer
    footer_top = 490
    footer_h = 135
    draw.rectangle([(60, footer_top), (w - 60, footer_top + footer_h)], fill=theme["badge_bg"], outline=theme["primary"], width=2)

    draw.text((85, footer_top + 20), f"OFFICIAL TICKER  : {TICKER}", fill=theme["primary"])
    draw.text((450, footer_top + 20), "PLATFORM: https://shill.money/clock-in", fill=(180, 195, 215))

    draw.text((85, footer_top + 55), "CONTRACT ADDRESS (EVM):", fill=(200, 210, 225))
    draw.text((85, footer_top + 85), CA, fill=theme["primary"])

    draw.rectangle([(w - 250, footer_top + 35), (w - 85, footer_top + 105)], fill=theme["primary"])
    draw.text((w - 225, footer_top + 60), "100% VERIFIED", fill=(0, 0, 0))

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
        # Dummy accounts fallback
        handles = [f"operator_{i}" for i in range(1, 9)]

    for idx, handle in enumerate(handles):
        out_path = generate_image_for_account(handle, idx)
        results[handle] = out_path
        preset = THEME_PRESETS[idx % len(THEME_PRESETS)]
        print(f"✓ Generated unique graphic for @{handle} [{preset['header']}] -> {Path(out_path).name}")

    return results


if __name__ == "__main__":
    generate_all_images()
