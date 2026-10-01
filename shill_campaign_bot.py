"""
Shill.Money Campaign Automation Bot
1. Task 1: Create unique promotional posts for all 8 accounts with attached images,
   ticker ($SHILL), CA (0x93cfF6Dc0cf59680b8d85b9F3312a24bF1a7c1D8), and @shillmoneyrh.
2. Task 2: Cross-Engagement Squad Raid:
   Every account interacts with all other accounts' posts:
   - Like ❤️ (+1)
   - Retweet 🔁 (+3)
   - Comment / Reply 💬 (+2)
"""

import asyncio
import json
import random
import re
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, BrowserContext, Page

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

from config import RESULTS_DIR
from accounts_manager import load_accounts, sync_active_cookies

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

CAMPAIGN_POSTS_FILE = RESULTS_DIR / "shill_campaign_posts.json"
CAMPAIGN_ENGAGEMENT_FILE = RESULTS_DIR / "shill_engagement_history.json"
SHILL_IMAGES_DIR = RESULTS_DIR / "shill_images"

TICKER = "$SHILL"
CA = "0x93cfF6Dc0cf59680b8d85b9F3312a24bF1a7c1D8"
TAG = "@shillmoneyrh"
URL = "https://shill.money/clock-in"

# 8 Postingan 100% Unik & Berbeda Sudut Pandang per Akun
POST_TEMPLATES = [
    (
        "Posts score highest when including complete identifiers (ticker, contract, and media), "
        "while scaling further through real discussion—like quotes and replies—plus transparent payout proofs.\n"
        f"{TAG}\n\n"
        f"Contract Address {TICKER}: {CA}"
    ),
    (
        "Social mining in Web3 done right. Real discussion, mutual squad quotes, and transparent creator paychecks beat passive spam.\n"
        f"Clocking in my shift at {URL}!\n\n"
        f"{TAG}\n"
        f"Contract Address {TICKER}: {CA}"
    ),
    (
        "Daily clock-in shift confirmed! Tracking every like, reply, repost, and quote on-chain.\n"
        f"Turn genuine reach into liquid yield at {URL}.\n\n"
        f"{TAG}\n"
        f"Contract Address {TICKER}: {CA}"
    ),
    (
        "Proof of Work meets SocialFi. The scoring algorithm rewards high-effort discussions and complete CA identifiers.\n"
        f"Securing my daily {TICKER} paycheck!\n\n"
        f"{TAG}\n"
        f"Contract Address {TICKER}: {CA}"
    ),
    (
        "Clock in, participate in authentic conversations, and claim your decentralized creator rewards.\n"
        f"Checking in my daily shift at {URL}!\n\n"
        f"{TAG}\n"
        f"Contract Address {TICKER}: {CA}"
    ),
    (
        "Why grind mindless farming when you can clock in with real discussion and get paid for measurable reach?\n"
        f"Squad shift active at {URL}!\n\n"
        f"{TAG}\n"
        f"Contract Address {TICKER}: {CA}"
    ),
    (
        "Decentralized wage distribution powered by smart contracts. Daily shift is officially open for creators.\n"
        "Every quote & repost counts!\n\n"
        f"{TAG}\n"
        f"Contract Address {TICKER}: {CA}"
    ),
    (
        f"Consistency is king in SocialFi. Just clocked in my daily shift on {URL}!\n"
        "Squad is active and pushing transparent creator rewards.\n\n"
        f"{TAG}\n"
        f"Contract Address {TICKER}: {CA}"
    )
]

# Bank Komentar / Replies yang Natural & Kontekstual
REPLY_TEMPLATES = [
    "Clocked in as well! The scoring math on $SHILL makes total sense. Let's push this reach! 🚀",
    "Real engagement beats bot spam every single time. Happy to support the shift! 🔥",
    "Transparency on the payout mechanics is exactly what CT needs. Validating this thread! 💯",
    "Verified shift entry! Mutual engagement scaling up the multipliers nicely @shillmoneyrh.",
    "Great breakdown of the clock-in incentives. Adding to the discussion volume for maximum score!",
    "Contract address verified and active. The decentralized attention economy is here with $SHILL!",
    "Logged in my hours too! Quotes and replies giving the strongest boost to the score. LFG!",
    "Squad is fully clocked in today. Authentic interaction always gets rewarded on-chain!"
]

# Bank Quote Tweets (Simple & Wajib Mencantumkan Contract address $SHILL: CA)
QUOTE_TEMPLATES = [
    f"Supporting this verified shift! 🚀\nContract address {TICKER}: {CA}",
    f"Clocked in and validating the squad thread! 🔥\nContract address {TICKER}: {CA}",
    f"Proof of work social mining active. LFG! ⚡\nContract address {TICKER}: {CA}",
    f"Amplifying genuine creator reach on-chain! 💎\nContract address {TICKER}: {CA}",
    f"Real discussion always beats bot spam. Clock in now! ⏰\nContract address {TICKER}: {CA}",
    f"Squad is fully clocked in and scaling reach! 📈\nContract address {TICKER}: {CA}",
    f"Active creator shift verified on-chain. Transparent rewards! ✨\nContract address {TICKER}: {CA}",
    f"Mutual engagement scaling up the multipliers nicely! 🎯\nContract address {TICKER}: {CA}"
]

def load_campaign_posts() -> dict:
    if not CAMPAIGN_POSTS_FILE.exists():
        return {}
    try:
        with open(CAMPAIGN_POSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_campaign_posts(posts: dict):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(CAMPAIGN_POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

def load_engagement_history() -> dict:
    if not CAMPAIGN_ENGAGEMENT_FILE.exists():
        return {}
    try:
        with open(CAMPAIGN_ENGAGEMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_engagement_record(account: str, target_tweet_id: str, action: str):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    hist = load_engagement_history()
    hist.setdefault(account, {})
    hist[account].setdefault(target_tweet_id, [])
    if action not in hist[account][target_tweet_id]:
        hist[account][target_tweet_id].append(action)
    with open(CAMPAIGN_ENGAGEMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)


async def post_shill_tweet(
    page: Page,
    account_name: str,
    tweet_text: str,
    image_path: str
) -> tuple[bool, str, str]:
    """Membuat dan memposting tweet baru dengan lampiran gambar."""
    created_tweet_id = None

    async def on_response(response):
        nonlocal created_tweet_id
        if "CreateTweet" in response.url:
            try:
                raw_text = await response.text()
                m = re.search(r'"rest_id"\s*:\s*"(\d+)"', raw_text)
                if m:
                    created_tweet_id = m.group(1)
                else:
                    res_json = json.loads(raw_text)
                    res = res_json.get("data", {}).get("create_tweet", {}).get("tweet_results", {}).get("result", {})
                    if res and res.get("rest_id"):
                        created_tweet_id = res.get("rest_id")
            except Exception:
                pass

    page.on("response", on_response)

    try:
        print(f"  {CYAN}🌐 Membuka timeline https://x.com/home...{RESET}", flush=True)
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=40000)
        await asyncio.sleep(2)

        if "login" in page.url or "i/flow/login" in page.url:
            return False, "", "Sesi login kedaluwarsa."

        # Buka modal komposer via SideNav_NewTweet_Button
        print(f"  {YELLOW}📝 Membuka jendela komposer tweet...{RESET}", flush=True)
        post_btn = page.locator('[data-testid="SideNav_NewTweet_Button"], a[href="/compose/post"]').first
        try:
            await post_btn.wait_for(state="visible", timeout=35000)
            await post_btn.click()
            await asyncio.sleep(1.5)
        except Exception:
            pass

        # Target dialog modal jika ada, atau fallback ke root page
        dialog = page.locator('div[role="dialog"]').first
        target_container = dialog if await dialog.count() > 0 else page

        # Tunggu textarea komposer muncul
        textarea = target_container.locator('[data-testid="tweetTextarea_0"]').first
        await textarea.wait_for(state="visible", timeout=20000)

        # 1. Upload Gambar jika ada
        if image_path and Path(image_path).exists():
            print(f"  {YELLOW}🖼️  Mengunggah gambar grafis $SHILL: {Path(image_path).name}...{RESET}", flush=True)
            file_input = target_container.locator('input[data-testid="fileInput"]').first
            if await file_input.count() > 0:
                await file_input.set_input_files(image_path)
                # Tunggu preview gambar termuat
                try:
                    await target_container.locator('[data-testid="attachments"]').wait_for(state="visible", timeout=15000)
                    print(f"  {GREEN}✓ Gambar berhasil terunggah dan terlampir!{RESET}", flush=True)
                except Exception:
                    print(f"  {YELLOW}Notice: Preview lampiran sedang diproses...{RESET}", flush=True)
                await asyncio.sleep(2)

        # 2. Tulis Teks Tweet
        print(f"  {YELLOW}✍️  Mengetik konten promosi kampanye $SHILL...{RESET}", flush=True)
        await textarea.click(force=True)
        await asyncio.sleep(0.5)
        await textarea.fill(tweet_text)
        await asyncio.sleep(1.0)

        # Trigger lexical change agar state React membaca teks
        await textarea.press("End")
        await textarea.type(" ")
        await textarea.press("Backspace")
        await asyncio.sleep(0.8)

        # Tutup autocomplete jika ada
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.8)

        # 3. Klik Tombol Kirim / Post di dalam dialog
        send_btn = target_container.locator('[data-testid="tweetButton"]').first
        await send_btn.wait_for(state="visible", timeout=10000)

        for _ in range(15):
            if await send_btn.is_enabled():
                break
            await asyncio.sleep(0.5)

        if await send_btn.is_enabled():
            print(f"  {YELLOW}🚀 Mengirim tweet ke timeline...{RESET}", flush=True)
            try:
                await send_btn.dispatch_event("click")
            except Exception:
                await send_btn.click(force=True)
        else:
            print(f"  {YELLOW}🚀 Mengirim via Ctrl+Enter...{RESET}", flush=True)
            await textarea.focus()
            await page.keyboard.press("Control+Enter")

        # Tunggu konfirmasi CreateTweet
        for _ in range(15):
            if created_tweet_id:
                break
            await asyncio.sleep(1.0)

        if not created_tweet_id:
            # Fallback 1: Cek toast popup
            try:
                toast_link = page.locator('[data-testid="toast"] a[href*="/status/"]').first
                if await toast_link.count() > 0:
                    href = await toast_link.get_attribute("href")
                    if href and "/status/" in href:
                        created_tweet_id = href.strip("/").split("/status/")[1].split("?")[0]
            except Exception:
                pass

        if not created_tweet_id:
            # Fallback 2: Buka profile untuk cek tweet teratas yang mengandung $SHILL
            try:
                print(f"  {YELLOW}Memverifikasi tweet terbaru di profil @{account_name}...{RESET}", flush=True)
                await page.goto(f"https://x.com/{account_name}", wait_until="domcontentloaded", timeout=25000)
                await asyncio.sleep(3)
                tweets = await page.locator('article[data-testid="tweet"]').all()
                for tw in tweets[:5]:
                    text_content = await tw.inner_text()
                    if "$SHILL" in text_content or "0x93cf" in text_content:
                        link_el = tw.locator('a[href*="/status/"]').first
                        if await link_el.count() > 0:
                            href = await link_el.get_attribute("href")
                            if href and "/status/" in href:
                                created_tweet_id = href.strip("/").split("/status/")[1].split("?")[0]
                                break
            except Exception:
                pass

        if not created_tweet_id:
            return False, "", "Gagal menangkap ID tweet yang terkirim."

        tweet_url = f"https://x.com/{account_name}/status/{created_tweet_id}"
        return True, created_tweet_id, tweet_url

    except Exception as e:
        return False, "", str(e)


async def execute_tweet_engagement(
    page: Page,
    author: str,
    tweet_id: str,
    tweet_url: str,
    current_account: str,
    reply_text: str,
    quote_text: str = ""
) -> dict:
    """Melakukan Like, Retweet, Quote, dan Reply/Komentar pada postingan target."""
    res = {"liked": False, "retweeted": False, "quoted": False, "replied": False}

    try:
        print(f"  {CYAN}🎯 Mengunjungi tweet @{author} ({tweet_url})...{RESET}", flush=True)
        await page.goto(tweet_url, wait_until="domcontentloaded", timeout=35000)
        await asyncio.sleep(2.0)

        # Tunggu tombol aksi tweet ter-mount secara sempurna di DOM
        try:
            action_anchor = page.locator('button[data-testid="like"], button[data-testid="unlike"]').first
            await action_anchor.wait_for(state="visible", timeout=15000)
        except Exception:
            pass

        # 1. LIKE ❤️ (+1 Poin)
        try:
            unlike_btn = page.locator('button[data-testid="unlike"]').first
            if await unlike_btn.count() > 0:
                print(f"    ❤️  Like   : Sudah di-like sebelumnya ✓", flush=True)
                res["liked"] = True
            else:
                like_btn = page.locator('button[data-testid="like"]').first
                if await like_btn.count() > 0:
                    await like_btn.scroll_into_view_if_needed()
                    await asyncio.sleep(0.5)
                    await like_btn.click(force=True)
                    await asyncio.sleep(1.5)
                    if await page.locator('button[data-testid="unlike"]').count() > 0:
                        print(f"    ❤️  Like   : {GREEN}✓ Berhasil Like (+1 Poin){RESET}", flush=True)
                        res["liked"] = True
                        save_engagement_record(current_account, tweet_id, "LIKE")
        except Exception as e:
            print(f"    ❤️  Like   : {YELLOW}Notice ({e}){RESET}", flush=True)

        await asyncio.sleep(random.uniform(2.0, 3.5))

        # 2. QUOTE TWEET 🔁💬 (+Poin Tertinggi)
        if quote_text:
            try:
                hist = load_engagement_history()
                account_history = hist.get(current_account, {}).get(tweet_id, [])
                if "QUOTE" in account_history:
                    print(f"    🔁💬 Quote  : Sudah di-quote sebelumnya ✓", flush=True)
                    res["quoted"] = True
                else:
                    rt_btn = page.locator('button[data-testid="retweet"]').first
                    if await rt_btn.count() > 0:
                        await rt_btn.scroll_into_view_if_needed()
                        await rt_btn.click(force=True)
                        await asyncio.sleep(1.0)

                        quote_opt = page.locator('a[href*="/compose/post"], a[href*="/compose/quote"], div[role="menuitem"]:has-text("Quote")').first
                        if await quote_opt.count() > 0:
                            await quote_opt.click(force=True)
                            await asyncio.sleep(1.5)

                            dialog = page.locator('div[role="dialog"]').first
                            if await dialog.count() > 0:
                                q_textarea = dialog.locator('[data-testid="tweetTextarea_0"]').first
                                await q_textarea.wait_for(state="visible", timeout=10000)
                                await q_textarea.fill(quote_text)
                                await asyncio.sleep(0.8)
                                await q_textarea.press("End")
                                await q_textarea.type(" ")
                                await q_textarea.press("Backspace")
                                await asyncio.sleep(0.5)

                                q_send_btn = dialog.locator('[data-testid="tweetButton"]').first
                                if await q_send_btn.count() > 0 and await q_send_btn.is_enabled():
                                    try:
                                        await q_send_btn.dispatch_event("click")
                                    except Exception:
                                        await q_send_btn.click(force=True)
                                    await asyncio.sleep(2.5)
                                    print(f"    🔁💬 Quote  : {GREEN}✓ Berhasil Quote Tweet (+Poin Multiplier){RESET}", flush=True)
                                    print(f"       Preview: \"{quote_text.splitlines()[0]}...\"", flush=True)
                                    res["quoted"] = True
                                    save_engagement_record(current_account, tweet_id, "QUOTE")
                        else:
                            await page.keyboard.press("Escape")
            except Exception as e:
                print(f"    🔁💬 Quote  : {YELLOW}Notice ({e}){RESET}", flush=True)
                try:
                    await page.keyboard.press("Escape")
                except Exception:
                    pass

            await asyncio.sleep(random.uniform(2.0, 3.5))

        # 3. RETWEET / REPOST 🔁 (+3 Poin)
        try:
            unrt_btn = page.locator('button[data-testid="unretweet"]').first
            if await unrt_btn.count() > 0:
                print(f"    🔁 Retweet: Sudah di-retweet sebelumnya ✓", flush=True)
                res["retweeted"] = True
            else:
                rt_btn = page.locator('button[data-testid="retweet"]').first
                if await rt_btn.count() > 0:
                    await rt_btn.scroll_into_view_if_needed()
                    await asyncio.sleep(0.5)
                    await rt_btn.click(force=True)
                    await asyncio.sleep(1.0)
                    confirm_btn = page.locator('[data-testid="retweetConfirm"]').first
                    if await confirm_btn.count() > 0:
                        await confirm_btn.click(force=True)
                        await asyncio.sleep(1.5)
                        if await page.locator('button[data-testid="unretweet"]').count() > 0:
                            print(f"    🔁 Retweet: {GREEN}✓ Berhasil Repost (+3 Poin){RESET}", flush=True)
                            res["retweeted"] = True
                            save_engagement_record(current_account, tweet_id, "RETWEET")
        except Exception as e:
            print(f"    🔁 Retweet: {YELLOW}Notice ({e}){RESET}", flush=True)

        await asyncio.sleep(random.uniform(2.0, 3.5))

        # 4. REPLY / COMMENT 💬 (+2 Poin)
        try:
            reply_area = page.locator('[data-testid="tweetTextarea_0"]').first
            if await reply_area.count() > 0:
                await reply_area.scroll_into_view_if_needed()
                await reply_area.click(force=True)
                await asyncio.sleep(0.5)
                await reply_area.fill(reply_text)
                await asyncio.sleep(1.0)
                await reply_area.press("End")
                await reply_area.type(" ")
                await reply_area.press("Backspace")
                await asyncio.sleep(0.5)

                reply_send = page.locator('[data-testid="tweetButtonInline"]').first
                if await reply_send.count() > 0 and await reply_send.is_enabled():
                    await reply_send.click(force=True)
                    await asyncio.sleep(2.5)
                    print(f"    💬 Reply  : {GREEN}✓ Berhasil Kirim Komentar (+2 Poin){RESET}", flush=True)
                    print(f"       Preview: \"{reply_text[:60]}...\"", flush=True)
                    res["replied"] = True
                    save_engagement_record(current_account, tweet_id, "REPLY")
        except Exception as e:
            print(f"    💬 Reply  : {YELLOW}Notice ({e}){RESET}", flush=True)

    except Exception as e:
        print(f"  {RED}Error interaksi tweet: {e}{RESET}", flush=True)

    return res


async def run_campaign_pipeline(cycle_num: int = 1):
    accs_data = load_accounts()
    all_accounts = [
        v for k, v in accs_data.get("accounts", {}).items()
        if not v.get("suspended") and v.get("auth_token") and v.get("ct0")
    ]

    print(f"""{CYAN}{BOLD}
╔═══════════════════════════════════════════════════════════════╗
║         🚀 SHILL.MONEY CLOCK-IN CAMPAIGN BOT                  ║
║   1. Pembuatan Postingan Unik (Akun Terpilih) + Media Grafis  ║
║   2. Saling Interaksi Silang: Like ❤️ Quote 🔁💬 Retweet 🔁 Reply 💬 ║
╚═══════════════════════════════════════════════════════════════╝{RESET}""")

    posters = [a for a in all_accounts if a.get("can_post", True)]
    engagers = [a for a in all_accounts if not a.get("can_post", True)]
    print(f"Total Akun Terlibat: {len(all_accounts)} Akun Aktif (Poster: {len(posters)}, Engager Only: {len(engagers)})\n")

    # =========================================================================
    # PHASE 1: POSTING TWEET UNIK KE SEMUA AKUN
    # =========================================================================
    print(f"{MAGENTA}{BOLD}================================================================{RESET}")
    print(f"{MAGENTA}{BOLD}📢 FASE 1: MEMBUAT POSTINGAN KAMPANYE $SHILL UNTUK AKUN TERPILIH{RESET}")
    print(f"{MAGENTA}{BOLD}================================================================{RESET}\n")

    posts = load_campaign_posts()

    for idx, acc in enumerate(all_accounts, 1):
        uname = acc.get("screen_name", "")
        clean_name = uname.lstrip("@").strip()

        print(f"{CYAN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{CYAN}{BOLD}▶ [{idx}/{len(all_accounts)}] Akun: @{clean_name}{RESET}")
        print(f"{CYAN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

        if not acc.get("can_post", True):
            print(f"  {YELLOW}⏩ Akun @{clean_name} dilewati dari pembuatan postingan (Mode: Engager Only).{RESET}\n")
            continue

        if clean_name in posts and posts[clean_name].get("tweet_url"):
            print(f"  {GREEN}✓ Akun @{clean_name} sudah memposting sebelumnya: {posts[clean_name]['tweet_url']}{RESET}\n")
            continue

        base_template = POST_TEMPLATES[(idx - 1) % len(POST_TEMPLATES)]
        tweet_content = base_template

        image_file = SHILL_IMAGES_DIR / f"shill_{clean_name}.png"
        if not image_file.exists():
            from generate_shill_images import generate_image_for_account
            generate_image_for_account(clean_name, idx - 1)

        # Luncurkan browser untuk akun ini
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                channel="chrome",
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = await browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )

            await context.add_cookies([
                {"name": "auth_token", "value": acc["auth_token"], "domain": ".x.com", "path": "/"},
                {"name": "ct0", "value": acc["ct0"], "domain": ".x.com", "path": "/"},
                {"name": "auth_token", "value": acc["auth_token"], "domain": ".twitter.com", "path": "/"},
                {"name": "ct0", "value": acc["ct0"], "domain": ".twitter.com", "path": "/"}
            ])

            page = await context.new_page()

            ok, t_id, t_url = await post_shill_tweet(
                page=page,
                account_name=clean_name,
                tweet_text=tweet_content,
                image_path=str(image_file.resolve()) if image_file.exists() else ""
            )

            await browser.close()

            if ok:
                posts[clean_name] = {
                    "account": clean_name,
                    "tweet_id": t_id,
                    "tweet_url": t_url,
                    "posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text": tweet_content
                }
                save_campaign_posts(posts)
                print(f"  {GREEN}{BOLD}🎉 Postingan Berhasil Dipublikasikan!{RESET}")
                print(f"  🔗 Link Tweet: {CYAN}{t_url}{RESET}\n")
            else:
                print(f"  {RED}❌ Gagal memposting untuk @{clean_name}: {t_url}{RESET}\n")

        # Jeda alami antar posting akun
        if idx < len(all_accounts):
            wait_s = random.randint(15, 25)
            print(f"{YELLOW}⏳ Jeda alami {wait_s} detik sebelum akun berikutnya memposting...{RESET}\n")
            await asyncio.sleep(wait_s)

    # Filter target postingan hanya dari akun pembuat postingan aktif
    allowed_poster_names = {
        a.get("screen_name", "").lstrip("@").strip().lower()
        for a in all_accounts if a.get("can_post", True)
    }
    raid_targets = {k: v for k, v in posts.items() if k.lower() in allowed_poster_names}

    print(f"\n{GREEN}{BOLD}================================================================{RESET}")
    print(f"{GREEN}{BOLD}🎉 FASE 1 SELESAI: {len(raid_targets)} Postingan Siap di-Raid!{RESET}")
    print(f"{GREEN}{BOLD}================================================================{RESET}\n")

    # =========================================================================
    # PHASE 2: MUTUAL CROSS-ENGAGEMENT (RAID SQUAD)
    # =========================================================================
    print(f"{MAGENTA}{BOLD}================================================================{RESET}")
    print(f"{MAGENTA}{BOLD}🔥 FASE 2: CROSS-ENGAGEMENT RAID (LIKE, QUOTE, RETWEET, REPLY){RESET}")
    print(f"{MAGENTA}{BOLD}================================================================{RESET}\n")

    for acc_idx, acc in enumerate(all_accounts, 1):
        uname = acc.get("screen_name", "")
        clean_name = uname.lstrip("@").strip()

        print(f"\n{CYAN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        print(f"{CYAN}{BOLD}▶ [{acc_idx}/{len(all_accounts)}] Mengoperasikan Akun: @{clean_name} untuk Raid{RESET}")
        print(f"{CYAN}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

        # Target tweet adalah tweet dari AKUN LAIN
        other_posts = [p_data for a_name, p_data in raid_targets.items() if a_name.lower() != clean_name.lower()]

        if not other_posts:
            print(f"  {YELLOW}Tidak ada postingan dari akun lain untuk di-engage.{RESET}")
            continue

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                channel="chrome",
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = await browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )

            await context.add_cookies([
                {"name": "auth_token", "value": acc["auth_token"], "domain": ".x.com", "path": "/"},
                {"name": "ct0", "value": acc["ct0"], "domain": ".x.com", "path": "/"},
                {"name": "auth_token", "value": acc["auth_token"], "domain": ".twitter.com", "path": "/"},
                {"name": "ct0", "value": acc["ct0"], "domain": ".twitter.com", "path": "/"}
            ])

            page = await context.new_page()

            for p_idx, target_p in enumerate(other_posts, 1):
                target_author = target_p["account"]
                target_id = target_p["tweet_id"]
                target_url = target_p["tweet_url"]

                # Pilih template reply dan quote acak
                chosen_reply = random.choice(REPLY_TEMPLATES)
                chosen_quote = random.choice(QUOTE_TEMPLATES)

                print(f"  [{p_idx}/{len(other_posts)}] Menyerang tweet @{target_author}...")
                await execute_tweet_engagement(
                    page=page,
                    author=target_author,
                    tweet_id=target_id,
                    tweet_url=target_url,
                    current_account=clean_name,
                    reply_text=chosen_reply,
                    quote_text=chosen_quote
                )

                if p_idx < len(other_posts):
                    inter_wait = random.randint(8, 16)
                    print(f"    ⏳ Jeda alami antar interaksi {inter_wait} detik...\n")
                    await asyncio.sleep(inter_wait)

            await browser.close()

        if acc_idx < len(all_accounts):
            acc_wait = random.randint(20, 35)
            print(f"\n{YELLOW}💤 Jeda istirahat akun {acc_wait} detik sebelum beralih ke akun berikutnya...{RESET}\n")
            await asyncio.sleep(acc_wait)

    print(f"\n{GREEN}{BOLD}╔═══════════════════════════════════════════════════════════════╗")
    print(f"║       🎉 SELURUH TAHAP SIKLUS KAMPANYE TELAH TUNTAS!          ║")
    print(f"║  • Postingan Unik Terbit dengan Gambar, Ticker & CA          ║")
    print(f"║  • Semua Akun Saling Like, Quote, Retweet & Reply Komentar          ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝{RESET}\n")


async def run_continuous_campaign(min_delay_minutes: int = 5, max_delay_minutes: int = 10):
    """Menjalankan seluruh siklus kampanye secara terus-menerus dengan jeda acak 5-10 menit antar siklus."""
    cycle = 1
    while True:
        print(f"\n{MAGENTA}{BOLD}╔═══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{MAGENTA}{BOLD}║         🚀 MEMULAI SIKLUS KAMPANYE SHILL #{cycle:<4}                ║{RESET}")
        print(f"{MAGENTA}{BOLD}╚═══════════════════════════════════════════════════════════════╝{RESET}\n")

        await run_campaign_pipeline(cycle_num=cycle)

        # Hitung jeda acak antar siklus (5 hingga 10 menit)
        cycle_delay_seconds = random.randint(min_delay_minutes * 60, max_delay_minutes * 60)
        delay_minutes_display = cycle_delay_seconds / 60

        print(f"\n{YELLOW}{BOLD}================================================================{RESET}")
        print(f"{YELLOW}{BOLD}⏳ SIKLUS #{cycle} SELESAI SEMPURNA!{RESET}")
        print(f"{YELLOW}{BOLD}💤 Memulai jeda istirahat siklus selama {delay_minutes_display:.1f} MENIT ({cycle_delay_seconds} detik)...{RESET}")
        print(f"{YELLOW}{BOLD}================================================================{RESET}\n")

        # Arsipkan postingan siklus ini dan bersihkan untuk siklus berikutnya
        current_posts = load_campaign_posts()
        if current_posts:
            archive_file = RESULTS_DIR / f"shill_posts_cycle_{cycle}.json"
            try:
                with open(archive_file, "w", encoding="utf-8") as f:
                    json.dump(current_posts, f, indent=2, ensure_ascii=False)
            except Exception:
                pass
            save_campaign_posts({})

        # Hitung mundur jeda siklus
        for remaining in range(cycle_delay_seconds, 0, -60):
            mins = remaining // 60
            if mins % 5 == 0 or mins <= 3:
                print(f"  [Sleep Timer] Sisa jeda siklus: {mins} menit menuju Siklus #{cycle + 1}...", flush=True)
            await asyncio.sleep(min(60, remaining))

        cycle += 1


if __name__ == "__main__":
    asyncio.run(run_continuous_campaign(min_delay_minutes=5, max_delay_minutes=10))

