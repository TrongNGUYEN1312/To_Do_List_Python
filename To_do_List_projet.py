
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import os


class ToDoList:
    def __init__(self, filename="Liste_Tache.txt"):
        self.root = Tk()
        self.root.title('ToDoList')
        self.root.geometry("500x850")
        self.root.configure(bg="#f0f2f5")
        self.filename = filename

        # Historique pour l'annulation (Undo)
        self.history = []

        # Denifir font et Couleurs
        self.font_title = Font(family="Segoe UI", size=24, weight="bold")
        self.font_text = Font(family="Segoe UI", size=14)
        self.font_btn = Font(family="Segoe UI", size=10, weight="bold")

        self.col_bg = "#f0f2f5"
        self.col_primary = "#4a90e2"  # Bleu
        self.col_success = "#2ecc71"  # Vert
        self.col_danger = "#e74c3c"  # Rouge
        self.col_warning = "#f1c40f"  # Jaune
        self.col_text = "#2c3e50"

        #En-tête
        Label(self.root, text="To-do list", font=self.font_title,
              bg=self.col_bg, fg=self.col_text).pack(pady=20)

        #Zone de saisie
        frame_entry = Frame(self.root, bg=self.col_bg)
        frame_entry.pack(pady=10)

        self.my_entry = Entry(frame_entry, font=self.font_text, width=28, bd=0, highlightthickness=1)
        self.my_entry.config(highlightbackground="#d1d8e0", highlightcolor=self.col_primary)
        self.my_entry.pack(side=LEFT, padx=10, ipady=5)

        #Touche Entrée pour ajouter
        self.my_entry.bind('<Return>', lambda event: self.add_item())
        
        #Frame des taches
        frame_list = Frame(self.root, bg="white")
        frame_list.pack(pady=10, padx=20, fill=BOTH, expand=True)
        
        # Scrollbar
        self.my_scrollbar = Scrollbar(frame_list)
        self.my_scrollbar.pack(side=RIGHT, fill=BOTH)
        
        
        #Liste des tâches (Listbox)
        self.my_list = Listbox(frame_list,
                               font=self.font_text,
                               width=25,
                               height=10,
                               bg="white",
                               bd=0,
                               fg=self.col_text,
                               selectbackground="#dff9fb",
                               selectforeground="#2c3e50",
                               activestyle="none",
                               yscrollcommand=self.my_scrollbar.set)

        self.my_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.my_scrollbar.config(command=self.my_list.yview)
        
        
        #Raccourcis clavier
        self.root.bind('<Delete>', lambda event: self.confirm_delete())  # Suppr
        self.root.bind('<Control-z>', lambda event: self.undo_action())  # Ctrl+Z

        #Boutons
        button_frame = Frame(self.root, bg=self.col_bg)
        button_frame.pack(pady=20, padx=20, fill=X)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        #Creer bouton
        def create_btn(text, cmd, color, row, col, colspan=1):
            btn = Button(button_frame, text=text, command=cmd,
                         bg=color, fg="white", font=self.font_btn,
                         bd=0, padx=10, pady=8, cursor="hand2", activebackground=color)
            btn.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=5, pady=5)
            return btn

        #Liste des boutons
        create_btn("➕ Ajouter", self.add_item, self.col_success, 0, 0)
        create_btn("🗑 Supprimer", self.confirm_delete, self.col_danger, 0, 1)

        create_btn("✓ Terminer", self.done_item, self.col_primary, 1, 0)
        create_btn("↺ Reprendre", self.ongoing_item, "#95a5a6", 1, 1)
        
        create_btn("★ Prioriser", self.priority_item, self.col_warning, 2, 0)
        create_btn("☆ Normal", self.remove_priority, "#7f8c8d", 2, 1)
    
        create_btn("↩ Annuler (Ctrl+Z)", self.undo_action, "#34495e", 3, 0, colspan=2)

        self.load_tasks()
        self.root.mainloop()

    #Gestion de l'historique (Undo)
    def save_snapshot(self):
        """Sauvegarder l'état actuel avant modification"""
        current_tasks = self.my_list.get(0, END)
        self.history.append(current_tasks)
        if len(self.history) > 50:  # Limite mémoire
            self.history.pop(0)

    def undo_action(self):
        """Restaurer l'état précédent"""
        if not self.history:
            messagebox.showinfo("Info", "Rien à annuler !")
            return

        last_state = self.history.pop()
        self.my_list.delete(0, END)

        priority_tasks = []
        normal_tasks = []

        # Retrier pour l'affichage correct des couleurs
        for task in last_state:
            if task.endswith("*") and not task.startswith("[✓]"):
                priority_tasks.append(task)
            else:
                normal_tasks.append(task)

        for task in priority_tasks:
            self.my_list.insert(END, task)
            self.my_list.itemconfig(END, fg="#c0392b")

        for task in normal_tasks:
            self.my_list.insert(END, task)
            idx = self.my_list.size() - 1
            if task.startswith("[✓]"):
                self.my_list.itemconfig(idx, fg="#bdc3c7")
            else:
                self.my_list.itemconfig(idx, fg=self.col_text)

        self.save_tasks_file()

    #Fonctions principales
    def load_tasks(self):
        """Charger les tâches depuis le fichier"""
        self.my_list.delete(0, END)
        if os.path.exists(self.filename):
            priority_tasks = []
            normal_tasks = []
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    task = line.strip()
                    if not task: continue
                    if not (task.startswith("[ ]") or task.startswith("[✓]")): task = "[ ] " + task
                    if task.endswith("*") and not task.startswith("[✓]"):
                        priority_tasks.append(task)
                    else:
                        normal_tasks.append(task)

            # Affichage avec couleurs
            for task in priority_tasks:
                self.my_list.insert(END, task)
                self.my_list.itemconfig(END, fg="#c0392b")
            for task in normal_tasks:
                self.my_list.insert(END, task)
                idx = self.my_list.size() - 1
                if task.startswith("[✓]"):
                    self.my_list.itemconfig(idx, fg="#bdc3c7")
                else:
                    self.my_list.itemconfig(idx, fg=self.col_text)

    def save_tasks_file(self):
        """Écriture dans le fichier texte"""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                for i in range(self.my_list.size()):
                    f.write(self.my_list.get(i) + "\n")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder: {e}")

    def add_item(self):
        """Ajouter une nouvelle tâche"""
        text = self.my_entry.get().strip()
        if text:
            self.save_snapshot()
            task = f"[ ] {text}"
            self.my_list.insert(END, task)
            self.my_entry.delete(0, END)
            self.save_tasks_file()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer une tâche!")

    def confirm_delete(self):
        """Demander confirmation avant suppression"""
        if not self.my_list.curselection():
            return

        response = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette tâche ?")
        if response == 1:
            self.save_snapshot()
            self.my_list.delete(ANCHOR)
            self.save_tasks_file()

    def done_item(self):
        """Marquer comme terminé"""
        try:
            index = self.my_list.curselection()[0]
            task = self.my_list.get(index)
            if task.startswith("[ ]"):
                self.save_snapshot()
                clean_task = task.replace("*", "")
                new_task = "[✓]" + clean_task[3:]
                self.my_list.delete(index)
                self.my_list.insert(index, new_task)
                self.my_list.itemconfig(index, fg="#bdc3c7")
                self.save_tasks_file()
        except IndexError:
            pass

    def ongoing_item(self):
        """Remettre en cours"""
        try:
            index = self.my_list.curselection()[0]
            task = self.my_list.get(index)
            if task.startswith("[✓]"):
                self.save_snapshot()
                new_task = "[ ]" + task[3:]
                self.my_list.delete(index)
                self.my_list.insert(index, new_task)
                self.my_list.itemconfig(index, fg=self.col_text)
                self.save_tasks_file()
        except IndexError:
            pass

    def priority_item(self):
        """Ajouter la priorité"""
        try:
            index = self.my_list.curselection()[0]
            task = self.my_list.get(index)
            if task.startswith("[✓]"): return
            if not task.endswith("*"):
                self.save_snapshot()
                self.my_list.delete(index)
                task = task + "*"
                self.my_list.insert(0, task)
                self.my_list.itemconfig(0, fg="#c0392b")
                self.save_tasks_file()
        except IndexError:
            pass

    def remove_priority(self):
        """Retirer la priorité"""
        try:
            index = self.my_list.curselection()[0]
            task = self.my_list.get(index)
            if task.endswith("*"):
                self.save_snapshot()
                self.my_list.delete(index)
                task = task[:-1]
                self.my_list.insert(END, task)
                self.my_list.itemconfig(END, fg=self.col_text)
                self.save_tasks_file()
        except IndexError:
            pass


if __name__ == "__main__":
    app = ToDoList()