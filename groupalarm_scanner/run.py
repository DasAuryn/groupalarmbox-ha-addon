#!/usr/bin/env python3
from zeroconf import Zeroconf, ServiceBrowser
import socket, time, json, ipaddress, requests

try:
    with open("/data/options.json", "r") as f:
        OPT = json.load(f)
except Exception:
    OPT = {}

TARGETS = [t.strip().lower() for t in OPT.get("targets", ["groupalarmbox"])]
BROWSE_TYPES = OPT.get("browse_types", ["_http._tcp.local."]) 

HA_BASE  = OPT.get("ha_base_url", "http://homeassistant:8123").rstrip("/")
HA_TOKEN = OPT.get("ha_token", "").strip()
ENTITY_ID = OPT.get("ha_entity_id", "sensor.groupalarmbox_ip")

MQTT_HOST = OPT.get("mqtt_host", "homeassistant")
MQTT_PORT = int(OPT.get("mqtt_port", 1883))
MQTT_USER = OPT.get("mqtt_user", "")
MQTT_PASS = OPT.get("mqtt_pass", "")
DISCOVERY_PREFIX = OPT.get("discovery_prefix", OPT.get("mqtt_discovery_prefix", "homeassistant"))

UDP_PORT = int(OPT.get("udp_port", 42424))
UDP_RETRIES = int(OPT.get("udp_retries", 3))
UDP_DELAY_MS = int(OPT.get("udp_delay_ms", 800))
SCAN_WINDOW_SEC = int(OPT.get("scan_window_sec", 30))
IDLE_RESCAN_SEC = int(OPT.get("idle_rescan_sec", 5))

HEADERS = {"Authorization": f"Bearer {HA_TOKEN}",
           "Content-Type": "application/json",
           "Accept": "application/json"} if HA_TOKEN else None

def fmt_addr(raw: bytes) -> str:
    if len(raw) == 4:
        return socket.inet_ntoa(raw)
    try:
        return str(ipaddress.ip_address(raw))
    except Exception:
        return repr(raw)

def resolve_ipv4(host: str) -> str | None:
    try:
        infos = socket.getaddrinfo(host, None, socket.AF_INET, socket.SOCK_STREAM)
        if infos:
            return infos[0][4][0]
    except Exception:
        pass
    return None

def ha_post(path: str, payload: dict):
    if not HA_TOKEN:
        return 0, "no token configured"
    try:
        r = requests.post(f"{HA_BASE}/api{path}", headers=HEADERS, data=json.dumps(payload), timeout=5)
        return r.status_code, r.text
    except Exception as e:
        return 0, str(e)

def set_ip_state(ip: str | None):
    if not HA_TOKEN:
        return
    state = ip if ip else "unavailable"
    attrs = {"friendly_name": "GroupAlarmBox IP", "icon": "mdi:ip"}
    code, _ = ha_post(f"/states/{ENTITY_ID}", {"state": state, "attributes": attrs})
    if code:
        print(f"[HA] set {ENTITY_ID} -> {state} ({code})", flush=True)

def build_msg() -> bytes:
    host_ip = (OPT.get("mqtt_host_ip") or "").strip() or (resolve_ipv4(MQTT_HOST) or "")
    return (
        f"host={MQTT_HOST};"
        f"host_ip={host_ip};"
        f"port={MQTT_PORT};"
        f"user={MQTT_USER};"
        f"pass={MQTT_PASS};"
        f"prefix={DISCOVERY_PREFIX}"
    ).encode()

def send_udp(ip: str):
    payload = build_msg()
    addr = (ip, UDP_PORT)
    for i in range(UDP_RETRIES):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(1.0)
                s.sendto(payload, addr)
            print(f"[PROVISION] UDP -> {ip}:{UDP_PORT} (try {i+1}/{UDP_RETRIES})", flush=True)
        except Exception as e:
            print(f"[WARN] UDP send failed to {ip}:{UDP_PORT}: {e}", flush=True)
        time.sleep(UDP_DELAY_MS/1000.0)

class TargetListener:
    def __init__(self):
        self.provisioned = set()  

    def _match(self, name, server):
        name_l = (name or "").lower()
        server_l = (server or "").lower()  
        return any(t in name_l for t in TARGETS) or any(t in server_l for t in TARGETS)

    def _handle(self, zc, typ, name, updated=False):
        info = zc.get_service_info(typ, name)
        if not info: 
            return
        if not self._match(name, getattr(info, "server", "")): 
            return

        addrs = [fmt_addr(a) for a in (info.addresses or [])]
        ip = addrs[0] if addrs else None
        mark = "[~]" if updated else "[+]"
        print(f"{mark} {name} @ {', '.join(addrs) if addrs else 'n/a'} (type: {typ})", flush=True)

        if ip and ip not in self.provisioned:
            self.provisioned.add(ip)
            set_ip_state(ip)
            send_udp(ip)

    def add_service(self, zc, typ, name):    self._handle(zc, typ, name, False)
    def update_service(self, zc, typ, name): self._handle(zc, typ, name, True)
    def remove_service(self, zc, typ, name): pass

def scan_loop():
    while True:
        print("\n[*] scanning via mDNS (no broadcast)...", flush=True)
        zc = Zeroconf()
        listener = TargetListener()
        browsers = [ServiceBrowser(zc, t, listener) for t in BROWSE_TYPES]
        start = time.time()

        try:
            while True:
                time.sleep(1)
                if time.time() - start > SCAN_WINDOW_SEC:
                    break
        except KeyboardInterrupt:
            zc.close()
            return
        finally:
            zc.close()

        print(f"[INFO] Scan abgeschlossen — neuer Scan in {IDLE_RESCAN_SEC} s", flush=True)
        time.sleep(IDLE_RESCAN_SEC)

if __name__ == "__main__":
    print("[INFO] starting GroupAlarmBox Scanner (mDNS only)...", flush=True)
    scan_loop()
