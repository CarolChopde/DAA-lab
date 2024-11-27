import random
import csv
import os
from typing import List

# Generate random course grades for students
def generate_grades(num_students: int, seq_length: int) -> List[List[str]]:
    if not isinstance(num_students, int) or not isinstance(seq_length, int):
        raise TypeError("Number of students and sequence length must be integers.")
    if num_students <= 0 or seq_length <= 0:
        raise ValueError("Number of students and sequence length must be positive.")
    
    grades = ['AA', 'AB', 'BB', 'BC', 'CC', 'CD', 'DD', 'FF']
    
    # Generate grades for each student
    return [[random.choice(grades) for _ in range(seq_length)] for _ in range(num_students)]

# Save grades to a CSV file
def save_grades_to_csv(grades: List[List[str]], filename: str) -> None:
    if not filename:
        raise ValueError("Filename cannot be empty.")
    
    if not isinstance(grades, list):
        raise TypeError("Grades should be a list of lists.")
    
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = [f"Student{i+1}" for i in range(len(grades))]
            writer.writerow(header)  # Write header
            for student_grades in grades:
                if len(student_grades) != len(header):
                    raise ValueError(f"Mismatch in number of grades for a student: expected {len(header)}, but got {len(student_grades)}.")
                writer.writerow(student_grades)  # Write each student's grades
        print(f"Grades successfully saved to {filename}.")
    except (IOError, PermissionError) as e:
        print(f"Error writing to file {filename}: {e}")

# Read grades from CSV file
def read_grades_from_csv(filename: str, num_students: int, seq_length: int) -> List[List[str]]:
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read header
            if len(header) != seq_length:
                raise ValueError(f"CSV header length {len(header)} does not match expected sequence length {seq_length}.")
            
            student_grades = []
            for i, row in enumerate(reader):
                if len(row) != len(header):
                    raise ValueError(f"Row {i+1} has an incorrect number of columns (expected {len(header)}, got {len(row)}).")
                if len(row) != seq_length:
                    raise ValueError(f"Row {i+1} has an incorrect number of grades (expected {seq_length}, got {len(row)}).")
                student_grades.append(row)

            if len(student_grades) != num_students:
                raise ValueError(f"Expected {num_students} students, but found {len(student_grades)}.")
            
            return student_grades

    except (FileNotFoundError, IOError) as e:
        print(f"Error reading file {filename}: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    return []

# Find the Longest Common Sequence (LCS) between two students' grade sequences
def find_lcs(seq1: str, seq2: str) -> str:
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table for LCS calculation
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack to find the actual LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i-1] == seq2[j-1]:
            lcs.append(seq1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))

# Main function to generate grades, save, read and find LCS for student pairs
def main():
    num_students = 20
    seq_length = 10
    filename = 'student_grades.csv'

    try:
        # Generate and save grades to CSV
        grades = generate_grades(num_students, seq_length)
        save_grades_to_csv(grades, filename)

        # Read grades from CSV
        student_grades = read_grades_from_csv(filename, num_students, seq_length)
        if not student_grades:
            raise ValueError("Failed to read valid student grades from CSV.")

        # Debug: Print the first few rows of the student_grades to check structure
        print(f"Total rows read: {len(student_grades)}")
        for i, row in enumerate(student_grades[:5]):  # Print the first 5 rows
            print(f"Row {i+1}: {row}")

        # Compare each pair of students and print LCS
        for i in range(num_students):
            for j in range(i + 1, num_students):
                seq1 = ''.join(student_grades[i])  # This is the first student's grade sequence
                seq2 = ''.join(student_grades[j])  # This is the second student's grade sequence
                lcs = find_lcs(seq1, seq2)
                print(f" {i+1} & {j+1}: LCS: {lcs} (Length: {len(lcs) // 2})")
                
    except (ValueError, IOError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
