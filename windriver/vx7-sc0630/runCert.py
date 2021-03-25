import os
import subprocess

def vx7CertGit ():
    cmdret = subprocess.run (args=['git checkout vx7-SC0630'], shell=True, 
                            cwd="/workspace/blan/helixsde/vx7-sc0630")
    if cmdret.returncode != 0:
        print ("failed")
        return
    subprocess.run(args=['git pull'], shell=True, 
                   cwd="/workspace/blan/helixsde/vx7-sc0630")

if __name__ == '__main__':
    vx7CertGit ()