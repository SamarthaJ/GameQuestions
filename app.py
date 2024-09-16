import customtkinter

# Initialize the app
app = customtkinter.CTk()
app.geometry("400x240")

# Function to handle button press and display result
def button_function():
    result_text = entry.get()  # Get text from entry
    result_label.configure(text=f"Result: {result_text}")  # Update the label to show the result

# Create a single-line text entry field
entry = customtkinter.CTkEntry(master=app, width=200)
entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

# Create a button to submit and show the result
button = customtkinter.CTkButton(master=app, text="Submit", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

# Create a label to display the result (this is your div-like area)
result_label = customtkinter.CTkLabel(master=app, text="Result will appear here")
result_label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

# Run the application
app.mainloop()
