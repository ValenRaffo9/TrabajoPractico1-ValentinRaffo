import pygame
import time

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Preguntados")

# Configuración del ícono de la aplicación
icon = pygame.image.load("D:/xampp2/htdocs/Juego/imagenes/icono.png")
pygame.display.set_icon(icon)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = (100, 149, 237)  # Color azul claro (Cornflower Blue)
MENU_COLOR = (255, 224, 189)  # Color crema
TEXT_COLOR = (20, 20, 20)  # Color de texto gris oscuro 

# Fuentes
font_large = pygame.font.Font(None, 48)  # Fuente grande para opciones del menú
font_medium = pygame.font.Font(None, 36)  # Fuente para preguntas
font_small = pygame.font.Font(None, 28)  # Fuente para opciones

# Cargar y redimensionar imágenes para respuestas correctas e incorrectas
correct_img = pygame.image.load("D:/xampp2/htdocs/Juego/imagenes/correcto.png")
incorrect_img = pygame.image.load("D:/xampp2/htdocs/Juego/imagenes/incorrecto.png")
correct_img = pygame.transform.scale(correct_img, (180, 180))  # Redimensionar a 180x180
incorrect_img = pygame.transform.scale(incorrect_img, (180, 180))  # Redimensionar a 180x180

# Cargar música de fondo
pygame.mixer.music.load("D:/xampp2/htdocs/Juego/cancion/song.mp3.mp3")  # Cambia la ruta a tu archivo de música
pygame.mixer.music.play(-1)  # -1 para reproducir en bucle

# Preguntas y respuestas
questions = {
    "Tecnología": [
        ("¿Qué es una IA?", ["Un tipo de robot", "Un software que simula inteligencia humana", "Un dispositivo de almacenamiento", "Un sistema operativo"], 1),
        ("¿Qué significa 'IoT'?", ["Internet of Things", "Internet of Technology", "Internet of Tools", "Interconnected Online Tech"], 0),
        ("¿Cuál es el lenguaje de programación más utilizado en el desarrollo web?", ["Python", "JavaScript", "Java", "C++"], 1),
        ("¿Qué es la nube en términos tecnológicos?", ["Un tipo de almacenamiento físico", "Almacenamiento en servidores remotos", "Un nuevo sistema operativo", "Un tipo de malware"], 1),
        ("¿Cuál de estos es un sistema operativo?", ["Microsoft Word", "Windows", "Google Chrome", "Adobe Photoshop"], 1),
    ],
    "Deportes": [
        ("¿Quién es el equipo con más Copas Libertadores?", ["Boca Juniors", "River Plate", "Independiente", "San Lorenzo"], 2),
        ("¿Cuál es el equipo más grande del mundo?", ["Barcelona", "Real Madrid", "Independiente", "Manchester United"], 2),
        ("¿Quién ganó la Copa del Mundo de 2014?", ["Argentina", "Alemania", "Brasil", "España"], 1),
        ("¿Qué deporte se juega con una pelota ovalada?", ["Fútbol", "Rugby", "Baloncesto", "Tenis"], 1),
        ("¿Quién es el máximo goleador de la historia del fútbol?", ["Pelé", "Diego Maradona", "Cristiano Ronaldo", "Lionel Messi"], 2),
    ]
}

# Variables del juego
score = 0
current_category = None
current_question_index = 0
selected_option = None
game_state = "menu"  # Estados posibles: "menu", "playing", "finished", "show_result"
result_shown_time = None  # Tiempo para mostrar el resultado

def display_text(text, color, x, y, font_size=font_medium):
    """Mostrar texto en la pantalla, centrado."""
    text_surface = font_size.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def display_question(question, options, selected_option=None, correct_answer=None):
    """Mostrar la pregunta y las opciones, indicando si la respuesta es correcta o incorrecta."""
    screen.fill(BACKGROUND_COLOR)
    
    # Mostrar la pregunta centrada
    display_text(question, TEXT_COLOR, WIDTH // 2, HEIGHT // 3, font_size=font_medium)

    for i, option in enumerate(options):
        color = TEXT_COLOR
        if selected_option is not None:
            if i == selected_option:
                color = GREEN if i == correct_answer else RED
            elif i == correct_answer:
                color = GREEN
        display_text(f"{i + 1}. {option}", color, WIDTH // 2, HEIGHT // 2 + i * 40, font_size=font_small)

def handle_click(option_index):
    """Gestionar la selección de una opción."""
    global selected_option, current_question_index, score, game_state, result_shown_time
    selected_option = option_index
    correct_answer = questions[current_category][current_question_index][2]
    if selected_option == correct_answer:
        score += 1
        game_state = "show_correct_image"
    else:
        game_state = "show_incorrect_image"
    result_shown_time = time.time()

def show_result_image():
    """Mostrar la imagen de resultado (correcta o incorrecta)."""
    global game_state, current_question_index, result_shown_time, selected_option
    screen.fill(BACKGROUND_COLOR)  # Limpiar la pantalla para mostrar la imagen correctamente
    if game_state == "show_correct_image":
        screen.blit(correct_img, (WIDTH // 2 - 90, HEIGHT // 2 - 90))  # Centrado de imagen
    elif game_state == "show_incorrect_image":
        screen.blit(incorrect_img, (WIDTH // 2 - 90, HEIGHT // 2 - 90))  # Centrado de imagen
    
    # Mostrar por 2 segundos
    if time.time() - result_shown_time > 2:
        game_state = "playing"
        current_question_index += 1
        selected_option = None  # Restablecer la selección
        if current_question_index >= len(questions[current_category]):
            game_state = "finished"
        else:
            # Volver a mostrar la pregunta y opciones para la siguiente
            selected_option = None  # Asegúrate de que no haya opción seleccionada

def display_tutorial():
    """Mostrar el tutorial del juego."""  
    screen.fill(BACKGROUND_COLOR)
    tutorial_text = [
        "Tutorial:",
        "1. Selecciona una categoría usando 1 o 2.",
        "2. Responde a las preguntas seleccionando la opción.",
        "3. Tu puntaje se incrementa por cada respuesta correcta.",
        "4. Presiona cualquier tecla para volver al menú."
    ]
    for i, line in enumerate(tutorial_text):
        display_text(line, TEXT_COLOR, WIDTH // 2, HEIGHT // 3 + i * 40, font_size=font_small)

def main():
    global current_category, game_state, selected_option
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if game_state == "menu":
                    if event.key == pygame.K_1:
                        current_category = "Tecnología"
                        game_state = "playing"
                        current_question_index = 0
                        selected_option = None  # Reiniciar la selección
                    elif event.key == pygame.K_2:
                        current_category = "Deportes"
                        game_state = "playing"
                        current_question_index = 0
                        selected_option = None  # Reiniciar la selección
                    elif event.key == pygame.K_t:
                        game_state = "tutorial"
                elif game_state == "playing":
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        handle_click(event.key - pygame.K_1)
                elif game_state == "finished":
                    # Volver al menú al presionar cualquier tecla
                    game_state = "menu"  # Volver al menú
                elif game_state == "tutorial":
                    game_state = "menu"  # Volver al menú

        if game_state == "menu":
            screen.fill(MENU_COLOR)
            display_text("Menú", TEXT_COLOR, WIDTH // 2, HEIGHT // 3, font_size=font_large)
            display_text("1. Tecnología", TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 20)
            display_text("2. Deportes", TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 20)
            display_text("Presiona 't' para tutorial", TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 60)
        elif game_state == "playing":
            if current_question_index < len(questions[current_category]):
                question, options, _ = questions[current_category][current_question_index]
                display_question(question, options, selected_option)
            else:
                game_state = "finished"
        elif game_state == "finished":
            screen.fill(MENU_COLOR)
            display_text("Juego terminado!", TEXT_COLOR, WIDTH // 2, HEIGHT // 3, font_size=font_large)
            display_text(f"Puntaje final: {score}", TEXT_COLOR, WIDTH // 2, HEIGHT // 2, font_size=font_large)
            display_text("Presiona cualquier tecla para volver al menú", TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 60, font_size=font_small)
        elif game_state == "show_correct_image" or game_state == "show_incorrect_image":
            show_result_image()
        
        elif game_state == "tutorial":
            display_tutorial()

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
