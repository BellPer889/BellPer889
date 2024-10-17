import pygame
import sys
import random

# Inizializza Pygame e la musica
pygame.init()
# Colore rosso per il punteggio
rosso = (255, 0, 0)

# Variabile per tenere traccia della vita
vita = 1

# Carica i fotogrammi dell'astronave
astronave_frames = [
    pygame.image.load("C:/Users/oertp/Documents/Nel_nero_del_buio/astronave_1.png"),
    pygame.image.load("C:/Users/oertp/Documents/Nel_nero_del_buio/astronave_2.png"),
]

# Carica i fotogrammi dello sfondo
sfondo_frames = [
    pygame.image.load("C:/Users/oertp/Documents/Nel_nero_del_buio/sfondo_1.png"),
    pygame.image.load("C:/Users/oertp/Documents/Nel_nero_del_buio/sfondo_2.png"),
    pygame.image.load("C:/Users/oertp/Documents/Nel_nero_del_buio/sfondo_3.png"),
]

# Carica l'immagine dell'asteroide e quella del game over
asteroide = pygame.image.load("C:/Users/oertp/Documents/Nel_nero_del_buio/asteroide.png")
game_over = pygame.image.load("C:/Users/oertp/Documents/Nel_nero_del_buio/game_over.png")

# Carica la musichetta di sottofondo
musichetta = pygame.mixer.music.load("C:/Users/oertp/Documents/Nel_nero_del_buio/musichetta.wav")
fine = pygame.mixer.Sound("C:/Users/oertp/Documents/Nel_nero_del_buio/fine.wav")

# Definisce le dimensioni della finestra di gioco
altezza = 500
lunghezza = 500

# Crea la finestra di gioco
schermo = pygame.display.set_mode((lunghezza, altezza))
pygame.display.set_caption('Nel nero del buio')  # Titolo della finestra

# Crea un orologio per controllare il frame rate
clock = pygame.time.Clock()
fps = 120  # Frame per secondo

# Inizializza il punteggio
score = 0

# Indici per il fotogramma dell'astronave e dello sfondo
astronave_frame_index = 0
sfondo_frame_index = 0
frame_time = 0
frame_duration = 100  # Durata di ciascun fotogramma in millisecondi

# Ottieni le dimensioni dell'astronave
larghezza_astronave, altezza_astronave = astronave_frames[0].get_size()

# Calcola la posizione iniziale dell'astronave
posizione_astronave_x = (lunghezza / 2) - (larghezza_astronave / 2)
posizione_astronave_y = altezza - altezza_astronave  # In fondo alla finestra

# Inizializza la posizione dell'asteroide
posizione_asteroide_y = 0  # Inizia sopra lo schermo
posizione_asteroide_x = (lunghezza / 2) - (asteroide.get_width() / 2)  # Centra l'asteroide

# Inizializza la posizione del game over
posizione_game_over_x = 0
posizione_game_over_y = 0

# Funzione per mostrare il punteggio
def your_score(score):
    score_font = pygame.font.SysFont("arial", 35)  # Font per il punteggio
    value = score_font.render(f"Score: {score}", True, rosso)  # Crea il testo del punteggio
    schermo.blit(value, [0, 0])  # Disegna il punteggio nello schermo

pygame.mixer.music.play(-1)
# Ciclo principale del gioco
run = True
while run:
    # Gestisci gli eventi di gioco
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Se l'utente chiude la finestra
            run = False

    # Aggiorna la posizione dell'astronave in base ai tasti premuti
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  # Se il tasto sinistro è premuto
        posizione_astronave_x -= 2  # Sposta a sinistra
    if keys[pygame.K_RIGHT]:  # Se il tasto destro è premuto
        posizione_astronave_x += 2  # Sposta a destra

    # Limita l'astronave ai bordi dello schermo
    if posizione_astronave_x < 0:
        posizione_astronave_x = 0  # Non può andare oltre il bordo sinistro
    if posizione_astronave_x > lunghezza - larghezza_astronave:
        posizione_astronave_x = lunghezza - larghezza_astronave  # Non può andare oltre il bordo destro

    # Aggiorna il tempo per il ciclo dei fotogrammi
    frame_time += clock.get_time()

    # Aggiorna il fotogramma dell'astronave e dello sfondo
    if frame_time >= frame_duration:
        astronave_frame_index = (astronave_frame_index + 1) % len(astronave_frames)
        sfondo_frame_index = (sfondo_frame_index + 1) % len(sfondo_frames)
        frame_time = 0  # Resetta il tempo

    # Aggiorna la posizione dell'asteroide
    if vita == 1:
        posizione_asteroide_y = posizione_asteroide_y + 4  # Muovi l'asteroide verso il basso
    if posizione_asteroide_y > altezza:  # Se l'asteroide esce dallo schermo
        posizione_asteroide_y = 0  # Resetta sopra lo schermo
        # Riposiziona l'asteroide in una posizione X casuale
        posizione_asteroide_x = random.randint(0, lunghezza - asteroide.get_width())
        score += 1  # Incrementa il punteggio

    # Disegna lo sfondo animato
    schermo.blit(sfondo_frames[sfondo_frame_index], (0, 0))
    
    # Disegna l'astronave animata
    schermo.blit(astronave_frames[astronave_frame_index], (posizione_astronave_x, posizione_astronave_y))
    
    # Disegna l'asteroide
    schermo.blit(asteroide, (posizione_asteroide_x, posizione_asteroide_y))

    # Disegna il punteggio
    your_score(score)

    # Crea i rettangoli per il controllo delle collisioni
    astronaut_rect = pygame.Rect(posizione_astronave_x, posizione_astronave_y, larghezza_astronave, altezza_astronave)
    asteroide_rect = pygame.Rect(posizione_asteroide_x, posizione_asteroide_y, asteroide.get_width(), asteroide.get_height())

    # Controlla collisione tra astronave e asteroide
    if astronaut_rect.colliderect(asteroide_rect):
        vita = 0  # Se c'è collisione, la vita diventa 0
        pygame.mixer.music.stop()
        fine.play()
        posizione_astronave_x = (lunghezza / 2) - (larghezza_astronave / 2)
        posizione_astronave_y = altezza - altezza_astronave
        posizione_asteroide_x = 250
        posizione_asteroide_y = 0
        print("Hai fatto", score, "punti.")
    # Se la vita è zero, termina il gioco
    if vita == 0:
        schermo.blit(game_over, (posizione_game_over_x, posizione_game_over_y))
        pygame.mixer.music.stop()
        if keys[pygame.K_q]:
            run = False
        if keys[pygame.K_r]:
            posizione_astronave_x = (lunghezza / 2) - (larghezza_astronave / 2)
            posizione_astronave_y = altezza - altezza_astronave
            posizione_asteroide_x = 250
            posizione_asteroide_y = 0
            pygame.mixer.music.stop()
            score = 0
            musichetta = pygame.mixer.music.load("C:/Users/oertp/Documents/Nel_nero_del_buio/musichetta.wav")
            pygame.mixer.music.play(-1)
            vita = 1

        

    # Aggiorna lo schermo
    pygame.display.flip()  # Mostra gli aggiornamenti sullo schermo
    clock.tick(fps)  # Limita il frame rate