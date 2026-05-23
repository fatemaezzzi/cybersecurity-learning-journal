password = input("Enter a password: ") #Takes input from the user as a string and stores it in password
score = 0 #A counter. Every time the password meets a strength criterion, score goes up by 1. Maximum possible score is 5

if len(password) >= 8: #Checks if the password is at least 8 characters long. len() counts characters. += 1 means score = score + 1
    score += 1
if any (c.isupper() for c in password): #for c in password loops through every character. .isupper() checks if that character is uppercase. any() returns True if at least one character passes. So this checks: does the password contain at least one uppercase letter?
    score += 1
if any (c.islower() for c in password): #for lower case
    score += 1
if any (c.isdigit() for c in password): #checks if at least one character is a digit (0–9).
    score += 1
if any (c in "!@#$%^&*" for c in password): #Checks if any character in the password exists inside that string of special characters.
    score += 1

#Evaluates the final score. 0–2 = Weak, 3–4 = Medium, 5 = Strong.
if score <= 2:
    print("Weak")
elif score <= 4:
    print("Medium")
else:
    print("Strong")

# =+ assign something to the variable
# += assignment operator (eg: add operator)