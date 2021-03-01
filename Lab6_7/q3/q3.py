import os
import sqlite3
import requests 
from bs4 import BeautifulSoup 
from prettytable import from_db_cursor

class CSE_Courses:
    def __init__(self):
        self.mydb = sqlite3.connect('CSE_Courses_DB.db')
        cursor = self.mydb.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS CSE_Courses (Course_Code text AUTO_INCREMENT, Name text, Instructor text, PRIMARY KEY (Course_Code))''')
        self.mydb.commit()
        self.mydb.close()  
            
    def get_courses(self,url):
        assert(isinstance(url,str))
        table_d = []
        r = requests.get(url) 
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.prettify()
        table = soup.table
        tables = table.find_all('tr')
        for row in tables:
            table_c = row.find_all('td')
            row_d = []
            for r in table_c:
                row_c = r.text
                row_c = row_c.strip()
                row_d.append(row_c)
            table_d.append(row_d)
        courses = table_d[1:]
        assert(isinstance(courses,list) and isinstance(courses[0],list))
        return courses

    def insert_data(self,courses):
        assert(isinstance(courses,list) and isinstance(courses[0],list))
        self.mydb = sqlite3.connect('CSE_Courses_DB.db')
        cursor = self.mydb.cursor()
        try:
            for j in courses:
                cursor.execute("INSERT INTO CSE_Courses VALUES(?,?,?)",(j[0],j[1],j[2]))
            self.mydb.commit()
        except:
            self.mydb.rollback()
        self.mydb.close()
        

    def print_data(self):
        self.mydb = sqlite3.connect('CSE_Courses_DB.db')
        cursor = self.mydb.cursor()
        cursor.execute('SELECT * FROM CSE_Courses')
        x = from_db_cursor(cursor)
        x.align["Course_Code"] = "l"
        x.align["Name"] = "l"
        x.align["Instructor"] = "l"
        print(x)
        self.mydb.close()
        
    def delete_data(self,course_code=None):
        self.mydb = sqlite3.connect('CSE_Courses_DB.db')
        cursor = self.mydb.cursor()
        if course_code:
            assert(isinstance(course_code,str))
            cursor.execute("DELETE FROM CSE_Courses WHERE Course_Code=?", (course_code,))
            self.mydb.commit()
        else:
            cursor.execute("DELETE FROM CSE_Courses")
            self.mydb.commit()
        self.mydb.close()
        
if __name__ == "__main__":
    url = "https://www.cse.iitb.ac.in/archive/page136"
    cse = CSE_Courses()
    courses = cse.get_courses(url)
    cse.delete_data()
    cse.insert_data(courses)
    cse.print_data()
    os.remove("CSE_Courses_DB.db")
