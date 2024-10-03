import streamlit as st
import pandas as pd
from io import BytesIO
import os
from model import QuestionManager

# Initialize the question manager
question_manager = QuestionManager()

# Dictionary to store game types and their corresponding labels
game_types = {
    "Never Have I Ever": "Submit 'Never Have I Ever' Questions",
    "Truth and Dare": "Submit 'Truth and Dare' Questions",
    "Other": "Submit 'Other' Game Questions"
    # Add more games here in the future
}

# Streamlit app setup
st.title("Game Question Submission App")

# Dropdown for selecting the game type
game_type = st.selectbox("Select a game", ["Choose a game"] + list(game_types.keys()))

# Function to handle question submission and return non-redundant results
def handle_question_submission():
    if new_questions.strip():
        questions_list = new_questions.splitlines()  # Split input into separate lines
        results = []  # List to hold result messages
        non_redundant_data = []  # Data for saving only non-redundant questions to Excel
        try:
            for question in questions_list:
                question = question.strip()
                if question:  # Check if the question is not empty
                    message, compared_question = question_manager.add_question(question)
                    if compared_question:
                        result = f"Redundant: {message} (compared to: '{compared_question}')"
                    else:
                        result = message
                        # Append non-redundant questions to the list for Excel
                        non_redundant_data.append({"Question": question, "Result": result})
                    results.append(result)
            # Display results
            for result in results:
                if "Redundant" in result:
                    st.error(result)  # Display redundancy messages as errors
                else:
                    st.success(result)  # Display success messages

            return non_redundant_data  # Return non-redundant data for Excel file
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter at least one question.")
        return None

# Function to generate the Excel file for download
def generate_excel(data, game_type):
    df = pd.DataFrame(data)  # Convert the data to a DataFrame
    output = BytesIO()  # In-memory bytes buffer
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Non-Redundant Questions")
    output.seek(0)  # Go to the start of the stream
    return output

# Function to save non-redundant questions to the game-specific Excel file and the master file
def save_to_excel(data, game_type):
    df = pd.DataFrame(data)  # Convert the data to a DataFrame
    game_file = f"{game_type}_questions.xlsx"  # File for specific game type
    master_file = "all_non_redundant_questions.xlsx"  # Master file for all non-redundant questions

    # Save or overwrite the game-specific file
    df.to_excel(game_file, index=False, sheet_name="Non-Redundant Questions")
    st.success(f"Non-redundant questions saved to {game_file}")

    # Append to the master file or create a new one
    if os.path.exists(master_file):
        # If the master file exists, append new non-redundant questions
        existing_df = pd.read_excel(master_file)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        # If the master file does not exist, create it
        combined_df = df
    
    combined_df.to_excel(master_file, index=False, sheet_name="All Non-Redundant Questions")
    st.success(f"All non-redundant questions have been saved to {master_file}")

# Conditional display based on the selected game type
if game_type != "Choose a game":
    st.subheader(game_types[game_type])
    new_questions = st.text_area(f"Enter your {game_type} questions (one per line)", height=150)

    # Submit button
    if st.button("Submit"):
        non_redundant_data = handle_question_submission()
        if non_redundant_data:
            # Generate the Excel data for download
            excel_data = generate_excel(non_redundant_data, game_type)
            st.download_button(
                label="Download Non-Redundant Questions as Excel",
                data=excel_data,
                file_name=f"{game_type}_questions.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Save to both game-specific and master files
            save_to_excel(non_redundant_data, game_type)
