import customtkinter
from model import QuestionManager  
app = customtkinter.CTk()
app.geometry("400x240")
question_manager = QuestionManager()
def button_function():
    """
    Called when the user clicks the "Submit" button. Retrieves the text from the
    entry field, adds it to the question manager, and updates the result label
    to show the new question.
    """
    new_question = entry.get()  
    try:
        question_manager.add_question(new_question)  
        result_label.configure(text=f"Question added: {new_question}")  
    except Exception as e:
        result_label.configure(text=f"Error adding question: {e}")

entry = customtkinter.CTkEntry(master=app, width=200)
entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)


button = customtkinter.CTkButton(master=app, text="Submit", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


result_label = customtkinter.CTkLabel(master=app, text="Result will appear here")
result_label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)


app.mainloop()
