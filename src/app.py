import tkinter as tk
from datetime import datetime


def on_button_click():
    print("Button clicked!")
    console.insert(0.0, str(datetime.now()) + " Button clicked!\n")


class Console(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


root = tk.Tk()  # Обявление приложения
root.geometry("400x300")  # Размер окна
button = tk.Button(root, text="Добавить новую причину простоя!", command=on_button_click)
button2 = tk.Button(root, text="Добавить новую причину простоя!", command=on_button_click)


button.pack(row=0, column=0, padx=10, pady=10)
button2.pack(row=0, column=1, padx=10, pady=10)

console = Console(root)
console.pack(row=1, column=0, columnspan=2)

if __name__ == "__main__":
    root.mainloop()
