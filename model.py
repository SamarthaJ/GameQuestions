import json
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
from nltk.corpus import wordnet as wn 
import nltk 
import os

class QuestionManager:
    """
    Class to manage the questions. It loads them from a file, allows to add new questions and checks for redundancy.
    """
    def __init__(self, json_file='questions.json'):
        self.json_file = json_file
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2') # pre-trained model from Sentence Transformers library
        self.questions_data = self.load_questions()
    
    
    def load_questions(self):
        """
        Load questions from the file. If the file does not exist or is empty, return an empty list.
        """
        if not os.path.exists(self.json_file) or os.path.getsize(self.json_file) == 0:
            return {"questions": []}
        with open(self.json_file, 'r') as file:
            return json.load(file)

    
    def save_questions(self):
        """
        Save the questions to the file.
        """
        with open(self.json_file, 'w') as file:
            json.dump(self.questions_data, file, indent=4)

        
    def add_question(self, new_question):
        """
        Add a new question to the list, if it is not redundant.
        """
        try:
            new_embedding = self.model.encode(new_question, convert_to_tensor=True).tolist()
            
            if self.check_redundancy(new_question, new_embedding):
                print("The question is redundant, not adding.")
            else:
                new_entry = {
                    "id": len(self.questions_data["questions"]) + 1,
                    "question_text": new_question,
                    "embedding": new_embedding,
                    "timestamp": datetime.now().isoformat()
                }
                self.questions_data["questions"].append(new_entry)
                self.save_questions()  
                print(f"Added question: '{new_question}'")
        except Exception as e:
            print(f"An error occurred while adding the question: {e}")

    
    def check_redundancy(self, new_question, new_embedding):
        """
        Check if a question is redundant by comparing it with all existing questions.
        """
        # Set a stricter threshold for detecting redundancy in full sentences
        similarity_threshold = 0.85
    
        for question in self.questions_data["questions"]:
            stored_embedding = question["embedding"]
            # Calculate cosine similarity between the embeddings
            similarity = util.pytorch_cos_sim(new_embedding, stored_embedding).item()

            if similarity > similarity_threshold:
                print(f"Question '{new_question}' is semantically similar to '{question['question_text']}' with similarity {similarity}")
                return True

            # Optionally, check word-level similarity (as it exists in the original code)
            if self.check_word_level_similarity(new_question, question["question_text"]):
                print(f"Question '{new_question}' is similar at word level to '{question['question_text']}'")
                return True

        return False

    
    def check_word_level_similarity(self, new_question, stored_question):
        """
        Check if two questions are similar at word level.
        """
        new_words = new_question.split()
        stored_words = stored_question.split()
        
        
        if len(new_words) != len(stored_words):
            return False
        
        
        for new_word, stored_word in zip(new_words, stored_words):
            if not self.are_words_similar(new_word, stored_word):
                return False
        return True
    
    nltk.download('averaged_perceptron_tagger')

    def are_words_similar(self, word1, word2):
        """
        Check if two words are similar based on direct match, synonym matching, and POS tagging.
        """
        # Perform POS tagging
        pos1 = nltk.pos_tag([word1])[0][1]
        pos2 = nltk.pos_tag([word2])[0][1]

        # Only proceed if words have the same part of speech (POS)
        if pos1 != pos2:
            return False

        # Check if the words are identical
        if word1.lower() == word2.lower():
            return True

        # Use WordNet synonyms to check word similarity
        synsets1 = wn.synsets(word1.lower())
        synsets2 = wn.synsets(word2.lower())

        if synsets1 and synsets2:
            # Compare words based on WordNet's Wu-Palmer similarity
            for synset1 in synsets1:
                for synset2 in synsets2:
                    if synset1.wup_similarity(synset2) and synset1.wup_similarity(synset2) > 0.8:
                        return True

        return False

if __name__ == "__main__":
    manager = QuestionManager()