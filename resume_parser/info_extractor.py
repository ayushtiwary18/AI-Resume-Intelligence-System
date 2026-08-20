import re


def extract_email(text):

    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


def extract_phone(text):

    pattern = r'(\+91[-\s]?)?[6-9]\d{9}'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None

def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip lines containing contact information
        if "@" in line or re.search(r"\d", line):
            continue

        # Skip common resume headings
        excluded_words = [
            "resume",
            "curriculum vitae",
            "profile",
            "summary",
            "objective",
            "education",
            "experience",
            "skills"
        ]

        if line.lower() in excluded_words:
            continue

        # Basic name validation
        words = line.split()

        if 2 <= len(words) <= 4:
            if all(word.replace(".", "").isalpha() for word in words):
                return line

    return None