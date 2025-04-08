import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time
import sys

# Load environment variables
load_dotenv()

# Configure the Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: Missing Gemini API key. Please set GEMINI_API_KEY in your .env file.")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# Select the model
model = genai.GenerativeModel('gemini-2.0-flash')

# Animal information cache to reduce API calls
animal_cache = {}

class PetAdoptionAssistant:
    def __init__(self):
        self.chat = None
        
    def initialize_conversation(self):
        """Initialize the chatbot with a system prompt."""
        system_prompt = """
        You are a helpful pet adoption assistant with expertise in all types of animals.
        When users ask about an animal, provide its common species/breeds.
        When users ask about a specific species/breed, provide detailed information including:
        - History and origin
        - Common health concerns/diseases
        - Temperament and behavior traits
        - Care requirements (feeding, exercise, grooming, space)
        - Pros and cons of ownership
        - Special considerations for adoption
        - Approximate lifespan
        - Cost considerations

        Always be informative, friendly, and supportive of ethical pet adoption practices.
        """
        # Start a new chat session with the system prompt
        self.chat = model.start_chat()
        # Send the system prompt as the first message
        self.chat.send_message(system_prompt)
    
    def generate_response(self, user_input):
        """Generate a response using the Gemini API."""
        # Check if request is for animal species list
        if "species" in user_input.lower() or "breeds" in user_input.lower() or "types" in user_input.lower():
            # Check cache first
            animal_type = self.extract_animal_type(user_input)
            if animal_type and animal_type in animal_cache:
                return animal_cache[animal_type]
        
        try:
            # Make sure chat is initialized
            if self.chat is None:
                self.initialize_conversation()
                
            # Send the user message and get the response
            response = self.chat.send_message(user_input)
            response_text = response.text
            
            # Cache animal species information if relevant
            if "species" in user_input.lower() or "breeds" in user_input.lower() or "types" in user_input.lower():
                animal_type = self.extract_animal_type(user_input)
                if animal_type:
                    animal_cache[animal_type] = response_text
            
            return response_text
        
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            return error_message
    
    def extract_animal_type(self, input_text):
        """Extract the animal type from user input."""
        # List of common animal types to check against
        common_animals = ["dog", "cat", "bird", "fish", "rabbit", "hamster", "guinea pig", 
                         "reptile", "snake", "lizard", "turtle", "ferret", "mouse", "rat"]
        
        words = input_text.lower().split()
        for animal in common_animals:
            if animal in words:
                return animal
        
        # For more complex extraction, we could use the Gemini API itself
        # But this simple approach handles most cases
        return None


def display_welcome():
    """Display welcome message and instructions."""
    print("\n" + "="*60)
    print("🐾 Welcome to the Pet Adoption Assistant! 🐾".center(60))
    print("="*60)
    print("\nI can help you learn about different animals and their species.")
    print("You can ask questions like:")
    print("  - What dog breeds are good for families?")
    print("  - Tell me about Bengal cats")
    print("  - What are the pros and cons of adopting a bearded dragon?")
    print("  - What species of rabbits are there?")
    print("\nType 'exit' to quit the program.\n")
    print("-"*60)

def main():
    # Create the assistant
    assistant = PetAdoptionAssistant()
    assistant.initialize_conversation()
    
    display_welcome()
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nThank you for using the Pet Adoption Assistant! Good luck with your pet adoption journey! 🐾")
            break
        
        print("\nThinking...")
        start_time = time.time()
        
        response = assistant.generate_response(user_input)
        
        # Calculate response time
        elapsed_time = time.time() - start_time
        
        print(f"\nAssistant ({elapsed_time:.2f}s):\n{response}")
        print("\n" + "-"*60)

if __name__ == "__main__":
    main()