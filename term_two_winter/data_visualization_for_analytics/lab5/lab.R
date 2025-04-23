# Step 1: Create Vectors
# Create character vector of student names
student_names <- c("Alice", "Bob", "Carol", "David")
# Create numeric vector of scores
scores <- c(85, 90, 78, 92)

# Step 2: Create a Data Frame
students <- data.frame(
  name = student_names,
  score = scores
)
print(students)

# Step 3: Inspect the students data frame
# View the structure of the data frame
str(students)

# Get summary statistics
summary(students)

# View the first few rows
head(students)

# View the last few rows
tail(students)

#Step 4: Summary Calculations
mean(students$score)
median(students$score)
students[which.max(students$score), ]

# Step 5.1: Get rows where score > 80
students[students$score > 80, ]

# Step 5.2: Extract just the names column
students$name
# students name as a data frame
students[, "name", drop = FALSE]

# Step 6: Add a grade column
students$grade <- ifelse(
  students$score >= 90, "A",
  ifelse(students$score >= 80, "B", "C")
)

print(students)

# Step 7: Sort by Score (Descending)
students <- students[order(-students$score), ]
print(students)

# Step 8.1: Save to CSV
write.csv(students, "students.csv", row.names = FALSE)

# Step 8.2: Load it back in
students_new <- read.csv("students.csv")
print(students_new)

# Step 9: Add a New Row
#Create a new row for Eva
new_row <- data.frame(
  name = "Eva",
  score = 88,
  grade = ifelse(88 >= 90, "A", ifelse(88 >= 80, "B", "C"))
)

#Add Eva to the students data frame
students <- rbind(students, new_row)

# Re-sort the Data After Adding Eva
students <- students[order(-students$score), ]
print(students)

