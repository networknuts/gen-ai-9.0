import re

USER_AI_INPUT = """
Hello, my name is aryan and my email is Aryan@example.net
please draft an email from my prespective to my employer at 
Info@example.net asking for a 10 day PTO.
"""

normalized_input = USER_AI_INPUT.lower()

result = re.findall(r"\w+@\w+\.\w+",normalized_input)

sanitized_input = re.sub(r"\w+@\w+\.\w+","<REDACTED_EMAIL>",normalized_input)
print(sanitized_input)