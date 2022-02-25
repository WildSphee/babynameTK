import tkinter as tk
import databaseCSV as dbCSV

root = tk.Tk()
root.title("Name Searcher")
root.geometry("250x380")

frame1 = tk.Frame(root, width=200, height=50)
frame1.grid(row=0, columnspan=2, pady=10, padx=20)
framedata = tk.Frame(root, width=100, height=100, bg="grey82")
framedata.grid(row=2, column=0, pady=10)
framedata2 = tk.Frame(root, width=100, height=100, bg="grey82")
framedata2.grid(row=2, column=1, pady=10)
labelinfo = tk.Label(root, text="")
labelinfo.grid(row=3, columnspan=2)
buttonSearch = tk.Button(root, text="Search")
buttonSearch.grid(row=4, columnspan=2)

f1label = tk.Label(frame1, text="Year Range:", font="Helvetica 10 bold")
f1label.grid(row=0, column=0, columnspan=2, sticky="w", ipady=1)
f1labelfrom = tk.Label(frame1, text="From:", font="Helvetica 8")
f1labelfrom.grid(row=1, column=0)
f1entry = tk.Entry(frame1, width=8)
f1entry.insert(0, string="1950")
f1entry.grid(row=1, column=1)
f1labelto = tk.Label(frame1, text="To:", font="Helvetica 8")
f1labelto.grid(row=1, column=2)
f1entry2 = tk.Entry(frame1, width=8)
f1entry2.insert(0, string="2009")
f1entry2.grid(row=1, column=3)

f2label = tk.Label(frame1, text="Name or Rank:", font="Helvetica 10 bold")
f2label.grid(row=2, column=0, columnspan=2, sticky="w", ipady=1)
f2option = ["RANK", "NAME"]
v = tk.StringVar()
v.set(f2option[1])
f2menu = tk.OptionMenu(frame1, v, *f2option)
f2menu.config(font="Helvetica 8")
f2menu.grid(row=3, column=0, padx=10, columnspan=2)
f2entry = tk.Entry(frame1, width=16)
f2entry.grid(row=3, column=2, columnspan=2)

oldsearch = (1950, 2009)

def search(event=None):

    #check whether range is valid
    try:
        f1 = int(f1entry.get())
        f2 = int(f1entry2.get())
    except:
        labelinfo["text"] = "Please enter current range"
        return
    a = True if f1 > 2009 or f1 < 1950 or f1 is None else False
    b = True if f2 > 2009 or f2 < 1950 or f2 is None or f1 > f2 else False
    if a or b:
        labelinfo["text"] = "Please enter correct range of date"
        if a:
            f1entry.delete(0, "end")
            f1entry.insert(0, "1950")
        if b:
            f1entry2.delete(0, "end")
            f1entry2.insert(0, "2009")
        return

    # check whether input name / id is valid
    if f2entry.get() == "":
        labelinfo["text"] = "Please enter valid name/rank"
        return
    if v.get() == "RANK" and not f2entry.get().isdigit():
        labelinfo["text"] = "Please enter valid rank in numbers"
        return

    # check for the need to recreate db
    global oldsearch
    newsearch = (f1, f2)
    print(oldsearch, newsearch)
    if newsearch != oldsearch:
        print("recounting csv..")
        oldsearch = newsearch
        dbCSV.recountCSV(restrain=newsearch)
    else:
        print("no need to recount csv..")
    labelinfo["text"] = "Fetching..."

    # officially fetch data from sql db
    data = None
    if v.get() == "RANK":
        data = dbCSV.fetchid(id=f2entry.get())
    elif v.get() == "NAME":
        data = dbCSV.fetchid(name=f2entry.get().lower().capitalize())

    # place data onto the frame
    def placeinFrame(frame, data):
        for e in frame.winfo_children():
            e.grid_forget()

        if data == []:
            label1 = tk.Label(frame, text="No Data", font="Helvetica 10 bold", bg="grey82").grid(padx=10, pady=10)
            return

        label1 = tk.Label(frame, text="Name", font="Helvetica 9 bold", bg="grey82").grid(row=0, column=0, sticky='w')
        # label2 = tk.Label(frame, text="Score", font="Helvetica 8 bold").grid(row=0, column=1)
        label3 = tk.Label(frame, text="Rank", font="Helvetica 9 bold", bg="grey82").grid(row=0, column=2, sticky='w')
        for r, re in enumerate(data):
            for c, ce in enumerate(re):
                if c == 1:
                    continue
                nlabel = tk.Label(frame, text=ce, bg="grey82")
                nlabel.grid(row=r+1, column=c, sticky="w")

    placeinFrame(framedata, data[0])
    placeinFrame(framedata2, data[1])

    labelinfo["text"] = "Done"

def main():
    dbCSV.recountCSV(oldsearch)

    buttonSearch.config(command=search)
    root.bind("<Return>", search)

    root.mainloop()


if __name__ == '__main__':
    main()