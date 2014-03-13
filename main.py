import pyglet
import math
from pyglet import clock
from pyglet.window import mouse
from pyglet.window import key
from pyglet.gl import *

window = pyglet.window.Window()
size_x = 800
size_y = 600
window.set_size(size_x,size_y)

draw = 1
radius = 10
pos_x = size_x/2
pos_y = size_y/2
Vx = 0
Vy = 0
maxVx = 125
maxVy = 200

fps_display = clock.ClockDisplay()

keys = key.KeyStateHandler()
window.push_handlers(keys)

def friction(axis):
	global Vx, Vy
	
	if axis == 'x':
		if Vx > 0:
			Vx -= 10
		
			if Vx < 0:
				Vx = 0
		elif Vx < 0:
			Vx += 10
		
			if Vx > 0:
				Vx = 0
	elif axis == 'y':
		if Vy > 0:
			Vy -= 10
		
			if Vy < 0:
				Vy = 0
		elif Vy < 0:
			Vy += 10
		
			if Vy > 0:
				Vy = 0

				
def collision(axis):
	global Vx, Vy

	if axis == 'x':
		Vx = Vx/2 * -1
	
	if axis == 'y':
		Vy = Vy/2 * -1
	
def handleBoundaries():
	global radius, pos_x, pos_y, Vx, Vy

	# collision left or right bounds
	if pos_x - radius < 0:
		collision('x')			
		pos_x = radius
	elif pos_x + radius > size_x:
		collision('x')			
		pos_x = size_x - radius
	
	# collision with top or bottom bounds
	if pos_y - radius < 0:
		collision('y')
		pos_y = radius
	elif pos_y + radius > size_y:
		collision('y')
		pos_y = size_y - radius

		
def move(dt):
	global pos_x, pos_y, Vx, Vy, maxVx, maxVy
	
	Dx = Vx * dt
	Dy = Vy * dt
	
	pos_x = pos_x + Dx
	pos_y = pos_y + Dy

	
def handleMovement():
	global radius, Vx, Vy

	if keys[key.W] and keys[key.A]:
		Vx -= 5
		Vy += 8
	elif keys[key.W] and keys[key.D]:
		Vx += 5
		Vy += 8
	elif keys[key.S] and keys[key.A]:
		Vx -= 5
		Vy -= 8
	elif keys[key.S] and keys[key.D]:
		Vx += 5
		Vy -= 8
	elif keys[key.W]:
		Vy += 8
		friction('x')
	elif keys[key.A]:
		Vx -= 5
		friction('y')
	elif keys[key.S]:
		Vy -= 8
		friction('x')
	elif keys[key.D]:
		Vx += 5
		friction('y')
	else:
		friction('x')
		friction('y')
	
	# max velocity
	if Vx > maxVx:
		Vx = maxVx
	elif Vx < -maxVx:
		Vx = -maxVx
	
	if Vy > maxVy:
		Vy = maxVy
	elif Vy < -maxVy:
		Vy = -maxVy
	
	handleBoundaries()

#def on_mouse_motion(x, y, dx, dy):
	

@window.event
def on_draw():
	global draw, radius, pos_x, pos_y

	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	
	glTranslatef(300,200,0)
	glRotatef(20, 0, 0, 1)
	
	glBegin(GL_LINE_LOOP)
	glVertex2i(0,0)
	glVertex2i(100,0)
	glVertex2i(50,200)
	glEnd()
	'''
	batch = pyglet.graphics.Batch()
	vertices = []
	
	
	for i in range(0,360):
		radians = math.radians(i)
		x = math.cos(radians) * radius + pos_x
		y = math.sin(radians) * radius + pos_y
		vertices.append(x)
		vertices.append(y)

	if draw:
		vertex_list = batch.add(360, GL_LINE_LOOP, None, ('v2f', vertices))
		fps_display.draw()
		batch.draw()
	'''

def update(dt):
	global Vx, Vy
	
	handleMovement()
	move(dt)
	
#pyglet.clock.schedule(update)
clock.set_fps_limit(60)
pyglet.app.run()