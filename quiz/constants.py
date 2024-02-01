LANGUAGE_LIST = [
    "c",
    "cpp",
    "csharp",
    "css",
    "dart",
    "django",
    "docker",
    "git",
    "go",
    "go-module",
    "graphql",
    "java",
    "javascript",
    "json",
    "mongodb",
    "nginx",
    "pascal",
    "perl",
    "php",
    "python",
    "r",
    "regex",
    "ruby",
    "rust",
    "sql",
    "swift",
    "typescript",
]


DIFFICULTY_LIST = ["Easy", "Medium", "Hard"]

PROMPT = (
    "Create a {lang} {topic} {level} quiz with multiple-choice questions, "
    "each having four options and one correct answer. The quiz should cover fundamental"
    "concepts of {lang} programming related to {topic}. Each question should be structured "
    "as a dictionary containing the question, proper options a,b,c,d, and the correct answer."
    " If any question involves code, include the code snippet in a separate key. "
    "provides the quiz in the required format as a list of dictionaries, without any extra imports or functions."
)

PROMPT = (
    "Create unique {lang} Programming {level} Quiz for {topic} topic in the dictionary"
    "format in the dictionary format list of the dictionary where each dictionary will have"
    "these keys like the question, option_a, option_b, option_c, option_d, answer, if the question"
    "has code then add a key-like code and add that code into the code"
)


NEW_PROMPT = (
    "Convert the list of Python dictionary topics into an HTML format. "
    "Include headings, subheadings, and any necessary HTML tags to structure the content properly."
)
