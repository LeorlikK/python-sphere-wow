import pyautogui
from mss import mss
import numpy as np
from threading import Thread
import keyboard
import tkinter as tk
import time

monitor_x = 0
monitor_y = 0


def corrector_x_y(corrector_x, corrector_y):
    if corrector_x == int(monitor_x)//2:
        pass
    if corrector_x < int(monitor_x)//2:
        corrector_x -= 10
        print('x - 10')
    if corrector_x > int(monitor_x)//2:
        corrector_x += 10
        print('x + 10')
    if corrector_y == int(monitor_y)//2:
        pass
    if corrector_y < int(monitor_y)//2:
        corrector_y -= 10
        print('y - 10')
    if corrector_y > int(monitor_y)//2:
        corrector_y += 10
        print('y + 10')
    return corrector_x, corrector_y


def get_rgb():
    global monitor_x, monitor_y
    red = btn3.get()
    green = btn5.get()
    blue = btn7.get()
    hotkey = btn9.get()
    hotkey2 = btn16.get()
    print(hotkey2)
    print('ETO HOT')
    monitor_x = btn13.get()
    monitor_y = btn15.get()
    if red and green and blue and hotkey:
        hotkey = hotkey.lower()
        print(str('RED: ') + red, str(' GREEN: ') + green, str(' BLUE: ') + blue, str(' HotKey: ') + hotkey)
        print(str('Monitor: ') + monitor_x + str('X') + monitor_y)

        win.destroy()

        sphere_function(r=red, g=green, b=blue, hotkey=hotkey, hotkey2=hotkey2)
        #t1 = Thread(target=sphere_function(red, green, blue, hotkey, hotkey2))
        #t2 = Thread(target=output_exit)

        #t1.start()
        #t2.start()

        #t1.join()
        #t2.join()
    else:
        print('Empty Entry')


def search(monitor, color):
    '''Нахожддение положения всех пикселей заданного цвета'''
    m = mss()
    crop_img1 = m.grab(monitor)
    img_arr = np.array(crop_img1)
    our_map = (color[2], color[1], color[0], 255)
    index = np.where(np.all(img_arr == our_map, axis=-1))
    our_crd = np.transpose(index)
    return our_crd


# def output_exit():
#     while True:
#         v = keyboard.read_hotkey()
#         if v == 'ctrl+f8':
#             print('CHETO TAM')


def sphere_function(r, g, b, hotkey, hotkey2=None):
    our_color_burgundy = [int(r), int(g), int(b)]
    monitor1 = {
        'left': 0,
        'top': 0,
        'width': int(monitor_x),
        'height': int(monitor_y),
    }
    while True:
        a = keyboard.read_key()
        a = a.lower()
        if a == hotkey:
            time1 = time.time()
            result_sphere = search(monitor1, our_color_burgundy)
            if result_sphere.__len__():
                index_y = 0
                number_list_y = []
                for value in result_sphere:
                    number_y = np.abs(result_sphere[index_y][0] - int(monitor_y)//2) + (np.abs(result_sphere[index_y][1] - int(monitor_x)//2))
                    number_list_y.append(number_y)
                    index_y += 1
                nearest_y = np.min(number_list_y)
                index_number_list_y = number_list_y.index(nearest_y)
                nearest_result_sphere_y = result_sphere[index_number_list_y][0]
                nearest_result_sphere_x = result_sphere[index_number_list_y][1]
                nearest_result_sphere_x, nearest_result_sphere_y = corrector_x_y(nearest_result_sphere_x, nearest_result_sphere_y)
                pyautogui.moveTo(nearest_result_sphere_x, nearest_result_sphere_y)
                pyautogui.click()
                if hotkey2 == '':
                    pass
                    print('Propyskay')
                else:
                    keyboard.send(str(hotkey2))
                time2 = time.time()
                time3 = time2 - time1
                print(time3)
                time.sleep(0.1)
                print('Found:  X = ' + str(nearest_result_sphere_x) + '  Y = ' + str(nearest_result_sphere_y))
            else:
                print('No results: ')


win = tk.Tk()
win.title('WOW Sphere')
win.config(bg='#2c363f')
win.geometry('600x400+660+340')
win.resizable(False, False)

btn1 = tk.Label(win, text='Color:Converter', bg='#2c363f', fg='black', font=('Arial', 30,), anchor='se')

btn2 = tk.Label(win, text='R', bg='#2c363f', fg='red', font=('Arial', 15,), anchor='s')
btn3 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)

btn4 = tk.Label(win, text='G', bg='#2c363f', fg='green', font=('Arial', 15,), anchor='s')
btn5 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)

btn6 = tk.Label(win, text='B', bg='#2c363f', fg='blue', font=('Arial', 15,), anchor='s')
btn7 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)

btn8 = tk.Label(win, text='HotKey', bg='#2c363f', fg='black', font=('Arial', 30,), anchor='e')
btn9 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)

btn10 = tk.Button(win, text='Start', bg='#2c363f', fg='white', width=20, command=get_rgb)

btn11 = tk.Label(win, text='Monitor Resolution ', bg='#2c363f', fg='black', font=('Arial', 30,), anchor='se') # Monitor

btn12 = tk.Label(win, text='X', bg='#2c363f', fg='black', font=('Arial', 15,), anchor='s')
btn13 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)
btn14 = tk.Label(win, text='Y', bg='#2c363f', fg='black', font=('Arial', 15,), anchor='s')
btn15 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)
btn16 = tk.Entry(win, bg='white', relief=tk.RAISED, bd=5, width=5)

btn1.grid(row=2, column=1, stick='sw', padx=5, columnspan=6) # Color

btn2.grid(row=3, column=1, stick='ne', padx=1) # R
btn3.grid(row=3, column=2, stick='nw', padx=1) # R value

btn4.grid(row=3, column=3, stick='ne', padx=1) # G
btn5.grid(row=3, column=4, stick='nw', padx=1) # G value

btn6.grid(row=3, column=5, stick='ne', padx=1) # B
btn7.grid(row=3, column=6, stick='nw', padx=1) # B value

btn8.grid(row=4, column=1, stick='nw', padx=5, columnspan=6) # HotKey
btn9.grid(row=4, column=4, stick='ne', padx=1, pady=10) # HotKey value

btn10.grid(row=5, column=1, stick='s', padx=1, columnspan=6)

btn11.grid(row=0, column=1, stick='se', padx=5, columnspan=6) # Monitor
btn12.grid(row=1, column=1, stick='ne', padx=1)
btn13.grid(row=1, column=2, stick='nw', padx=1)
btn14.grid(row=1, column=3, stick='ne', padx=1)
btn15.grid(row=1, column=4, stick='nw', padx=1)

btn16.grid(row=4, column=5, stick='ne', padx=1, pady=10) # HotKey2 value


win.grid_rowconfigure(0, minsize=60)
win.grid_columnconfigure(0, minsize=130)

win.grid_rowconfigure(1, minsize=60)

win.grid_rowconfigure(2, minsize=60)

win.grid_rowconfigure(3, minsize=60)

win.grid_rowconfigure(4, minsize=60)

win.grid_rowconfigure(5, minsize=60)

win.mainloop() # Цикл














