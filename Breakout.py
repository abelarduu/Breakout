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
        if cond1 and self.x >8: self.x-=2                    
        if cond2 and self.x + self.w <= pyxel.width-9: self.x+=2
        if cond3: self.y-=2                                  
        if cond4: self.y+=2        

    def check_collision(self, obj):
        if self.y+ self.h >= obj.y and self.y <= obj.y +obj.h:
            if self.x + self.w >= obj.x and self.x<= obj.x + obj.w:
                return True
             
    def destroy(self):
        self.y= -16

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.imgx, self.imgy, self.w, self.h)
        
class Game:
    def __init__(self):
        pyxel.init(100,100,"Breakout")
        self.play= False
        #Objetos
        self.player= Object(pyxel.width/2 -19/2,pyxel.height -11,0,8,30,19,8)
        self.ball= Object(pyxel.width/2 -3, pyxel.height -20, 0, 8,39, 6, 6)
        self.ball.eixX1= True
        self.ball.eixX2= False
        self.ball.eixY1= True
        self.ball.eixY2= False

        self.block1= Object(9,10,0,8,21,14,8)
        self.block2= Object(26,10,0,23,21,14,8)
        self.block3= Object(43,10,0,38,21,14,8)
        self.block4= Object(60,10,0,53,21,14,8)
        self.block5= Object(77,10,0,68,21,14,8)
        
        self.block6= Object(9,20,0,8,21,14,8)
        self.block7= Object(26,20,0,23,21,14,8)
        self.block8= Object(43,20,0,38,21,14,8)
        self.block9= Object(60,20,0,53,21,14,8)
        self.block10= Object(77,20,0,68,21,14,8)    
        
        self.block11= Object(9,30,0,8,21,14,8)
        self.block12= Object(26,30,0,23,21,14,8)
        self.block13= Object(43,30,0,38,21,14,8)
        self.block14= Object(60,30,0,53,21,14,8)
        self.block15= Object(77,30,0,68,21,14,8)

        self.block16= Object(9,40,0,8,21,14,8)
        self.block17= Object(26,40,0,23,21,14,8)
        self.block18= Object(43,40,0,38,21,14,8)
        self.block19= Object(60,40,0,53,21,14,8)
        self.block20= Object(77,40,0,68,21,14,8)
        self.listBlock= [self.block1, self.block2, self.block3, self.block4, self.block5,
                         self.block6, self.block7, self.block8, self.block9, self.block10,
                         self.block11, self.block12, self.block13, self.block14, self.block15,
                         self.block16, self.block17, self.block18, self.block19, self.block20]
        
        pyxel.load("resources/Breakout.pyxres")
        pyxel.run(self.update, self.draw)
    
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
            self.player.move(cond1= pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A), cond2= pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D))
            self.ball.move(cond1= self.ball.eixX1, cond2= self.ball.eixX2,cond3= self.ball.eixY1, cond4= self.ball.eixY2)

            if self.ball.x <= 8:
                self.ball.eixX1=False
                self.ball.eixX2=True
                
            if self.ball.x+ self.ball.w >= pyxel.width-8:
                self.ball.eixX1=True 
                self.ball.eixX2=False

            if self.ball.y <= 8:
                self.ball.eixY1=False
                self.ball.eixY2=True

            if self.ball.check_collision(self.player):
                self.ball.eixY1=True
                self.ball.eixY2=False
                self.flip_ball(self.player)
    
            for block in self.listBlock:
                if self.ball.check_collision(block):
                    self.ball.eixY2=True
                    self.ball.eixY1=False
                    self.flip_ball(block)
                    block.destroy()
                    if block.imgx== 8: self.player.scores+=5
                    if block.imgx== 23: self.player.scores+=10
                    if block.imgx== 38: self.player.scores+=15
                    if block.imgx== 53: self.player.scores+=20
                    if block.imgx== 68: self.player.scores+=30
        else:
            if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START):
                self.play=True
                        
    def draw(self):
        pyxel.cls(1)
        pyxel.blt(5,0,0,7,0,100,7)
        pyxel.blt(0,0,0,0,0,7,100)
        pyxel.blt(pyxel.height-7,0,0,0,0,-7,100)
        
        self.ball.draw()
        self.player.draw()
        for block in self.listBlock:
            block.draw()
         
        if self.play: 
            pyxel.text(pyxel.width/2 - len(str(self.player.scores))/2 * pyxel.FONT_WIDTH, 1, str(self.player.scores),7)
        else:
            pyxel.blt(pyxel.width/2 - 63/2,pyxel.height/2 ,0,8,8,63,12)
            pyxel.text(pyxel.width/2 -len("press start")/2 * pyxel.FONT_WIDTH, pyxel.height/2 +13, "press start", pyxel.frame_count %16)

if __name__ == "__main__":
    Game()