
import subprocess
import json
import os

def start_bw():
    """UNLOCK BW AND GET SESSION"""
    result = subprocess.run(
        ["bw", "status"]
    )
    # status = json.loads(result.stdout)#['status']
    # print(f"Bitwarden status: {status}")
    print(result.stdout.replace("mac failed.", ""))

def main():
    start_bw()

if __name__ == "__main__":
    main()