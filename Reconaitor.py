import ipaddress, pyfiglet, re, socket, threading, time, requests, json, sys
from netaddr import *
from colorama import Fore
import art
from nmap import *

global website_url
import time

# Artistic Information
artpost = art.text2art("Reconaitor")


def info():
    print(Fore.WHITE, 'Created by: NanoExploiters')
    print(Fore.GREEN, '   ---> Abdulaziz Al-Boraei : 2200400019')
    print(Fore.BLUE, '   ---> Abdulaziz Al-Hassan : 2190001931')
    print(Fore.RED, '   ---> Basil Abdulrahman : 2190002560')
    print(Fore.CYAN, '   ---> Mohammed Al-Zahrani: 2190002349')
    print(Fore.MAGENTA, '   ---> Nawaf Al-Sukaibi: 2190000802')
    print(Fore.YELLOW, '   ---> Saif Al-Sayegh: 2190005084')
    print(Fore.LIGHTGREEN_EX, 'Supervised by: Mr. Hussain Al-Attas')
    print(Fore.LIGHTBLUE_EX, 'Course: CYS 403 - Programming for Cybersecurity')
    print(Fore.LIGHTBLACK_EX, 'Version 1.0')


# re
ip_add_pattern = re.compile("^(?:[0-9]{1,3}.){3}[0-9]{1,3}$")
re.compile("^(?:[0-9]{1,3}.){3}[0-9]{1,3}$")
re.compile("^(?:[0-9]{1,3}.){3}[0-9]{1,3}$")
checkurl = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" + "+[A-Za-z]{2,6}"
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
global ports
ports = []

scanner=nmap.PortScanner()
# method that scans web for open ports and website's information
def ScanWeb(ip):
    
    OS=scanner.scan(ip, arguments='-O')['scan'][ip]['osmatch'][1]['name']
    
    print("Please enter the range of ports to scan. ex: 30-60 ")
    # input validation for port range (will not exit the loop until the range is correct)
    while True:
        port_range = input("enter port range: ")
        # line 44 will remove any additional spaces
        port_range_valid = port_range_pattern.search(port_range.replace(" ", ""))
        # Port validation
        if port_range_valid:
            # if the range is valid we will split the 2 ranges so we can add them in the port list
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            break
        print("\nPlease enter the range again. ex: 30-60")
    print("scanning ports..")
    time.sleep(1)
    ScanPort_Thread(ip_add_entered, port_min, port_max)
    try:
        # requests website data
        req = requests.get("https://ipinfo.io/" + ip + "/json")
        # transfers requested data into a dictionary
        data = json.loads(req.text)
        print("connecting to server..")
        time.sleep(0.6)
        print("connected")
        print("retriving data.. \n")
        time.sleep(2)

        # prints the available data
        if data["ip"]:
            print("IP:", data["ip"])
        try:
            if data["hostname"]:
                print("Hostname:", data["hostname"])
        except:
           pass
        if data["city"]:
            print("City:", data["city"])
        if data["region"]:
            print("Region:", data["region"])
        if data["country"]:
            print("Country:", data["country"])
        if data["loc"]:
            print("Geo location address:", data["loc"])
        if data["org"]:
            print("Organization:", data["org"])
        if data["timezone"]:
            print("Timezone:", data["timezone"])
        if OS:
            print('Operating system: ',OS)    
        print("\nWould you like to print the results in a file?")
        print("1: yes")
        print("2: no")
        # validation user input for saving the file.
        while True:
            filec = input("--:")
            if filec == "1": 
                break

            elif filec == "2":
                break
            else:
                print("Wrong input")

        # if user chooses 1: we will print the information on a file in a directory he chooses.
        if filec == "1":
            print("Where would you like to save the file? (enter file directory)")
            direc = input("--:")
            
            localwebservices_file = open(direc, "w+")
            localwebservices_file.write('Results for: ' + website_url + '\n')
            if data["ip"]:
                localwebservices_file.write(f'IP: {data["ip"]}\n')
            try:
                if data["hostname"]:
                    localwebservices_file.write(f'Hostname: {data["hostname"]}\n')
            except:
                pass
            if data["city"]:
                localwebservices_file.write(f'City: {data["city"]}\n')
            if data["region"]:
                localwebservices_file.write(f'Region: {data["region"]}\n')
            if data["country"]:
                localwebservices_file.write(f'Country: {data["country"]}\n')
            if data["loc"]:
                localwebservices_file.write(f'Geo location address: {data["loc"]}\n')
            if data["org"]:
                localwebservices_file.write(f'Organization: {data["org"]}\n')
            if data["timezone"]:
                localwebservices_file.write(f'Timezone: {data["timezone"]}\n')
            if ports:
                localwebservices_file.write(f'Open ports: {ports}\n') 
            if OS:
                localwebservices_file.write(f'Operating system: {OS} \n')       
            print("Data has been written successfuly!")
            localwebservices_file.close()
    except Exception as ex:
        print("Exception: " + str(ex))

    finally:
        print("Terminating...")
        time.sleep(1)

# scan ports (check the connection for the host on specific port)
def PortScan(ip, portnum):
    try:
        # create a new ipv4 socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as object:
            # check ip and port connection
            object.connect((ip, portnum))
            # appends open ports
            ports.append(portnum)
            print("port: ", portnum, " is open")
    except Exception as E:
        pass


def ScanPort_Thread(ip, Startport, endPort):
    try:
        
        for i in range(Startport, endPort + 1):
            # each iteration we will create a new thread that will be sent to the port scan method
            t = threading.Thread(target=PortScan, args=(ip, i))
            # thread starting point
            t.start()
        time.sleep(7)
        if ports: # if there are any ports open
            # for Local Host Scan
            if (str(ip_add_entered).startswith("192") | str(ip_add_entered).startswith("127") | str(
                    ip_add_entered).startswith("10")):

                print("\n\nwould you like to print the results in a file?")
                print("1: yes")
                print("2: no")
                while True:
                    filec = input("--:")
                    if filec == "1":
                        break

                    elif filec == "2":
                        break
                    else:
                        print("Wrong input")
                if filec == "1":
                    print("Where would you like to save the file? (enter file directory)")
                    direc = input("--:")
                    localwebservices_file = open(direc, "w+")
                    for i in ports:
                        localwebservices_file.write(f'Port {i} is opened \n')
                        # port_file.write(f"port {i} is opened\n")
                        socket.getservbyport(i)
                    print("Data has been written successfuly!")
        else: # Scan for website
            pass

    except Exception as ex:
        print("Exception: " + str(ex))

    finally:
        print("Terminating...")
        time.sleep(1)


# main
print(Fore.RED, artpost)
info()
print(Fore.LIGHTGREEN_EX)
print("What would you like to scan?")
print("1: Website")
print("2: Local host")
while True:
    choice = input("--: ")
    if choice == "1":
        break

    elif choice == "2":
        break
    else:
        print("Wrong input")

while True: # limiting user input.
    try:
        if choice == "1": # for scanning website 
            ip_add_entered = input("\nPlease enter website URL: ")
            website_url = ip_add_entered
            print("checking URL")
            ip_add_entered = socket.gethostbyname(ip_add_entered)
            # checking if the IP address is correct and public address
            if ipaddress.ip_address(ip_add_entered) and not IPAddress(ip_add_entered).is_private():
                print(ip_add_entered, "is valid ")
                break
            else:
                print("The URL address is wrong, please try again!")
        elif choice == "2":# for scanning Local Host
            ip_add_entered = input("\nPlease enter a local ip address: ")
            # checking if the IP address is correct and private address
            if ipaddress.ip_address(ip_add_entered) and IPAddress(ip_add_entered).is_private():
                print(ip_add_entered, "is valid ")
                break
            else:
                print("The IP address is wrong, please try again!")

    except Exception as ex:
        print("The IP address is wrong, please try again!")

    

if (choice == "1"): # For Scanning Website  
    try:

        ScanWeb(ip_add_entered)
    except Exception:
        print("Some error occurred while scanning")


elif choice == "2": # For Scanning Local Host 
    while True:
        print("please enter the range of ports to scan. ex: 30-60 ")
        port_range = input("enter port range: ")
        print("scanning ports..")
        time.sleep(1)
        # line 262 will remove any additional spaces
        port_range_valid = port_range_pattern.search(port_range.replace(" ", ""))
        # Port validation
        if port_range_valid:
            # if the range is valid we will split the 2 ranges so we can add them in the port list
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            #port = [port_min, port_max]
            break
    ScanPort_Thread(ip_add_entered, port_min, port_max)