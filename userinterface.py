import scraper
from tkinter import*
from tkinter import ttk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import os
import pickle


SAVELOGIN = "login.p"

DISTRICTOPTIONS = scraper.scrapeOptions()


BACKGROUND = '#fafafa'

tk = Tk()
tk.iconbitmap("logo.ico")
tk.state('zoomed')
tk.configure(background=BACKGROUND)

font = tkFont.Font(family="calibri", size=14)
smallfont = tkFont.Font(family="calibri", size=9)
mediumfont = tkFont.Font(family="calibri", size=12)

ENTRYSTYLE = dict(font=font)

LABELSTYLE = dict(font=font, background=BACKGROUND)

LISTBOXSTYLE = dict(font=smallfont, borderwidth=0, highlightthickness=0, background=BACKGROUND)

BUTTONSTYLE = dict(font=mediumfont,background="lightgrey")

CREDITSTYLE = dict(font=smallfont, width=50, height=2, background=BACKGROUND)

LOADINGSTYLE = dict(font=font, background=BACKGROUND, width=50,height=5)


class Widget(Frame):
    def __init__(self):
        super().__init__()

        self.master.title("HomeAccess")
        self.configure(background=BACKGROUND)

        self.pack()

        self.style = ttk.Style(self)
        self.style.theme_use("default")
        self.style.configure('.', font=font)
        self.style.configure('Treeview', rowheight=30)
        self.style.configure("Treeview.Heading", font=mediumfont)

        self.initData()

        if os.path.exists(SAVELOGIN):
            with open(SAVELOGIN,"rb") as f:
                self.username, self.password, self.district = pickle.load(f)
                self.get_home_data()
                self.open_home()
        else:
            self.loginUI()

    def initData(self):
        self.username = None
        self.password = None
        self.homeData = None
        self.scheduleData = None

    def buildHeader(self):
        image = Image.open("logo.ico")
        photo = ImageTk.PhotoImage(image)
        logo = Label(self, image=photo, **LABELSTYLE)
        logo.image = photo
        return logo

    def buildFooter(self):
        credits = Label(self, text="created by puffyboa, contributors: lavarack", **CREDITSTYLE)
        return credits

    def destroyWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def update_district_search(self):
        self.districtListbox.delete(0,END)
        entry = self.districtSearchEntry.get()
        for item in DISTRICTOPTIONS:
            if entry.lower() in item.lower():
                self.districtListbox.insert(END,item)

    def set_district_entry(self, event):
        listbox = event.widget
        selection = listbox.get(listbox.curselection())
        self.districtSearchEntry.delete(0,END)
        self.districtSearchEntry.insert(0,selection)

    def loginUI(self):
        self.master.title("Login")

        self.buildHeader().grid(row=0,columnspan=2)

        self.districtListbox = Listbox(self,selectmode=SINGLE, height=4, **LISTBOXSTYLE)
        self.districtListbox.bind("<Double-Button-1>", self.set_district_entry)

        self.districtSearch = StringVar()
        self.districtSearch.trace("w", lambda name, index, mode: self.update_district_search())

        self.districtSearchEntry = Entry(self, textvariable=self.districtSearch, **ENTRYSTYLE)

        self.update_district_search()

        self.usernameEntry = Entry(self, **ENTRYSTYLE)
        self.passwordEntry = Entry(self, show="*", **ENTRYSTYLE)

        self.login = Button(self, text="Login", command=self.login_callback, **BUTTONSTYLE)

        Label(self, text="District", **LABELSTYLE).grid(row=1, sticky=W, padx=5, pady=5)
        Label(self, text="Username", **LABELSTYLE).grid(row=3, sticky=W, padx=5, pady=5)
        Label(self, text="Password", **LABELSTYLE).grid(row=4, sticky=W, padx=5, pady=5)

        self.districtSearchEntry.grid(row=1, column=1, padx=5, pady=5)
        self.districtListbox.grid(row=2, sticky='we', column=1, pady=5)
        self.usernameEntry.grid(row=3, column=1, padx=5, pady=10)
        self.passwordEntry.grid(row=4, column=1, padx=5, pady=10)

        self.login.grid(row=5,columnspan=2, padx=5,pady=10)

        self.buildFooter().grid(row=6,columnspan=2, padx=5,pady=5)

    def scheduleUI(self, data):
        self.master.title("Schedule")

        self.buildHeader().pack(pady=10)

        self.goHome = Button(self, text="Home", command=self.home_callback, **BUTTONSTYLE)
        self.goHome.pack()

        self.tableUI(data)

        self.signout = Button(self, text="Sign out", command=self.signout_callback, **BUTTONSTYLE)
        self.signout.pack()

        self.buildFooter().pack()

    def homeUI(self, data):
        self.master.title("Home")

        self.buildHeader().pack(pady=10)

        self.goSchedule = Button(self, text="Schedule", command=self.schedule_callback, **BUTTONSTYLE)
        self.goSchedule.pack()

        self.tableUI(data)

        self.signout = Button(self, text="Sign out", command=self.signout_callback, **BUTTONSTYLE)
        self.signout.pack()

        self.buildFooter().pack()

    def tableUI(self,data):
        container = Frame(self, pady=10, background=BACKGROUND)
        container.pack(fill='both', expand=True)

        tree = ttk.Treeview(self, columns=data[0], show="headings", height=len(data), padding=5, selectmode="none")

        hsb = ttk.Scrollbar(orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)

        tree.grid(column=0, row=0, sticky='nsew', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        tree.pack()
        for r,row in enumerate(data):
            if row == data[0]:
                for col in row:
                    tree.heading(col, text=col.title(),
                                      command=lambda c=col: self.sortby(tree, c, 0))
                    tree.column(col, width=tkFont.Font().measure(col.title()))
            else:
                tree.insert('', 'end', values=row)
                for ix, val in enumerate(row):
                    col_w = tkFont.Font().measure(val)
                    if tree.column(data[0][ix], width=None) < col_w:
                        tree.column(data[0][ix], width=col_w)

    def sortby(self,tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))

    def loading_popup(self):
        popup = Label(self.master, text="Loading...", **LOADINGSTYLE)
        popup.pack(side=TOP,fill=BOTH)
        return popup

    def get_home_data(self):
        if self.homeData is None:
            popup = self.loading_popup()
            self.master.update()
            self.homeData = scraper.scrapeHome(self.username, self.password, self.district)
            popup.destroy()

    def get_schedule_data(self):
        if self.scheduleData is None:
            popup = self.loading_popup()
            self.master.update()
            self.scheduleData = scraper.scrapeSchedule(self.username, self.password, self.district)
            popup.destroy()

    def login_callback(self):
        self.username, self.password, self.district = self.usernameEntry.get(), self.passwordEntry.get(), DISTRICTOPTIONS[self.districtSearchEntry.get()]
        self.get_home_data()
        if self.homeData is not None:
            if not os.path.exists(SAVELOGIN):
                with open(SAVELOGIN, "wb") as f:
                    pickle.dump([self.username, self.password, self.district], f)
            self.open_home()
        else:
            self.login.config(text="incorrect login, retry")

    def home_callback(self):
        self.get_home_data()
        if self.homeData is not None:
            self.open_home()

    def open_home(self):
        self.destroyWidgets()
        self.homeUI(self.homeData)

    def schedule_callback(self):
        self.get_schedule_data()
        if self.scheduleData is not None:
            if not os.path.exists(SAVELOGIN):
                with open(SAVELOGIN, "wb") as f:
                    pickle.dump([self.usernameEntry.get(), self.passwordEntry.get()], f)
            self.open_schedule()

    def open_schedule(self):
        self.destroyWidgets()
        self.scheduleUI(self.scheduleData)

    def signout_callback(self):
        self.destroyWidgets()
        self.initData()
        self.loginUI()
        if os.path.exists(SAVELOGIN):
            os.remove(SAVELOGIN)


app = Widget()

tk.mainloop()
