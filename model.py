import json
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import os

class QuestionManager:
    def __init__(self, json_file='questions.json'):
        self.json_file = json_file
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.questions_data = self.load_questions()
    
    # Load existing questions from JSON file
    def load_questions(self):
        if not os.path.exists(self.json_file) or os.path.getsize(self.json_file) == 0:
            return {"questions": []}
        with open(self.json_file, 'r') as file:
            return json.load(file)

    # Save questions to JSON file
    def save_questions(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.questions_data, file, indent=4)

    # Add a new question to the JSON file
    def add_question(self, new_question):
        # Compute the embedding for the new question
        new_embedding = self.model.encode(new_question, convert_to_tensor=True).tolist()

        # Check if the question is redundant
        if self.check_redundancy(new_question, new_embedding):
            print("The question is redundant, not adding.")
        else:
            # Add the new question to the list
            new_entry = {
                "id": len(self.questions_data["questions"]) + 1,
                "question_text": new_question,
                "embedding": new_embedding,
                "timestamp": datetime.now().isoformat()
            }
            self.questions_data["questions"].append(new_entry)  # Append new entry to the questions list
            self.save_questions()  # Save the updated list back to the JSON file
            print(f"Added question: '{new_question}'")

    # Check if a question is redundant
    def check_redundancy(self, new_question, new_embedding):
        for question in self.questions_data["questions"]:
            stored_embedding = question["embedding"]
            similarity = util.pytorch_cos_sim(new_embedding, stored_embedding).item()
            
            if similarity > 0.8:
                print(f"Question '{new_question}' is similar to '{question['question_text']}' with similarity {similarity}")
                return True
        return False

# Example usage in another app
if __name__ == "__main__":
    manager = QuestionManager()  # Initialize the QuestionManager class
    manager.add_question("Never have I ever broken a leg")  # Pass the new question from another app
