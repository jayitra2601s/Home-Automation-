import os
import dotenv

# Load environment variables from the .env file
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# Access the MASTER variable
gender = os.getenv('MASTER')


# Example opening text
opening_text = [
    f"Cool, I'm on it {gender}.",
    f"Okay {gender}, I'm working on it.",
    f"Just a second {gender}.",
    "Please hold on...",
]
