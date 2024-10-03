import streamlit as st
from model import QuestionManager

# Initialize the question manager
question_manager = QuestionManager()

# Streamlit app setup
st.title("Question Submission App")

# Text area for multiple questions input
new_questions = st.text_area("Enter your questions (one per line)", height=150)

# Submit button
if st.button("Submit"):
    if new_questions.strip():
        questions_list = new_questions.splitlines()  # Split input into separate lines
        results = []  # List to hold result messages
        for question in questions_list:
            question = question.strip()
            if question:  # Check if the question is not empty
                message, compared_question = question_manager.add_question(question)
                if compared_question:
                    # If the question was found to be redundant
                    results.append(f"Redundant: {message} (compared to: '{compared_question}')")
                else:
                    # If the question was successfully added
                    results.append(message)
        # Display results
        for result in results:
            st.write(result)
    else:
        st.warning("Please enter at least one question.")
