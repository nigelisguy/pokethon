import tkinter as tk
from tkinter import ttk, filedialog
import json
import copy

TILE_SIZE = 24

TILES = [
    "empty", "grass", "water", "hill",
    "tree", "cut_tree", "npc", "item",
    "legendary", "spawn", "door"
]

BASE_COLORS = {
    "empty": "#ffffff",   
    "grass": "#2ecc71",
    "water": "#3498db",
    "hill": "#8e5a2b",
    "tree": "#145a32",
    "cut_tree": "#6b4226",
    "npc": "#9b59b6",
    "item": "#f1c40f",
    "legendary": "#e74c3c",
    "spawn": "#ffd700",
    "door": "#95a5a6",
}

DISPLAY = {
    "empty": "",
    "grass": "#",
    "water": "~",
    "hill": "",  # handled separately with arrows
    "tree": "⬜",
    "cut_tree": "▲",
    "npc": "☺",
    "item": "●",
    "legendary": "M",
    "spawn": "@",
    "door": "D",
}


class MapData:
    def __init__(self, w=80, h=10):
        self.width = w
        self.height = h

        self.spawn = (0, 0)

        self.grass_tiles = set()
        self.water_tiles = set()
        self.tree_tiles = set()
        self.cut_trees = set()

        self.hill_tiles = {}
        self.npcs = {}
        self.items = {}
        self.legendary_mons = {}
        self.doors = {}


class Editor:
    def __init__(self, root):
        self.root = root

        self.maps = {"map1": MapData()}
        self.current_map = "map1"

        self.mode = tk.StringVar(value="grass")

        self.undo = []
        self.redo = []

        self.door_buffer = None
        self.selected = None
        self.drag = False

        self.build_ui()
        self.build_canvas()
        self.draw()

    def build_ui(self):
        top = tk.Frame(self.root)
        top.pack(side=tk.TOP, fill=tk.X)

        self.map_name_entry = tk.Entry(top, width=10)
        self.map_name_entry.insert(0, "map1")
        self.map_name_entry.pack(side=tk.LEFT)

        tk.Button(top, text="Rename Map", command=self.rename_map).pack(side=tk.LEFT)

        self.w_var = tk.StringVar(value="80")
        self.w_entry = ttk.Combobox(
            top,
            textvariable=self.w_var,
            values=[str(i) for i in range(1, 81)],
            width=5,
            state="readonly"
        )
        self.w_entry.pack(side=tk.LEFT)

        self.h_var = tk.StringVar(value="10")
        self.h_entry = ttk.Combobox(
            top,
            textvariable=self.h_var,
            values=[str(i) for i in range(1, 11)],
            width=5,
            state="readonly"
        )
        self.h_entry.pack(side=tk.LEFT)

        tk.Button(top, text="Resize Map", command=self.resize_map).pack(side=tk.LEFT)
        ttk.Combobox(top, textvariable=self.mode, values=TILES, state="readonly").pack(side=tk.LEFT)
        tk.Button(top, text="Undo", command=self.undo_action).pack(side=tk.LEFT)
        tk.Button(top, text="Redo", command=self.redo_action).pack(side=tk.LEFT)
        tk.Button(top, text="Save", command=self.save).pack(side=tk.LEFT)
        self.load_text = tk.Text(top, height=3, width=40)
        self.load_text.pack(side=tk.LEFT)

        tk.Button(top, text="Load Text", command=self.load_from_text).pack(side=tk.LEFT)
        tk.Button(top, text="Export", command=self.export).pack(side=tk.LEFT)
        tk.Button(top, text="New Map", command=self.new_map).pack(side=tk.LEFT)

        self.inspector = tk.Frame(self.root, width=240, bg="#222")
        self.inspector.pack(side=tk.RIGHT, fill=tk.Y)

        self.info = tk.Label(self.inspector, text="No selection", fg="white", bg="#222")
        self.info.pack(pady=10)

        self.preview = tk.Canvas(self.inspector, width=100, height=100, bg="#111")
        self.preview.pack(pady=10)

        self.hill_frame = tk.Frame(self.inspector, bg="#222")
        self.npc_frame = tk.Frame(self.inspector, bg="#222")
        self.legend_frame = tk.Frame(self.inspector, bg="#222")
        self.item_frame = tk.Frame(self.inspector, bg="#222")
        self.door_frame = tk.Frame(self.inspector, bg="#222")
        tk.Label(self.door_frame, text="Door Editor", fg="white", bg="#222").pack(pady=5)

        self.door_map_entry = tk.Entry(self.door_frame)
        self.door_map_entry.pack()

        self.door_y_entry = tk.Entry(self.door_frame, width=5)
        self.door_y_entry.pack()

        self.door_x_entry = tk.Entry(self.door_frame, width=5)
        self.door_x_entry.pack()

        self.save_door_btn = tk.Button(
            self.door_frame,
            text="Save Door",
            command=self.save_door
        )
        self.save_door_btn.pack(pady=5)
        self.door_map_entry.bind("<Return>", lambda e: self.save_door())
        self.door_y_entry.bind("<Return>", lambda e: self.save_door())
        self.door_x_entry.bind("<Return>", lambda e: self.save_door())

        self.dialog_label = tk.Label(self.npc_frame, text="NPC Dialogue", fg="white", bg="#222")
        self.dialog_label.pack(pady=5)

        self.dialog_entry = tk.Text(self.npc_frame, height=6, width=25)
        self.dialog_entry.pack(pady=5)

        self.save_dialog_btn = tk.Button(
            self.npc_frame,
            text="Save NPC Dialogue",
            command=self.save_npc_dialogue
        )
        self.save_dialog_btn.pack(pady=5)
        self.dialog_entry.bind("<Return>", lambda e: (self.save_npc_dialogue(), "break"))
        self.hill_dir_var = tk.StringVar(value="up")
        self.hill_menu = ttk.Combobox(
            self.hill_frame,
            textvariable=self.hill_dir_var,
            values=["up", "right", "down", "left"],
            state="readonly"
        )
        self.hill_menu.pack(pady=5)

        self.save_hill_btn = tk.Button(
            self.hill_frame,
            text="Set Hill Direction",
            command=self.save_hill_direction
        )
        self.save_hill_btn.pack(pady=5)
        self.hill_menu.bind("<Return>", lambda e: self.save_hill_direction())
        tk.Label(self.legend_frame, text="Legendary Pokémon", fg="white", bg="#222").pack(pady=5)

        self.legend_name = tk.Entry(self.legend_frame)
        self.legend_name.insert(0, "Mewtwo")
        self.legend_name.pack()

        self.legend_level = tk.Entry(self.legend_frame)
        self.legend_level.insert(0, "50")
        self.legend_level.pack()

        self.save_legend_btn = tk.Button(
            self.legend_frame,
            text="Save Legendary",
            command=self.save_legendary
        )
        self.save_legend_btn.pack(pady=5)
        self.legend_name.bind("<Return>", lambda e: self.save_legendary())
        self.legend_level.bind("<Return>", lambda e: self.save_legendary())
        tk.Label(self.item_frame, text="Item Editor", fg="white", bg="#222").pack(pady=5)

        self.item_id = tk.Entry(self.item_frame)
        self.item_id.insert(0, "potion")
        self.item_id.pack()

        self.item_qty = tk.Entry(self.item_frame)
        self.item_qty.insert(0, "1")
        self.item_qty.pack()

        self.save_item_btn = tk.Button(
            self.item_frame,
            text="Save Item",
            command=self.save_item
        )
        self.save_item_btn.pack(pady=5)
        self.item_id.bind("<Return>", lambda e: self.save_item())
        self.item_qty.bind("<Return>", lambda e: self.save_item())
    def build_canvas(self):
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="black")
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set)

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag_move)
        self.canvas.bind("<ButtonRelease-1>", self.release)

    def cur(self):
        return self.maps[self.current_map]

    def switch_map(self, e):
        self.current_map = self.map_select.get()
        self.draw()

    def new_map(self):
        name = f"map{len(self.maps)+1}"
        self.maps[name] = MapData()
        self.map_label.config(text=name)
        self.current_map = name
        self.draw()

    def pos(self, e):
        return e.y // TILE_SIZE, e.x // TILE_SIZE

    def click(self, e):
        self.drag = True
        self.apply(e)

    def drag_move(self, e):
        if self.drag:
            self.apply(e)

    def release(self, e):
        self.drag = False

    def apply(self, e):
        m = self.cur()
        y, x = self.pos(e)

        if not (0 <= y < m.height and 0 <= x < m.width):
            return

        self.push_undo()
        self.selected = (y, x)

        mode = self.mode.get()

        for s in [m.grass_tiles, m.water_tiles, m.tree_tiles, m.cut_trees]:
            s.discard((y, x))
        m.npcs.pop((y, x), None)
        m.items.pop((y, x), None)
        m.legendary_mons.pop((y, x), None)
        m.doors.pop((y, x), None)

        if mode == "spawn":
            m.spawn = (y, x)

        elif mode == "grass":
            m.grass_tiles.add((y, x))

        elif mode == "water":
            m.water_tiles.add((y, x))

        elif mode == "tree":
            m.tree_tiles.add((y, x))

        elif mode == "cut_tree":
            m.cut_trees.add((y, x))

        elif mode == "hill":
            dirs = ["up", "right", "down", "left"]
            cur = m.hill_tiles.get((y, x), "up")
            m.hill_tiles[(y, x)] = dirs[(dirs.index(cur) + 1) % 4] if cur in dirs else "up"

        elif mode == "npc":
            m.npcs[(y, x)] = ("☺", ["hello", "..."])

        elif mode == "item":
            m.items[(y, x)] = ("item", 1)

        elif mode == "legendary":
            m.legendary_mons[(y, x)] = {
                "name": "Mewtwo",
                "mon_id": 150,
                "level": 50,
                "moves": [340, 340, 340, 340]
            }

        elif mode == "door":
            if self.door_buffer is None:
                self.door_buffer = (self.current_map, y, x)
            else:
                src_map, sy, sx = self.door_buffer
                m.doors[(sy, sx)] = (self.current_map, y, x)
                self.door_buffer = None

        self.update_inspector()
        self.draw()

    def update_inspector(self):
        if not self.selected:
            return

        m = self.cur()
        y, x = self.selected

        tile = "empty"
        if (y, x) in m.grass_tiles: tile = "grass"
        elif (y, x) in m.water_tiles: tile = "water"
        elif (y, x) in m.tree_tiles: tile = "tree"
        elif (y, x) in m.cut_trees: tile = "cut_tree"
        elif (y, x) in m.npcs: tile = "npc"
        elif (y, x) in m.items: tile = "item"
        elif (y, x) in m.legendary_mons: tile = "legendary"
        elif (y, x) in m.hill_tiles: tile = "hill"
        elif (y, x) in m.doors: tile = "door"
        elif m.spawn == (y, x): tile = "spawn"

        self.info.config(text=f"Tile: {tile}\nPos: ({y},{x})")

        self.preview.delete("all")
        self.preview.create_rectangle(
            10, 10, 90, 90,
            fill=BASE_COLORS[tile],
            outline="white"
        )

        for f in [self.npc_frame, self.hill_frame, self.legend_frame, self.item_frame, self.door_frame]:
            try:
                f.pack_forget()
            except:
                pass

        if (y, x) in m.npcs:
            self.npc_frame.pack(pady=5)
            self.dialog_entry.delete("1.0", tk.END)
            dialogue = m.npcs[(y, x)][1]
            self.dialog_entry.insert(tk.END, "\n".join(dialogue))

        elif (y, x) in m.hill_tiles:
            self.hill_frame.pack(pady=5)
            self.hill_dir_var.set(m.hill_tiles[(y, x)])

        elif (y, x) in m.legendary_mons:
            self.legend_frame.pack(pady=5)

            data = m.legendary_mons[(y, x)]
            self.legend_name.delete(0, tk.END)
            self.legend_name.insert(0, data.get("name", ""))

            self.legend_level.delete(0, tk.END)
            self.legend_level.insert(0, str(data.get("level", 1))) 
            if "moves" not in data:
                data["moves"] = [340, 340, 340, 340]

        elif (y, x) in m.items:
            self.item_frame.pack(pady=5)

            data = m.items[(y, x)]
            self.item_id.delete(0, tk.END)
            self.item_id.insert(0, data[0])

            self.item_qty.delete(0, tk.END)
            self.item_qty.insert(0, str(data[1]))

        elif (y, x) in m.doors:
            self.door_frame.pack(pady=5)

            data = m.doors[(y, x)]
            self.door_map_entry.delete(0, tk.END)
            self.door_map_entry.insert(0, data[0])

            self.door_y_entry.delete(0, tk.END)
            self.door_y_entry.insert(0, str(data[1]))

            self.door_x_entry.delete(0, tk.END)
            self.door_x_entry.insert(0, str(data[2]))


    def save_npc_dialogue(self):
        if not self.selected:
            return

        m = self.cur()
        y, x = self.selected

        if (y, x) in m.npcs:
            text = self.dialog_entry.get("1.0", tk.END).strip().split("\n")
            text = [line for line in text if line != ""]
            sprite = m.npcs[(y, x)][0]
            m.npcs[(y, x)] = (sprite, text)

        self.draw()


    def save_hill_direction(self):
        if not self.selected:
            return

        m = self.cur()
        y, x = self.selected

        m.hill_tiles[(y, x)] = self.hill_dir_var.get()
        self.draw()

    def save_legendary(self):
        if not self.selected:
            return

        m = self.cur()
        y, x = self.selected

        if (y, x) in m.legendary_mons:
            old = m.legendary_mons[(y, x)]
            m.legendary_mons[(y, x)] = {
                "name": self.legend_name.get(),
                "mon_id": old.get("mon_id", 150),
                "level": int(self.legend_level.get()),
                "moves": old.get("moves", [340, 340, 340, 340])
            }

        self.draw()

    def save_item(self):
        if not self.selected:
            return

        m = self.cur()
        y, x = self.selected

        if (y, x) in m.items:
            m.items[(y, x)] = (
                self.item_id.get(),
                int(self.item_qty.get())
            )

        self.draw()

    def save_door(self):
        if not self.selected:
            return

        m = self.cur()
        y, x = self.selected

        if (y, x) in m.doors:
            try:
                m.doors[(y, x)] = (
                    self.door_map_entry.get(),
                    int(self.door_y_entry.get()),
                    int(self.door_x_entry.get())
                )
            except:
                pass

        self.draw()

    def rename_map(self):
        new_name = self.map_name_entry.get()

        if not new_name or new_name in self.maps:
            return

        old_name = self.current_map

        self.maps[new_name] = self.maps.pop(old_name)

        # update doors referencing old map name
        for m in self.maps.values():
            for k, v in list(m.doors.items()):
                target_map, ty, tx = v
                if target_map == old_name:
                    m.doors[k] = (new_name, ty, tx)

        self.current_map = new_name
        self.draw()

    def resize_map(self):
        try:
            w = min(80, max(1, int(self.w_entry.get())))
            h = min(10, max(1, int(self.h_entry.get())))

            m = self.cur()

            m.width = w
            m.height = h

            # Update UI dropdowns safely (locked readonly)
            self.w_var.set(str(w))
            self.h_var.set(str(h))

            # remove out-of-bounds tiles
            def clamp_set(s):
                return {(y, x) for (y, x) in s if y < h and x < w}

            m.grass_tiles = clamp_set(m.grass_tiles)
            m.water_tiles = clamp_set(m.water_tiles)
            m.tree_tiles = clamp_set(m.tree_tiles)
            m.cut_trees = clamp_set(m.cut_trees)

            m.npcs = {k: v for k, v in m.npcs.items() if k[0] < h and k[1] < w}
            m.items = {k: v for k, v in m.items.items() if k[0] < h and k[1] < w}
            m.legendary_mons = {k: v for k, v in m.legendary_mons.items() if k[0] < h and k[1] < w}
            m.hill_tiles = {k: v for k, v in m.hill_tiles.items() if k[0] < h and k[1] < w}
            m.doors = {k: v for k, v in m.doors.items() if k[0] < h and k[1] < w}

            self.draw()

        except:
            print("Invalid size")

    def draw(self):
        self.canvas.delete("all")
        m = self.cur()

        for y in range(m.height):
            for x in range(m.width):

                t = "empty"

                if (y, x) in m.grass_tiles: t = "grass"
                elif (y, x) in m.water_tiles: t = "water"
                elif (y, x) in m.tree_tiles: t = "tree"
                elif (y, x) in m.cut_trees: t = "cut_tree"
                elif (y, x) in m.npcs: t = "npc"
                elif (y, x) in m.items: t = "item"
                elif (y, x) in m.legendary_mons: t = "legendary"
                elif (y, x) in m.hill_tiles: t = "hill"
                elif (y, x) in m.doors: t = "door"
                elif m.spawn == (y, x): t = "spawn"

                self.canvas.create_rectangle(
                    x*TILE_SIZE, y*TILE_SIZE,
                    x*TILE_SIZE+TILE_SIZE,
                    y*TILE_SIZE+TILE_SIZE,
                    fill=BASE_COLORS[t],
                    outline="black"
                )
                # Draw symbol if exists
                symbol = DISPLAY.get(t, "")
                if symbol:
                    self.canvas.create_text(
                        x*TILE_SIZE + TILE_SIZE//2,
                        y*TILE_SIZE + TILE_SIZE//2,
                        text=symbol,
                        fill="black"
                    )

                if (y, x) in m.hill_tiles:
                    dir = m.hill_tiles[(y, x)]
                    arrows = {
                        "up": "↑",
                        "down": "↓",
                        "left": "←",
                        "right": "→",
                    }
                    self.canvas.create_text(
                        x*TILE_SIZE + TILE_SIZE//2,
                        y*TILE_SIZE + TILE_SIZE//2,
                        text=arrows.get(dir, "?"),
                        fill="white"
                    )
                if (y, x) in m.doors:
                    self.canvas.create_text(
                        x*TILE_SIZE+12,
                        y*TILE_SIZE+12,
                        text="→",
                        fill="black"
                    )

        # Update scroll region to allow full width viewing
        self.canvas.config(scrollregion=(0, 0, m.width * TILE_SIZE, m.height * TILE_SIZE))
        self.update_inspector()

    def push_undo(self):
        self.undo.append(copy.deepcopy(self.maps))
        self.redo.clear()

    def undo_action(self):
        if self.undo:
            self.redo.append(copy.deepcopy(self.maps))
            self.maps = self.undo.pop()
            self.draw()

    def redo_action(self):
        if self.redo:
            self.undo.append(copy.deepcopy(self.maps))
            self.maps = self.redo.pop()
            self.draw()

    def save(self):
        with open("project.json", "w") as f:
            json.dump(self.serialize(), f)

    def load(self):
        pass

    def load_from_text(self):
        try:
            data = json.loads(self.load_text.get("1.0", tk.END))
            self.maps = {}

            for name, m in data.items():
                new_map = MapData(m["width"], m["height"])
                new_map.spawn = tuple(m["spawn"])

                new_map.grass_tiles = set(tuple(t) for t in m.get("grass_tiles", []))
                new_map.water_tiles = set(tuple(t) for t in m.get("water_tiles", []))
                new_map.tree_tiles = set(tuple(t) for t in m.get("trees", []))
                new_map.cut_trees = set(tuple(t) for t in m.get("cut_trees", []))

                new_map.hill_tiles = {tuple(k): v for k, v in m.get("hill_tiles", {}).items()}
                new_map.npcs = {tuple(k): v for k, v in m.get("npcs", {}).items()}
                new_map.items = {tuple(k): v for k, v in m.get("items", {}).items()}
                new_map.legendary_mons = {tuple(k): v for k, v in m.get("legendary_mons", {}).items()}
                new_map.doors = {tuple(k): tuple(v) for k, v in m.get("doors", {}).items()}

                self.maps[name] = new_map

            self.current_map = list(self.maps.keys())[0]
            self.draw()

        except Exception as e:
            print("Invalid JSON:", e)
    
    def serialize(self):
        out = {}
        for name, m in self.maps.items():
            out[name] = {
                "width": m.width,
                "height": m.height,
                "spawn": m.spawn,
                "npcs": m.npcs,
                "grass_tiles": list(m.grass_tiles),
                "water_tiles": list(m.water_tiles),
                "hill_tiles": m.hill_tiles,
                "items": m.items,
                "cut_trees": list(m.cut_trees),
                "trees": list(m.tree_tiles),
                "legendary_mons": m.legendary_mons,
                "doors": m.doors
            }
        return out

    def export(self):
        print(self.serialize())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PokéTERMINAL Map GUI Editor (UNFINISHED)")
    app = Editor(root)
    root.mainloop()