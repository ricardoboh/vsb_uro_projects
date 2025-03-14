# -*- coding: utf-8 -*-
from tkinter import *
import json
from math import sqrt
#from PIL import Image, ImageTk
from tkinter import messagebox as msg
import tkinter.font
from tkinter import filedialog
from tkinter import ttk
import random
from datetime import datetime

def loadOrders():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            orders = json.load(file)

            # Ensure it returns a list of dictionaries
            if not isinstance(orders, list):
                raise ValueError("Error: JSON data is not a list.")

            return orders
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON: {e}")
        return []
    
light_red    = "#f79797"
light_green  = "#9af797"
light_yellow = "#f4f797"
light_blue   = "#97c2f7"
light_purple = "#c597f7"

dark_red     = "#f73a34"
dark_green   = "#0d8701"
dark_yellow  = "#d1a711"
dark_blue    = "#2958cf"
dark_purple  = "#a922d6"

dark_text_color  = "#06010a"
light_text_color = "#eee9f2"

order_id_unique = 0

names = [
    "Josef ", "Honza ", "Jiří ", "Tomáš ", "Petr ",
    "Martin ", "Janek ", "Lukáš ", "Michal ", "Jakub ",
    "David ", "Pavel ", "Jindřich ", "Adam ", "Marek ",
    "Václav ", "Filip ", "Ondřej ", "Dominik ", "Daniel ",
    "František ", "Miroslav ", "Richard ", "Zdeněk ", "Karel ",
    "Radek ", "Jaroslav ", "Aleš ", "Vojtěch ", "Robert ",
    "Patrik ", "Libor ", "Radim ", "Stanislav ", "Milan ",
    "René ", "Matěj ", "Radovan ", "Vladimír ", "Eldar ",
    "Šimon ", "Tadeáš ", "Bohumil ", "Bohuslav ", "Bořek ",
    "Bořivoj ", "Božek ", "Břetislav ", "Čeněk ", "Čestmír ",
    "Dalibor ", "Dobroslav ", "Dušan ", "Emil ", "Gabriel ",
    "Gustav ", "Hynek ", "Chval ", "Ignác ", "Ivo ",
    "Jáchym ", "Patrick ", "Janko ", "Gigli ", "Jeroným ",
    "Jonáš ", "Kamil ", "Kryštof ", "Lev ", "Matouš ",
    "Mikoláš ", "Nikolas ", "Oldřich ", "Olej ", "Oskar ",
    "Osmar ", "Otokar ", "Oto ", "Radan ", "Roman ",
    "Rostislav ", "Samuel ", "Silvestr ", "Soběslav ", "Abdullahi ",
    "Svatopluk ", "Štefan ", "Štěpán ", "Tomášek ", "Vasil ",
    "Viktor ", "Vilém ", "Vlastimil ", "Vladan ", "Zbyšek ",
    "Hans ", "Gandalf ", "Hugoslav ", "Batman ", "Superman "
]

surnames = [
    "Letáček", "Blažek", "Frydrych", "Kpozo", "Ndefe",
    "Rusnák", "Buchta", "Veselý", "Klíma", "Tanko",
    "Pospíšil", "Marek", "Hájek", "Rigo", "Jelínek",
    "Malý", "Urban", "Richter", "Sýkora", "Kříž",
    "Adamec", "Vaněk", "Kratochvíl", "Zeman", "Šimek",
    "Beneš", "Holub", "Fišer", "Bartoš", "Vlček",
    "Schmidt", "Nováček", "Kovář", "Bílý", "Pokorný",
    "Dušek", "Pech", "Čech", "Růžička", "Havlíček",
    "Horvát", "Matějka", "Čermák", "Štěpánek", "Šín",
    "Hruška", "Kolář", "Havlík", "Krejčí", "Liška",
    "Čížek", "Janda", "Konečný", "Sedláček", "Voříšek",
    "Němeček", "Blažek", "Prokop", "Ewerton", "Hrubý",
    "Macháček", "Zima", "Šváb", "Šebek", "Janoušek",
    "Holý", "Mareš", "Bárta", "Kadlec", "Mach", 
    "Klaus", "Petráš", "Bílek", "Bohunovský", "Křeček",
    "Sobotka", "Horáček", "Kubát", "Stehlík", "Kočí",
    "Mikeš", "Kubíček", "Doubravský", "Stehlíček", "Tichý",
    "Bezduch", "Moravec", "Lorenc", "Slepýš", "Pěvec",
    "Vojtek", "Apl", "Kutnahora", "Nejezrohlik", "Lidl",
    "Souček", "Turbo", "Bimho", "Žufánek", "Podlaha"
]

product_list = [
    ("Hamburger", "129 Kč"),
    ("Pizza Martha", "110 Kč"),
    ("Pizza Bolzano", "129 Kč"),
    ("Pizza Saluto", "150 Kč"),
    ("Pizza Hawaii", "149 Kč"),
    ("Pizza Curiosa", "149 Kč"),
    ("Pizza Havana", "129 Kč"),
    ("Hamburger XXL", "210 Kč"),
    ("Pasta Carbonara", "99 Kč"),
    ("Pasta Tomato", "89 Kč"),
    ("Pasta Cheese", "119 Kč"),
    ("Fries", "55 Kč"),
    ("Fries XXL", "75 Kč"),
    ("Baguette", "29 Kč"),
    ("Rozmarine soup", "45 Kč"),
    ("Wine", "150 Kč"),
    ("Coca-cola", "49 Kč"),
    ("Cola XXL", "79 Kč"),
    ("Kofola", "45 Kč"),
    ("Tofu sticks", "70 Kč"),
    ("Chilli Pizza", "189 Kč"),
    ("Nachos", "79 Kč"),
    ("Salted pop-corn", "100 Kč"),
    ("Meatballs", "85 Kč"),
    ("Beer", "35 Kč")
]

villages = [
    "Troubelice", "Lazce", "Dědinka", "Pískov", "Nová Hradečná", "Libina", "Červenka",
    "Lipinka", "Klopina", "Medlov", "Benkov", "Pňovice", "Střelice", "Mladeč", "Nové Zámky",
    "Nový Dvůr", "Králová", "Hradečná", "Hradec", "Plinkout", "Plíškův Mlýn", "Dlouhá Loučka",
    "Horní Sukolom", "Dolní Sukolom", "Nová Dědina", "Benkov", "Medlov", "Dědinka", "Holubice",
    "Úsov", "Veleboř", "Sídliště", "Lipinka", "Březové", "Lhota nad Moravou", "Tři Dvory",
    "U Studánky", "Nové Mlýny", "Zadní Újezd", "Hlivice"
]


class OrderApp:


    def __init__(self, root):

        #Window title
        root.title('Pizza app')

        #Window sizes
        root.resizable(False, False)
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.geometry(f"{self.screen_width-70}x{self.screen_height}+70+0")

        #Variables
        self.varTakeAwaySum = IntVar(value = 1000)
        self.varDeferment = IntVar(value = 0)
        self.varDictDeliveries = {1: IntVar(value = 0), 2: IntVar(value = 0),
                                  3: IntVar(value = 0), 4: IntVar(value = 0),
                                  5: IntVar(value = 0), 6: IntVar(value = 0)
                                  }
        self.varCash = IntVar(value = 0)


        #Fonts
        self.def_font = tkinter.font.nametofont("TkDefaultFont")
        self.def_font.config(size=16)

        #Graphics functions
        self.CreateMainPageLayout(root)
        self.CreateNotebook()
        self.CreateShiftEndPage()
        self.CreateHistoryOrdersPage()
        self.CreateActiveOrdersPage()


        #Key bindings
        root.bind("<Escape>", lambda event: root.destroy())
        self.frameShiftEnd.bind("<FocusIn>", lambda event: root.bind("<Return>", lambda event: self.CountEndShift()))
        self.frameShiftEnd.bind("<FocusOut>", lambda event: root.unbind("<Return>"))

    def CreateMainPageLayout(self, root):
        #---Partitions of main page
        self.headerFrame = Frame(root)
        self.headerFrame.pack(side="top", fill="x")
        self.headerFrame.configure(background=dark_yellow, height=self.screen_height//25)
        self.mainFrame = Frame(root)
        self.mainFrame.pack(side="bottom", fill="both", expand=1)
        self.CreateHeaderLayout()

    def CreateHeaderLayout(self):
        #----Header what will be the same for all pages

        self.headerFrame.grid_columnconfigure(0, weight=1)
        self.headerFrame.grid_columnconfigure(1, weight=1)
        self.headerFrame.grid_columnconfigure(2, weight=1)

        self.btnCreateOrder = Button(self.headerFrame, text="MAKE ORDER",
                                     command=lambda:self.generateRandomOrder())
        self.btnCreateOrder.grid(row=0, column=1, sticky="nswe")
        self.btnCreateOrder.configure(background=light_blue, width=self.screen_width//25)

        self.lblBranchName = Label(self.headerFrame, text="Bistro Olomouc")
        self.lblBranchName.grid(row=0, column=0, sticky="w", padx=(25,0))
        self.lblBranchName.configure(foreground="white", background=dark_yellow)

        self.btnLogout = Button(self.headerFrame, text="Odhlasit se")
        self.btnLogout.grid(row=0, column=3, sticky="e", padx=(0, 10))
        self.btnLogout.configure(foreground="white", background=dark_yellow)

    def generateRandomOrder(self):
        name = random.choice(names) + random.choice(surnames)
        village = random.choice(villages)
        address = f"{village} {random.randint(1, 500)}, {village}"
        phone = f"7{random.randint(700000000, 800000000)}"

        num_products = random.randint(1, 8)
        selected_products = random.sample(product_list, num_products)

        products = [{"name": p[0], "price": f"{p[1]}"} for p in selected_products]

        total_price = sum(int(p[1].split()[0]) for p in selected_products)
        total_price_str = f"{total_price} Kč"

        status = random.choice(["Neověřeno", "Ověřeno"])
        delivery = "Neznámý"

        global order_id_unique
        order_id_unique += 1

        new_order = {
            "id": order_id_unique,
            "datetime": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            "status": status,
            "total_price": total_price_str,
            "delivery": delivery,
            "customer": {
                "name": name,
                "address": address,
                "phone": phone
            },
            "products": products
        }

        try:
            with open("orders.json", "r", encoding="utf-8") as file:
                orders = json.load(file)
                if not isinstance(orders, list):
                    orders = []
        except (FileNotFoundError, json.JSONDecodeError):
            orders = []

        orders.append(new_order)

        with open("orders.json", "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        self.UpdateFramesList()


    def CreateNotebook(self):
        #----Notebook on main page
        self.notebook = ttk.Notebook(self.mainFrame)
        self.notebook.pack(fill="both", expand=1)
        
        self.frameActiveOrders = ttk.Frame(self.notebook)
        self.frameActiveOrders.pack()
        self.frameHistoryOrders = ttk.Frame(self.notebook)
        self.frameHistoryOrders.pack()
        self.frameShiftEnd = ttk.Frame(self.notebook)
        self.frameShiftEnd.pack()

        self.notebook.add(self.frameActiveOrders, text="Active Orders")
        self.notebook.add(self.frameHistoryOrders, text="Orders history")
        self.notebook.add(self.frameShiftEnd, text="End of shift")
    
    def CreateShiftEndInfo(self):
        #Components in End Info Shift End

        
        self.frameGenerated = Frame(self.frameEndInfoShiftEnd)
        self.frameGenerated.grid(column=0, row=0, sticky="nw", padx=0)

        self.lblEnd = Label(self.frameGenerated, text="END OF SHIFT", font="Helvetica 18 bold")
        self.lblEnd.grid(column=0, row=0, columnspan=2, pady=(25,5), sticky="nw")
        

        """
        self.lblGenerated = Label(self.frameGenerated, text="Generated: ---Date and Time when Notebook page button was clicked---")
        self.lblGenerated.grid(column=0, row=1, sticky=W, padx=10, pady=2)
        self.lblGenerated.configure(font="Helvetica 16")
        self.lblDateFrom = Label(self.frameGenerated, text="Date from: ---Date and Time when the first Order was accepted---")
        self.lblDateFrom.grid(column=0, row=2, sticky=W, padx=10, pady=2)
        self.lblDateFrom.configure(font="Helvetica 16")
        self.lblDateTo = Label(self.frameGenerated, text="Date to: ---Date and Time when the last Order was accepted---")
        self.lblDateTo.grid(column=0, row=3, sticky=W, padx=10, pady=2)
        self.lblDateTo.configure(font="Helvetica 16")
        self.lblNumOfOrders = Label(self.frameGenerated, text="Number of Orders: ---The sum of accepted orders---")
        self.lblNumOfOrders.grid(column=0, row=4, sticky=W, padx=10, pady=2)
        self.lblNumOfOrders.configure(font="Helvetica 16")
        """

        # Upgraded the printing of Labels, the value of label has
        # the same alligment as the value before and the title labels 
        # has also the same alligment
        #"""

        self.lblGenerated = Label(self.frameGenerated, text="Generated:", font="Helvetica 16")
        self.lblGenerated.grid(column=0, row=1, sticky="nw", padx=0, pady=2)

        self.lblDateFrom = Label(self.frameGenerated, text="Date from:", font="Helvetica 16")
        self.lblDateFrom.grid(column=0, row=2, sticky="nw", padx=0, pady=2)

        self.lblDateTo = Label(self.frameGenerated, text="Date to:", font="Helvetica 16")
        self.lblDateTo.grid(column=0, row=3, sticky="nw", padx=0, pady=2)

        self.lblNumOfOrders = Label(self.frameGenerated, text="Number of Orders:", font="Helvetica 16")
        self.lblNumOfOrders.grid(column=0, row=4, sticky="nw", padx=0, pady=2)

        # Dynamic Values (Right Column)
        self.valueGenerated = Label(self.frameGenerated, text="---", font="Helvetica 16", fg="blue")
        self.valueGenerated.grid(column=1, row=1, sticky="nw", padx=15, pady=2)

        self.valueDateFrom = Label(self.frameGenerated, text="---", font="Helvetica 16", fg="blue")
        self.valueDateFrom.grid(column=1, row=2, sticky="nw", padx=15, pady=2)

        self.valueDateTo = Label(self.frameGenerated, text="---", font="Helvetica 16", fg="blue")
        self.valueDateTo.grid(column=1, row=3, sticky="nw", padx=15, pady=2)

        self.valueNumOfOrders = Label(self.frameGenerated, text="---", font="Helvetica 16", fg="blue")
        self.valueNumOfOrders.grid(column=1, row=4, sticky="nw", padx=15, pady=2)
        #"""


        
        self.frameDeliveries = Frame(self.frameEndInfoShiftEnd)
        self.frameDeliveries.grid(column=0, row=1, sticky="nw", padx=0, pady=5)
        self.lblAllDeliveriesInfo = Label(self.frameDeliveries, text="Division by deliveries:")
        self.lblAllDeliveriesInfo.configure(font="Helvetica 16 bold")
        self.lblAllDeliveriesInfo.grid(column=0, row=0, columnspan=2, sticky="nw", padx=0, pady=(15, 2))

        """
        This is the list of labels of Delivery guys and the Take away and what is
        their current ammount of money they need to give at the End Of Shift...
        Use cases:
        1.
        When the Order hasn't been assign yet, the Order has status Unknown, 
        so when the first Order is created, the Unknow label is created as well.
        Every next Order created is assigned as Unknown till some Delivery Guy 
        deliver the Order and mark it as Done, then it is assign to this Delivery Guy.
        Or when the Order is picked up as Take Away then it is assigned to the Take Away.
        2.
        When the Order is canceled and no Order has had this status yet, the Label Canceled
        is created.
        3.
        When the Delivery guy is assigned to some Order and he hasn't had
        any order this day yet. The new Label is created with the number of
        delivery guy such as R1,R2...
        4.
        When the Take away is assigned to some Order and no Order has been assigned
        as Take Away the new Label Take Away is created.
        This value which is in this Label will be used in Form when the End Of Shift is
        counted.
        """
        
        for key, value in self.varDictDeliveries.items():
            if value.get() != 0:
                Label(self.frameDeliveries, text=f"R{key} - {value.get()}Kč").grid(column=0, row=key, sticky="w")
                #Label(self.frameDeliveries, text=f"R{key}").grid(column=0, row=key, sticky="w")
                #Label(self.frameDeliveries, text=f"{value.get()}Kč").grid(column=1, row=key, sticky="w")
        if self.varTakeAwaySum.get() != 0:
            Label(self.frameDeliveries ,text=f"Take away - {self.varTakeAwaySum.get()}Kč").grid(column=0, row=8, sticky="w")
            #Label(self.frameDeliveries ,text=f"Take away").grid(column=0, row=8, sticky="w")
            #Label(self.frameDeliveries ,text=f"{self.varTakeAwaySum.get()}Kč").grid(column=1, row=8, sticky="w")
                

        self.frameSumaryOfDeliveries = Frame(self.frameEndInfoShiftEnd)
        self.frameSumaryOfDeliveries.grid(column=0, row=2, sticky="nw", padx=0, pady=25)
        """
        This Label(lblSumDone) has value which is counted only for the finished Orders
        the canceled Orders and the unknown Orders values ARE NOT COUNTED IN HERE! 
        """

        """
        self.lblSumDone = Label(self.frameSumaryOfDeliveries, text="FINISHED SUM: ---Sum of orders which was marked as finished---")
        self.lblSumDone.grid(column=0, row=0, sticky="nw", padx=10, pady=(0, 10))
        self.lblSumDone.configure(font="Helvetica 18 bold")
        
        self.lblSumAll = Label(self.frameSumaryOfDeliveries, text="Total Sum: ---Sum of all Orders which was accepted that day---")
        self.lblSumAll.grid(column=0, row=1, sticky="nw", padx=10, pady=(0, 10))
        self.lblSumAll.configure(font="Helvetica 15 bold")
        """

        #"""
        # Labels (Left Column)
        self.lblSumDone = Label(self.frameSumaryOfDeliveries, text="FINISHED SUM:", font="Helvetica 18 bold")
        self.lblSumDone.grid(column=0, row=0, sticky="nw", padx=0, pady=(0, 10))

        self.lblSumAll = Label(self.frameSumaryOfDeliveries, text="Total Sum:", font="Helvetica 15 bold")
        self.lblSumAll.grid(column=0, row=1, sticky="nw", padx=0, pady=(0, 10))

        # Dynamic Values (Right Column)
        self.valueSumDone = Label(self.frameSumaryOfDeliveries, text="---", font="Helvetica 18 bold", fg="blue")
        self.valueSumDone.grid(column=1, row=0, sticky="nw", padx=20, pady=(0, 10))

        self.valueSumAll = Label(self.frameSumaryOfDeliveries, text="---", font="Helvetica 15 bold", fg="blue")
        self.valueSumAll.grid(column=1, row=1, sticky="nw", padx=20, pady=(0, 10))
        #"""

        #~Form Labels 
    def CreateForm(self):
         
        # Ensure both columns are correctly configured for alignment
        self.frameEndFormShiftEnd.grid_columnconfigure(0, weight=1)  # Labels column
        self.frameEndFormShiftEnd.grid_columnconfigure(1, weight=1)  # Entries column

        # --- Take Away Sum ---
        self.lblSumTakeAway = Label(self.frameEndFormShiftEnd, text="Take Away Sum:", font=("Helvetica", 18))
        self.lblSumTakeAway.grid(column=0, row=0, sticky="w", padx=10, pady=(20, 10))

        self.entrySumTakeAway = Entry(self.frameEndFormShiftEnd, width=20, textvariable=self.varTakeAwaySum, font=("Helvetica", 18))
        self.entrySumTakeAway.grid(column=1, row=0, padx=25, ipady=5, pady=(20, 10), sticky="ew")

        # --- Food Card Sum ---
        self.lblSumFoodCards = Label(self.frameEndFormShiftEnd, text="Food Card Sum:", font=("Helvetica", 18))
        self.lblSumFoodCards.grid(column=0, row=1, sticky="w", padx=10, pady=10)

        self.entrySumFoodCards = Entry(self.frameEndFormShiftEnd, width=20, font=("Helvetica", 18))
        self.entrySumFoodCards.grid(column=1, row=1, padx=25, pady=10, ipady=5, sticky="ew")

        # --- Cards Sum ---
        self.lblSumCards = Label(self.frameEndFormShiftEnd, text="Cards Sum:", font=("Helvetica", 18))
        self.lblSumCards.grid(column=0, row=2, sticky="w", padx=10, pady=10)

        self.entrySumCards = Entry(self.frameEndFormShiftEnd, width=20, font=("Helvetica", 18))
        self.entrySumCards.grid(column=1, row=2, padx=25, pady=10, ipady=5, sticky="ew")

        # --- Extra Spendings ---
        self.lblSumShopping = Label(self.frameEndFormShiftEnd, text="Extra Spendings:", font=("Helvetica", 18))
        self.lblSumShopping.grid(column=0, row=3, sticky="w", padx=10, pady=10)

        self.entrySumShopping = Entry(self.frameEndFormShiftEnd, width=20, font=("Helvetica", 18))
        self.entrySumShopping.grid(column=1, row=3, padx=25, pady=10, ipady=5, sticky="ew")

        # --- Money Deferment (1000Kč) ---
        self.lblExtraMoney = Label(self.frameEndFormShiftEnd, text="Money Deferment (1000Kč):", font=("Helvetica", 18))
        self.lblExtraMoney.grid(column=0, row=4, sticky="w", padx=10, pady=10)

        self.entrySumExtraMoney = Entry(self.frameEndFormShiftEnd, width=20, textvariable=self.varDeferment, font=("Helvetica", 18), state="disabled")
        self.entrySumExtraMoney.grid(column=1, row=4, padx=25, pady=10, ipady=5, sticky="ew")

        # --- Cash Handed Over ---
        self.lblSumOfTakeAway = Label(self.frameEndFormShiftEnd, text="Cash handed over:", font=("Helvetica", 18))
        self.lblSumOfTakeAway.grid(column=0, row=5, sticky="w", padx=10, pady=10)

        self.entrySumOfTakeAway = Entry(self.frameEndFormShiftEnd, width=20, textvariable=self.varCash, font=("Helvetica", 18))
        self.entrySumOfTakeAway.grid(column=1, row=5, padx=25, pady=10, ipady=5, sticky="ew")

        #~Two extra buttons
        self.frameButtonsFormShiftEnd = Frame(self.frameEndFormShiftEnd)
        self.frameButtonsFormShiftEnd.grid(column=0, columnspan=3, row=6,
                                           sticky="nsew", pady=(14, 0))
        
        self.frameButtonsFormShiftEnd.grid_columnconfigure(0, weight=1)
        self.frameButtonsFormShiftEnd.grid_columnconfigure(1, weight=1)
        self.frameButtonsFormShiftEnd.grid_columnconfigure(2, weight=1)

        # --- COUNT Button ---
        self.btnCountEndShift = Button(self.frameButtonsFormShiftEnd, text="COUNT", width=10)
        self.btnCountEndShift.grid(column=2, row=1, sticky="nsew", padx=(0, 24))
        self.btnCountEndShift.configure(command=self.CountEndShift)

        # --- SAVE Button---
        self.btnSaveEndShift = Button(self.frameButtonsFormShiftEnd, text="SAVE", width=5)
        self.btnSaveEndShift.grid(column=0, row=1, sticky="nsew", padx=(10, 0))
        self.btnSaveEndShift.configure(command=self.SaveEndShift)

    """
    def CreateForm1(self):    
        self.lblSumTakeAway = Label(self.frameEndFormShiftEnd, text="Take Away Sum:")
        self.lblSumTakeAway.grid(column=0, row=0, sticky=W)
        self.lblSumFoodCards = Label(self.frameEndFormShiftEnd, text="Food Card Sum:")
        self.lblSumFoodCards.grid(column=0, row=1, sticky=W)
        self.lblSumCards = Label(self.frameEndFormShiftEnd, text="Cards Sum: ")
        self.lblSumCards.grid(column=0, row=2, sticky=W)
        self.lblSumShopping = Label(self.frameEndFormShiftEnd, text="Extra Spendings: ")
        self.lblSumShopping.grid(column=0, row=3, sticky=W)
        
        
        # This is the amount of money which are put aside
        # There are three usecases that can happened:
        # 1. 
        # The whole 1000Kc are put aside and the last entry (Cash handed over: )
        # is possitive number, this is the correct approach and does not have to
        # be more specified
        # 2.
        # The whole 1000Kc are put aside and the last entry (Cash handed over: )
        # is negative number, this is also possible, because the Shop has less than
        # 1000Kc cash in the cashier.
        # This approach is handled like this:
        # 1.1 The info message is shown, that the cash is less than 0 what
        # means, that the Money Deferment won't be 1000Kc, but less.
        # 1.2 the Cash handled over became 0 and the rest of the cash is add for the deferment.
        # Example:
        # After decreasing the Take Away Sum by the Food cards, cards and extra spendings
        # the take away sum of cash is 950Kc and the deferment hasn't been decreased yet
        # So the Cash handled Over will be -50Kc...
        # The info message is shown and the Cash handled over becomes 0, the Cash deferment becomes 950Kc.
        # 3.
        # The whole 1000Kc are put aside and the last entry (Cash handed over: )
        # is negative number, but even when the use cases is triggered, the number is still negative.
        # In other words, the Cash Deferment is 0 and the Cash handled over is negative number.
        # this isn't correct approach and it is an error, so the error message must be triggered 
        # and who is responsible for the cashier has to look for some error in the sum of Cards or so...

        self.lblExtraMoney = Label(self.frameEndFormShiftEnd, text="Money Deferment (1000Kč): ")
        self.lblExtraMoney.grid(column=0, row=4, sticky=W)
        self.lblSumOfTakeAway = Label(self.frameEndFormShiftEnd, text="Cash handed over: ")
        self.lblSumOfTakeAway.grid(column=0, row=5, sticky=W)

        #~Form Entrys
        self.entrySumTakeAway = Entry(self.frameEndFormShiftEnd, width=21, textvariable=self.varTakeAwaySum)
        self.entrySumTakeAway.grid(column=1, row=0, padx=(25,0))
        self.entrySumTakeAway.configure()

        self.entrySumFoodCards = Entry(self.frameEndFormShiftEnd, width=21)
        self.entrySumFoodCards.grid(column=1, row=1, padx=(25,0))
        
        self.entrySumCards = Entry(self.frameEndFormShiftEnd, width=21)
        self.entrySumCards.grid(column=1, row=2, padx=(25,0))
        
        self.entrySumShopping = Entry(self.frameEndFormShiftEnd, width=21)
        self.entrySumShopping.grid(column=1, row=3, padx=(25,0))
        
        self.entrySumExtraMoney = Entry(self.frameEndFormShiftEnd, width=21, textvariable=self.varDeferment)
        self.entrySumExtraMoney.grid(column=1, row=4, padx=(25,0))
        
        self.entrySumOfTakeAway = Entry(self.frameEndFormShiftEnd, width=21, textvariable=self.varCash)
        self.entrySumOfTakeAway.grid(column=1, row=5, padx=(25,0))

        #~Two extra buttons
        self.frameButtonsFormShiftEnd = Frame(self.frameEndFormShiftEnd)
        self.frameButtonsFormShiftEnd.grid(column=0, columnspan=3, row=6,
                                           sticky="nsew", pady=(14, 0))
        
        self.btnCountEndShift = Button(self.frameButtonsFormShiftEnd, text="COUNT",
                                       width=12)
        self.btnCountEndShift.pack(side="right")
        self.btnCountEndShift.configure(command=self.CountEndShift)
        
        self.btnSaveEndShift = Button(self.frameButtonsFormShiftEnd, text="SAVE")
        self.btnSaveEndShift.pack(side="left")
        self.btnSaveEndShift.configure(command=self.SaveEndShift)
    """

    def EditEndShiftForm(self):
        self.btnCountEndShift.config(text="COUNT", command=self.CountEndShift)
        self.entrySumCards.config(state="normal")
        self.entrySumFoodCards.config(state="normal")
        self.entrySumShopping.config(state="normal")
        self.entrySumTakeAway.config(state="normal")
        self.entrySumOfTakeAway.config(state="normal")

    def SaveEndShift(self):
        self.btnCountEndShift.config(text="EDIT", command=self.EditEndShiftForm)
        self.entrySumCards.config(state="disabled")
        self.entrySumExtraMoney.config(state="disabled")
        self.entrySumFoodCards.config(state="disabled")
        self.entrySumOfTakeAway.config(state="disabled")
        self.entrySumShopping.config(state="disabled")
        self.entrySumTakeAway.config(state="disabled")
    
    def MakeFinalSum(self):

        form_entry_fields = {
            "take_away_sum": self.entrySumTakeAway,
            "cards": self.entrySumCards,
            "food_cards": self.entrySumFoodCards,
            "deferment": self.entrySumExtraMoney,
            "shopping": self.entrySumShopping,
            "final_sum": self.entrySumOfTakeAway
        }

        values = {}
        for key, entry in form_entry_fields.items():
            try:
                values[key] = int(entry.get())
                entry.config(background="white", foreground=dark_text_color)
            except ValueError:
                entry.config(background=dark_red, foreground=light_text_color)
                return

        expenses = values["cards"] + values["food_cards"] + values["shopping"]

        if values["take_away_sum"] < expenses:
            error_field = False
            for key in ["cards", "food_cards", "shopping"]:
                if values[key] > values["take_away_sum"]:
                    form_entry_fields[key].config(background=dark_red, foreground=light_text_color)
                    error_field = True

            if error_field:
                self.ShowErrorMessage(f"Field with red background\n"
                    f"has unexpectedly high value\n"
                    f"Please take a look at this field\n"
                    )
            else:
                self.ShowErrorMessage(f"\n\n\nThe expenses are higher\n"
                    f"than expected.\n"
                    f"Please take a look at this field\n\n"
                    f"In case that there were\n"
                    f"big shopping expenses,\n"
                    f"plese give the receipt to\n"
                    f"any delivery guy and erase\n"
                    f"the value here."
                    )

        else:
            sum_with_deferment = values["take_away_sum"] - expenses
            if sum_with_deferment < 1000:
                self.varDeferment.set(sum_with_deferment)
                self.varCash.set(0)
            else:
                self.varDeferment.set(1000)
                self.varCash.set(sum_with_deferment - 1000)
            
            self.ErrorMessageSuccess()

    def ShowErrorMessage(self, message):
        self.errorCanvas.itemconfig(self.canvasText, text=message, fill=dark_text_color)
        self.errorCanvas.config(bg=light_red)

    def ErrorMessageSuccess(self):
        success_message = (
            f"\n\n\n\nEverything looks good\n\n"
            f"Please pack:\n"
        )

        if self.varCash.get() != 0:
            success_message+=f"\t{self.varCash.get()}Kč in cash\n"
        if self.entrySumCards.get() != "0":
            success_message+=f"\t{self.entrySumCards.get()}Kč in card reciepts\n"
        if self.entrySumFoodCards.get() != "0":
            success_message+=f"\t{self.entrySumFoodCards.get()}Kč in food cards\n"



        self.errorCanvas.itemconfig(self.canvasText,
            text=success_message, fill=dark_text_color)
        self.errorCanvas.config(bg=light_green)

    def CountEndShift(self):

        entry_fields = {
            "oSum": self.entrySumTakeAway,
            "cSum": self.entrySumCards,
            "fSum": self.entrySumFoodCards,
            "sSum": self.entrySumShopping
        }

        error_found = False

        self.errorCanvas = Canvas(self.frameEndFormShiftEnd, width=300, height=100, bg="lightgrey")
        self.errorCanvas.grid(column=3, row=0, rowspan=7, padx=10, pady=(20, 0), sticky="nsw")

        self.canvasText = self.errorCanvas.create_text(140, 80, text="", font=("Helvetica", 14, "bold"), fill=dark_red, width=300)
    
        for key, entry in entry_fields.items():
            try:
                int(entry.get())
                entry.config(background=light_text_color, foreground=dark_text_color)
            except ValueError:
                entry.config(background=dark_red, foreground=light_text_color)
                error_found = True

        if error_found:
            self.ShowErrorMessage(f"In a field with red background\n"
            f"is an unexpected character.\n"
            f"Please insert only numbers\n"
            )
        else:
            self.MakeFinalSum()

        
    def UploadAction(self):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)

    def CreateShiftEndPage(self):

        #--Partition of the Shift End notebook page
        self.frameInteractiveShiftEnd = Frame(self.frameShiftEnd)
        self.frameInteractiveShiftEnd.pack(anchor="nw")
        self.frameButtonsShiftEnd = Frame(self.frameInteractiveShiftEnd)
        self.frameButtonsShiftEnd.grid(column=0, row=1, sticky="w", padx=2, pady=(50, 10), ipadx=15)
        self.frameEndInfoShiftEnd = Frame(self.frameInteractiveShiftEnd)
        self.frameEndInfoShiftEnd.grid(column=0, row=3, sticky="nw", padx=(15, 0))
        self.frameEndFormShiftEnd = Frame(self.frameInteractiveShiftEnd)
        self.frameEndFormShiftEnd.grid(column=1, row=3, padx=(170,0), sticky="nw")
        
        #Components in Buttons Shift End
        self.btnPrintEnd = Button(self.frameInteractiveShiftEnd, text="PRINT DAILY OVERVIEW", 
                                  bg=light_blue, fg=light_text_color, border=2, borderwidth=2,
                                  padx=15)
        self.btnPrintEnd.grid(column=0, row=0, rowspan=2,
                              padx=(15, 0), pady=(15,10),
                              sticky="n")
        
        self.btnSaveInovice = Button(self.frameInteractiveShiftEnd, text="UPLOAD INOVICE", 
                                  bg=light_blue, fg=light_text_color, border=2, borderwidth=2,
                                    padx=15, command=lambda: self.UploadAction())
        self.btnSaveInovice.grid(column=1, row=0, rowspan=2,
                                 padx=(170,0), pady=(15,0),
                                 sticky="wn")
        self.CreateShiftEndInfo()
        self.CreateForm()





    def CreateHistoryOrdersPage(self):
        """Creates a scrollable frame for displaying order history."""
        
        #-- Canvas Scrollbar
        self.canvas = Canvas(self.frameHistoryOrders, bg="white")
        self.scrollbar = Scrollbar(self.frameHistoryOrders, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        self.scrollable_frame = Frame(self.canvas, bg="white")

        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=(0, 0, self.canvas.bbox("all")[2], self.canvas.bbox("all")[3] + 150)
            )
        )

        self.canvas.bind("<Enter>", self._bind_scroll_events)
        self.canvas.bind("<Leave>", self._unbind_scroll_events)

        self.canvas.pack(side="left", fill="both", expand=1)
        self.scrollbar.pack(side="right", fill="y", ipadx=8)

        self.CreateHeaderRow()

        for index, order in enumerate(loadOrders()):
            self.CreateOrderRow(order, index)


    def _bind_scroll_events(self, event):

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows/macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # Linux (scroll up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # Linux (scroll down)

    def _unbind_scroll_events(self, event):

        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):

        self.scroll_speed = 0.015
        current_position = self.canvas.yview()[0]

        if event.num == 4:
            new_position = max(0, current_position - self.scroll_speed)
        elif event.num == 5:
            new_position = min(1, current_position + self.scroll_speed)
        else:
            new_position = max(0, min(1, current_position - (event.delta / 120) * self.scroll_speed))

        self.canvas.yview_moveto(new_position)

    def _on_mousewheel_active(self, event):
        
        self.scroll_speed = 0.015

        current_position = self.activeCanvas.yview()[0]
        
        if event.num == 4:
            new_position = max(0, current_position - self.scroll_speed)
        if event.num == 5:
            new_position = min(1, current_position + self.scroll_speed)
        
        self.activeCanvas.yview_moveto(new_position)

    def CreateHeaderRow(self):
        
        headers = ["Přijato", "State and Price", "Order Info", "Customer"]
        widthColumn = int(self.screen_width/105)
        self.column_widths = [int(widthColumn*1.5), int(widthColumn*1.5), int(widthColumn*4.5), int(widthColumn*2.5)]


        header_frame = Frame(self.scrollable_frame, bg="gray", padx=5, pady=5)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        for col, text in enumerate(headers):
            label = Label(header_frame, text=text, font=("Helvetica", 14, "bold"), 
                        bg="gray", fg="white", width=self.column_widths[col], anchor="w")
            label.grid(row=0, column=col, padx=5, pady=2, sticky="w")


    def CreateOrderRow(self, order, index):

        bg_color = light_text_color

        row_frame = Frame(self.scrollable_frame, bg=bg_color, padx=5, pady=5)
        row_frame.grid(row=(index+1)*2, column=0, columnspan=4, sticky="ew")

        # Column 1: Date
        date_time_order = f"{order["datetime"].split()[0]} - {order["datetime"].split()[1]}"
        datetime_label = Label(row_frame, text=date_time_order, font=("Helvetica", 16), bg=bg_color, anchor="w", width=23)
        datetime_label.grid(row=0, column=0, padx=(5,0), pady=2, sticky="ew", ipady=60)

        # Column 2: State
        status_price_text = f"Stav: {order['status']}\nCelkem cena: {order['total_price']}\nDoprava: {order['delivery']}"
        status_price_label = Label(row_frame, text=status_price_text, font=("Helvetica", 16), bg=bg_color, width=23, justify=LEFT,
                                   anchor="w")
        status_price_label.grid(row=0, column=1, pady=2, padx=(4,0), sticky="ew")

        # Column 3: Order
        items_text = "\n".join(f" • {p['name']} ({p['price']})" for p in order["products"])
        items_label = Label(row_frame, text=items_text, font=("Helvetica", 16), bg=bg_color, justify=LEFT, anchor="w", width=68)
        items_label.grid(row=0, column=2, pady=16, padx=(8,0), sticky="ew")

        # Column 4: Customer
        customer_info = f"{order['customer']['name']}\n{order['customer']['address']}\nTel.: {order['customer']['phone']}\nCena: {order['total_price']}"
        customer_label = Label(row_frame, text=customer_info, font=("Helvetica", 16), bg=bg_color, justify=LEFT, anchor="w")
        customer_label.grid(row=0, column=3, pady=2, sticky="ew")

        separator = Frame(self.scrollable_frame, height=2, bg=dark_text_color)
        separator.grid(row=(index+1)*2+1, column=0, columnspan=4, sticky="ew", pady=2)



    def CreateActiveOrdersPage(self):
        
        
        self.activeCanvas = Canvas(self.frameActiveOrders, bg="white")
        self.activeScrollbar = Scrollbar(self.frameActiveOrders, orient="vertical", command=self.activeCanvas.yview)
        self.activeCanvas.configure(yscrollcommand=self.activeScrollbar.set)

        self.active_scrollable_frame = Frame(self.activeCanvas, bg="white")

        self.window_id = self.activeCanvas.create_window((0, 0), window=self.active_scrollable_frame, anchor="nw")

        self.active_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.activeCanvas.configure(
                scrollregion=(0, 0, self.activeCanvas.bbox("all")[2], self.activeCanvas.bbox("all")[3] + 50)
            )
        )
        self.activeCanvas.bind_all("<MouseWheel>", self._on_mousewheel_active)
        self.activeCanvas.bind_all("<Button-4>", self._on_mousewheel_active)
        self.activeCanvas.bind_all("<Button-5>", self._on_mousewheel_active)

        self.activeCanvas.pack(side="left", fill="both", expand=1)
        self.activeScrollbar.pack(side="right", fill="y", ipadx=8)

        self.activeCanvas.config(scrollregion=(0,0,1000,10000))

        self.CreateActiveHeaderRow()

        orders = loadOrders()
        
        sorted_orders = sorted(orders, key=lambda order: (order.get('status') != "Neověřeno", order.get('delivery') == "Neznámý"))


        for index, order in enumerate(sorted_orders):
            if order['status'] == "Neověřeno" or (order['status'] == "Ověřeno" and order['delivery'] == "Neznámý"):
                self.CreateActiveOrderRow(order, index)


    def UpdateFramesList(self):
        self.active_scrollable_frame.destroy()

        self.active_scrollable_frame = Frame(self.activeCanvas, bg="white")

        self.active_scrollable_frame.bind("<Configure>", lambda e: self.activeCanvas.configure(scrollregion=self.activeCanvas.bbox("all")))
        self.activeCanvas.create_window((0, 0), window=self.active_scrollable_frame, anchor="nw")

        self.CreateActiveHeaderRow()

        sorted_orders = sorted(
            loadOrders(),
            key=lambda order: (order['status'] != "Neověřeno", order['delivery'] == "Neznámý")
        )

        for index, order in enumerate(sorted_orders):
            if order['status'] == "Neověřeno" or (order['status'] == "Ověřeno" and order['delivery'] == "Neznámý"):
                self.CreateActiveOrderRow(order, index)

        for index, order in enumerate(loadOrders()):
            self.CreateOrderRow(order, index)

        for key, value in self.varDictDeliveries.items():
            if value.get() != 0:
                Label(self.frameDeliveries, text=f"R{key} - {value.get()}Kč").grid(column=0, row=key, sticky="w")
                #Label(self.frameDeliveries, text=f"R{key}").grid(column=0, row=key, sticky="w")
                #Label(self.frameDeliveries, text=f"{value.get()}Kč").grid(column=1, row=key, sticky="w")
        if self.varTakeAwaySum.get() != 0:
            Label(self.frameDeliveries ,text=f"Take away - {self.varTakeAwaySum.get()}Kč").grid(column=0, row=8, sticky="w")
            #Label(self.frameDeliveries ,text=f"Take away").grid(column=0, row=8, sticky="w")
            #Label(self.frameDeliveries ,text=f"{self.varTakeAwaySum.get()}Kč").grid(column=1, row=8, sticky="w")
            
        
    def CreateActiveHeaderRow(self):
        
        headers = ["Přijato", "Order Info", "State and Price", "Customer", "Actions"]
        widthColumn = int(self.screen_width/105)
        self.column_widths = [int(widthColumn*1.3), int(widthColumn*3.7), int(widthColumn*1.5), int(widthColumn*1.8), int(widthColumn*1.7)]


        header_frame = Frame(self.active_scrollable_frame, bg="gray", padx=5, pady=5)
        header_frame.grid(row=0, column=0, columnspan=5, sticky="ew")

        for col, text in enumerate(headers):
            label = Label(header_frame, text=text, font=("Helvetica", 14, "bold"), 
                        bg="gray", fg="white", width=self.column_widths[col], anchor="w")
            label.grid(row=0, column=col, padx=5, pady=2, sticky="w")

    def FinishOrder(self, order_id):

        def set_delivery(delivery_name):
            
            orders = loadOrders()
            for order in orders:
                if order["id"] == order_id:
                    order["status"] = "Hotovo"
                    order["delivery"] = delivery_name
                    break
            
            if delivery_name == "Take Away":
                self.varTakeAwaySum.set(self.varTakeAwaySum.get() + int(order["total_price"].replace("Kč", "").strip())) 
            else:
                self.varDictDeliveries[int(delivery_name[1])].set(self.varDictDeliveries[int(delivery_name[1])].get() + int(order["total_price"].replace("Kč", "").strip())) 

            with open("orders.json", "w", encoding="utf-8") as file:
                json.dump(orders, file, indent=4, ensure_ascii=False)

            self.active_scrollable_frame.update()
            finish_window.destroy()

            self.UpdateFramesList()

        finish_window = Toplevel(self.frameHistoryOrders)
        finish_window.title("Select Delivery")
        finish_window.geometry("800x400")
        finish_window.configure(bg="white")

        finish_window.grab_set()
        finish_window.focus_set()
        finish_window.transient(self.frameHistoryOrders)

        finish_window.update_idletasks()
        win_width = finish_window.winfo_width()
        win_height = finish_window.winfo_height()
        screen_width = finish_window.winfo_screenwidth()
        screen_height = finish_window.winfo_screenheight()
        x_position = (screen_width // 2) - (800 // 2)
        y_position = (screen_height // 2) - (400 // 2)
        finish_window.geometry(f"800x400+{x_position}+{y_position}")

        Label(finish_window, text="Select Delivery Method", font=("Helvetica", 14, "bold"), bg="white").grid(
            row=0, column=0, columnspan=3, sticky="ew", pady=10
        )

        self.leftFrameWin = Frame(finish_window, bg="white")
        self.leftFrameWin.grid(row=1, column=0, padx=(30, 0), pady=10, sticky="nsew")

        separator = Frame(finish_window, bg=dark_text_color, width=2)
        separator.grid(row=1, column=1, sticky="ns", padx=(25, 0), pady=2)

        self.rightFrameWin = Frame(finish_window, bg="white")
        self.rightFrameWin.grid(row=1, column=2, padx=(30, 0), pady=10, sticky="nsew")

        self.leftFrameWin.grid_columnconfigure(0, weight=1)
        self.rightFrameWin.grid_columnconfigure(0, weight=1)
        self.rightFrameWin.grid_columnconfigure(1, weight=1)

        Button(self.rightFrameWin, text="R1", font=("Helvetica", 16), width=15, height=2, command=lambda d="R1": set_delivery(d)).grid(column=0, row=0, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R2", font=("Helvetica", 16), width=15, height=2, command=lambda d="R2": set_delivery(d)).grid(column=1, row=0, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R3", font=("Helvetica", 16), width=15, height=2, command=lambda d="R3": set_delivery(d)).grid(column=0, row=1, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R4", font=("Helvetica", 16), width=15, height=2, command=lambda d="R4": set_delivery(d)).grid(column=1, row=1, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R5", font=("Helvetica", 16), width=15, height=2, command=lambda d="R5": set_delivery(d)).grid(column=0, row=2, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R6", font=("Helvetica", 16), width=15, height=2, command=lambda d="R6": set_delivery(d)).grid(column=1, row=2, padx=5, pady=(30, 0))

        Button(self.leftFrameWin, text="Take Away", font=("Helvetica", 16), width=15, height=2, command=lambda: set_delivery("Take Away")).grid(row=0, column=0, padx=5, pady=116)

        finish_window.grid_columnconfigure(0, weight=1)
        finish_window.grid_columnconfigure(1, weight=0)
        finish_window.grid_columnconfigure(2, weight=1)
        finish_window.grid_rowconfigure(1, weight=1)



    def VerifyOrder(self, btn_verify, order_id):

        btn_verify.config(text="HOTOVO", command=lambda: self.FinishOrder(order_id))

        orders = loadOrders()
        for order in orders:
            if order["id"] == order_id:
                order["status"] = "Ověřeno"
                break
        
        with open("orders.json", "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        self.UpdateFramesList()


    def CancelOrder(self, order_id):

        orders = loadOrders()
        res = msg.askquestion('Cancel Order', 'Do you really want to cancel order')
        if res == "no" : return
        for order in orders:
            if order["id"] == order_id:
                order["status"] = "Canceled"
                order["delivery"] = "Nedoručeno"
                break
        
        with open("orders.json", "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        self.UpdateFramesList()

    def PrintOrder(self):
        pass

    def CreateActiveOrderRow(self, order, index):

        if order["status"] == "Neověřeno":
            bg_color = light_red
        else:
            bg_color = light_green
        

        row_frame = Frame(self.active_scrollable_frame, bg=bg_color, padx=5, pady=5)
        row_frame.grid(row=(index+1)*2, column=0, columnspan=5, sticky="ew", ipady=10)
        row_frame.grid_rowconfigure(0, weight=1)

        date_time_order = f"{order['datetime'].split()[0]}\n   {order['datetime'].split()[1]}"
        datetime_label = Label(row_frame, text=date_time_order, font=("Helvetica", 16), bg=bg_color, anchor="w", width=17)
        datetime_label.grid(row=0, column=0, padx=(5, 0), pady=(10, 10), sticky="nsw")

        status_price_text = f"Stav: {order['status']}\nCelkem cena: {order['total_price']}\nDoprava: {order['delivery']}"
        status_price_label = Label(row_frame, text=status_price_text, font=("Helvetica", 16), bg=bg_color, width=23, justify=LEFT, anchor="w")
        status_price_label.grid(row=0, column=2, pady=(10, 10), padx=(1, 0), sticky="nsw")

        items_text = "\n".join(f" • {p['name']} ({p['price']})" for p in order["products"])
        items_label = Label(row_frame, text=items_text, font=("Helvetica", 16), bg=bg_color, justify=LEFT, anchor="w", width=56)
        items_label.grid(row=0, column=1, pady=(10, 10), padx=(33, 0), sticky="nsw")

        customer_info = f"{order['customer']['name']}\n{order['customer']['address']}\nTel.: {order['customer']['phone']}\nCena: {order['total_price']}"
        customer_label = Label(row_frame, text=customer_info, font=("Helvetica", 16), bg=bg_color, justify=LEFT, anchor="w", width=27, wraplength=250)
        customer_label.grid(row=0, column=3, pady=(10, 10), padx=(2,10), sticky="nsw")

        self.lblButtons = Frame(row_frame, bg=bg_color)
        self.lblButtons.grid(row=0, column=4, pady=(10, 10), sticky="nsw")

        self.lblButtons.grid_rowconfigure(0, weight=1)
        self.lblButtons.grid_rowconfigure(1, weight=1)
        self.lblButtons.grid_rowconfigure(2, weight=1)

        btn_verify = Button(self.lblButtons, width=15, text="")
        btn_verify.grid(column=0, row=0, pady=(5, 5))

        if order['status'] == "Ověřeno":
            btn_verify.config(text="HOTOVO", command=lambda: self.FinishOrder(order["id"]))
        elif order['status'] == "Neověřeno":
            btn_verify.config(text="OVĚŘIT", command=lambda: self.VerifyOrder(btn_verify, order["id"]))

        self.btnCancel = Button(self.lblButtons, width=15, text="STORNO", command=lambda: self.CancelOrder(order["id"]))
        self.btnCancel.grid(column=0, row=1, pady=(5, 5))

        self.btnPrint = Button(self.lblButtons, width=15, text="TISK", command=self.PrintOrder)
        self.btnPrint.grid(column=0, row=2, pady=0)

        separator = Frame(self.active_scrollable_frame, height=3, bg=dark_text_color)
        separator.grid(row=(index+1)*2+1, column=0, columnspan=5, sticky="ew")



root = Tk()

app = OrderApp(root)
root.mainloop()