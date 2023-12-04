# Christopher Chamberlain
# Advent of Code 2023
# Day 1.2

# Read input data
with open("day_01_input.txt", encoding='utf-8') as file:
    input = file.readlines()

# ----
# Construct helpers
# ----

number_words = {
    "one": '1',
    "two": '2',
    "three": '3',
    "four": '4',
    "five": '5',
    "six": '6',
    "seven": '7',
    "eight": '8',
    "nine": '9',
}

# Table that maps the first letter of each word to their words
number_word_lookup = {w[0]: [] for w in number_words}
for word in number_words:
    number_word_lookup[word[0]].append(word)

# ----
# Compute answer
# ----

sum = 0
for line in input:

    digits = []

    i = 0
    while i < len(line):

        # If potentially a number word...
        if line[i] in number_word_lookup:
            # Try each candidate...
            for candidate in number_word_lookup[line[i]]:
                # Does this substring match the candidate?
                if line[i: i + len(candidate)] == candidate:
                    digits.append(number_words[candidate])
                    break

        # If potentially a regular digit...
        if line[i].isdigit():
            digits.append(line[i])

        i += 1

    print(digits)
    sum += int("".join([digits[0], digits[-1]]))

print(sum)  # 54249
