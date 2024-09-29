from __future__ import annotations
import requests
import multitasking
import signal
import tkinter as tk
from tkinter import ttk
import threading
# 导入 retry 库以方便进行下载出错重试
from retry import retry
signal.signal(signal.SIGINT, multitasking.killall)
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
# 定义 1 MB 多少为 B
def get_file_name(url):
    file_name=str(str(url).split("/")[-1])
    return str(file_name)
    
MB = 1024**2
def split(start: int, end: int, step: int) -> list[tuple[int, int]]:
    # 分多块
    parts = [(start, min(start+step, end))
             for start in range(0, end-1, step)]
    return parts
def get_file_size(url: str, raise_error: bool = False) -> int:
    response = requests.head(url,verify=False
                             )
    file_size = response.headers.get('Content-Length')
    if file_size is None:
        if raise_error is True:
            raise ValueError('Cannot download because "Content-Length" is None.')
        return file_size
    return int(file_size)

def download_t():
    try:
        url = 'https://github.com/githubtohaoyangli/python_tool/releases/download/1.0.2/python_tool.dmg'
        #file_name = str(str(url).split("/")[-1])
        file_name=get_file_name(url)
        button.config(state="disabled")
        def download(url: str, file_name: str, retry_times: int = 3, each_size=16*MB) -> None:
            try:
                f = open(file_name, 'wb')
                file_size = get_file_size(url)
                @retry(tries=retry_times)
                @multitasking.task
                def start_download(start: int, end: int) -> None:
                    try:
                        downloaded=0
                        _headers = headers.copy()
                        # 分段下载的核心
                        _headers['Range'] = f'bytes={start}-{end}'
                        # 发起请求并获取响应（流式）
                        response = session.get(url, headers=_headers, stream=True,allow_redirects=True,verify=False)
                        # 每次读取的流式响应大小
                        chunk_size = 128*1024
                        # 暂存已获取的响应，后续循环写入
                        chunks = []
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            # 暂存获取的响应
                            chunks.append(chunk)
                            downloaded+=chunk_size
                            progressbar['value']+=chunk_size
                            progressbar.update()
                            lab.config(text=f"{progressbar['value']/(1024**2):.2f}/{file_size/(1024**2):.2f}")
                        f.seek(start)
                        for chunk in chunks:
                            f.write(chunk)
                        # 释放已写入的资源
                        del chunks
                    except Exception as b:
                        lab.config(text=f"error:{str(b)}")
                        button.config(state="enabled")
            except Exception as a:
                lab.config(text=f"error:{str(a)}")
                button.config(state="enabled")
            session = requests.Session()
            # 分块文件如果比文件大，就取文件大小为分块大小
            try:
                each_size = min(each_size, file_size)
            except TypeError as type:
                button.config(state="enabled")
                raise TypeError(f"{type}")
            # 分块
            parts = split(0, file_size, each_size)
            print(f'分块数：{len(parts)}')
            # 创建进度条
            progressbar['value']=0 
            
            file_size = get_file_size(url)
            progressbar["maximum"]=file_size
            downloaded=0
            for part in parts:
                start, end = part
                #start_download(start, end)
                tdownload_thread=threading.Thread(target=start_download,args=(start,end),daemon=True)
                tdownload_thread.start()
            # 等待全部线程结束
            multitasking.wait_for_tasks()
            f.close()
            progressbar['value']=file_size
            lab.config(text="Download Complate!")
            button.config(state="enabled")
        download_thread=threading.Thread(target=download,args=(url,file_name),daemon=True)
        download_thread.start()
    except Exception as e:
        lab.config(text=f"error:{e}")
        button.config(state="enabled")
def downloading():
    try:
        downth=threading.Thread(target=download_t,daemon=True
                                )
        downth.start()
    except Exception as e:
        lab.config(text="retrying...")
root=tk.Tk()
root.title("downloader")

button=ttk.Button(root,width=10,command=download_t,text="download")
button.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
progressbar=ttk.Progressbar(root,length=200,mode="determinate")
progressbar.grid(row=1,column=0,columnspan=3,padx=10,pady=10)
lab=ttk.Label(root,text="")
lab.grid(row=2,column=0,columnspan=3,padx=10,pady=10)
if "__main__" == __name__:
    root.mainloop()