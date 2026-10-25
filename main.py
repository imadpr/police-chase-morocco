from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import random, os

# Touch-friendly Android adaptation of Police Chase Morocco.
class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_x = 0.5
        self.player_y = 0.15
        self.enemies = []
        self.notes = []
        self.score = 0
        self.money = 0
        self.speed = 0.42
        self.spawn = 0
        self.cash_spawn = 0
        self.road_offset = 0
        self.over = False
        self.siren_on = True
        self.siren = SoundLoader.load(os.path.join(os.path.dirname(__file__), 'police_siren.mp3'))
        if self.siren:
            self.siren.loop = True
            self.siren.volume = .6
            self.siren.play()
        self.bind(size=self.redraw, pos=self.redraw)
        Clock.schedule_interval(self.update, 1/60)
        self.redraw()

    def rect(self, color, x, y, w, h, radius=0):
        Color(*color)
        if radius:
            RoundedRectangle(pos=(x,y), size=(w,h), radius=[radius])
        else:
            Rectangle(pos=(x,y), size=(w,h))

    def label(self, text, x, y, size=18, color=(1,1,1,1), width=260):
        l = Label(text=text, pos=(x,y), size_hint=(None,None), size=(width,32), font_size=size, color=color, bold=True, halign='left', valign='middle')
        l.text_size = l.size
        self.add_widget(l)

    def car(self, cx, cy, w, h, police=False, color=(.8,.1,.1,1)):
        x, y = cx-w/2, cy-h/2
        self.rect((.04,.04,.05,1), x-5,y+h*.18,8,h*.22,3)
        self.rect((.04,.04,.05,1), x+w-3,y+h*.18,8,h*.22,3)
        self.rect((.04,.04,.05,1), x-5,y+h*.62,8,h*.22,3)
        self.rect((.04,.04,.05,1), x+w-3,y+h*.62,8,h*.22,3)
        self.rect((.95,.95,.94,1) if police else color, x,y,w,h,9)
        if police:
            self.rect((.08,.23,.65,1),x+3,y+h*.25,w-6,h*.38,5)
        self.rect((.24,.65,.78,1),x+w*.16,y+h*.63,w*.68,h*.2,4)
        self.rect((.15,.35,.45,1),x+w*.2,y+h*.43,w*.6,h*.13,3)
        if police:
            self.rect((1,.08,.08,1),x+w*.17,y+h*.9,w*.27,5,2)
            self.rect((.1,.25,1,1),x+w*.56,y+h*.9,w*.27,5,2)
            self.label('POLICE',x+1,y+h*.25, max(9,w*.18), width=w)
        else:
            self.rect((1,.85,.15,1),x+w*.1,y+h*.94,w*.2,4)
            self.rect((1,.85,.15,1),x+w*.7,y+h*.94,w*.2,4)

    def redraw(self, *args):
        self.canvas.clear()
        self.clear_widgets()
        w,h=self.size
        if w<=0 or h<=0: return
        with self.canvas:
            self.rect((.12,.48,.22,1),0,0,w,h)
            left=w*.15; rw=w*.70
            self.rect((.20,.20,.23,1),left,0,rw,h)
            self.rect((.95,.95,.95,1),left,0,4,h)
            self.rect((.95,.95,.95,1),left+rw-4,0,4,h)
            for lane in (left+rw/3,left+2*rw/3):
                y=-(self.road_offset % (h*.11))
                while y<h:
                    self.rect((.95,.95,.95,1),lane-2,y,4,h*.055)
                    y += h*.11
            for n in self.notes:
                x=n['x']*w; y=n['y']*h
                c={20:(.7,.25,.6,1),50:(.1,.55,.3,1),100:(.8,.25,.15,1),200:(.1,.45,.7,1)}[n['value']]
                self.rect(c,x-23,y-12,46,24,4)
                Color(1,1,1,1); Line(rectangle=(x-23,y-12,46,24),width=1.2)
                self.label(str(n['value']),x-22,y-15,12,width=44)
            for e in self.enemies:
                self.car(e['x']*w,e['y']*h,w*.075,h*.12,color=e['color'])
            self.car(self.player_x*w,self.player_y*h,w*.085,h*.13,police=True)
        self.label(f'Score: {self.score}',8,h-40,18,width=150)
        self.label(f'Argent: {self.money} DH',8,h-72,15,(1,.85,.2,1),width=190)
        self.label('SIRENE: '+('ON' if self.siren_on else 'OFF')+' (bouton)',8,h-102,12,width=230)
        if self.over:
            self.rect((0,0,0,.72),w*.08,h*.30,w*.84,h*.36,12)
            self.label('GAME OVER!',w*.25,h*.53,30,(1,.15,.15,1),width=w*.5)
            self.label(f'Score: {self.score}    Dirhams: {self.money} DH',w*.1,h*.45,16,width=w*.8)
            self.label('Appuie sur REJOUER',w*.2,h*.37,17,width=w*.6)

    def update(self, dt):
        if self.over: return
        w,h=self.size
        if w<=0 or h<=0:return
        self.score += 1
        self.speed=min(.85,.42+self.score/7000)
        self.road_offset += h*self.speed*dt
        self.spawn += dt; self.cash_spawn += dt
        if self.spawn > max(.38,1.05-self.score/9000):
            self.spawn=0
            self.enemies.append({'x':random.uniform(.24,.76),'y':1.12,'color':random.choice([(1,.12,.12,1),(1,.75,.1,1),(.7,.15,.7,1),(.1,.7,.35,1),(.9,.4,.1,1)]),'speed':random.uniform(.22,.5)})
        if self.cash_spawn>1.7:
            self.cash_spawn=0
            self.notes.append({'x':random.uniform(.23,.77),'y':1.05,'value':random.choice([20,50,100,200])})
        for e in self.enemies:e['y']-= (self.speed+e['speed'])*dt
        self.enemies=[e for e in self.enemies if e['y']>-.15]
        for n in self.notes:n['y']-=self.speed*dt
        kept=[]
        for n in self.notes:
            if abs(n['x']-self.player_x)<.09 and abs(n['y']-self.player_y)<.09:self.money+=n['value']
            elif n['y']>-.05:kept.append(n)
        self.notes=kept
        for e in self.enemies:
            if abs(e['x']-self.player_x)<.09 and abs(e['y']-self.player_y)<.10:
                self.over=True
                break
        self.redraw()

    def on_touch_down(self,touch):
        if self.over:return True
        self.move_to(touch.x,touch.y)
        return True
    def on_touch_move(self,touch):
        if not self.over:self.move_to(touch.x,touch.y)
        return True
    def move_to(self,x,y):
        w,h=self.size
        if w and h:
            self.player_x=max(.23,min(.77,x/w))
            self.player_y=max(.12,min(.88,y/h))
            self.redraw()
    def toggle_siren(self,*args):
        self.siren_on=not self.siren_on
        if self.siren:
            if self.siren_on:self.siren.play()
            else:self.siren.stop()
        self.redraw()
    def restart(self,*args):
        self.player_x=.5; self.player_y=.15; self.enemies=[]; self.notes=[]
        self.score=0; self.money=0; self.spawn=0; self.cash_spawn=0; self.over=False
        self.redraw()

class PoliceApp(App):
    def build(self):
        root=FloatLayout()
        self.game=Game(size_hint=(1,1))
        root.add_widget(self.game)
        siren_btn=Button(text='SIRENE ON/OFF',size_hint=(.28,.065),pos_hint={'right':.98,'top':.99},font_size='13sp')
        siren_btn.bind(on_release=self.game.toggle_siren)
        root.add_widget(siren_btn)
        restart_btn=Button(text='REJOUER',size_hint=(.25,.065),pos_hint={'right':.98,'y':.01},font_size='13sp')
        restart_btn.bind(on_release=self.game.restart)
        root.add_widget(restart_btn)
        return root
    def on_stop(self):
        if getattr(self,'game',None) and self.game.siren:self.game.siren.stop()

if __name__ == '__main__':
    PoliceApp().run()
