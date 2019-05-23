from tkinter import *
from tkinter import messagebox

from pynput.keyboard import Controller

from Backend import *
from Exceptions import *


class Interface:
    def __init__(self):
        self._root = Tk()
        self._root.title("Minesweeper")
        Grid.rowconfigure(self._root, 0, weight=1)
        Grid.columnconfigure(self._root, 0, weight=1)
        self._root.minsize(width=440, height=200)
        self._root.resizable(False, False)
        self._root.bind("<KeyPress-x><KeyPress-y><KeyPress-z><KeyPress-z><KeyPress-y>", self.cheat)

        self._frameBoard = Frame(self._root, width=440, height=50)
        self._frameBoard.pack(side=BOTTOM)

        self._frame_settings = Frame(self._root, width=200, height=150)
        self._frame_settings.pack(side=LEFT)

        self._labelBoardSize = Label(self._frame_settings, text="Rozmiar planszy")
        self._labelMines = Label(self._frame_settings, text="Miny")
        self._labelMinesAmount = Label(self._frame_settings, text="Liczba Min")
        self._labelColumn = Label(self._frame_settings, text="Podaj column:")
        self._labelRow = Label(self._frame_settings, text="Podaj row:")
        self._entryColumn = Entry(self._frame_settings, width=4)
        self._entryRow = Entry(self._frame_settings, width=4)
        self._entryMinesAmount = Entry(self._frame_settings, width=4)
        self._buttonNewGame = Button(self._frame_settings, text="Nowa Gra", command=lambda: self.set_new_game_labels())
        self._labelBoardSize.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self._labelMines.grid(row=0, column=5, columnspan=3, padx=5, pady=5)
        self._labelMinesAmount.grid(row=1, column=6, padx=5, pady=5)
        self._labelColumn.grid(row=1, column=0, sticky=E)
        self._labelRow.grid(row=2, column=0, sticky=E)
        self._entryColumn.grid(row=1, column=2, sticky=W)
        self._entryRow.grid(row=2, column=2, sticky=W)
        self._entryMinesAmount.grid(row=1, column=7)
        self._buttonNewGame.grid(row=3, column=6, padx=15, pady=15)

        self._frame_info = Frame(self._root, width=200, height=150)
        self._frame_info.pack(side=RIGHT)
        self._labelGameStatus = Label(self._frame_info, text="Status aktualnej gry")
        self._labelMinesAmountt = Label(self._frame_info, text="Liczba Min:")
        self._labelMarkedFieldAmountt = Label(self._frame_info, text="Liczba oznaczonych pól:")
        self._labelMinesAmount = Label(self._frame_info)
        self._labelMarkedFieldAmount = Label(self._frame_info)
        self._labelGameStatus.place(x=60, y=5)
        self._labelMinesAmountt.place(x=10, y=40)
        self._labelMarkedFieldAmountt.place(x=10, y=70)
        self._labelMinesAmount.place(x=150, y=40)
        self._labelMarkedFieldAmount.place(x=150, y=70)

        # png

        self._buttonQx = PhotoImage(file='icons/questionx.png')
        self._buttonDx = PhotoImage(file='icons/trianglex.png')
        self._button = PhotoImage(file='icons/button.png')
        self._buttonX = PhotoImage(file='icons/buttonx.png')
        self._button0 = PhotoImage(file='icons/zero.png')
        self._button1 = PhotoImage(file='icons/one.png')
        self._button2 = PhotoImage(file='icons/two.png')
        self._button3 = PhotoImage(file='icons/three.png')
        self._button4 = PhotoImage(file='icons/four.png')
        self._button5 = PhotoImage(file='icons/five.png')
        self._button6 = PhotoImage(file='icons/six.png')
        self._button7 = PhotoImage(file='icons/seven.png')
        self._button8 = PhotoImage(file='icons/eight.png')
        self._buttonBomb = PhotoImage(file='icons/bomb.png')
        self._buttonQ = PhotoImage(file='icons/question.png')
        self._buttonD = PhotoImage(file='icons/triangle.png')

        self._buttons = {0: self._button0,
                         1: self._button1,
                         2: self._button2,
                         3: self._button3,
                         4: self._button4,
                         5: self._button5,
                         6: self._button6,
                         7: self._button7,
                         8: self._button8,
                         'bomb': self._buttonBomb,
                         'Q': self._buttonQ,
                         'D': self._buttonD,
                         'button': self._button,
                         'buttonX': self._buttonX,
                         'Qx': self._buttonQx,
                         'Dx': self._buttonDx
                         }

        self._column = None
        self._row = None
        self._boardButton = None
        self._gra = None
        self._shown = False
        self._cheat = False
        self._root.mainloop()

    def show_number(self, _event, r, c):
        if not self._gra.is_end():
            temp = []
            if self._gra.check_neighbours(r, c, temp):
                for r, c in temp:
                    self._boardButton[r][c]['image'] = self._buttons[self._gra.ret_value(r, c)]
                if self._gra.won():
                    messagebox.showinfo("Koniec gry", "Wygrałeś!!! :D")
                    self._shown = True

            else:
                self._boardButton[r][c]['image'] = self._buttons['bomb']
                # self._boardButton[r][c].config(state=DISABLED)
                self.show()
                messagebox.showinfo("Koniec gry", "Przegrana! :(")
                self._shown = True

    def right_button(self, _event, r, c):
        if self._gra.ret_marked(r, c) == 0 and not self._gra.is_end():
            self._gra.add_marked(r, c)
            if self._cheat and self._gra.is_bomb(r, c):
                self._boardButton[r][c]['image'] = self._buttons['Dx']
            else:
                self._boardButton[r][c]['image'] = self._buttons['D']
            self._gra.add_counter()

        elif self._gra.ret_marked(r, c) == 1 and not self._gra.is_end():
            self._gra.add_marked(r, c)
            if self._cheat and self._gra.is_bomb(r, c):
                self._boardButton[r][c]['image'] = self._buttons['Qx']
            else:
                self._boardButton[r][c]['image'] = self._buttons['Q']
            self._gra.sub_counter()

        elif self._gra.ret_marked(r, c) == 2 and not self._gra.is_end():
            self._gra.add_marked(r, c)
            if self._cheat and self._gra.is_bomb(r, c):
                self._boardButton[r][c]['image'] = self._buttons['buttonX']
            else:
                self._boardButton[r][c]['image'] = self._buttons['button']

        self._labelMarkedFieldAmount["text"] = str(self._gra.ret_counter())

        if self._gra.won() and self._gra.is_end() and not self._shown:                       # POWTARZAJĄCY SIĘ KOMUNIKAT PO WYGRANIU PPM!!!
            messagebox.showinfo("Koniec gry", "Wygrałeś!!! :D")
            self._shown = True

    def set_new_game_labels(self):
        keyboard = Controller()
        keyboard.press('\t')
        # keyboard.release('\t')

        try:
            if self._boardButton is not None:
                for col in range(self._column):
                    for r in range(self._row):
                        self._boardButton[r][col].destroy()

            self._column = int(self._entryColumn.get())
            self._row = int(self._entryRow.get())
            if not isinstance(self._column, int) or self._column < 2 or self._column > 15:
                raise IncorrectBoardSizeException(self._column, self._row)

            if not isinstance(self._row, int) or self._row < 2 or self._row > 15:
                raise IncorrectBoardSizeException(self._column, self._row)

            temp = int(self._entryMinesAmount.get())
            if not isinstance(temp, int) or temp < 0 or temp > self._column * self._row:
                raise IncorrectMineAmountException(temp)

            self._gra = Game(self._row, self._column, temp)
            self._gra.print_board()
            self._labelMinesAmount["text"] = temp
            self._labelMarkedFieldAmount["text"] = str(self._gra.ret_counter())

            self._boardButton = [[Button(self._frameBoard, image=self._buttons['button']) for _ in range(self._column)]
                                 for _ in
                                 range(self._row)]

            for i in range(self._row):
                for j in range(self._column):
                    self._boardButton[i][j].bind("<Button-1>",
                                                 lambda e, rx=i, c=j, cc=self._column, rr=self._row: self.show_number(e, rx, c))
                    self._boardButton[i][j]['border'] = '0'
                    self._boardButton[i][j].bind("<Button-3>", lambda e, rx=i, c=j: self.right_button(e, rx, c))
                    self._boardButton[i][j].grid(row=i, column=j, sticky=N + S + E + W, padx=10, pady=10)

            if self._gra.won():
                messagebox.showinfo("Koniec gry", "Wygrałeś!!! :D")

        except IncorrectMineAmountException:
            messagebox.showinfo("ERROR", "Niepoprawna ilość min!\nMinimum 0\nMaksimum wiersze * kolumny")

        except IncorrectBoardSizeException:
            messagebox.showinfo("ERROR", "Niepoprawne wymiary planszy!\nMinumim 2 x 2\nMaksimum 15 x 15")

        except (AnotherDataValidationException, ValueError) as _:
            messagebox.showinfo("ERROR", "Wystąpił problem... Sprawdź jeszcze raz wszytkie wprowadzone dane!")

    def cheat(self, _event):
        temp = self._gra.xyzzy()
        self._cheat = True
        for rr, cc in temp:
            if self._gra.ret_marked(rr, cc) == 0:
                self._boardButton[rr][cc]['image'] = self._buttons['buttonX']
            elif self._gra.ret_marked(rr, cc) == 1:
                self._boardButton[rr][cc]['image'] = self._buttons['Dx']
            elif self._gra.ret_marked(rr, cc) == 2:
                self._boardButton[rr][cc]['image'] = self._buttons['Qx']

    def show(self):
        temp = self._gra.xyzzy()
        for rr, cc in temp:
            self._boardButton[rr][cc]['image'] = self._buttons['bomb']


if __name__ == "__main__":
    play = Interface()
