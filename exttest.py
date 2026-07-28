import tkinter as tk

def open_custom_messagebox():
    # 1. Create the separate popup window
    popup = tk.Toplevel(root)
    popup.title("Custom Alert")
    popup.geometry("300x150")
    
    # Optional: Prevent resizing to mimic standard messageboxes
    popup.resizable(False, False)
    
    # 2. Make the window modal (blocks interaction with the main window)
    popup.grab_set()
    
    # 3. Add custom widgets (Icon, Message text, Buttons)
    label = tk.Label(popup, text="This is a completely custom messagebox!", wraplength=250, pady=20)
    label.pack()
    
    # 4. Create a close function that releases the grab and destroys the window
    def close_popup():
        popup.grab_release()  # Release control back to main window
        popup.destroy()       # Close the window
        
    close_button = tk.Button(popup, text="OK", width=10, command=close_popup)
    close_button.pack(pady=10)

# Main Application Window
root = tk.Tk()
root.title("Main Application")
root.geometry("400x300")

# Button to trigger the custom messagebox
btn = tk.Button(root, text="Trigger Custom Messagebox", command=open_custom_messagebox)
btn.pack(expand=True)

root.mainloop()