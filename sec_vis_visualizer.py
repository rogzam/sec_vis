from tkinter import *

sec_vis = Tk()

sec_vis.geometry('450x450+500+300')
sec_vis.title('Section visualizer')

mlabel = Label(text='Label 1',fg='red')
mlabel.grid(row=0,column=2)

sec_vis.mainloop()
