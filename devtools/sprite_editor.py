import tkinter as tk

WIDTH = 25
HEIGHT = 11
CELL_SIZE = 25

# Approximate curses → hex
CURSES_TO_HEX = {
    1: "#ffffff", 2: "#ffff00", 3: "#00ffff", 4: "#00ff00",
    5: "#ff00ff", 6: "#0000ff", 7: "#ff0000",
    8: "#cccccc", 9: "#ff4444", 10: "#ffaa00",
    11: "#ccffcc", 12: "#4444ff", 13: "#00ff88",
    14: "#ffff88", 15: "#ff8888", 16: "#ff8800",
    17: "#e6d3a3", 18: "#000000", 19: "#8b4513",
    20: "#000000", 21: "#ffffff"
}

DEFAULT_CHAR = " "

class SpriteEditor:

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

            item = tk.Frame(self.palette_frame)
            item.pack(side=tk.LEFT, padx=3)

            swatch = tk.Label(
                item,
                text="  ",
                bg=color,
                width=2,
                height=1,
                relief="ridge"
            )
            swatch.pack()

            label = tk.Label(item, text=f"{ch} ({color_id})")
            label.pack()

    def __init__(self, root):
        self.root = root
        self.root.title("Pokéthon sprite editor (UNFINISHED)")

        self.front = [[DEFAULT_CHAR]*WIDTH for _ in range(HEIGHT)]
        self.back = [[DEFAULT_CHAR]*WIDTH for _ in range(HEIGHT)]

        self.current_layer = "front"
        self.current_palette = "normal"
        self.current_char = "#"

        self.palettes = {
            "normal": {},
            "shiny": {}
        }

        self.build_ui()
        self.draw_grid()
        self.update_palette_display()
        self.update_status_label()

    def build_ui(self):
        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH*CELL_SIZE,
            height=HEIGHT*CELL_SIZE,
            bg="black"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.paint)

        controls = tk.Frame(self.root)
        controls.pack()

        # Status title
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=5)

        # Character input
        tk.Label(controls, text="Char:").pack(side=tk.LEFT)
        self.char_entry = tk.Entry(controls, width=3)
        self.char_entry.pack(side=tk.LEFT)
        tk.Button(controls, text="Set", command=self.set_char).pack(side=tk.LEFT)

        # Palette editor
        tk.Label(controls, text=" Map Char→ColorID ").pack(side=tk.LEFT)

        self.map_char = tk.Entry(controls, width=3)
        self.map_char.pack(side=tk.LEFT)

        self.map_color = tk.Entry(controls, width=3)
        self.map_color.pack(side=tk.LEFT)

        tk.Button(controls, text="Apply", command=self.map_color_to_char).pack(side=tk.LEFT)

        # Toggles
        tk.Button(controls, text="Front/Back", command=self.toggle_layer).pack(side=tk.LEFT)
        tk.Button(controls, text="Normal/Shiny", command=self.toggle_palette).pack(side=tk.LEFT)

        tk.Button(controls, text="Export", command=self.export).pack(side=tk.LEFT)
        self.palette_frame = tk.Frame(self.root)
        self.palette_frame.pack(pady=5)
        
    def update_status_label(self):
        text = f"{self.current_layer.upper()} | {self.current_palette.upper()} PALETTE"
        self.status_label.config(text=text)

    def get_grid(self):
        return self.front if self.current_layer == "front" else self.back

    def set_char(self):
        val = self.char_entry.get()
        if val:
            self.current_char = val[0]

    def map_color_to_char(self):
        ch = self.map_char.get()
        try:
            color_id = int(self.map_color.get())
        except:
            return

        if ch:
            self.palettes[self.current_palette][ch[0]] = color_id
            self.draw_grid()
            self.update_palette_display()

    def toggle_layer(self):
        self.current_layer = "back" if self.current_layer == "front" else "front"
        self.draw_grid()
        self.update_status_label()

    def toggle_palette(self):
        self.current_palette = "shiny" if self.current_palette == "normal" else "normal"
        self.draw_grid()
        self.update_palette_display()
        self.update_status_label()

    def paint(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE

        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid = self.get_grid()
            grid[y][x] = self.current_char
            self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        grid = self.get_grid()
        palette = self.palettes[self.current_palette]

        for y in range(HEIGHT):
            for x in range(WIDTH):
                ch = grid[y][x]
                color_id = palette.get(ch, None)
                color = CURSES_TO_HEX.get(color_id, "#111111")

                self.canvas.create_rectangle(
                    x*CELL_SIZE,
                    y*CELL_SIZE,
                    (x+1)*CELL_SIZE,
                    (y+1)*CELL_SIZE,
                    fill=color,
                    outline="gray"
                )

    def grid_to_string(self, grid):
        return "\n".join("".join(row) for row in grid)

    def export(self):
        front_str = self.grid_to_string(self.front)
        back_str = self.grid_to_string(self.back)

        print("\n=== COPY THIS ===\n")
        print(f'''RenderImage(
front_art=\"\"\"
{front_str}
\"\"\",
back_art=\"\"\"
{back_str}
\"\"\",
palettes={self.palettes}
)
''')

# Run
root = tk.Tk()
app = SpriteEditor(root)
root.mainloop()