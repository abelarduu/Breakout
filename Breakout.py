############
# Breakout #
############
import pyxel

class Object:
    def __init__(self, x:int, y:int, img:int, imgx:int, imgy:int, w:int, h:int):
        self.x = x
        self.y = y
        self.img = img
        self.imgx= imgx
        self.imgy= imgy
        self.w = w
        self.h= h
        self.scores= 0
        
    def move(self, cond1, cond2, cond3=None, cond4=None):
        if cond1 and self.x > 8: self.x-=2                    
        if cond2 and self.x + self.w <= pyxel.width-9: self.x+=2
        if cond3: self.y-=2                                  
        if cond4: self.y+=2        

    def check_collision(self, obj):
        if self.y+ self.h >= obj.y and self.y <= obj.y +obj.h:
            if self.x + self.w >= obj.x and self.x<= obj.x + obj.w:
                return True
                
    def destroy(self):
        self.y=(self.y-50)

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.imgx, self.imgy, self.w, self.h)
        
class Game:
    def __init__(self):
        pyxel.init(100, 100, "Breakout")
        self.play= False
        #Objetos
        self.player= Object(pyxel.width/2 - 19/2, pyxel.height -11, 0, 8, 30, 19, 8)
        self.ball= Object(pyxel.width/2 - 3, pyxel.height -20, 0, 8,39, 6, 6)
        self.ball.eixX1= True
        self.ball.eixX2= False
        self.ball.eixY1= True
        self.ball.eixY2= False

        self.listBlock = []
        self.blocks_creator()

        pyxel.load("resources/Breakout.pyxres")
        pyxel.run(self.update, self.draw)

    def blocks_creator(self):
        x=-8
        y=0
        imgx=-7
        for Y in range(4):
            x=-8
            y+= 10
            imgx=-7
            
            for X in range(5):
                x+= 17
                imgx+= 15
                block=Object(x, y, 0, imgx, 21, 14, 8)
                self.listBlock.append(Object(x, y, 0, imgx, 21, 14, 8))

    def reset(self):
        self.ball.x, self.ball.y= pyxel.width/2 -3, pyxel.height -20
        self.player.x= pyxel.width/2 -19/2
        self.player.scores= 0
        self.play= False

        for block in self.listBlock:
            if block.y< 0:
                block.y = (block.y+50)
        
    def flip_ball(self, obj):
        if self.ball.x< obj.x + obj.w/2-3:
            self.ball.eixX1=True
            self.ball.eixX2=False
            
        elif self.ball.x> obj.x + obj.w/2+3:
            self.ball.eixX1=False
            self.ball.eixX2=True
            
        else:
            self.ball.eixX1=True
            self.ball.eixX2=True

    def update(self):
        if self.play:
            self.player.move(cond1= pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A),
                             cond2= pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D))
                             
            self.ball.move(cond1= self.ball.eixX1, 
                           cond2= self.ball.eixX2,
                           cond3= self.ball.eixY1,
                           cond4= self.ball.eixY2)

            if self.ball.x <= 8:
                self.ball.eixX1=False
                self.ball.eixX2=True
                pyxel.play(1,1)
                
            if self.ball.x+ self.ball.w >= pyxel.width-8:
                self.ball.eixX1=True 
                self.ball.eixX2=False
                pyxel.play(1,1)
                 
            if self.ball.y <= 8:
                self.ball.eixY1=False
                self.ball.eixY2=True
                pyxel.play(1,1)

            if self.ball.check_collision(self.player):
                self.ball.eixY1=True
                self.ball.eixY2=False
                self.flip_ball(self.player)
                pyxel.play(1,1)
                
            for block in self.listBlock:
                if self.ball.check_collision(block):
                    self.ball.eixY2=True
                    self.ball.eixY1=False
                    self.flip_ball(block)
                    block.destroy()
                    pyxel.play(0,0)
                    
                    for n in range(6):
                        if block.imgx == (8-15)+(15*n):
                            self.player.scores+= (5*n)
                        
            if pyxel.btn(pyxel.KEY_R):
                self.reset()
        else:
            if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START):
                self.play=True


            
    def draw(self):
        pyxel.cls(1)
        pyxel.blt(5, 0, 0, 7, 0, 100, 7)
        pyxel.blt(0, 0, 0, 0, 0, 7, 100)
        pyxel.blt(pyxel.height-7, 0, 0, 0, 0, -7, 100)

        
        self.ball.draw()
        self.player.draw()
        for block in self.listBlock:
            block.draw()
         
        if self.play: 
            pyxel.text(pyxel.width/2 - len(str(self.player.scores))/2 * pyxel.FONT_WIDTH, 1, str(self.player.scores), 7)
            
            if self.player.scores == 300 or self.ball.y > pyxel.height:
                pyxel.blt(pyxel.width/2 - 50/2, pyxel.height/2 - 34/2, 0, 8, 46, 50, 34)
                pyxel.text(pyxel.width/2 - (len("Total:")/2 * pyxel.FONT_WIDTH), pyxel.height/2 - pyxel.FONT_HEIGHT, "Total:", 7)
                pyxel.text(pyxel.width/2 - (len(str(self.player.scores))/2 * pyxel.FONT_WIDTH), pyxel.height/2+2, str(self.player.scores), 7)
                pyxel.text(pyxel.width/2 - (len("Press 'R'")/2 * pyxel.FONT_WIDTH), pyxel.height/2+20, "Press 'R'\nto return", 7)
        else:
            pyxel.blt(pyxel.width/2 - 63/2, pyxel.height/2 , 0, 8, 8, 63, 12)
            pyxel.text(pyxel.width/2 -len("press start")/2 * pyxel.FONT_WIDTH, pyxel.height/2 +13, "press start", pyxel.frame_count %16)

if __name__ == "__main__":
    Game()