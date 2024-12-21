"""
Script to calculate the sum and mean of birth year, month, and day values.
This script prints the calculated results along with the user's name and student number.

Instructions:
- Replace `year_of_birth`, `month_of_birth`, and `day_of_birth` with actual values.
- Update `name` and `student_number` with your personal information.


The script is formatted according to PEP 8 guidelines:
    Variable names are in lowercase with underscores.
    There’s consistent spacing between sections for readability.
    Lines do not exceed 79 characters.
    Inline comments are used sparingly and only where necessary.
"""

# Define variables for year, month, and day of birth
year_of_birth = 1995
month_of_birth = 8
day_of_birth = 26

# Calculate the sum of year, month, and day
birth_sum = year_of_birth + month_of_birth + day_of_birth

# Calculate the mean by dividing the sum by 3 (since we have 3 values)
birth_mean = birth_sum / 3

# Define student details
name = "Chioma Onyekpere"
student_number = "3188187"

# Print results
print("Name:", name)
print("Student Number:", student_number)
print("Sum of year, month, and day of birth:", birth_sum)
print("Mean of year, month, and day of birth:", birth_mean)
