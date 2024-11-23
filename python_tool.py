import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os
import threading
import requests
import getpass
import shutil
import re
import sv_ttk
cancel_event = threading.Event()
user_name = getpass.getuser()
if os.path.exists(f"/Users/{user_name}/pt_saved/update"):
    shutil.rmtree(f"/Users/{user_name}/pt_saved/update")
    os.system("kill Update")
VERSIONS = [
    "3.12.0",
    "3.12.1",
    "3.12.2",
    "3.12.3",
    "3.12.4",
    "3.12.5",
    "3.12.6",
    "3.11.0",
    "3.11.1",
    "3.11.2",
    "3.11.3",
    "3.11.4",
    "3.11.5",
    "3.11.6",
    "3.11.7",
    "3.11.8",
    "3.11.9",
    "3.10.0",
    "3.10.1",
    "3.10.2",
    "3.10.3",
    "3.10.4",
    "3.10.5",
    "3.10.6",
    "3.10.7",
    "3.10.8",
    "3.10.9",
    "3.10.10",
    "3.10.11",
    "3.9.0",
    "3.9.1",
    "3.9.2",
    "3.9.3",
    "3.9.4",
    "3.9.5",
    "3.9.6",
    "3.9.7",
    "3.9.8",
    "3.9.9",
    "3.8.0",
    "3.8.1",
    "3.8.2",
    "3.8.3",
    "3.8.4",
    "3.8.5",
    "3.8.6",
    "3.8.7",
    "3.8.8",
    "3.8.9",
    "3.8.10",
    "3.7.0",
    "3.7.1",
    "3.7.2",
    "3.7.3",
    "3.7.4",
    "3.7.5",
    "3.7.6",
    "3.7.7",
    "3.7.8",
    "3.7.9",
    "3.6.0",
    "3.6.1",
    "3.6.2",
    "3.6.3",
    "3.6.4",
    "3.6.5",
    "3.6.6",
    "3.6.7",
    "3.6.8",
    "3.5.0",
    "3.5.1",
    "3.5.2",
    "3.5.3",
    "3.5.4",
]
MIRROR_PYTHODOWLOADER = [
    #https://registry.npmmirror.com/-/binary/python/3.10.0
    #https://registry.npmmirror.com/-/binary/python/3.10.0/python-3.10.0-amd64.exe
    "python.org",
    "registry.npmmirror.com(China)"
]
PYTHONTOOL_DOWNLAOD = [
    "github.io",
    "github.com",
    "ghp.ci"
]


def check_python_installation(delay=3000):
    """
    检查Python3是否已安装。
    
    本函数尝试执行'python3 --version'命令来检查Python3的安装情况。
    如果命令执行出错，说明Python3未安装，则更新界面标签并禁用相关按钮。
    """
    try:
        # 执行命令并获取输出
        version_output = subprocess.check_output(["python3", "--version"], stderr=subprocess.STDOUT, text=True)
        
        # 验证输出是否包含预期的Python版本信息
        if "Python 3" not in version_output:
            raise ValueError("Unexpected Python version output: " + version_output.strip())
    except subprocess.CalledProcessError:
        # 如果命令执行失败，说明Python3未安装
        status_label.config(text="Python3 is not installed.")
        pip_upgrade_button.config(state="disabled")
        install_button.config(state="disabled")
        uninstall_button.config(state="disabled")
        
        # 延时指定时间后清除当前状态标签的文本
        root.after(delay, clear_a)
    except ValueError as e:
        # 处理其他异常，例如版本输出不符合预期
        status_label.config(text=str(e))
        root.after(delay, clear_a)

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
    """
    获取代理服务器的地址和端口，并返回一个包含代理信息的字典。

    从用户界面的输入框中读取代理服务器的地址和端口。如果地址或端口为空，
    或者端口不是一个有效的数字，则返回False。否则，将地址和端口格式化为
    一个代理字符串，并创建一个包含HTTP和HTTPS代理的字典。

    Returns:
        False: 如果地址或端口为空，或端口不是一个有效的数字。
        dict: 包含HTTP和HTTPS代理的字典。
    """
    # 获取用户输入的代理服务器地址和端口
    address = address_entry.get()
    port = port_entry.get()

    # 检查地址是否为空
    if not address:
        return False

    # 检查端口是否为空
    if not port:
        return False

    # 验证地址格式
    if not re.match(r'^[a-zA-Z0-9.-]+$', address):
        return False

    # 尝试将端口转换为整数，并构建代理字符串
    try:
        port = int(port)
        if port <= 0 or port > 65535:
            return False
        proxy = f"http://{address}:{port}"

        # 创建并返回包含代理信息的字典
        proxies = {
            "http": proxy,
            "https": proxy
        }
        return proxies
    except ValueError:
        return False
def get_url(des):
    if des==1:
        #selected version
        selected_version=version_combobox.get()

        selected=selected_version.split(".")

        selea=int(selected[1])
        if selea>=10:
            return f"https://www.python.org/ftp/python/{selected_version}/python-{selected_version}-macos11.pkg"
        elif selea<=6:
            return f"https://www.python.org/ftp/python/{selected_version}/python-{selected_version}-macosx10.6.pkg"
        else:
            return f"https://www.python.org/ftp/python/{selected_version}/python-{selected_version}-macosx10.9.pkg"
    elif des==2:
        return "https://githubtohaoyangli.github.io/info/info.json"
    elif des==3:
        return "https://githubtohaoyangli.github.io/download/python_tool/Mac/Latest/python_tool.dmg"
def download_file(destination_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    url = get_url(1)
    file_name = url.split("/")[-1]
    destination = os.path.join(destination_path, file_name)
    if os.path.exists(destination):
        os.remove(destination)

    def download(url, frame):
        download_pb['value'] = 0
        download_pb["maximum"] = 100
        proxie = proxies()
        response = requests.get(url, stream=True, proxies=proxie, headers=headers)
        file_size = int(response.headers.get('content-length', 0))
        with open(frame, "wb") as file:
            downloaded = 0
            chunk_size = 1024 * 100
            for data in response.iter_content(chunk_size=chunk_size):
                if cancel_event.is_set():
                    status_label.config(text="Download Interrupted!")
                    root.after(3000, clear_a)
                    return
                file.write(data)
                downloaded += len(data)
                percentage = (downloaded / file_size) * 100
                downloaded_mb = downloaded / (1024 * 1024)
                status_label.config(text=f"Downloading: {percentage:.3f}% | {downloaded_mb:.3f} MB | {file_size / (1024 * 1024):.3f} MB ｜ ")
                status_label.update()
                download_pb["value"] = percentage
                download_pb.update()
        status_label.config(text="Download Complete!")
        root.after(3000, clear_a)

    try:
        sav_ver()
        down_thread = threading.Thread(target=download, args=(url, destination), daemon=True)
        down_thread.start()
        cancel_download_button.config(state="enabled")
        down_thread.join()
        cancel_download_button.config(state="disabled")
    except Exception as e:
        status_label.config(text=f"Download Failed: {str(e)}")
        root.after(3000, clear_a)

# 中断下载函数
def cancel_download():
    cancel_event.set()
    status_label.config(text="Cancelling download...")
    download_pb['value'] = 0  # 重置进度条
    
    # 获取目标文件路径
    destination_path = destination_entry.get()
    url = get_url(1)
    file_name = url.split("/")[-1]
    destination = os.path.join(destination_path, file_name)
    
    # 检查目标文件是否存在，如果存在则删除
    if os.path.exists(destination):
        os.remove(destination)
        status_label.config(text="Download cancelled and incomplete file removed.")
    else:
        status_label.config(text="Download cancelled.")
    
    root.after(3000, clear_a)

# 下载版本函数
def download_selected_version():
    destination_path = destination_entry.get()

    if not os.path.exists(destination_path):
        status_label.config(text="Invalid path!")
        root.after(2000, clear_a)
        return

    cancel_event.clear()
    down_thread = threading.Thread(target=download_file, args=(destination_path,), daemon=True)
    down_thread.start()
status_label = None
upgrade_pip_button = None
root = None
pip_upgrade_button = None
def get_current_pip_version():
    """
    获取当前安装的 pip 版本。
    
    Returns:
        str: 当前 pip 版本号。
    """
    try:
        pip_version = subprocess.check_output(["pip3", "--version"]).decode().strip().split()[1]
        return pip_version
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to get current pip version.") from e
def update_pip_button_text():
    """
    更新 pip 升级按钮的文本。
    """
    def update_pip_button():
        
        try:
            current_version = get_current_pip_version()
            pip_upgrade_button.config(text=f"Upgrade pip: {current_version}")
        except Exception as e:
            pip_upgrade_button.config(text=f"Error: {str(e)}")
        # 每 5 秒钟再次调用此函数
        root.after(1000, update_pip_button_text)
    upbuthread=threading.Thread(target=update_pip_button, daemon=True)
    upbuthread.start()
    

def start_pip_version_update():
    """
    启动 pip 版本更新的定时任务。
    """
    update_pip_button_text()
def get_latest_pip_version():
    """
    获取最新可用的 pip 版本。
    
    Returns:
        str: 最新的 pip 版本号。
        

    """
    #/usr/local/opt/python@3.12/bin/python3.12 -m pip install --upgrade pip
    try:
        response = requests.get("https://pypi.org/pypi/pip/json")
        response.raise_for_status()
        latest_version = response.json()["info"]["version"]
        return latest_version
    except requests.RequestException as e:
        raise RuntimeError("Failed to get latest pip version.") from e

def update_pip(latest_version):
    """
    更新 pip 到最新版本。
    
    Args:
        latest_version (str): 最新的 pip 版本号。
    """
    try:
        up_pip=subprocess.run(["pip", "install", "--upgrade", "pip","--break-system-packages"], check=True)
        if "Successfully installed" in up_pip.stdout.decode():
            status_label.config(text=f"pip has been updated to {latest_version}")
            update_pip_button_text()
        else:
            status_label.config(text=f"Failed to update pip.:we don't know why")
            update_pip_button_text()
        root.after(3000, clear_a)
    except subprocess.CalledProcessError as e:
        try:
            up_pip=subprocess.run(["pip3", "install", "--upgrade", "pip","--break-system-packages"], check=True)
            if "Successfully installed" in up_pip.stdout.decode():
                status_label.config(text=f"pip has been updated to {latest_version}")
                update_pip_button_text()
            else:
                status_label.config(text=f"Failed to update pip.:we don't know why")
                update_pip_button_text()
            root.after(3000, clear_a)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to update pip.:{str(e)}") from e
        
def check_pip_version():
    """
    检查当前 pip 版本是否为最新版本，如果不是则进行更新。
    """
    upgrade_pip_button.config(state="disabled")
    try:
        current_version = get_current_pip_version()
        latest_version = get_latest_pip_version()

        if current_version != latest_version:
            status_label.config(text=f"Current pip version: {current_version}\nLatest pip version: {latest_version}\nUpdating pip...")
            update_pip(latest_version)
        else:
            status_label.config(text=f"pip is up to date: {current_version}")
            root.after(3000, clear_a)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
    finally:
        upgrade_pip_button.config(state="enabled")

def upgrade_pip():
    """
    启动一个线程来检查并更新 pip。
    """
    try:
        subprocess.check_output(["python3", "--version"])
        upgrade_thread = threading.Thread(target=check_pip_version, daemon=True)
        upgrade_thread.start()
    except FileNotFoundError:
        status_label.config(text="Python is not installed.")
        root.after(3000, clear_a)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        root.after(3000, clear_a)
def install_package():
    install_button.config(state="disabled")
    try:
        #pip freeze>python_modules.txt
        subprocess.check_output(["python3", "--version"])
        package_name = package_entry.get()
        
        def install_package_thread():  
            try:
                installed_packages = subprocess.check_output(["python3", "-m", "pip", "list", "--format=columns"], text=True)
                if package_name.lower() in installed_packages.lower():
                    status_label.config(text=f"Package '{package_name}' is already installed.")
                    root.after(3000,clear_a)
                else:
                    result = subprocess.run(["python3", "-m", "pip", "install", package_name], capture_output=True, text=True)
                    if "Successfully installed" in result.stdout:
                        status_label.config(text=f"Package '{package_name}' has been installed successfully!")
                        root.after(3000,clear_a)
                        #Requirement already satisfied
                    #elif "Requirement already satisfied" in result.stdout:
                        #status_label.config(text=f"Package '{package_name}' is already installed.")
                        #root.after(3000,clear_a)
                    else:
                        status_label.config(text=f"Error installing package '{package_name}': {result.stderr}")
                        root.after(3000,clear_a)
            except Exception as e:
                status_label.config(text=f"Error installing package '{package_name}': {str(e)}")
                root.after(3000,clear_a)
        install_thread = threading.Thread(target=install_package_thread,daemon=True)
        install_thread.start()
    except FileNotFoundError:
        status_label.config(text="Python is not installed.")
        root.after(3000,clear_a)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        root.after(3000,clear_a)
    install_button.config(state="enabled")
def uninstall_package():
    uninstall_button.config(state="disabled")
    try:
        subprocess.check_output(["python3", "--version"])
        package_name = package_entry.get()
        def uninstall_package_thread():
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
        uninstall_thread = threading.Thread(target=uninstall_package_thread, daemon=True)
        uninstall_thread.start()
    except FileNotFoundError:
        status_label.config(text="Python is not installed.")
        root.after(3000,clear_a)
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
        root.after(3000,clear_a)
    uninstall_button.config(state="enabled")
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
    def check_ver():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        # root.after(2000,clear_b)
        proxy = proxies()
        url = get_url(2)
        file_name = url.split("/")[-1]
        user_name = getpass.getuser()
        destination = f"/Users/{user_name}/pt_saved"
        
        try:
            os.mkdir(destination + "/" + "Update")
        except FileExistsError:
            pass
        response = requests.get(url, stream=True, proxies=proxy, headers=headers)
        file_size = int(response.headers.get('content-length', 0))
        #url = "http://githubtohaoyangli.github.io/info/info.json"
        r = requests.get(url, headers=headers,verify=False)
        latest_version = r.json()["releases"]["release1"]["version"]
        #if int(latest_version) >int(myver):
        
        return str(str(latest_version).split(".")[0]+","+str(latest_version).split(".")[1]+","+str(latest_version).split(".")[2]).split(",")
    def prepare_download():
        myver="1.1.0"
        myverl=str(myver).split(".")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        url=[str(get_url(3)),]
        try:
            check_pro['value']=0 
            check_pro["maximum"]=100
            proxie=proxies()
            if int(check_ver()[0]) > int(myverl[0]) or int(check_ver()[1]) > int(myverl[1]) or int(check_ver()[2]) > int(myverl[2]):
                r = requests.get(url, headers=headers,verify=False,stream=True,proxies=proxie)
                file_size = int(r.headers.get('content-length', 0))
                user=getpass.getuser()
                file_des=f"/Users/{user}/pt_saved/update/dumpdownload"
                if os.path.exists(f"/Users/{user}/pt_saved/update/dumpdownload")==False:
                    os.mkdir(f"/Users/{user}/pt_saved/update/dumpdownload")  
                if os.path.exists(file_des+"/python_tool")==False:
                    os.mkdir(file_des+"/python_tool")
                if os.path.exists(file_des+"/updater")==False:
                    os.mkdir(file_des+"/updater")
                des_pt=file_des+"/python_tool"
                des_updater=file_des+"/updater"
                def download(url,des):
                    with open(file_des, "wb") as file:
                        downloaded = 0
                        chunk_size = 1024*100
                        for data in r.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            downloaded += len(data)
                            percentage = (downloaded / file_size) * 100
                            downloaded_mb = downloaded / (1024*1024)
                            status_label.config(text=f"Downloading: {percentage:.3f}% | {downloaded_mb:.3f} MB | {file_size/(1024*1024):.3f} MB ｜ ")
                            status_label.update()
                            check_pro["value"]=percentage
                            check_pro.update()
            else:
                check.destroy()
        except Exception as e:
            lab.config(text=f"Error:{e}")
    def no():
        check.deiconify()

    check=tk.Tk()
    check.title("updater") 
    check_pro=ttk.Progressbar(check,length=200,mode="determinate")
    check_pro.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
    lab=ttk.Label(check,text="Checking for update....")
    lab.grid(row=1,column=0,columnspan=3,padx=10,pady=10)
    yes_bu=ttk.Button(check,text="Yes",command=prepare_download)
    yes_bu.grid(row=2,column=0,columnspan=3,padx=10,pady=10)
    yes_bu=ttk.Button(check,text="No",command=no)
    yes_bu.grid(row=2,column=0,columnspan=3,padx=10,pady=10)

    
    
    
    
    #root.deiconify()
    
    
        
def switch_theme():
    user_name = getpass.getuser()

    if switch.get():
        sv_ttk.set_theme("dark")
        if os.path.exists(f"/Users/{user_name}/pt_saved/") == False:
            os.mkdir(f"/Users/{user_name}/pt_saved/")
        if os.path.exists(f"/Users/{user_name}/pt_saved/theme/") == False:
            os.mkdir(f"/Users/{user_name}/pt_saved/theme")
        with open(f"/Users/{user_name}/pt_saved/theme/theme.txt", "w") as a:
            a.write("dark")
    else:
        sv_ttk.set_theme("light")
        if os.path.exists(f"/Users/{user_name}/pt_saved/") == False:
            os.mkdir(f"/Users/{user_name}/pt_saved/")
        if os.path.exists(f"/Users/{user_name}/pt_saved/theme/") == False:
            os.mkdir(f"/Users/{user_name}/pt_saved/theme")
        with open(f"/Users/{user_name}/pt_saved/theme/theme.txt", "w") as a:
            a.write("light")


def load_theme():
    try:
        user_name = getpass.getuser()
        with open(f"/Users/{user_name}/pt_saved/theme/theme.txt", "r") as r:
            theme = r.read()
        if theme == "dark":
            switch.set(True)
            sv_ttk.set_theme("dark")
        elif theme == "light":
            switch.set(False)
            sv_ttk.set_theme("light")
    except Exception:
        sv_ttk.set_theme("light")

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
select_button.grid(row=1, column=2, pady=10,padx=10)
#DOWNLOAD
download_button = ttk.Button(framea_tab, text="Download Selected Version", command=download_selected_version)
download_button.grid(row=2, column=0, columnspan=5, pady=10)
cancel_download_button = ttk.Button(framea_tab, text="Cancel Download", command=cancel_download, state="disabled")
cancel_download_button.grid(row=3, column=0, columnspan=3, pady=10)
#PIP(UPDRADE)
pip_upgrade_button = ttk.Button(framea_tab, text="Upgrade pip: Checking...", command=upgrade_pip)
pip_upgrade_button.grid(row=4, column=0, columnspan=3, pady=20)
upgrade_pip_button = pip_upgrade_button  # Alias for disabling/enabling later
package_label = ttk.Label(framea_tab, text="Enter Package Name:")
package_label.grid(row=5, column=0, pady=10)
package_entry = ttk.Entry(framea_tab, width=40)
package_entry.grid(row=5, column=1, pady=10)
#PIP(INSTALL)
install_button = ttk.Button(framea_tab, text="Install Package", command=install_package)
install_button.grid(row=6, column=0, columnspan=3, pady=10)
#PIP(UNINSTALL)
uninstall_button = ttk.Button(framea_tab, text="Uninstall Package", command=uninstall_package)
uninstall_button.grid(row=7, column=0, columnspan=3, pady=10)
#progressbar-options:length(number),mode(determinate(从左到右)，indeterminate(来回滚动)),...length=500,mode="indeterminate"
download_pb=ttk.Progressbar(framea_tab,length=500,mode="determinate")
download_pb.grid(row=8,column=0,pady=20,columnspan=3)
#TEXT(TAB1)
status_label = ttk.Label(framea_tab, text="", padding="10")
status_label.grid(row=9, column=0, columnspan=3)
#SETTINGS TAB
fsetting = ttk.Frame(root, padding="20")
tab_control.add(fsetting,text="Settings")
tab_control.pack(expand=1, fill='both', padx=10, pady=10)
frameb_tab = ttk.Frame(fsetting)
frameb_tab.pack(padx=20, pady=20)

address=ttk.Label(frameb_tab,text="Address:")
address.grid(row=1,column=0,padx=10,pady=10)

address_entry=ttk.Entry(frameb_tab,width=15)
address_entry.grid(row=1,column=1,columnspan=2,pady=10)

port=ttk.Label(frameb_tab,text="Port:")
port.grid(row=2,column=0,padx=0,pady=10)

port_entry=ttk.Entry(frameb_tab,width=5)
port_entry.grid(row=2,column=1,pady=10,columnspan=2)

sav=ttk.Button(frameb_tab,text="Apply",command=save)
sav.grid(row=3,column=0,padx=10,pady=10,columnspan=3)


switch = tk.BooleanVar()  # 创建一个BooleanVar变量，用于检测复选框状态
themes = ttk.Checkbutton(frameb_tab, text="dark mode", variable=switch, style="Switch.TCheckbutton",command=switch_theme)
themes.grid(row=5,column=0,padx=10,pady=10,columnspan=3)

sav_label = ttk.Label(frameb_tab, text="")
sav_label.grid(row=6, column=0,columnspan=3)
#update(not available)
top=tk.Menu(root)
menucheck = tk.Menu(top)
top.add_cascade(label='Menu',menu=menucheck)
menucheck.add_command(label="Check for update",command=update_pt)
root.config(menu=top)
load()
load_theme()
# Set sv_ttk theme
update_pip_button_text()
check_python_installation()
root.resizable(False,False)
root.mainloop()
#root.after(3000,)