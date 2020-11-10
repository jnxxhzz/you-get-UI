#pyinstaller -i C:\Users\admin\Desktop\video\favicon.ico -F --path=C:\Users\admin\AppData\Local\Programs\Python\Python38\Lib\site-packages --hidden-import=you_get.extractors --hidden-import=you_get.cli_wrapper --hidden-import=you_get.processor --hidden-import=you_get.utl video.py
import re
import sys
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import tkinter.messagebox as msgbox
import webbrowser
import you_get
from icon import Icon
import base64

class Download:
    # construct
    def selectPath(self):
    	path_=askdirectory()
    	self.path.set(path_)
    
    def __init__(self, width=400, height=170):
        self.w = width
        self.h = height
        self.title = '视频下载'
        self.root = tk.Tk(className=self.title)
        self.url = tk.StringVar()
        self.start = tk.IntVar()
        self.end = tk.IntVar()
        self.path = tk.StringVar()
        self.path.set('D:/')
        
        # 以下是图标文件，没有则注释掉
        with open('tmp.ico','wb') as tmp:
            tmp.write(base64.b64decode(Icon().img))
        self.root.iconbitmap('tmp.ico')
        os.remove('tmp.ico')
        # 图标文件结束

        # define frame
        frame_1 = tk.Frame(self.root)
        frame_2 = tk.Frame(self.root)
        frame_3 = tk.Frame(self.root)
        frame_4 = tk.Frame(self.root)
 
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        menu1 = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='选项', menu=menu1)
        menu1.add_command(label='关于我', command=lambda: webbrowser.open('https://blog.csdn.net/jnxxhzz'))
        menu1.add_command(label='退出', command=lambda: self.root.quit())
 
        # set frame_1
        label1 = tk.Label(frame_1, text='输入视频链接：')
        entry_url = tk.Entry(frame_1, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=35)

        # set frame_3
        label2 = tk.Label(frame_2, text='视频输出地址：')
        entry_path = tk.Entry(frame_2, textvariable=self.path, highlightcolor='Fuchsia', highlightthickness=1, width=35)
        
        # set frame_2
        path = tk.StringVar()
        url_path = tk.Button(frame_3, text = "路径选择", font=('楷体', 12), fg='black', width=3, height=-1, command = self.selectPath)
        down = tk.Button(frame_3, text='下载', font=('楷体', 12), fg='black', width=3, height=-1,
                         command=self.video_download)
        
        label_desc = tk.Label(frame_4, fg='red', font=('楷体', 12),
                              text='注意：请勿移作商用！')
        label_jnxxhzz = tk.Label(frame_4, fg='red', font=('楷体', 10),
                              text='--by jnxxhzz')
 
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        frame_4.pack()
 
        label1.grid(row=0, column=0)
        entry_url.grid(row=0, column=1)
 
        label2.grid(row=1, column=0,pady=10)
        entry_path.grid(row=1, column=1,pady=10)	
        
        url_path.grid(row=1,column=0, ipadx=20,padx = 5)
        down.grid(row=1, column=3, ipadx=20)
        
        label_desc.grid(row=1, column=0)
        label_jnxxhzz.grid(row=2, column=0)

    
    def video_download(self):
        url = self.url.get()
        path = self.path.get()
        if re.match(r'^https?:/{2}\w.+$', url):
            if path != '':
                msgbox.showwarning(title='警告', message='下载过程中窗口如果出现短暂卡顿说明文件正在下载中！')
                try:
                    self.root.withdraw()
                    sys.argv = ['you-get', '-o', path, url]
                    you_get.main()
                except Exception as e:
                    msgbox.showerror(title='警告', message=e)

                msgbox.showinfo(title='成功', message='下载完成！')
                self.root.wm_deiconify()
            else:
                msgbox.showerror(title='警告', message='输出地址错误！')
                self.root.wm_deiconify()
        else:
            msgbox.showerror(title='警告', message='视频地址错误！')
            self.root.wm_deiconify()
 
    def center(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = int((ws / 2) - (self.w / 2))
        y = int((hs / 2) - (self.h / 2))
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))
 
    def event(self):
        self.root.resizable(False, False)
        self.center()
        self.root.mainloop()
 
 
if __name__ == '__main__':
    app = Download()
    app.event()