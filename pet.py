import tkinter as tk
import random

# --- Настройки нашего питомца (с выравниванием) ---
pet_name = "Мурзик"

happy_pet = r'''
 /\_/\  
( ^.^ )       
 > ^ <        
'''
sad_pet = r'''
 /\_/\  
( T_T )       
 > _ <        
'''
sleeping_pet = r'''
 /\_/\  
( -.- ) Zzz   
 > ~ <        
'''
playing_pet = r'''
 /\_/\  
( >.< )       
 > O <        
'''

# --- Начальные характеристики питомца ---
satiety = 5
happiness = 5
energy = 5

# --- Функции-действия ---
def feed_pet():
    global satiety, energy
    satiety = min(10, satiety + 3)
    energy = min(10, energy + 1)
    update_display()

def play_with_pet():
    global happiness, energy, satiety
    if energy > 2:
        happiness = min(10, happiness + 2)
        energy = max(0, energy - 2)
        satiety = max(0, satiety - 1)
    update_display()

def sleep_pet():
    global energy, happiness
    energy = min(10, energy + 4)
    happiness = max(0, happiness - 1)
    pet_label.config(text=sleeping_pet) 
    update_stats_only()

# --- Главные функции обновления ---
def update_display():
    update_pet_art()
    update_stats_only()

def update_pet_art():
    if happiness <= 3 or satiety <= 3:
        current_pet_art = sad_pet
    elif energy <= 3:
        current_pet_art = sleeping_pet
    elif happiness >= 8:
        current_pet_art = playing_pet
    else:
        current_pet_art = happy_pet
    pet_label.config(text=current_pet_art)

def update_stats_only():
    stats_widget.config(state=tk.NORMAL)
    stats_widget.delete("1.0", tk.END)

    stats_widget.insert(tk.END, "Сытость: ", "label")
    stats_widget.insert(tk.END, '█' * satiety, "green")
    stats_widget.insert(tk.END, '░' * (10 - satiety), "grey")
    stats_widget.insert(tk.END, f" [{satiety}/10]\n", "label")

    stats_widget.insert(tk.END, "Счастье: ", "label")
    stats_widget.insert(tk.END, '♥' * happiness, "red")
    stats_widget.insert(tk.END, '♡' * (10 - happiness), "grey")
    stats_widget.insert(tk.END, f" [{happiness}/10]\n", "label")

    stats_widget.insert(tk.END, "Энергия:  ", "label")
    stats_widget.insert(tk.END, '⚡' * energy, "yellow")
    stats_widget.insert(tk.END, ' ' * (10 - energy), "grey")
    stats_widget.insert(tk.END, f" [{energy}/10]", "label")

    stats_widget.config(state=tk.DISABLED)

# --- Функция "течения времени" ---
def live_life():
    global satiety, happiness
    satiety = max(0, satiety - 1)
    if energy > 0:
        happiness = max(0, happiness - 1)
    
    if satiety <= 0 or happiness <= 0:
        pet_label.config(text=sad_pet)
        stats_widget.config(state=tk.NORMAL)
        stats_widget.delete("1.0", tk.END)
        stats_widget.insert(tk.END, f"{pet_name} убежал...\n\nGAME OVER", "red")
        stats_widget.config(state=tk.DISABLED)
        return

    update_display()
    window.after(5000, live_life)

# --- Создание графического окна ---
window = tk.Tk()
window.title("Мой Цифровой Питомец")

# =================================================================
# ВОТ ИЗМЕНЕНИЕ - ДОБАВЛЯЕМ ЦВЕТ КОТИКУ
pet_label = tk.Label(window, text=happy_pet, font=("Courier", 14, "bold"), justify=tk.LEFT, fg="#E8740C")
pet_label.pack(pady=10)
# =================================================================

stats_widget = tk.Text(window, height=4, font=("Arial", 10), bg=window.cget("bg"), borderwidth=0, wrap="word")
stats_widget.pack(pady=5, padx=10)

stats_widget.tag_configure("label", foreground="black")
stats_widget.tag_configure("green", foreground="green", font=("Arial", 10, "bold"))
stats_widget.tag_configure("red", foreground="red", font=("Arial", 10, "bold"))
stats_widget.tag_configure("yellow", foreground="#E5B513", font=("Arial", 10, "bold"))
stats_widget.tag_configure("grey", foreground="lightgrey")

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

feed_button = tk.Button(button_frame, text="Покормить", command=feed_pet)
feed_button.pack(side=tk.LEFT, padx=5)

play_button = tk.Button(button_frame, text="Поиграть", command=play_with_pet)
play_button.pack(side=tk.LEFT, padx=5)

sleep_button = tk.Button(button_frame, text="Уложить спать", command=sleep_pet)
sleep_button.pack(side=tk.LEFT, padx=5)

# --- Первый запуск ---
live_life()
window.mainloop()