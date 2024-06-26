import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os
import threading
import requests
from tqdm.tk import trange,tqdm
import getpass
import zipfile
import time
import shutil
VERSIONS = [
    "3.12.0",
    "3.11.0",
    "3.10.0",
    "3.9.0",
    "3.8.0",
    "3.7.0",
    "3.6.0",
    "3.5.0"
]
def clear_a():
    status_label.config(text="")
def clear_b():
    sav_label.config(text="")
def select_destination():
    destination_path = filedialog.askdirectory()
    if destination_path:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, destination_path)
def proxies():
    address=address_entry.get()
    port=port_entry.get()
    if address=="":
        return False
    elif port=="":
        return False
    else:
        try:
            int(port)
            proxy = f"http://{address}:{port}"
            proxies = {
                        "http":proxy,
                        "https":proxy
                    }
            return proxies
        except Exception:
            return False
def download_file(selected_version, destination_path):
    def get_url():        
        selected=selected_version.split(".")
        sele=len(selected)
        selea=int(selected[1])
        if selea>=10:
            return f"https://www.python.org/ftp/python/{selected_version}/python-{selected_version}-macos11.pkg"
        elif selea<=6:
            return f"https://www.python.org/ftp/python/{selected_version}/python-{selected_version}-macosx10.6.pkg"
        else:
            return f"https://www.python.org/ftp/python/{selected_version}/python-{selected_version}-macosx10.9.pkg"
    url=get_url()
    file_name = url.split("/")[-1]
    destination = os.path.join(destination_path,file_name)
    if os.path.exists(destination):
        os.remove(destination)    
    def download(url,frame):        
        # 发送 GET 请求并流式处理
        proxie=proxies()
        response = requests.get(url, stream=True
                                ,proxies=proxie)
        # 获取文件大小（如果可用）
        file_size = int(response.headers.get('content-length', 0))
        # 输出文件名
        #file_name = url.split("/")[-1]        
        with open(frame, "wb") as file:
            downloaded = 0
            chunk_size = 1024*1024
            
            for data in response.iter_content(chunk_size=chunk_size):
                start_time=None
                #nonlocal start_time
                file.write(data)
                downloaded += len(data)
                percentage = (downloaded / file_size) * 100
                downloaded_mb = downloaded / (1024*1024)               
                status_label.config(text=f"Downloading: {percentage:.3f}% | {downloaded_mb:.3f} MB | {file_size/(1024*1024):.3f} MB ")
                status_label.update()
            install_thread = threading.Thread(target=download)
            install_thread.start()
    def sav_ver():
        user_name = getpass.getuser()
        version_len=len(VERSIONS)
        get=version_combobox.get()     
        for i in range(version_len):
            if get in VERSIONS[i]:
                if os.path.exists(f"/Users/{user_name}/pt_saved/")==False:
                    os.mkdir(f"/Users/{user_name}/pt_saved/")
                with open(f"/Users/{user_name}/pt_saved/version.txt","w") as wri:
                    wri.write(get)
    try:
        sav_ver()
        download(url,destination)
        status_label.config(text="Download Complete!")
        
        root.after(3000,clear_a)
    except Exception as e:
        status_label.config(text=f"Download Failed: {str(e)}")
        root.after(3000,clear_a)


def check_pip_version():
    try:
        pip_version = subprocess.check_output(["pip3", "--version"]).decode().strip().split()[1]
        r = requests.get("https://pypi.org/pypi/pip/json")
        latest_version = r.json()["info"]["version"]

        if pip_version != latest_version:
            status_label.config(text=f"Current pip version: {pip_version}\nLatest pip version: {latest_version}\nUpdating pip...")
            subprocess.run(["python3", "-m", "pip", "install", "--upgrade", "pip"])
            status_label.config(text="pip has been updated!")
            root.after(3000,clear_a)
        else:
            status_label.config(text=f"pip is up to date: {pip_version}")
            root.after(3000,clear_a)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

def download_selected_version():
    selected_version = version_combobox.get()
    destination_path = destination_entry.get()
    
    if not os.path.exists(destination_path):
        status_label.config(text="Invalid path!")
        root.after(2000,clear_a)
        return
    
    download_thread = threading.Thread(target=download_file, args=(selected_version, destination_path))
    download_thread.start()

def upgrade_pip():
    try:
        subprocess.check_output(["python3", "--version"])
        check_pip_version()
    except FileNotFoundError:
        status_label.config(text="Python is not installed.")
        root.after(3000,clear_a)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        root.after(3000,clear_a)
def install_package():
    try:
        #pip freeze>python_modules.txt
        subprocess.check_output(["python3", "--version"])
        package_name = package_entry.get()
        
        def install_package_thread():  
            try:
                result = subprocess.run(["python3", "-m", "pip", "install", package_name], capture_output=True, text=True)
                if "Successfully installed" in result.stdout:
                    status_label.config(text=f"Package '{package_name}' has been installed successfully!")
                    root.after(3000,clear_a)
                    #Requirement already satisfied
                elif "Requirement already satisfied" in result.stdout:
                    status_label.config(text=f"Package '{package_name}' is already installed.")
                    root.after(3000,clear_a)
                else:
                    status_label.config(text=f"Error installing package '{package_name}': {result.stderr}")
                    root.after(3000,clear_a)
            except Exception as e:
                status_label.config(text=f"Error installing package '{package_name}': {str(e)}")
                root.after(3000,clear_a)
        install_thread = threading.Thread(target=install_package_thread)
        install_thread.start()
    except FileNotFoundError:
        status_label.config(text="Python is not installed.")
        root.after(3000,clear_a)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        root.after(3000,clear_a)
def uninstall_package():
    try:
        subprocess.check_output(["python3", "--version"])
        package_name = package_entry.get()       
        try:
            installed_packages = subprocess.check_output(["python3", "-m", "pip", "list", "--format=columns"], text=True)
            if package_name.lower() in installed_packages.lower():
                result = subprocess.run(["python3", "-m", "pip", "uninstall", "-y", package_name], capture_output=True, text=True)
                if "Successfully uninstalled" in result.stdout:
                    status_label.config(text=f"Package '{package_name}' has been uninstalled successfully!")
                    root.after(3000,clear_a)
                else:
                    status_label.config(text=f"Cannot uninstall package '{package_name}': {result.stderr}")
                    root.after(3000,clear_a)
            else:
                status_label.config(text=f"Package '{package_name}' is not installed.")
                root.after(3000,clear_a)
        except Exception as e:
            status_label.config(text=f"Error uninstalling package '{package_name}': {str(e)}")
            root.after(3000,clear_a)
    except FileNotFoundError:
        status_label.config(text="Python is not installed.")
        root.after(3000,clear_a)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        root.after(3000,clear_a)
def check_python_installation():
    try:
        subprocess.check_output(["python3", "--version"])
    except Exception:
        status_label.config(text="Python3 is not installed.")
        pip_upgrade_button.config(state="disabled")
        install_button.config(state="disabled")
        uninstall_button.config(state="disabled")
        root.after(3000,clear_a)
def load():
    user_name = getpass.getuser() 
    if os.path.exists(f"/Users/{user_name}/pt_saved/proxy.txt"):
        with open(f"/Users/{user_name}/pt_saved/proxy.txt","r") as re:
            ree=re.readlines()
            reee=len(ree)
            for i in range(reee):
                if "address:" in ree[i]:
                    add=ree[i].split(":")
                    addlen=len(add)
                    address=add[addlen-1]
                    address=address.strip()
                    address_entry.insert(0,address)
                if "port" in ree[i]:
                    poo=ree[i].split(":")
                    poolen=len(poo)
                    port=poo[poolen-1]
                    port=port.strip()
                    port_entry.insert(0,port)
    else:
        address_entry.insert(0,"")
        port_entry.insert(0,"")
def save():
    address=address_entry.get()
    port=port_entry.get()
    try:
        user_name = getpass.getuser() 
        if os.path.exists(f"/Users/{user_name}/pt_saved/proxy.txt"):
            os.remove(f"/Users/{user_name}/pt_saved/proxy.txt")
        if os.path.exists(f"/Users/{user_name}/pt_saved/")==False:
            os.mkdir(f"/Users/{user_name}/pt_saved/")
        with open(f"/Users/{user_name}/pt_saved/proxy.txt","w")as wr:
            wr.write(f"address:{address}\n")
            wr.write(f"port:{port}\n")
            sav_label.config(text="Proxy settings has been saved successfully!")
            root.after(1000,clear_b)
    except Exception as e:
        sav_label.config(text=f"Error: Cannot save proxy settings {str(e)}")
        root.after(1000,clear_b)
def load_com():
    #f"/Users/{user_name}/pt_saved/"
    try:
        user_name = getpass.getuser()
        version_len=len(VERSIONS)
        with open(f"/Users/{user_name}/pt_saved/version.txt","r") as r:
            re=r.read()
        for i in range(version_len):
            if re in VERSIONS[i]:
                return int(i)
    except Exception:
        return 0
user_name = getpass.getuser()
def update_pt():
    try:
        try:
            user_name = getpass.getuser()
            proxie=proxies()
            #https://github.com/githubtohaoyangli/python_tool_update/releases/download/1.x/version.txt
            my_version="1.0.2"
            if os.path.exists(f"/Users/{user_name}/pt_saved/update"):
                shutil.rmtree(f"/Users/{user_name}/pt_saved/update")
            os.mkdir(f"/Users/{user_name}/pt_saved/update")
            ge="https://github.com/githubtohaoyangli/python_tool_update/releases/download/1.x/version.txt"
            r=requests.get(ge,proxies=proxie)
            sav_label.config(text="Getting....")
            with open(f"/Users/{user_name}/pt_saved/update/version.txt","wb")as down:
                down.write(r.content)
            with open (f"/Users/{user_name}/pt_saved/update/version.txt","r") as re:
                latest_version=re.read()
            if latest_version > my_version:
                try:
                    os.remove(f"/Users/{user_name}/pt_saved/update/version.txt")
                    #https://github.com/githubtohaoyangli/python_tool/releases/download/1.0.1/python_tool.exe
                    url=f"https://github.com/githubtohaoyangli/python_tool/releases/download/{latest_version}/python_tool_mac.zip"
                    file_name = url.split("/")[-1]
                    
                    do=requests.get(url,stream=True,proxies=proxie)
                    os.mkdir(f"/Users/{user_name}/pt_saved/update/soc")
                    with open(f"/Users/{user_name}/pt_saved/update/soc/{file_name}", "wb") as file:
                        downloaded = 0
                        chunk_size = 1024*1024
                        file_size = int(do.headers.get('content-length', 0))
                        for data in do.iter_content(chunk_size=chunk_size):
                            #nonlocal start_time
                            file.write(data)
                            downloaded += len(data)
                            percentage = (downloaded / file_size) * 100
                            status_label.config(text=f"Downloading: {percentage:.2f}%")
                            status_label.update()
                    f=zipfile.ZipFile(f"/Users/{user_name}/pt_saved/update/soc/python_tool_mac.zip","r")
                    sav_label.config(text="Extracting...")
                    f.extractall()
                    time.sleep(0.5)
                    for i in range(5):
                        a=5
                        sav_label.config(text=f"You're getting ready! {a}seconds.....,then restart.")
                        time.sleep(1)
                        a-=1
                        sav_label.update()
                    os.system(f"cd /Users/{user_name}/pt_saved/update/soc/python_tool_mac")
                    os.system("update")
                    exit(0)
                except Exception as ea:
                    sav_label.config(text=f"Download/Install Failed: {str(ea)}")
                    root.after(2000,clear_b)
            else:
                sav_label.config(text="python_tool is up to date!")
                root.after(2000,clear_b)
        except Exception as e:
            sav_label.config(text=f"Getting Failed:{str(e)}")
            root.after(2000,clear_b)
    except Exception as a:
        sav_label.config(text=f"Cannot update:{str(a)}")
        root.after(2000,clear_b)
#GUI
root = tk.Tk()
root.title("Python Tool")
#TAB CONTROL
tab_control = ttk.Notebook(root)
#MODE TAB
fmode = ttk.Frame(root, padding="20")
tab_control.add(fmode,text="Mode")
tab_control.pack(expand=1, fill='both', padx=10, pady=10)
framea_tab = ttk.Frame(fmode)
framea_tab.pack(padx=20, pady=20)
#PYTHON VERSION
version_label = ttk.Label(framea_tab, text="Select Python Version:")
version_label.grid(row=0, column=0, pady=10)
selected_version = tk.StringVar()
version_combobox = ttk.Combobox(framea_tab, textvariable=selected_version, values=VERSIONS, state="read")
version_combobox.grid(row=0, column=1, pady=10)
ins=load_com()
version_combobox.current(ins)
#SAVE PATH
destination_label = ttk.Label(framea_tab, text="Select Destination:")
destination_label.grid(row=1, column=0, pady=10)
destination_entry = ttk.Entry(framea_tab, width=40)
destination_entry.grid(row=1, column=1, pady=10)
select_button = ttk.Button(framea_tab, text="Select", command=select_destination)
select_button.grid(row=1, column=2, pady=10)
#DOWNLOAD
download_button = ttk.Button(framea_tab, text="Download Selected Version", command=download_selected_version)
download_button.grid(row=2, column=0, columnspan=5, pady=10)
#PIP(UPDRADE)
pip_upgrade_button = ttk.Button(framea_tab, text="Upgrade pip", command=upgrade_pip)
pip_upgrade_button.grid(row=3, column=0, columnspan=3, pady=20)
upgrade_pip_button = pip_upgrade_button  # Alias for disabling/enabling later
package_label = ttk.Label(framea_tab, text="Enter Package Name:")
package_label.grid(row=4, column=0, pady=10)
package_entry = ttk.Entry(framea_tab, width=40)
package_entry.grid(row=4, column=1, pady=10)
#PIP(INSTALL)
install_button = ttk.Button(framea_tab, text="Install Package", command=install_package)
install_button.grid(row=5, column=0, columnspan=3, pady=10)
#PIP(UNINSTALL)
uninstall_button = ttk.Button(framea_tab, text="Uninstall Package", command=uninstall_package)
uninstall_button.grid(row=6, column=0, columnspan=3, pady=10)
#TEXT(TAB1)
status_label = ttk.Label(framea_tab, text="", padding="10")
status_label.grid(row=8, column=0, columnspan=3)
#SETTINGS TAB
fsetting = ttk.Frame(root, padding="20")
tab_control.add(fsetting,text="Settings")
tab_control.pack(expand=1, fill='both', padx=10, pady=10)
frameb_tab = ttk.Frame(fsetting)
frameb_tab.pack(padx=20, pady=20)
proxy_label=ttk.Label(frameb_tab,text="Download Proxy(HTTP/HTTPS)")
proxy_label.grid(row=0,column=1,padx=17,pady=10)
address=ttk.Label(frameb_tab,text="Address:")
address.grid(row=1,column=0,padx=0,pady=10)
address_entry=ttk.Entry(frameb_tab,width=15)
address_entry.grid(row=1,column=8,padx=0,pady=10)
port=ttk.Label(frameb_tab,text="Port:")
port.grid(row=2,column=0,padx=0,pady=5)
port_entry=ttk.Entry(frameb_tab,width=5)
port_entry.grid(row=2,column=8,padx=0,pady=5)
sav=ttk.Button(frameb_tab,text="Apply",padding="1",command=save)
sav.grid(row=3,column=1,padx=10,pady=0)
update_b=ttk.Button(frameb_tab,text="update pt",command=update_pt,padding="4")
update_b.grid(row=4,column=1,pady=10,padx=100)
sav_label = ttk.Label(frameb_tab, text="")
sav_label.grid(row=5, column=1)
load()

check_python_installation()
root.mainloop()
#root.after(3000,)