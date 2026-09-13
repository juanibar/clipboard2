import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import keyboard
import time

CSV_FILE = "mensajes_clipboard.csv"

class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Mensajes Rápidos")
        self.root.geometry("900x550")
        self.root.minsize(700, 400)
        
        self.root.attributes('-topmost', True) 
        
        self.data = self.load_data()
        self.current_category = "Todos los mensajes"
        
        self.tooltip_win = None
        self.tooltip_id = None
        self.hovered_item = None
        
        self.setup_ui()
        self.update_categories()
        self.refresh_list()
        
        keyboard.add_hotkey('ctrl+space+k', self.trigger_show_window)
        keyboard.add_hotkey('ctrl+space+p', self.trigger_paste_selected)
        self.root.bind('<Return>', lambda e: self.paste_selected())

    def load_data(self):
        if not os.path.exists(CSV_FILE):
            return []
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [{'id': int(row['id']), 'name': row.get('name', f"Mensaje {row['id']}"), 'category': row['category'], 'text': row['text'], 'count': int(row['count'])} for row in reader]

    def save_data(self):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'category', 'text', 'count'])
            writer.writeheader()
            writer.writerows(self.data)

    def trigger_show_window(self):
        self.root.after(0, self.show_window)

    def trigger_paste_selected(self):
        self.root.after(0, self.paste_selected)

    def show_window(self):
        self.root.deiconify()
        self.root.focus_force()

    def setup_ui(self):
        left_frame = ttk.Frame(self.root, width=200, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(left_frame, text="Categorías", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.cat_listbox = tk.Listbox(left_frame, exportselection=False, font=("Arial", 10))
        self.cat_listbox.pack(fill=tk.BOTH, expand=True)
        self.cat_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda name, index, mode: self.refresh_list())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        columns = ("nombre", "texto", "usos", "categoria")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("texto", text="Mensaje")
        self.tree.heading("usos", text="Usos")
        self.tree.heading("categoria", text="Categoría")
        
        self.tree.column("nombre", width=150)
        self.tree.column("texto", width=300)
        self.tree.column("usos", width=50, anchor=tk.CENTER)
        self.tree.column("categoria", width=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind("<Motion>", self.on_tree_motion)
        self.tree.bind("<Leave>", self.on_tree_leave)
        
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Pegar en aplicación", command=self.paste_selected).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.edit_message).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_message).pack(side=tk.RIGHT, padx=5)
        
        self.tree.bind("<Double-1>", lambda e: self.paste_selected())
        
        add_frame = ttk.LabelFrame(right_frame, text="Agregar Nuevo Mensaje", padding=10)
        add_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(add_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.new_name_entry = ttk.Entry(add_frame, width=20)
        self.new_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(add_frame, text="Categoría:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.new_cat_entry = ttk.Entry(add_frame, width=20)
        self.new_cat_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(add_frame, text="Mensaje:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.NW)
        self.new_text_entry = tk.Text(add_frame, height=3, width=50)
        self.new_text_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Button(add_frame, text="Guardar Mensaje", command=self.add_message).grid(row=1, column=4, padx=10, sticky=tk.S)
        add_frame.columnconfigure(1, weight=1)

    def on_tree_motion(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id != self.hovered_item:
            self.cancel_tooltip()
            self.hovered_item = item_id
            if item_id:
                self.tooltip_id = self.root.after(500, self.show_tooltip, event.x_root, event.y_root, item_id)

    def on_tree_leave(self, event):
        self.cancel_tooltip()

    def show_tooltip(self, x, y, item_id):
        if not self.tree.exists(item_id):
            return
            
        text = self.tree.item(item_id, 'values')[1]
        
        self.tooltip_win = tk.Toplevel(self.root)
        self.tooltip_win.wm_overrideredirect(True) 
        self.tooltip_win.attributes('-topmost', True) 
        
        self.tooltip_win.wm_geometry(f"+{x + 15}+{y + 10}")
        
        label = tk.Label(self.tooltip_win, text=text, justify='left', 
                         background="#ffffe0", relief='solid', borderwidth=1, 
                         font=("Arial", 10), wraplength=500, padx=5, pady=5)
        label.pack()

    def cancel_tooltip(self):
        if self.tooltip_id:
            self.root.after_cancel(self.tooltip_id)
            self.tooltip_id = None
        if self.tooltip_win:
            self.tooltip_win.destroy()
            self.tooltip_win = None
        self.hovered_item = None

    def update_categories(self):
        self.cat_listbox.delete(0, tk.END)
        categories = ["Todos los mensajes", "Más utilizados"]
        
        db_cats = sorted(list(set([m['category'] for m in self.data])))
        categories.extend(db_cats)
        
        for cat in categories:
            self.cat_listbox.insert(tk.END, cat)
            
        try:
            idx = categories.index(self.current_category)
            self.cat_listbox.selection_set(idx)
        except ValueError:
            self.cat_listbox.selection_set(0)
            self.current_category = "Todos los mensajes"

    def on_category_select(self, event):
        selection = self.cat_listbox.curselection()
        if selection:
            self.current_category = self.cat_listbox.get(selection[0])
            self.refresh_list()

    def refresh_list(self):
        self.cancel_tooltip() 
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_term = self.search_var.get().lower()
        
        if self.current_category == "Todos los mensajes":
            filtered_data = self.data.copy()
        elif self.current_category == "Más utilizados":
            filtered_data = sorted(self.data, key=lambda x: x['count'], reverse=True)[:10]
        else:
            filtered_data = [m for m in self.data if m['category'] == self.current_category]
            
        if search_term:
            filtered_data = [m for m in filtered_data if search_term in m['text'].lower() or search_term in m.get('name', '').lower()]
            
        filtered_data.sort(key=lambda x: x['count'], reverse=True)
        
        for m in filtered_data:
            self.tree.insert("", tk.END, values=(m.get('name', 'Sin Nombre'), m['text'], m['count'], m['category']), tags=(str(m['id']),))

    def add_message(self):
        name = self.new_name_entry.get().strip()
        cat = self.new_cat_entry.get().strip()
        text = self.new_text_entry.get("1.0", tk.END).strip()
        
        if not name or not cat or not text:
            messagebox.showwarning("Error", "El nombre, la categoría y el mensaje no pueden estar vacíos.")
            return
            
        new_id = 1 if not self.data else max(m['id'] for m in self.data) + 1
        self.data.append({'id': new_id, 'name': name, 'category': cat, 'text': text, 'count': 0})
        self.save_data()
        self.data = self.load_data() # Recarga forzada
        
        self.new_name_entry.delete(0, tk.END)
        self.new_text_entry.delete("1.0", tk.END)
        self.update_categories()
        self.refresh_list()

    def delete_message(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccioná un mensaje de la lista para eliminar.")
            return
            
        if messagebox.askyesno("Confirmar", "¿Seguro que querés eliminar este mensaje?"):
            msg_id = int(self.tree.item(selected[0], "tags")[0])
            self.data = [m for m in self.data if m['id'] != msg_id]
            
            self.save_data()
            self.data = self.load_data() # Recarga forzada
            self.update_categories()
            self.refresh_list()

    def edit_message(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccioná un mensaje de la lista para editar.")
            return
            
        msg_id = int(self.tree.item(selected[0], "tags")[0])
        msg_to_edit = next((m for m in self.data if m['id'] == msg_id), None)
        
        if not msg_to_edit:
            return
            
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Editar Mensaje")
        edit_win.geometry("500x320")
        edit_win.transient(self.root) 
        edit_win.grab_set() 
        
        ttk.Label(edit_win, text="Nombre:").pack(anchor=tk.W, padx=10, pady=(10,0))
        name_var = tk.StringVar(value=msg_to_edit.get('name', ''))
        ttk.Entry(edit_win, textvariable=name_var).pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(edit_win, text="Categoría:").pack(anchor=tk.W, padx=10, pady=(5,0))
        cat_var = tk.StringVar(value=msg_to_edit['category'])
        ttk.Entry(edit_win, textvariable=cat_var).pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(edit_win, text="Mensaje:").pack(anchor=tk.W, padx=10)
        text_widget = tk.Text(edit_win, height=5)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        text_widget.insert("1.0", msg_to_edit['text'])
        
        def save_edit():
            new_name = name_var.get().strip()
            new_cat = cat_var.get().strip()
            new_text = text_widget.get("1.0", tk.END).strip()
            
            if not new_name or not new_cat or not new_text:
                messagebox.showwarning("Error", "Todos los campos son obligatorios.", parent=edit_win)
                return
                
            msg_to_edit['name'] = new_name
            msg_to_edit['category'] = new_cat
            msg_to_edit['text'] = new_text
            
            self.save_data()
            self.data = self.load_data() # Recarga forzada
            self.update_categories()
            self.refresh_list()
            edit_win.destroy()
            
        ttk.Button(edit_win, text="Guardar cambios", command=save_edit).pack(pady=10)

    def paste_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
            
        msg_id = int(self.tree.item(selected[0], "tags")[0])
        item = self.tree.item(selected[0])
        msg_text = item['values'][1]
        
        for m in self.data:
            if m['id'] == msg_id:
                m['count'] += 1
                break
        
        self.save_data()
        self.data = self.load_data() # Recarga forzada (opcional aquí, pero mantiene consistencia)
        self.refresh_list()
        
        self.root.clipboard_clear()
        self.root.clipboard_append(msg_text)
        
        keyboard.release('ctrl')
        keyboard.release('space')
        keyboard.release('p')
        time.sleep(0.1) 
        
        keyboard.send('alt+tab')
        time.sleep(0.2)
        keyboard.send('ctrl+v')

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardManager(root)
    root.mainloop()