import os
import time

users = ["alice", "bob", "charlie", "david", "eve", "frank", "testuser"]
password = "Password123"

for user in users:
    cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@localhost exit"
    print(f"Trying {password} for {user}")
    os.system(cmd)
    time.sleep(1)
