import tkinter as tk
from tkinter import Menu



class ResizableWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Redact")

        self.configure(bg='black')    # Set the background color
        
        ## default size
        self.geometry('400x400')

        self.grip_size = 10  # Size of the resize grip area

        # Initialize variables for dragging
        self.dragging = False
        self.startX = None
        self.startY = None

        # Invisible frame for resizing from the right (horizontal resize)
        self.grip_e = tk.Frame(self, cursor='right_side', bg='black')
        self.grip_e.bind("<ButtonPress-1>", lambda e: self.start_resize(e, 'e'))
        self.grip_e.bind("<B1-Motion>", self.on_horizontal_resize)

        self.grip_e.pack(side='right', fill='y', ipadx=self.grip_size)

        # Invisible frame for resizing from the bottom (vertical resize)
        self.grip_s = tk.Frame(self, cursor='bottom_side', bg='black')
        self.grip_s.bind("<ButtonPress-1>", lambda e: self.start_resize(e, 's'))
        self.grip_s.bind("<B1-Motion>", self.on_vertical_resize)
        self.grip_s.pack(side='bottom', fill='x', ipady=self.grip_size)

        # Make the window draggable
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_move)

        # make a right click on the window close it
        self.bind("<Button-2>", lambda e: self.destroy())

        self.attributes('-topmost', True)

        menubar = Menu(self)
        self.config(menu=menubar)

        window_menu = Menu(menubar)

        window_menu.add_command(
            label='New',
            command=self.new,
            accelerator='Cmd+N'
            )

        # add the File menu to the menubar
        menubar.add_cascade(
            label="Window",
            menu=window_menu 
            )
        self.bind('<Command-n>', lambda e: self.new())




    def new(self):
        window = ResizableWindow()

        

    def is_within_grips(self, event):
        # Check if the event is within the bounds of the resize grips
        if event.widget == self.grip_e or event.widget == self.grip_s:
            return True
        return False

    def start_move(self, event):
        if not self.is_within_grips(event):
            self.dragging = True
            self.startX = event.x
            self.startY = event.y

    def stop_move(self, event):
        self.dragging = False
        self.startX = None
        self.startY = None

    def on_move(self, event):
        if self.dragging:
            x = self.winfo_x() - self.startX + event.x
            y = self.winfo_y() - self.startY + event.y
            self.geometry(f"+{x}+{y}")

    def start_resize(self, event, direction):
        self.startX = event.x
        self.startY = event.y

    def on_horizontal_resize(self, event):
        new_width = max(self.winfo_width() - self.startX + event.x, self.grip_size * 2)
        self.geometry(f"{new_width}x{self.winfo_height()}")

    def on_vertical_resize(self, event):
        new_height = max(self.winfo_height() - self.startY + event.y, self.grip_size * 2)
        self.geometry(f"{self.winfo_width()}x{new_height}")

    

def main():

    root = ResizableWindow()
    root.mainloop()

if __name__ == "__main__":
    main()
