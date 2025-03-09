# Vyskakovací menu, po stisknutí praveho tlačítka- Zadat objednavku a refresh


# -*- coding: utf-8 -*-
from tkinter import *
import json
from math import sqrt
from PIL import Image, ImageTk
from tkinter import messagebox as msg
import tkinter.font
from tkinter import ttk

def loadOrders():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: orders.json file not found.")
        return []


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
        self.varTakeAwaySum = IntVar(value = 0)
        self.varDeferment = IntVar(value = 0)
        self.varDictDeliveries = {"R1": IntVar(value = 0), "R2": IntVar(value = 0),
                                  "R3": IntVar(value = 0), "R4": IntVar(value = 0),
                                  "R5": IntVar(value = 0), "R6": IntVar(value = 0)
                                  }
        self.varCash = IntVar(value = 0)

        #Key bindings
        root.bind("<Escape>", lambda event: root.destroy()) 

        #Fonts
        self.def_font = tkinter.font.nametofont("TkDefaultFont")
        self.def_font.config(size=16)

        #Graphics functions
        self.CreateMainPageLayout(root)
        self.CreateNotebook()
        self.CreateShiftEndPage()
        self.CreateHistoryOrdersPage()
    def CreateMainPageLayout(self, root):
        #---Partitions of main page
        self.headerFrame = Frame(root)
        self.headerFrame.pack(side="top", fill="x", expand=1)
        self.headerFrame.configure(background="red", height=self.screen_height//25)
        self.mainFrame = Frame(root)
        self.mainFrame.pack(side="bottom", fill="both", expand=1)
        self.CreateHeaderLayout()

    def CreateHeaderLayout(self):
        #----Header what will be the same for all pages

        self.headerFrame.grid_columnconfigure(0, weight=1)
        self.headerFrame.grid_columnconfigure(1, weight=1)
        self.headerFrame.grid_columnconfigure(2, weight=1)

        self.btnCreateOrder = Button(self.headerFrame, text="MAKE ORDER")
        self.btnCreateOrder.grid(row=0, column=1, sticky="nswe")
        self.btnCreateOrder.configure(background="blue", width=self.screen_width//165)

        self.lblBranchName = Label(self.headerFrame, text="Bistro Olomouc")
        self.lblBranchName.grid(row=0, column=0, sticky="w", padx=(25,0))
        self.lblBranchName.configure(foreground="white")

        self.btnLogout = Button(self.headerFrame, text="Odhlasit se")
        self.btnLogout.grid(row=0, column=3, sticky="e", padx=(0, 10))
        self.btnLogout.configure(foreground="white")


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
        self.lblAllDeliveriesInfo.grid(column=0, row=0, sticky="nw", padx=0, pady=2)

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
        
        self.listOfDeliveryLabels = []

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

        self.entrySumExtraMoney = Entry(self.frameEndFormShiftEnd, width=20, textvariable=self.varDeferment, font=("Helvetica", 18))
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
        
        # Configure the grid to allow buttons to expand and fill space
        self.frameButtonsFormShiftEnd.grid_columnconfigure(0, weight=1)  # Left side
        self.frameButtonsFormShiftEnd.grid_columnconfigure(1, weight=1)  # Space in between
        self.frameButtonsFormShiftEnd.grid_columnconfigure(2, weight=1)  # Right side

        # --- COUNT Button (Left Side) ---
        self.btnCountEndShift = Button(self.frameButtonsFormShiftEnd, text="COUNT", width=10)
        self.btnCountEndShift.grid(column=2, row=1, sticky="nsew", padx=(0, 24))  # Expands to fill space
        self.btnCountEndShift.configure(command=self.CountEndShift)

        # --- SAVE Button (Right Side) ---
        self.btnSaveEndShift = Button(self.frameButtonsFormShiftEnd, text="SAVE", width=5)
        self.btnSaveEndShift.grid(column=0, row=1, sticky="nsew", padx=(10, 0))  # Expands to fill space
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
                entry.config(background="white", foreground="black")
            except ValueError:
                entry.config(background="red", foreground="white")
                return

        expenses = values["cards"] + values["food_cards"] + values["shopping"]

        if values["take_away_sum"] < expenses:
            for key in ["cards", "food_cards", "shopping"]:
                if values[key] > values["take_away_sum"]:
                    form_entry_fields[key].config(background="red", foreground="white")
                    # !!!!!!!!!!!!!!!!!!!! Do Some conversation block
                    # !!!!!!!!!!!!!!!!!!!!
                    # Work to do
        else:
            sum_with_deferment = values["take_away_sum"] - expenses
            if sum_with_deferment < 1000:
                self.varDeferment.set(sum_with_deferment)
                self.varCash.set(0)
            else:
                self.varDeferment.set(1000)
                self.varCash.set(sum_with_deferment - 1000)



    def CountEndShift(self):

        entry_fields = {
            "oSum": self.entrySumTakeAway,
            "cSum": self.entrySumCards,
            "fSum": self.entrySumFoodCards,
            "sSum": self.entrySumShopping
        }
        try:
            for key, entry in entry_fields.items():
                try:
                    int(entry.get())
                    entry.config(background="white", foreground="black")
                except ValueError:
                    entry.config(background="red", foreground="white")
        except:
            pass
        else:
            self.MakeFinalSum()

        


    def SaveEndShift(self):
        self.btnCountEndShift.config(text="EDIT", command=self.EditEndShiftForm)
        self.entrySumCards.config(state="disabled")
        self.entrySumExtraMoney.config(state="disabled")
        self.entrySumFoodCards.config(state="disabled")
        self.entrySumOfTakeAway.config(state="disabled")
        self.entrySumShopping.config(state="disabled")
        self.entrySumTakeAway.config(state="disabled")


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
                                  bg="lightblue", fg="white", border=2, borderwidth=2,
                                  padx=15)
        self.btnPrintEnd.grid(column=0, row=0, rowspan=2,
                              padx=(15, 0), pady=(15,10),
                              sticky="n")
        
        self.btnSaveInovice = Button(self.frameInteractiveShiftEnd, text="UPLOAD INOVICE", 
                                  bg="lightblue", fg="white", border=2, borderwidth=2,
                                    padx=15)
        self.btnSaveInovice.grid(column=1, row=0, rowspan=2,
                                 padx=(170,0), pady=(15,0),
                                 sticky="wn")
        self.CreateShiftEndInfo()
        self.CreateForm()

    def CreateTreeviewLayout(self):
        orders = loadOrders()

        for i, order in enumerate(orders):
            
            tagname = ""
            if i%2 == 0:
                tagname = "evenrow"
            else:
                tagname = "oddrow"
            
            
            products = ""
            datetimeOrder = order["datetime"].split()
            customer_details = (
                f"{order['customer']['name']}\n"
                f"{order['customer']['address']}\n"
                f"Tel.: {order['customer']['phone']}\n"
                f"Cena za jídlo: {order['total_price']}"
            )

            order_details = (
                f"Stav: {order['status']}\n"
                f"Celkem cena: {order['total_price']}\n"
                f"Doprava: {order['delivery']}"
            )

            for product in order["products"]:
                products += f" • {product['name']} ({product['price']})\n"

            self.tree.insert(
                "", "end", 
                values=(
                    f"{datetimeOrder[0]}\n{datetimeOrder[1]}",
                    order_details,
                    products,
                    customer_details
                ), 
                tags=tagname
            )

            

    def CreateHistoryOrdersPage(self):
        style = ttk.Style()
        style.configure("Treeview", rowheight=170)  # Increases row height
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

        # Create Treeview
        columns = ("Datum přijetí", "Status a cena", "Objednávka", "Zákazník")
        self.tree = ttk.Treeview(self.frameHistoryOrders, columns=columns, show="headings")
        self.tree.tag_configure("evenrow", background="white")
        self.tree.tag_configure("oddrow", background="lightgrey")


        # Define column headings
        self.tree.heading("Datum přijetí", text="Datum přijetí", anchor="w")
        self.tree.heading("Status a cena", text="Status a cena", anchor="w")
        self.tree.heading("Objednávka", text="Objednávka", anchor="w")
        self.tree.heading("Zákazník", text="Zákazník", anchor="w")

        # Adjust column widths for better spacing
        self.tree.column("Datum přijetí", width=100, anchor="w")
        self.tree.column("Status a cena", width=120, anchor="w")
        self.tree.column("Objednávka", width=500, anchor="w")
        self.tree.column("Zákazník", width=300, anchor="w")

        self.CreateTreeviewLayout()

        self.treeScrollbar = ttk.Scrollbar(self.frameHistoryOrders, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.treeScrollbar.set)
        self.treeScrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="both")



root = Tk()

app = OrderApp(root)
root.mainloop()