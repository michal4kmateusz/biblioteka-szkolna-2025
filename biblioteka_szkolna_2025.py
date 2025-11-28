import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from datetime import date, timedelta, datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import winsound

# =============================================
# LOGOWANIE - BEZ ZMIAN
# =============================================
def ekran_logowania():
    login_win = tk.Tk()
    login_win.title("Logowanie – Biblioteka Szkolna 2025")
    login_win.geometry("450x600")
    login_win.configure(bg="#667eea")
    login_win.resizable(False, False)

    tk.Label(login_win, text="BIBLIOTEKA SZKOLNA", 
             font=("Segoe UI", 28, "bold"), fg="white", bg="#667eea").pack(pady=60)
    tk.Label(login_win, text="System zarządzania wypożyczeniami", 
             font=("Segoe UI", 12), fg="#e0d6ff", bg="#667eea").pack(pady=10)

    tk.Label(login_win, text="Login", font=("Segoe UI", 14), fg="white", bg="#667eea").pack(pady=(40,5))
    login_e = tk.Entry(login_win, font=("Segoe UI", 14), width=28, justify="center", relief="solid", bd=2)
    login_e.pack(pady=5)
    login_e.focus_set()

    tk.Label(login_win, text="Hasło", font=("Segoe UI", 14), fg="white", bg="#667eea").pack(pady=(25,5))
    haslo_e = tk.Entry(login_win, font=("Segoe UI", 14), width=28, justify="center", show="*", relief="solid", bd=2)
    haslo_e.pack(pady=5)

    def sprawdz():
        if login_e.get().strip() and haslo_e.get().strip():
            login_win.destroy()
            uruchom_aplikacje()
        else:
            messagebox.showwarning("Uwaga", "Wpisz login i hasło!")
            login_e.delete(0, "end")
            haslo_e.delete(0, "end")
            login_e.focus_set()

    login_e.bind("<Return>", lambda event: haslo_e.focus_set())
    haslo_e.bind("<Return>", lambda event: sprawdz())

    przycisk_frame = tk.Frame(login_win, bg="#667eea")
    przycisk_frame.pack(pady=30)
    
    tk.Button(przycisk_frame, text="ZATWIERDŹ", 
              font=("Segoe UI", 18, "bold"),
              bg="#27ae60", fg="white",
              activebackground="#2ecc71",
              activeforeground="white",
              command=sprawdz, 
              width=10, height=1,
              relief="raised", bd=4,
              cursor="hand2").pack()

    login_win.mainloop()

# =============================================
# FUNKCJA WYLOGOWANIA
# =============================================
def wyloguj():
    """Zamyka aplikację główną i wraca do ekranu logowania"""
    if messagebox.askyesno("Wylogowanie", "Czy na pewno chcesz się wylogować?"):
        root.destroy()
        ekran_logowania()

# =============================================
# GŁÓWNA APLIKACJA - WYLOGUJ POD WYPOŻYCZ
# =============================================
def uruchom_aplikacje():
    # DANE TESTOWE - ZAWSZE DZIAŁAJĄ
    klienci = [
        "Kowalski Jan", "Nowak Anna", "Wiśniewska Ola", "Zieliński Tomek", 
        "Jankowska Maria", "Lewandowska Zofia", "Kaczmarek Piotr"
    ]
    
    wszystkie_ksiazki = [
        "Wiedźmin: Ostatnie życzenie (INV-005)",
        "Harry Potter i Kamień Filozoficzny (INV-007)",
        "Pan Tadeusz (INV-009)",
        "Quo vadis (INV-001)",
        "Solaris – Stanisław Lem (INV-003)",
        "Bieguni – Olga Tokarczuk (INV-004)",
        "Lalka – Bolesław Prus (INV-010)",
        "Ferdydurke – Witold Gombrowicz (INV-012)",
        "Dziady cz. III (INV-015)"
    ]
    
    wypozyczenia = [
        {"uczen": "Kowalski Jan", "ksiazka": "Solaris – Stanisław Lem (INV-003)", "do_kiedy": date.today() - timedelta(days=12)},
        {"uczen": "Nowak Anna", "ksiazka": "Bieguni – Olga Tokarczuk (INV-004)", "do_kiedy": date.today() + timedelta(days=8)},
        {"uczen": "Wiśniewska Ola", "ksiazka": "Harry Potter i Kamień Filozoficzny (INV-007)", "do_kiedy": date.today() - timedelta(days=3)},
    ]

    # === FUNKCJE ===
    def dostepne_ksiazki():
        zajete = {w["ksiazka"] for w in wypozyczenia}
        return [k for k in wszystkie_ksiazki if k not in zajete]

    def odswiez_wszystko():
        nonlocal klienci, wszystkie_ksiazki, wypozyczenia
        uczen_cb["values"] = klienci
        ksiazka_cb["values"] = dostepne_ksiazki()
        update_zwrot()
        odswiez_tabele()
        aktywne_lbl.config(text=len(wypozyczenia))
        przetrzymane_lbl.config(text=sum(1 for w in wypozyczenia if (date.today() - w["do_kiedy"]).days > 0))
        odswiez_liste_klientow()
        odswiez_liste_ksiazek()

    def odswiez_tabele():
        for i in tree.get_children():
            tree.delete(i)
        szukaj = search_var.get().lower()
        for w in wypozyczenia:
            if szukaj in w["uczen"].lower() or szukaj in w["ksiazka"].lower():
                dni = max(0, (date.today() - w["do_kiedy"]).days)
                tag = "przetrzymane" if dni > 0 else ""
                tree.insert("", "end", values=(
                    w["uczen"],
                    w["ksiazka"],
                    w["do_kiedy"].strftime("%d.%m.%Y"),
                    dni,
                    f"{dni*1.0:.2f} zł"
                ), tags=(tag,))

    def update_zwrot():
        zwrot_cb["values"] = [f"{w['uczen']} → {w['ksiazka']} (do {w['do_kiedy'].strftime('%d.%m.%Y')})" for w in wypozyczenia]

    def odswiez_liste_klientow():
        for i in tree_klientow.get_children():
            tree_klientow.delete(i)
        for klient in sorted(klienci):
            tree_klientow.insert("", "end", values=(klient,))

    def odswiez_liste_ksiazek():
        for i in tree_ksiazek.get_children():
            tree_ksiazek.delete(i)
        for ksiazka in sorted(wszystkie_ksiazki):
            tree_ksiazek.insert("", "end", values=(ksiazka,))

    def dodaj_ucznia():
        imie = simpledialog.askstring("Nowy uczeń", "Podaj imię i nazwisko:")
        if imie and imie.strip() and imie.strip() not in klienci:
            klienci.append(imie.strip())
            odswiez_wszystko()
            messagebox.showinfo("Gotowe", f"Dodano: {imie.strip()}")

    def dodaj_ksiazke():
        tytul = simpledialog.askstring("Nowa książka", "Tytuł i numer inwentarza (np. Hobbit (INV-999)):")
        if tytul and tytul.strip() and tytul.strip() not in wszystkie_ksiazki:
            wszystkie_ksiazki.append(tytul.strip())
            odswiez_wszystko()
            messagebox.showinfo("Gotowe", f"Dodano książkę:\n{tytul.strip()}")

    def wypozycz():
        uczen = uczen_cb.get()
        ksiazka = ksiazka_cb.get()
        if not uczen or not ksiazka:
            messagebox.showwarning("Uwaga", "Wybierz ucznia i książkę!")
            return
        wypozyczenia.append({"uczen": uczen, "ksiazka": ksiazka, "do_kiedy": date.today() + timedelta(days=30)})
        winsound.Beep(1200, 300)
        messagebox.showinfo("WYPOŻYCZONO!", f"{uczen}\n→ {ksiazka}")
        odswiez_wszystko()
        uczen_cb.set(""); ksiazka_cb.set("")

    def oddaj():
        sel = zwrot_cb.get()
        if not sel:
            messagebox.showwarning("Uwaga", "Wybierz wypożyczenie!")
            return
        for w in wypozyczenia[:]:
            if w["uczen"] in sel and w["ksiazka"] in sel:
                wypozyczenia.remove(w)
                winsound.Beep(1500, 400)
                messagebox.showinfo("ZWROT!", f"Zwrócono:\n{w['ksiazka']}")
                odswiez_wszystko()
                zwrot_cb.set("")
                break

    def eksport_pdf():
        plik = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not plik: return
        doc = SimpleDocTemplate(plik, pagesize=A4)
        elementy = []
        style = getSampleStyleSheet()
        elementy.append(Paragraph(f"BIBLIOTEKA SZKOLNA – {date.today().strftime('%d.%m.%Y')}", style['Title']))
        elementy.append(Spacer(1, 30))
        dane = [["Uczeń", "Książka", "Termin zwrotu", "Dni po", "Kara"]]
        for w in wypozyczenia:
            dni = max(0, (date.today() - w["do_kiedy"]).days)
            dane.append([w["uczen"], w["ksiazka"], w["do_kiedy"].strftime("%d.%m.%Y"), str(dni), f"{dni*1.0:.2f} zł"])
        t = Table(dane)
        t.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 1, colors.grey),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#667eea")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ]))
        elementy.append(t)
        doc.build(elementy)
        messagebox.showinfo("Gotowe!", "PDF zapisany!")
        os.startfile(plik)

    # === OKNO GŁÓWNE ===
    global root
    root = tk.Tk()
    root.title("Biblioteka Szkolna 2025")
    root.geometry("1600x850")
    root.configure(bg="#f4f6f9")

    main_container = tk.Frame(root, bg="#f4f6f9")
    main_container.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_container, bg="#f4f6f9", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg="#f4f6f9")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", on_configure)

    def on_canvas_configure(event):
        canvas.itemconfig(canvas.find_withtag("all"), width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    # === NAGŁÓWEK ===
    header = tk.Canvas(scrollable_frame, height=120, bg="#667eea", highlightthickness=0)
    header.pack(fill="x")
    header.create_rectangle(0, 0, 2000, 120, fill="#667eea", outline="")
    header.create_rectangle(0, 0, 2000, 120, fill="#764ba2", outline="", stipple="gray50")
    header.create_text(60, 60, text="BIBLIOTEKA SZKOLNA", font=("Segoe UI", 36, "bold"), fill="white", anchor="w")
    header.create_text(60, 95, text="System zarządzania wypożyczeniami 2025", font=("Segoe UI", 14), fill="#e0d6ff", anchor="w")

    def clock():
        now = datetime.now().strftime("%d.%m.%Y | %H:%M:%S")
        clock_label.config(text=now)
        root.after(1000, clock)
    clock_label = tk.Label(header, font=("Consolas", 16, "bold"), fg="white", bg="#667eea")
    clock_label.place(x=1250, y=70)
    clock()

    # === STATYSTYKI ===
    stats_frame = tk.Frame(scrollable_frame, bg="#f4f6f9")
    stats_frame.pack(pady=25)
    tk.Label(stats_frame, text="Aktywne:", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").grid(row=0, column=0, padx=40)
    aktywne_lbl = tk.Label(stats_frame, text="0", font=("Segoe UI", 48, "bold"), fg="#667eea", bg="#f4f6f9")
    aktywne_lbl.grid(row=0, column=1)
    tk.Label(stats_frame, text=" | Przetrzymane:", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").grid(row=0, column=2, padx=40)
    przetrzymane_lbl = tk.Label(stats_frame, text="0", font=("Segoe UI", 48, "bold"), fg="#e74c3c", bg="#f4f6f9")
    przetrzymane_lbl.grid(row=0, column=3)

    # === LEWY PANELE Z LISTAMI ===
    left_panel = tk.Frame(scrollable_frame, bg="#f4f6f9")
    left_panel.pack(side="left", padx=20, pady=20, fill="y")

    klienci_frame = tk.LabelFrame(left_panel, text="👥 Lista wszystkich klientów", font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50")
    klienci_frame.pack(fill="both", expand=True, pady=(0, 15))

    tree_klientow = ttk.Treeview(klienci_frame, columns=("klient",), show="headings", height=6)
    tree_klientow.heading("klient", text="Imię i nazwisko")
    tree_klientow.column("klient", width=220)
    tree_klientow.pack(padx=10, pady=10, fill="both", expand=True)

    ksiazki_frame = tk.LabelFrame(left_panel, text="📚 Lista wszystkich książek", font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50")
    ksiazki_frame.pack(fill="both", expand=True)

    tree_ksiazek = ttk.Treeview(ksiazki_frame, columns=("ksiazka",), show="headings", height=6)
    tree_ksiazek.heading("ksiazka", text="Tytuł (numer inwentarza)")
    tree_ksiazek.column("ksiazka", width=220)
    tree_ksiazek.pack(padx=10, pady=10, fill="both", expand=True)

    # === DODAWANIE ===
    add_frame = tk.Frame(scrollable_frame, bg="#f4f6f9")
    add_frame.pack(pady=10)
    tk.Button(add_frame, text="+ Dodaj ucznia", bg="#9b59b6", fg="white", font=("Segoe UI", 13, "bold"), width=18, command=dodaj_ucznia).pack(side="left", padx=30)
    tk.Button(add_frame, text="+ Dodaj książkę", bg="#9b59b6", fg="white", font=("Segoe UI", 13, "bold"), width=18, command=dodaj_ksiazke).pack(side="left", padx=30)

    # === WYSZUKIWARKA ===
    search_frame = tk.Frame(scrollable_frame, bg="#f4f6f9")
    search_frame.pack(pady=10)
    tk.Label(search_frame, text="Szukaj:", font=("Segoe UI", 14, "bold"), bg="#f4f6f9").pack(side="left", padx=20)
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, font=("Segoe UI", 14), width=50).pack(side="left", padx=10)

    # === TABELA ===
    tree_frame = tk.LabelFrame(scrollable_frame, text=" 📋 Aktualnie wypożyczone książki ", font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50")
    tree_frame.pack(padx=40, pady=15, fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("uczen","ksiazka","do","dni","kara"), show="headings")
    tree.heading("uczen", text="Uczeń"); tree.heading("ksiazka", text="Książka"); tree.heading("do", text="Do kiedy")
    tree.heading("dni", text="Dni po"); tree.heading("kara", text="Kara")
    tree.column("uczen", width=230, anchor="center"); tree.column("ksiazka", width=620)
    tree.column("do", width=160, anchor="center"); tree.column("dni", width=130, anchor="center"); tree.column("kara", width=140, anchor="center")
    tree.pack(padx=30, pady=25, fill="both", expand=True)
    tree.tag_configure("przetrzymane", background="#ff6b6b", foreground="white", font=("Segoe UI", 11, "bold"))

    # === PRZYCISKI - WYLOGUJ POD WYPOŻYCZ ===
    buttons_frame = tk.Frame(scrollable_frame, bg="#f4f6f9")
    buttons_frame.pack(pady=40)

    # Combobox'y
    uczen_frame = tk.Frame(buttons_frame, bg="#f4f6f9")
    uczen_frame.pack(side="left", padx=(0, 20))
    tk.Label(uczen_frame, text="Wypożycz:", font=("Segoe UI", 14, "bold"), bg="#f4f6f9").pack()
    uczen_cb = ttk.Combobox(uczen_frame, values=klienci, state="readonly", width=35, font=("Segoe UI", 13))
    uczen_cb.pack(pady=(5, 0))

    ksiazka_frame = tk.Frame(buttons_frame, bg="#f4f6f9")
    ksiazka_frame.pack(side="left", padx=(0, 30))
    tk.Label(ksiazka_frame, text="Książka:", font=("Segoe UI", 14, "bold"), bg="#f4f6f9").pack()
    ksiazka_cb = ttk.Combobox(ksiazka_frame, state="readonly", width=60, font=("Segoe UI", 13))
    ksiazka_cb.pack(pady=(5, 0))

    # LEWA KOLUMNA: WYPOŻYCZ + WYLOGUJ POD NIM
    left_buttons = tk.Frame(buttons_frame, bg="#f4f6f9")
    left_buttons.pack(side="left", padx=10)

    btn_wypozycz = tk.Button(left_buttons, text="✅\nWYPOŻYCZ", bg="#27ae60", fg="white", 
                             font=("Segoe UI", 14, "bold"), width=12, height=2, 
                             relief="raised", bd=6, command=wypozycz)
    btn_wypozycz.pack(pady=5)

    btn_wyloguj = tk.Button(left_buttons, text="🚪\nWYLOGUJ", bg="#f39c12", fg="white", 
                           font=("Segoe UI", 14, "bold"), width=12, height=2, 
                           relief="raised", bd=6, command=wyloguj)
    btn_wyloguj.pack(pady=5)

    # PRAWA KOLUMNA: ODDAJ
    right_buttons = tk.Frame(buttons_frame, bg="#f4f6f9")
    right_buttons.pack(side="left", padx=20)

    # Combobox zwrot
    zwrot_frame = tk.Frame(right_buttons, bg="#f4f6f9")
    zwrot_frame.pack(pady=(0, 10))
    tk.Label(zwrot_frame, text="Zwrot:", font=("Segoe UI", 14, "bold"), bg="#f4f6f9").pack()
    zwrot_cb = ttk.Combobox(zwrot_frame, state="readonly", width=70, font=("Segoe UI", 13))
    zwrot_cb.pack(pady=(5, 0))

    btn_oddaj = tk.Button(right_buttons, text="🔄\nODDAJ", bg="#e74c3c", fg="white", 
                          font=("Segoe UI", 14, "bold"), width=12, height=2, 
                          relief="raised", bd=6, command=oddaj)
    btn_oddaj.pack(pady=5)

    # === PDF ===
    pdf_frame = tk.Frame(scrollable_frame, bg="#f4f6f9")
    pdf_frame.pack(pady=40)
    tk.Button(pdf_frame, text="📄 EKSPORTUJ DO PDF", bg="#9b59b6", fg="white", font=("Segoe UI", 16, "bold"), relief="raised", bd=10, command=eksport_pdf).pack()

    # === START ===
    search_var.trace("w", lambda *a: odswiez_tabele())
    odswiez_wszystko()
    root.mainloop()

# =============================================
# URUCHOMIENIE
# =============================================
if __name__ == "__main__":
    ekran_logowania()
