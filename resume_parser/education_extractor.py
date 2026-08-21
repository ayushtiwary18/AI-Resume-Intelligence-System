DEGREES = [
    "bachelor of technology",
    "b.tech",
    "btech",
    "bachelor of engineering",
    "b.e.",
    "master of technology",
    "m.tech",
    "mtech",
    "master of science",
    "m.sc",
    "msc",
    "bachelor of science",
    "b.sc",
    "bsc",
    "bachelor of computer applications",
    "bca",
    "master of computer applications",
    "mca",
    "mba",
    "phd"
]


def extract_education(text):

    found_degrees = []

    text = text.lower()

    for degree in DEGREES:

        if degree in text:
            found_degrees.append(degree)

    return found_degrees