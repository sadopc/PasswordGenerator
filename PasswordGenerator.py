import customtkinter as ctk
from tkinter import messagebox
import random
import string
import pyperclip

# Tema ve görünüm ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def animate_sifre(final_sifre, iteration=0, max_iterations=8):
    if iteration < max_iterations:
        # Generate a random string of the same length as the final password
        temp_sifre = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) 
                            for _ in range(len(final_sifre)))
        sifre_entry.delete(0, ctk.END)
        sifre_entry.insert(0, temp_sifre)
        pencere.after(40, lambda: animate_sifre(final_sifre, iteration + 1, max_iterations))
    else:
        # Show final password
        sifre_entry.delete(0, ctk.END)
        sifre_entry.insert(0, final_sifre)
        sifre_entry.configure(text_color="white")

def sifre_olustur():
    uzunluk = int(uzunluk_slider.get())
    karakterler = ''
    if rakam_var.get():
        karakterler += string.digits
    if buyuk_harf_var.get():
        karakterler += string.ascii_uppercase
    if kucuk_harf_var.get():
        karakterler += string.ascii_lowercase
    if sembol_var.get():
        karakterler += string.punctuation

    if not karakterler:
        sifre_entry.delete(0, ctk.END)
        sifre_entry.insert(0, "Lütfen en az bir karakter türü seçin!")
        sifre_entry.configure(text_color="red")
        return

    final_sifre = ''.join(random.choice(karakterler) for _ in range(uzunluk))
    
    # Start the animation
    olustur_button.configure(state="disabled")  # Disable button during animation
    animate_sifre(final_sifre)
    pencere.after(400, lambda: olustur_button.configure(state="normal"))  # Re-enable button after animation

def sifreyi_kopyala():
    sifre = sifre_entry.get()
    if sifre and sifre != "Lütfen en az bir karakter türü seçin!":
        pyperclip.copy(sifre)
        bildirim_label.configure(text="✓ Kopyalandı", 
                               text_color="#00FF00",
                               font=ctk.CTkFont(size=14, weight="bold"))
        # 2 saniye sonra bildirimi temizle
        pencere.after(2000, lambda: bildirim_label.configure(text=""))
    else:
        bildirim_label.configure(text="❌", 
                               text_color="red",
                               font=ctk.CTkFont(size=14, weight="bold"))
        pencere.after(2000, lambda: bildirim_label.configure(text=""))

# Ana pencere
pencere = ctk.CTk()
pencere.title("Rastgele Şifre Oluşturucu")
pencere.geometry("500x650")

# Ana çerçeve
ana_cerceve = ctk.CTkFrame(pencere)
ana_cerceve.pack(fill="both", expand=True, padx=20, pady=20)

# Başlık
baslik = ctk.CTkLabel(ana_cerceve, text="Şifre Oluşturucu", font=ctk.CTkFont(size=24, weight="bold"))
baslik.pack(pady=20)

# Karakter seçenekleri çerçevesi
karakter_cercevesi = ctk.CTkFrame(ana_cerceve)
karakter_cercevesi.pack(fill="x", padx=20, pady=10)

karakter_baslik = ctk.CTkLabel(karakter_cercevesi, text="Karakter Seçenekleri", 
                              font=ctk.CTkFont(size=16, weight="bold"))
karakter_baslik.pack(pady=10)

# Seçenekler
rakam_var = ctk.BooleanVar(value=True)
buyuk_harf_var = ctk.BooleanVar(value=True)
kucuk_harf_var = ctk.BooleanVar(value=True)
sembol_var = ctk.BooleanVar(value=False)

rakam_check = ctk.CTkCheckBox(karakter_cercevesi, text="Rakamlar (123)", variable=rakam_var)
rakam_check.pack(anchor="w", pady=5, padx=20)

buyuk_harf_check = ctk.CTkCheckBox(karakter_cercevesi, text="Büyük Harf (ABC)", variable=buyuk_harf_var)
buyuk_harf_check.pack(anchor="w", pady=5, padx=20)

kucuk_harf_check = ctk.CTkCheckBox(karakter_cercevesi, text="Küçük Harf (abc)", variable=kucuk_harf_var)
kucuk_harf_check.pack(anchor="w", pady=5, padx=20)

sembol_check = ctk.CTkCheckBox(karakter_cercevesi, text="Semboller (!@#)", variable=sembol_var)
sembol_check.pack(anchor="w", pady=5, padx=20)

# Uzunluk ayarları
uzunluk_cercevesi = ctk.CTkFrame(ana_cerceve)
uzunluk_cercevesi.pack(fill="x", padx=20, pady=20)

uzunluk_baslik = ctk.CTkLabel(uzunluk_cercevesi, text="Şifre Uzunluğu", 
                             font=ctk.CTkFont(size=16, weight="bold"))
uzunluk_baslik.pack(pady=10)

uzunluk_slider = ctk.CTkSlider(uzunluk_cercevesi, from_=8, to=32, number_of_steps=24)
uzunluk_slider.set(12)
uzunluk_slider.pack(fill="x", padx=20, pady=10)

uzunluk_deger = ctk.CTkLabel(uzunluk_cercevesi, text="12 karakter")
uzunluk_deger.pack()

# Slider değeri değiştiğinde etiketi güncelle
def slider_event(value):
    uzunluk_deger.configure(text=f"{int(value)} karakter")
uzunluk_slider.configure(command=slider_event)

# Butonlar
buton_cercevesi = ctk.CTkFrame(ana_cerceve)
buton_cercevesi.pack(fill="x", padx=20, pady=20)

olustur_button = ctk.CTkButton(buton_cercevesi, text="Şifre Oluştur", 
                              command=sifre_olustur, height=40)
olustur_button.pack(side="left", expand=True, padx=5)

kopyala_button = ctk.CTkButton(buton_cercevesi, text="Kopyala", 
                              command=sifreyi_kopyala, height=40)
kopyala_button.pack(side="left", expand=True, padx=5)

# Şifre gösterimi
sifre_cercevesi = ctk.CTkFrame(ana_cerceve)
sifre_cercevesi.pack(fill="x", padx=20, pady=10)

sifre_baslik = ctk.CTkLabel(sifre_cercevesi, text="Oluşturulan Şifre:", 
                           font=ctk.CTkFont(size=16, weight="bold"))
sifre_baslik.pack(pady=10)

# Şifre kutusu ve bildirim için frame
sifre_kutusu_frame = ctk.CTkFrame(sifre_cercevesi)
sifre_kutusu_frame.pack(fill="x", padx=20, pady=5)

sifre_entry = ctk.CTkEntry(sifre_kutusu_frame, height=40, font=ctk.CTkFont(size=16))
sifre_entry.pack(side="left", fill="x", expand=True)

bildirim_label = ctk.CTkLabel(sifre_kutusu_frame, text="", width=100)
bildirim_label.pack(side="right", padx=10)

# Durum etiketi ana_cerceve içinde oluşturuluyor
sifre_durum_etiketi = ctk.CTkLabel(ana_cerceve, text="", 
                                  font=ctk.CTkFont(size=14, weight="bold"))
sifre_durum_etiketi.pack(pady=10)

pencere.mainloop()