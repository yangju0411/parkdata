import pandas as pd
import numpy as np

import sys 
from tkinter import * 
from tkinter import filedialog



root = Tk()
t1 = Text(root) 
t1.pack(side = LEFT)

canvas = Canvas(root)
canvas.pack(side = RIGHT)

#-------------------------------------------------
def domenu():
    print("OK")
    
# 파일 여는 부분
def open():
    def file_path():
        filepath = filedialog.askopenfilename(initialdir="./", title="Select file",
                                          filetypes=(("csv files", "*.csv"),
                                          ("all files", "*.*")))
        path_label.config(text = filepath)
    
    def open_exit():
        filepath = path_label.cget("text")
        report(filepath)
        df = pd.read_csv(filepath)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            report(df)
        
            
    open_menu = Toplevel()
    open_menu.title("파일 열기")
    open_menu.geometry("500x250")
    
    path_bt = Button(open_menu, text = "열기", command = file_path)
    path_label = Label(open_menu, text = "파일의 경로가 표시됩니다.")
    exit_bt = Button(open_menu, text = "확인", command = open_exit)
    
    
    path_label.pack(side = LEFT)
    path_bt.pack(side = RIGHT)
    exit_bt.pack(side = BOTTOM)

#--------------------------------------------------------------------------------

# Statistics 동작
def descript():
    print("OK")
def ttest():
    print("OK")
def lr():
    print("OK")
def pca():
    print("OK")

#메뉴 프로그래밍
menubar = Menu(root)                                # 윈도우에 메뉴바 추가
filemenu = Menu(menubar, tearoff=0)                 # 상위 메뉴 탭 항목 추가
menubar.add_cascade(label="File", menu=filemenu)    # 상위 메뉴 탭 설정  # 항목 추가
filemenu.add_command(label="Open", command=open)
filemenu.add_separator()                            # 분리선 추가
filemenu.add_command(label="Exit", command = root.destroy)

statisticsmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Statistics", menu=statisticsmenu)
statisticsmenu.add_command(label="Descriptive Statistics", command=descript)
statisticsmenu.add_command(label="T-test", command=ttest)
statisticsmenu.add_command(label="Linear Regression", command=lr)
statisticsmenu.add_command(label="Principal Component Analysis", command=pca)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=domenu)

root.config(menu=menubar) 
#--------------------------------------------------------

def report(s):
    t1.insert(CURRENT, s)
    t1.insert(CURRENT, "\n")    
 
report("csv 파일을 열어주세요.")

mainloop()