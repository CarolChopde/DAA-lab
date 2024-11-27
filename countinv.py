"""Consider first/second year course-code choices of 100 students. 
Find inversion count of these choices.
Find students with zero, one, two, three inversion counts comment on your result. 
"""

import random

def merge_splitcount(C,D):
    B = []
    i, j, splitcount =  0, 0, 0
    while i<len(C) and j<len(D):
        if C[i] < D[j]:
            B.append(C[i])
            i+=1
        else:
            B.append(D[j])
            j+=1
            splitcount += len(C) - i 

    #if any elements are still left
    if i < len(C):
        B.extend(C[i:])
    if j < len(D):
        B.extend(D[j:])

    return (B, splitcount)

def CountInv(arr):
    n = len(arr)
    mid = len(arr)//2
    if (len(arr) < 2):
        return (arr, 0)
    
    else:
        C, leftinv = CountInv(arr[:mid])
        D, rightinv = CountInv(arr[mid:])
        B, splitinv = merge_splitcount(C,D)
        return (B, leftinv+rightinv+splitinv)

def inversion_counts_of_students(course_codes_list):
    inversion_counts = []
    
    # For each student's course code list, calculate inversion count
    for codes in course_codes_list:
        _, inversion_count = CountInv(codes)
        inversion_counts.append(inversion_count)
    
    # Count students with 0, 1, 2, or 3 inversions
    count_zero = inversion_counts.count(0)
    count_one = inversion_counts.count(1)
    count_two = inversion_counts.count(2)
    count_three = inversion_counts.count(3)
    
    return count_zero, count_one, count_two, count_three

# User input
course_codes = [] #list of lists where each list contains course codes selected by a student
for _ in range(100):
    student_courses = random.sample(range(1, 11), 5)  # 5 course codes per student
    course_codes.append(student_courses)

A = []
count = 0
A, count = CountInv(course_codes)
count_zero, count_one, count_two, count_three = inversion_counts_of_students(course_codes)
print(f"Number of students with 0 inversions: {count_zero}")
print(f"Number of students with 1 inversion: {count_one}")
print(f"Number of students with 2 inversions: {count_two}")
print(f"Number of students with 3 inversions: {count_three}")

