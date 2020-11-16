import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tkinter import * 
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import p_stats

class readData:
    def __init__(self, Main):      
        self.main = Main
    
        self.filepath = filedialog.askopenfilename(initialdir="./", title="Select file",
                                          filetypes=(("csv files", "*.csv"),
                                          ("all files", "*.*")))
        self.df = pd.read_csv(self.filepath)
        open_csv = Toplevel()
        open_csv.title(self.filepath)
        print_csv = Text(open_csv)
        print_csv.pack()
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print_csv.insert(CURRENT, self.df)        
        
        
        menubar = Menu(open_csv)
        statisticsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Statistics", menu = statisticsmenu)
        statisticsmenu.add_command(label="Descriptive Statistics", command = self.descript)
        statisticsmenu.add_command(label="One Sample T-test", command = self.one_ttest)
        statisticsmenu.add_command(label="Independent T-test", command = self.in_ttest)
        statisticsmenu.add_command(label="Paired T-test", command = self.pair_ttest)
        statisticsmenu.add_command(label="Linear Regression", command = self.lr)
        statisticsmenu.add_command(label="Principal Component Analysis", command = self.pca)
        
        open_csv.config(menu=menubar)
        
    def descript(self):
        def descript_ok():
            vars = list(var_list.curselection()) # curselection은 튜플 반환하므로 리스트로 변경
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                self.main.report(self.df.iloc[:,vars].describe())
            
        variables = self.df.columns
        descript_menu = Toplevel()
        descript_menu.title("기술 통계량 출력")
        descript_menu.geometry("500x250")
        
        var_list = Listbox(descript_menu, selectmode = "multiple")
        
        
        for i in variables:
            var_list.insert(END, i)
        
        print_bt = Button(descript_menu, text = "확인", command = descript_ok)
        
        print_bt.pack(side = BOTTOM)
        var_list.pack()  

    def one_ttest(self):
        def ttest():
            col_index = int(var_list.curselection()[0])
            value = float(value_Entry.get())
            tt = p_stats.One_Ttest(x = self.df.iloc[:, col_index], value = value)
            print(tt.var_x)
            print(tt.t)
            print(tt.p)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                self.main.report(tt.result())
                
        variables = self.df.columns
        one_ttest_menu = Toplevel()
        one_ttest_menu.title("단일표본 t검정")
        one_ttest_menu.geometry("500x250")
        
        var_list = Listbox(one_ttest_menu, selectmode = "single")
        
        for i in variables:
            var_list.insert(END, i)
        
        print_bt = Button(one_ttest_menu, text = "확인", command = ttest)
        
        value_Label = Label(one_ttest_menu, text = "검정값")
        value_Entry = Entry(one_ttest_menu)
        value_Entry.insert(0, "0")
        
        var_list.grid(row = 0, column = 1)
        value_Label.grid(row = 1, column = 0)
        value_Entry.grid(row = 1, column = 1)
        print_bt.grid(row = 2, column = 1)
        
    def pair_ttest(self):
        def ttest():
            col1_index = int(before_LB.curselection()[0])
            col2_index = int(after_LB.curselection()[0])
            if col1_index != col2_index:
                value = float(value_Entry.get())
                tt = p_stats.Paired_Ttest(before = self.df.iloc[:, col1_index], after = self.df.iloc[:, col2_index], value = value)
                print(tt.t)
                print(tt.p)
                with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                    self.main.report(tt.result())
            else:
                self.main.report("같은 변수를 선택하였습니다.")
                
        variables = self.df.columns
        pair_ttest_menu = Toplevel()
        pair_ttest_menu.title("대응표본 t검정")
        pair_ttest_menu.geometry("500x250")
        
        before_Label = Label(pair_ttest_menu, text = "변수 1")
        after_Label = Label(pair_ttest_menu, text = "변수 2")
        before_LB = Listbox(pair_ttest_menu, selectmode = "single", exportselection=0)
        after_LB = Listbox(pair_ttest_menu, selectmode = "single", exportselection=0)
        
        for i in variables:
            before_LB.insert(END, i)
            after_LB.insert(END, i)
        
        print_bt = Button(pair_ttest_menu, text = "확인", command = ttest)
        
        value_Label = Label(pair_ttest_menu, text = "검정값")
        value_Entry = Entry(pair_ttest_menu)
        value_Entry.insert(0, "0")
        
        before_Label.grid(row = 0, column = 0)
        after_Label.grid(row = 0, column = 1)
        before_LB.grid(row = 1, column = 0)
        after_LB.grid(row = 1, column = 1)
        value_Label.grid(row = 2, column = 0)
        value_Entry.grid(row = 2, column = 1)
        print_bt.grid(row = 3, column = 1)
    
    def in_ttest(self):
        def ttest():
            var_index = int(before_LB.curselection()[0])
            group_index = int(after_LB.curselection()[0])
            value = float(value_Entry.get())
            tt = p_stats.Inde_Ttest(x = self.df.iloc[:, var_index], group = self.df.iloc[:, group_index], value = value)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                self.main.report(tt.result())

                
        variables = self.df.columns
        in_ttest_menu = Toplevel()
        in_ttest_menu.title("독립표본 t검정")
        in_ttest_menu.geometry("500x250")
        
        before_Label = Label(in_ttest_menu, text = "변수")
        after_Label = Label(in_ttest_menu, text = "그룹 변수")
        before_LB = Listbox(in_ttest_menu, selectmode = "single", exportselection=0)
        after_LB = Listbox(in_ttest_menu, selectmode = "single", exportselection=0)
        
        for i in variables:
            before_LB.insert(END, i)
            after_LB.insert(END, i)
        
        print_bt = Button(in_ttest_menu, text = "확인", command = ttest)
        
        value_Label = Label(in_ttest_menu, text = "검정값")
        value_Entry = Entry(in_ttest_menu)
        value_Entry.insert(0, "0")
        
        before_Label.grid(row = 0, column = 0)
        after_Label.grid(row = 0, column = 1)
        before_LB.grid(row = 1, column = 0)
        after_LB.grid(row = 1, column = 1)
        value_Label.grid(row = 2, column = 0)
        value_Entry.grid(row = 2, column = 1)
        print_bt.grid(row = 3, column = 1)
        
    def lr(self):
        pass
    def pca(self):
        pass
