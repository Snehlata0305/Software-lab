
CSE Git link:
 https://git.cse.iitb.ac.in/sanjnamohan/eBookmaker



Team Members:
  Sanjna Mohan (20305R006) : Merging of codes, Epub creation, Documentation
  Manjusree MP (203059007) : Content extraction from links and saving in required format for epub creation
  Pooja Gayakwad (203050076) : Merging of codes and GUI Implementation
  Snehlata Yadav (203050075) : Nested links extraction from webpage of inputted URL

Motivation:
  While going through vast tutorials on the web, sometimes it becomes tedious to go to all the links and read.
  Moreover, the availability only in the presence of Internet makes it difficult for future reference.
  We have come up with this project to ease the process and to download the tutorial onto our computers as an eBook.
  This way, not only we get the contents in an organized manner, but also we can avail it as and when we require.
  Our solution is a GUI application that takes the particular URL from the user as input, and use web scraping to get the contents as a centralized epub document which can be saved at our convenience.

NOTE:
  This is a Windows application.

How to use:
Clone the repository onto your system:
  git clone https://sanjnamohan@git.cse.iitb.ac.in/sanjnamohan/eBookmaker.git

To install Python for Windows : https://www.python.org/downloads/windows/
To install/upgrade pip : https://pip.pypa.io/en/stable/installing/ 

For executing:
NOTE:
  Do not change the directory structure after cloning.

  Go inside the folder "eBookmaker/source".

  Make sure the relevant libraries are installed:
    pip install -r requirements.txt

  Double click on epub.exe and wait for few seconds till the GUI appears.

  Once the GUI appears, enter the URL of which the document is to be created and select the destination folder using "Browse" button.
  Select either of "Single Page" or "Complete Tutorial" radio buttons and click "Generate Epub" button.
  The generated eBook would be present at the set destination folder.

Alternatively:

  Go inside the folder "eBookmaker/source"
  
  Make sure the relevant libraries are installed:
    pip install -r requirements.txt

  The source code is available in epub.py. To execute directly from the source, run:
    python epub.py

  Once the GUI appears, enter the URL of which the document is to be created and select the destination folder using "Browse" button.
  Select either of "Single Page" or "Complete Tutorial" radio buttons and click "Generate Epub" button.
  The generated eBook would be present at the set destination folder.


Works for the following links now:
    Tutorial topics in https://www.tutorialspoint.com/
    https://www.geeksforgeeks.org/c-programming-language/ and other tutorial topics in geeksforgeeks
    https://numpy.org/doc/stable/user/quickstart.html
    https://docs.python.org/3/tutorial/
    


References:
	https://www.tutorialspoint.com/python\_web\_scraping/index.htm
	https://www.geeksforgeeks.org/
	https://stackoverflow.com/
	https://nullprogram.com/blog/2017/05/15/
	https://github.com/aerkalov/ebooklib
	https://realpython.com/beautiful-soup-web-scraper-python/
	https://www.thepythoncode.com/article/download-web-page-images-python
	https://www.kite.com/python/answers/how-to-check-internet-connection-in-python
	https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
	https://youtu.be/D8-snVfekto

