import streamlit as st
from PIL import Image

# --- Настройка страницы ---
st.set_page_config(page_title="Тамагочи Огнегрив", page_icon="🔥")

# --- Функция для загрузки изображений ---
@st.cache_data
def load_images():
    try:
        images = {
            'happy': Image.open("happy.png"),
            'sad': Image.open("sad.png"),
            'sleeping': Image.open("sleeping.png"),
            'playing': Image.open("playing.png")
        }
        return images
    except FileNotFoundError as e:
        st.error(f"Ошибка: Не могу найти файл с картинкой! Убедись, что все .png файлы лежат в той же папке. Детали: {e}")
        return None

images = load_images()

# --- Инициализация состояния игры ---
if 'satiety' not in st.session_state:
    st.session_state.satiety = 8
    st.session_state.happiness = 8
    st.session_state.energy = 8
    st.session_state.days_survived = 0
    st.session_state.is_sleeping = False
    st.session_state.just_woke_up = False
    st.session_state.message = "Привет! Я Огнегрив! Позаботься обо мне!"

# --- Функции для кнопок ---
def feed_pet():
    st.session_state.satiety = min(10, st.session_state.satiety + 3)
    st.session_state.happiness = min(10, st.session_state.happiness + 1) # Еда тоже радует
    st.session_state.message = "Ням-ням! Очень вкусно!"
    st.session_state.is_sleeping = False

def play_with_pet():
    if st.session_state.energy >= 3:
        st.session_state.happiness = min(10, st.session_state.happiness + 3)
        st.session_state.energy = max(0, st.session_state.energy - 2)
        st.session_state.satiety = max(0, st.session_state.satiety - 1)
        st.session_state.message = "Ура! Мы играем! Это так весело!"
    else:
        st.session_state.message = "Я слишком устал, чтобы играть..."
    st.session_state.is_sleeping = False

def sleep_pet():
    st.session_state.energy = 10 # Полностью восстанавливает энергию
    st.session_state.is_sleeping = True
    st.session_state.message = "Хррр-пссс... Я сплю. Разбуди меня, когда я понадоблюсь."
    
def wake_up():
    st.session_state.is_sleeping = False
    st.session_state.days_survived += 1 # Новый день!
    st.session_state.happiness = max(0, st.session_state.happiness - 2) # Сон был долгим, стало скучно
    st.session_state.satiety = max(0, st.session_state.satiety - 2)   # И проголодался
    st.session_state.message = f"Я проснулся! Мы вместе уже {st.session_state.days_survived} дней! Я немного голоден и хочу играть."

def restart_game():
    st.session_state.satiety = 8
    st.session_state.happiness = 8
    st.session_state.energy = 8
    st.session_state.days_survived = 0
    st.session_state.is_sleeping = False
    st.session_state.message = "Новая игра! Попробуем еще раз!"

# --- Главная часть - отрисовка интерфейса ---
if images:
    st.title("Тамагочи Огнегрив 🔥")

    # Проверка на проигрыш
    game_over = st.session_state.satiety <= 0 or st.session_state.happiness <= 0

    if game_over:
        st.image(images['sad'], width=250)
        st.error(f"О нет! Огнегрив прожил с тобой {st.session_state.days_survived} дней и убежал... GAME OVER")
        if st.button("Начать заново", on_click=restart_game):
            pass # Кнопка сама перезапустит игру
    else:
        # Логика выбора картинки
        if st.session_state.is_sleeping:
            current_image = images['sleeping']
        elif st.session_state.happiness <= 3 or st.session_state.satiety <= 3:
            current_image = images['sad']
        elif st.session_state.happiness >= 9:
             current_image = images['playing']
        else:
            current_image = images['happy']
        
        st.image(current_image, width=250)
        st.info(st.session_state.message)
        
        # Отображение статов
        st.metric("Дней прожито:", st.session_state.days_survived)
        st.subheader("Показатели:")
        st.text("Сытость:")
        st.progress(st.session_state.satiety / 10)
        st.text("Счастье:")
        st.progress(st.session_state.happiness / 10)
        st.text("Энергия:")
        st.progress(st.session_state.energy / 10)
        
        # Кнопки действий
        st.subheader("Действия:")
        if st.session_state.is_sleeping:
            if st.button("Разбудить Огнегрива", on_click=wake_up):
                pass
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Покормить", on_click=feed_pet)
            with col2:
                st.button("Поиграть", on_click=play_with_pet)
            with col3:
                st.button("Уложить спать", on_click=sleep_pet)