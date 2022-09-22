# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import json
from tkinter import *
from PIL import ImageTk, Image

suggestionList = set()


def textAnalyzer(textNode):
    deduction = 0
    infractions_added = 0
    if "textCase" in textNode and textNode["textCase"] != 'UPPER':
        deduction = deduction + 1
        suggestion = "Might want to make text uppercase"
        infractions_added = infractions_added + 1
        suggestionList.add(suggestion)
    if textNode["fontSize"] < 10:
        deduction = deduction + 1
        infractions_added = infractions_added + 1
        suggestion = "Font size too small"
        suggestionList.add(suggestion)
    if textNode["textAlignHorizontal"] != 'CENTER':
        deduction = deduction + 1
        infractions_added = infractions_added + 1
        suggestion = "Text alignment not proper"
        suggestionList.add(suggestion)
    if textNode["letterSpacing"] < -0.2:
        deduction = deduction + 1
        infractions_added = infractions_added + 1
        suggestion = "Letter spacing too low"
        suggestionList.add(suggestion)
    return deduction, infractions_added


def callFigma():
    infractions = 0
    marks = 100
    textFieldEntry = txtfld.get()
    figmaUrl = "UQZm4M8tjARHlLjoRM0eZM"

    if textFieldEntry !="" and (len(textFieldEntry) > 28):
        figmaUrl = textFieldEntry[27:49]
    else:
        txtfld.insert(END, "https://www.figma.com/file/UQZm4M8tjARHlLjoRM0eZM" )

    # Use a breakpoint in the code line below to debug your script.
    # api_url_node = 'https://api.figma.com/v1/files/UQZm4M8tjARHlLjoRM0eZM/nodes?ids=0:0'
    api_url_file = 'https://api.figma.com/v1/files/' + figmaUrl
    response_file = requests.get(api_url_file,
                                 headers={'X-Figma-Token': 'figd_ovii34p8XXnD-ypGWygDWk2NPJLRlVAxGmXS0ERS'})
    # response_node = requests.get(api_url_node, headers={'X-Figma-Token': 'figd_ovii34p8XXnD-ypGWygDWk2NPJLRlVAxGmXS0ERS'})

    curr = response_file.json()["document"]["children"][0]["children"]
    for childNodes in curr:
        if childNodes["type"] == "FRAME":
            for propertyNodes in childNodes["children"]:
                if propertyNodes["type"] == "TEXT":
                    deduction, infractions_added = textAnalyzer(propertyNodes['style'])
                    marks, infractions = marks - deduction, infractions + infractions_added
    if marks < 0:
        marks = 0
    resultMarks.delete(0, END)
    resultMarks.insert(0, str(marks))
    resultInfractions.delete(0, END)
    resultInfractions.insert(0, str(infractions))
    resultSuggestion.insert(END, ', '.join(suggestionList))

    f = open("hack.txt", "a")
    f.write(json.dumps(response_file.json(), indent=4))
    # f.write("\n ----------------------Node--------------------------\n")
    # f.write(json.dumps(response_node.json(), indent=4))
    f.close()


top = Tk()
top.title("Yoda: the usability analyzer")
top.geometry("600x600")
lbl = Label(top, text="Application make usable you will", fg='red', font=("Helvetica", 16))
lbl.place(x=150, y=50)
lbl2 = Label(top, text="Enter figma url", fg='blue', font=("Helvetica", 8))
lbl2.place(x=150, y=295)
txtfld = Entry(top, text="Enter the figma url", fg='red', bd=5, width=25)
txtfld.place(x=230, y=290)
figmaUrl = txtfld.get()
analyze_button = Button(top, text="Analyze", command=callFigma)
analyze_button.place(x=280, y=500)
frame = Frame(top, width=15, height=10)
frame.pack()
frame.place(anchor='center', relx=0.49, rely=0.3)
# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("yoda.png").resize((125, 144)))
# Create a Label Widget to display the text or Image
lbl3 = Label(frame, image=img)
lbl3.pack()
lbl4 = Label(top, text="Marks", fg='blue', font=("Helvetica", 8))
lbl4.place(x=150, y=315)
lbl4 = Label(top, text="Infractions", fg='blue', font=("Helvetica", 8))
lbl4.place(x=150, y=335)
lbl5 = Label(top, text="Suggestions", fg='blue', font=("Helvetica", 8))
lbl5.place(x=150, y=375)
resultMarks = Entry(top, text="Results", fg='blue', bd=5, width=25)
resultMarks.place(x=230, y=310)
resultInfractions = Entry(top, text="Infractions", fg='blue', bd=5, width=25)
resultInfractions.place(x=230, y=330)
resultSuggestion = Text(top, fg='blue', bd=5, width=25, height=4)
resultSuggestion.place(x=230, y=370)
resultSuggestion.place(x=230, y=370)
top.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
