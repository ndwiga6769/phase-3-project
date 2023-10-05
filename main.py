#!/usr/bin/env python3

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    task_lists = relationship('TaskList', back_populates='user')

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username})>'

class TaskList(Base):
    __tablename__ = 'task_lists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship('User', back_populates='task_lists')
    tasks = relationship('Task', back_populates='task_list')

    def __repr__(self):
        return f'<TaskList(id={self.id}, title={self.title})>'

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    task_list_id = Column(Integer, ForeignKey('task_lists.id'))
    created_at = Column(DateTime, default=datetime.now)

    task_list = relationship('TaskList', back_populates='tasks')

    def __repr__(self):
        return f'<Task(id={self.id}, title={self.title}, description={self.description}, created_at={self.created_at})>'

# Initialize the database
engine = create_engine('sqlite:///todo_database.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# CRUD Operations

def create_user(session, username, password):
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    return user

def get_user_by_username(session, username):
    return session.query(User).filter(User.username == username).first()

def create_task_list(session, title, user_id):
    task_list = TaskList(title=title, user_id=user_id)
    session.add(task_list)
    session.commit()
    return task_list

def get_task_lists_by_user(session, user_id):
    return session.query(TaskList).filter(TaskList.user_id == user_id).all()

def create_task(session, title, description, task_list_id):
    task = Task(title=title, description=description, task_list_id=task_list_id)
    session.add(task)
    session.commit()
    return task

def get_tasks_by_task_list(session, task_list_id):
    return session.query(Task).filter(Task.task_list_id == task_list_id).all()

def update_task(session, task_id, title, description):
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        task.title = title
        task.description = description
        session.commit()
        return task
    return None

def delete_task(session, task_id):
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        session.delete(task)
        session.commit()
        return True
    return False

def delete_task_list(session, task_list_id):
    task_list = session.query(TaskList).filter(TaskList.id == task_list_id).first()
    if task_list:
        session.delete(task_list)
        session.commit()
        return True
    return False

def main():
    while True:
        print("=== To-Do List Management System ===")
        print("1. Create User")
        print("2. Create Task List")
        print("3. Create Task")
        print("4. View Tasks in a Task List")
        print("5. Update Task")
        print("6. Delete Task")
        print("7. Delete Task List")
        print("8. Quit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            username = input("Enter username: ")
            password = input("Enter password: ")
            create_user(session, username, password)
            print("User created successfully!")

        elif choice == 2:
            username = input("Enter username of the owner: ")
            user = get_user_by_username(session, username)
            if user:
                title = input("Enter task list title: ")
                create_task_list(session, title, user.id)
                print("Task list created successfully!")
            else:
                print("User not found.")

        elif choice == 3:
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            task_list_id = int(input("Enter task list ID: "))
            create_task(session, title, description, task_list_id)
            print("Task created successfully!")

        elif choice == 4:
            task_list_id = int(input("Enter task list ID: "))
            tasks_in_list = get_tasks_by_task_list(session, task_list_id)
            for task in tasks_in_list:
                print(f'Task ID: {task.id}, Title: {task.title}, Description: {task.description}, Created At: {task.created_at}')

        elif choice == 5:
            task_id = int(input("Enter task ID: "))
            title = input("Enter new task title: ")
            description = input("Enter new task description: ")
            update_task(session, task_id, title, description)
            print("Task updated successfully!")

        elif choice == 6:
            task_id = int(input("Enter task ID: "))
            delete_task(session, task_id)
            print("Task deleted successfully!")

        elif choice == 7:
            task_list_id = int(input("Enter task list ID: "))
            delete_task_list(session, task_list_id)
            print("Task list deleted successfully!")

        elif choice == 8:
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
