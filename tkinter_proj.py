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
from functools import partial


def loadOrders():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            orders = json.load(file)

            if not isinstance(orders, list):
                raise ValueError("JSON data not in a list.")

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

dark_text_color  = "#000000"
light_text_color = "#eee9f2"

order_row_color = "#C9C9C9"

# White
background_color_ternary = "#CEE5F2"
#background_color_ternary = "#6D696A"
# Yellow
background_color_secondary = "#DDB967"
# Grey
background_color_primary = "#767676"

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
    ("Pizza Mozzarella", "179 Kč"),
    ("Pizza Quattro Formaggi", "179 Kč"),
    ("Pizza Vegetariano", "189 Kč"),
    ("Pizza Primavera", "189 Kč"),
    ("Pizza Caprese", "179 Kč"),
    ("Pizza Prosciuto", "179 Kč"),
    ("Pizza Salami", "179 Kč"),
    ("Pizza Hawaii", "179 Kč"),
    ("Pizza Quattro di Salami", "179 Kč"),
    ("Pizza Capricciosa", "179 Kč"),
    ("Pizza Rimini", "179 Kč"),
    ("Pizza San Daniele", "194 Kč"),
    ("Pizza Monako", "208 Kč"),
    ("Pizza Cardinale", "179 Kč"),
    ("Pizza Madona", "189 Kč"),
    ("Pizza Popay", "179 Kč"),
    ("Pizza Milano", "179 Kč"),
    ("Pizza Curiosa", "179 Kč"),
    ("Pizza Agadir", "179 Kč"),
    ("Pizza Gustosa", "179 Kč"),
    ("Pizza Zola", "179 Kč"),
    ("Pizza Generosa", "179 Kč"),
    ("Pizza Familiare", "179 Kč"),
    ("Pizza Piacentina", "214 Kč")
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

        root.title("Aplikace pizzerie")

        #Window sizes
        root.resizable(False, False)
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.geometry(f"{self.screen_width-70}x{self.screen_height-70}+70+0")

        #Variables
        #Take Away Sum
        self.varTakeAwaySum = IntVar(value = 0)
        #Deferment from TakeAway
        self.varDeferment = IntVar(value = 0)
        #Delivery guys financials
        self.varDictDeliveries = {1: IntVar(value = 0), 2: IntVar(value = 0),
                                  3: IntVar(value = 0), 4: IntVar(value = 0),
                                  5: IntVar(value = 0), 6: IntVar(value = 0)
                                  }
        #Cash handled by Take Away
        self.varCash = IntVar(value = 0)
        #Sum of Orders without canceled Orders
        self.varFinalSum = IntVar(value = 0)
        #Sum of Orders with canceled Orders
        self.varDailyPrice = IntVar(value = 0)
        #Num of Orders
        self.varOrderNum = IntVar(value = 0)
        #Date first order
        self.varDateFirstOrder = StringVar(value = "")
        #Date last Order
        self.varDateLastOrder = StringVar(value = "")
        #Date end generated
        self.varActualDate = StringVar(value="")


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
        self.frameShiftEnd.bind("<FocusIn>", lambda event: root.bind("<Return>", lambda event: self._trigger_count_and_enable_save()))
        self.frameShiftEnd.bind("<FocusOut>", lambda event: root.unbind("<Return>"))

    # Custom Scrolling event which synchoronize the two scrollbars 
    # One in Active Orders and Second in History of Orders
    def _on_mousewheel_active(self, event):
        
        self.scroll_speed = 0.015

        current_position_active = self.activeCanvas.yview()[0]
        current_position = self.canvas.yview()[0]

        if event.num == 4:
            new_position_active = max(0, current_position_active - self.scroll_speed)
            new_position = max(0, current_position - self.scroll_speed)
        if event.num == 5:
            new_position_active = min(1, current_position_active + self.scroll_speed)
            new_position = min(1, current_position + self.scroll_speed)
        
        self.activeCanvas.yview_moveto(new_position_active)
        self.canvas.yview_moveto(new_position)

    def _tab_selected(self, event):
        selected_tab = event.widget.index(event.widget.select())
        tab_text = self.notebook.tab(selected_tab, "text")

        if tab_text == "Konec směny":
            self.varActualDate.set(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
            self.valueGenerated.config(text=str(self.varActualDate.get()))

    def _trigger_count_and_enable_save(self):
        self.CountEndShift()
        self.btnCountEndShift.focus_set()

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

        #For now it generates random order after click
        self.btnCreateOrder = Button(self.headerFrame, text="VYTVOŘIT OBJEDNÁVKU",
                                     command=lambda:self.generateRandomOrder())
        self.btnCreateOrder.grid(row=0, column=1, sticky="nswe")
        self.btnCreateOrder.configure(background=light_blue, width=self.screen_width//25)

        #Info label in header
        self.lblBranchName = Label(self.headerFrame, text="Bistro Olomouc - BOH0162")
        self.lblBranchName.grid(row=0, column=0, sticky="w", padx=(25,0))
        self.lblBranchName.configure(foreground="white", background=dark_yellow)

        #Logout button
        self.btnLogout = Button(self.headerFrame, text="Odhlasit se", border=0)
        self.btnLogout.grid(row=0, column=3, sticky="e", padx=(0, 0))
        self.btnLogout.configure(foreground="white", background=dark_yellow)

    #Generates random order with random values
    def generateRandomOrder(self):
        name = random.choice(names) + random.choice(surnames)
        village = random.choice(villages)
        address = f"{village} {random.randint(1, 500)}, {village}"
        phone = f"{random.randint(700, 800)} {random.randint(000, 1000)} {random.randint(000, 999)}"

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
        
        self.varDailyPrice.set(self.varDailyPrice.get() + total_price)
        if(self.varOrderNum.get() < 1):
            self.varDateFirstOrder.set(new_order["datetime"])
            self.valueDateFrom.config(text=str(self.varDateFirstOrder.get()))
        self.varDateLastOrder.set(new_order["datetime"])
        self.varOrderNum.set(self.varOrderNum.get() + 1)

        self.UpdateFramesList()



    def CreateNotebook(self):
        #----Notebook on main page
        self.notebook = ttk.Notebook(self.mainFrame)
        self.notebook.pack(fill="both", expand=1)

        # Binding
        self.notebook.bind("<<NotebookTabChanged>>", self._tab_selected)
        
        self.frameActiveOrders = ttk.Frame(self.notebook)
        self.frameActiveOrders.pack()
        self.frameHistoryOrders = ttk.Frame(self.notebook)
        self.frameHistoryOrders.pack()
        self.frameShiftEnd = ttk.Frame(self.notebook)
        self.frameShiftEnd.pack()

        self.notebook.add(self.frameActiveOrders, text="Aktivní objednávky")
        self.notebook.add(self.frameHistoryOrders, text="Historie objednávek")
        self.notebook.add(self.frameShiftEnd, text="Konec směny")
    
    #Info page when shift ends
    def CreateShiftEndInfo(self):
        
        self.frameGenerated = Frame(self.frameEndInfoShiftEnd)
        self.frameGenerated.grid(column=0, row=0, sticky="nw", padx=0)

        # Main info label
        self.lblEnd = Label(self.frameGenerated, text="UZÁVĚRKA FINANCÍ SMĚNY", font="Helvetica 18 bold")
        self.lblEnd.grid(column=0, row=0, columnspan=2, pady=(25,5), sticky="nw")
        

        # Left Info labels
        self.lblGenerated = Label(self.frameGenerated, text="Uzávěrka generována:", font="Helvetica 16")
        self.lblGenerated.grid(column=0, row=1, sticky="nw", padx=0, pady=2)

        self.lblDateFrom = Label(self.frameGenerated, text="První objednávka přijata:", font="Helvetica 16")
        self.lblDateFrom.grid(column=0, row=2, sticky="nw", padx=0, pady=2)

        self.lblDateTo = Label(self.frameGenerated, text="Poslední objednávka přijata:", font="Helvetica 16")
        self.lblDateTo.grid(column=0, row=3, sticky="nw", padx=0, pady=2)

        self.lblNumOfOrders = Label(self.frameGenerated, text="Počet objednávek:", font="Helvetica 16")
        self.lblNumOfOrders.grid(column=0, row=4, sticky="nw", padx=0, pady=2)

        # Right Values label
        self.valueGenerated = Label(self.frameGenerated, text=str(self.varActualDate.get()), font="Helvetica 16", fg=dark_blue)
        self.valueGenerated.grid(column=1, row=1, sticky="nw", padx=15, pady=2)

        self.valueDateFrom = Label(self.frameGenerated, text=str(self.varDateFirstOrder.get()), font="Helvetica 16", fg=dark_blue)
        self.valueDateFrom.grid(column=1, row=2, sticky="nw", padx=15, pady=2)

        self.valueDateTo = Label(self.frameGenerated, text=str(self.varDateLastOrder.get()), font="Helvetica 16", fg=dark_blue)
        self.valueDateTo.grid(column=1, row=3, sticky="nw", padx=15, pady=2)

        self.valueNumOfOrders = Label(self.frameGenerated, text=str(self.varOrderNum.get()), font="Helvetica 16", fg=dark_blue)
        self.valueNumOfOrders.grid(column=1, row=4, sticky="nw", padx=15, pady=2)

        
        # Frame for Deliveries Info Labels
        self.frameDeliveries = Frame(self.frameEndInfoShiftEnd)
        self.frameDeliveries.grid(column=0, row=1, sticky="nw", padx=0, pady=5)

        self.lblAllDeliveriesInfo = Label(self.frameDeliveries, text="Rozdělení podle rozvozců:")
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
                # Anonymous Label with delivery info
                Label(self.frameDeliveries, text=f"R{key} - {value.get()}Kč").grid(column=0, row=key, sticky="w")
        if self.varTakeAwaySum.get() != 0:
            # Anonymous Label with delivery info
            Label(self.frameDeliveries ,text=f"Bistro - {self.varTakeAwaySum.get()}Kč").grid(column=0, row=8, sticky="w")
   

        # Frame for Deliveries Values Labels
        self.frameSumaryOfDeliveries = Frame(self.frameEndInfoShiftEnd)
        self.frameSumaryOfDeliveries.grid(column=0, row=2, sticky="nw", padx=0, pady=25)
        
        """
        This Label(lblSumDone) has value which is counted only for the finished Orders
        the canceled Orders and the unknown Orders values ARE NOT COUNTED IN HERE! 
        """
        # Left Column with Info
        self.lblSumDone = Label(self.frameSumaryOfDeliveries, text="CELKEM HOTOVO:", font="Helvetica 18 bold")
        self.lblSumDone.grid(column=0, row=0, sticky="nw", padx=0, pady=(0, 10))

        self.lblSumAll = Label(self.frameSumaryOfDeliveries, text="Přijato celkem:", font="Helvetica 15 bold")
        self.lblSumAll.grid(column=0, row=1, sticky="nw", padx=0, pady=(0, 10))

        # Right Column with Values
        self.valueSumDone = Label(self.frameSumaryOfDeliveries, text="", font="Helvetica 18 bold", fg=dark_blue)
        self.valueSumDone.grid(column=1, row=0, sticky="nw", padx=20, pady=(0, 10))

        self.valueSumAll = Label(self.frameSumaryOfDeliveries, text="", font="Helvetica 15 bold", fg=dark_blue)
        self.valueSumAll.grid(column=1, row=1, sticky="nw", padx=20, pady=(0, 10))

        # When the first Order is accepted, the values are set
        if self.varDailyPrice.get() < 1:
            self.valueSumAll.config(text="---")
            self.valueSumDone.config(text="---")
        else:
            self.valueSumAll.config(text=str(self.varDailyPrice.get()))
            self.valueSumDone.config(text=str(self.varFinalSum.get()))


    #~Form Labels 
    def CreateForm(self):
         
        self.frameEndFormShiftEnd.grid_columnconfigure(0, weight=1)
        self.frameEndFormShiftEnd.grid_columnconfigure(1, weight=1)

        # Take Away Sum
        self.lblSumTakeAway = Label(self.frameEndFormShiftEnd, text="Objednávky bistro:", font=("Helvetica", 18))
        self.lblSumTakeAway.grid(column=0, row=0, sticky="w", padx=10, pady=(20, 10))

        self.entrySumTakeAway = Entry(self.frameEndFormShiftEnd, width=20, textvariable=self.varTakeAwaySum, font=("Helvetica", 18))
        self.entrySumTakeAway.grid(column=1, row=0, padx=25, ipady=5, pady=(20, 10), sticky="ew")
        self.entrySumTakeAway.bind("<KeyRelease>", lambda event: self.btnSaveEndShift.config(state="disabled"))

        # Food Card Sum
        self.lblSumFoodCards = Label(self.frameEndFormShiftEnd, text="Zaplaceno stravenkami:", font=("Helvetica", 18))
        self.lblSumFoodCards.grid(column=0, row=1, sticky="w", padx=10, pady=10)

        self.entrySumFoodCards = Entry(self.frameEndFormShiftEnd, width=20, font=("Helvetica", 18))
        self.entrySumFoodCards.grid(column=1, row=1, padx=25, pady=10, ipady=5, sticky="ew")
        self.entrySumFoodCards.bind("<KeyRelease>", lambda event: self.btnSaveEndShift.config(state="disabled"))

        # Cards Sum
        self.lblSumCards = Label(self.frameEndFormShiftEnd, text="Zaplaceno kartou:", font=("Helvetica", 18))
        self.lblSumCards.grid(column=0, row=2, sticky="w", padx=10, pady=10)

        self.entrySumCards = Entry(self.frameEndFormShiftEnd, width=20, font=("Helvetica", 18))
        self.entrySumCards.grid(column=1, row=2, padx=25, pady=10, ipady=5, sticky="ew")
        self.entrySumCards.bind("<KeyRelease>", lambda event: self.btnSaveEndShift.config(state="disabled"))

        # Extra Spendings
        self.lblSumShopping = Label(self.frameEndFormShiftEnd, text="Výdaje navíc:", font=("Helvetica", 18))
        self.lblSumShopping.grid(column=0, row=3, sticky="w", padx=10, pady=10)

        self.entrySumShopping = Entry(self.frameEndFormShiftEnd, width=20, font=("Helvetica", 18))
        self.entrySumShopping.grid(column=1, row=3, padx=25, pady=10, ipady=5, sticky="ew")
        self.entrySumShopping.bind("<KeyRelease>", lambda event: self.btnSaveEndShift.config(state="disabled"))

        """
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
        """
        # Money Deferment (1000Kč)
        self.lblExtraMoney = Label(self.frameEndFormShiftEnd, text="Denní odklad (1000Kč):", font=("Helvetica", 18))
        self.lblExtraMoney.grid(column=0, row=4, sticky="w", padx=10, pady=10)

        self.entrySumExtraMoney = Entry(self.frameEndFormShiftEnd, width=20, textvariable=self.varDeferment, font=("Helvetica", 18), state="disabled")
        self.entrySumExtraMoney.grid(column=1, row=4, padx=25, pady=10, ipady=5, sticky="ew")

        # Cash Handed Over
        self.lblSumOfTakeAway = Label(self.frameEndFormShiftEnd, text="Odevzdat v hotovosti:", font=("Helvetica", 18))
        self.lblSumOfTakeAway.grid(column=0, row=5, sticky="w", padx=10, pady=10)

        self.entrySumOfTakeAway = Entry(self.frameEndFormShiftEnd, width=20, textvariable=self.varCash, font=("Helvetica", 18), state="disabled")
        self.entrySumOfTakeAway.grid(column=1, row=5, padx=25, pady=10, ipady=5, sticky="ew")
        self.entrySumOfTakeAway.bind("<KeyRelease>", lambda event: self.btnSaveEndShift.config(state="disabled"))

        # Two control buttons Frame
        self.frameButtonsFormShiftEnd = Frame(self.frameEndFormShiftEnd)
        self.frameButtonsFormShiftEnd.grid(column=0, columnspan=3, row=6,
                                           sticky="nsew", pady=(14, 0))
        
        self.frameButtonsFormShiftEnd.grid_columnconfigure(0, weight=1)
        self.frameButtonsFormShiftEnd.grid_columnconfigure(1, weight=1)
        self.frameButtonsFormShiftEnd.grid_columnconfigure(2, weight=1)

        # COUNT Button
        self.btnCountEndShift = Button(self.frameButtonsFormShiftEnd, text="KONTROLA", width=11)
        self.btnCountEndShift.grid(column=2, row=1, sticky="nsew", padx=(0, 24), ipadx=4)
        self.btnCountEndShift.configure(command=self.CountEndShift)

        # SAVE Button
        self.btnSaveEndShift = Button(self.frameButtonsFormShiftEnd, text="ULOŽIT", width=5, state="disabled")
        self.btnSaveEndShift.grid(column=0, row=1, sticky="nsew", padx=(10, 0))
        self.btnSaveEndShift.configure(command=self.SaveEndShift)

    # Editing the current form 
    def EditEndShiftForm(self):
        self.btnCountEndShift.config(text="KONTROLA", command=self.CountEndShift)
        self.entrySumCards.config(state="normal")
        self.entrySumFoodCards.config(state="normal")
        self.entrySumShopping.config(state="normal")
        self.entrySumTakeAway.config(state="normal")
        self.entrySumOfTakeAway.config(state="normal")

    # Saving current form which will be saved and printed when the Print Shift end is triggered
    def SaveEndShift(self):
        # !!!!!!! Make one more logic for not possible to save the corrupted form
        self.btnCountEndShift.config(text="UPRAVIT", command=self.EditEndShiftForm)
        self.entrySumCards.config(state="disabled")
        self.entrySumExtraMoney.config(state="disabled")
        self.entrySumFoodCards.config(state="disabled")
        self.entrySumOfTakeAway.config(state="disabled")
        self.entrySumShopping.config(state="disabled")
        self.entrySumTakeAway.config(state="disabled")
    
    # Counting if the form is valid with the acceptable values
    def MakeFinalSum(self):
        # All fields
        form_entry_fields = {
            "take_away_sum": self.entrySumTakeAway,
            "cards": self.entrySumCards,
            "food_cards": self.entrySumFoodCards,
            "deferment": self.entrySumExtraMoney,
            "shopping": self.entrySumShopping,
            "final_sum": self.entrySumOfTakeAway
        }

        # Saving the values into the dict
        values = {}
        for key, entry in form_entry_fields.items():
            try:
                values[key] = int(entry.get())
                entry.config(background=background_color_ternary, foreground=dark_text_color)
            # If not filled error
            except ValueError:
                entry.config(background=dark_red, foreground=light_text_color)
                return

        # Expences that have to be decreased from the final sum
        expenses = values["cards"] + values["food_cards"] + values["shopping"]

        #Error when the expenses are higher thatexpected
        if values["take_away_sum"] < expenses:
            error_field = False
            for key in ["cards", "food_cards", "shopping"]:
                # If some Value is higher than the Final Sum it is wrong
                if values[key] > values["take_away_sum"]:
                    form_entry_fields[key].config(background=dark_red, foreground=light_text_color)
                    error_field = True

            if error_field:
                self.ShowErrorMessage(
                    f"Pole s červeným pozadím\n"
                    f"má neočekávaně vysokou hodnotu.\n"
                    f"Prosím zkontrolujte toto pole.\n"
                    )
            else:
                self.ShowErrorMessage(
                    f"\n\n\nCelkové výdaje jsou vyšší,\n"
                    f"než by se očekávalo.\n"
                    f"Prosím zkontrolujte tyto pole.\n\n"
                    f"Pokud se dělal velký nákup,\n"
                    f"prosím předejte účtenku rozvozci.\n"
                    f"ten vám za ni dá tolik peněz,\n"
                    f"kolik jste zaplatili.\n"
                    f"Poté smažte hodnotu v poli výdaje.\n"
                    )

        # Counting the money deferment
        else:
            sum_with_deferment = values["take_away_sum"] - expenses
            if sum_with_deferment < 1000:
                self.varDeferment.set(sum_with_deferment)
                self.varCash.set(0)
            else:
                self.varDeferment.set(1000)
                self.varCash.set(sum_with_deferment - 1000)
            
            self.ErrorMessageSuccess()
            self.btnSaveEndShift.config(state="normal")

    # Message when something goes wrong
    def ShowErrorMessage(self, message):
        self.errorCanvas.itemconfig(self.canvasText, text=message, fill=dark_text_color)
        self.errorCanvas.config(bg=light_red)

    # Message when everything looks good
    def ErrorMessageSuccess(self):
        if self.varCash.get() == 0 and self.entrySumCards.get() == "0" and self.entrySumFoodCards.get() == "0":
            success_message = (
            f"\n\n\n\nDo obálky neodevzdáváte\n"
            f"žádnou hotovost, stravenkové karty "
            f"ani účtenky z karet\n")

        else:
            success_message = (
                f"\n\n\n\nVše vypadá dobře spočítáno.\n"
                f"Do obálky prosím odevzdejte:\n"
            )

            if self.varCash.get() != 0:
                success_message+=f"\t{self.varCash.get()}Kč v hototvosti\n"
            if self.entrySumCards.get() != "0":
                success_message+=f"\t{self.entrySumCards.get()}Kč v účtenkách karet\n"
            if self.entrySumFoodCards.get() != "0":
                success_message+=f"\t{self.entrySumFoodCards.get()}Kč ve stravenkách\n"
            
        self.errorCanvas.itemconfig(self.canvasText,
            text=success_message, fill=dark_text_color)
        self.errorCanvas.config(bg=light_green)

    # Counting: the form logic
    def CountEndShift(self):

        entry_fields = {
            "oSum": self.entrySumTakeAway,
            "cSum": self.entrySumCards,
            "fSum": self.entrySumFoodCards,
            "sSum": self.entrySumShopping
        }

        # Variable signalizes that there is an error in create values
        error_found = False

        # The Canvas for the error visualizing
        self.errorCanvas = Canvas(self.frameEndFormShiftEnd, width=450, height=100, bg=background_color_ternary)
        self.errorCanvas.grid(column=3, row=0, rowspan=7, padx=10, pady=(20, 0), sticky="nsw")

        self.canvasText = self.errorCanvas.create_text(180, 110, text="", font=("Helvetica", 14, "bold"), fill=dark_red, width=300)
    
        for key, entry in entry_fields.items():
            try:
                int(entry.get())
                entry.config(background=light_text_color, foreground=dark_text_color)
            except ValueError:
                entry.config(background=dark_red, foreground=light_text_color)
                error_found = True

        if error_found:
            self.ShowErrorMessage(f"V poli s červeným pozadím\n"
            f"je jiný znak, než číslo.\n"
            f"Prosím pište jen čísla.\n"
            )
        else:
            self.MakeFinalSum()

    
    # Uploading the Inovice Future implementation now just dialog
    def UploadAction(self):
        filename = filedialog.askopenfilename()
        print('Vybráno:', filename)

    def CreateShiftEndPage(self):

        # Main frame in the notebook page with its context
        self.frameInteractiveShiftEnd = Frame(self.frameShiftEnd)
        self.frameInteractiveShiftEnd.pack(anchor="nw")

        # Frame where are buttons for Printing shift end and uploading inovice
        self.frameButtonsShiftEnd = Frame(self.frameInteractiveShiftEnd)
        self.frameButtonsShiftEnd.grid(column=0, row=1, sticky="w", padx=2, pady=(50, 10), ipadx=15)
        
        # Frame in which is the preview of values 
        self.frameEndInfoShiftEnd = Frame(self.frameInteractiveShiftEnd)
        self.frameEndInfoShiftEnd.grid(column=0, row=3, sticky="nw", padx=(15, 0))
        
        # Frame where is placed the form
        self.frameEndFormShiftEnd = Frame(self.frameInteractiveShiftEnd)
        self.frameEndFormShiftEnd.grid(column=1, row=3, padx=(170,0), sticky="nw")
        

        #Components in Buttons Shift End
        self.btnPrintEnd = Button(self.frameInteractiveShiftEnd, text="TISK DENNÍ UZÁVĚRKY", 
                                  bg=light_blue, fg=light_text_color, border=2, borderwidth=2,
                                  padx=15)
        self.btnPrintEnd.grid(column=0, row=0, rowspan=2,
                              padx=(15, 0), pady=(15,10),
                              sticky="wn")
        
        self.btnSaveInovice = Button(self.frameInteractiveShiftEnd, text="NAHRÁT FAKTURU/ÚČTENKU", 
                                  bg=light_blue, fg=light_text_color, border=2, borderwidth=2,
                                    padx=15, command=lambda: self.UploadAction())
        self.btnSaveInovice.grid(column=1, row=0, rowspan=2,
                                 padx=(170,0), pady=(15,0),
                                 sticky="wn")
        # Function that creates the Info labels in the shift end
        self.CreateShiftEndInfo()

        # Function, that creates the form for shift end
        self.CreateForm()


    # Creates the History of Orders preview with the CanvaFrame method
    def CreateHistoryOrdersPage(self):

        #-- Canvas Scrollbar
        self.canvas = Canvas(self.frameHistoryOrders, bg=background_color_ternary)
        self.scrollbar = Scrollbar(self.frameHistoryOrders, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = Frame(self.canvas, bg=background_color_ternary)

        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # -Binding of scrollbar
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=(0, 0, self.canvas.bbox("all")[2], self.canvas.bbox("all")[3])
            )
        )

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_active)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_active)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_active)


        self.canvas.pack(side="left", fill="both", expand=1)
        self.scrollbar.pack(side="right", fill="y", ipadx=8)

        # Creating the once header row Label
        self.CreateHeaderRow()

        # Creating the record Labels with the Orders
        for index, order in enumerate(loadOrders()):
            self.CreateOrderRow(order, index)


    def CreateHeaderRow(self):
        
        # Header titles
        headers = ["Přijato", "Stav objednávky", "Objednávka", "Zákazník"]
        widthColumn = int(self.screen_width/105)
        self.column_widths = [int(widthColumn*1.5), int(widthColumn*2), int(widthColumn*4), int(widthColumn*2.5)]

        # Main header Frame 
        header_frame = Frame(self.scrollable_frame, bg=background_color_primary, padx=5, pady=5)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        # Placing the Label titles in the Frame
        for col, text in enumerate(headers):
            label = Label(header_frame, text=text, font=("Helvetica", 14, "bold"), 
                        bg=background_color_primary, fg=light_text_color, width=self.column_widths[col], anchor="w")
            label.grid(row=0, column=col, padx=5, pady=2, sticky="w")

    def ChangeDelivery(self, delivery_name, order_id):
        origin_delivery = ""
        changed_order = ""
        orders = loadOrders()
        for order in orders:
            if order["id"] == order_id:
                origin_delivery = order["delivery"]
                changed_order = order
                break

        if origin_delivery == "" or origin_delivery == "Neznámý" or changed_order == "":
            return

        self.SetDelivery(delivery_name, order_id)

        if origin_delivery == "Bistro":
            self.varTakeAwaySum.set(self.varTakeAwaySum.get() - int(changed_order["total_price"].replace("Kč", "").strip())) 
        else:
            self.varDictDeliveries[int(origin_delivery[1])].set(self.varDictDeliveries[int(origin_delivery[1])].get() - int(changed_order["total_price"].replace("Kč", "").strip())) 

        self.varFinalSum.set(self.varFinalSum.get() - int(changed_order["total_price"].replace("Kč", "").strip()))

        self.UpdateFramesList()

    def create_context_menu(self, row_frame, order):

        def show_context_menu(event):

            if hasattr(self, "context_menu"):
                self.context_menu.destroy()

            self.context_menu = Menu(self.frameHistoryOrders, tearoff=0)
            self.context_menu.config(font=("Helvetica", 22), bg=background_color_ternary)
            self.context_menu.add_command(label="Tisk objednávky", command=lambda: self.PrintOrder())

            # Create a submenu for delivery change
            delivery_menu = Menu(self.context_menu, tearoff=0)
            delivery_menu.config(font=("Helvetica", 20))
            delivery_options = ["R1", "R2", "R3", "R4", "R5", "R6", "Bistro"]
            for delivery in delivery_options:
                delivery_menu.add_command(label=delivery, command=partial(self.ChangeDelivery, delivery, order["id"]))

            self.context_menu.add_cascade(label="Změnit rozvoz", menu=delivery_menu)

            # Show the menu x and y by clik
            self.context_menu.post(event.x_root, event.y_root)

        # Binding
        row_frame.bind("<Button-3>", show_context_menu)
        for widget in row_frame.winfo_children():
            widget.bind("<Button-3>", show_context_menu)


    # Creating one record of the Order which is written in the history
    def CreateOrderRow(self, order, index):

        bg_color = order_row_color

        row_frame = Frame(self.scrollable_frame, bg=bg_color, padx=5, pady=5)
        row_frame.grid(row=(index+1)*2, column=0, columnspan=4, sticky="ew")

        self.create_context_menu(row_frame, order)

        # Column 1: Date
        date_time_order = f"{order["datetime"].split()[0]} - {order["datetime"].split()[1]}"
        datetime_label = Label(row_frame, text=date_time_order, font=("Helvetica", 16), bg=bg_color, anchor="w", width=23)
        datetime_label.grid(row=0, column=0, padx=(5,0), pady=2, sticky="ew", ipady=60)

        # Column 2: State
        status_price_text = f"Stav: {order['status']}\nCelkem cena: {order['total_price']}\nDoprava: {order['delivery']}"
        status_price_label = Label(row_frame, text=status_price_text, font=("Helvetica", 16), bg=bg_color, width=29, justify=LEFT,
                                   anchor="w")
        status_price_label.grid(row=0, column=1, pady=2, padx=(6,0), sticky="ew")

        # Column 3: Order
        items_text = "\n".join(f" • {p['name']} ({p['price']})" for p in order["products"])
        items_label = Label(row_frame, text=items_text, font=("Helvetica", 16), bg=bg_color, justify=LEFT, anchor="w", width=61)
        items_label.grid(row=0, column=2, pady=16, padx=(14,4), sticky="ew")

        # Column 4: Customer
        customer_info = f"{order['customer']['name']}\n{order['customer']['address']}\nTel.: {order['customer']['phone']}\nCena: {order['total_price']}"
        customer_label = Label(row_frame, text=customer_info, font=("Helvetica", 16), bg=bg_color, justify=LEFT, anchor="w", wraplength=200)
        customer_label.grid(row=0, column=3, pady=2, sticky="ew")

        for widget in row_frame.winfo_children():
            widget.bind("<Button-3>", lambda event: self.create_context_menu(row_frame, order))

        separator = Frame(self.scrollable_frame, height=3, bg=dark_text_color)
        separator.grid(row=(index+1)*2+1, column=0, columnspan=4, sticky="ew")


    # Creates the Active Order page preview with the CanvaFrame method
    def CreateActiveOrdersPage(self):
        
        self.activeCanvas = Canvas(self.frameActiveOrders, bg=background_color_primary)
        self.activeScrollbar = Scrollbar(self.frameActiveOrders, orient="vertical", command=self.activeCanvas.yview)
        self.activeCanvas.configure(yscrollcommand=self.activeScrollbar.set)

        self.active_scrollable_frame = Frame(self.activeCanvas, bg=background_color_ternary)

        self.window_id = self.activeCanvas.create_window((0, 0), window=self.active_scrollable_frame, anchor="nw")

        # Binding of events
        self.active_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.activeCanvas.configure(
                scrollregion=(0, 0, self.activeCanvas.bbox("all")[2], self.activeCanvas.bbox("all")[3])
            )
        )
        self.activeCanvas.bind_all("<MouseWheel>", self._on_mousewheel_active)
        self.activeCanvas.bind_all("<Button-4>", self._on_mousewheel_active)
        self.activeCanvas.bind_all("<Button-5>", self._on_mousewheel_active)


        self.activeCanvas.pack(side="left", fill="both", expand=1)
        self.activeScrollbar.pack(side="right", fill="y", ipadx=8)

        self.CreateActiveHeaderRow()

        orders = loadOrders()
        
        sorted_orders = sorted(orders, key=lambda order: (order.get('status') != "Neověřeno", order.get('delivery') == "Neznámý"))

        # On the page the Not verified orders will be first and after them the verified
        for index, order in enumerate(sorted_orders):
            if order['status'] == "Neověřeno" or (order['status'] == "Ověřeno" and order['delivery'] == "Neznámý"):
                self.CreateActiveOrderRow(order, index)

    def CreateActiveHeaderRow(self):
        
        # Header titles
        headers = ["Přijato", "Objednávka", "Stav doručení", "Zákazník", "Volby"]
        widthColumn = int(self.screen_width/105)
        self.column_widths = [int(widthColumn*1.3), int(widthColumn*3.4), int(widthColumn*1.8), int(widthColumn*1.8), int(widthColumn*1.7)]

        # Main header Frame 
        header_frame = Frame(self.active_scrollable_frame, bg=background_color_primary, padx=5, pady=5)
        header_frame.grid(row=0, column=0, columnspan=5, sticky="ew")

        # Placing the Label titles in the Frame
        for col, text in enumerate(headers):
            label = Label(header_frame, text=text, font=("Helvetica", 14, "bold"), 
                        bg=background_color_primary, fg=light_text_color, width=self.column_widths[col], anchor="w")
            label.grid(row=0, column=col, padx=5, pady=2, sticky="w")


    # Creating one record of the Order with which can be manipulated
    def CreateActiveOrderRow(self, order, index):

        # Diversification of the Verified and not verified Orders
        if order["status"] == "Neověřeno":
            bg_color = light_red
        else:
            bg_color = light_green
        

        # One row Frame
        row_frame = Frame(self.active_scrollable_frame, bg=bg_color, padx=5, pady=5)
        row_frame.grid(row=(index+1)*2, column=0, columnspan=5, sticky="ew", ipady=10)
        row_frame.grid_rowconfigure(0, weight=1)


        # The values which are in the row Frame
        date_time_order = f"{order['datetime'].split()[0]}\n\n   {order['datetime'].split()[1]}"
        datetime_label = Label(row_frame, text=date_time_order, font=("Helvetica", 16), bg=bg_color, anchor="w", width=17)
        datetime_label.grid(row=0, column=0, padx=(5, 0), pady=(10, 10), sticky="nsw")

        status_price_text = f"Stav: {order['status']}\nCelkem cena: {order['total_price']}\nDoprava: {order['delivery']}"
        status_price_label = Label(row_frame, text=status_price_text, font=("Helvetica", 16), bg=bg_color, width=26, justify=LEFT, anchor="w")
        status_price_label.grid(row=0, column=2, pady=(10, 10), padx=(1, 13), sticky="nsw")

        items_text = "\n".join(f" • {p['name']} ({p['price']})" for p in order["products"])
        items_label = Label(row_frame, text=items_text, font=("Helvetica", 16), bg=bg_color, justify=LEFT, anchor="w", width=52)
        items_label.grid(row=0, column=1, pady=(10, 10), padx=(33, 1), sticky="nsw")

        customer_info = f"{order['customer']['name']}\n{order['customer']['address']}\nTel.: {order['customer']['phone']}\nCena: {order['total_price']}"
        customer_label = Label(row_frame, text=customer_info, font=("Helvetica", 16), bg=bg_color, justify=LEFT, anchor="w", width=27, wraplength=250)
        customer_label.grid(row=0, column=3, pady=(10, 10), padx=(2,7), sticky="nsw")

        self.lblButtons = Frame(row_frame, bg=bg_color)
        self.lblButtons.grid(row=0, column=4, pady=(10, 10), sticky="nsw")

        self.lblButtons.grid_rowconfigure(0, weight=1)
        self.lblButtons.grid_rowconfigure(1, weight=1)
        self.lblButtons.grid_rowconfigure(2, weight=1)

        btn_verify = Button(self.lblButtons, width=15, text="")
        btn_verify.grid(column=0, row=0, pady=(5, 5))

        # Diversification of the interactions on button clicks
        # Not in the start of the function 'cause new status could 
        # Be added in future and the extension will be easier
        if order['status'] == "Ověřeno":
            btn_verify.config(text="HOTOVO", command=lambda: self.FinishOrder(order["id"]))
        elif order['status'] == "Neověřeno":
            btn_verify.config(text="OVĚŘIT", command=lambda: self.VerifyOrder(btn_verify, order["id"]))

        self.btnCancel = Button(self.lblButtons, width=15, text="STORNO", command=lambda: self.CancelOrder(order["id"]))
        self.btnCancel.grid(column=0, row=1, pady=(5, 5))

        self.btnPrint = Button(self.lblButtons, width=15, text="TISK", command=self.PrintOrder)
        self.btnPrint.grid(column=0, row=2, pady=0)

        # Frame that is used as the separator of the orders, The Separator component
        # isn't used, cause I am using the the .grid placement and using the Frame
        # is simplier.
        separator = Frame(self.active_scrollable_frame, height=3, bg=dark_text_color)
        separator.grid(row=(index+1)*2+1, column=0, columnspan=5, sticky="ew")


    # When the new Order is added, the page should refresh and the new Order should
    # display, the jl' is on page:
    # - Active Orders - Canvas is destroyed and displayed again
    # - History of Orders - Order is added
    # - Labels in the Shift end - the variables are updated
    def UpdateFramesList(self):
        self.frameActiveOrders.destroy()

        self.frameActiveOrders = ttk.Frame(self.notebook)
        self.frameActiveOrders.pack()
        self.notebook.insert(0, self.frameActiveOrders, text="Aktivní objednávky")

        self.CreateActiveOrdersPage()

        self.notebook.select(self.frameActiveOrders)

        sorted_orders = sorted(
            loadOrders(),
            key=lambda order: (order['status'] != "Neověřeno", order['delivery'] == "Neznámý")
        )

        for index, order in enumerate(sorted_orders):
            if order['status'] == "Neověřeno" or (order['status'] == "Ověřeno" and order['delivery'] == "Neznámý"):
                self.CreateActiveOrderRow(order, index)

        for index, order in enumerate(loadOrders()):
            self.CreateOrderRow(order, index)

        self.activeCanvas.configure(scrollregion=self.activeCanvas.bbox("all"))

        for widget in self.frameDeliveries.winfo_children():
            widget.destroy()

        self.lblAllDeliveriesInfo = Label(self.frameDeliveries, text="Rozdělení podle rozvozců:")
        self.lblAllDeliveriesInfo.configure(font="Helvetica 16 bold")
        self.lblAllDeliveriesInfo.grid(column=0, row=0, columnspan=2, sticky="nw", padx=0, pady=(15, 2))

        for key, value in self.varDictDeliveries.items():
            if value.get() > 0:
                Label(self.frameDeliveries, text=f"R{key} - {value.get()}Kč").grid(column=0, row=key, sticky="w")
                #Label(self.frameDeliveries, text=f"R{key}").grid(column=0, row=key, sticky="w")
                #Label(self.frameDeliveries, text=f"{value.get()}Kč").grid(column=1, row=key, sticky="w")
            
        if self.varTakeAwaySum.get() > 0:
            Label(self.frameDeliveries ,text=f"Bistro - {self.varTakeAwaySum.get()}Kč").grid(column=0, row=8, sticky="w")
            #Label(self.frameDeliveries ,text=f"Take away").grid(column=0, row=8, sticky="w")
            #Label(self.frameDeliveries ,text=f"{self.varTakeAwaySum.get()}Kč").grid(column=1, row=8, sticky="w")

        self.valueSumAll.config(text=str(self.varDailyPrice.get()) + " Kč")
        self.valueSumDone.config(text=str(self.varFinalSum.get()) + " Kč")

        self.valueDateTo.config(text=str(self.varDateLastOrder.get()))
        self.valueNumOfOrders.config(text=str(self.varOrderNum.get()))

    def SetDelivery(self, delivery_name, order_id):
        """Sets the delivery method and updates the order."""
        
        orders = loadOrders()
        for order in orders:
            if order["id"] == order_id:
                order["status"] = "Hotovo"
                order["delivery"] = delivery_name
                break
        
        if delivery_name == "Bistro":
            self.varTakeAwaySum.set(self.varTakeAwaySum.get() + int(order["total_price"].replace("Kč", "").strip())) 
        else:
            self.varDictDeliveries[int(delivery_name[1])].set(self.varDictDeliveries[int(delivery_name[1])].get() + int(order["total_price"].replace("Kč", "").strip())) 

        self.varFinalSum.set(self.varFinalSum.get() + int(order["total_price"].replace("Kč", "").strip()))

        with open("orders.json", "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        self.active_scrollable_frame.update()
        self.UpdateFramesList()

    # Function for Finishing the Order in simplier term the Delivery success
    def FinishOrder(self, order_id):

        # Creating the new smaller window for options of the deliveries and the take away
        # After the button click is the delivery assigned and Order finished.
        # It disappears from the Active Orders, but it is still in the History of Orders
        self.finish_window = Toplevel(self.frameHistoryOrders, bg=order_row_color)
        self.finish_window.title("Vyberte druh rozvozu")
        self.finish_window.geometry("800x400")

        self.finish_window.grab_set()
        self.finish_window.focus_set()
        self.finish_window.transient(self.frameHistoryOrders)

        self.finish_window.update_idletasks()
        win_width = self.finish_window.winfo_width()
        win_height = self.finish_window.winfo_height()
        screen_width = self.finish_window.winfo_screenwidth()
        screen_height = self.finish_window.winfo_screenheight()
        x_position = (screen_width // 2) - (800 // 2)
        y_position = (screen_height // 2) - (400 // 2)
        self.finish_window.geometry(f"800x400+{x_position}+{y_position}")

        Label(self.finish_window, text="Vyberte druh rozvozu:", font=("Helvetica", 14, "bold"), bg=order_row_color).grid(
            row=0, column=0, columnspan=3, sticky="ew", pady=10
        )

        self.leftFrameWin = Frame(self.finish_window, bg=order_row_color)
        self.leftFrameWin.grid(row=1, column=0, padx=(30, 0), pady=10, sticky="nsew")

        separator = Frame(self.finish_window, bg=dark_text_color, width=2)
        separator.grid(row=1, column=1, sticky="ns", padx=(25, 0), pady=2)

        self.rightFrameWin = Frame(self.finish_window, bg=order_row_color)
        self.rightFrameWin.grid(row=1, column=2, padx=(30, 0), pady=10, sticky="nsew")

        self.leftFrameWin.grid_columnconfigure(0, weight=1)
        self.rightFrameWin.grid_columnconfigure(0, weight=1)
        self.rightFrameWin.grid_columnconfigure(1, weight=1)

        Button(self.rightFrameWin, text="R1", font=("Helvetica", 16), width=15, height=2, 
            command=lambda d="R1": (self.SetDelivery(d, order_id), self.finish_window.destroy()), bg=background_color_ternary
        ).grid(column=0, row=0, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R2", font=("Helvetica", 16), width=15, height=2, command=lambda d="R2": (self.SetDelivery(d, order_id), self.finish_window.destroy()), bg=background_color_ternary).grid(column=1, row=0, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R3", font=("Helvetica", 16), width=15, height=2, command=lambda d="R3": (self.SetDelivery(d, order_id), self.finish_window.destroy()), bg=background_color_ternary).grid(column=0, row=1, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R4", font=("Helvetica", 16), width=15, height=2, command=lambda d="R4": (self.SetDelivery(d, order_id), self.finish_window.destroy()), bg=background_color_ternary).grid(column=1, row=1, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R5", font=("Helvetica", 16), width=15, height=2, command=lambda d="R5": (self.SetDelivery(d, order_id), self.finish_window.destroy()), bg=background_color_ternary).grid(column=0, row=2, padx=5, pady=(30, 0))
        Button(self.rightFrameWin, text="R6", font=("Helvetica", 16), width=15, height=2, command=lambda d="R6": (self.SetDelivery(d, order_id), self.finish_window.destroy()), bg=background_color_ternary).grid(column=1, row=2, padx=5, pady=(30, 0))

        # Separated button for take away delivery
        Button(self.leftFrameWin, text="Odběr na\nbistru", font=("Helvetica", 16), width=15, height=2, command=lambda d="Bistro": (self.SetDelivery(d, order_id), self.finish_window.destroy()), bg=background_color_ternary).grid(row=0, column=0, padx=5, pady=116)

        self.finish_window.grid_columnconfigure(0, weight=1)
        self.finish_window.grid_columnconfigure(1, weight=0)
        self.finish_window.grid_columnconfigure(2, weight=1)
        self.finish_window.grid_rowconfigure(1, weight=1)


    # Verifying the order and changing the button setup
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

    #Canceling the Order and moving it into History of Orders as cancelled
    def CancelOrder(self, order_id):

        orders = loadOrders()
        res = msg.askquestion("Zrušit objednávku", "Opravdu chcete objednávku stornovat?")
        
        if res == "no" : return

        for order in orders:
            if order["id"] == order_id:
                order["status"] = "Zrušeno"
                order["delivery"] = "Nedoručeno"
                break
        
        with open("orders.json", "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        self.UpdateFramesList()

    def PrintOrder(self):
        msgInfo = msg.showinfo("Tisk Objednavky...", "Tisk probiha odsouhlaste tlacitkem")
        pass

root = Tk()

app = OrderApp(root)
root.mainloop()