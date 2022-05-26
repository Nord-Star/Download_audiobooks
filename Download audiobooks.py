# Downloading audiobooks from https://audiokniga-online.ru/

from tkinter import *
import requests
from bs4 import BeautifulSoup
from playsound import playsound


# Pop-up for the 'paste' / 'copy' menu for input window
def do_popup_in(event):
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()
        menu.entryconfigure('Paste',
                            command=lambda: url_entry.event_generate('<<Paste>>'))


# Downloading audiofile
def dwnld():
    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    url = url_entry.get()  # Web-address of an audiobook page for downloading
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Getting the audiobook's name
    title = soup.title.text
    if ' (аудиокнига онлайн)' in title:
	    title = title.replace(' (аудиокнига онлайн)', '')
    else:
	    title = title.replace(' (Аудиокнига онлайн)', '')

    # Getting the audiobook's address
    link = soup.find_all('script')
    link = str(link[1])
    start = link.find('https')
    if 'mp3' in link:
        end = link.find('mp3')
    elif 'm4a' in link:
	    end = link.find('m4a')
    else:
	    print('Wrong audiofile extension')
    link = link[start:end+3]

    r = requests.get(link)
    with open(str(title)+'.mp3','wb') as mp3:
        mp3.write(r.content)

    playsound('Download Complete.wav')  # 'Download Complete' sound


# ========== INTERFACE ==========
root = Tk()
root.title('Downloading audiobooks from https://audiokniga-online.ru/')
root.resizable(0, 0)

# 'Paste' / 'Copy' menu
menu = Menu(root, tearoff = 0)
menu.add_command(label='Paste')

lbl_frame = LabelFrame(root, text = 'Paste an audiobook\'s page address',
					   height=100, width=400, relief = RIDGE)
lbl_frame.grid(row=0, column=0, padx=5, pady=10)

url_entry = Entry(lbl_frame, width=95)
url_entry.grid(row=0, column=0, padx=5, pady=5)
url_entry.focus_set()
url_entry.bind('<Button-3>', do_popup_in)

dwnld_btn = Button(lbl_frame, text='Download', width=94, command=dwnld)
dwnld_btn.grid(row=1, column=0, padx=5, pady=5)

statusbar = Label(root, text='© Lazy Cat', bd=1, relief=SUNKEN, anchor=E)
statusbar.grid(row=2, column=0, columnspan=3, sticky=W+E)

root.mainloop()
