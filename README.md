# you-get-UI
用 tkinter 实现的 you-get 的 简单UI 界面

具体的实现过程可以查看
https://blog.csdn.net/jnxxhzz/article/details/109597944

这里可以使用 11.py 文件将命名为 pen.ico 的图标文件进行编码然后生成 icon.py 文件用于导入图标文件

video.py 即为主文件


@[toc]

## github地址
[https://github.com/jnxxhzz/you-get-UI](https://github.com/jnxxhzz/you-get-UI)

##  实现思路
you-get 库是命令行下非常常用的下载视频的命令，但是由于很多时候很多人总是会来问你，B 站视频怎么下载，啥啥啥视频怎么下载，你能不能帮我下载一下...

苦于这么频繁的被问所以索性写个简单的 UI 界面打包一下 you-get 库给别人下载视频用
那么首先在命令行里是叫 you-get ，但是在在代码中可以发现名字是叫做 you_get ，python 的库不允许用 - 只能用 _

具体的实现其实没什么好讲的...用 tkinter 实现一下界面，然后用 sys.argv 手动添加输入内容，也就是 you-get 的基本格式:  `you-get -o 保存地址 视频连接` ，调用 you_get.main() 即可

## pyinstaller 打包成 exe
实现过程中最麻烦的其实不是代码的实现，代码的实现还是简单的

最麻烦的在于用 pyintaller 打包，首先给出 pyinstaller 打包的命令，主要是需要额外打包几个库，否则直接打包就会发现没有办法运行
```cpp
#pyinstaller -F --path=C:\Users\admin\AppData\Local\Programs\Python\Python38\Lib\site-packages --hidden-import=you_get.extractors --hidden-import=you_get.cli_wrapper --hidden-import=you_get.processor --hidden-import=you_get.utl video.py
```
这里解释一下，首先 --path 是指向你的 python 第三方库中 you-get 所在的目录，这样才能找到后面需要的
`you_get.extractors，you_get.cli_wrapper，you_get.processor，you_get.utl` 这个几个库，如果没有引入这几个库的话会发现直接运行代码是可以的，但是打包以后 exe 文件直接运行就会无效

这个应该是 you-get 二次开发打包成 exe 最麻烦的问题了，我也找了很久问题....最后才找到解决办法

然后这里打包成 exe 时没有隐藏命令行，因为没有写映射，所以如果隐藏了命令行那代码运行的时候会出现未响应，所以想了一下索性还是下载时把 UI 隐藏直接给用户看命令行里的读条比较好..

## UI 左上角图标
因为用的是 tkinter 所以 UI 界面左上角的图标默认是一个小羽毛，而这个图标是可以改的，但是因为同时要使用 pyinstaller 打包，那就意味着要么把图标文件打包进去，要么就必须把图标文件放在 exe 旁边否则就会报错。
这里给出一个比较简单的可以直接把图标文件写入代码中的方法
因为图标文件不大，所以可以将图标文件进行编码然后直接 import
将图标文件命名为 `pen.ico` 然后放在以下这份代码同目录下，运行下面这份代码会产生一个 `icon.py` 文件
将 `icon.py` 文件放在下面主代码 `video.py` 的目录下直接使用 `from icon import Icon` 导入即可
```python
import base64
with open("icon.py","a") as f:
    f.write('class Icon(object):\n')
    f.write('\tdef __init__(self):\n')
    f.write("\t\tself.img='")
with open("pen.ico","rb") as i:
    b64str = base64.b64encode(i.read())
    with open("icon.py","ab+") as f:
        f.write(b64str)
with open("icon.py","a") as f:
    f.write("'")
```
然后通过以下这段代码每次运行时先通过编码文件翻译成图片保存，设置为图标后删除图片文件
```python
with open('tmp.ico','wb') as tmp:
	tmp.write(base64.b64decode(Icon().img))
self.root.iconbitmap('tmp.ico')
os.remove('tmp.ico')
```
这样就不需要解决图片需要打包的问题了

## 运行效果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201110143255141.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2pueHhoeno=,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201110143315434.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2pueHhoeno=,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201110143325449.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2pueHhoeno=,size_16,color_FFFFFF,t_70#pic_center)

## 代码

```python
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
```
