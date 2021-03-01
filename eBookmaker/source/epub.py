#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog as fd, Text
from tkinter import messagebox as msg
from PIL import Image, ImageTk
import socket
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
import shutil
import ebooklib
from ebooklib import epub
import codecs
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import io
from time import sleep
import sys

HEIGHT = 500
WIDTH = 800

root = tk.Tk()
root.title("Welcome to eBook Maker")

# placing GUI window at the center of the screen
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/4 - windowWidth/3) + 20
positionDown = int(root.winfo_screenheight()/4 - windowHeight/3) + 20
root.geometry("+{}+{}".format(positionRight, positionDown))

# GUI variables
dirpath = tk.StringVar()
url = tk.StringVar()

# variables for progress bar
progress_bar = None
progress_var = tk.DoubleVar()
progress=0
popup = None
pb_label = tk.StringVar()


# In[3]:


# ---------------- directories for keeping temporary files ---------------->>>
pathTemp = '__tempdir__'
pathImg = 'images'
textfilepath = ''


listOfFiles = []
listofImg = []
book_title=''


# # Step 3 : creating epub from all the links
# (Sanjana's code)

# In[4]:


def generate_epub(url, path):
    '''
    Generate epub document at the given path, taking list of html file names of listOfFiles and taking images from listofImg.
    Each html file is added as a new chapter.
    
    Parameters
    -----------
        path : Path to which epub is saved, as given by the user in the GUI.
        
    Returns
    ---------
        Status of execution: "Okay" if successful ; Exception otherwise.
        
    '''
    global pb_label
    global progress
    global progress_var
    global popup
    # setting progress in progress bar
    popup.title("Generating Epub...")
    pb_label.set("Now generating epub from extracted contents....")
    popup.update()
    sleep(5/1000) # lauch task
    progress = 85
    progress_var.set(progress)
    
    try:
        book = epub.EpubBook()
        # add metadata
        book.set_identifier('sample12345678')
        
        book.set_title(book_title)
        book.set_language('en')
        object_list = []
        spine_list = ['cover', 'nav']
        
        book.add_author('We_did_our_best')

        img = Image.open("cover.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", size=20)
        MAX_W, MAX_H = img.size
        w, h = draw.textsize(book_title, font=font)
        draw.text(((MAX_W - w) / 2, (MAX_H - h) / 2), book_title, fill="white", font=font, anchor="ms", align="center")

        img.save('cover-out.jpg')
        book.set_cover("cover-out.jpg", open('cover-out.jpg', 'rb').read())
        
        j = 0
        global listOfFiles
        global listofImg
        for i in listOfFiles:
            htmlfile = i + ".html"
            pathForTemp = os.path.join(path, pathTemp)
            htmlfilepath = pathForTemp + "/" + htmlfile
            file = codecs.open(htmlfilepath, "r", "utf-8")
            
            content = file.read()
            soup1 = BeautifulSoup(content, "html.parser")
            chaptertitle = soup1.find('title').string
            # Adding chapters
            chaptertitle = chaptertitle.strip()

            c1 = epub.EpubHtml(title=chaptertitle, file_name=chaptertitle + '.xhtml', lang='en')
            c1.content = content
            object_list.append(c1)
            spine_list.append(c1)
            book.add_item(c1)
            j = j + 1

        # adding images
        for img in listofImg:
            ext = img.split(".")[-1]
            if ext == "svg":
                continue
            elif ext == "jpg":
                ext1 = "JPEG"
            else:
                ext1 = ext

            i = Image.open(img)
            b = io.BytesIO();
            i.save(b, ext1)
            j = b.getvalue()
            ei = epub.EpubImage()
            ei.file_name = img
            ei.media_type = 'image/' + ext
            ei.content = j
            book.add_item(ei)

            # add table of contents
        book.toc = object_list

        # add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # define css style
        style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
    }
    h2 {
         text-align: left;
         text-transform: uppercase;
         font-weight: 200;     
    }
    ol {
            list-style-type: none;
    }
    ol > li:first-child {
            margin-top: 0.3em;
    }
    nav[epub|type~='toc'] > ol > li > ol  {
        list-style-type:square;
    }
    nav[epub|type~='toc'] > ol > li > ol > li {
            margin-top: 0.3em;
    }
    '''

        # add css file
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        book.add_item(nav_css)

        # spine
        book.spine = spine_list

        # create epub file
        
        epubname = os.path.join(path, book_title + '.epub')
        
        epub.write_epub(epubname, book, {})
        
    except Exception as e:
        listOfFiles=[]
        listofImg=[]
        print(e)
        return "Exception"
    
    listOfFiles=[]
    listofImg=[]
    
    # setting progress in progress bar
    popup.update()
    sleep(5/1000) # lauch task
    progress = 100
    pb_label.set("saved epub doc at: \n{} ....".format(path))
    progress_var.set(progress)
    popup.update()
    sleep(3)
    popup.withdraw()
    
    print("saved epub doc at {}".format(path))
    return "Okay"
   
    


# # Step 2: Extracting content from nested URLs
# (Manjusree's code)

# In[5]:


# ---------------- for each link in links.txt, call function to extract HTML contents  ---------------->>>
def extract_contents(url, path, textfilepath):
    '''
    For each link present in __links__.txt , call extractPerLink() to extract HTML contents.
    
    Parameters
    -----------
        path : Path to which epub is saved, as given by the user in the GUI.
        textfilepath : Path to the file __links__.txt that contains the urls to be extracted.
        
    Returns
    --------
        Status of execution: "Okay" if successful ; Exception otherwise.
    '''
    global pb_label
    global progress
    global popup
    popup.title("Extracting contents...")
    try:
        
        pathForTemp = os.path.join(path, pathTemp)
        if os.path.isdir(pathForTemp):
            shutil.rmtree(pathForTemp)

        os.makedirs(pathForTemp)
        ipfile = open(textfilepath, 'r')
        for urls in ipfile:
            
            try:
                retname = extractPerLink(urls, pathForTemp)
                listOfFiles.append(retname)
                
            except (requests.ConnectionError, requests.Timeout) as y:
                return "No internet"
            
            except Exception as e:
                pass
                

        # ---------------- storing the list of files in listoffiles.txt ---------------->>>
        flist = open(os.path.join(pathForTemp, "listoffiles.txt"), "w")
        for htmlfilename in listOfFiles:
            flist.write(htmlfilename + ".html\n")
        flist.close()
        
        
        
        popup.update()
        pb_label.set("Extraction done....")
        popup.update()
        sleep(5/1000) # lauch task
        progress = 65
        progress_var.set(progress)
        
    except (requests.ConnectionError, requests.Timeout) as y:
        return "No internet"
    
    except Exception as e:
        return "Exception"
    
    return "Okay"

# ---------------- for given URL, extract HTML contents  ---------------->>>
def extractPerLink(url, pathArg):
    '''
    For a given URL, extract HTML contents, save as .html file in a temporary directory created.
    
    Parameters
    ------------
        url : The URL from which the content is to be extracted.
        pathArg : Path to the temporary directory created at the path specified by user in GUI for saving epub.
        
    Returns
    ---------
        The name of the html file created.
        
    '''
    global listofImg
    url = url.strip()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titlePage = soup.find('title')
    # ---------------- declare two lists to store class tag and id tag to be removed from main content ---------------->>>
    taglistClass = []
    taglistId = []
    h2listClass = []
    mainContent = ''

    # ---------------- define the lists to store class tag and id tag specific to website to be removed from main content ---------------->>>
    if "tutorialspoint.com" in url:
        taglistClass = ['center-aligned tutorial-menu', 'mui-container-fluid button-borders', 'tutorial-home-menu']
        taglistId = ['bottom_navigation', 'google-bottom-ads', 'google-top-ads']
        mainContent = 'mui-col-md-6 tutorial-content'
    elif "geeksforgeeks.org" in url:
        taglistClass = ['clear hideIt', 'plugins', 'recommendedPostsDiv', 'code-gutter', 'code-editor-container', 'code-output-container']
        taglistId = ['AP_G4GR_5', 'AP_G4GR_6']
        h2listClass = ['tabtitle']
        mainContent = 'entry-content'
    elif "geeksquiz.com" in url:
        taglistClass = ['clear hideIt', 'plugins', 'recommendedPostsDiv', 'code-gutter', 'code-editor-container', 'code-output-container']
        taglistId = ['AP_G4GR_5', 'AP_G4GR_6']
        h2listClass = ['tabtitle']
        mainContent = 'entry-content'
    elif "docs.python.org" in url:
        taglistClass = ['toctree-wrapper compound']
        mainContent = 'section'
    elif "numpy.org" in url:
        taglistClass = ['admonition seealso']
        mainContent = 'bodywrapper'

    # ---------------- extracting main content ---------------->>>
    # ---------------- mainContent for URLs with # (fragment specifier) ---------------->>>
    if "#" in url:
        fragid = url.split("#")[-1]
        mainContent = fragid
        results = soup.find(id=mainContent)
    else:
        # ---------------- mainContent for complete webpage ---------------->>>
        results = soup.find(class_=mainContent)

    # ---------------- remove the tags mentioned in the lists if present ---------------->>>
    for itemClass in taglistClass:
        if results.find_all("div", {"class": itemClass}):
            for eachdivClass in results.find_all("div", {"class": itemClass}):
                eachdivClass.decompose()

    for itemId in taglistId:
        if results.find_all("div", {'id': itemId}):
            for eachdivId in results.find_all('div', {'id': itemId}):
                eachdivId.decompose()

    for itemh2Class in h2listClass:
        if results.find_all("h2", {"class": itemh2Class}):
            for eachh2Class in results.find_all("h2", {"class": itemh2Class}):
                eachh2Class.decompose()
    
    global pb_label
    global progress
    global popup
    popup.update()
    sleep(5/1000) # lauch task
    progress = 45
    progress_var.set(progress)
    pb_label.set("Extracting contents from...\n{}".format(url))
    
    # ---------------- extracting Images ---------------->>>
    urls = []
    for img in results.find_all("img"):
        img_url = img.attrs.get("src")
        if not img_url:
            # no src attribute
            continue
        # join domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        # check if the url is valid
        if is_valid(img_url):
            urls.append(img_url)

    for img in urls:
        # for each img, download it
        oppath = os.path.join(pathArg, pathImg)
        downloadImg(img, oppath)

    
    for img in results.find_all("img"):
        img_url = img.attrs.get("src")
        img_new_url = os.path.join(pathArg, pathImg, img_url.split("/")[-1])
        img['src'] = img_new_url
        listofImg.append(img_new_url)
        
    listofImg = list(set(listofImg))
    # ---------------- writing the content to file ---------------->>>
    if url.split("/")[-1] == '':
        # ---------------- URLs ending with / ---------------->>>
        htmlfilename = url.split("/")[-2]
    else:
        htmlfilename = url.split("/")[-1]

    f = open(os.path.join(pathArg, htmlfilename + ".html"), "w", encoding="utf-8")
    f.write(titlePage.prettify())
    f.write(results.prettify())
    f.close()

    return htmlfilename


# ---------------- functions for extracting images ---------------->>>
def is_valid(url):
    '''
    Check if the url of image present in the webpage is valid or not.
    Parameters
    -----------
        url : URL of the image to be downloaded.
    Returns
    ----------
        True or False 
    '''
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def downloadImg(url, pathname):
    '''
    Downloads the image specified by the URL to the temporary images folder.
    
    Parameters
    ------------
        url : URL of the image contained in the webpage.
        pathname : Path to the "images" folder inside the temporary directory created.
        
    No Return Value
    '''
    # ---------------- downloads the image file given by url to the pathname path ---------------->>>
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True,unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    


# # Step 1 : Extracting links from the input URL
# (Sneha's code)

# In[6]:


def extract_links(url, path, doctype=1):
    '''
    It fetches the useful links of content from the webpage of given URL.
    
    Parameters
    -------------
        url : It is URL inputted by the user in the GUI
        path : Path to which epub is saved, as given by the user in the GUI.
        doctype : Whether the user wants to convert a "Single Page" or "Complete Tutorial" into epub. By default "Complete Tutorial"(1)
        
    Returns
    ---------
        Status of execution: "Okay" if successful ; Exception otherwise.
        
    '''
    tables = []
    list = []
    ulist = []

    try:
        url = url.strip()
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find("title")
        global book_title
        global textfilepath
        book_title = title.string
        print("Book title: {}".format(book_title))
        textfilepath = path + "/__links__.txt"
        if (doctype == 2):

            # -----------------------------to get main url-------------------------------------------->>>
            if ".com" in url:
                url_without_extension = url.split('.com')
                url_with_extension = url_without_extension[0] + ".com"
            elif ".org" in url:
                url_without_extension = url.split('.org')
                url_with_extension = url_without_extension[0] + ".org"
            elif ".net" in url:
                url_without_extension = url.split('.net')
                url_with_extension = url_without_extension[0] + ".net"
            elif ".in" in url:
                url_without_extension = url.split('.in')
                url_with_extension = url_without_extension[0] + ".in"
            else:
                print("Please enter valid URL")

            if "python.org" in url:
                url_with_extension = url
                if (url_with_extension[-1] == "/"):
                    url_with_extension = url_with_extension[:-1]

            if "numpy.org" in url:
                url_with_extension = url
                if (url_with_extension[-1] == "/"):
                    url_with_extension = url_with_extension[:-1]

            if "geeksforgeeks.org" in url:
                url_with_extension = ""
            

            # ----------------------to get main content----------------------------------------------->>>
            testing_links = [ "/must-do-coding-questions-for-companies-like-amazon-microsoft-adobe/", 
                         "/must-coding-questions-company-wise/", 
                         "/top-10-programming-languages-to-learn-in-2020-demand-jobs-career-growth/", 
                         "/quadratic-probing-in-hashing/", 
                         "/how-to-fix-the-height-of-rows-in-the-table/", 
                         "geeksforgeeks.org/top-40-python-interview-questions-answers/", 
                         "/upload-and-retrieve-image-on-mongodb-using-mongoose/", 
                         "/how-to-set-input-type-date-in-dd-mm-yyyy-format-using-html/", 
                         "/pass-by-reference-vs-value-in-python/", 
                         "geeksforgeeks.org/contribute/", 
                         "/write-interview-experience/", 
                         "/internship/",
                         "/how-to-contribute-videos-to-geeksforgeeks/",
                         "/copyright-information/",
                         "geeksforgeeks.org/tag/",
                         "auth.geeksforgeeks",
                         "linkedin.com",
                         "practice.geeksforgeeks",
                         "quiz.geeksforgeeks",
                         "geeksquiz.com/", 
                         "youtube.com/"
                         ]
            if "geeksforgeeks.org" in url:
                main_list = []
                ol_list = soup.find_all('ol')
                if (len(ol_list)>3):
                    content_olist = []
                    for i in ol_list:
                        content_list = []
                        content_list.clear()
                        for j in i.find_all('a', href=True):
                            alist = j['href']
                            if alist != []:
                                content_list.append(alist) 
                        if content_list != []:
                            content_olist.append(content_list)
                        main_list.append(content_olist)
                    
                else:
                    for div in soup.find_all("p"): 
                        div.decompose()
                    for div in soup.find_all("footer"): 
                        div.decompose()            
                    for div in soup.find_all("article"): 
                        div.decompose()
                    for div in soup.find_all('ul', {'class':'leftBarList'}):
                        div.decompose()
                    for div in soup.find_all("div", {'class':'leftSideBarParent'}): 
                        div.decompose()
                    for div in soup.find_all("div", {'class':'header-main__wrapper'}): 
                        div.decompose()
                    for div in soup.find_all("div", {'class':'cookie-consent hide-consent'}): 
                        div.decompose()

                    alist = []
                    main_list = []
                    for j in soup.find_all('a', href=True):
                        alist.append(j['href'])
                    print(len(alist))

                    true_false = []
                    for i in alist:
                        for j in testing_links:
                            if j in i:
                                true_false.append(j)
                        
                        if len(true_false)==0:
                            main_list.append(i)
                        true_false.clear()
                    MyFile = open(textfilepath,'w')

                    for element in main_list:
                        MyFile.write(element)
                        MyFile.write('\n')
                    MyFile.close()
                    exit()

            elif "tutorialspoint" in url:
                ul_list = soup.find_all('ul')
                content_ulist = []
                for i in ul_list:
                    content_list = []
                    content_list.clear()
                    for j in i.find_all('a', href=True):
                        alist = j['href']
                        if alist != []:
                            content_list.append(alist) 
                    if content_list != []:
                        content_ulist.append(content_list)
                #-------------name of tutorial
                a = url.split("/")
                for i in a:
                    if (i == "www.tutorialspoint.com"):
                        j =a.index(i)
                        j +=1
                    if (a.index(i) == j):
                        topic = i
                temp_link = topic+"/index.htm"
                
                #---------------------extract links from tutorialspoint
                main_list = []
                main_list1 = []
                for i in content_ulist:
                        for j in i:
                            if temp_link in j:
                                main_list1.append(i)
                for i in main_list1:
                    for j in i:
                        main_list.append(j)
                
            
            else:
                ul_list = soup.find_all('ul')
                content_ulist = []
                for i in ul_list:
                    content_list = []
                    content_list.clear()
                    for j in i.find_all('a', href=True):
                        alist = j['href']
                        if alist != []:
                            content_list.append(alist) 
                    if content_list != []:
                        content_ulist.append(content_list)
                main_list = max(content_ulist, key=len)
                    
            global pb_label
            global progress
            global popup
            popup.update()
            sleep(5/1000) # lauch task
            progress = 20
            progress_var.set(progress)
            # ---------------------to check list elements starts with slash otherwise add it---------->>>
            if "geeksforgeeks.org" not in url:
                main_list1 = [i[0] for i in main_list]
                if "/" in main_list1:
                    main_list = main_list
                else:
                    main_list = ["/" + list_ele for list_ele in main_list]
                    
            # -------------------check if list has unnecessary string starts with #------------------->>>
            if "geeksforgeeks.org" not in url:
                main_list = [i.split("#")[0] for i in main_list]
            

            # ------------------get only unique urls-------------------------------------------------->>>
            unique_list = []
            for x in main_list:
                if (x[-1] == "/"):
                    x = x[:-1]
                if x not in unique_list:
                    unique_list.append(x)
            main_list.clear()
            main_list = [None] * len(unique_list)
            for i in range(len(unique_list)):
                main_list[i] = unique_list[i]

            # ------------------to attach url with list elements-------------------------------------->>>
            if "geeksforgeeks.org" not in url:
                final_list = [url_with_extension + list_ele for list_ele in main_list]
            
            else:
                final_list = []
                for i in main_list:
                    for j in i:
                        for k in j:
                            final_list.append(k)

            # -----------------writing links in text file--------------------------------------------->>>
            MyFile = open(textfilepath, 'w')

            for element in final_list:
                MyFile.write(element)
                MyFile.write('\n')
            MyFile.close()
           
        else:
            MyFile = open(textfilepath, 'w')
            MyFile.write(url)
            MyFile.close()
            
        
    except (requests.ConnectionError, requests.Timeout) as y:
        return "No internet"
    
    except socket.error as e:
        print(e)
        return "Invalid URL"
    
    except Exception as e:
        return "Exception"
    else:
        pb_label.set("Now processing extracted links in a text file..")
        popup.update()
        sleep(5/1000) # lauch task
        progress = 30
        progress_var.set(progress)
        
    return "Okay" 
        


# # GUI code

# In[ ]:


def delete_temp_folder(path):
    '''
    Deletes temporary files and folders, if created, that were necessary for the execution and creation of epub document.
    
    Parameters:
    -------------
        path : Path to temporary files and folders; which is same as the path inputted by the user in GUI.
        
    No Return values.
    '''
    # deleting all the temporary files and folders
    global textfilepath
    path = os.path.join(path,'__tempdir__')
    if os.path.isdir(path):
        shutil.rmtree(path)
        
    if os.path.isfile(textfilepath):
        os.remove(textfilepath)

    if os.path.isfile('cover-out.jpg'):
        os.remove('cover-out.jpg')
        
def on_closing():
    '''
    When user wants to close the application, it displays a prompt, and once user confirms quitting, closes all the windows and terminates all the background processes.
    
    No parameters
    
    No Return Values
    '''
    if msg.askokcancel("Quit", "Do you want to quit?"):
        if popup:
            popup.destroy()
        root.destroy()
        os._exit(0)

def take_path():
    '''
    This function is bound to "Browse" button of GUI and it allows the user to browse through all the locations on his computer to select the destination for epub document.
    
    No parameters.
    
    No Return Values.
    
    '''
    path = fd.askdirectory()
    pathEntry.config(state='normal')
    pathEntry.delete(0, "end")
    pathEntry.insert(0, path)
    pathEntry.config(state="disabled")
    dirpath.set(path)
    


def validate_entries():
    '''
    This function is bound to "Generate epub" button. It checks if all the input fields are non-empty.
    Calls extract_links(), extract_contents(), and generate_epub() and handles exceptions.
    Calls delete_temp_folder() at the end.
    
    No parameters.
    
    No Return Values.
    
    '''
    invalid = False
    url = URLentry.get()
    path = pathEntry.get()
    

    # checking if entries are empty
    if url == "" or url == 'Enter URL:' or path == "Browse to select location" or path == "":
        msg.showerror("Invalid arguments:",
                      "Error: URL and location can't be empty. \n Please insert url or select a location.")
        invalid = True

    elif pagevar.get() == 0:
        msg.showerror("Document type not selected:",
                      "Error: please select whether you want single page epub or complete tutorial.")
        invalid = True
    else:
        invalid = False
        # a variable to check if user wants complete tutorial epub or single page epub.
        tutorial = pagevar.get()
        pagevar.set(0)

    response = True
    # if entries are non-empty , then proceed.
    if invalid == False:
        # code for progress bar:
        global popup
        global progress_var
        global progress_bar
        global progress
        global pb_label
        global textfilepath
        
        # a popup window for progress bar
        popup = tk.Toplevel(root)
        
        # placing popup window at the center of root window
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        positionRight = int(WIDTH/4 - windowWidth/3) + 500
        positionDown = int(HEIGHT/4 - windowHeight/3) +340
        popup.geometry("+{}+{}".format(positionRight, positionDown))
        
        popup.geometry('600x150')
        popup.title("Extracting Links....")
        popup.transient(root)
        popup.iconbitmap("book_icon.ico") # adding an icon
        
        progress_frame = tk.Frame(popup)
        progress_frame.place(relx=0.5, rely=0.05, relwidth=0.95, relheight=0.80, anchor='n')
        
        progress_label= tk.Label(progress_frame ,textvariable = pb_label).place(relx=0.1, rely=0, relwidth = 0.80, relheight = 0.3)
        pb_label.set("Generating Epub doc....")
        
        progress = 0
        progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
        progress_bar.place(relx=0.1,rely=0.40,relwidth=0.75 , relheight=0.25)
        popup.pack_slaves()
        
        bookbutton['state'] = "disabled"
        browseButton['state'] = 'disabled'
        # <======== STEP 1  ============================================= >>
        response = extract_links(url, path, tutorial)
        if response == "Invalid URL":
            msg.showerror("Invalid url:", "Error: Please enter a valid url")
            popup.withdraw()
        elif response == "No internet":
            msg.showerror("Unable to connect:", "Error: Please check your internet connection!")
            popup.withdraw()
        elif response=="Exception":
            msg.showerror("Unable to process:", "Error: Some error occured while processing.\n Please try again.")
            popup.withdraw()
           
        else:
             # <======== STEP 2  ============================================= >>
            response = extract_contents(url, path, textfilepath) # step 2
            if response == "No internet":
                msg.showerror("Unable to connect:", "Error: Please check your internet connection!")
                popup.withdraw()
            elif response == "Exception":
                msg.showerror("Unable to process:", "Error: Some error occured while processing.\n Please try again.")
                popup.withdraw()
               
            else:
                 # <======== STEP 3  ============================================= >>
                response = generate_epub(url, path) # step 3
                if response == "Exception":
                    msg.showerror("Unable to process:", "Error: Some error occured while processing.\n Please try again.")
                    popup.withdraw()
                    
    delete_temp_folder(path)
    browseButton['state'] = 'normal'   
    bookbutton['state'] = "normal"
    
def URLentry_click(event):
    '''
    This function is bound to "URLentry" entry widget of GUI. When user FOCUS-IN, it takes appropriate action.
    
    Parameter:
    -----------
        event : call-back event.
    
    No Return Values.
    
    '''
    if URLentry.get() == 'Enter URL:':
        URLentry.delete(0, "end")
        URLentry.insert(0, '')


def singlepage():
    '''
    It is bound to "Single Page" radio button, indicates contents from a single page to be extracted.
    
    No Parameters
    
    No Return Values
    
    '''
    pagevar.set(1)


def multipage():
    '''
    It is bound to "Complete Tutorial" radio button, indicates contents from the whole tutorial to be extracted.
    
    No Parameters
    
    No Return Values
    
    '''
    pagevar.set(2)


def resize_image(event):
    '''
    Resizing the background image to the size of the GUI window.
    
    Parameter:
    ------------
        event : callback event.
        
    No return values.
    
    '''
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    back_label.config(image=photo)
    back_label.image = photo  

if __name__ == '__main__' : 
    '''
    Creating a GUI structure, adding widgets, binding events to widgets.
    
    '''
    # adding canvas to the root window
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()
    
    # adding background image to the root window
    bg_image = Image.open('bg_gif.gif')
    copy_of_image = bg_image.copy()
    back_img = ImageTk.PhotoImage(bg_image)
    back_label = ttk.Label(root, image=back_img)
    back_label.place(x=0.75, y=0.75, relwidth=1, relheight=1)
    back_label.bind('<Configure>', resize_image)
    
    
    # creating a frame for URLentry widget
    urlframe = tk.Frame(root, bg='#fae4a7', bd=5)
    urlframe.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

    # placing an entry widget in URL frame for taking input URL 
    URLentry = tk.Entry(urlframe, font=("Times", 15))
    URLentry.place(relwidth=1, relheight=1)
    URLentry.insert(0, 'Enter URL:')
    URLentry.bind('<FocusIn>', URLentry_click)
    
    # create label for URL frame
    urlLabel = tk.Label(urlframe, text="Enter URL", bg='white')
    urlLabel.place(relx=0.255, rely=0, relwidth=0.45, relheight=0.25)

    #creating a frame for pathentry and Browse button widgets
    pathframe = tk.Frame(root, bg='#fae4a7', bd=5)
    pathframe.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.1, anchor='n')

    pathEntry = tk.Entry(pathframe, font=("courier", 10, "italic", "bold"))
    pathEntry.place(relwidth=0.84, relheight=1)
    pathEntry.insert(0, 'Browse to select location')
    pathEntry.config(state="disabled")

    browseButton = tk.Button(pathframe, text='Browse', bg='gray', fg='white', command=take_path)
    browseButton.place(relx=0.85, relwidth=0.15, relheight=0.8)

    createbookframe = tk.Frame(root, bg='#fae4a7', bd=5)
    createbookframe.place(relx=0.5, rely=0.40, relwidth=0.75, relheight=0.25, anchor='n')

    pagevar = tk.IntVar()
    pagevar.set(0)
    onepage = tk.Radiobutton(createbookframe, text="Single Page", font=("Times", 15, "bold"), bg='#fae4a7',
                             command=singlepage, variable=pagevar, value=1, anchor='n')
    onepage.place(relx=0.05, rely=0.075, relwidth=0.30, relheight=0.5)

    multipage = tk.Radiobutton(createbookframe, text='Complete Tutorial', font=("Times", 15, "bold"), bg='#fae4a7',
                               command=multipage, variable=pagevar, value=2, anchor='n')
    multipage.place(relx=0.4, rely=0.075, relwidth=0.60, relheight=0.5)

    
    bookbutton = tk.Button(createbookframe, text='Generate Epub', bg='gray', fg='white', command=validate_entries)
    bookbutton.place(relx=0.35, rely=0.5, relwidth=0.25, relheight=0.3)

    # when closing window...pop message 'Do you want to quit?'
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # adding icon
    root.iconbitmap("book_icon.ico")
    
    root.mainloop()


# ## Test links
# 1. tutorialspoint done
# 2. python.org done
# 3. numpy.org done
# 4. geeksforgeeks done
# 
#     
# ## for testing tutorials links
# 1. https://www.tutorialspoint.com/cprogramming/index.htm 
# 2. https://www.geeksforgeeks.org/c-programming-language/ 
# 3. https://numpy.org/doc/stable/user/quickstart.html 
# 4. https://docs.python.org/3/tutorial/ 
# 
# ### for testing specific from those tutorials
# 1. https://www.tutorialspoint.com/cprogramming/c_variables.htm
# 2. https://numpy.org/doc/stable/user/quickstart.html#universal-functions
# 3. https://docs.python.org/3/tutorial/introduction.html
# 
# 

# In[ ]:





# In[ ]:




