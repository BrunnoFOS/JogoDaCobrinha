import pygame
import random

LARGURA_TELA = 800
ALTURA_TELA = 600
TAMANHO_GRADE = 20
LARGURA_GRADE = LARGURA_TELA // TAMANHO_GRADE
ALTURA_GRADE = ALTURA_TELA // TAMANHO_GRADE
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

CIMA = (0, -1)
BAIXO = (0, 1)
ESQUERDA = (-1, 0)
DIREITA = (1, 0)

class Cobra:
    def __init__(self):
        self.corpo = [(LARGURA_GRADE // 2, ALTURA_GRADE // 2)]
        self.direcao = random.choice([CIMA, BAIXO, ESQUERDA, DIREITA])
        self.pontos = 0
        self.viva = True

    def mover(self, comida):
        if self.viva:
            cabeca = (self.corpo[0][0] + self.direcao[0], self.corpo[0][1] + self.direcao[1])
            if cabeca in self.corpo[1:] or not (0 <= cabeca[0] < LARGURA_GRADE and 0 <= cabeca[1] < ALTURA_GRADE):
                self.viva = False
            else:
                self.corpo.insert(0, cabeca)
                if cabeca == comida.posicao:
                    self.pontos += 1
                    comida.spawn()
                else:
                    self.corpo.pop()

    def mudar_direcao(self, direcao):
        if (direcao[0] * -1, direcao[1] * -1) != self.direcao:
            self.direcao = direcao

    def desenhar(self, superficie):
        for segmento in self.corpo:
            pygame.draw.rect(superficie, VERDE, (segmento[0] * TAMANHO_GRADE, segmento[1] * TAMANHO_GRADE, TAMANHO_GRADE, TAMANHO_GRADE))
            pygame.draw.rect(superficie, PRETO, (segmento[0] * TAMANHO_GRADE, segmento[1] * TAMANHO_GRADE, TAMANHO_GRADE, TAMANHO_GRADE), 1)

class Comida:
    def __init__(self):
        self.posicao = (random.randint(0, LARGURA_GRADE - 1), random.randint(0, ALTURA_GRADE - 1))

    def spawn(self):
        self.posicao = (random.randint(0, LARGURA_GRADE - 1), random.randint(0, ALTURA_GRADE - 1))

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, VERMELHO, (self.posicao[0] * TAMANHO_GRADE, self.posicao[1] * TAMANHO_GRADE, TAMANHO_GRADE, TAMANHO_GRADE))

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption('Jogo da Cobra')
    relogio = pygame.time.Clock()

    cobra = Cobra()
    comida = Comida()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    cobra.mudar_direcao(CIMA)
                elif evento.key == pygame.K_DOWN:
                    cobra.mudar_direcao(BAIXO)
                elif evento.key == pygame.K_LEFT:
                    cobra.mudar_direcao(ESQUERDA)
                elif evento.key == pygame.K_RIGHT:
                    cobra.mudar_direcao(DIREITA)

        tela.fill(BRANCO)

        cobra.mover(comida)  # Passando a instância da comida como parâmetro
        cobra.desenhar(tela)
        comida.desenhar(tela)

        if not cobra.viva:
            fonte = pygame.font.Font(None, 36)
            texto = fonte.render('Game Over! Pontuação: {}'.format(cobra.pontos), True, PRETO)
            tela.blit(texto, ((LARGURA_TELA - texto.get_width()) // 2, (ALTURA_TELA - texto.get_height()) // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        pygame.display.flip()
        relogio.tick(10)

if __name__ == "__main__":
    main()
