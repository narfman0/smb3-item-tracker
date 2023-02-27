#!/usr/bin/env python3

import configparser
import tkinter as tk
from tkinter import messagebox

"""
[ page 1 ] x 7
[ page 2 ] x 7
[ page 3 ] x 7
[ page 4 ] x 7

[whistle] [star] [p-wing] [hammer] [music box] [cloud] [mushroom] [leaf]

"""


class Settings:
    def __init__(self):
        self.skip_prompts = False
        self.starting_item_strs = []
        try:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            self.skip_prompts = config.getboolean(
                "default", "skip_prompts", fallback=False
            )
            self.starting_item_strs = config.get("default", "starting_items").split(",")
        except Exception as e:
            # if the format is wonky or for whatever reason, lets just continue
            print(e)


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.settings = Settings()
        self.init_starting_items()

    def create_widgets(self):
        self.inventory = Inventory(self)
        self.item_selector = ItemSelector(self, self.inventory)

    def init_starting_items(self):
        for starting_item_str in self.settings.starting_item_strs:
            for item_button in self.item_selector.item_buttons:
                if item_button.item.name == starting_item_str:
                    item_button.clicked()


class Inventory(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.items = []
        self.rows = []
        self.create_widgets()

    def create_widgets(self):
        self.row1 = InventoryRow(self, 0)
        self.row2 = InventoryRow(self, 1)
        self.row3 = InventoryRow(self, 2)
        self.row4 = InventoryRow(self, 3)
        self.rows = [self.row1, self.row2, self.row3, self.row4]

    def add(self, item):
        if len(self.items) == 28:
            self.items.pop()
        self.items.append(item)
        self.refresh()

    def remove(self, id):
        self.items.pop(id)
        self.refresh()

    def clear(self):
        for row in self.rows:
            row.clear()
        self.items = []

    def refresh(self):
        for row in self.rows:
            row.clear()
        for i in range(len(self.items)):
            self.rows[i // 7].add(self.items[i])


class InventoryRow(tk.Frame):
    def __init__(self, master, id):
        super().__init__(master, width=266, height=38, bg="#FFD3CC")
        self.pack(side="top")
        self.grid_propagate(0)
        self.inventory = master
        self.id = id
        self.items = []

    def add(self, item):
        button = InventoryItemButton(self, item, len(self.items), (0, len(self.items)))
        self.items.append(button)

    def clear(self):
        for item in self.items:
            item.destroy()
        self.items = []

    def remove(self, item_id):
        self.inventory.remove((self.id * 7) + item_id)


class ItemSelector(tk.Frame):
    def __init__(self, master, inventory):
        super().__init__(master)
        self.pack(side="bottom")
        self.inventory = inventory
        self.create_buttons()

    def create_buttons(self):
        self.star = AddItemButton(self, Item("star"), (0, 0), self.inventory)
        self.pwing = AddItemButton(self, Item("pwing"), (0, 1), self.inventory)
        self.hammer = AddItemButton(self, Item("hammer"), (0, 2), self.inventory)
        self.musicbox = AddItemButton(self, Item("musicbox"), (0, 3), self.inventory)
        self.cloud = AddItemButton(self, Item("cloud"), (0, 4), self.inventory)
        self.whistle = AddItemButton(self, Item("whistle"), (0, 5), self.inventory)
        self.leaf = AddItemButton(self, Item("leaf"), (0, 6), self.inventory)
        self.mushroom = AddItemButton(self, Item("mushroom"), (1, 0), self.inventory)
        self.fireflower = AddItemButton(
            self, Item("fireflower"), (1, 1), self.inventory
        )
        self.frogsuit = AddItemButton(self, Item("frogsuit"), (1, 2), self.inventory)
        self.hammersuit = AddItemButton(
            self, Item("hammersuit"), (1, 3), self.inventory
        )
        self.tanukisuit = AddItemButton(
            self, Item("tanukisuit"), (1, 4), self.inventory
        )
        self.anchor = AddItemButton(self, Item("anchor"), (1, 5), self.inventory)
        self.item_buttons = [
            self.star,
            self.pwing,
            self.hammer,
            self.musicbox,
            self.cloud,
            self.whistle,
            self.leaf,
            self.mushroom,
            self.fireflower,
            self.frogsuit,
            self.hammersuit,
            self.tanukisuit,
            self.anchor,
        ]
        oof_img = tk.PhotoImage(file="img/oof.gif")
        self.clear = tk.Button(self, image=oof_img, command=self.clear_inventory)
        self.clear.image = oof_img
        self.clear.grid(row=1, column=6)

    def clear_inventory(self):
        if len(self.inventory.items) > 0:
            if self.master.settings.skip_prompts or messagebox.askokcancel(
                "Clear inventory?", "Are you sure? There is no undo."
            ):
                self.inventory.clear()
                self.master.init_starting_items()


class Item:
    def __init__(self, name):
        self.name = name
        self.img_small = tk.PhotoImage(file="img/" + name + ".gif")
        self.img_big = tk.PhotoImage(file="img/" + name + "big.gif")


class InventoryItemButton(tk.Button):
    def __init__(self, master, item, id, coords):
        super().__init__(
            master,
            image=item.img_big,
            relief=tk.FLAT,
            bg="#FFD3CC",
            command=self.clicked,
        )
        self.grid(row=coords[0], column=coords[1])
        self.row = master
        self.item = item
        self.id = id

    def clicked(self):
        """remove this item"""
        self.row.remove(self.id)


class AddItemButton(tk.Button):
    def __init__(self, master, item, coords, inventory):
        super().__init__(master, image=item.img_small, command=self.clicked)
        self.grid(row=coords[0], column=coords[1])
        self.item = item
        self.inventory = inventory

    def clicked(self):
        """send this item to the inventory"""
        self.inventory.add(self.item)


def quit():
    if not app.settings.skip_prompts and len(app.inventory.items) > 0:
        message = "Are you sure?\nAll your progress will be lost."
        if not messagebox.askokcancel("Quit?", message, icon="warning"):
            return
    root.destroy()


if __name__ == "__main__":
    global app
    root = tk.Tk()
    icon = tk.PhotoImage(file="img/6.gif")
    root.tk.call("wm", "iconphoto", root._w, icon)
    root.title("SMB3 Item Tracker")
    root.resizable(0, 0)
    app = App(master=root)
    root.protocol("WM_DELETE_WINDOW", quit)
    app.mainloop()
