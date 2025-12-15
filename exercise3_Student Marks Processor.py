import numpy as np
import os
from datetime import datetime

def assign_grade(overall):
    if overall >= 70:
        return "A"
    elif overall >= 60:
        return "B"
    elif overall >= 50:
        return "C"
    elif overall >= 40:
        return "D"
    else:
        return "F"
    
def find_input_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(base_dir, "student_input.txt"),
        os.path.join(base_dir, "Week3_Assignment", "student_input.txt"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def process_marks():
    try:
        input_file = find_input_file()
        if input_file is None:
            print("Error: Input file 'student_input.txt' not found in expected locations.")
            return

        base_dir = os.path.dirname(input_file)
        output_file = os.path.join(base_dir, "students_output.txt")

        records = []
        with open(input_file, "r") as file:
            for line in file:
                reg_no, exam, coursework = line.strip().split(",")
                exam = float(exam)
                coursework = float(coursework)
                overall = (0.7 * exam) + (0.3 * coursework)
                grade = assign_grade(overall)
                records.append((reg_no, exam, coursework, overall, grade))

        dtype = [
            ("RegNo", "U10"),
            ("Exam", "f4"),
            ("Coursework", "f4"),
            ("Overall", "f4"),
            ("Grade", "U1")
        ]
        students_array = np.array(records, dtype=dtype)
        sorted_students = np.sort(students_array, order="Overall")[::-1]

        with open(output_file, "w") as file:
            file.write("RegNo,Exam,Coursework,Overall,Grade\n")
            for student in sorted_students:
                file.write(
                    f"{student['RegNo']},{student['Exam']:.2f},"
                    f"{student['Coursework']:.2f},{student['Overall']:.2f},"
                    f"{student['Grade']}\n"
                )

        grade_stats = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for student in sorted_students:
            grade_stats[student["Grade"]] += 1

        print("Grade Statistics:")
        for grade, count in grade_stats.items():
            print(f"Grade {grade}: {count} students")
        print("\nResults successfully written to", output_file)

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Please ensure it exists.")

    except ValueError:
        print("Error: Invalid mark detected in input file.")

    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    process_marks()
