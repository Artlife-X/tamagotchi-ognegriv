import streamlit as st
from PIL import Image
import time

# --- Настройка страницы (заголовок вкладки в браузере и иконка) ---
# Это первое, что "видит" Streamlit.
st.set_page_config(page_title="Тамагочи Огнегрив", page_icon="🔥")

# --- Функция для загрузки изображений (с кэшированием) ---
# @st.cache_data говорит Streamlit загрузить картинки один раз и не перезагружать их постоянно
@st.cache_data
def load_images():
    try:
        # Убедись, что файлы с такими именами лежат в той же папке
        images = {
            'happy': Image.open("happy.png"),
            'sad': Image.open("sad.png"),
            'sleeping': Image.open("sleeping.png"),
            'playing': Image.open("playing.png")
        }
        return images
    except FileNotFoundError as e:
        # Эта ошибка появится, если картинки не найдены
        st.error(f"Ошибка: Не могу найти файл с картинкой! Убедись, что все .png файлы лежат в той же папке. Детали: {e}")
        return None

images = load_images()

# --- Инициализация состояния игры (самая важная часть для Streamlit) ---
# st.session_state - это "память" нашего приложения между нажатиями кнопок.
# Без этого игра бы "забывала" все после каждого клика.
if 'satiety' not in st.session_state:
    st.session_state.satiety = 5
    st.session_state.happiness = 5
    st.session_state.energy = 5
    st.session_state.is_sleeping = False
    st.session_state.message = "Привет! Я Огнегрив!"

# --- Функции, которые вызываются при нажатии на кнопки ---
def feed_pet():
    st.session_state.satiety = min(10, st.session_state.satiety + 3)
    st.session_state.energy = min(10, st.session_state.energy + 1)
    st.session_state.is_sleeping = False
    st.session_state.message = "Ням-ням! Очень вкусно!"

def play_with_pet():
    if st.session_state.energy > 2:
        st.session_state.happiness = min(10, st.session_state.happiness + 2)
        st.session_state.energy = max(0, st.session_state.energy - 2)
        st.session_state.satiety = max(0, st.session_state.satiety - 1)
        st.session_state.message = "Ура! Мы играем!"
    else:
        st.session_state.message = "Я слишком устал, чтобы играть..."
    st.session_state.is_sleeping = False

def sleep_pet():
    st.session_state.energy = min(10, st.session_state.energy + 4)
    st.session_state.happiness = max(0, st.session_state.happiness - 1)
    st.session_state.is_sleeping = True
    st.session_state.message = "Хррр-пссс... Я сплю."

# --- Логика "течения времени" ---
# Упрощенная версия для веб. При каждом действии питомец немного голодает и скучает.
def time_tick():
    st.session_state.satiety = max(0, st.session_state.satiety - 1)
    st.session_state.happiness = max(0, st.session_state.happiness - 1)

# --- Главная часть - отрисовка интерфейса ---
if images: # Если картинки успешно загрузились
    # Заголовок
    st.title("Тамагочи Огнегрив 🔥")
    
    # Выбираем картинку для отображения
    if st.session_state.is_sleeping:
        current_image = images['sleeping']
    elif st.session_state.happiness <= 3 or st.session_state.satiety <= 3:
        current_image = images['sad']
    elif st.session_state.happiness >= 8:
        current_image = images['playing']
    else:
        current_image = images['happy']
        
    # Отображаем картинку и сообщение под ней
    st.image(current_image, width=250)
    st.info(st.session_state.message)
    
    # Отображение статов
    st.subheader("Показатели:")
    st.text(f"Сытость:")
    st.progress(st.session_state.satiety / 10)
    
    st.text(f"Счастье:")
    st.progress(st.session_state.happiness / 10)
    
    st.text(f"Энергия:")
    st.progress(st.session_state.energy / 10)
    
    # Проверка на проигрыш
    if st.session_state.satiety <= 0 or st.session_state.happiness <= 0:
        st.error("О нет! Огнегрив убежал, потому что о нем плохо заботились... GAME OVER")
    else:
        st.subheader("Действия:")
        # Кнопки в три колонки (для красоты на мобильном)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Покормить"):
                feed_pet()
                time_tick()
                st.rerun() # Команда для немедленной перерисовки страницы
        with col2:
            if st.button("Поиграть"):
                play_with_pet()
                time_tick()
                st.rerun()
        with col3:
            if st.button("Уложить спать"):
                sleep_pet()
                time_tick()
                st.rerun()