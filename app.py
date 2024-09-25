import customtkinter
from model import QuestionManager  

app = customtkinter.CTk()
app.geometry("400x300")
question_manager = QuestionManager()

def button_function():
    """
    Called when the user clicks the "Submit" button. Retrieves the text from the
    text area, adds it to the question manager, and updates the result label
    to show each question added one after the other.
    """
    new_questions = text_area.get("1.0", "end-1c").strip()  # Get all text from the text area
    if new_questions:
        questions_list = new_questions.splitlines()  # Split input into separate lines
        results = []  # List to hold result messages
        for question in questions_list:
            question = question.strip()
            if question:  # Check if the question is not empty
                try:
                    question_manager.add_question(question)  # Add the question
                    results.append(f"Added: {question}")
                except Exception as e:
                    results.append(f"Error adding '{question}': {e}")
        # Display results one after the other
        result_label.configure(text="\n".join(results))
        text_area.delete("1.0", "end")  # Clear the text area
    else:
        result_label.configure(text="Please enter at least one question.")

text_area = customtkinter.CTkTextbox(master=app, width=300, height=150)
text_area.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Submit", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

result_label = customtkinter.CTkLabel(master=app, text="Result will appear here")
result_label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

app.mainloop()
