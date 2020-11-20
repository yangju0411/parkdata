from tkinter import * 

import read_data

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('1920x1080')
        self.t1 = Text(self.root, width = 1920, height = 1080)
        self.t1.pack(side = LEFT)
        self.root.title("박데이터")
                
        menubar = Menu(self.root)                                # 윈도우에 메뉴바 추가
        filemenu = Menu(menubar, tearoff=0)                 # 상위 메뉴 탭 항목 추가
        menubar.add_cascade(label="File", menu = filemenu)    # 상위 메뉴 탭 설정  # 항목 추가
        filemenu.add_command(label="Open", command = self.load)
        filemenu.add_separator()                            # 분리선 추가
        filemenu.add_command(label="Exit", command = self.root.destroy)
        
        reportmenu = Menu(menubar, tearoff=0)  
        menubar.add_cascade(label="Report", menu = reportmenu)
        reportmenu.add_command(label="Clear All report", command = self.clear)       

        self.root.config(menu = menubar)
        
        self.report("csv 파일을 열어주세요.")
        
        
        mainloop()

    def load(self):
        self.data = read_data.readData(self)
        self.report(self.data.filepath)
        
    def report(self, s):
        self.t1.insert(END, s)
        self.t1.insert(END, "\n----------------------------------------------------------------------------------\n")
    
    def clear(self):
        self.t1.delete(1.0, END)
 
main = Main()


