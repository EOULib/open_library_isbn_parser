import tkinter as tk

class Clipboard:

	def copy(self, win, entry_object, object_value):
		win.clipboard_clear()
		win.clipboard_append('')
		entry_object_value = entry_object.get()
		win.clipboard_append(entry_object_value)

	def cut(self, win, entry_object, object_value):
		win.clipboard_clear()
		win.clipboard_append('')
		entry_object_value = entry_object.get()
		win.clipboard_append(entry_object_value)
		object_value.set("")

	def paste(self, win, entry_object, object_value):
		current_clipboard = win.clipboard_get()
		object_value.set("")
		entry_object.insert('end', current_clipboard)

	def menu_display(self, event):
		self.clipboard_menu.tk_popup(event.x_root, event.y_root)

	def add_menu(self, win, entry_object, object_value):
		self.clipboard_menu = tk.Menu(entry_object, tearoff=0)
		self.clipboard_menu.add_command(label="Copy", command=lambda: self.copy(win, entry_object, object_value))
		self.clipboard_menu.add_separator()
		self.clipboard_menu.add_command(label="Cut", command=lambda: self.cut(win, entry_object, object_value))
		self.clipboard_menu.add_separator()
		self.clipboard_menu.add_command(label="Paste", command=lambda: self.paste(win, entry_object, object_value))
		entry_object.bind("<Button - 3>", self.menu_display)