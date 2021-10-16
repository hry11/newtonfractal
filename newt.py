import math
import pyglet
import time

window = pyglet.window.Window(resizable=True)
mouse = pyglet.window.mouse
window.maximize()
pyglet.gl.glClearColor(0,0,0.05,1)

class plane():
    origin = (0, 0)
    xaxis = None
    yaxis = None
    scale = 1  #1 pixel = 1 unit
    xmarks = []
    ymarks = []
    def __init__(self, o1, o2, s):
        self.origin = (o1, o2)
        self.scale = s
    def dispx(self, marks = True):
        self.xaxis = pyglet.shapes.Line(0, self.origin[1], window.width, self.origin[1], width=1, color=(255, 255, 255))
        self.xaxis.draw()
        if marks == True:
            self.updatexmarks()
            for m in self.xmarks:
                m.draw()
    def dispy(self, marks = True):
        self.yaxis = pyglet.shapes.Line(self.origin[0], 0, self.origin[0], window.height, width=1, color=(255, 255, 255))
        self.yaxis.draw()
        if marks == True:
            self.updateymarks()
            for m in self.ymarks:
                m.draw()
    def updatexmarks(self, p=1):
        self.xmarks = []
        #positive values
        for i in range(p*(window.width-self.origin[0])//self.scale):
            xpos = self.origin[0] + i*self.scale//p 
            num = i/p
            text = str(num)[:4]
            self.xmarks.append(pyglet.text.Label(text, font_name='Times New Roman', font_size=12, x=xpos, y=self.origin[1], anchor_x='center', anchor_y='top'))
        #negative values
        for i in range(p*self.origin[0]//self.scale):
            xpos = self.origin[0] - i*self.scale//p 
            num = -i/p
            text = str(num)[:4]
            self.xmarks.append(pyglet.text.Label(text, font_name='Times New Roman', font_size=12, x=xpos, y=self.origin[1], anchor_x='center', anchor_y='top'))
    def updateymarks(self, p=1):
        self.ymarks = []
        #positive values
        for i in range(p*(window.height-self.origin[1])//self.scale):
            ypos = self.origin[1] + i*self.scale//p 
            num = i/p
            text = str(num)[:4] if num != 0 else ''
            self.ymarks.append(pyglet.text.Label(text, font_name='Times New Roman', font_size=12, x=self.origin[0], y=ypos, anchor_x='right', anchor_y='center'))
        #negative values
        for i in range(p*self.origin[1]//self.scale):
            ypos = self.origin[1] - i*self.scale//p 
            num = -i/p
            text = str(num)[:4] if num != 0 else ''
            self.ymarks.append(pyglet.text.Label(text, font_name='Times New Roman', font_size=12, x=self.origin[0], y=ypos, anchor_x='right', anchor_y='center'))
    def moveorigin(self, dx, dy):
        self.origin = (self.origin[0]+dx, self.origin[1]+dy)
        for m in self.xmarks:
            m.x += dx
            m.y += dy
        for m in self.ymarks:
            m.x += dx
            m.y += dy
    def zoom(self, dy, mx, my):
        self.scale += dy
        d1 = (mx-self.origin[0])//self.scale
        d2 = (my-self.origin[1])//self.scale
        self.moveorigin(-dy*d1, -dy*d2)

class im():
    a, b, m, t = 0, 0, 0, 0
    color = (0, 0, 0)
    def mod(self):
        return math.sqrt(self.a**2 + self.b**2)
    def arg(self):
        if self.a != 0:
            return math.atan(self.b / self.a)
        return math.pi/2
    def disp(self, pl):
        app = pyglet.shapes.Circle(pl.origin[0] + self.a * pl.scale, pl.origin[1] + self.b * pl.scale, radius=pl.scale//15, color=self.color)
        app.draw()
    def __init__(self, a, b = 0, c = (0, 0, 0)):
        self.a = a
        self.b = b
        self.color = c
        #self.m = self.mod() #repair later
        #self.t = self.arg()
    def __add__(self, other):
        if type(other) == int or type(other) == float:
            other = im(other, 0)
        return im(self.a + other.a, self.b + other.b)
    def __radd__(self, other):
        if type(other) == int or type(other) == float:
            other = im(other, 0)
        return im(self.a + other.a, self.b + other.b)
    def __sub__(self, other):
        if type(other) == int or type(other) == float:
            other = im(other, 0)
        return im(self.a - other.a, self.b - other.b)
    def __rsub__(self, other):
        if type(other) == int or type(other) == float:
            other = im(other, 0)
        return im(self.a - other.a, self.b - other.b)
    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            other = im(other, 0)
        return im((self.a * other.a) - (self.b * other.b), self.a * other.b + self.b * other.a)
    def __rmul__(self, other):
        if type(other) == int or type(other) == float:
            other = im(other, 0)
        return im((self.a * other.a) - (self.b * other.b), self.a * other.b + self.b * other.a)
    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            other = im(other, 0)
        m = other.mod()**2
        if m == 0:
            return im(0, 0)
        opp = im(other.a/m, -other.b/m)
        return self * opp
    def __pow__(self, other):
        p = im(1, 0)
        for i in range(other):
            p *= self
        return p
    def __rpow__(self, other):
        p = im(1, 0)
        for i in range(other):
            p *= self
        return p
    def __str__(self):
        sign = '+' if self.b >= 0 else '-'
        return '(' + str(self.a) + sign + str(abs(self.b)) + 'i)'

class polynomial():
    #eg: x^5 + 5x^4 + (4+ i) should be [[1,5],[5,4],[im(4, 1), 0]]
    coeff = []
    def __init__(self, l = [[0, 0]]):
        self.coeff = l
    def __str__(self):
        s = ''
        for i in self.coeff:
            s += str(i[0]) + "x"
            if i[1] != 0:
                s += "^" + str(i[1]) + " + "
        return s 
    def image(self, x):
        s = 0
        for i in self.coeff:
            s += i[0] * (x**i[1])
        return s
    def differentiate(self):
        diffcoeff = []
        for i in self.coeff:
            if i[1] >= 1:
                diffcoeff.append([i[1]*i[0], i[1]-1])
        return polynomial(diffcoeff)

def newtonm(px, seed, i=1):
    dpx = px.differentiate()
    guess = seed
    for i in range(i):
        guess = guess - (px.image(guess)/dpx.image(guess))
    return guess

def fractal(px, roots, botright, topleft, it):
    image = [im(x, y) for x in range(botright[0], topleft[0]) for y in range(botright[1], topleft[1])]
    for z in image:
        end = newtonm(px, z, it)
        closest = roots[0]
        for z2 in roots:
            if (end-z2).mod() <= (end-closest).mod():
                closest = z2
        z.color = closest.color
    return image


p = plane(500, 500, 50)
p1 = polynomial([[1,5],[1,2],[-1, 1],[1,0]])
#p1 = polynomial([[1,2],[-7, 0]]) 
r = [im(0, -1, (255,0,0)), im(0, 1, (0, 255, 0)), im(-1.3247, 0, (0,0,255)), im(0.66236, 0.56228, (255,255,0)), im(0.66236,- 0.56228, (0,255,255))]
im = fractal(p1, r, (-10,-10), (10,10), 5)

@window.event
def on_draw():
    window.clear()
    p.dispx()
    p.dispy()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        p.moveorigin(dx, dy)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    p.zoom(scroll_y, x, y)

#pyglet.clock.schedule_interval(1, 1/30.0)
pyglet.app.run()
