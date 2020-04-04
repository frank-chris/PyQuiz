
# importing required modules

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolTip, QLineEdit
from PyQt5 import *
from PyQt5.QtCore import *
from functools import partial
import requests
import re
import random
from bs4 import BeautifulSoup

# sources used to learn PyQt5:

# YouTube Channel:   https://www.youtube.com/watch?v=pnpL9Sl79g8&list=PL1FgJUcJJ03uwFW8ys2ov2dffKs3ieGYk&index=1
# StackOverflow:     https://stackoverflow.com/questions/21586643/pyqt-widget-connect-and-disconnect


# class for creating a QMainWindow

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.setGeometry(5,5,1910,1050)
        self.setWindowTitle("PyQuiz")

        self.labeli = QLabel(self)
        self.labeli.setPixmap(QtGui.QPixmap("top bar.png"))
        self.labeli.setGeometry(0,20,1920,140)
        self.show()                
            
    # function to close window
    def close(self):
        QCoreApplication.instance().quit()

        
# function to update text on a label
def updatelabel(label,t):
    label.setText(t)
    label.show()

# function to create a line edit
def createline(x,y,w,h):
    line=QLineEdit("Enter Quiz Code and Click Go",window)
    line.move(x,y)
    line.resize(w,h)
    line.selectAll()
    line.show()
    return line

# function to create a button
def createbutton(text,tip,x,y):
    button=QPushButton(text,window)
    button.move(x,y)
    button.setToolTip(tip)
    button.show()
    return button

# function to create a label
def createlabel(text,x,y,w,h):
    label = QLabel(window)
    label.setText(text)
    label.setStyleSheet("background-color: rgb(219,22,47); color:rgb(255,255,255); font:bold 16pt 'Helvetica'")
    label.setMargin(10)
    label.setGeometry(x,y,w,h)
    label.resize(w,h)
    label.show()
    return label

# function for general quizzes
def general(n):
    r=requests.get("http://www.quizballs.com/full-quiz-list/")
    c=r.content
    soup=BeautifulSoup(c,"html.parser")

    linksdict={}
    titlesdict={}

    links=soup.find_all("a")

    for link in  links:
        if re.search(r"(QA)",link.text):
            titlesdict[link.text.split()[1]]=link.text.strip("(QA)")
            linksdict[link.text.split()[1]]=link.get("href")
    
    quizmenu=""
    
    for i in titlesdict:
        quizmenu += titlesdict[i].strip("quiz")+"\n"
    
    quizmenu=quizmenu.split("\n")
    
    label1=createlabel("\n".join(quizmenu[17*(n-1):17*n]),30,190,600,590)
    label1.setStyleSheet("background-color: rgb(219,22,47); color:rgb(255,255,255); font:bold 20pt 'Helvetica'")
    label2=createlabel("\n".join(quizmenu[17*n:17*(n+1)]),660,190,600,590)
    label2.setStyleSheet("background-color: rgb(219,22,47); color:rgb(255,255,255); font:bold 20pt 'Helvetica'")
    label4=createlabel("\n".join(quizmenu[17*(n+1):17*(n+2)]),1290,190,600,590) 
    label4.setStyleSheet("background-color: rgb(219,22,47); color:rgb(255,255,255); font:bold 20pt 'Helvetica'")
    line1=createline(700,800,400,32)
    go=createbutton("Go","Go",1120,800)

    # function that executes a general quiz
    def choice():
        ch=line1.text()
        line1.deleteLater()
        label1.deleteLater()
        label2.deleteLater()
        label4.deleteLater()
        go.deleteLater()

        if  re.search(r"[^0-9]",ch):  
            general(n)
        
        elif int(ch) not in range(1733-17*(n+2),1733-17*(n-1)):
            general(n)
        else:

            title=createlabel(titlesdict[ch],1200,50,600,70)
            r=requests.get(linksdict[ch])
            c=r.content
            soup=BeautifulSoup(c,"html.parser")

            qnumlist=[]
            qqueslist=[]
            qanslist=[]
            qoptlist=[]

            numbers=soup.find_all("td",{"class":"wptable qnum"})
            for num in numbers:
                qnumlist.append(num.text)

            questions=soup.find_all("td",{"class":"wptable qques"})
            for ques in questions:
                qqueslist.append(ques.text.split("? ")[0]+"?")

            answers=soup.find_all("td",{"class":"wptable qans"})
            for ans in answers:
                qanslist.append(ans.text)

            # exception handling is applied on the following code blocks to ensure smooth working even if the requested webpage stores questions without options or without the required number of options
            try:
                for i in questions:
                    qoptlist.append(i.text.split("? ")[1].split(", "))
                            
                question=createlabel("",0,350,1920,510)
                question.setAlignment(QtCore.Qt.AlignCenter)
                opta=createbutton("Option A","A",700,720)
                optb=createbutton("Option B","B",1100,720)
                optc=createbutton("Option C","C",700,800)
                optd=createbutton("Option D","D",1100,800)
                
                # function to view quiz answers
                def view():
                    ansstr=""
                    for i in range(len(qnumlist)):
                        ansstr+=qnumlist[i]+". "+qqueslist[i]+"\t"+qanslist[i]+"\n"
                    question.setAlignment(QtCore.Qt.AlignLeft)
                    question.setAlignment(QtCore.Qt.AlignVCenter)
                    question.setGeometry(390,190,1140,590)
                    updatelabel(question,ansstr)

                # function to play quiz       
                def quizplay(h,score):
                    #functions that are executed on clicking an option button
                    def A():
                        opta.clicked.disconnect(A)
                        optb.clicked.disconnect(B)
                        optc.clicked.disconnect(C)
                        optd.clicked.disconnect(D)
                        if qoptlist[h][0]==qanslist[h]:
                            quizplay(h+1,score+1)
                        else:
                            quizplay(h+1,score)
                    def B():
                        opta.clicked.disconnect(A)
                        optb.clicked.disconnect(B)
                        optc.clicked.disconnect(C)
                        optd.clicked.disconnect(D)
                        if qoptlist[h][1]==qanslist[h]:
                            quizplay(h+1,score+1)
                        else:
                            quizplay(h+1,score)
                    def C():                
                        opta.clicked.disconnect(A)
                        optb.clicked.disconnect(B)
                        optc.clicked.disconnect(C)
                        optd.clicked.disconnect(D)
                        if qoptlist[h][2]==qanslist[h]:
                            quizplay(h+1,score+1)
                        else:
                            quizplay(h+1,score)                
                    def D():
                        opta.clicked.disconnect(A)
                        optb.clicked.disconnect(B)
                        optc.clicked.disconnect(C)
                        optd.clicked.disconnect(D)
                        if qoptlist[h][3]==qanslist[h]:
                            quizplay(h+1,score+1)
                        else:
                            quizplay(h+1,score)       

                    if h<len(qnumlist): 
                        print(h,score)
                        updatelabel(question,qnumlist[h]+". "+qqueslist[h]+"\nA. "+qoptlist[h][0]+"\tB. "+qoptlist[h][1]+"\nC. "+qoptlist[h][2]+"\tD. "+qoptlist[h][3])
                        opta.clicked.connect(A)
                        optb.clicked.connect(B)
                        optc.clicked.connect(C)
                        optd.clicked.connect(D)
                    elif h==len(qnumlist):
                        updatelabel(question,"You have scored "+str(score)+" out of 20")
                        opta.deleteLater()
                        optb.deleteLater()
                        optc.deleteLater()
                        optd.deleteLater()
                        home=createbutton("Return to Home Page","Click to return to home page",700,880)
                        viewans=createbutton("View Answers","Click to view the answers of the quiz",1000,880)
                        viewans.resize(200,32)
                        viewans.clicked.connect(view)
                        viewans.clicked.connect(viewans.deleteLater)
                        home.resize(200,32)
                        home.clicked.connect(question.deleteLater)
                        home.clicked.connect(viewans.deleteLater)
                        home.clicked.connect(title.deleteLater)
                        home.clicked.connect(main)
                        home.clicked.connect(home.deleteLater)
                quizplay(0,0)
            except:
                error=createlabel("We are sorry, but the quiz you chose can not be scraped as it does not meet the required format in the webpage\nPlease try another quiz",0,350,1920,300)
                error.setAlignment(QtCore.Qt.AlignCenter)
                back=createbutton("Back","Click to go back to the quiz list",850,850)
                back.clicked.connect(partial(general,n))
                back.clicked.connect(back.deleteLater)
                back.clicked.connect(error.deleteLater)
    go.clicked.connect(choice)

# function for quote-based quizzes
def quotesfunc():
    r=requests.get("https://www.brainyquote.com/topics")
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    
    topicslist=[]
    topics=soup.find_all("span",{"class":"topicContentName"})
    topicsdict={}

    for topic in topics:
        topicslist.append(topic.text) 
        topicsdict[topic.text]=topic.text

    label5=createlabel("\n".join(topicslist[:25]),70,190,300,640)
    label6=createlabel("\n".join(topicslist[25:50]),430,190,300,640)
    label7=createlabel("\n".join(topicslist[50:75]),790,190,300,640)
    label8=createlabel("\n".join(topicslist[75:100]),1150,190,300,640)
    label9=createlabel("\n".join(topicslist[100:]),1510,190,300,640)
    line2=QLineEdit("Enter Topic and Click Go",window)
    line2.move(700,850)
    line2.resize(400,32)
    line2.selectAll()
    line2.show()
    go=createbutton("Go","Go",1120,850)

    # function that executes a quote-based quiz
    def topicchoice():
        ch=line2.text()
        line2.deleteLater()
        label5.deleteLater()
        label6.deleteLater()
        label7.deleteLater()
        label8.deleteLater()
        label9.deleteLater()
        go.deleteLater()

        if ch.capitalize() not in topicslist:
            quotesfunc()

        title=createlabel(topicsdict[ch.capitalize()],1200,50,600,70)
        r=requests.get("https://www.brainyquote.com/topics"+"/"+ch.lower())
        c=r.content
        soup=BeautifulSoup(c,"html.parser")

        quotes=soup.find_all("a",{"title":"view quote"})
        authors=soup.find_all("a",{"title":"view author"})
        quotelist=[]
        authorlist=[]

        

        for author in authors:
            authorlist.append(author.text)
        for quote in quotes:
            if re.match(r"\w",str(quote.text)):
                quotelist.append(quote.text[:150]+"\n"+quote.text[150:])

        optlist=[[] for x in range(len(authorlist))]
        
        for i in range(len(authorlist)):
            while len(optlist[i]) < 3:
                ran=random.randint(0,len(authorlist)-1)    
                if authorlist[ran] not in optlist[i] and authorlist[ran]!=authorlist[i]:
                        optlist[i].append(authorlist[ran])
            optlist[i].append(authorlist[i])
            optlist[i].sort()
        
        question=createlabel("",0,350,1920,510)
        question.setAlignment(QtCore.Qt.AlignCenter) 
        opta=createbutton("Option A","A",700,720)
        optb=createbutton("Option B","B",1100,720)
        optc=createbutton("Option C","C",700,800)
        optd=createbutton("Option D","D",1100,800)
        
        # function to view quiz answers
        def view():
            ansstr=""
            for i in range(len(authorlist)):
                ansstr+=str(i+1)+". "+quotelist[i][:60]+"... -   "+authorlist[i]+"\n"
            question.setAlignment(QtCore.Qt.AlignLeft)
            question.setGeometry(0,190,1920,820)
            updatelabel(question,ansstr)

        # function to play quiz
        def quizplay(h,score):
            # functions executed when an option button is clicked
            def A():
                opta.clicked.disconnect(A)
                optb.clicked.disconnect(B)
                optc.clicked.disconnect(C)
                optd.clicked.disconnect(D)
                if optlist[h][0]==authorlist[h]:
                    quizplay(h+1,score+1)
                else:
                    quizplay(h+1,score)
            def B():
                opta.clicked.disconnect(A)
                optb.clicked.disconnect(B)
                optc.clicked.disconnect(C)
                optd.clicked.disconnect(D)
                if optlist[h][1]==authorlist[h]:
                    quizplay(h+1,score+1)
                else:
                    quizplay(h+1,score)
            def C():                
                opta.clicked.disconnect(A)
                optb.clicked.disconnect(B)
                optc.clicked.disconnect(C)
                optd.clicked.disconnect(D)
                if optlist[h][2]==authorlist[h]:
                    quizplay(h+1,score+1)
                else:
                    quizplay(h+1,score)                
            def D():
                opta.clicked.disconnect(A)
                optb.clicked.disconnect(B)
                optc.clicked.disconnect(C)
                optd.clicked.disconnect(D)
                if optlist[h][3]==authorlist[h]:
                    quizplay(h+1,score+1)
                else:
                    quizplay(h+1,score)       
            if h<len(authorlist): 
                print(h,score)
                updatelabel(question,str(h+1)+". "+quotelist[h]+"\nA. "+optlist[h][0]+"\tB. "+optlist[h][1]+"\nC. "+optlist[h][2]+"\tD. "+optlist[h][3])
                opta.clicked.connect(A)
                optb.clicked.connect(B)
                optc.clicked.connect(C)
                optd.clicked.connect(D)
            elif h==len(authorlist):
                updatelabel(question,"You have scored "+str(score)+" out of "+str(len(authorlist)))
                opta.deleteLater()
                optb.deleteLater()
                optc.deleteLater()
                optd.deleteLater()
                home=createbutton("Return to Home Page","Click to return to home page",1600,880)
                viewans=createbutton("View Answers","Click to view the answers of the quiz",1300,880)
                viewans.resize(200,32)
                viewans.clicked.connect(view)
                viewans.clicked.connect(viewans.deleteLater)
                home.resize(200,32)
                home.clicked.connect(question.deleteLater)
                home.clicked.connect(viewans.deleteLater)
                home.clicked.connect(title.deleteLater)
                home.clicked.connect(main)
                home.clicked.connect(home.deleteLater)
        quizplay(0,0)
    go.clicked.connect(topicchoice)
   
    
# function that shows home page with different quiz collections available
def main():
    a=createbutton("General Quiz - I ","Play over 50 quizzes (MCQ type)",600,500)
    a.resize(120,32)
    b=createbutton("Who said this?","Find out whose quote it is",1200,500)
    b.resize(120,32)
    c=createbutton("General Quiz - II","Play over 50 quizzes (MCQ type)",900,500)
    c.resize(120,32)
    d=createbutton("General Quiz - III","Play over 50 quizzes (MCQ type)",600,600)
    d.resize(120,32)
    e=createbutton("General Quiz - IV","Play over 50 quizzes (MCQ type)",900,600)
    e.resize(120,32)
    f=createbutton("General Quiz - V","Play over 50 quizzes (MCQ type)",1200,600)
    f.resize(120,32)
    exitbutton=createbutton("Exit","Click me to exit from the program",900,700)
    exitbutton.resize(120,32)
    a.clicked.connect(partial(general,1))
    a.clicked.connect(a.deleteLater)
    a.clicked.connect(b.deleteLater)
    a.clicked.connect(c.deleteLater)
    a.clicked.connect(d.deleteLater)
    a.clicked.connect(e.deleteLater)
    a.clicked.connect(f.deleteLater)
    a.clicked.connect(exitbutton.deleteLater)
    b.clicked.connect(quotesfunc)
    b.clicked.connect(a.deleteLater)
    b.clicked.connect(b.deleteLater)
    b.clicked.connect(c.deleteLater)
    b.clicked.connect(d.deleteLater)
    b.clicked.connect(e.deleteLater)
    b.clicked.connect(f.deleteLater)
    b.clicked.connect(exitbutton.deleteLater)    
    c.clicked.connect(partial(general,4))
    c.clicked.connect(a.deleteLater)
    c.clicked.connect(b.deleteLater)
    c.clicked.connect(c.deleteLater)
    c.clicked.connect(d.deleteLater)
    c.clicked.connect(e.deleteLater)
    c.clicked.connect(f.deleteLater)
    c.clicked.connect(exitbutton.deleteLater)
    d.clicked.connect(partial(general,7))
    d.clicked.connect(a.deleteLater)
    d.clicked.connect(b.deleteLater)
    d.clicked.connect(c.deleteLater)
    d.clicked.connect(d.deleteLater)
    d.clicked.connect(e.deleteLater)
    d.clicked.connect(f.deleteLater)
    d.clicked.connect(exitbutton.deleteLater)
    e.clicked.connect(partial(general,10))
    e.clicked.connect(a.deleteLater)
    e.clicked.connect(b.deleteLater)
    e.clicked.connect(c.deleteLater)
    e.clicked.connect(d.deleteLater)
    e.clicked.connect(e.deleteLater)
    e.clicked.connect(f.deleteLater)
    e.clicked.connect(exitbutton.deleteLater)
    f.clicked.connect(partial(general,13))
    f.clicked.connect(a.deleteLater)
    f.clicked.connect(b.deleteLater)
    f.clicked.connect(c.deleteLater)
    f.clicked.connect(d.deleteLater)
    f.clicked.connect(e.deleteLater)
    f.clicked.connect(f.deleteLater)
    f.clicked.connect(exitbutton.deleteLater)
    exitbutton.clicked.connect(window.close)
    a.clicked.disconnect(partial(general,4))
    c.clicked.disconnect(partial(general,4))
    b.clicked.disconnect(quotesfunc)
    d.clicked.disconnect(partial(general,7))
    e.clicked.disconnect(partial(general,10))
    f.clicked.disconnect(partial(general,13))

# creating a QApplication using input from command line
apple=QApplication(sys.argv)

# creating a QMainWindow
window=Window()

# initial screen
l=createlabel("Play over 250 general quizzes and 120 quote-based quizzes\n\nwith PyQuiz, a quiz app developed with Python\n\nthat uses web-scraping to generate quizzes",0,350,1920,300)
l.setAlignment(QtCore.Qt.AlignCenter)
message=createlabel("If the program does not respond due to internet issues, please close and run again",0,850,1920,40)
message.setAlignment(QtCore.Qt.AlignCenter)
message.setStyleSheet("background-color: rgb(219,22,47); color:rgb(255,255,255); font:bold 10pt 'Helvetica'")
developer=createlabel("Developed by Chris Francis",0,600,1920,40)
developer.setAlignment(QtCore.Qt.AlignCenter)
developer.setStyleSheet("background-color: rgb(219,22,47); color:rgb(255,255,255); font:bold 13pt 'Helvetica'")
button=createbutton("Start","Get Started",900,700)
button.clicked.connect(button.deleteLater)
button.clicked.connect(l.deleteLater)
button.clicked.connect(message.deleteLater)
button.clicked.connect(main)
button.clicked.connect(developer.deleteLater)

# executing the QApplication
sys.exit(apple.exec())
