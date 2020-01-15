# PDF-Bible
This contains a simple python script to pull a PDF Bible from biblehub.com. 

Background:
  With the proliferation of laptops with pen support, I was looking for a PDF version of a bible so that I would be able to take handwritten notes in the digital age. Unfortunately, due to copyright issues (I assume) most bibles are not made availible in PDF format. As a result, I made my own.

Dependencies:
-urllib3 to access the site
-beautifulsoup to parse the HTML
-Python 3
-Command line LaTeX installation

Notes:
  This program was written for a linux environment, so the system call to LaTeX may not work on Windows. If it breaks, the program still produces a valide .tex document that can be complied by your editor of choice. 

  If you do use linux (which you should!), you can install latex using "sudo apt-get install texlive-full". Be warned, it will take around 3 Gb of storage.
