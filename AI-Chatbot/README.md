# AI Chatbot (Rule-Based)

Simple terminal chatbot built with Python. It uses regex pattern matching to answer common questions and includes a help menu, movie suggestions, coding tips, and an attendance calculator.

## Features

- Greetings and small talk (`hi`, `how are you`, `who created you`)
- `help` command listing what you can ask
- Coding help (DSA tips, Big-O explanation, Python vs C++)
- Movie suggestions by mood/genre
- Attendance calculator using: `attendance 40 30` (40 classes, 30 attended)
- Fallback responses when no pattern matches

## How to Run

cd AI-Chatbot
python3 -m pip install -r requirements.txt # first time only
python3 chatbot.py

text

Then try messages like:

- `help`
- `coding tips`
- `movie recommendation`
- `attendance 40 30`
- `motivate me`
- `bye`

## Interview Talking Points

- Built a rule-based chatbot using regex patterns to detect different intents.
- Designed a help system so users can discover available commands.
- Implemented small tools inside the bot (movie recommender, attendance calculator).
- Can be extended to a true AI chatbot by replacing rule-based replies with an LLM API.

## CV Snippet

AI Chatbot (Python, regex) – Rule-based terminal chatbot with help menu, movie suggestions, coding tips, and attendance calculator.

