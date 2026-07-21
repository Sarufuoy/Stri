import tkinter as tk

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="Enter text...", color="grey", **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self.cget("fg")
        self.placeholder_visible = False

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
            self.placeholder_visible = True

    def _clear_placeholder(self, event=None):
        if self.placeholder_visible:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg_color)
            self.placeholder_visible = False

    def get_value(self):
        if self.placeholder_visible:
            print(f"<No Value At {self} - {self.placeholder}>")
            return ""
        return self.get()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Placeholder Entry Test")
    root.geometry("300x150")
    entry = PlaceholderEntry(root, placeholder="Hello World")
    entry.place(x=50, y=50)
    tk.Button(root, text="Print", command=lambda: print(entry.get_value())).pack()
    root.mainloop()
