import tkinter as tk
from tkinter import ttk

class Progressbar:
	def __init__(self, frame):
		self.target_frame = frame
		self.progressbar = ttk.Progressbar(self.target_frame, orient="horizontal", value=0, length=200, mode="determinate")
		self.progress_update = tk.StringVar()
		self.progressbar.grid(row=2, column=1, sticky="we")
		self.progressbar_message = ttk.Label(self.target_frame, textvariable=self.progress_update)
		self.progressbar_message.grid(row=3, column=1)

	def start_display(self):
		self.progressbar.start()

	def stop_display(self, number_of_records):
		self.progressbar.stop()
		self.progress_update.set("Done Processing " + str(number_of_records) + " ISBNs")

	def update_display(self, number_of_records, record_number):
		increase_value = record_number/number_of_records
		self.progressbar['value'] = increase_value * 100
		self.progress_update.set(str(record_number) + " of " + str(number_of_records) + " ISBNs processed")