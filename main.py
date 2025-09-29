import pygame
import random
import time

# Inicializando o Pygame
pygame.init()

# Definindo cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

# Tamanho da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo de Ação")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Carregando imagens
player_img = pygame.Surface((50, 50))
player_img.fill(AZUL)

enemy_img = pygame.Surface((50, 50))
enemy_img.fill(VERMELHO)

bullet_img = pygame.Surface((10, 5))
bullet_img.fill(VERDE)

enemy_bullet_img = pygame.Surface((10, 5))
enemy_bullet_img.fill(VERMELHO)  # Cor do tiro do inimigo

meteoro_img = pygame.Surface((30, 30))
meteoro_img.fill((150, 150, 150))  # Cor cinza para os meteoros

# Classe do jogador
class Player:
    def __init__(self):
        self.x = 100
        self.y = ALTURA_TELA // 2
        self.velocidade = 5
        self.vivo = True
        self.vidas = 3
        self.ultimo_tiro = 0  # Variável para controlar o tempo entre os tiros

    def mover(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if keys[pygame.K_RIGHT] and self.x < LARGURA_TELA - 50:
            self.x += self.velocidade
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.velocidade
        if keys[pygame.K_DOWN] and self.y < ALTURA_TELA - 50:
            self.y += self.velocidade

    def desenhar(self):
        tela.blit(player_img, (self.x, self.y))

    def pode_disparar(self, intervalo=0.3):
        tempo_atual = time.time()
        if tempo_atual - self.ultimo_tiro >= intervalo:
            self.ultimo_tiro = tempo_atual
            return True
        return False

# Classe do inimigo
class Enemy:
    def __init__(self):
        self.x = LARGURA_TELA - 100
        self.y = random.randint(50, ALTURA_TELA - 100)
        self.velocidade = 2
        self.vida = 150  # Vida do inimigo
        self.ultimo_tiro = 0  # Controle de tempo do tiro do inimigo

    def mover(self):
        self.y += self.velocidade
        if self.y >= ALTURA_TELA - 50 or self.y <= 0:
            self.velocidade = -self.velocidade

    def disparar(self):
        tempo_atual = time.time()
        # Tiro aleatório com intervalo entre 0.5 a 1.5 segundos
        if tempo_atual - self.ultimo_tiro >= random.uniform(0.5, 1.5):  
            self.ultimo_tiro = tempo_atual
            # Gerar um tiro aleatório em uma posição vertical aleatória
            pos_y_tiro = self.y + random.randint(-20, 20)  # Aleatorizar a posição do tiro verticalmente
            return Bullet(self.x - 10, pos_y_tiro, -15)  # O tiro vai para a esquerda com velocidade maior
        return None

    def desenhar(self):
        tela.blit(enemy_img, (self.x, self.y))

    def mostrar_vida(self):
        font = pygame.font.SysFont("Arial", 20)
        texto = font.render(f'Vida: {self.vida}', True, BRANCO)
        tela.blit(texto, (self.x, self.y - 30))  # Exibe acima do inimigo

# Classe do meteoro
class Meteoro:
    def __init__(self):
        # Posicionar o meteoro em um canto aleatório da tela
        self.x = random.choice([0, LARGURA_TELA])  # Inicia em um dos cantos horizontais
        self.y = random.randint(0, ALTURA_TELA)  # Altura aleatória na tela
        self.velocidade_x = random.choice([1, -1]) * random.randint(3, 6)  # Direção aleatória (diagonal)
        self.velocidade_y = random.randint(3, 6)  # Velocidade vertical

    def mover(self):
        # Atualiza a posição com base na velocidade
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        # Garantir que o meteoro não saia da tela
        if self.x < 0 or self.x > LARGURA_TELA:
            self.velocidade_x = -self.velocidade_x  # Inverte a direção horizontal
        if self.y > ALTURA_TELA:
            self.y = -30  # Reinicia a posição do meteoro no topo

    def desenhar(self):
        tela.blit(meteoro_img, (self.x, self.y))

    def colisao(self, player):
        # Verificar se o meteoro colidiu com o jogador
        if player.x < self.x + 30 and player.x + 50 > self.x and player.y < self.y + 30 and player.y + 50 > self.y:
            return True
        return False

# Classe do tiro
class Bullet:
    def __init__(self, x, y, velocidade):
        self.x = x
        self.y = y
        self.velocidade = velocidade

    def mover(self):
        self.x += self.velocidade

    def desenhar(self):
        tela.blit(bullet_img, (self.x, self.y))

# Função para mostrar texto na tela
def texto(msg, cor, pos_x, pos_y):
    font = pygame.font.SysFont("Arial", 30)
    texto_surface = font.render(msg, True, cor)
    tela.blit(texto_surface, (pos_x, pos_y))

# Função principal
def jogo():
    player = Player()
    enemy = Enemy()
    meteoros = [Meteoro() for _ in range(5)]  # Criar 5 meteoros no início
    tiros = []
    tiros_inimigo = []
    pausado = False
    game_over = False
    vitoria = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if not pausado and not game_over:
            player.mover(keys)

            # Tiro do jogador
            if keys[pygame.K_SPACE] and player.pode_disparar():
                tiros.append(Bullet(player.x + 50, player.y + 20, 10))  # O tiro vai para a direita

            # Movimento do inimigo
            enemy.mover()

            # O inimigo atira (tiros rápidos e aleatórios)
            tiro_inimigo = enemy.disparar()
            if tiro_inimigo:
                tiros_inimigo.append(tiro_inimigo)

            # Movimentar os tiros
            for tiro in tiros:
                tiro.mover()
                if tiro.x > LARGURA_TELA:
                    tiros.remove(tiro)

            for tiro in tiros_inimigo:
                tiro.mover()
                if tiro.x < 0:
                    tiros_inimigo.remove(tiro)

            # Colisão entre tiro e inimigo
            for tiro in tiros:
                if enemy.x < tiro.x < enemy.x + 50 and enemy.y < tiro.y < enemy.y + 50:
                    enemy.vida -= 10
                    tiros.remove(tiro)
                    if enemy.vida <= 0:
                        vitoria = True
                        game_over = True

            # Colisão entre inimigo e jogador
            if player.x < enemy.x + 50 and player.x + 50 > enemy.x and player.y < enemy.y + 50 and player.y + 50 > enemy.y:
                player.vidas -= 1
                if player.vidas <= 0:
                    game_over = True

            # Colisão entre tiro do inimigo e jogador
            for tiro_inimigo in tiros_inimigo:
                if player.x < tiro_inimigo.x < player.x + 50 and player.y < tiro_inimigo.y < player.y + 50:
                    player.vidas -= 1
                    tiros_inimigo.remove(tiro_inimigo)
                    if player.vidas <= 0:
                        game_over = True

            # Colisão entre meteoros e jogador
            for meteoro in meteoros:
                meteoro.mover()
                if meteoro.colisao(player):
                    player.vidas -= 1
                    meteoros.remove(meteoro)
                    if player.vidas <= 0:
                        game_over = True

        # Tela
        tela.fill(PRETO)

        # Mostrar o personagem
        player.desenhar()

        # Mostrar o inimigo
        enemy.desenhar()
        enemy.mostrar_vida()

        # Mostrar tiros do jogador
        for tiro in tiros:
            tiro.desenhar()

        # Mostrar tiros do inimigo
        for tiro_inimigo in tiros_inimigo:
            tela.blit(enemy_bullet_img, (tiro_inimigo.x, tiro_inimigo.y))

        # Mostrar meteoros
        for meteoro in meteoros:
            meteoro.desenhar()

        # Mostrar vidas
        texto(f'Vidas: {player.vidas}', BRANCO, 10, 10)

        # Pausar jogo
        if keys[pygame.K_p]:
            pausado = not pausado

        if game_over:
            if vitoria:
                texto("Você Venceu!", VERDE, LARGURA_TELA // 2 - 100, ALTURA_TELA // 2)
            else:
                texto("Você Perdeu!", VERMELHO, LARGURA_TELA // 2 - 100, ALTURA_TELA // 2)

        pygame.display.update()

        clock.tick(FPS)

# Iniciar o jogo
jogo()