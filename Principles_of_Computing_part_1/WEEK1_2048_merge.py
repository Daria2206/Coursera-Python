"""
Principles of Computing (by Coursera and Rice
University). Week 1 programming assignment: "Merge function for 2048 game".
Link to code in CodeSculptor: http://www.codeskulptor.org/#user42_kw5TP25GmE_2.py
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    output = [x for x in line if x != 0]

    for num in range(1, len(output)):
        if len(output) > num:
            key = output[num]
            prev = num - 1

            if output[prev] == key:
                output[prev + 1] = output[prev] * 2
                output[prev:prev + 1] = []

    num_of_zeros_to_fill = len(line) - len(output)
    output += [0] * num_of_zeros_to_fill

    return output
