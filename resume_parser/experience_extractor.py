import re


def extract_experience(text):

    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
        r'(\d+)\+?\s*yrs?\s*(?:of)?\s*experience',
        r'experience\s*[:\-]?\s*(\d+)\+?\s*years?',
    ]

    experience = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:
            value = f"{match}+ Years"
            
            if value not in experience:
                experience.append(value)

    return experience