import subprocess
import sys
with subprocess.Popen(["ssh", "%s" % "pi@192.168.1.108", "ls"], shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE) as ssh:
    result = ssh.stdout.readlines()
