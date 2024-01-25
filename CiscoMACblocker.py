def print_banner():
	print("""\n
*******************************************************************************************************
*                                                                                                     *
*   ___  _                 __                        _  _      _                                      *
*  / ____/  _/ ___// ____/ __ \   /  |/  /   | / ____/  / __ )/ /   / __ \/ ____/ //_// ____/ __ \    *
* / /    / / \__ \/ /   / / / /  / /|_/ / /| |/ /      / __  / /   / / / / /   / ,<  / __/ / /_/ /    *
*/ /____/ / ___/ / /___/ /_/ /  / /  / / ___ / /___   / /_/ / /___/ /_/ / /___/ /| |/ /___/ _, _/     *
*\____/___//____/\____/\____/  /_/  /_/_/  |_\____/  /_____/_____/\____/\____/_/ |_/_____/_/ |_       *
* Coded by Zeeshan Aslam                                                                              *
* qpzeeshan@gmail.com                                                                                 *
* Block and unblock unwanted MAC address on Cisco Vlan 200 based on secure shell                      *
*******************************************************************************************************\n\n""")
print_banner()
import paramiko, time
import re
import sys
import netaddr
from prompt_toolkit import prompt
from collections import Counter
connection = paramiko.SSHClient()
connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
IP = input("Enter IP address of Cisco Interface: ")
User = input("Enter username: ")
Password = prompt('Enter password: ', is_password=True)
connection.connect(IP, username= User, password= Password , look_for_keys=False, allow_agent=False)
new_connection = connection.invoke_shell()
new_connection.send("enable \n")
time.sleep(3)
EnPassword = prompt('Enter configuration mode password: ', is_password=True)
#output = new_connection.recv(5000)
#print(output)
new_connection.send(EnPassword)
new_connection.send("\n")
time.sleep(3)
output = new_connection.recv(5000)
count = sum(1 for match in re.finditer(r"\bPassword\b", output.decode('utf-8')))
if count == 2:
 new_connection.close()
 print("\nWrong enable password exiting...")
 sys.exit()
new_connection.send("conf t \n")
time.sleep(3)
#output = new_connection.recv(5000)
#print(output)
#new_connection.send("ip access-group 101 in \n")
#new_connection.send("no ip access-group 101 in \n")
MACAddress = '_'    
while True:
 try:
  var = int(input("Enter 1 to block MAC address or 2 to unblock it and for quit enter 3: "))
  if var == 1: 
   MACAddress = input('Please enter a MACAddress (Only unicast and hexdecimal upto 12 characters):')
   mac = netaddr.EUI(MACAddress)
   mac_is_multicast = bool(mac.words[0] & 0b01)  # Is LSB set?
   if mac_is_multicast == False and re.match("^[A-Fa-f0-9]{12}$", MACAddress):
    t = iter(MACAddress)
    MACAddress= '.'.join(a+b+c+d for a,b,c,d in zip(t, t, t, t))
    new_connection.send("mac address-table static ")
    new_connection.send(MACAddress)
    new_connection.send(" vlan 200 drop \n")
    time.sleep(3)
    print("Block MACAddress: ", MACAddress)
    #output = new_connection.recv(5000)
    #print(output)
  elif var == 2: 
   MACAddress = input('Please enter a MACAddress (Only unicast and hexdecimal upto 12 characters):')
   mac = netaddr.EUI(MACAddress)
   mac_is_multicast = bool(mac.words[0] & 0b01)  # Is LSB set?
   if  mac_is_multicast == False and re.match("^[A-Fa-f0-9]{12}$", MACAddress):
    t = iter(MACAddress)
    MACAddress= '.'.join(a+b+c+d for a,b,c,d in zip(t, t, t, t))
    new_connection.send("no mac address-table static ")
    new_connection.send(MACAddress)
    new_connection.send(" vlan 200 \n")
    time.sleep(3)
    print("Unblock MACAddress: ", MACAddress)
    #output = new_connection.recv(5000)
    #print(output)
  elif var == 3:
   break
   new_connection.close()
   sys.exit()
  else:
   print("Invalid number")
 except (SyntaxError, ValueError):
  print("You didn't enter a number")
 except:
  #output = new_connection.recv(5000)
  #print(output)
  print("\nSomething else went wrong")

