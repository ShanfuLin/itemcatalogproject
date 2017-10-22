ITEM CATALOG APPLICATION (UDACITY PROJECT FOR FSND STUDENTS)

Overview
Item catalog is a project that students of Udacity's Full Stack Nanodegree have to complete as part of their graduation criteria from the program.

Software Requirements
The software components needed to run this python code is VirtualBox (VB) (https://www.virtualbox.org/wiki/Downloads), Vagrant (https://www.vagrantup.com/downloads.html), Python 2, sqlalchemy, flask, oauth2client, and httplib2 library.
Together, VB and Vagrant forms the Virtual Machine (VM) which the virtual database is managed and residing in. If you are interested in learning more about how VM works, watch youtube video (https://www.youtube.com/watch?v=djnqoEO2rLc) to find out more.

Quickstart

1. Importing of code from GITHUB

From your terminal, run the following code to clone the code needed to run the application:

    git clone https://github.com/ShanfuLin/itemcatalogproject.git

This will give you a directory named itemcatalogproject completed with the source code for the application:
  a) coding_core.py (file containing all the code that handle all the HTTP requests, OAuth authentication process)
  b) project_dbsetup.py (file that help set up the backend database framework for the application)
  c) dummydata.py (file that provide the users with some dummy data to try out the application)
  d) Templates folder that contain all the html templates required for the application
  e) static folder that contain all the css files for the html templates

2. Run and start up the virtual machine

Using the terminal, change directory to the itemcatalogproject (**cd itemcatalogproject**), then type **vagrant up** to launch your virtual machine.
Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt.  After you have typed **vagrant ssh** change to the /vagrant directory by typing **cd /vagrant**. This will take you to the folder in virtual machine and host machine where you will see all the files and folders mentioned in (1).

3. Starting the application

If this is your first time running the application, set up the database by first running the file dummydata.py by typing **python dummydata.py**. Once the database is set up, the application is now ready to be run. Type **python coding_core.py** to run application on your port5000 of your localhost. When this is done successfully, you should see the following code on your terminal.

  ** Running on http://0.0.0.0:5000/
  ** Restarting with reloader

 To view the application, open any of your browser and enter "http://0.0.0.0:5000/" in the URL field. Voila! You have successfully launched the application and are now ready to explore its features.
 License/usage restriction

This is a public domain work and there is no license/usage restriction on it. Please feel free to use/modify the codes in anyway to suit your own needs. If you have more questions pertaining to this application, drop an email to Shanfu87@yahoo.com and I will be happy to assist you.
