# chatbot.py - Rule-based AI Chatbot for Portfolio
# Works in terminal. Run with:  python3 chatbot.py

import random
import re

# -----------------------------
# PATTERN → RESPONSES / ACTIONS
# -----------------------------

def get_movie_suggestions(genre=None):
    """Return a simple movie suggestion list."""
    movies = {
        "sci-fi": ["Interstellar", "The Matrix", "Inception"],
        "action": ["The Dark Knight", "Mad Max: Fury Road", "John Wick"],
        "drama": ["The Shawshank Redemption", "Forrest Gump", "The Social Network"],
        "anime": ["Your Name", "Spirited Away", "Attack on Titan"],
        "general": ["Interstellar", "The Dark Knight", "Forrest Gump"]
    }
    if genre and genre in movies:
        return f"Here are some {genre} movies: " + ", ".join(movies[genre]) + "."
    return "Here are some good movies to watch: " + ", ".join(movies["general"]) + "."

def calculate_attendance(current_classes, attended_classes, required_percent=75):
    """
    Very simple attendance calculator.
    Returns a message about how many more classes you can miss or must attend.
    """
    if current_classes == 0:
        return "You have 0 classes recorded. Start attending and then ask me again."

    current_percent = (attended_classes / current_classes) * 100

    if current_percent >= required_percent:
        # How many more classes can you skip and still stay >= required_percent?
        # Solve (attended) / (total + x) = required_percent
        # x = (attended * 100 / required_percent) - total
        max_total = (attended_classes * 100 / required_percent)
        can_bunk = int(max_total - current_classes)
        if can_bunk <= 0:
            return f"Your attendance is {current_percent:.1f}%. You are just at or above {required_percent}%. Try not to miss classes."
        return f"Your attendance is {current_percent:.1f}%. You can safely miss about {can_bunk} more classes and stay above {required_percent}%."
    else:
        # How many more classes do you need to attend consecutively to reach required_percent?
        # Solve (attended + x) / (total + x) = required_percent
        # x = (required_percent*total - 100*attended) / (100 - required_percent)
        need = (required_percent * current_classes - 100 * attended_classes) / (100 - required_percent)
        need = int(need) + 1
        return f"Your attendance is {current_percent:.1f}%. You must attend the next {need} classes in a row to reach {required_percent}%."

def show_help():
    """Return help text with all main features."""
    return (
        "Here are some things you can ask me:\n"
        "- Greetings: 'hi', 'hello', 'how are you'\n"
        "- About me: 'what is your name', 'who created you'\n"
        "- Coding help: 'coding tips', 'how to learn DSA', 'explain big o', 'python or c++'\n"
        "- Movie suggestions: 'suggest a movie', 'sci-fi movies', 'anime movies'\n"
        "- Attendance: 'attendance 40 30' (40 classes total, 30 attended)\n"
        "- Study / life: 'study tips', 'motivate me', 'i am tired'\n"
        "- Fun: 'tell me a joke'\n"
        "- Type 'bye' or 'quit' to exit."
    )

PATTERNS = [
    # Greetings
    (r'\b(hi|hello|hey)\b', [
        "Hello! How can I help you today?",
        "Hi there! What do you want to talk about?",
        "Hey! Need help with coding, movies, or attendance?"
    ]),

    (r'\bhow are you\b', [
        "I'm doing great, thanks for asking! How are you?",
        "All systems running fine. How are you feeling?",
        "I’m good. Ready to help you with anything."
    ]),

    # About bot
    (r'\bwhat is your name\b', [
        "I'm a simple AI chatbot built by Samarth Shukla.",
        "You can call me SamBot, made by Samarth Shukla.",
        "I'm Samarth's chatbot project for his AI/ML portfolio."
    ]),

    (r'\b(who created you|your creator)\b', [
        "I was created by Samarth Shukla, B.Tech CSE (AIML) at SRMIST Delhi NCR.",
        "Samarth Shukla built me as a rule-based chatbot project.",
        "My creator is Samarth Shukla."
    ]),

    # Help / options
    (r'\b(help|options|what can i ask|what can you do)\b', [
        show_help
    ]),

    # Coding help
    (r'\bcoding tips\b', [
        "Start with small problems daily, then move to LeetCode / Codeforces. Focus on understanding, not memorizing.",
        "Pick one language (Python or C++) and be consistent. Solve at least 2–3 DSA problems each day.",
        "Read other people's solutions after trying yourself. You learn patterns and clean coding style."
    ]),

    (r'\bhow to learn dsa\b', [
        "Start with arrays, strings, hash maps, and two pointers. Then move to recursion, trees, and DP.",
        "Pick a roadmap: arrays → strings → stacks/queues → trees → graphs → DP. Solve at least 5–10 questions per topic."
    ]),

    (r'\b(explain big o|what is big o)\b', [
        "Big O describes how fast or slow an algorithm grows as input size increases. Example: O(n) grows linearly, O(n^2) much slower.",
        "Think of Big O as 'how many steps' roughly. Fewer steps for large n is better."
    ]),

    (r'\b(python or c\+\+)\b', [
        "Python is faster to write and great for ML and quick scripts. C++ is faster to run and used in competitive programming.",
        "If you care about interviews and LeetCode speed, C++ is solid. For AI/ML projects and fast prototyping, Python is perfect."
    ]),

    # Movie suggestions
    (r'\b(suggest a movie|movie recommendation|movie suggester|recommend a movie)\b', [
        lambda: get_movie_suggestions()
    ]),

    (r'\b(sci[- ]?fi movies|science fiction movies)\b', [
        lambda: get_movie_suggestions("sci-fi")
    ]),

    (r'\b(action movies)\b', [
        lambda: get_movie_suggestions("action")
    ]),

    (r'\b(drama movies)\b', [
        lambda: get_movie_suggestions("drama")
    ]),

    (r'\b(anime movies?|anime)\b', [
        lambda: get_movie_suggestions("anime")
    ]),

    # Attendance calculator: pattern like "attendance 40 30"
    (r'\battendance\s+(\d+)\s+(\d+)\b', 'attendance'),

    # Study / life conversations
    (r'\bstudy tips\b', [
        "Use 25 minutes focus + 5 minute break (Pomodoro). Put phone away during the 25 minutes.",
        "Teach the topic to an imaginary friend. If you can explain it simply, you understand it."
    ]),

    (r'\b(motivate me|i am tired|i feel lazy)\b', [
        "Totally normal to feel tired. Do one very small task now, just 5 minutes. Momentum matters more than motivation.",
        "Remember why you started B.Tech CSE (AIML). Future you will thank present you for today’s 30 minutes of focus.",
        "You don't have to be perfect; you just need to be a little better than yesterday."
    ]),

    # Jokes
    (r'\b(joke|make me laugh|tell me a joke)\b', [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "There are only 10 types of people in the world: those who understand binary and those who don't.",
        "I had a bug in my code, so I added a print statement. Now I have two problems."
    ]),
]

# -----------------------------
# CORE CHATBOT FUNCTIONS
# -----------------------------

def clean_input(text: str) -> str:
    """Lowercase and strip extra spaces."""
    return text.strip().lower()

def find_response(user_input: str) -> str:
    """Match user input against patterns and return a response string."""
    text = clean_input(user_input)

    for pattern, responses in PATTERNS:
        match = re.search(pattern, text)
        if not match:
            continue

        # Attendance special case
        if responses == 'attendance':
            total_classes = int(match.group(1))
            attended_classes = int(match.group(2))
            return calculate_attendance(total_classes, attended_classes)

        # If response is a callable (function), call it
        if callable(responses):
            return responses()

        # If response is a list, randomly choose one
        if isinstance(responses, list):
            # Some list entries may be functions (like lambda for movies)
            choice = random.choice(responses)
            if callable(choice):
                return choice()
            return choice

    # Fallback if nothing matched
    fallback_responses = [
        "That's interesting. You can type 'help' to see what I can do.",
        "I'm not sure about that yet. Try asking for 'help' to see my skills.",
        "I didn't understand fully. Type 'help' to see example questions."
    ]
    return random.choice(fallback_responses)

def display_welcome():
    """Print welcome banner."""
    print("\n" + "=" * 60)
    print("SAMARTH'S AI CHATBOT")
    print("=" * 60)
    print("Type 'help' to see what I can do.")
    print("Type 'bye' or 'quit' to exit.\n")

def main():
    """Main chat loop."""
    display_welcome()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ["bye", "quit", "exit", "goodbye"]:
            print("Chatbot: Goodbye! Have a great day.")
            break

        response = find_response(user_input)
        print(f"Chatbot: {response}\n")

if __name__ == "__main__":
    main()

