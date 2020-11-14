import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tkinter import * 
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
        variables = self.df.columns
        one_ttest_menu = Toblevel()
        one_ttest_menu.title("단일표본 t검정")
        one_ttest_menu.geometry("500x250")
        
        var_list = Listbox(one_ttest_menu, selectmode = "single")
        
        for i in variables:
            var_list.insert(END, i)
            
        mu = Entry(one_ttest_menu)
        
        pass
    def pair_ttest(self):
        pass
    def in_ttest(self):
        pass
    def lr(self):
        pass
    def pca(self):
        pass
