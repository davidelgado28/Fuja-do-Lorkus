import sys
import random
import pygame

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fuga da Aula: Desvie dos Livros do Prof. Lorkus!")
RELOGIO = pygame.time.Clock()
FPS = 60
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (220, 50, 50)
AZUL = (50, 120, 220)       
ROSA = (230, 100, 180)     
VERDE = (50, 200, 80)
AMARELO = (240, 200, 50)
CINZA = (120, 120, 140)
MENU = "MENU"
SELECAO = "SELECAO"
JOGANDO = "JOGANDO"
DERROTA = "DERROTA"
VITORIA = "VITORIA"

class Aluno:
    def __init__(self, x, y, genero="homem"):
        self.largura = 40
        self.altura = 50
        self.rect = pygame.Rect(x, y, self.largura, self.altura)
        self.velocidade = 6
        self.genero = genero

    def mover(self, teclas):
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and self.rect.right < LARGURA:
            self.rect.x += self.velocidade
        if (teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and self.rect.bottom < ALTURA:
            self.rect.y += self.velocidade

    def desenhar(self, superficie):
        if self.genero == "homem":
            pygame.draw.rect(superficie, AZUL, self.rect)
            pygame.draw.rect(superficie, BRANCO, (self.rect.x + 8, self.rect.y + 10, 8, 8))
            pygame.draw.rect(superficie, BRANCO, (self.rect.x + 24, self.rect.y + 10, 8, 8))
            pygame.draw.rect(superficie, PRETO, (self.rect.x + 10, self.rect.y + 4, 20, 4))
        else:
            pygame.draw.rect(superficie, ROSA, self.rect)
            pygame.draw.rect(superficie, BRANCO, (self.rect.x + 8, self.rect.y + 10, 8, 8))
            pygame.draw.rect(superficie, BRANCO, (self.rect.x + 24, self.rect.y + 10, 8, 8))
            pygame.draw.rect(superficie, AMARELO, (self.rect.x + 30, self.rect.y + 10, 8, 16))

class Livro:
    def __init__(self, dificuldade="normal"):
        self.largura = 30
        self.altura = 20
        self.dificuldade = dificuldade
        self.resetar()

    def resetar(self):
        self.rect = pygame.Rect(
            random.randint(0, LARGURA - self.largura),
            random.randint(-150, -40),
            self.largura,
            self.altura
        )
        if self.dificuldade == "facil":
            self.velocidade_y = random.randint(2, 4)
            self.velocidade_x = random.choice([-1, 0, 1])
        else:
            self.velocidade_y = random.randint(5, 9)
            self.velocidade_x = random.choice([-2, -1, 0, 1, 2])

    def mover(self):
        self.rect.y += self.velocidade_y
        self.rect.x += self.velocidade_x
        if self.rect.top > ALTURA or self.rect.right < 0 or self.rect.left > LARGURA:
            self.resetar()

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, VERMELHO, self.rect)
        pygame.draw.rect(superficie, BRANCO, (self.rect.x + 4, self.rect.y + 4, self.largura - 8, self.altura - 8))

class Jogo:
    def __init__(self):
        self.estado = MENU
        self.fonte_titulo = pygame.font.SysFont("arial", 42, bold=True)
        self.fonte_texto = pygame.font.SysFont("arial", 22)
        self.bg_y = 0
        self.tempo_sobrevivencia = 0
        self.meta_tempo = 30.0  
        self.genero_escolhido = "homem"
        self.aluno = Aluno(LARGURA // 2 - 20, ALTURA - 80, self.genero_escolhido)
        self.livros = []
        self.tempo_inicio = 0

    def resetar_jogo(self, genero):
        self.genero_escolhido = genero
        dificuldade = "facil" if genero == "mulher" else "normal"
        num_livros = 4 if genero == "mulher" else 8  

        self.aluno = Aluno(LARGURA // 2 - 20, ALTURA - 80, genero)
        self.livros = [Livro(dificuldade) for _ in range(num_livros)]
        self.tempo_inicio = pygame.time.get_ticks()
        self.tempo_sobrevivencia = 0

    def atualizar_scrolling(self):
        self.bg_y = (self.bg_y + 3) % ALTURA

    def desenhar_fundo(self, superficie):
        superficie.fill((30, 30, 45))
        for y in range(self.bg_y - ALTURA, ALTURA, 60):
            pygame.draw.line(superficie, (45, 45, 65), (0, y), (LARGURA, y), 2)

    def executar(self):
        rodando = True
        while rodando:
            RELOGIO.tick(FPS)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                
                if evento.type == pygame.KEYDOWN:
                    if self.estado == MENU and evento.key == pygame.K_SPACE:
                        self.estado = SELECAO
                    elif self.estado == SELECAO:
                        if evento.key in (pygame.K_1, pygame.K_h):
                            self.resetar_jogo("homem")
                            self.estado = JOGANDO
                        elif evento.key in (pygame.K_2, pygame.K_m):
                            self.resetar_jogo("mulher")
                            self.estado = JOGANDO
                    elif self.estado in (DERROTA, VITORIA):
                        if evento.key == pygame.K_r:
                            self.resetar_jogo(self.genero_escolhido)
                            self.estado = JOGANDO
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado = MENU

            self.atualizar()
            self.desenhar()

        pygame.quit()
        sys.exit()

    def atualizar(self):
        if self.estado == JOGANDO:
            self.atualizar_scrolling()
            self.aluno.mover(pygame.key.get_pressed())

            self.tempo_sobrevivencia = round((pygame.time.get_ticks() - self.tempo_inicio) / 1000, 1)

            if self.tempo_sobrevivencia >= self.meta_tempo:
                self.estado = VITORIA

            for livro in self.livros:
                livro.mover()
                if self.aluno.rect.colliderect(livro.rect):
                    self.estado = DERROTA

    def desenhar(self):
        self.desenhar_fundo(TELA)

        if self.estado == MENU:
            txt_titulo = self.fonte_titulo.render("Fuga do Prof. Lorkus", True, AMARELO)
            txt_sub = self.fonte_texto.render("Pressione ESPAÇO para ir à Seleção de Personagem", True, BRANCO)
            TELA.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 200))
            TELA.blit(txt_sub, (LARGURA // 2 - txt_sub.get_width() // 2, 300))

        elif self.estado == SELECAO:
            txt_titulo = self.fonte_titulo.render("Escolha o seu Personagem", True, AMARELO)
            txt_h = self.fonte_texto.render("[1 ou H] Garoto", True, AZUL)
            txt_m = self.fonte_texto.render("[2 ou M] Menina", True, ROSA)
            txt_voltar = self.fonte_texto.render("Pressione [ESC] para voltar ao Menu", True, CINZA)
            
            TELA.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 160))
            TELA.blit(txt_h, (LARGURA // 2 - txt_h.get_width() // 2, 250))
            TELA.blit(txt_m, (LARGURA // 2 - txt_m.get_width() // 2, 310))
            TELA.blit(txt_voltar, (LARGURA // 2 - txt_voltar.get_width() // 2, 420))

        elif self.estado == JOGANDO:
            self.aluno.desenhar(TELA)
            for livro in self.livros:
                livro.desenhar(TELA)

            dif_txt = "Fácil"
            txt_info = self.fonte_texto.render(f"Modo: {dif_txt} | Tempo: {self.tempo_sobrevivencia}s / {self.meta_tempo}s", True, BRANCO)
            TELA.blit(txt_info, (20, 20))

        elif self.estado == DERROTA:
            txt_fim = self.fonte_titulo.render("VOCÊ FOI MOLESTADO PELO LORKUS", True, VERMELHO)
            txt_inst = self.fonte_texto.render("Pressione [R] para Tentar Novamente ou [ESC] para o Menu", True, BRANCO)
            TELA.blit(txt_fim, (LARGURA // 2 - txt_fim.get_width() // 2, 200))
            TELA.blit(txt_inst, (LARGURA // 2 - txt_inst.get_width() // 2, 300))

        elif self.estado == VITORIA:
            txt_vit = self.fonte_titulo.render("VOCÊ ESCAPOU DO LORKUS!", True, VERDE)
            txt_inst = self.fonte_texto.render("Pressione [R] para Jogar Novamente ou [ESC] para o Menu", True, BRANCO)
            TELA.blit(txt_vit, (LARGURA // 2 - txt_vit.get_width() // 2, 200))
            TELA.blit(txt_inst, (LARGURA // 2 - txt_inst.get_width() // 2, 300))

        pygame.display.flip()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
