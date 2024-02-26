import tkinter as tk

window = tk.Tk()
window.title("Hello World")

label = tk.Label(window, text="Hello World")
label.pack()

button = tk.Button(window, text="Click me!", command=window.destroy)
button.pack()

window.mainloop()