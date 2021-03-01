.. eBook Maker documentation master file, created by
   sphinx-quickstart on Thu Nov 26 22:25:10 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to eBook Maker's documentation!
=======================================
eBook Maker is a GUI application that lets you to download the content from any webpage onto your system as an epub document.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   dependencies

.. note:: This is a Windows application.

.. note::
   Works for the following links now:

   * Tutorial topics in https://www.tutorialspoint.com/.
   * https://www.geeksforgeeks.org/c-programming-language/ and other tutorial topics in geeksforgeeks.
   * https://numpy.org/doc/stable/user/quickstart.html.
   * https://docs.python.org/3/tutorial/.

Usage
-----
* Clone the repository.

.. code-block::

   $ git clone https://sanjnamohan@git.cse.iitb.ac.in/sanjnamohan/eBookmaker.git

.. note::
   Do not change the directory structure after cloning

* Make sure you have Python and pip installed

  * To install Python for Windows : https://www.python.org/downloads/windows/.
  * To install/upgrade pip : https://pip.pypa.io/en/stable/installing/.

* Go inside the folder "eBookmaker/source".

  Make sure the relevant libraries are installed:

.. code-block::

   $ pip install -r requirements.txt

* Double click on epub.exe file OR run the source file using:

.. code-block::

   $ python epub.py


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
