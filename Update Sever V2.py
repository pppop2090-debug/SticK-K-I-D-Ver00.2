import time
import sys
import random
import select
import os
import json
import requests
import webbrowser
from colorama import Fore, Back, Style, init

# Khởi tạo thư viện màu sắc
init(autoreset=True)

# ==========================================================================
# HỆ THỐNG KHÓA PHIÊN BẢN CŨ TỪ XA (ĐÃ CẬP NHẬT LOGIC)
# ==========================================================================
CURRENT_VERSION = "1.0.3"

def force_update_check():
    try:
        # Thêm tham số t=time.time() để tránh cache của GitHub/Trình duyệt
        url = "https://raw.githubusercontent.com/pppop2090-debug/SticK-K-I-D-Ver00.2/refs/heads/main/version.json?t=" + str(time.time())
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            latest = str(data['latest_version']).strip()
            current = str(CURRENT_VERSION).strip()
            
            # Logic: Nếu phiên bản trên web khác phiên bản hiện tại thì bắt buộc cập nhật
            if latest != current:
                clear_screen()
                print(f"{Fore.RED}{Style.BRIGHT}================================================")
                print(f"{Fore.YELLOW}   [!] HỆ THỐNG YÊU CẦU CẬP NHẬT PHIÊN BẢN MỚI")
                print(f"{Fore.CYAN}   [!] Phiên bản hiện tại: {current}")
                print(f"{Fore.GREEN}   [!] Phiên bản bắt buộc: {latest}")
                print("-" * 48)
                print(f"{Fore.WHITE}   Hệ thống sẽ tự động mở trang tải xuống...")
                print(f"{Fore.MAGENTA}   {data['update_url']}")
                print(f"{Fore.RED}{Style.BRIGHT}================================================")
                webbrowser.open(data['update_url'])
                while True:
                    input(f"{Fore.RED}[KHÓA] BẤM ENTER ĐỂ THỬ LẠI HOẶC TẢI BẢN MỚI...")
                    force_update_check()
    except Exception as e:
        # Nếu có lỗi kết nối, vẫn cho phép người dùng vào app
        print(f"{Fore.RED}[!] Không thể kết nối máy chủ update: {e}")

# Gọi hàm kiểm tra ngay khi mở app
force_update_check()

def check_for_updates():
    try:
        github_url = "https://raw.githubusercontent.com/pppop2090-debug/SticK-K-I-D-Ver00.2/refs/heads/main/Update%20Sever%20V2.py"
        response = requests.get(github_url, timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[!] Hệ thống đã kiểm tra: Đang sử dụng phiên bản mới nhất.")
    except:
        print(f"{Fore.RED}[!] Không thể kết nối tới máy chủ cập nhật GitHub.")

# ==========================================================================
# KHỞI TẠO DỮ LIỆU CŨ (GIỮ NGUYÊN)
# ==========================================================================
SYSTEM_COMMANDS = {f"CMD_{i}": f"SYSTEM_EXECUTE_TASK_{i:03d}" for i in range(1, 531)}
SELECTED_DEVICE = "UNKNOWN"
REQUIRED_VIP_KEY = "testkey"
CHAT_ACCESS_KEYS = ["SAMPKEY", "SAMPTX"]
USER_DATA_FILE = "user_config.json"

def load_account_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"username": "admin", "password": "admintest"}

DATABASE_ACCOUNT = load_account_data()
CURRENT_USER = ""
IS_ADMIN = False
HAS_CHAT_ACCESS = False

ADMIN_RESPONSES = ["Để nhận file mod mới nhất, e check mail hoặc ib trực tiếp Fanpage nhé!", "Bên a có hỗ trợ cài qua UltraViewer, cần thì nhắn a nha.", "Bản này tối ưu cho iOS 15+, ae cứ yên tâm sử dụng.", "Sv đang bảo trì định kỳ, ae đợi tầm 30p là vào đc thui.", "Key VIP vĩnh viễn, dùng thoải mái k giới hạn thiết bị nhé.", "Check lại mạng đi ông, thường do đường truyền bên ông đó.", "A đang update thêm AIMBOT 2026, tối nay có bản mới nha.", "Đừng chia sẻ Key VIP cho lạ, kẻo bay acc hệ thống đó.", "Có vđề j cứ chụp màn hình gửi qua Zalo, a rep nhanh lém.", "Bản này chạy mượt trên Android 11, lỗi thì xóa cache game nhé.", "Ib a gửi file hướng dẫn cài đặt từ A-Z cho, đơn giản lém.", "Đang fix lỗi văng game ở phiên bản mới, ae đợi tí nhé.", "Bản mod này k bị quét đâu, tui test kĩ rồi mới share.", "Cần hỗ trợ trực tiếp thì call a số hotline nha, a rảnh suốt.", "Ae dùng bản này né ban hiệu quả, đừng dùng quá đà là đc.", "Vừa đẩy thêm 1 bản update fix lag, check link ở web nhé.", "Đã nhận đc tin nhắn, tí nữa a rep từng bạn nha, thông cảm.", "Cứ làm đúng theo hướng dẫn là k lỗi đâu, đừng táy máy nhé.", "Bản này hỗ trợ cả giả lập nhé, mượt lém.", "Uy tín luôn, làm ăn là phải lâu dài, ae yên tâm nhé!"]
FAKE_USER_DB = [("Pro_SAMP", "Ae check phiên 882 chưa, thấy cầu 1-2-1 đẹp vãi.", Fore.CYAN), ("Girl_Xinh", "Ai có link mod skin FF k cho e xin vs, e luv mng.", Fore.MAGENTA), ("Hack_Tool_Vip", "Tool bản này chạy mượt, 0 sợ bay màu acc nhé.", Fore.GREEN), ("Newbie_99", "Cho e hỏi làm sao để bật đc mod xuyên tường v ạ?", Fore.WHITE), ("Cuong_FF", "Cứ chọn mục [A] r bật ESP là nhìn thấy địch hết.", Fore.YELLOW), ("Thien_Ha_Vo_Dich", "Hôm nay server lag thế nhỉ, ae có bị k?", Fore.RED), ("Gaming_Pro", "Do đường truyền bên mạng của ông đấy, t vẫn bắn ầm ầm.", Fore.BLUE), ("WeChat_Addict", "Add wechat anh THH PHAYY ở đâu ấy nhỉ mn?", Fore.LIGHTGREEN_EX), ("Tai_Xiu_Thu", "Vừa húp 5 tay Tài, ae theo t k?", Fore.LIGHTCYAN_EX), ("Anti_Ban_User", "Dùng bản này né quét file hệ thống tốt cực.", Fore.WHITE), ("iOS_User", "E dùng iPhone mà cài khó quá, admin hỗ trợ e vs.", Fore.LIGHTBLUE_EX), ("FF_Pro_Player", "Đã đạt Top 1 rank nhờ tool, uy tín nhé.", Fore.LIGHTMAGENTA_EX), ("Hacker_Muon_Thua", "Ae ơi, có cách nào bypass lỗi kết nối server k?", Fore.LIGHTYELLOW_EX), ("Lazy_Boy", "Chỉ cần bật Auto Ghim Tâm là xong, khỏe re.", Fore.CYAN), ("Admin_Fan_Club", "Admin ơi khi nào ra bản update AIMBOT mới v?", Fore.MAGENTA)]
ADMIN_THH = {"NAME": "THH PHAYY", "PHONE": "0362454241", "FACEBOOK": "FB.COM/THHPHAYY.OFFICIAL", "EMAIL": "THHPHAYY.CONTACT@GMAIL.COM", "WECHAT": "THHPHAYY_AMB"}
ADMIN_BNHUU = {"NAME": "TRPHH BNHUU", "PHONE": "0987" + str(random.randint(100000, 999999)), "FACEBOOK": "FB.COM/TRPHH.BNHUU.OFFICIAL", "EMAIL": "TRPHHBNHUU.BUSINESS@GMAIL.COM", "WECHAT": "BNHUU_TRPHH99"}
RAINBOW_COLORS = [Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX]
BIG_NUMBERS = {5: ["██████████", "██        ", "██████████", "        ██", "██████████"], 4: ["██       ██", "██       ██", "██████████", "        ██", "        ██"], 3: ["██████████", "        ██", "██████████", "        ██", "██████████"], 2: ["██████████", "        ██", "██████████", "██        ", "██████████"], 1: ["    ██    ", "  ████    ", "    ██    ", "    ██    ", "  ██████  "]}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_delay(text, delay=0.004, color=Fore.GREEN):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_update_banner():
    text = "S T I C K I D V1.0.3 UPDATE BY - THH PHAYY"
    for _ in range(2):
        for i in range(len(RAINBOW_COLORS)):
            sys.stdout.write("\r" + RAINBOW_COLORS[i] + Style.BRIGHT + text)
            sys.stdout.flush()
            time.sleep(0.15)
    print("\n" + "="*75)

def print_rgb_flashing_text(text_to_print, duration_loops=30):
    text_to_print = text_to_print.upper()
    for loop in range(duration_loops):
        sys.stdout.write("\r   ")
        for idx, char in enumerate(text_to_print):
            color_idx = (idx - loop) % len(RAINBOW_COLORS)
            sys.stdout.write(f"{RAINBOW_COLORS[color_idx]}{Style.BRIGHT}{char}")
        sys.stdout.flush()
        time.sleep(0.04)
    print()

def get_flashing_rainbow_text(text):
    return f"{random.choice(RAINBOW_COLORS)}{Style.BRIGHT}[{text}]"

def progress_bar(task_name, duration=1.0):
    steps = 15
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        bar = '█' * i + '░' * (steps - i)
        sys.stdout.write(f"\r{Fore.YELLOW}[{bar}] {percent}% | {task_name}")
        sys.stdout.flush()
        time.sleep(duration / steps)
    print(f"\n{Fore.GREEN}[OK] Hoàn tất tiến trình!\n")

def check_device_root_status():
    clear_screen()
    print(f"{Fore.RED}{Style.BRIGHT}================================================")
    print_rgb_flashing_text("HỆ THỐNG KIỂM TRA BẢO MẬT ROOT", duration_loops=20)
    print(f"{Fore.RED}{Style.BRIGHT}================================================")
    print(f"{Fore.YELLOW}[!] TRẠNG THÁI: THIẾT BỊ CHƯA ĐƯỢC ROOT!")
    print(f"{Fore.RED}[!] YÊU CẦU: VUI LÒNG CẤP QUYỀN ROOT ĐỂ TIẾP TỤC.")
    confirm = input(f"\n{Fore.CYAN}➔ BẠN ĐÃ CẤP QUYỀN ROOT CHƯA? (Y/N): ").strip().upper()
    if confirm == 'Y':
        clear_screen()
        hack_commands = ["su", "mount -o remount,rw /system", "chmod 777 /data/local/tmp", "insmod /system/lib/modules/root.ko", "bypass_selinux_enforcing -> permissive", "verifying_integrity...", "patching_kernel_binary...", "injecting_magisk_daemon...", "syncing_root_state...", "finalizing_root_access_privileges...", "re-mounting_partition..."]
        print(f"{Fore.GREEN}{Style.BRIGHT}--- ĐANG THIẾT LẬP KẾT NỐI ROOT (PRO_MODE) ---")
        for cmd in hack_commands:
            print(f"{Fore.WHITE}root@system:~# {Fore.LIGHTCYAN_EX}{cmd}")
            time.sleep(random.uniform(0.3, 0.7))
        progress_bar("ĐANG XÁC THỰC GÓI TIN", 1.0)
        print(f"\n{Fore.GREEN}{Style.BRIGHT}================================================")
        print(f"{Fore.CYAN}  [+] THIẾT BỊ ĐÃ ĐƯỢC ROOT THÀNH CÔNG!")
        print(f"{Fore.YELLOW}  [!] PHIÊN CẤP QUYỀN: 30 PHÚT ĐÃ ĐƯỢC KÍCH HOẠT")
        print(f"{Fore.GREEN}{Style.BRIGHT}================================================")
        time.sleep(2)
        return True
    else:
        print(f"\n{Fore.RED}[!] HỆ THỐNG ĐÌNH CHỈ TRUY CẬP DO THIẾU QUYỀN!")
        time.sleep(2)
        return False

def run_game_booster():
    booster_features = {"1": {"name": "CPU_OVERCLOCK_CORE_MAX", "status": "OFF"}, "2": {"name": "GPU_RENDERING_BOOST", "status": "OFF"}, "3": {"name": "RAM_CACHE_CLEANING", "status": "OFF"}, "4": {"name": "PING_STABILIZER_MODE", "status": "OFF"}, "5": {"name": "THERMAL_CONTROL_FORCE", "status": "OFF"}, "6": {"name": "VULKAN_API_OPTIMIZATION", "status": "OFF"}, "7": {"name": "FRAME_LIMIT_BYPASS_60FPS", "status": "OFF"}, "8": {"name": "NETWORK_JITTER_REDUCTION", "status": "OFF"}, "9": {"name": "BATTERY_DRAIN_THROTTLING", "status": "OFF"}, "0": {"name": "DPI_RESOLUTION_SCALING", "status": "OFF"}}
    while True:
        clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}{Style.BRIGHT}║             GAME TURBO ULTRA - 2026                    ║")
        print(f"{Fore.CYAN}{Style.BRIGHT}╚══════════════════════════════════════════════════════════╝")
        print(f"{Fore.YELLOW}  [STATUS]: READY | [DEVICE]: {SELECTED_DEVICE} | [ENGINE]: V8.0")
        print("-" * 60)
        for k, v in booster_features.items():
            color = Fore.GREEN if v["status"] == "ON" else Fore.RED
            print(f"  {Fore.WHITE}[{k}] {v['name']:<25} | {color}{Style.BRIGHT}{v['status']}")
        print("-" * 60)
        print(f"{Fore.WHITE}  [A] ENABLE ALL FEATURES\n  [E] EXECUTE OPTIMIZATION ENGINE\n  [Q] EXIT TO DASHBOARD")
        choice = input(f"\n{Fore.LIGHTYELLOW_EX}➔ INPUT_COMMAND: ").strip().upper()
        if choice in booster_features:
            booster_features[choice]["status"] = "ON"
        elif choice == "A":
            for k in booster_features:
                booster_features[k]["status"] = "ON"
            print(f"{Fore.GREEN}[!] ALL FEATURES ACTIVATED.")
            time.sleep(0.5)
        elif choice == "E":
            print(f"\n{Fore.GREEN}[!] INITIALIZING FULL SYSTEM OPTIMIZATION...")
            logs = ["-> CLOCK_BOOST_REQUESTED...", "-> CLEANING_MEMORY_BLOCKS...", "-> REFRESHING_NETWORK_SOCKETS...", "-> BYPASSING_THERMAL_THROTTLING...", "-> APPLYING_GPU_VULKAN_PATCH...", "-> INJECTING_FRAME_BYPASS_DATA...", "-> OPTIMIZING_PACKET_ROUTING...", "-> FINALIZING_HARDWARE_CONFIG..."]
            for log in logs:
                sys.stdout.write(f"{Fore.LIGHTBLACK_EX}[LOG]: {log}\n")
                time.sleep(0.4)
            progress_bar("BOOSTING SYSTEM PERFORMANCE", 4.0)
            print(f"{Fore.CYAN}{Style.BRIGHT}[SUCCESS] SYSTEM OPTIMIZED: +45% PERFORMANCE GAIN.")
            time.sleep(2)
        elif choice == "Q":
            break
        else:
            print(f"{Fore.RED}[!] COMMAND_NOT_FOUND")
            time.sleep(0.5)

def device_selection_menu():
    global SELECTED_DEVICE
    while True:
        clear_screen()
        print(Fore.LIGHTBLACK_EX + "==========================================================")
        print_rgb_flashing_text("BẠN ĐANG SỬ DỤNG THIẾT BỊ NÀO?")
        print(Fore.LIGHTBLACK_EX + "==========================================================")
        print(f"{Fore.CYAN}{Style.BRIGHT}   [1] MOBILE")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}   [2] WINDOWS")
        choice = input(f"\n{Fore.YELLOW}➔ NHẬP LỰA CHỌN (1 HOẶC 2): ").strip()
        if choice == "1":
            while True:
                print(f"\n{Fore.CYAN}--- CHỌN HỆ ĐIỀU HÀNH MOBILE ---")
                print(f"{Fore.GREEN}   [1] ANDROID\n   [2] IOS")
                sub_choice = input(f"{Fore.YELLOW}➔ Lựa chọn: ").strip()
                if sub_choice == "1":
                    SELECTED_DEVICE = "ANDROID"
                    break
                elif sub_choice == "2":
                    SELECTED_DEVICE = "IOS"
                    break
            break
        elif choice == "2":
            print(f"\n{Fore.RED}[!] THÔNG BÁO: HỆ THỐNG HIỆN CHƯA HỖ TRỢ THIẾT BỊ WINDOWS.")
            time.sleep(2)
            continue
    print(f"\n{Fore.GREEN}[+] HỆ THỐNG ĐÃ GHI NHẬN THIẾT BỊ: {SELECTED_DEVICE}")
    time.sleep(1)

def print_admin_denied_board(feature_name):
    print("\n" + Back.RED + Fore.WHITE + Style.BRIGHT + " ⛔ [ TRUY CẬP BỊ TỪ CHỐI ] ⛔ ")
    print(Fore.RED + Style.BRIGHT + f" ❌ LỖI: KHÔNG THỂ KHỞI CHẠY TIẾN TRÌNH: {feature_name}")
    print(Fore.YELLOW + " ➔ Cấp độ tài khoản không đủ thẩm quyền xử lý gói tin.")
    print(Fore.CYAN + " ➔ Mẹo: Liên hệ bộ đôi Admin để nhận mã kích hoạt VIP!")
    print(Back.RED + Fore.WHITE + Style.BRIGHT + " ============================================\n")
    time.sleep(1.5)

def print_gta5_block_alert():
    print("\n" + Back.RED + Fore.YELLOW + Style.BRIGHT + " 🔥 [ CRITICAL ERROR - SECURITY SYSTEM BLOCK ] 🔥 ")
    print(Fore.RED + Style.BRIGHT + " ⛔ THÔNG BÁO KHẨN CẤP: TIẾN TRÌNH BYPASS GTA5VN KHÔNG THỂ SỬ DỤNG VÀO LÚC NÀY!")
    logs = [
        "[-] DETECTING GAME VERSION: BUILD 2026 (ONLINE_SERVER)...",
        "[-] WARNING: ANTICHEAT ROCKSTAR SHIELD HAS BEEN INJECTED...",
        "[-] STATUS: ĐANG ĐỒNG BỘ HÓA GÓI TIN ĐÈ MEMORY CHỐNG BAN ACC...",
        "[-] BAO TRÌ: ADMIN ĐANG KHÓA CỔNG BƠM DATA ĐỂ TRÁNH QUÉT PHÂN VÙNG CỤC BỘ!"
    ]
    for log in logs:
        sys.stdout.write(Fore.LIGHTBLACK_EX + "[GTA5_LOG] ")
        print_delay(log, 0.003, Fore.LIGHTRED_EX)
        time.sleep(0.04)
    print(Fore.YELLOW + Style.BRIGHT + " ➔ VUI LÒNG QUAY LẠI SAU KHI TIẾN TRÌNH QUÉT AN TOÀN HOÀN TẤT VÀ CÓ LỆNH TỪ ADMIN!")
    print(Back.RED + Fore.YELLOW + Style.BRIGHT + " ======================================================================== ")
    time.sleep(1.5)

def run_disabled_brute_force():
    print("\n" + Back.RED + Fore.WHITE + Style.BRIGHT + " ❌ [ CỔNG KHAI THÁC ĐÃ BỊ KHÓA ] ❌ ")
    print(Fore.RED + Style.BRIGHT + " [!] THÔNG BÁO: CHỨC NĂNG BẺ KHÓA BẰNG BRUTE-FORCE TỰ ĐỘNG ĐÃ BỊ VÔ HIỆU HÓA.")
    print(Fore.YELLOW + f" -> LÝ DO: Hệ thống phát hiện xung đột dữ liệu trên phiên bản mới 2026.")
    print(Fore.CYAN + f" -> GIẢI PHÁP: Vui lòng nhắn tin trực tiếp cho Admin tại mục [E] HELP ngoài sảnh để đăng ký mã kích hoạt VIP.")
    print(Back.RED + Fore.WHITE + Style.BRIGHT + " ======================================================= ")
    time.sleep(1.5)

def print_rainbow_contact():
    print("\n" + "="*75)
    print(f"{Fore.RED}{Style.BRIGHT} [👑] ADMIN 1: {ADMIN_THH['NAME']}")
    print(f"      - HOTLINE : {ADMIN_THH['PHONE']:<15} | FACEBOOK: {ADMIN_THH['FACEBOOK']}")
    print(f"      - EMAIL   : {ADMIN_THH['EMAIL']:<15} | WECHAT  : {ADMIN_THH['WECHAT']}")
    print(f"{Fore.GREEN}{Style.BRIGHT} ---------------------------------------------------------------------------")
    print(f"{Fore.CYAN}{Style.BRIGHT} [🎀] ADMIN 2: {ADMIN_BNHUU['NAME']}")
    print(f"      - HOTLINE : {ADMIN_BNHUU['PHONE']:<15} | FACEBOOK: {ADMIN_BNHUU['FACEBOOK']}")
    print(f"      - EMAIL   : {ADMIN_BNHUU['EMAIL']:<15} | WECHAT  : {ADMIN_BNHUU['WECHAT']}")
    print("="*75 + "\n")

def simulate_hacker_matrix(proc_name):
    print(Fore.YELLOW + f"\n[!] KHỞI CHẠY TIẾN TRÌNH: {proc_name}")
    logs = [
        f"[-] Đang dò tìm vùng nhớ tiến trình game: 0x{random.randint(1000,9999)}...",
        "[-] Ghi đè mã lệnh (Opcode Byte Patching)... SUCCESS",
        "[-] Vượt qua tường lửa Anti-Cheat thế hệ mới...",
        "[-] Trạng thái bộ nhớ: Đã tối ưu hóa dòng lệnh mã độc."
    ]
    for log in logs:
        sys.stdout.write(Fore.LIGHTBLACK_EX + "[SYS_LOG] ")
        print_delay(log, 0.003, Fore.LIGHTGREEN_EX)
        time.sleep(0.04)

def simulate_typing(sender_name):
    sys.stdout.write(f"{Fore.YELLOW}[...] {sender_name} đang nhập...")
    sys.stdout.flush()
    time.sleep(random.uniform(0.5, 1.2))
    sys.stdout.write("\r" + " " * 60 + "\r")

def system_auth_manager():
    global CURRENT_USER, IS_ADMIN, DATABASE_ACCOUNT, HAS_CHAT_ACCESS
    device_selection_menu()
    print(Fore.LIGHTBLACK_EX + "==========================================================================")
    print_rgb_flashing_text("CHÀO MỪNG BẠN ĐẾN AIMBOT FREEFIRE - TAIXIU SAMP", duration_loops=35)
    print(Fore.LIGHTBLACK_EX + "==========================================================================")
    time.sleep(0.3)
    while True:
        print("\n" + Fore.LIGHTBLACK_EX + "--------------------------------------------------------------------------")
        print_rgb_flashing_text("BẠN CHỌN ĐĂNG KÝ HAY ĐĂNG NHẬP", duration_loops=25)
        print(Fore.LIGHTBLACK_EX + "--------------------------------------------------------------------------")
        print(f"{Fore.CYAN}{Style.BRIGHT}   [1] ĐĂNG KÝ TÀI KHOẢN MỚI\n   [2] ĐĂNG NHẬP HỆ THỐNG LAUNCHER")
        print(Fore.LIGHTBLACK_EX + "--------------------------------------------------------------------------")
        auth_choice = input(f"{Fore.YELLOW}➔ Nhập lựa chọn của bạn (1 hoặc 2): ").strip()
        if auth_choice == "1":
            reg_user = input(f"{Fore.YELLOW}➔ Tạo Tên Tài Khoản Mới: ").strip()
            reg_pass = input(f"{Fore.YELLOW}➔ Tạo Mật Khẩu Tài Khoản: ").strip()
            if not reg_user or not reg_pass:
                print(Fore.RED + "[!] Lỗi: Không được để trống dữ liệu đăng ký!\n")
                continue
            DATABASE_ACCOUNT = {"username": reg_user, "password": reg_pass}
            with open(USER_DATA_FILE, "w") as f:
                json.dump(DATABASE_ACCOUNT, f)
            print(Fore.GREEN + Style.BRIGHT + "\n[ THÀNH CÔNG ] Tài khoản đã được lưu!")
            progress_bar("Đang tạo phân vùng bảo mật", 0.5)
            break
        elif auth_choice == "2":
            login_user = input(f"{Fore.LIGHTBLUE_EX}➔ Nhập Tài Khoản: ").strip()
            login_pass = input(f"{Fore.LIGHTBLUE_EX}➔ Nhập Mật Khẩu: ").strip()
            if login_user == DATABASE_ACCOUNT["username"] and login_pass == DATABASE_ACCOUNT["password"]:
                CURRENT_USER = login_user
                print(f"\n{Fore.YELLOW}=== NHẬP KEY KÍCH HOẠT HỆ THỐNG ===\n• Key kích hoạt : {Fore.CYAN}{CHAT_ACCESS_KEYS[0]} / {CHAT_ACCESS_KEYS[1]}\n{Fore.YELLOW}===================================")
                key_in = input(f"{Fore.RED}➔ Nhập Key của bạn: ").strip().lower()
                if key_in == REQUIRED_VIP_KEY.lower():
                    IS_ADMIN = True
                    HAS_CHAT_ACCESS = True
                    print(Fore.GREEN + Style.BRIGHT + "\n[+] XÁC THỰC THÀNH CÔNG: QUYỀN ADMIN (FULL)!")
                elif key_in.upper() in CHAT_ACCESS_KEYS:
                    IS_ADMIN = False
                    HAS_CHAT_ACCESS = True
                    print(Fore.CYAN + "\n[+] XÁC THỰC THÀNH CÔNG: QUYỀN CHAT & BOOSTER ĐÃ MỞ!")
                else:
                    IS_ADMIN = False
                    HAS_CHAT_ACCESS = False
                    print(Fore.YELLOW + "\n[+] Đăng nhập thành viên thường.")
                progress_bar("Đang giải nén Menu Tiện Ích", 0.5)
                return
            else:
                print(Fore.RED + "\n[ THẤT BẠI ] Sai tên tài khoản hoặc mật khẩu hệ thống!")
                time.sleep(1.2)
        else:
            print(Fore.RED + "\n[!] Phím bấm không hợp lệ!\n")
            time.sleep(0.8)

def direct_admin_help_hub():
    print("\n" + "="*15 + " ☎️  HỆ THỐNG ĐƯỜNG DÂY NÓNG TRỢ GIÚP KHẨN CẤP ☎️  " + "="*15)
    print(f"{Fore.GREEN}[HỆ THỐNG] Đã định tuyến luồng ưu tiên. Kết nối thẳng tới bộ đôi Admin.")
    print(f"{Fore.YELLOW}[THÔNG BÁO] Nhập câu hỏi của bạn để gửi, gõ 'thoat' hoặc 'bye' để rút khỏi phòng hỗ trợ.")
    print("-" * 75)
    print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} 📢 PING! THÀNH VIÊN @{DATABASE_ACCOUNT['username'].upper()} VỪA GỬI TÍN HIỆU CỨU HỘ! 📢 ")
    simulate_typing("THH PHAYY")
    print(f"{Fore.MAGENTA}THH PHAYY: {Fore.WHITE}Chào @{DATABASE_ACCOUNT['username']} nhé! Anh nhận được thông báo hỗ trợ từ ngoài Menu chính rồi.")
    simulate_typing("TRPHH BNHUU")
    print(f"{Fore.LIGHTRED_EX}TRPHH BNHUU: {Fore.WHITE}Hello bạn yêu nha! Mình túc trực hỗ trợ cài đặt file mod cho bạn đây nè 🎀")
    while True:
        user_in = input(f"\n{Fore.GREEN}[BẠN]: {Fore.WHITE}").strip()
        if not user_in:
            continue
        if user_in.lower() in ["thoát", "out", "bye", "thoat"]:
            simulate_typing("TRPHH BNHUU")
            print(f"{Fore.LIGHTRED_EX}TRPHH BNHUU: {Fore.WHITE}Oki bái bai bạn nhé! Cần gì cứ bấm nút [E] ngoài sảnh nha moa moa! ✨")
            break
        response = random.choice(ADMIN_RESPONSES)
        reply_admin = random.choice(["PHAYY", "BNHUU"])
        if reply_admin == "PHAYY":
            simulate_typing("THH PHAYY")
            print(f"{Fore.MAGENTA}THH PHAYY: {Fore.WHITE}{response}")
        else:
            simulate_typing("TRPHH BNHUU")
            print(f"{Fore.LIGHTRED_EX}TRPHH BNHUU: {Fore.WHITE}{response}")

def global_online_chat_room():
    print("\n" + "="*15 + " 🌐 KÊNH CHAT CỘNG ĐỒNG ONLINE (VERSION 2026) 🌐 " + "="*15)
    print(f"{Fore.GREEN}[HỆ THỐNG] Phòng chat trực tuyến ổn định.")
    print(f"{Fore.YELLOW}[THÔNG BÁO] Gõ 'thoat' hoặc 'bye' để rời phòng chat.")
    print("-" * 75)
    for _ in range(3):
        u_name, u_text, u_color = random.choice(FAKE_USER_DB)
        simulate_typing(u_name)
        print(f"{u_color}{u_name}: {Fore.WHITE}{u_text}")
    while True:
        ready, _, _ = select.select([sys.stdin], [], [], 2.5)
        if ready:
            user_msg = sys.stdin.readline().strip()
            if not user_msg:
                continue
            if user_msg.lower() in ["thoát", "out", "bye", "thoat"]:
                break
            reply = random.choice(ADMIN_RESPONSES)
            simulate_typing("ADMIN_BOT")
            print(f"{Fore.RED}[ADMIN]: {Fore.WHITE}{reply}")
        else:
            u_name, u_text, u_color = random.choice(FAKE_USER_DB)
            simulate_typing(u_name)
            print(f"{u_color}{u_name}: {Fore.WHITE}{u_text}")

def run_samp_taixiu_tool():
    clear_screen()
    print(f"{Fore.YELLOW}{Style.BRIGHT}================================================")
    print(f"{Fore.CYAN}{Style.BRIGHT}   VUI LÒNG NHẬP SỐ PHIÊN TÀI XỈU HIỆN TẠI")
    print(f"{Fore.YELLOW}{Style.BRIGHT}================================================")
    input_phien = input(f"{Fore.WHITE}➔ Nhập số phiên: ").strip().upper()
    for count in range(5, 0, -1):
        clear_screen()
        print(f"{Fore.RED}{Style.BRIGHT}=== [ INJECTING LÕI THUẬT TOÁN CODES GTAVIET.NET - CHỜ ĐỒNG BỘ ] ===")
        print("\n" * 2)
        for row in BIG_NUMBERS[count]:
            color = random.choice(RAINBOW_COLORS)
            print(f"            {color}{Style.BRIGHT}{row}")
        print("\n" * 2)
        print(f"{Fore.YELLOW}👉 ĐANG ĐỒNG BỘ GÓI PACKET VÀO CỔNG GTAVIET.NET SAMP... {count}S")
        time.sleep(1.0)
    print(Fore.CYAN + "[+] ĐỒNG BỘ DATABASE THÀNH CÔNG: https://gtaviet.net/samp/taixiu-database")
    time.sleep(0.3)
    while True:
        d1, d2, d3 = random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)
        tong_diem = d1 + d2 + d3
        is_tai = tong_diem >= 11
        pred1 = f"{Fore.LIGHTRED_EX}{Style.BRIGHT}TAI (TÀI)" if is_tai else f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}XIU (XỈU)"
        pred2 = f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}XIU (XỈU)" if is_tai else f"{Fore.LIGHTRED_EX}{Style.BRIGHT}TAI (TÀI)"
        rate1 = random.randint(85, 99)
        rate2 = 100 - rate1
        for timer in range(40, -1, -1):
            clear_screen()
            print(f"{Fore.GREEN}==========================================================================")
            sys.stdout.write("  PHIÊN HIỆN TẠI: ")
            for char in input_phien:
                sys.stdout.write(f"{random.choice(RAINBOW_COLORS)}{Style.BRIGHT}{char}")
            print(f"\n{Fore.GREEN}==========================================================================")
            print(f"{Fore.WHITE} [+] ĐƯỜNG TRUYỀN SERVER : {Fore.GREEN}GTAVIET.NET SAMP CORE (STABLE)")
            print(f"{Fore.WHITE} [+] THỜI GIAN CÒN LẠI   : {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{timer} Giây")
            print(f"{Fore.GREEN}--------------------------------------------------------------------------")
            if timer > 5:
                print(f"{Fore.CYAN}[ PHÂN TÍCH ] {Fore.WHITE}Đang quét luồng dữ liệu RAM, phân tích xúc xắc...")
            else:
                print(f"{Fore.GREEN}[ KHÓA CỔNG THÀNH CÔNG ] {Fore.LIGHTGREEN_EX}Đã bẻ khóa thuật toán!")
                print(f"{Fore.WHITE} [+] KẾT QUẢ XÚC XẮC  : {Fore.MAGENTA}{d1} - {d2} - {d3} {Fore.WHITE}(Tổng: {Fore.YELLOW}{tong_diem} nút{Fore.WHITE})")
                print(f"{Fore.WHITE} ➔ DỰ ĐOÁN 1 ({rate1}%): {pred1}")
                print(f"{Fore.WHITE} ➔ DỰ ĐOÁN 2 ({rate2}%): {pred2}")
            print(f"{Fore.GREEN}==========================================================================")
            print(f"{Fore.LIGHTBLACK_EX}[HỆ THỐNG] Ấn phím bất kỳ rồi bấm Enter để rút về sảnh chính...")
            ready, _, _ = select.select([sys.stdin], [], [], 1.0)
            if ready:
                sys.stdin.readline()
                return

# ==========================================================================
# KHỞI CHẠY HỆ THỐNG
# ==========================================================================
check_for_updates()
system_auth_manager()
print(Fore.RED + Style.BRIGHT + f"\n==================================================\n   LAUNCHER CONSOLE MULTI-GAME (UPDATE 2026)      \n   XIN CHÀO THÀNH VIÊN: {DATABASE_ACCOUNT['username'].upper()}\n==================================================")
time.sleep(0.2)

while True:
    print_update_banner()
    status_label = get_flashing_rainbow_text("THÀNH CÔNG") if IS_ADMIN else (f"{Fore.GREEN}[CHAT+BOOST]" if HAS_CHAT_ACCESS else f"{Fore.RED}[NONE]")
    print(f"\n{Fore.CYAN}--- DANH SÁCH MENU ĐIỀU KHIỂN CHÍْNH ---")
    print(f"{Fore.WHITE}[A] MENU MOD FREE FIRE ĐA TÍNH NĂNG {status_label}")
    print(f"{Fore.GREEN}{Style.BRIGHT}[B] Samp Launcher [ Tool Tài Xỉu GtaViet.Net ] {status_label} {Fore.YELLOW}[OPEN]")
    print(f"{Fore.WHITE}[C] KÊNH CHAT ONLINE CỘNG ĐỒNG GIẢ LẬP")
    print(f"{Fore.YELLOW}{Style.BRIGHT}[G] GAME TURBO ULTRA (BOOSTER & OPTIMIZER)")
    print(f"{Fore.GREEN}{Style.BRIGHT}[E] HELP - GỌI TRỰC TIẾP ADMIN TRỢ GIÚP KHẨN CẤP [MẶT TIỀN]")
    print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[F] MOD MENU GTA5VN BYPASS BY ADMIN {status_label} {Fore.YELLOW}[HOT]")
    if not IS_ADMIN:
        print(f"{Fore.GREEN}[D] BẺ KHÓA CHỨNG CHỈ QUYỀN ADMIN [ĐÃ KHÓA CỔNG]")
    print(f"{Fore.WHITE}[Q] THOÁT KHỎI HỆ THỐNG")
    print("-------------------------------------------------------")
    game_choice = input(f"{Fore.LIGHTBLUE_EX}Chọn tính năng trên màn hình: ").strip().upper()
    if game_choice == "Q":
        print_delay("\n[+] Đang xóa cache, tắt tiến trình an toàn... Tạm biệt!", 0.008, Fore.YELLOW)
        break
    elif game_choice in ["A", "B", "G"]:
        if not check_device_root_status():
            continue
    if game_choice == "A":
        if not IS_ADMIN:
            print_admin_denied_board("FreeFire_Multi_Premium_Injector")
            continue
        print_delay("\n[+] Đang tải Cơ sở dữ liệu hack FreeFire Premium...", 0.005, Fore.GREEN)
        ff_features = {"1": {"name": "AUTO AIMBOT LOCK HEAD (KHÓA ĐẦU)", "active": False, "proc": "FF_AimbotHead.dll"}, "2": {"name": "AUTO GHIM TÂM VÀO NGƯỜI 100%", "active": False, "proc": "FF_GhimTam.dll"}, "3": {"name": "MENU NHÌN XUYÊN TƯỜNG (ESP WALL)", "active": False, "proc": "FF_EspWall.sys"}, "4": {"name": "KÍCH HOẠT HACK BAY (FLY HACK)", "active": False, "proc": "FF_FlyPremium.dll"}, "5": {"name": "ĐI XUYÊN ĐÁ VÀ ĐỊA HÌNH SÂN ĐẤU", "active": False, "proc": "FF_XuyenDa.sys"}, "6": {"name": "HACK TỐC ĐỘ CHẠY (SPEED RUN X5)", "active": False, "proc": "FF_SpeedRun.dll"}}
        while True:
            print(f"\n{Fore.CYAN}--- 💎 MENU HACK FREE FIRE PREMIUM VIETNAM 💎 ---")
            for key, val in ff_features.items():
                status = f"{Fore.GREEN}[ĐÃ BẬT]" if val["active"] else f"{Fore.RED}[ĐÃ TẮT]"
                print(f"{Fore.WHITE}[{key}] Kích hoạt {val['name']:<40} {status}")
            print(f"{Fore.WHITE}[7] TIẾN HÀNH BƠM TẤT CẢ VÀO GAME VÀ VÀO TRẬN")
            print(f"{Fore.WHITE}[8] QUAY LẠI MENU CHÍNH")
            print("-----------------------------------------------------------------")
            choice = input(f"{Fore.LIGHTBLUE_EX}Vui lòng chọn số (1-8): ").strip()
            if choice in ff_features:
                if ff_features[choice]["active"]:
                    print(f"{Fore.YELLOW}\n[!] Tính năng này sếp đã bật sẵn từ trước rồi!")
                else:
                    simulate_hacker_matrix(ff_features[choice]["proc"])
                    progress_bar(f"Injecting {ff_features[choice]['proc']}", 1.2)
                    ff_features[choice]["active"] = True
            elif choice == "7":
                progress_bar("Đang liên kết dữ liệu tổng và khởi chạy game", 1.8)
                print(Fore.GREEN + Style.BRIGHT + "[SUCCESS] KÍCH HOẠT THÀNH CÔNG! HÃY VÀO GAME ĐỂ TRẢI NGHIỆM.")
                break
            elif choice == "8":
                break
            else:
                print(f"\n{Fore.RED}[!] Nút bấm không hợp lệ, vui lòng chọn lại!\n")
                time.sleep(0.5)
        print_rainbow_contact()
    elif game_choice == "B":
        if not IS_ADMIN:
            print_admin_denied_board("SAMP_TaiXiu_Algorithm_Bypass")
            continue
        run_samp_taixiu_tool()
        print_rainbow_contact()
    elif game_choice == "G":
        if not HAS_CHAT_ACCESS:
            print_admin_denied_board("Game_Booster_Feature")
            continue
        run_game_booster()
        print_rainbow_contact()
    elif game_choice == "C":
        if not HAS_CHAT_ACCESS:
            print_admin_denied_board("Online_Chat_Room")
            continue
        global_online_chat_room()
        print_rainbow_contact()
    elif game_choice == "E":
        if not HAS_CHAT_ACCESS:
            print_admin_denied_board("Admin_Support_Help")
            continue
        direct_admin_help_hub()
        print_rainbow_contact()
    elif game_choice == "F":
        if not IS_ADMIN:
            print_admin_denied_board("GTA5VN_Server_Bypass_Core")
            continue
        print_gta5_block_alert()
        print_rainbow_contact()
    elif game_choice == "D":
        if IS_ADMIN:
            continue
        run_disabled_brute_force()
        print_rainbow_contact()
    else:
        print(f"\n{Fore.RED}[!] Lựa chọn không hợp lệ. Thử lại!\n")
        time.sleep(0.5)
