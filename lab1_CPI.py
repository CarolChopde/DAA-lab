import math
def compute_CPI(n, s, cred, grade):
    if n <= 0 or s <= 0: #no of sems or subjs cannot be 0
        return ("Invalid input")
    for i in range(n):
        for subj in range(s):  # for each subject
            sum, csum, SPIsum = 0.0, 0.0, 0.0
            #checking the criteria for grades and credits
            if cred[i][subj] < 0 or cred[i][subj] > 8 or grade[i][subj] < 0 or grade[i][subj] > 10: 
                return ("Invalid input")
            
            sum += (cred[i][subj] * grade[i][subj])
            csum += cred[i][subj] 

        if csum == 0: #denominator cannot be 0
            return "Invalid input"
        
        SPI = sum / csum
        SPIsum += SPI

    CPI = SPIsum / n
    print(CPI)
    return (round(CPI, 2))

n = int(input("Enter the total number of semesters: "))
s = int(input("Enter the total number of subjects per semester: "))
cred = []
grade = []

for i in range(n):
    cred.append([])
    grade.append([])
    print(f"Enter the credits and grades for semester {i + 1}:")
    for j in range(s):
        c = float(input(f"  Enter the credit for subject {j + 1}: "))
        g = float(input(f"  Enter the grade for subject {j + 1}: "))
        cred[i].append(c)
        grade[i].append(g)

result = compute_CPI(n, s, cred, grade)
print("CPI:", result)

 