from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import imageio

#Functions
def pop_qut():
    qut_bol = messagebox.askyesno(title='Quit',message='Are you sure?')
    if qut_bol:
        sec_vis.destroy()
        return
    else:
        pass

def pop_opn():
    opn_adr = filedialog.askdirectory()
    opn_pfx = '/'+opn_adr[-3:]+'_1.png'
    img_act = PhotoImage(file=opn_adr+opn_pfx)
    img_lab = Label(sec_vis,image=img_act)
    return


#Creates the GUI window
sec_vis = Tk()
sec_vis.geometry('1280x400')
sec_vis.title('Section visualizer')

#Variables

#Menu construction
men_bar = Menu(sec_vis)

#File menu
men_fil = Menu(men_bar)
men_fil.add_command(label='Open...', command = pop_opn)
men_fil.add_command(label='Exit',command = pop_qut)

#Export menu
men_exp = Menu(men_bar)
men_exp.add_command(label='Export still image')
men_exp.add_command(label='Export animated gif')

#View menu
men_vie = Menu(men_bar,tearoff = 0)
men_vie.add_checkbutton(label='View axonometry',onvalue=1,offvalue=0)
men_vie.add_checkbutton(label='View section')
men_vie.add_checkbutton(label='View both')

men_bar.add_cascade(label='File', menu=men_fil)
men_bar.add_cascade(label='Export', menu=men_exp)
men_bar.add_cascade(label='View', menu=men_vie)

sec_vis.config(menu=men_bar)

#Slider
men_sli = Scale(sec_vis,orient=HORIZONTAL,length=300, width=10,sliderlength=20,sliderrelief=FLAT,borderwidth=1).pack()

#Images

sec_vis.mainloop()
