import csv
import random
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

RARITY_VALUES = {
    'common': 50,
    'uncommon': 325,
    'rare': 1250,
    'very rare': 3000,
    'legendary': 30000,
    'artifact': 60000,
}

LEVEL_RARITY_TABLE = {
    1: {'common': 6, 'uncommon': 4, 'rare': 1, 'very rare': 0, 'legendary': 0},
    2: {'common': 6, 'uncommon': 4, 'rare': 1, 'very rare': 0, 'legendary': 0},
    3: {'common': 6, 'uncommon': 4, 'rare': 1, 'very rare': 0, 'legendary': 0},
    4: {'common': 6, 'uncommon': 4, 'rare': 1, 'very rare': 0, 'legendary': 0},
    5: {'common': 10, 'uncommon': 13, 'rare': 2, 'very rare': 1, 'legendary': 0},
    6: {'common': 10, 'uncommon': 14, 'rare': 3, 'very rare': 1, 'legendary': 0},
    7: {'common': 10, 'uncommon': 15, 'rare': 4, 'very rare': 1, 'legendary': 0},
    8: {'common': 10, 'uncommon': 16, 'rare': 5, 'very rare': 2, 'legendary': 0},
    9: {'common': 10, 'uncommon': 17, 'rare': 6, 'very rare': 2, 'legendary': 1},
    10: {'common': 8, 'uncommon': 16, 'rare': 8, 'very rare': 2, 'legendary': 1},
    11: {'common': 7, 'uncommon': 13, 'rare': 10, 'very rare': 4, 'legendary': 1},
    12: {'common': 5, 'uncommon': 10, 'rare': 11, 'very rare': 6, 'legendary': 1},
    13: {'common': 5, 'uncommon': 9, 'rare': 11, 'very rare': 6, 'legendary': 1},
    14: {'common': 4, 'uncommon': 7, 'rare': 11, 'very rare': 9, 'legendary': 1},
    15: {'common': 3, 'uncommon': 6, 'rare': 11, 'very rare': 11, 'legendary': 2},
    16: {'common': 3, 'uncommon': 5, 'rare': 11, 'very rare': 11, 'legendary': 2},
    17: {'common': 2, 'uncommon': 3, 'rare': 10, 'very rare': 12, 'legendary': 2},
    18: {'common': 0, 'uncommon': 2, 'rare': 10, 'very rare': 13, 'legendary': 3},
    19: {'common': 0, 'uncommon': 2, 'rare': 10, 'very rare': 14, 'legendary': 3},
    20: {'common': 0, 'uncommon': 2, 'rare': 10, 'very rare': 15, 'legendary': 3},
}

GEMSTONE_VALUE_LIST = {
    'AMETHYST': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'AQUAMARINE': {'Flawless': 400, 'Brilliant': 300, 'Cut': 200, 'Raw': 100, 'Rough': 50},
    'CITRINE': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'GARNET': {'Flawless': 200, 'Brilliant': 150, 'Cut': 100, 'Raw': 75, 'Rough': 50},
    'ONYX': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'OPAL': {'Flawless': 400, 'Brilliant': 350, 'Cut': 300, 'Raw': 250, 'Rough': 200},
    'PEARL': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'RUBY': {'Flawless': 700, 'Brilliant': 600, 'Cut': 500, 'Raw': 400, 'Rough': 300},
    'SAPPHIRE': {'Flawless': 800, 'Brilliant': 700, 'Cut': 600, 'Raw': 500, 'Rough': 400},
    'TOPAZ': {'Flawless': 100, 'Brilliant': 75, 'Cut': 50, 'Raw': 20, 'Rough': 5},
    'TOURMALINE': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'DIAMOND': {'Flawless': 1000, 'Brilliant': 800, 'Cut': 700, 'Raw': 500, 'Rough': 300},
    'EMERALD': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'JADE': {'Flawless': 400, 'Brilliant': 350, 'Cut': 300, 'Raw': 250, 'Rough': 200},
    'JASPER': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'PERIDOT': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'SPINEL': {'Flawless': 600, 'Brilliant': 500, 'Cut': 400, 'Raw': 300, 'Rough': 200},
    'ZIRCON': {'Flawless': 500, 'Brilliant': 400, 'Cut': 300, 'Raw': 200, 'Rough': 100},
    'AMBER': {'Flawless': 300, 'Brilliant': 250, 'Cut': 200, 'Raw': 150, 'Rough': 100},
    'MOONSTONE': {'Flawless': 400, 'Brilliant': 350, 'Cut': 300, 'Raw': 250, 'Rough': 200},
    'TURQUOISE': {'Flawless': 200, 'Brilliant': 150, 'Cut': 100, 'Raw': 75, 'Rough': 50},
}

RARITY_LIST = ['common', 'uncommon', 'rare', 'very rare', 'legendary', 'artifact']

def get_rarity(row, header=None):
    idx = 3
    if header:
        for i, col in enumerate(header):
            if col.strip().lower() == 'rarity':
                idx = i
                break
    rarity = row[idx].strip().lower()
    if rarity in RARITY_LIST:
        return rarity
    for r in RARITY_LIST:
        if r in rarity:
            return r
    return 'unknown'

def filter_items_by_rarity(items, rarity):
    return [item for item in items if get_rarity(item) == rarity]

def get_random_rarity_distribution(level):
    rarity_caps = LEVEL_RARITY_TABLE.get(level, LEVEL_RARITY_TABLE[1])
    rarity_dist = {}
    for rarity, cap in rarity_caps.items():
        if cap > 0:
            rarity_dist[rarity] = random.randint(0, cap)
        else:
            rarity_dist[rarity] = 0
    return rarity_dist

def select_items_by_level(items, level):
    rarity_counts = get_random_rarity_distribution(level)
    selected = []
    for rarity, count in rarity_counts.items():
        pool = filter_items_by_rarity(items, rarity)
        if pool and count > 0:
            selected.extend(random.sample(pool, min(count, len(pool))))
    return selected

def get_item_value(rarity):
    import random
    ranges = {
        'common': (40, 60),
        'uncommon': (150, 500),
        'rare': (500, 2000),
        'very rare': (1000, 5000),
        'legendary': (10000, 50000),
        'artifact': (50000, 70000),
    }
    low, high = ranges.get(rarity, (0, 0))
    return random.randint(low, high)

def write_csv_shop(header, data, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def write_csv_loot(header, data, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def run_generation(mode, method, out_name, max_items, level=None, value=None):
    csv_path = 'magic items.csv'
    out_path = f'{out_name}.csv'
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if not rows:
            raise Exception('No data found.')
        header = rows[0]
        data = rows[1:]

    if method == 'level':
        selected = select_items_by_level(data, level)
    elif method == 'value':
        selected = select_items_by_value(data, value)
    else:
        raise Exception('Invalid method.')
    if len(selected) > max_items:
        selected = random.sample(selected, max_items)

    if mode == 'Shop':
        shop_header = ['Name', 'Rarity', 'Type', 'Value', 'Attunement', 'Text']
        shop_data = []
        for row in selected:
            name = row[0]
            rarity = row[3]
            typ = row[4]
            value = get_item_value(rarity.title())
            attunement = row[5]
            text = row[11]
            shop_data.append([name, rarity, typ, value, attunement, text])
        write_csv_shop(shop_header, shop_data, out_path)
        return f'Shop inventory saved to {out_path}'
    elif mode == 'Loot':
        loot_header = ['Name', 'Rarity', 'Type', 'Attunement', 'Text']
        loot_data = []
        for row in selected:
            name = row[0]
            rarity = row[3]
            typ = row[4]
            attunement = row[5]
            text = row[11]
            loot_data.append([name, rarity, typ, attunement, text])
        write_csv_loot(loot_header, loot_data, out_path)
        return f'Loot table saved to {out_path}'
    else:
        raise Exception('Invalid mode.')

def select_items_by_value(items, total_value):
    selected = []
    pool = items[:]
    random.shuffle(pool)
    current_value = 0
    while pool and current_value < total_value:
        item = pool.pop()
        rarity = get_rarity(item)
        value = get_item_value(rarity)
        if current_value + value <= total_value:
            selected.append(item)
            current_value += value
        elif not selected:
            selected.append(item)
            break
    return selected

def gui_main():
    root = tk.Tk()
    root.title('Magic Item Generator')

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    gen_frame = ttk.Frame(notebook)
    notebook.add(gen_frame, text='Generator')

    mode_var = tk.StringVar(value='Shop')
    ttk.Label(gen_frame, text='Mode:').grid(row=0, column=0, sticky='w')
    ttk.Radiobutton(gen_frame, text='Shop', variable=mode_var, value='Shop').grid(row=0, column=1, sticky='w')
    ttk.Radiobutton(gen_frame, text='Loot', variable=mode_var, value='Loot').grid(row=0, column=2, sticky='w')

    method_var = tk.StringVar(value='level')
    ttk.Label(gen_frame, text='Loot Generation Method:').grid(row=1, column=0, sticky='w')
    ttk.Radiobutton(gen_frame, text='By character level', variable=method_var, value='level').grid(row=1, column=1, sticky='w')
    ttk.Radiobutton(gen_frame, text='By total gold value', variable=method_var, value='value').grid(row=1, column=2, sticky='w')

    ttk.Label(gen_frame, text='Output file name (no .csv):').grid(row=2, column=0, sticky='w')
    out_name_entry = ttk.Entry(gen_frame)
    out_name_entry.grid(row=2, column=1, columnspan=2, sticky='we')

    ttk.Label(gen_frame, text='Max items:').grid(row=3, column=0, sticky='w')
    max_items_entry = ttk.Entry(gen_frame)
    max_items_entry.grid(row=3, column=1, columnspan=2, sticky='we')

    ttk.Label(gen_frame, text='Character level (1-20):').grid(row=4, column=0, sticky='w')
    level_entry = ttk.Entry(gen_frame)
    level_entry.grid(row=4, column=1, columnspan=2, sticky='we')

    ttk.Label(gen_frame, text='Total gold value (GP):').grid(row=5, column=0, sticky='w')
    value_entry = ttk.Entry(gen_frame)
    value_entry.grid(row=5, column=1, columnspan=2, sticky='we')

    def update_fields(*args):
        if method_var.get() == 'level':
            level_entry.config(state='normal')
            value_entry.config(state='disabled')
        else:
            level_entry.config(state='disabled')
            value_entry.config(state='normal')
    method_var.trace_add('write', update_fields)
    update_fields()

    def on_generate():
        mode = mode_var.get()
        method = method_var.get()
        out_name = out_name_entry.get().strip()
        max_items = max_items_entry.get().strip()
        level = level_entry.get().strip()
        value = value_entry.get().strip()
        if not out_name or not max_items or (method == 'level' and not level) or (method == 'value' and not value):
            messagebox.showerror('Error', 'Please fill in all required fields.')
            return
        try:
            max_items = int(max_items)
            if method == 'level':
                level = int(level)
                msg = run_generation(mode, method, out_name, max_items, level=level)
            else:
                value = int(value)
                msg = run_generation(mode, method, out_name, max_items, value=value)
            messagebox.showinfo('Success', msg)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    generate_btn = ttk.Button(gen_frame, text='Generate', command=on_generate)
    generate_btn.grid(row=6, column=0, columnspan=3, pady=10)

    viewer_frame = ttk.Frame(notebook)
    notebook.add(viewer_frame, text='CSV Viewer')

    status_var = tk.StringVar(value='Ready.')
    status_bar = ttk.Label(viewer_frame, textvariable=status_var, anchor='w', relief='sunken')
    status_bar.grid(row=99, column=0, columnspan=2, sticky='we', pady=(8,0))

    def save_csv():
        if not csv_data['file_path'] or not csv_data['header']:
            messagebox.showerror('Error', 'No CSV loaded.')
            return
        try:
            with open(csv_data['file_path'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(csv_data['header'])
                for row in csv_data['rows']:
                    writer.writerow(row)
            messagebox.showinfo('Saved', 'CSV file updated.')
            status_var.set('CSV file saved.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save CSV: {e}')
            status_var.set('Failed to save CSV.')

    action_frame = ttk.Frame(viewer_frame)
    action_frame.grid(row=1, column=0, columnspan=2, sticky='we', pady=5)
    del_btn = ttk.Button(action_frame, text='Delete Selected Item(s)')
    del_btn.grid(row=0, column=0, padx=10, pady=5)
    save_btn = ttk.Button(action_frame, text='Save CSV', state='normal')
    save_btn.grid(row=0, column=1, padx=10, pady=5)

    filter_var = tk.StringVar()
    filter_frame = ttk.Frame(viewer_frame)
    filter_frame.grid(row=2, column=0, columnspan=2, sticky='we')
    ttk.Label(filter_frame, text='Search:').pack(side='left')
    filter_entry = ttk.Entry(filter_frame, textvariable=filter_var, width=30)
    filter_entry.pack(side='left', padx=4)
    clear_filter_btn = ttk.Button(filter_frame, text='Clear', command=lambda: filter_var.set(''))
    clear_filter_btn.pack(side='left', padx=2)

    tree = None
    csv_data = {'header': [], 'rows': [], 'file_path': None, 'filtered_rows': []}
    sort_state = {'col': None, 'reverse': False}

    preview_frame = ttk.Frame(viewer_frame)
    preview_frame.grid(row=7, column=0, columnspan=2, sticky='we', pady=5)
    ttk.Label(preview_frame, text='Text Preview:').grid(row=0, column=0, sticky='w')
    preview_text = tk.Text(preview_frame, height=6, width=80, wrap='word', state='disabled')
    preview_text.grid(row=1, column=0, sticky='we')
    preview_frame.grid_columnconfigure(0, weight=1)

    def sort_by_column(col):
        if not csv_data['header']:
            return
        idx = csv_data['header'].index(col)
        reverse = not sort_state['reverse'] if sort_state['col'] == col else False
        sort_state['col'] = col
        sort_state['reverse'] = reverse
        try:
            sorted_rows = sorted(csv_data['filtered_rows'], key=lambda r: float(r[idx]) if r[idx].replace('.','',1).isdigit() else r[idx], reverse=reverse)
        except Exception:
            sorted_rows = sorted(csv_data['filtered_rows'], key=lambda r: r[idx], reverse=reverse)
        build_tree(csv_data['header'], sorted_rows)
        csv_data['filtered_rows'] = sorted_rows
        status_var.set(f"Sorted by {col} ({'desc' if reverse else 'asc'})")

    def update_preview(event=None):
        if not tree or not csv_data['filtered_rows']:
            preview_text.config(state='normal')
            preview_text.delete('1.0', tk.END)
            preview_text.config(state='disabled')
            return
        selected = tree.selection()
        if not selected:
            preview_text.config(state='normal')
            preview_text.delete('1.0', tk.END)
            preview_text.config(state='disabled')
            return
        idxs = [tree.index(s) for s in selected]
        row = csv_data['filtered_rows'][idxs[0]]
        text_idx = None
        for i, col in enumerate(csv_data['header']):
            if col.strip().lower() == 'text':
                text_idx = i
                break
        preview_text.config(state='normal')
        preview_text.delete('1.0', tk.END)
        if text_idx is not None and row[text_idx]:
            preview_text.insert(tk.END, row[text_idx])
        preview_text.config(state='disabled')

    def bind_tree_select():
        if tree:
            tree.bind('<<TreeviewSelect>>', update_preview)

    def delete_selected():
        if not tree or not csv_data['filtered_rows']:
            messagebox.showerror('Error', 'No CSV loaded.')
            return
        selected = tree.selection()
        if not selected:
            messagebox.showerror('Error', 'No item selected.')
            return
        idxs = sorted([tree.index(s) for s in selected], reverse=True)
        for idx in idxs:
            row = csv_data['filtered_rows'][idx]
            if row in csv_data['rows']:
                csv_data['rows'].remove(row)
        update_tree()
        status_var.set(f"Deleted {len(idxs)} item(s).")
    del_btn.config(command=delete_selected)

    tree_frame = ttk.Frame(viewer_frame)
    tree_frame.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=4)
    viewer_frame.grid_rowconfigure(3, weight=1)
    viewer_frame.grid_columnconfigure(0, weight=1)

    def build_tree(header, data):
        nonlocal tree
        for widget in tree_frame.winfo_children():
            widget.destroy()
        tree = ttk.Treeview(tree_frame, columns=header, show='headings', selectmode='extended')
        for col in header:
            def sort_col_factory(c=col):
                return lambda e=None: sort_by_column(c)
            tree.heading(col, text=col, command=sort_col_factory(col))
            tree.column(col, width=120, anchor='w')
        for row in data:
            tree.insert('', 'end', values=row)
        tree.grid(row=0, column=0, sticky='nsew')
        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=vsb.set)
        vsb.grid(row=0, column=1, sticky='ns')
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal', command=tree.xview)
        tree.configure(xscroll=hsb.set)
        hsb.grid(row=1, column=0, sticky='ew')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        bind_tree_select()
        update_preview()

    def filter_rows():
        if not csv_data['header']:
            return []
        query = filter_var.get().strip().lower()
        if not query:
            return csv_data['rows']
        filtered = [row for row in csv_data['rows'] if any(query in str(cell).lower() for cell in row)]
        return filtered

    def update_tree():
        filtered = filter_rows()
        csv_data['filtered_rows'] = filtered
        build_tree(csv_data['header'], filtered)
        status_var.set(f"{len(filtered)} / {len(csv_data['rows'])} items shown.")

    filter_var.trace_add('write', lambda *a: update_tree())

    def load_csv():
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if not file_path:
            return
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if not rows:
                    messagebox.showerror('Error', 'CSV file is empty.')
                    return
                header = rows[0]
                data = rows[1:]
            csv_data['header'] = header
            csv_data['rows'] = data
            csv_data['file_path'] = file_path
            update_tree()
            status_var.set(f"Loaded {file_path} ({len(data)} items)")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load CSV: {e}')
            status_var.set('Failed to load CSV.')

    open_btn = ttk.Button(viewer_frame, text='Open CSV File', command=load_csv)
    open_btn.grid(row=0, column=0, sticky='w', pady=5, padx=5)

    action_frame = ttk.Frame(viewer_frame)
    action_frame.grid(row=5, column=0, columnspan=2, sticky='we', pady=5)
    del_btn = ttk.Button(action_frame, text='Delete Selected Item(s)')
    del_btn.grid(row=0, column=0, padx=10, pady=5)
    save_btn = ttk.Button(action_frame, text='Save CSV', state='normal')
    save_btn.grid(row=0, column=1, padx=10, pady=5)

    add_frame = ttk.Frame(viewer_frame)
    add_frame.grid(row=4, column=0, columnspan=2, sticky='we', pady=5)
    ttk.Label(add_frame, text='Add Potions/Gemstones:').grid(row=0, column=0, sticky='w')
    ttk.Label(add_frame, text='Number of Potions:').grid(row=0, column=1, sticky='e')
    num_potions_var = tk.StringVar(value='1')
    num_potions_entry = ttk.Entry(add_frame, textvariable=num_potions_var, width=4)
    num_potions_entry.grid(row=0, column=2, padx=2)
    add_potion_btn = ttk.Button(add_frame, text='Add Potions', state='normal')
    add_potion_btn.grid(row=0, column=3, padx=10)
    ttk.Label(add_frame, text='Gemstone Value:').grid(row=0, column=4, sticky='e')
    gem_value_var = tk.StringVar(value='100')
    gem_value_entry = ttk.Entry(add_frame, textvariable=gem_value_var, width=8)
    gem_value_entry.grid(row=0, column=5, padx=2)
    add_gem_btn = ttk.Button(add_frame, text='Add Gemstones', state='normal')
    add_gem_btn.grid(row=0, column=6, padx=10)

    def add_potions():
        if not csv_data['header']:
            messagebox.showerror('Error', 'No CSV loaded.')
            return
        try:
            n = int(num_potions_var.get())
            if n < 1:
                raise ValueError
        except Exception:
            messagebox.showerror('Error', 'Enter a valid number of potions.')
            return
        try:
            with open('magic items.csv', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                magic_rows = list(reader)
                if not magic_rows:
                    messagebox.showerror('Error', 'magic items.csv is empty.')
                    return
                magic_header = magic_rows[0]
                magic_data = magic_rows[1:]
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load magic items.csv: {e}')
            return
        type_idx = None
        rarity_idx = None
        for i, col in enumerate(magic_header):
            if col.strip().lower() == 'type':
                type_idx = i
            if col.strip().lower() == 'rarity':
                rarity_idx = i
        if type_idx is None or rarity_idx is None:
            messagebox.showerror('Error', 'magic items.csv missing Type or Rarity column.')
            return
        potions = [row for row in magic_data if 'potion' in row[type_idx].lower() and row[rarity_idx].strip().lower() in ['common', 'uncommon']]
        if not potions:
            messagebox.showerror('Error', 'No potions found in magic items.csv.')
            return
        chosen = random.sample(potions, min(n, len(potions)))
        for row in chosen:
            new_row = []
            for col in csv_data['header']:
                col_lower = col.strip().lower()
                if col_lower in [c.strip().lower() for c in magic_header]:
                    idx = [c.strip().lower() for c in magic_header].index(col_lower)
                    new_row.append(row[idx] if idx < len(row) else '')
                else:
                    new_row.append('')
            csv_data['rows'].append(new_row)
        update_tree()
        status_var.set(f'Added {len(chosen)} potion(s).')
    add_potion_btn.config(command=add_potions)

    def add_gemstones():
        if not csv_data['header']:
            messagebox.showerror('Error', 'No CSV loaded.')
            return
        try:
            target_value = int(gem_value_var.get())
            if target_value < 1:
                raise ValueError
        except Exception:
            messagebox.showerror('Error', 'Enter a valid gemstone value.')
            return
        min_total = int(target_value * 0.9)
        max_total = int(target_value * 1.1)
        total = 0
        gems = []
        tries = 0
        while total < min_total and tries < 1000:
            gem = random.choice(list(GEMSTONE_VALUE_LIST.keys()))
            quality = random.choice(list(GEMSTONE_VALUE_LIST[gem].keys()))
            value = GEMSTONE_VALUE_LIST[gem][quality]
            if total + value > max_total:
                tries += 1
                continue
            gems.append((gem, quality, value))
            total += value
            tries += 1
        if not gems:
            messagebox.showerror('Error', 'Could not generate gemstones for the given value.')
            return
        for gem, quality, value in gems:
            row = []
            for col in csv_data['header']:
                col_lower = col.strip().lower()
                if col_lower == 'name':
                    row.append(f'{quality} {gem.title()}')
                elif col_lower == 'type':
                    row.append('Gemstone')
                elif col_lower == 'rarity':
                    if value < 100:
                        row.append('common')
                    elif value < 300:
                        row.append('uncommon')
                    elif value < 600:
                        row.append('rare')
                    elif value < 1000:
                        row.append('very rare')
                    else:
                        row.append('legendary')
                elif col_lower == 'value':
                    row.append(str(value))
                else:
                    row.append('')
            csv_data['rows'].append(row)
        update_tree()
        status_var.set(f'Added {len(gems)} gemstone(s) totaling {total} gp.')
    add_gem_btn.config(command=add_gemstones)

    additem_frame = ttk.Frame(viewer_frame)
    additem_frame.grid(row=5, column=0, columnspan=2, sticky='we', pady=5)
    ttk.Label(additem_frame, text='Add Item by Rarity/Name:').grid(row=0, column=0, sticky='w')
    rarity_choices = RARITY_LIST
    additem_rarity_var = tk.StringVar(value=rarity_choices[0].title())
    rarity_menu = ttk.Combobox(additem_frame, textvariable=additem_rarity_var, values=[r.title() for r in rarity_choices], width=12, state='readonly')
    rarity_menu.grid(row=0, column=1, padx=2)
    ttk.Label(additem_frame, text='(optional) Name:').grid(row=0, column=2, sticky='e')
    additem_name_var = tk.StringVar()
    additem_name_entry = ttk.Entry(additem_frame, textvariable=additem_name_var, width=18)
    additem_name_entry.grid(row=0, column=3, padx=2)
    additem_btn = ttk.Button(additem_frame, text='Add Item')
    additem_btn.grid(row=0, column=4, padx=6)

    def fuzzy_match(query, candidates):
        import difflib
        matches = [c for c in candidates if query.lower() in c.lower()]
        if matches:
            return matches[0]
        close = difflib.get_close_matches(query, candidates, n=1)
        return close[0] if close else None

    def add_item_by_rarity():
        if not csv_data['header']:
            messagebox.showerror('Error', 'No CSV loaded.')
            return
        rarity_idx = None
        for i, col in enumerate(csv_data['header']):
            if col.strip().lower() == 'rarity':
                rarity_idx = i
                break
        if rarity_idx is None:
            messagebox.showerror('Error', 'No Rarity column in CSV.')
            return
        rarity = additem_rarity_var.get().strip().lower()
        name_query = additem_name_var.get().strip()
        try:
            with open('magic items.csv', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                magic_rows = list(reader)
                if not magic_rows:
                    messagebox.showerror('Error', 'magic items.csv is empty.')
                    return
                magic_header = magic_rows[0]
                magic_data = magic_rows[1:]
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load magic items.csv: {e}')
            return
        magic_rarity_idx = None
        for i, col in enumerate(magic_header):
            if col.strip().lower() == 'rarity':
                magic_rarity_idx = i
                break
        if magic_rarity_idx is None:
            messagebox.showerror('Error', 'No Rarity column in magic items.csv.')
            return
        pool = [row for row in magic_data if get_rarity(row, magic_header) == rarity]
        if not pool:
            pool = [row for row in magic_data if rarity in row[magic_rarity_idx].strip().lower()]
        if not pool:
            available = set(row[magic_rarity_idx].strip().lower() for row in magic_data)
            messagebox.showerror('Error', f'No items of rarity {additem_rarity_var.get()} found in magic items.csv.\nAvailable rarities: {sorted(available)}')
            return
        if name_query:
            name_idx = None
            for i, col in enumerate(magic_header):
                if col.strip().lower() == 'name':
                    name_idx = i
                    break
            if name_idx is None:
                messagebox.showerror('Error', 'No Name column in magic items.csv.')
                return
            names = [row[name_idx] for row in pool]
            match = fuzzy_match(name_query, names)
            if not match:
                messagebox.showerror('Error', f'No close match for "{name_query}" in {additem_rarity_var.get()} (magic items.csv).')
                return
            row = next(row for row in pool if row[name_idx] == match)
        else:
            row = random.choice(pool)
        new_row = []
        for col in csv_data['header']:
            col_lower = col.strip().lower()
            if col_lower in [c.strip().lower() for c in magic_header]:
                idx = [c.strip().lower() for c in magic_header].index(col_lower)
                new_row.append(row[idx] if idx < len(row) else '')
            else:
                new_row.append('')
        csv_data['rows'].append(new_row)
        update_tree()
        status_var.set(f'Added item: {new_row[0]} ({rarity.title()})')
    additem_btn.config(command=add_item_by_rarity)

    addcustom_frame = ttk.Frame(viewer_frame)
    addcustom_frame.grid(row=6, column=0, columnspan=2, sticky='we', pady=5)
    ttk.Label(addcustom_frame, text='Add Custom Item:').grid(row=0, column=0, sticky='w')
    ttk.Label(addcustom_frame, text='Name:').grid(row=0, column=1, sticky='e')
    custom_name_var = tk.StringVar()
    custom_name_entry = ttk.Entry(addcustom_frame, textvariable=custom_name_var, width=14)
    custom_name_entry.grid(row=0, column=2, padx=2)
    ttk.Label(addcustom_frame, text='Type:').grid(row=0, column=3, sticky='e')
    custom_type_var = tk.StringVar()
    custom_type_entry = ttk.Entry(addcustom_frame, textvariable=custom_type_var, width=12)
    custom_type_entry.grid(row=0, column=4, padx=2)
    ttk.Label(addcustom_frame, text='Rarity:').grid(row=0, column=5, sticky='e')
    custom_rarity_var = tk.StringVar(value=rarity_choices[0].title())
    custom_rarity_menu = ttk.Combobox(addcustom_frame, textvariable=custom_rarity_var, values=[r.title() for r in rarity_choices], width=10, state='readonly')
    custom_rarity_menu.grid(row=0, column=6, padx=2)
    ttk.Label(addcustom_frame, text='Text:').grid(row=1, column=1, sticky='e')
    custom_text_var = tk.StringVar()
    custom_text_entry = ttk.Entry(addcustom_frame, textvariable=custom_text_var, width=32)
    custom_text_entry.grid(row=1, column=2, columnspan=3, padx=2, sticky='we')
    ttk.Label(addcustom_frame, text='Value:').grid(row=1, column=5, sticky='e')
    custom_value_var = tk.StringVar()
    custom_value_entry = ttk.Entry(addcustom_frame, textvariable=custom_value_var, width=10)
    custom_value_entry.grid(row=1, column=6, padx=2)
    addcustom_btn = ttk.Button(addcustom_frame, text='Add Custom Item')
    addcustom_btn.grid(row=0, column=7, rowspan=2, padx=6)

    def add_custom_item():
        if not csv_data['header']:
            messagebox.showerror('Error', 'No CSV loaded.')
            return
        name = custom_name_var.get().strip()
        typ = custom_type_var.get().strip()
        rarity = custom_rarity_var.get().strip().lower()
        text = custom_text_var.get().strip()
        value = custom_value_var.get().strip()
        if not name or not typ or not rarity:
            messagebox.showerror('Error', 'Name, Type, and Rarity are required.')
            return
        row = []
        for col in csv_data['header']:
            col_lower = col.strip().lower()
            if col_lower == 'name':
                row.append(name)
            elif col_lower == 'type':
                row.append(typ)
            elif col_lower == 'rarity':
                row.append(rarity)
            elif col_lower == 'text':
                row.append(text)
            elif col_lower == 'value':
                if value:
                    row.append(value)
                else:
                    if 'value' in [c.strip().lower() for c in csv_data['header']]:
                        row.append(str(get_item_value(rarity)))
                    else:
                        row.append('')
            else:
                row.append('')
        csv_data['rows'].append(row)
        update_tree()
        status_var.set(f'Added custom item: {name} ({rarity.title()})')
    addcustom_btn.config(command=add_custom_item)

    def on_ctrl_s(event):
        save_csv()
        return 'break'
    def on_delete(event):
        delete_selected()
        return 'break'
    def on_f5(event):
        pass
    def on_ctrl_f(event):
        filter_entry.focus_set()
        return 'break'
    root.bind_all('<Control-s>', on_ctrl_s)
    root.bind_all('<Delete>', on_delete)
    root.bind_all('<F5>', on_f5)
    root.bind_all('<Control-f>', on_ctrl_f)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', font=('Segoe UI', 11), padding=4)
    style.configure('TButton', font=('Segoe UI', 11), padding=4)
    style.configure('TEntry', font=('Segoe UI', 11), padding=2)
    style.configure('TCheckbutton', font=('Segoe UI', 11), padding=2)
    style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'))
    style.configure('Treeview', font=('Segoe UI', 10), rowheight=26)
    style.map('TButton', foreground=[('active', '#1a73e8')], background=[('active', '#e3f0fc')])
    root.option_add('*tearOff', False)
    root.minsize(900, 600)
    root.update_idletasks()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = w//2 - size[0]//2
    y = h//2 - size[1]//2
    root.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
    viewer_frame.configure(style='Custom.TFrame')
    style.configure('Custom.TFrame', background='#f7fafd')
    for child in viewer_frame.winfo_children():
        child.grid_configure(padx=8, pady=4)
    for child in gen_frame.winfo_children():
        child.grid_configure(padx=8, pady=4)
    preview_text.config(bg='#f0f4fa', relief='groove', bd=2, font=('Segoe UI', 10))
    if tree:
        tree.config(relief='groove', bd=2)

    root.mainloop()

if __name__ == '__main__':
    gui_main()
