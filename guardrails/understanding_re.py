import re 

EMAIL_DATA = """
john <john@networknuts.net>
jane <jane@networknuts.net>
arthur <arthur@networknuts.net>
thomas <thomas@networknuts.net>
chris <chris@networknuts.net>
bobbi <bobbi@networknuts.net>
"""

# SIMPLE STRING EXAMPLE
result_1 = re.search(r"[b,r]obb[i,y]",EMAIL_DATA)

# SEARCHING IF WE KNOW ONLY FIRST 3 LETTERS
result_2 = re.search(r"chr[a-z][a-z]",EMAIL_DATA)

# SEARCHING IF WE KNOW 3 LETTERS - BETTER WAY
result_3 = re.search(r"art[a-z]{3}",EMAIL_DATA)

# SEARCHING IF WE KNOW ONLY 1 OR X LETTERS
result_4 = re.search(r"j[a-z]+",EMAIL_DATA)

# SEARCHING FOR AN EMAIL ADDRESS - METHOD 1
result_5 = re.search(r"[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9]+",EMAIL_DATA)

# SEARCHING FOR ALL EMAIL ADDRESSES - METHOD 2
result_6 = re.findall(r"[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9]+",EMAIL_DATA)

# SEARCHING FOR ALL EMAIL ADDRESSES - METHOD 3
result_7 = re.findall(r"\w+@\w+\.\w+",EMAIL_DATA)
print(result_7)