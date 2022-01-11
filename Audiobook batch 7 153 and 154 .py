import curses
from re import T
import speech_recognition as sr
from gtts import gTTS
import os
import pdfplumber
from tkinter.filedialog import *
import pyttsx3

menu = ['Speech-To-Text','Text-To-Speech',  'Audio Book', 'Exit']

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
        stdscr.refresh()

def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

def app(stdscr,current_row):
    stdscr.clear()

    if current_row== 0:
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print_center(stdscr,"say something")
            audio=r.listen(source)

        try:
            text=r.recognize_google(audio)
            print_center(stdscr,"you said : {}".format(text))

        except:
            print_center(stdscr,"couldnt recognize")
               

    elif current_row==1:

        u= stdscr.getstr(5,0)
        u=str(u)

        language='en'

        output=gTTS(text=u,lang=language,slow=False)
        output.save("output.mp3")
        print_center(stdscr, "Your text is converted.Do you want to play it.")
        key=stdscr.getch()
        if key==ord('y'):
           os.system("start output.mp3")

    elif current_row==2:
        pdf_path = askopenfilename()

        pdf = pdfplumber.open(pdf_path)
        page = pdf.pages[1]
        text = page.extract_text()
        pdf.close()

        language = 'en'
        gtts_transformer = gTTS(text=text, lang=language)
        gtts_transformer.save("audiobook.mp3")
        print_center(stdscr, "Your audio book is created.Do you want to play it.")
        key=stdscr.getch()
        if key==ord('y'):
            os.system("start audiobook.mp3")
        
    stdscr.refresh()

def main(stdscr):
    # turn off cursor blinking
    curses.curs_set(0)

    # color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # specify the current selected row
    current_row = 0

    # print the menu
    print_menu(stdscr, current_row)

    while 1:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1

        elif key == curses.KEY_ENTER or key in [10, 13]:
            app(stdscr,current_row)
            stdscr.getch()
			# if user selected last row, exit the program
            if current_row == len(menu)-1:
                break

        print_menu(stdscr, current_row)


curses.wrapper(main)


