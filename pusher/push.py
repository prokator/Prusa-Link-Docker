import os, requests, time

token = os.getenv("TOKEN")
url = os.getenv("SNAPSHOT_URL")
# Use PUT as per Prusa API spec; Fingerprint can match Token for "Other" cams
headers = {
    "Token": token,
    "Fingerprint": token,
    "Content-Type": "image/jpeg",
    "Accept": "*/*"
}

print(f"Pusher started. Using token: {token[:5]}...")

while True:
    try:
        img_res = requests.get(url, timeout=5)
        if img_res.status_code == 200:
            # Explicitly include Content-Length for Prusa's server
            headers["Content-Length"] = str(len(img_res.content))
            
            # Prusa Connect uses PUT for /c/snapshot
            r = requests.put(
                "https://connect.prusa3d.com/c/snapshot",
                headers=headers,
                data=img_res.content,
                timeout=10
            )
            
            if r.status_code in [200, 204]:
                print("Snapshot successfully synced.")
            else:
                print(f"PrusaConnect Error: {r.status_code} - {r.text}")
        else:
            print(f"Camera Error: {img_res.status_code}")
            
    except Exception as e:
        print(f"Loop Error: {e}")
    
    # PrusaConnect limits snapshots to roughly every 10 seconds
    time.sleep(10)