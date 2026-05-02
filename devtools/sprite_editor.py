import tkinter as tk
import copy
import ast

WIDTH = 25
HEIGHT = 11
CELL_W = 18
CELL_H = 36

# Approximate curses → hex
CURSES_TO_HEX = {
    1: "#ffffff", 2: "#ffff00", 3: "#00ffff", 4: "#00ff00",
    5: "#ff00ff", 6: "#0000ff", 7: "#ff0000",

    8: "#cccccc", 9: "#ff4444", 10: "#ffaa00",
    11: "#ccffcc", 12: "#4444ff", 13: "#00ff88",
    14: "#ffff88", 15: "#ff8888",

    16: "#ff8000",   # orange
    17: "#e6d9b3",   # beige
    18: "#000000",   # black
    19: "#996600",   # brown
    20: "#000000",   # black bg
    21: "#ffffff",   # white bg
    22: "#66cc66",   # soft green
    23: "#008000",   # dark green
    24: "#80b3ff",   # light blue
    25: "#0033b3",   # deep blue
    26: "#ff99b3",   # pink
    27: "#9900cc",   # purple
    28: "#cc99ff",   # lavender
    29: "#808080",   # gray
    30: "#404040",   # dark gray
    31: "#ffd9b3",   # light skin
    32: "#cc9966",   # tan
    33: "#ffd700",   # gold
    34: "#b30000",   # crimson
    35: "#00b3b3",   # teal
    36: "#99ffcc",   # mint
    37: "#663300",   # dark brown
    38: "#ffff99",   # pale yellow
}

DEFAULT_CHAR = " "

class SpriteEditor:
    def import_from_text(self, text):
        try:
            # name
            name_split = text.split("=RenderImage", 1)
            if len(name_split) < 2:
                return
            name = name_split[0].strip()

            body = name_split[1]

            def extract_block(key):
                start = body.find(key + "=\"\"\"")
                if start == -1:
                    return ""
                start += len(key) + 3
                end = body.find("\"\"\"", start)
                return body[start:end]

            front = extract_block("front_art")
            back = extract_block("back_art")

            pal_start = body.find("palettes=")
            if pal_start == -1:
                palettes = {"normal": {}, "shiny": {}}
            else:
                pal_str = body[pal_start + len("palettes="):].strip()
                palettes = ast.literal_eval(pal_str)

            # convert grids
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)

            self.front = [list(r.ljust(WIDTH)[:WIDTH]) for r in front.splitlines()]
            self.back = [list(r.ljust(WIDTH)[:WIDTH]) for r in back.splitlines()]

            self.palettes = palettes

            self.draw_grid()
            self.update_palette_display()
            self.update_status_label()

        except Exception as e:
            print("Import failed:", e)

    def open_import_window(self):
        win = tk.Toplevel(self.root)
        win.title("Import Sprite")

        text_box = tk.Text(win, width=60, height=20)
        text_box.pack()

        def do_import():
            data = text_box.get("1.0", tk.END)
            self.import_from_text(data)
            win.destroy()

        tk.Button(win, text="Import", command=do_import).pack()

    def update_palette_display(self):
        # Clear old
        for widget in self.palette_frame.winfo_children():
            widget.destroy()

        palette = self.palettes[self.current_palette]

        if not palette:
            tk.Label(self.palette_frame, text="No mappings yet").pack()
            return

        for ch, color_id in palette.items():
            color = CURSES_TO_HEX.get(color_id, "#111111")
            is_bg = color_id in [8,9,10,11,12,13,14,15,20,21]

            item = tk.Frame(self.palette_frame)
            item.pack(side=tk.LEFT, padx=3)

            swatch = tk.Label(
                item,
                text="BG" if is_bg else "FG",
                bg=color if is_bg else "#000000",
                fg="#ffffff" if is_bg else color,
                width=3,
                height=1,
                relief="ridge"
            )
            swatch.pack()

            label = tk.Label(item, text=f"{ch} ({color_id})")
            label.pack()

    def __init__(self, root):
        self.root = root
        self.root.title("Pokéthon sprite editor (UNFINISHED)")
        # set window size to match grid exactly
        self.root.update_idletasks()

        canvas_w = WIDTH * CELL_W
        canvas_h = HEIGHT * CELL_H

        # extra space for UI (toolbars + palette + status)
        ui_height = 220

        self.root.geometry(f"{canvas_w}x{canvas_h + ui_height}")
        self.root.resizable(False, False)

        self.front = [[DEFAULT_CHAR]*WIDTH for _ in range(HEIGHT)]
        self.back = [[DEFAULT_CHAR]*WIDTH for _ in range(HEIGHT)]

        self.current_layer = "front"
        self.current_palette = "normal"
        self.current_char = "#"
        self.show_reference = True
        self.tool_mode = "paint"
        self.undo_stack = []
        self.redo_stack = []

        self.palettes = {
            "normal": {},
            "shiny": {}
        }

        self.build_ui()
        self.draw_grid()
        self.update_palette_display()
        self.update_status_label()
        self.root.bind("<Command-z>", lambda e: self.undo())
        self.root.bind("<Control-z>", lambda e: self.undo())

    def build_ui(self):
        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH*CELL_W,
            height=HEIGHT*CELL_H,
            bg="black"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.start_paint)
        self.canvas.bind("<B1-Motion>", self.paint_drag)
        self.painting = False

        self.controls_top = tk.Frame(self.root)
        self.controls_top.pack()

        self.controls_bottom = tk.Frame(self.root)
        self.controls_bottom.pack()

        self.controls_third = tk.Frame(self.root)
        self.controls_third.pack()

        # Palette frame (must exist before update_palette_display is called)
        self.palette_frame = tk.Frame(self.root)
        self.palette_frame.pack(pady=5)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=5)

        tk.Label(self.controls_top, text=" Symbol ").pack(side=tk.LEFT)

        self.map_char = tk.Entry(self.controls_top, width=3)
        self.map_char.insert(0, "#")
        self.map_char.pack(side=tk.LEFT)

        # Dropdown for color IDs (sorted)
        color_ids = sorted(CURSES_TO_HEX.keys())
        def color_label(cid):
            names = {
                1:"white",2:"yellow",3:"cyan",4:"green",5:"magenta",6:"blue",7:"red",
                8:"white_bg",9:"red_bg",10:"yellow_bg",11:"green_bg",12:"blue_bg",
                13:"green_white",14:"yellow_white",15:"red_white",
                16:"orange",17:"beige",18:"black",19:"brown",
                20:"black_bg",21:"white_bg",

                22:"soft_green",23:"dark_green",
                24:"light_blue",25:"deep_blue",
                26:"pink",27:"purple",28:"lavender",
                29:"gray",30:"dark_gray",
                31:"skin_light",32:"skin_tan",
                33:"gold",34:"crimson",
                35:"teal",36:"mint",
                37:"dark_brown",38:"pale_yellow"
            }
            return f"{cid} ({names.get(cid, 'unknown')})"

        self.color_options = {color_label(cid): cid for cid in color_ids}
        first_label = list(self.color_options.keys())[0]

        self.map_color_var = tk.StringVar(value=first_label)
        self.map_color = tk.OptionMenu(self.controls_top, self.map_color_var, *self.color_options.keys())
        self.map_color.config(width=4)
        self.map_color.pack(side=tk.LEFT)

        tk.Button(self.controls_top, text="Apply", command=self.map_color_to_char).pack(side=tk.LEFT)

        # Toggles
        tk.Button(self.controls_top, text="Front/Back", command=self.toggle_layer).pack(side=tk.LEFT)
        tk.Button(self.controls_top, text="Normal/Shiny", command=self.toggle_palette).pack(side=tk.LEFT)
        tk.Button(self.controls_bottom, text="Toggle Ref", command=self.toggle_reference).pack(side=tk.LEFT)
        tk.Button(self.controls_bottom, text="Export", command=self.export).pack(side=tk.LEFT)
        tk.Button(self.controls_bottom, text="Import", command=self.open_import_window).pack(side=tk.LEFT)
        tk.Button(self.controls_bottom, text="Clear", command=self.clear_grid).pack(side=tk.LEFT)
        tk.Button(self.controls_bottom, text="Paint", command=lambda: self.set_tool("paint")).pack(side=tk.LEFT)
        tk.Button(self.controls_bottom, text="Eraser", command=lambda: self.set_tool("eraser")).pack(side=tk.LEFT)
        tk.Button(self.controls_bottom, text="Bucket", command=lambda: self.set_tool("bucket")).pack(side=tk.LEFT)
        tk.Button(self.controls_bottom, text="Cycle Tool", command=self.cycle_tool).pack(side=tk.LEFT)
        tk.Button(self.controls_third, text="Undo", command=self.undo).pack(side=tk.LEFT)
        tk.Button(self.controls_third, text="Redo", command=self.redo).pack(side=tk.LEFT)
        name_frame = tk.Frame(self.controls_third)
        name_frame.pack(side=tk.LEFT)

        tk.Label(name_frame, text="Name").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(name_frame, width=10)
        self.name_entry.insert(0, "sprite")
        self.name_entry.pack(side=tk.LEFT)

    def toggle_reference(self):
        self.show_reference = not self.show_reference
        self.draw_grid()

    def set_tool(self, mode):
        self.tool_mode = mode
        self.update_status_label()

    def cycle_tool(self):
        order = ["paint", "eraser", "bucket"]
        if self.tool_mode not in order:
            self.tool_mode = "paint"
        else:
            idx = order.index(self.tool_mode)
            self.tool_mode = order[(idx + 1) % len(order)]

        self.update_status_label()

    def update_status_label(self):
        name = self.name_entry.get().strip() or "sprite"
        text = f"{name} | {self.current_layer.upper()} | {self.current_palette.upper()} | {self.tool_mode.upper()}"
        self.status_label.config(text=text)

    def get_grid(self):
        return self.front if self.current_layer == "front" else self.back

    def get_palette_chars(self):
        chars = set()

        # characters defined in palettes
        for p in self.palettes.values():
            for ch in p.keys():
                chars.add(ch)

        # characters actually used in grids (front/back)
        for row in self.front:
            for ch in row:
                if ch:
                    chars.add(ch)

        for row in self.back:
            for ch in row:
                if ch:
                    chars.add(ch)

        # ensure default always exists
        chars.add(DEFAULT_CHAR)

        return sorted(list(chars))

    def refresh_char_dropdown(self):
        return

        menu = self.char_dropdown["menu"]
        menu.delete(0, "end")

        self.char_options = self.get_palette_chars()

        for ch in self.char_options:
            menu.add_command(label=ch, command=lambda v=ch: self.char_var.set(v))

        if self.char_options:
            self.char_var.set(self.char_options[0])

    def set_char(self):
        val = self.char_entry.get()
        if val:
            self.current_char = val[0]

    def map_color_to_char(self):
        self.save_state()
        ch = self.map_char.get()
        try:
            color_id = self.color_options.get(self.map_color_var.get())
        except:
            return

        if ch and color_id is not None:
            self.palettes[self.current_palette][ch[0]] = color_id
            self.draw_grid()
            self.update_palette_display()

    def toggle_layer(self):
        self.save_state()
        self.current_layer = "back" if self.current_layer == "front" else "front"
        self.draw_grid()
        self.update_status_label()

    def toggle_palette(self):
        self.save_state()
        self.current_palette = "shiny" if self.current_palette == "normal" else "normal"
        self.draw_grid()
        self.update_palette_display()
        self.update_status_label()

    def start_paint(self, event):
        self.painting = True
        self.paint(event)

    def paint_drag(self, event):
        if self.painting:
            self.paint(event)

    def paint(self, event):
        x = event.x // CELL_W
        y = event.y // CELL_H

        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            return

        self.save_state()

        grid = self.get_grid()

        # ERASER
        if self.tool_mode == "eraser":
            grid[y][x] = DEFAULT_CHAR
            self.draw_grid()
            return

        # BUCKET
        if self.tool_mode == "bucket":
            ch = self.map_char.get()
            replacement = ch[0] if ch else DEFAULT_CHAR
            target = grid[y][x]

            if target != replacement:
                self.flood_fill(grid, x, y, target, replacement)

            self.draw_grid()
            return

        # NORMAL PAINT
        ch = self.map_char.get()
        grid[y][x] = ch[0] if ch else DEFAULT_CHAR
        self.draw_grid()

        self.root.bind("<ButtonRelease-1>", lambda e: setattr(self, "painting", False))

    def flood_fill(self, grid, x, y, target, replacement):
        if target == replacement:
            return
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            return
        if grid[y][x] != target:
            return

        stack = [(x, y)]

        while stack:
            cx, cy = stack.pop()

            if not (0 <= cx < WIDTH and 0 <= cy < HEIGHT):
                continue
            if grid[cy][cx] != target:
                continue

            grid[cy][cx] = replacement

            stack.extend([
                (cx+1, cy),
                (cx-1, cy),
                (cx, cy+1),
                (cx, cy-1)
            ])

    def draw_grid(self):
        self.canvas.delete("all")
        grid = self.get_grid()
        palette = self.palettes[self.current_palette]

        # Determine reference layer/palette
        ref_grid = None
        ref_palette = None

        if self.show_reference:
            # reference is SAME layer, opposite palette (normal <-> shiny)
            other_palette = "shiny" if self.current_palette == "normal" else "normal"

            ref_grid = self.get_grid()
            ref_palette = self.palettes[other_palette]

        for y in range(HEIGHT):
            for x in range(WIDTH):
                ch = grid[y][x]
                color_id = palette.get(ch, None)
                color = CURSES_TO_HEX.get(color_id, "#111111")
                is_bg = color_id in [8,9,10,11,12,13,14,15,20,21]

                # Draw reference (faded background)
                if ref_grid:
                    ref_ch = ref_grid[y][x]
                    ref_color_id = ref_palette.get(ref_ch, None)
                    ref_color = CURSES_TO_HEX.get(ref_color_id, "#000000")

                    # draw faint reference
                    self.canvas.create_rectangle(
                        x*CELL_W,
                        y*CELL_H,
                        (x+1)*CELL_W,
                        (y+1)*CELL_H,
                        fill=ref_color,
                        outline="",
                        stipple="gray25"
                    )

                self.canvas.create_rectangle(
                    x*CELL_W,
                    y*CELL_H,
                    (x+1)*CELL_W,
                    (y+1)*CELL_H,
                    fill=color if is_bg else "",
                    outline="gray"
                )
                if not is_bg and color_id is not None:
                    self.canvas.create_text(
                        x*CELL_W + CELL_W//2,
                        y*CELL_H + CELL_H//2,
                        text=ch,
                        fill=color
                    )

    def grid_to_string(self, grid):
        return "\n".join("".join(row) for row in grid)

    def clear_grid(self):
        self.save_state()
        grid = self.get_grid()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                grid[y][x] = DEFAULT_CHAR
        self.draw_grid()
        self.update_status_label()

    def export(self):
        name = self.name_entry.get().strip() or "sprite"

        front_str = self.grid_to_string(self.front)
        back_str = self.grid_to_string(self.back)

        output = f"""{name}=RenderImage(
front_art=\"\"\"
{front_str}
\"\"\",
back_art=\"\"\"
{back_str}
\"\"\",
palettes={self.palettes}
)
"""

        print("\n=== COPY THIS ===\n")
        print(output)

    def save_state(self):
        self.undo_stack.append((
            copy.deepcopy(self.front),
            copy.deepcopy(self.back),
            copy.deepcopy(self.palettes),
            self.current_layer,
            self.current_palette
        ))
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return

        # save current state to redo
        self.redo_stack.append((
            copy.deepcopy(self.front),
            copy.deepcopy(self.back),
            copy.deepcopy(self.palettes),
            self.current_layer,
            self.current_palette
        ))

        self.front, self.back, self.palettes, self.current_layer, self.current_palette = self.undo_stack.pop()
        self.draw_grid()
        self.update_palette_display()
        self.update_status_label()

    def redo(self):
        if not self.redo_stack:
            return

        self.undo_stack.append((
            copy.deepcopy(self.front),
            copy.deepcopy(self.back),
            copy.deepcopy(self.palettes),
            self.current_layer,
            self.current_palette
        ))

        self.front, self.back, self.palettes, self.current_layer, self.current_palette = self.redo_stack.pop()
        self.draw_grid()
        self.update_palette_display()
        self.update_status_label()

# Run
root = tk.Tk()
app = SpriteEditor(root)
root.mainloop()