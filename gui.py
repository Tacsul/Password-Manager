import customtkinter as ctk
from tkinter import messagebox
# Importăm funcțiile tale logice din login.py
from login import verify_login, register_user, verify_user, add_password_safe, print_safe, json

# --- CONFIGURARE TEMĂ ȘI DESIGN ---
ctk.set_appearance_mode("dark")  # Setează modul Dark în mod explicit
ctk.set_default_color_theme("blue")  # Temă de culori pentru butoane/elemente

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Vault - Password Manager")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # Variabilă pentru a ține minte utilizatorul logat curent
        self.current_user = None

        # Pornim cu ecranul de Login
        self.afiseaza_ecran_login()

    def curata_ecran(self):
        """Șterge toate elementele grafice de pe ecran pentru a face loc altora."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- 1. ECRANUL DE LOGIN / ÎNREGISTRARE ---
    def afiseaza_ecran_login(self):
        self.curata_ecran()

        # Titlu
        titlu = ctk.CTkLabel(self.root, text="🔐 SECURE VAULT", font=("Arial", 24, "bold"))
        titlu.pack(pady=(40, 20))

        subtitlu = ctk.CTkLabel(self.root, text="Introduceți datele de master user", font=("Arial", 12))
        subtitlu.pack(pady=(0, 20))

        # Câmpuri de text (Inputs)
        self.entry_user = ctk.CTkEntry(self.root, placeholder_text="Master Username", width=300, height=40)
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self.root, placeholder_text="Master Password", show="*", width=300, height=40)
        self.entry_pass.pack(pady=10)

        # Butoane
        btn_login = ctk.CTkButton(self.root, text="Autentificare", command=self.proceseaza_login, width=300, height=40, font=("Arial", 14, "bold"))
        btn_login.pack(pady=(20, 10))

        btn_register = ctk.CTkButton(self.root, text="Creează Cont Nou", fg_color="transparent", border_width=2, command=self.proceseaza_inregistrare, width=300, height=40)
        btn_register.pack(pady=10)

    def proceseaza_login(self):
        user = self.entry_user.get().strip()
        parola = self.entry_pass.get().strip()

        if not user or not parola:
            messagebox.showwarning("Atenție", "Te rugăm să completezi toate câmpurile!")
            return

        if verify_login(user, parola):
            self.current_user = user
            self.afiseaza_ecran_seif()  # Mergem la seif dacă logarea e corectă
        else:
            messagebox.showerror("Eroare", "Master Username sau Parolă incorectă!")

    def proceseaza_inregistrare(self):
        user = self.entry_user.get().strip()
        parola = self.entry_pass.get().strip()

        if not user or not parola:
            messagebox.showwarning("Atenție", "Completează ambele câmpuri pentru înregistrare!")
            return

        if verify_user(user):
            messagebox.showerror("Eroare", "Acest Master Username este deja luat!")
        else:
            register_user(user, parola)
            messagebox.showinfo("Succes", f"Contul '{user}' a fost creat! Acum te poți autentifica.")

    # --- 2. ECRANUL PRINCIPAL AL SEIFULUI ---
    def afiseaza_ecran_seif(self):
        self.curata_ecran()

        # Header Seif
        header = ctk.CTkLabel(self.root, text=f"Seiful lui {self.current_user.upper()}", font=("Arial", 20, "bold"), text_color="#1f538d")
        header.pack(pady=(20, 10))

        # --- Zona de adăugare parolă nouă ---
        frame_add = ctk.CTkFrame(self.root)
        frame_add.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_add, text="Adaugă un cont nou în seif:", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.entry_site = ctk.CTkEntry(frame_add, placeholder_text="Nume Site (ex: Facebook, Google)", width=260)
        self.entry_site.pack(pady=5)
        
        self.entry_site_user = ctk.CTkEntry(frame_add, placeholder_text="Username / Email cont", width=260)
        self.entry_site_user.pack(pady=5)
        
        self.entry_site_pass = ctk.CTkEntry(frame_add, placeholder_text="Parolă cont", show="*", width=260)
        self.entry_site_pass.pack(pady=5)

        btn_salveaza = ctk.CTkButton(frame_add, text="🔒 Salvează în siguranță", command=self.salveaza_parola_in_seif, fg_color="#228B22", hover_color="#006400")
        btn_salveaza.pack(pady=10)

        # --- Zona de afișare/vizualizare ---
        btn_vezi_parole = ctk.CTkButton(self.root, text="👁️ Vezi parolele în consolă", command=self.afiseaza_in_consola, width=200)
        btn_vezi_parole.pack(pady=10)

        # Buton Deconectare
        btn_logout = ctk.CTkButton(self.root, text="Deconectare", fg_color="#8B0000", hover_color="#550000", command=self.afiseaza_ecran_login)
        btn_logout.pack(pady=(20, 10))

    def salveaza_parola_in_seif(self):
        site = self.entry_site.get().strip()
        site_user = self.entry_site_user.get().strip()
        site_pass = self.entry_site_pass.get().strip()

        if not site or not site_user or not site_pass:
            messagebox.showwarning("Atenție", "Completează toate datele contului!")
            return

        # Apelăm funcția ta originală din login.py (care face criptarea Fernet)
        add_password_safe(self.current_user, site, site_user, site_pass)
        messagebox.showinfo("Succes", f"Datele pentru {site} au fost criptate și salvate!")
        
        # Resetăm câmpurile de adăugare
        self.entry_site.delete(0, 'end')
        self.entry_site_user.delete(0, 'end')
        self.entry_site_pass.delete(0, 'end')

    def afiseaza_in_consola(self):
        """Folosește funcția ta curentă ca să printeze parolele decriptate în terminal."""
        print_safe(self.current_user)
        messagebox.showinfo("Info", "Parolele decriptate au fost listate în terminalul tău VS Code!")

# --- PORNIREA APLICAȚIEI ---
if __name__ == "__main__":
    root = ctk.CTk()
    app = PasswordManagerGUI(root)
    root.mainloop()