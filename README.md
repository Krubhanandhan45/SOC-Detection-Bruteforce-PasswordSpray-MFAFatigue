SOC Detection Engineering Project
Brute Force (T1110.001) • Password Spraying (T1110.003) • MFA Fatigue (T1621)
📌 Overview

This project simulates three real-world authentication attacks and builds Splunk detection rules to identify them.
The detections follow MITRE ATT&CK standards and demonstrate how SOC analysts monitor and investigate identity-based threats.

This repository includes:

Attack simulation scripts

Raw logs (Hydra, SSH, custom MFA logs)

Splunk SPL queries

MITRE mappings

Screenshots + documentation

🛠️ Tools Used

Splunk Enterprise

Hydra (SSH brute force tool)

Python 3 (password spraying script)

Ubuntu WSL

SSH logs (/var/log/auth.log)

Custom MFA push logs (mfa.log)

MITRE ATT&CK Navigator

1️⃣ Brute Force Attack — T1110.001
🔥 Simulation Command
hydra -l testuser -P passwords.txt ssh://localhost -t 4 -V


This generates multiple SSH login failures, similar to real attacker behavior.

🔎 Splunk Detection Query
index=* "Failed password" sourcetype=linux_secure
| stats count by user src
| where count > 10

🎯 Detection Logic

High number of failed authentications

Same user targeted repeatedly

Same source IP → brute force pattern

2️⃣ Password Spraying Attack — T1110.003
🐍 Python Script (spray.py)
import os, time
users = ["alice","bob","charlie","david","eve"]
password = "Password123"

for user in users:
    print(f"Trying password for {user}")
    os.system(f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@localhost exit")
    time.sleep(1)

🔎 Splunk Detection Query
index=* "Failed password"
| stats dc(user) as unique_users count by src
| where unique_users > 5

🎯 Detection Logic

Many users targeted

Same password attempted

Low-and-slow technique to avoid lockouts

3️⃣ MFA Fatigue Attack — T1621 (Push Bombing)
📄 Sample MFA Log (mfa.log)
2025-12-04T11:30:01Z user=testuser action=MFA_Push status=Sent reason=LoginAttempt
2025-12-04T11:30:05Z user=testuser action=MFA_Push status=Denied reason=UserIgnored
2025-12-04T11:30:10Z user=testuser action=MFA_Push status=Denied reason=UserIgnored
2025-12-04T11:30:15Z user=testuser action=MFA_Push status=Denied reason=UserIgnored
2025-12-04T11:30:20Z user=testuser action=MFA_Push status=Denied reason=UserIgnored
2025-12-04T11:30:25Z user=testuser action=MFA_Push status=Approved reason=UserAccepted

🔎 Splunk Detection Query
index=* sourcetype="mfa_logs"
| stats count values(status) as status_list by user
| where count > 5 AND mvfind(status_list, "Approved") >= 0

🎯 Detection Logic

Flags the scenario where:

A user receives a large number of MFA pushes (>5)

User eventually approves one → attacker succeeded

This replicates real attacks seen in: Uber, Cisco, Microsoft, Rockstar Games.

📊 MITRE ATT&CK Mapping
Technique	Description	ID
Brute Force	Repeated rapid password attempts	T1110.001
Password Spraying	Same password against many users	T1110.003
MFA Fatigue / Push Bombing	Flooding user with MFA prompts	T1621
📎 Screenshots

Screenshots included in the screenshots/ folder:

Hydra brute force output

Password spraying execution

Splunk raw events

Splunk statistics

MFA fatigue detection results

🧠 What I Learned

How to simulate multiple identity-based attack types

How to ingest and normalize Linux & custom logs in Splunk

SPL query design for authentication anomaly detection

MITRE ATT&CK technique mapping

Building detections aligned to real SOC workflows

Identifying compromise through multi-event correlation

🙌 Author

Krubhanandhan Krishnan
SOC / Threat Detection / Blue Team enthusiast
France 🇫🇷
