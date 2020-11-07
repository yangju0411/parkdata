import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tkinter import * 
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


root = Tk()
root.geometry('1920x1080')
t1 = Text(root, width = 1920, height = 1080)
t1.pack(side = LEFT)

'''
fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side = RIGHT)
'''
#-------------------------------------------------
def domenu():
    print("OK")
    
# 파일 여는 부분
def open():
    filepath = filedialog.askopenfilename(initialdir="./", title="Select file",
                                          filetypes=(("csv files", "*.csv"),
                                          ("all files", "*.*")))
    report(filepath)
    global df # 불러온 데이터프레임을 전역으로 설정함
    df = pd.read_csv(filepath)
    
    open_csv = Toplevel()
    open_csv.title(filepath)
    print_csv = Text(open_csv)
    print_csv.pack()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print_csv.insert(CURRENT, df)
    

#--------------------------------------------------------------------------------

# Statistics 동작
def descript():
    try:
        def descript_ok():
            vars = list(var_list.curselection()) # curselection은 튜플 반환하므로 리스트로 변경
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                report(df.iloc[:,vars].describe())
            
        variables = df.columns
        descript_menu = Toplevel()
        descript_menu.title("기술 통계량 출력")
        descript_menu.geometry("500x250")
        
        var_list = Listbox(descript_menu, selectmode = "multiple")
        
        
        for i in variables:
            var_list.insert(END, i)
        
        print_bt = Button(descript_menu, text = "확인", command = descript_ok)
        
        
        print_bt.pack(side = BOTTOM)
        var_list.pack()
    except NameError:
        report("csv 파일을 아직 열지 않았습니다.")
def ttest():
    try:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                report(df.describe())
        report(df.describe())
    except NameError:
        report("csv 파일을 아직 열지 않았습니다.")
def lr():
    try:
        report(df.describe())
    except NameError:
        report("csv 파일을 아직 열지 않았습니다.")
def pca():
    try:
        report(df.describe())
    except NameError:
        report("csv 파일을 아직 열지 않았습니다.")
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
    t1.insert(END, s)
    t1.insert(END, "\n")    
 
report("메뉴에서 통계 분석을 실시해주세요.")

mainloop()