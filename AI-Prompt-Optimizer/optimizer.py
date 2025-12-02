# optimizer.py - AI Prompt Optimizer (pure Python)
# Run with:  python3 optimizer.py

import re
import random


class PromptOptimizer:
    """Analyze and improve text prompts for AI models."""

    def __init__(self):
        self.history = []

    def analyze(self, prompt: str) -> dict:
        """Return a quality score and list of issues."""
        score = 100
        issues = []

        text = prompt.strip()

        if len(text) < 15:
            issues.append("Prompt is very short. Add more detail and context.")
            score -= 25

        if text and text[0].islower():
            issues.append("Start the prompt with a capital letter for clarity.")
            score -= 5

        uncertain = re.findall(r"\b(maybe|probably|might|could|possibly|somehow)\b", text, re.IGNORECASE)
        if uncertain:
            issues.append("Remove uncertain words: " + ", ".join(sorted(set(uncertain))))
            score -= 15

        if not any(w in text.lower() for w in ["format", "style", "tone", "length", "steps", "bullet"]):
            issues.append("Specify output format (length, bullets, steps, style, tone).")
            score -= 20

        if not any(w in text.lower() for w in ["act as", "you are", "as an expert", "role:"]):
            issues.append("Add a role for the AI (e.g., 'Act as an expert tutor').")
            score -= 15

        if not any(w in text.lower() for w in ["example", "e.g.", "for instance"]):
            issues.append("Add at least one example of the desired output.")
            score -= 10

        return {
            "score": max(score, 0),
            "issues": issues,
            "length": len(text),
        }

    def enhance(self, prompt: str) -> str:
        """Return an improved version of the prompt."""
        base = prompt.strip()

        if not re.search(r"act as|you are|as an expert|role:", base, re.IGNORECASE):
            base = "You are an expert AI assistant. " + base

        if "format" not in base.lower():
            base += " Format the answer in clear sections with headings and bullet points where helpful."

        if "length" not in base.lower():
            base += " Keep the answer concise (about 3–5 short paragraphs)."

        # Make sure first letter is capital
        base = base[0].upper() + base[1:]

        return base

    def optimize_once(self, prompt: str) -> str:
        """Analyze + enhance a single prompt and print a report."""
        print("\n" + "=" * 70)
        print("AI PROMPT OPTIMIZER")
        print("=" * 70)

        print(f"\nOriginal prompt:\n\"{prompt}\"\n")

        report = self.analyze(prompt)
        print(f"Quality score: {report['score']}/100")
        print(f"Length: {report['length']} characters\n")

        if report["issues"]:
            print("Issues detected:")
            for i, issue in enumerate(report["issues"], start=1):
                print(f"  {i}. {issue}")
        else:
            print("No major issues detected. Prompt already looks strong.")

        improved = self.enhance(prompt)

        print("\nSuggested improved prompt:\n")
        print(improved)
        print()

        self.history.append(
            {"original": prompt, "improved": improved, "score": report["score"]}
        )

        return improved

    def interactive(self):
        """Loop to optimize multiple prompts from user input."""
        print("\n" + "=" * 70)
        print("INTERACTIVE MODE")
        print("=" * 70)
        print("Type a prompt and press Enter. Type 'quit' to exit.\n")

        while True:
            user_input = input("Enter your prompt: ").strip()
            if user_input.lower() in {"quit", "exit", "q"}:
                print(f"\nOptimized {len(self.history)} prompts. Goodbye!")
                break

            if not user_input:
                continue

            self.optimize_once(user_input)


def main():
    optimizer = PromptOptimizer()

    # Example prompts to show behaviour
    demo_prompts = [
        "write me a blog about ai",
        "maybe create some ideas for youtube videos",
    ]

    for p in demo_prompts:
        optimizer.optimize_once(p)

    start = input("\nStart interactive mode? (y/n): ").strip().lower()
    if start == "y":
        optimizer.interactive()


if __name__ == "__main__":
    main()

