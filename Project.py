import json
import os
from typing import List, Dict, Any

TASK_FILE = "tasks.json"

def load_tasks() -> List[Dict[str, Any]]:
    """Loads tasks from the JSON file, or returns an empty list if the file doesn't exist."""
    # Check if the file exists
    if not os.path.exists(TASK_FILE):
        return []
    
    try:
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Warning: {TASK_FILE} is corrupted or empty. Starting with an empty task list.")
        return []
    except Exception as e:
        print(f"An error occurred while loading tasks: {e}")
        return []

def save_tasks(tasks: List[Dict[str, Any]]):
    """Saves the current list of tasks to the JSON file."""
    try:
        with open(TASK_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving tasks: {e}")

def add_task(tasks: List[Dict[str, Any]]):
    """Prompts the user for a task description and adds it to the list."""
    description = input("Enter the new task description: ").strip()
    
    if description:
        new_task = {
            "id": len(tasks) + 1,
            "description": description,
            "done": False
        }
        tasks.append(new_task)
        save_tasks(tasks)
        print(f"\n✅ Task '{description}' added successfully.")
    else:
        print("\n❌ Task description cannot be empty.")

def view_tasks(tasks: List[Dict[str, Any]]):
    """Displays all tasks with their ID, status, and description."""
    print("\n" + "="*40)
    print("           📋 TO-DO LIST 📋")
    print("="*40)
    
    if not tasks:
        print("    The task list is currently empty.")
    else:
        print(f"| {'ID':<4} | {'Status':<8} | {'Task Description':<20} |")
        print("-" * 40)
        
        for task in tasks:
            status = "✅ Done" if task["done"] else "⏳ Pending"
            print(f"| {task['id']:<4} | {status:<8} | {task['description'][:20]:<20} |")
    
    print("="*40)

def mark_task_done(tasks: List[Dict[str, Any]]):
    """Marks a task as done based on its ID."""
    view_tasks(tasks)
    if not tasks:
        return
        
    try:
        task_id = int(input("Enter the ID of the task to mark as DONE: "))
    except ValueError:
        print("\n❌ Invalid input. Please enter a valid number for the ID.")
        return

    # Find the task by ID
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            found = True
            save_tasks(tasks)
            print(f"\n🎉 Task ID {task_id} marked as DONE: '{task['description']}'")
            break
            
    if not found:
        print(f"\n❌ Task with ID {task_id} not found.")

def delete_task(tasks: List[Dict[str, Any]]):
    """Deletes a task based on its ID."""
    view_tasks(tasks)
    if not tasks:
        return
        
    try:
        task_id = int(input("Enter the ID of the task to DELETE: "))
    except ValueError:
        print("\n❌ Invalid input. Please enter a valid number for the ID.")
        return

    initial_length = len(tasks)
    tasks[:] = [task for task in tasks if task["id"] != task_id]
    
    if len(tasks) < initial_length:
        for i, task in enumerate(tasks):
            task['id'] = i + 1
            
        save_tasks(tasks)
        print(f"\n🗑️ Task with ID {task_id} successfully deleted.")
    else:
        print(f"\n❌ Task with ID {task_id} not found.")


def main():
    tasks = load_tasks() 

    while True:
        print("\n" + "*"*40)
        print("    Python Task Management System CLI")
        print("*"*40)
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Mark task as done")
        print("4. Delete a task")
        print("5. Exit")
        print("*"*40)

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_task_done(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            print("\n👋 Saving and exiting. Goodbye!")
            break
        else:
            print("\n⚠️ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()