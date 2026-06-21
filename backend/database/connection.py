import os  
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))  
# Locating to the database
target_file_path = os.path.join(current_dir, "nextgenforge.db")

#Function to connect to database
def connect_to_database():        
       conn = sqlite3.connect(target_file_path)
       return conn
