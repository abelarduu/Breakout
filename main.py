import pyxel

class Object:
    def __init__(self, x, y, img, imgx, imgy, w, h):
        self.x = x
        self.y = y
        self.img = img
        self.imgx = imgx
        self.imgy = imgy
        self.w = w
        self.h = h
        self.scores = 0
        
    def move(self, left, right, up= None, down= None):
        """Atualiza a posição da objeto com base na condições colocadas e aplica a gravidade."""
        if (left and self.x > 8):
            self.x -= 2
            
        if (right and self.x + self.w <= pyxel.width - 9):
            self.x += 2
        
        if up: 
            self.y -= 2 
            
        if down: 
            self.y += 2        

    def check_collision(self, obj):
        """Verifica se há colisão com um determinado objeto."""
        if (self.y + self.h >= obj.y and
            self.y <= obj.y + obj.h):
            
            if (self.x + self.w >= obj.x and
                self.x <= obj.x + obj.w):
                return True
                
    def destroy(self):
        """Remove/move objeto para fora da tela."""
        self.y = (self.y - 50)

    def draw(self):
        """Desenha o objeto na tela."""
        pyxel.blt(self.x,
                  self.y,
                  self.img,
                  self.imgx,
                  self.imgy,
                  self.w,
                  self.h)
        
class Game:
    def __init__(self):
        pyxel.init(100, 100, "Breakout")
        self.play = False
        
        # Objetos
        self.player = Object(pyxel.width/2 - 19/2, pyxel.height -11, 0, 8, 30, 19, 8)
        
        self.ball = Object(pyxel.width/2 - 3, pyxel.height -20, 0, 8,39, 6, 6)
        self.ball.eixX1 = True
        self.ball.eixX2 = False
        self.ball.eixY1 = True
        self.ball.eixY2 = False

        self.listBlock = []
        self.blocks_creator()

        pyxel.load("assets/Breakout.pyxres")
        pyxel.run(self.update, self.draw)

    def blocks_creator(self):
        """Cria e posiciona os blocos para o jogo Breakout."""
        x =- 8
        y = 0
        imgx =- 7
        
        for Y in range(4):
            x =- 8
            y += 10
            imgx =- 7
            
            for X in range(5):
                x += 17
                imgx += 15
                block = Object(x, y, 0, imgx, 21, 14, 8)
                self.listBlock.append(Object(x, y, 0, imgx, 21, 14, 8))

    def reset(self):
        """Resetar/restaura todo o game do início."""
        self.ball.x = pyxel.width/2 - 3 
        self.ball.y = pyxel.height - 20
        
        self.player.x = pyxel.width/2 - 19/2
        self.player.scores = 0
        self.play = False

        for block in self.listBlock:
            if block.y < 0:
                block.y = (block.y + 50)
        
    def flip_ball(self, obj):
        """Rebate a bola e muda a sua direção quando houver colisões"""
        if self.ball.x < obj.x + obj.w/2 - 3:
            self.ball.eixX1 = True
            self.ball.eixX2 = False
            
        elif self.ball.x > obj.x + obj.w/2 + 3:
            self.ball.eixX1 = False
            self.ball.eixX2 = True
            
        else:
            self.ball.eixX1 = True
            self.ball.eixX2 = True

    def check_all_collisions(self):
        """Verifica todas as colisões que devem ocorrer no jogo."""
        if self.ball.x <= 8:
            self.ball.eixX1 = False
            self.ball.eixX2 = True
            pyxel.play(1, 1)
            
        if self.ball.x + self.ball.w >= pyxel.width - 8:
            self.ball.eixX1 = True 
            self.ball.eixX2 = False
            pyxel.play(1, 1)
             
        if self.ball.y <= 8:
            self.ball.eixY1 = False
            self.ball.eixY2 = True
            pyxel.play(1, 1)

        if self.ball.check_collision(self.player):
            self.ball.eixY1 = True
            self.ball.eixY2 = False
            self.flip_ball(self.player)
            pyxel.play(1, 1)
            
        for block in self.listBlock:
            if self.ball.check_collision(block):
                self.ball.eixY2 = True
                self.ball.eixY1 = False
                self.flip_ball(block)
                block.destroy()
                pyxel.play(0, 0)
                
                for n in range(6):
                    if block.imgx == (8 - 15) + (15 * n):
                        self.player.scores += (5 * n)

    def update(self):
        """Verifica interação a cada quadro."""
        if self.play:
            self.player.move(left= (pyxel.btn(pyxel.KEY_LEFT) or
                                    pyxel.btn(pyxel.KEY_A) or
                                    pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)),
                             right= pyxel.btn(pyxel.KEY_RIGHT) or
                                    pyxel.btn(pyxel.KEY_D) or
                                    pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))
                             
            self.ball.move(left= self.ball.eixX1, 
                           right= self.ball.eixX2,
                           up= self.ball.eixY1,
                           down= self.ball.eixY2)

            self.check_all_collisions()
            
            #Game Over
            if (self.player.scores == 300 or
                self.ball.y > pyxel.height):
                
                #Verificação para resetar
                if (pyxel.btnr(pyxel.KEY_RETURN) or
                    pyxel.btnr(pyxel.KEY_KP_ENTER) or
                    pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)):
                    self.reset()
        
        #Menu Inicial
        else:
            #Verificação para inicialização do game
            if (pyxel.btnr(pyxel.KEY_RETURN) or
                pyxel.btnr(pyxel.KEY_KP_ENTER) or
                pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)):
                self.play = True
                pyxel.play(0, 0)

    def draw_centered_text(self, txt, y, col):
        """Centraliza e desenha o texto na tela"""
        text_center_x = len(txt) / 2 * pyxel.FONT_WIDTH
        pyxel.text(pyxel.width / 2 - text_center_x, y, txt, col)
    
    def draw(self):
        """atualiza a interface a cada quadro."""
        pyxel.cls(1)
        pyxel.blt(5, 0, 0, 7, 0, 100, 7)
        pyxel.blt(0, 0, 0, 0, 0, 7, 100)
        pyxel.blt(pyxel.height-7, 0, 0, 0, 0, -7, 100)

        self.ball.draw()
        self.player.draw()
        for block in self.listBlock:
            block.draw()
        
        if self.play: 
            self.draw_centered_text(str(self.player.scores), 1, 7)
            
            #Game Over
            if (self.player.scores == 300 or
                self.ball.y > pyxel.height):
                
                #Caixa de hight score
                pyxel.blt(pyxel.width/2 - 50/2, pyxel.height/2 - 34/2, 0, 8, 46, 50, 34)
                self.draw_centered_text("Total:", pyxel.height/2 - pyxel.FONT_HEIGHT, 7)
                self.draw_centered_text(str(self.player.scores), pyxel.height/2+2, 7)
                self.draw_centered_text("Press start", pyxel.height/2 + 20, 7)
                self.draw_centered_text("to return", pyxel.height/2 + 30, 7)
        
        #Menu inicial
        else:
            pyxel.blt(pyxel.width/2 - 63/2, pyxel.height/2 , 0, 8, 8, 63, 12)
            self.draw_centered_text("press start", pyxel.height/2 + 13, pyxel.frame_count %16)
        
if __name__ == "__main__":
    Game()
