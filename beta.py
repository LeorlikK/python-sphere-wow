from pyautogui import moveTo, click, position
from mss import mss
import numpy as np
from keyboard import send, read_key
import tkinter as tk
from tkinter import StringVar
from threading import Thread


class SearchSphere:

    def __init__(self):
        self.resolution_width = win.winfo_screenwidth()
        self.resolution_height = win.winfo_screenheight()
        self.messageX = StringVar()
        self.messageX.set(self.resolution_width)
        self.messageY = StringVar()
        self.messageY.set(self.resolution_height)
        self.messageR = StringVar()
        self.messageG = StringVar()
        self.messageB = StringVar()
        self.messageR.set("0")
        self.messageG.set("0")
        self.messageB.set("0")

    @staticmethod
    def search(monitor, color):
        """Нахожддение положения всех пикселей заданного цвета"""
        m = mss()
        crop_img1 = m.grab(monitor)
        img_arr = np.array(crop_img1)
        our_map = (color[2], color[1], color[0], 255)
        index = np.where(np.all(img_arr == our_map, axis=-1))
        our_crd = np.transpose(index)
        return our_crd

    @staticmethod
    def flow():
        t1 = Thread(target=pix.grab_pix())
        t1.start()

    def grab_pix(self):
        input_key_color = read_key()
        input_key_color = input_key_color.lower()
        if input_key_color == 'p':
            x_color, y_color = position()
            monitor_for_grad_color = {
                'left': int(x_color),
                'top': int(y_color),
                'width': 1,
                'height': 1,

            }
            m = mss()
            img = m.grab(monitor_for_grad_color)
            img = np.array(img)
            self.messageR.set(f'{img[0][0][2]}')
            self.messageG.set(f'{img[0][0][1]}')
            self.messageB.set(f'{img[0][0][0]}')
            print(f'Capture R:{img[0][0][2]} G:{img[0][0][1]} B:{img[0][0][0]}')
        else:
            pix.grab_pix()

    def corrector_x_y(self, corrector_x, corrector_y):
        if corrector_x == int(self.resolution_width) // 2:
            pass
        if corrector_x < int(self.resolution_width) // 2:
            corrector_x -= 10
        if corrector_x > int(self.resolution_width) // 2:
            corrector_x += 10
        if corrector_y == int(self.resolution_height) // 2:
            pass
        if corrector_y < int(self.resolution_height) // 2:
            corrector_y -= 10
        if corrector_y > int(self.resolution_height) // 2:
            corrector_y += 10
        return corrector_x, corrector_y

    def get_rgb(self):
        red = btn3.get()
        green = btn5.get()
        blue = btn7.get()
        hotkey = btn9.get()
        hotkey2 = btn16.get()
        monitor_x = btn13.get()
        monitor_y = btn15.get()
        self.resolution_width = int(monitor_x)
        self.resolution_height = int(monitor_y)
        if red and green and blue and hotkey:
            hotkey = hotkey.lower()
            print(f'RED: {red} GREEN: {green} BLUE: {blue} HotKey: {hotkey} HotKeyUse {hotkey2}')
            print(f'Monitor: {self.resolution_width}X{self.resolution_height} ')

            win.destroy()

            pix.sphere_function(r=red, g=green, b=blue, hotkey=hotkey, hotkey2=hotkey2)
        else:
            print('Empty Entry')

    def sphere_function(self, r, g, b, hotkey, hotkey2=None):
        """Основной блок"""
        our_color_burgundy = [int(r), int(g), int(b)]
        monitor1 = {
            'left': 0,
            'top': 0,
            'width': int(self.resolution_width),
            'height': int(self.resolution_height),
        }
        while True:
            """Главный цикл"""
            input_key = read_key()
            input_key = input_key.lower()
            if input_key == hotkey:
                result_sphere = SearchSphere.search(monitor1, our_color_burgundy)
                if result_sphere.__len__():
                    index_y = 0
                    number_list_y = []
                    for value in result_sphere:
                        number_y = np.abs(result_sphere[index_y][0] - int(self.resolution_height) // 2) + (
                            np.abs(result_sphere[index_y][1] - int(self.resolution_width) // 2))
                        number_list_y.append(number_y)
                        index_y += 1
                    nearest_y = np.min(number_list_y)
                    index_number_list_y = number_list_y.index(nearest_y)
                    nearest_result_sphere_y = result_sphere[index_number_list_y][0]
                    nearest_result_sphere_x = result_sphere[index_number_list_y][1]
                    nearest_result_sphere_x, nearest_result_sphere_y = pix.corrector_x_y(nearest_result_sphere_x,
                                                                                         nearest_result_sphere_y)
                    moveTo(nearest_result_sphere_x, nearest_result_sphere_y)
                    click()
                    if hotkey2 == '':
                        pass
                    else:
                        send(str(hotkey2))
                    print('Found:  X = ' + str(nearest_result_sphere_x) + '  Y = ' + str(nearest_result_sphere_y))
                else:
                    print('No results: ')


win = tk.Tk()
win.title('WOW Sphere')
win.config(bg='#2c363f')
win.geometry('600x400+660+340')
win.resizable(False, False)


pix = SearchSphere()

btn1 = tk.Label(win, text='Color:Converter', bg='#2c363f', fg='black', font=('Arial', 30,), anchor='se')

btn2 = tk.Label(win, text='R', bg='#2c363f', fg='red', font=('Arial', 15,), anchor='s')
btn3 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5, textvariable=pix.messageR)

btn4 = tk.Label(win, text='G', bg='#2c363f', fg='green', font=('Arial', 15,), anchor='s')
btn5 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5, textvariable=pix.messageG)

btn6 = tk.Label(win, text='B', bg='#2c363f', fg='blue', font=('Arial', 15,), anchor='s')
btn7 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5, textvariable=pix.messageB)

btn8 = tk.Label(win, text='HotKey', bg='#2c363f', fg='black', font=('Arial', 30,), anchor='e')
btn9 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)

btn10 = tk.Button(win, text='Start', bg='#2c363f', fg='white', width=20, command=pix.get_rgb)

btn11 = tk.Label(win, text='Monitor Resolution ', bg='#2c363f', fg='black', font=('Arial', 30,),
                 anchor='se')  # Monitor

btn12 = tk.Label(win, text='X', bg='#2c363f', fg='black', font=('Arial', 15,), anchor='s')
btn13 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5, textvariable=pix.messageX)
btn14 = tk.Label(win, text='Y', bg='#2c363f', fg='black', font=('Arial', 15,), anchor='s')
btn15 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5, textvariable=pix.messageY)
btn16 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)

btn17 = tk.Button(win, text='Сapture(p) ', bg='#2c363f', fg='white', width=10, command=SearchSphere.flow)

btn1.grid(row=2, column=1, stick='sw', padx=5, columnspan=6)  # Color

btn2.grid(row=3, column=1, stick='ne', padx=1)  # R
btn3.grid(row=3, column=2, stick='nw', padx=1)  # R value

btn4.grid(row=3, column=3, stick='ne', padx=1)  # G
btn5.grid(row=3, column=4, stick='nw', padx=1)  # G value

btn6.grid(row=3, column=5, stick='ne', padx=1)  # B
btn7.grid(row=3, column=6, stick='nw', padx=1)  # B value

btn8.grid(row=4, column=1, stick='nw', padx=5, columnspan=6)  # HotKey
btn9.grid(row=4, column=4, stick='ne', padx=1, pady=10)  # HotKey value

btn10.grid(row=5, column=1, stick='s', padx=1, columnspan=6)

btn11.grid(row=0, column=1, stick='se', padx=5, columnspan=6)  # Monitor
btn12.grid(row=1, column=1, stick='ne', padx=1)
btn13.grid(row=1, column=2, stick='nw', padx=1)
btn14.grid(row=1, column=3, stick='ne', padx=1)
btn15.grid(row=1, column=4, stick='nw', padx=1)

btn16.grid(row=4, column=5, stick='ne', padx=1, pady=10)  # HotKey2 value

btn17.grid(row=5, column=0, stick='s', padx=1)

win.grid_rowconfigure(0, minsize=60)
win.grid_columnconfigure(0, minsize=130)

win.grid_rowconfigure(1, minsize=60)

win.grid_rowconfigure(2, minsize=60)

win.grid_rowconfigure(3, minsize=60)

win.grid_rowconfigure(4, minsize=60)

win.grid_rowconfigure(5, minsize=60)

win.mainloop()