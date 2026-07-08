import random 
import tkinter as tk 
from tkinter import messagebox as mb
import os 

DATA_FILE = os.path.join(os.path.dirname(__file__), "records.txt")


root = tk.Tk()
root.title("REGISTRATION FORM")
root.geometry("400x400")

tk.Label(root, text="CONGRATUALTIONS! YOU HAVE BEEN SHORTLISTED AT ABC UNIVERSITY.\n AS THE NEXT STEP , PLEASE FILL THE FORM BELOW AND GENERATE YOUR ROLL NUMBER. ").pack(pady=10)
tk.Label(root, text="Name:").pack(pady=5)
name = tk.Entry(root)
name.pack(pady=5)
tk.Label(root, text="Date of Birth:").pack(pady=5)
dob = tk.Entry(root)
dob.pack(pady=5)
tk.Label(root, text="Course:").pack(pady=5)
course = tk.Entry(root)
course.pack(pady=5)

rai = ["253URA001" , "253URA002" , "253URA003" , "253URA004" , "253URA005" , "253URA006" , "253URA007" , "253URA008" , "253URA009" , "253URA010" , "253URA011" , "253URA012" , "253URA013" , "253URA014" , "253URA015" ]
mechanical = ["253UME001" , "253UME002" , "253UME003" , "253UME004" , "253UME005" , "253UME006" , "253UME007" , "253UME008" , "253UME009" , "253UME010" , "253UME011" , "253UME012" , "253UME013" , "253UME014" , "253UME015"]
civil = ["253UCE001" , "253UCE002" , "253UCE003" , "253UCE004" , "253UCE005" , "253UCE006" , "253UCE007" , "253UCE008" , "253UCE009" , "253UCE010" , "253UCE011" , "253UCE012" , "253UCE013" , "253UCE014" , "253UCE015"]

def get_roll_number(course_value):
    course_lower = course_value.lower()
    
    if course_lower == "robotics and ai" or course_lower == "rai":
        if not rai:
            raise Exception("All RAI roll numbers have been assigned!")
        assigned = random.choice(rai)
        rai.remove(assigned)
        return assigned
    elif course_lower == "mechanical engineering" or course_lower == "mechanical":
        if not mechanical:
            raise Exception("All Mechanical roll numbers have been assigned!")
        assigned = random.choice(mechanical)
        mechanical.remove(assigned)
        return assigned
    elif course_lower == "civil engineering" or course_lower == "civil":
        if not civil:
            raise Exception("All Civil roll numbers have been assigned!")
        assigned = random.choice(civil)
        civil.remove(assigned)
        return assigned
    else:
        raise Exception("Invalid course! Please enter: RAI, Mechanical, or Civil")


def record():
    try:
        name_value = name.get()
        dob_value = dob.get()
        course_value = course.get()

        if not name_value or not dob_value or not course_value:
            mb.showerror("Error", "Please fill in all fields.")
            return

        roll_number = get_roll_number(course_value)

        if not name_value or not dob_value or not course_value:
            mb.showerror("Error", "Please fill in all fields.")
            return

        with open(DATA_FILE, "a") as file:
            file.write(f"Name: {name_value}, DOB: {dob_value}, Course: {course_value}, Roll Number: {roll_number}\n")

        mb.showinfo("Success", f"Registration successful! Your roll number is: {roll_number}")
   
    except Exception as e:
        mb.showerror("Error", f"An error occurred: {str(e)}\nFile: {DATA_FILE}")

tk.Button(root, text="Submit", command=record).pack(pady=20)








root.mainloop()
