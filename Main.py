import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "database.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
#cursor.execute("SELECT * FROM users")
#print(cursor.fetchall())
#conn.close()

# This code connects to a SQLite database located in the same directory as this script,
# retrieves all records from the 'users' table, and prints them to the console.



def opening_statement():
    print("Welcome to the SQLite Database Viewer!")
    print("This application connects to a local SQLite database and retrieves data from it for you to track your fitness!.")
    print("Make sure the database file 'database.db' exists in the same directory as this script.")
    print("You can sign in and view your data easily or create a new account.")
    print("You can also enter your own specific workouts and your personal records.")
    print("Let's get started!")




def options_menu():
    print("Options Menu:")
    print("1. Sign In")
    print("2. Create New Account")
    print("3. Exit")
    choice = input("Please select an option (1-3):").strip()
    return choice




def sign_in():
        while True:
            username = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()
            cursor.execute("SELECT id FROM users WHERE email = ? AND password = ? ", (username, password,))
            result = cursor.fetchone()
            if result is not None:
                return username, password
            else:
                print("Invalid email or password. Please try again.")

def sign_in_menu():
    print("Sign In Menu:")
    print("1. View Workouts")
    print("2. Add Workout PR")
    print("3. Sign Out")
    choice = input("Please select an option (1-3):").strip()
    return choice
    



def create_account():
    print("Create New Account")
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ")
    name = input("Enter your name: ")
    cursor.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)", (email, password, name))
    conn.commit()
    print("Account created successfully.")

def add_workout(username, password):
    print("Add New Workout Best Record")
    workout_name = input("Enter workout name: ").strip()
    workout_weight = input("Enter workout weight: ").strip()
    workout_reps = input("Enter workout reps: ").strip()
    workout_duration = input("If applicable, enter workout duration (in minutes): ").strip()
    if workout_duration == '':
        workout_duration = None
    else:
        workout_duration = int(workout_duration)
    workout_type = input("Enter workout area focus: ").strip()
    fon = cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (username, password))
    user_id = fon.fetchone()[0]
    cursor.execute("INSERT INTO user_workouts (user_id, workout_name, affected_muscle) VALUES (?, ?, ?);",
                   (user_id, workout_name, workout_type))
    workout_id = cursor.lastrowid
    cursor.execute("INSERT INTO user_workouts_prs (workout_id, workout_weight, workout_reps, duration_minutes) VALUES (?, ?, ?, ?);", (workout_id,workout_weight, workout_reps, workout_duration))
    conn.commit()
    print("Workout added successfully.")

def view_workouts(username, password):
    fon = cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (username, password))
    user_id = fon.fetchone()[0]
    cursor.execute("""
        SELECT
        user_workouts.workout_name,
        user_workouts.affected_muscle,
        user_workouts_prs.workout_weight,
        user_workouts_prs.workout_reps,
        user_workouts_prs.duration_minutes
        FROM user_workouts
        JOIN user_workouts_prs ON user_workouts.workout_id = user_workouts_prs.workout_id
        WHERE user_workouts.user_id = ?;
        """, (user_id,))
    workouts = cursor.fetchall()

    if not workouts:
        print("No workout records found.")
        return

    print("Your Workout Records:")
    for workout in workouts:
        workout_name, affected_muscle, workout_weight, workout_reps, duration_minutes = workout
        print(f"Workout Name: {workout_name}, Affected Muscle: {affected_muscle}, Weight: {workout_weight}, Reps: {workout_reps}, Duration (minutes): {duration_minutes}")
    



if __name__ == "__main__":
    opening_statement()
    while True:
        choice = options_menu()
        if choice == '1':
            while True:
                username, password= sign_in()
                print("You are now signed in.")
                menu_choice = sign_in_menu()
                if menu_choice == '1':
                    print("View workout records.")
                    view_workouts(username, password)
                    
                elif menu_choice == '2':
                    add_workout(username, password)
                elif menu_choice == '3':
                    print("Signing out.")
                    break
                else:
                    print("Invalid option.")

        elif choice == '2':
            print("Create New Account selected.")
            if create_account() == True:
                print("Account created successfully.")
        elif choice == '3':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

