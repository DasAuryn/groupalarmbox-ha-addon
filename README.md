# 🧭 GroupAlarmBox Add-on für Home Assistant

**Schnell. Einfach. Automatisch verbunden.**

Das GroupAlarmBox Add-on verbindet dein Smart Home direkt mit deiner GroupAlarmBox.  
Sobald das Add-on aktiv ist, wird dein Netzwerk automatisch nach einer Box durchsucht –  
und sobald sie gefunden wird, übernimmt Home Assistant die Kommunikation.

---

## 🚀 Was das Add-on macht

- Erkennt automatisch deine **GroupAlarmBox** im lokalen Netzwerk  
- Stellt eine sichere Verbindung her und übergibt die benötigten Einstellungen  
- Empfängt Alarmmeldungen direkt aus deiner Box und macht sie in Home Assistant sichtbar  
- Informiert dich zuverlässig über neue Einsätze, Warnungen oder Statusmeldungen  

Keine manuelle Einrichtung, keine komplizierten Schritte – einfach starten und verbunden sein.

---

## ⚙️ Einrichtung

1. Öffne in Home Assistant den **Add-on-Store**.  
2. Füge das Repository hinzu und installiere das Add-on **GroupAlarmBox**.  
3. In der Konfiguration kannst du folgende Angaben machen:

   | Einstellung | Beschreibung |
   |--------------|--------------|
   | `Home Assistant URL` | Adresse deines Home Assistant-Servers *(Standard: `http://homeassistant:8123`)* |
   | `MQTT-Host` | Adresse deines MQTT Brokers |
   | `MQTT-Benutzer` | Benutzername deines MQTT Brokers |
   | `MQTT-Passwort` | Passwort deines MQTT-Benutzers |

4. Add-on speichern und starten.  
   Innerhalb weniger Sekunden wird deine GroupAlarmBox erkannt.  

---

## 🔔 Wenn ein Alarm eingeht

Sobald die Box eine Alarmmeldung empfängt, erscheint diese automatisch in Home Assistant.  
Du kannst sie dort direkt in Automationen, Szenen oder Benachrichtigungen einbinden —  
zum Beispiel:

- Lichter einschalten, wenn ein Alarm ausgelöst wird  
- Eine Push-Mitteilung senden, sobald ein neuer Einsatz eingeht  
- Akustische Signale im Haus aktivieren  

---

## 🌐 Funktionsweise

Das Add-on durchsucht regelmäßig dein lokales Netzwerk (mDNS-Scan) nach einer GroupAlarmBox.  
Sobald sie gefunden wurde, wird eine sichere Verbindung hergestellt.  
Die Box übermittelt ihre Informationen und sendet bei Alarm automatisch eine Meldung an Home Assistant.  

Alles geschieht lokal — schnell, sicher und ohne externe Server.

---

## 💡 Vorteile

- **Plug & Play:** Keine manuelle IP-Eingabe nötig  
- **Sofort einsatzbereit:** Erkennt Boxen automatisch nach dem Einschalten  
- **Sicher & lokal:** Keine Cloud-Abhängigkeit  

---

## 🧾 Lizenz & Haftung

Dieses Add-on wird kostenlos bereitgestellt und ist für die private oder organisatorische Nutzung gedacht.  
Die Nutzung erfolgt auf eigene Verantwortung. Für Alarme, die nicht oder verspätet übermittelt werden, wird keine Haftung übernommen.

---

## 📞 Support

Fragen, Feedback oder Ideen?  
Besuche [groupalarm.com](https://www.groupalarm.com) oder kontaktiere dein Support-Team.

---

**GroupAlarmBox Add-on für Home Assistant**  
