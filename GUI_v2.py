from tkinter import *
import sqlite3

#Search
def findey():

    text = textentry.get()
    
    conn = sqlite3.connect("forward.db")
    result = []
    heading = []
    # cursor to move around the database
    c = conn.cursor()
    for i in text:
        head = c.execute("SELECT heading FROM forward WHERE heading = ?", (i,))
        head = c.fetchall()
        heading.append(head)
        res = c.execute("SELECT doc_id FROM words WHERE word = ?", (i,))
        res = c.fetchall()
        result.append(res)

    x = 0
    for j in result:
        if i in heading:
            result[j], result[x] = result[x], result[j]
            x += 1

    to_printlist = []
    for i in result:
        print(i)
        for j in i:
            print(j)
            c.execute("SELECT address, heading FROM forward where doc_id LIKE ?",(j[0],))
            to_print = c.fetchall()
            to_printlist.append(to_print[0])

    print(to_printlist)


    return


##def rank(result, heading):
##    x = 0
##    print(result)
##    print(heading)
##    for i in result:
##        if i in heading:
##            result[i], result[x] = result[x], result[i]
##            x += 1
##
##
##    return


#de, gh = findey('fairchild', 'orphan')
#rank(de, gh)


###click function
##def click():
##    entered_text=textentry.get() #will get text from entry box
##    output.delete(0.0, END)
##    try:
##        definition = dict[entered_text]
##    except:
##        definition = "Sorry, search result does not exist"
##    output.insert(END, definition)


    
window = Tk()
window.title("Psypher")

Label(window, bg='black').grid(row=0, column=0, sticky=W)

#text entry box
textentry = Entry(window, width = 110, bg = "white")
textentry.grid(row=2, column=0, sticky  = E)

#Search button
Button(window, text='Search',width = 15, command=findey).grid(row=3, column=0,sticky=N)

#Output
output = Text(window, width = 100,height = 50,wrap = WORD,background="white")
output.grid(row=5,column= 0, columnspan=2, sticky=W)


window.mainloop()
