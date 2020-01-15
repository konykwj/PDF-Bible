#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 05:39:52 2018

@author: konykwj

This file will pull all resolutions from the SBC into a folder. 
If there are changes to the website it will need to be changed as well (as has already happened!)
"""

import urllib3 as ul
from bs4 import BeautifulSoup
import re
import pickle
import os

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def latex_clean(string):
    string = re.sub(r"\n", "", string)
    string = re.sub(r"[\t]*", "", string)
    string = string.replace('&','\\&')
    string = string.replace('$','\\$')
    string = string.replace('%','\\%')
    string = string.replace('~','\\~')
    string = string.replace('^','\\^')
    string = string.replace('#','\\#')
    string = string.replace('_','\\_')
    string = string.replace('{','\\{')
    string = string.replace('}','\\}')
    string = string.replace('﷓','-')
    string = string.replace('“','``')
    string = string.replace('”',"''")
    return string


def write_chapter(main_file, chapter, book, book_title, site, hdr, missing_chapters):
    try:
        try:
            soup = pickle.load(open('./soup_objects/{}_{}.pkl'.format(book, chapter), 'rb'))
        
        except:
            req = http.request('GET',site, headers=hdr)
                
            try:
                content = req.data
            
                soup=BeautifulSoup(content, features = 'lxml')
            
                pickle.dump(soup, open('./soup_objects/{}_{}.pkl'.format(book, chapter), 'wb'))
            
            except:
                pass
            
        main_file.append('\\section{'+book_title+' '+str(chapter)+'}')
        
        text = soup.find_all('p')
        
        
        for paragraph in text:
            #These replace the divine name of the Lord, as it breaks the patterns.
            paragraph = str(paragraph).replace('<span class="divine-name">Lord</span>', 'LORD')
            paragraph = str(paragraph).replace('<span class="divine-name">God</span>', 'GOD')
            
            #This removes footnotes from the text. They have the form like so: <span class="footnote"><sup><a href="#footnotes" title="Some Hebrew manuscripts you">e</a></sup></span>
            paragraph = re.sub(r'<span class="footnote"(.*?)/span>', '', paragraph)
    
            #This captures the section headings
            if 'class="heading"' in str(paragraph):
                heading = re.findall(r">(.*?)<", str(paragraph))[0]
                main_file.append('\subsubsection{'+heading+'}')
                
            #This deals with regular, paragraph/block text.
            if 'class="regular"' in str(paragraph):
                #Pulls anything between brackets
                paragraph = re.findall(r'>([\w\W]*?)<', paragraph)
                
                latex_paragraph = []
                for words in paragraph:
                        
                    #Finds verse numbers first then appends to the main list.
                    try:
                        verse = int(words)
                        latex_paragraph.append('\\textsuperscript{'+str(verse)+'}')
                        
                    except ValueError:                
                        
                        if words == '':
                            pass
                        else:
                            words = latex_clean(words)
                            latex_paragraph.append(words+' ')
                    
                
                main_file.append(''.join(latex_paragraph))
                
            #This deals with the line-group, used for quotes, psalms, prophecy, etc.
            if 'class="line-group"' in str(paragraph):
                
                paragraph = re.findall(r'>([\w\W]*?)<', paragraph)
                
                latex_paragraph = []
                #The words_appended flag allows the program to correctly apply a line break after each section.
                words_appended = False
                #Moves the text over a bit. This can be adjusted as desired.
                latex_paragraph.append('\\begin{adjustwidth}{20pt}{0pt}')
                for words in paragraph:
                    
                    try:
                        verse = int(words)
                        latex_paragraph.append('\\textsuperscript{'+str(verse)+'}')
                        words_appended = False
    
                    except ValueError:                
                        
                        if words == '':
                            pass
                        else:
                            words = latex_clean(words)
                            latex_paragraph.append(words+' ')  #'\\hspace{\\parindent} '+
                            latex_paragraph.append(' ') #This is added to ensure that the new lines are created as desired
                            words_appended = True
                
                #Appends a line break if the last thing appended was text
                if words_appended == True:   
                    latex_paragraph.pop()
                    latex_paragraph.append('\\\\')
                
                #Appends to the main document.
                latex_paragraph.append('\\end{adjustwidth}')
                for line in latex_paragraph:
                    main_file.append(line)
    
            main_file.append(' ')
            
  
    except UnboundLocalError:
        print('Soup object was not produced.')
        missing_chapters.append([book_title, chapter, site])
        pickle.dump(missing_chapters, open('./missing_chapters.pkl','wb'))

            


'''
Control Variables
'''


#hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#       'Accept-Encoding': 'none',
#       'Accept-Language': 'en-US,en;q=0.8',
#       'Connection': 'keep-alive'}

hdr = { }


reslist=[]
blanklist=[]

http = ul.PoolManager()

bible_name = 'kjv'

mkdir('./soup_objects/')

title = 'The {} Translation of the Bible'.format(bible_name.upper())
author = 'Pulled From biblehub.com'
run_name = 'SBC_Resolutions'

report_final_location = './{}/'.format(bible_name)
filename = '{}_bible.tex'.format(bible_name)


#Creates the data structure for the main file. This will be written to a .tex file to be compiled by latex later.
main_file= []
#        \\graphicspath{{Images/}{'''+report_image_location+'''}} If desiring to add graphics...
#Appends the preamble to the main file
main_file.append('''

\\documentclass[12pt, letterpaper]{report}
\\usepackage[margin = 1.0in]{geometry} % see geometry.pdf on how to lay out the page. There's lots.
\\geometry{letterpaper} % or letter or a5paper or ... etc                 

\\usepackage{amssymb, graphicx, enumitem}
\\usepackage{indentfirst}
\\usepackage[colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black]{hyperref}
\\usepackage{titlesec}
\\usepackage{caption}
\\usepackage{float}
\\usepackage{changepage}

\\usepackage{sectsty}
\\renewcommand*\\arraystretch{.5}
\\chapterfont{\\normalsize}
\\sectionfont{\\normalsize}
\\subsectionfont{\\normalsize}
\\partfont{\\normalsize}

\\titleformat{\\chapter}[display]
  {\\normalfont\\bfseries}{}{0pt}{\\large}
  
\\titlespacing*{\\chapter}{0pt}{-40pt}{10pt}

\\makeatletter
\\renewcommand*{\\numberline}[1]{\\hb@xt@1em{\\hfil}} 
\\makeatother

\\title{'''+title+'''}
\\author{'''+author+'''}

\\begin{document}

\\maketitle


\\tableofcontents
\\vspace{-2cm}

\\newpage
\\pagenumbering{arabic}

''')

book_list = [
       ['Genesis',50],
       ['Exodus',40],
       ['Leviticus', 27],
       ['Numbers', 36],
       ['Deuteronomy', 34],
       
       ['Joshua', 24],
       ['Judges',21],
       ['Ruth',4],
       ['1 Samuel', 31],
       ['2 Samuel', 24],
       ['1 Kings',22],
       ['2 Kings',25],
       ['1 Chronicles',29],
       ['2 Chronicles',36],
       ['Ezra',10],
       ['Nehemiah',13],
       ['Esther',10],
       
       ['Job',42],
       ['Psalms',150],
       ['Proverbs',31],
       ['Ecclesiastes',12],
       ['Song of Solomon',8],
       
       ['Isaiah',66],
       ['Jeremiah',52],
       ['Lamentations',5],
       ['Ezekiel',48],
       ['Daniel',12],
       
       ['Hosea',14],
       ['Joel',3],
       ['Amos',9],
       ['Obadiah',1],
       ['Jonah',4],
       ['Micah',7],
       ['Nahum',3],
       ['Habakkuk',3],
       ['Zephaniah',3],
       ['Haggai',2],
       ['Zechariah',14],
       ['Malachi',4],
       
       ['Matthew',28],
       ['Mark',16],
       ['Luke',24],
       ['John',21],
       
       ['Acts',28],
       
       ['Romans',16],
       ['1 Corinthians',16],
       ['2 Corinthians', 13],
       ['Galatians',6],
       ['Ephesians',6],
       ['Philippians',4],
       ['Colossians',4],
       ['1 Thessalonians',5],
       ['2 Thessalonians',3],
       ['1 Timothy',6],
       ['2 Timothy',4],
       ['Titus',3],
       ['Philemon',1],
       
       ['Hebrews',13],
       ['James',5],
       ['1 Peter',5],
       ['2 Peter',3],
       ['1 John',5],
       ['2 John',1],
       ['3 John',1],
       ['Jude',1],
       
       ['Revelation',22]
        ]


missing_chapters = []

for book_info in book_list:
    chapters = range(book_info[1])
    book_title= book_info[0]
    if book_title == 'Song of Solomon':
        book = 'songs'
    else:
        book = book_title.replace(' ','_').lower()
    
    main_file.append("\\"+'chapter{'+book_title+'}')
    
    for chapter in chapters:
        print('Processing {}, chapter {}'.format(book_title, chapter+1))
        site='biblehub.com/{}/{}/{}.htm'.format(bible_name,book,chapter+1)
        print(site)
    
    
        write_chapter(main_file, chapter+1, book, book_title, site, hdr, missing_chapters)
        
main_file.append('''

\\end{document}
''')

#Writes main file
with open(filename, 'w') as f:
    for item in main_file:
        f.write("%s\n" % item)
          
#    
#This intentionally runs twice; I think that somehow this makes the table of contents load properly.
os.system('pdflatex '+filename)
os.system('pdflatex '+filename)