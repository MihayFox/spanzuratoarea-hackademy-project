import tkinter as tk
import random

def incarca_cuvinte(din_fisier):
    with open(din_fisier, "r", encoding="utf-8") as f:
        cuvinte = [linie.strip() for linie in f if linie.strip()]
    return list(set(cuvinte))

cuvinte = incarca_cuvinte("substantive.txt")

class SpanzuratoareaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spânzurătoarea Completă")
        self.canvas = None
        self.creeaza_ui()
        self.reset_joc()

    def creeaza_ui(self):
        self.label_titlu = tk.Label(self.root, text="Spânzurătoarea", font=("Helvetica", 20))
        self.label_titlu.pack(pady=10)

        self.stare_var = tk.StringVar()
        self.label_stare = tk.Label(self.root, textvariable=self.stare_var, font=("Courier", 24))
        self.label_stare.pack(pady=10)

        self.incercari_var = tk.StringVar()
        self.label_incercari = tk.Label(self.root, textvariable=self.incercari_var, font=("Helvetica", 14))
        self.label_incercari.pack(pady=5)

        self.entry = tk.Entry(self.root, font=("Helvetica", 14), justify="center")
        self.entry.pack(pady=5)

        self.buton_litera = tk.Button(self.root, text="Ghiceste litera", command=self.verifica_litera)
        self.buton_litera.pack(pady=5)

        self.buton_cuvant = tk.Button(self.root, text="Ghiceste cuvantul complet", command=self.verifica_cuvant)
        self.buton_cuvant.pack(pady=5)

        self.mesaj_var = tk.StringVar()
        self.label_mesaj = tk.Label(self.root, textvariable=self.mesaj_var, font=("Helvetica", 12), fg="blue")
        self.label_mesaj.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=200, height=250)
        self.canvas.pack()
        self.deseneaza_spanzuratoarea()

        self.buton_restart = tk.Button(self.root, text="Restart joc", command=self.reset_joc)
        self.buton_restart.pack(pady=10)

    def reset_joc(self):
        self.cuvant = random.choice(cuvinte)
        self.litere_ghicite = []
        self.incercari = 7
        self.stare_var.set(self.afiseaza_stare())
        self.incercari_var.set(f"Încercări rămase: {self.incercari}")
        self.mesaj_var.set("")
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.buton_litera.config(state="normal")
        self.buton_cuvant.config(state="normal")
        if self.canvas:
            self.canvas.delete("all")
            self.deseneaza_spanzuratoarea()
        print(f"[DEBUG] Cuvânt ales: {self.cuvant}")

    def afiseaza_stare(self):
        return " ".join([lit if lit in self.litere_ghicite else "_" for lit in self.cuvant])

    def verifica_litera(self):
        litera = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if len(litera) != 1 or not litera.isalpha():
            self.mesaj_var.set("Introduce o literă validă.")
            return

        if litera in self.litere_ghicite:
            self.mesaj_var.set("Ai mai ghicit litera aceasta.")
            return

        self.litere_ghicite.append(litera)

        if litera in self.cuvant:
            self.mesaj_var.set("Litera este corectă!")
        else:
            self.incercari -= 1
            self.mesaj_var.set(f"Litera greșită. Încercări rămase: {self.incercari}")
            self.deseneaza_spanzurat_parta()

        self.actualizeaza_stare()

    def verifica_cuvant(self):
        cuvant_introdus = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if cuvant_introdus == self.cuvant:
            self.stare_var.set(self.cuvant)
            self.mesaj_var.set("Felicitări! Ai ghicit cuvântul complet!")
            self.salveaza_scor("castigat")
            self.blocheaza_joc()
        else:
            self.incercari -= 1
            self.mesaj_var.set(f"Nu este corect. Încercări rămase: {self.incercari}")
            self.deseneaza_spanzurat_parta()
            self.actualizeaza_stare()

    def actualizeaza_stare(self):
        self.stare_var.set(self.afiseaza_stare())
        self.incercari_var.set(f"Încercări rămase: {self.incercari}")

        if "_" not in self.afiseaza_stare():
            self.mesaj_var.set("Ai câștigat! Bravo!")
            self.salveaza_scor("castigat")
            self.blocheaza_joc()
        elif self.incercari == 0:
            self.mesaj_var.set(f"Ai pierdut! Cuvântul era: {self.cuvant}")
            self.stare_var.set(self.cuvant)
            self.salveaza_scor("pierdut")
            self.deseneaza_spanzurat_parta()
            self.blocheaza_joc()

    def blocheaza_joc(self):
        self.entry.config(state="disabled")
        self.buton_litera.config(state="disabled")
        self.buton_cuvant.config(state="disabled")

    def deseneaza_spanzuratoarea(self):
        self.canvas.create_line(20, 230, 180, 230)
        self.canvas.create_line(50, 230, 50, 30)
        self.canvas.create_line(50, 30, 130, 30)
        self.canvas.create_line(130, 30, 130, 50)

    def deseneaza_spanzurat_parta(self):
        p = 7 - self.incercari
        if p == 1:
            self.canvas.create_oval(110, 50, 150, 90)
        elif p == 2:
            self.canvas.create_line(130, 90, 130, 150)
        elif p == 3:
            self.canvas.create_line(130, 100, 110, 130)
        elif p == 4:
            self.canvas.create_line(130, 100, 150, 130)
        elif p == 5:
            self.canvas.create_line(130, 150, 110, 190)
        elif p == 6:
            self.canvas.create_line(130, 150, 150, 190)
        elif p == 7:
            self.canvas.create_text(100, 10, text="GAME OVER", font=("Arial", 16), fill="red")

    def salveaza_scor(self, rezultat):
        with open("scoruri.txt", "a", encoding="utf-8") as f:
            f.write(f"Rezultat: {rezultat}, Cuvânt: {self.cuvant}\n")

root = tk.Tk()
app = SpanzuratoareaApp(root)
root.mainloop()
