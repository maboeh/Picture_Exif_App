from gui import Gui
from applicationLogic import ApplicationLogic
import ttkbootstrap as ttk

#!!

def main():
    root = ttk.Window(title="Bilder - EXIF - App", themename="lumen")
    logic = ApplicationLogic()
    gui = Gui(root, logic)
    root.mainloop()
if __name__ == "__main__":
    main()