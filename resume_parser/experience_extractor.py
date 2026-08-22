# import re


# def extract_experience(text):

#     text = text.lower()

#     patterns = [
#         r'\b\d+\+?\s+years?\b',
#         r'\b\d+\+?\s+yrs?\b',
#         r'\b\d+\s*-\s*\d+\s+years?\b'
#     ]

#     experience = []

#     for pattern in patterns:
#         matches = re.findall(pattern, text)

#         for match in matches:
#             if match not in experience:
#                 experience.append(match)

#     return experience