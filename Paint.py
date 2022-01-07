from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename,asksaveasfile
from tkinter.ttk import Combobox
from math import sin,cos,ceil
from PIL import Image,ImageTk
import pyscreenshot
import io
import os

class window:
	global root
	def __init__(self):
		global canvas
		global last
		self.file=None
		self.now=None
		self.status=Label(root,text='welcome',bd=1,relief=SUNKEN,anchor=E)
		self.status.pack(side=BOTTOM,fill=X)
		root.bind('<Motion>',self.coords)
		menu=Menu(root)
		root.config(menu=menu)
		#buttons
		self.size=1
		data=list(range(1,51))
		buttonframe=Frame(root)
		buttonframe.pack(fill=X)
		self.cb=Combobox(buttonframe,values=data)
		self.cb.pack(side=LEFT)
		self.cb.bind('<<ComboboxSelected>>',self.size_change)
		self.fgcolor='black'
		Button(buttonframe,text='forground color',command=lambda:self.color_choose('fg')).pack(side=LEFT)
		pen_button=Button(buttonframe,text='pen',width=10,command=lambda:self.binder('pen')).pack(side=LEFT)
		eraser=Button(buttonframe,text='eraser',width=10,command=lambda:self.binder('eraser')).pack(side=LEFT)
		canvas=Canvas(root,width=1057,height=655,bd=2,relief=RAISED,bg='white')
		canvas.pack(fill=BOTH,expand='yes')
		#file slidebar
		file=Menu(menu)
		menu.add_cascade(label='File',menu=file)
		file.add_command(label='Open',command=lambda:self.file_operations('open'))
		file.add_command(label='New',command=lambda:self.file_operations('new'))
		file.add_command(label='save',command=lambda:self.file_operations('save'))
		file.add_command(label='save as',command=lambda:self.file_operations('saveas'))
		file.add_command(label='About Paint')
		file.add_separator()
		file.add_command(label='Exit',command=root.quit)
		#shapes submenu
		shapes=Menu(menu)
		menu.add_cascade(label='Shapes',menu=shapes)
		shapes.add_command(label='line',command=lambda:self.binder('l'))
		shapes.add_command(label='rectangle',command=lambda:self.binder('r'))
		shapes.add_command(label='oval',command=lambda:self.binder('o'))
		shapes.add_command(label='polygon',command=lambda:self.binder('polygon'))
		shapes.add_command(label='regular polygon',command=lambda:self.binder('rpolygon'))
	def open_file(self,event):
		self.photo = ImageTk.PhotoImage(file=self.file)
		self.Artwork=canvas.create_image(event.x, event.y,anchor=NW,image=self.photo)
		root.unbind('<ButtonPress-1>')
	def _canvas(self):
		x=canvas.winfo_rootx()
		y=canvas.winfo_rooty()
		x1=x+canvas.winfo_width()
		y1=y+canvas.winfo_height()
		box=(x,y,x1,y1)
		return(box)		
	def color_choose(self,type):
		canvas.unbind('<ButtonPress-1>')
		canvas.unbind('<ButtonRelease-1>')
		canvas.unbind('<B1-Motion>')
		if type=='fg':
			self.fgcolor=askcolor(color=self.fgcolor)[1]
	def size_change(self,event):
		canvas.unbind('<ButtonPress-1>')
		canvas.unbind('<ButtonRelease-1>')
		canvas.unbind('<B1-Motion>')
		self.size=self.cb.get()
	def coords(self,event):
		self.status.forget()
		self.status=Label(root,text=str(event.x)+','+str(event.y)+' | welcome',bd=1,relief=SUNKEN,anchor=E)
		self.status.pack(side=BOTTOM,fill=X)
	def saveas(self,fname):
		ps=canvas.postscript(colormode='color')
		img=Image.open(io.BytesIO(ps.encode('utf-8')))
		# img.show()
		with open(fname.name, 'wb') as f:
			img.save(f, format="png")
			f.close()
	def file_operations(self,type):
		if type=='saveas':
			fname=asksaveasfile(mode='wb', defaultextension='.png')
			self.saveas(fname)
		elif type=='save':
			if self.file==None:
				fname=asksaveasfile(mode='wb', defaultextension='.png')
				self.file=fname
				self.saveas(fname)
			else:
				self.saveas(self.file)
		elif type=='open':
			fname=askopenfilename(filetypes=(('JPEG files','*.jpeg'),('PNG files','*.png')))
			self.file=fname
			root.bind('<ButtonPress-1>',self.open_file)
		elif type=='new':
			os.system('python main.py')
	def binder(self,shape):
		canvas.unbind('<ButtonPress-1>')
		canvas.unbind('<ButtonRelease-1>')
		canvas.unbind('<B1-Motion>')
		if shape=='l':
			canvas.bind('<ButtonPress-1>',self.draw_line)
			canvas.bind('<B1-Motion>',self.draw_line)
			canvas.bind('<ButtonRelease-1>',self.draw_line)
		elif shape=='r':
			canvas.bind('<ButtonPress-1>',self.draw_rectangle)
			canvas.bind('<B1-Motion>',self.draw_rectangle)
			canvas.bind('<ButtonRelease-1>',self.draw_rectangle)
		elif shape=='o':
			canvas.bind('<ButtonPress-1>',self.draw_oval)
			canvas.bind('<B1-Motion>',self.draw_oval)
			canvas.bind('<ButtonRelease-1>',self.draw_oval)
		elif shape=='pen':
			canvas.bind('<ButtonPress-1>',self.pen)
			canvas.bind('<B1-Motion>',self.pen)
			canvas.bind('<ButtonRelease-1>',self.reset_coords)
		elif shape=='eraser':
			canvas.bind('<ButtonPress-1>',self.eraser)
			canvas.bind('<B1-Motion>',self.eraser)
			canvas.bind('<ButtonRelease-1>',self.reset_coords)
		elif shape=='polygon':
			self.label=Label(root,text='Enter no. of sides')
			self.label.pack(side=LEFT)
			self.sides_get=Entry(root)
			self.sides_get.pack(side=LEFT)
			self.n=0
			self.sides_get.bind('<Return>',self.draw_polygon)
		elif shape=='rpolygon':
			self.label=Label(root,text='Enter no. of sides')
			self.label.pack(side=LEFT)
			self.sides_get=Entry(root)
			self.sides_get.pack(side=LEFT)
			self.n=0
			self.sides_get.bind('<Return>',self.regular_polygon)
		
	def pen(self,event):
		if str(event.type)=='ButtonPress':
			canvas.oldcoords=event.x,event.y
		else:
			x,y=event.x,event.y
			if canvas.oldcoords:
				xf,yf=canvas.oldcoords
				canvas.create_line(x,y,xf,yf,width=self.size,capstyle=ROUND,smooth=True,splinesteps=2,fill=self.fgcolor)
			canvas.oldcoords=x,y
			self.now=canvas.postscript(colormode='color')
	def eraser(self,event):
		if str(event.type)=='ButtonPress':
			canvas.oldcoords=event.x,event.y
		else:
			x,y=event.x,event.y
			if canvas.oldcoords:
				xf,yf=canvas.oldcoords
				canvas.create_line(x,y,xf,yf,width=40,fill='white',capstyle=ROUND,smooth=True,splinesteps=2)
			canvas.oldcoords=x,y
			self.now=canvas.postscript(colormode='color')
	def draw_line(self,event):
		if str(event.type)=='ButtonPress':
			canvas.oldcoords=event.x,event.y
			global myline
			myline=canvas.create_line(event.x,event.y,event.x+1,event.y+1,width=self.size,capstyle=ROUND,smooth=True,fill=self.fgcolor)
		elif str(event.type)=='ButtonRelease':
			canvas.delete(myline)
			xf,yf=event.x,event.y
			xi,yi=canvas.oldcoords
			last=canvas.create_line(xi,yi,xf,yf,width=self.size,capstyle=ROUND,smooth=True,fill=self.fgcolor)
			canvas.oldcoords=None
		else:
			canvas.delete(myline)
			xf,yf=event.x,event.y
			xi,yi=canvas.oldcoords
			myline=canvas.create_line(xi,yi,xf,yf,width=self.size,capstyle=ROUND,smooth=True,fill=self.fgcolor)
	def draw_rectangle(self,event):
		if str(event.type)=='ButtonPress':
			canvas.oldcoords=event.x,event.y
			global myrect
			myrect=canvas.create_rectangle(event.x,event.y,event.x+1,event.y+1,width=self.size,outline=self.fgcolor)
		elif str(event.type)=='ButtonRelease':
			canvas.delete(myrect)
			xf,yf=event.x,event.y
			xi,yi=canvas.oldcoords
			last=canvas.create_rectangle(xi,yi,xf,yf,width=self.size,outline=self.fgcolor)
			canvas.oldcoords=None
		else:
			canvas.delete(myrect)
			xf,yf=event.x,event.y
			xi,yi=canvas.oldcoords
			myrect=canvas.create_rectangle(xi,yi,xf,yf,width=self.size,outline=self.fgcolor)
	def draw_oval(self,event):
		if str(event.type)=='ButtonPress':
			canvas.oldcoords=event.x,event.y
			global myoval
			myoval=canvas.create_oval(event.x,event.y,event.x+1,event.y+1,width=self.size,outline=self.fgcolor)
		elif str(event.type)=='ButtonRelease':
			xf,yf=event.x,event.y
			xi,yi=canvas.oldcoords
			last=canvas.create_oval(xi,yi,xf,yf,width=self.size,outline=self.fgcolor)
			canvas.oldcoords=None
		else:
			canvas.delete(myoval)
			xf,yf=event.x,event.y
			xi,yi=canvas.oldcoords
			myoval=canvas.create_oval(xi,yi,xf,yf,width=self.size,outline=self.fgcolor)
	def draw_polygon(self,event):
		self.sides=int(self.sides_get.get())
		self.sides_get.forget()
		self.label.forget()
		if self.n==0:
			self.n+=1
			canvas.bind('<ButtonPress-1>',self.draw_polygon)
		elif self.n==1:
			self.xi,self.yi=event.x,event.y
			self.xf,self.yf=event.x,event.y
			self.n+=1
			canvas.bind('<ButtonPress-1>',self.draw_polygon)
		elif self.n<self.sides:
			canvas.unbind('<ButtonPress-1>')
			canvas.create_line(self.xi,self.yi,event.x,event.y,width=self.size,capstyle=ROUND,smooth=True,fill=self.fgcolor)
			self.xi,self.yi=event.x,event.y
			self.n+=1
			canvas.bind('<ButtonPress-1>',self.draw_polygon)
		elif self.n==self.sides:
			canvas.unbind('<ButtonPress-1>')
			canvas.create_line(self.xi,self.yi,event.x,event.y,width=self.size,capstyle=ROUND,smooth=True,fill=self.fgcolor)
			canvas.create_line(event.x,event.y,self.xf,self.yf,width=self.size,capstyle=ROUND,smooth=True,fill=self.fgcolor)
	def regular_polygon(self,event):
		self.sides=int(self.sides_get.get())
		self.sides_get.forget()
		self.label.forget()
		self.angle=2*3.14159/self.sides
		if self.n==0:
			self.n+=1
			canvas.bind('<ButtonPress-1>',self.regular_polygon)
		elif self.n==1:
			canvas.unbind('<ButtonPress-1>')
			self.n+=1
			self.l=[]
			self.xi,self.yi=event.x,event.y
			canvas.bind('<ButtonPress-1>',self.regular_polygon)
		else:
			canvas.unbind('<ButtonPress-1>')
			self.l.append(event.x)
			self.l.append(event.y)
			r=(((event.x-self.xi)**2)+((event.y-self.yi)**2))**(1/2)
			while self.n<=self.sides:
				self.n+=1
				self.l.append(ceil((self.xi+(self.l[-2]-self.xi)*cos(self.angle))-((self.l[-1]-self.yi)*sin(self.angle))))
				self.l.append(ceil((self.yi+(self.l[-2]-self.yi)*cos(self.angle))+((self.l[-3]-self.xi)*sin(self.angle))))
			canvas.create_polygon(self.l,width=self.size,fill='',outline=self.fgcolor)
	def reset_coords(self,event):
		canvas.oldcoords = None


root=Tk()
root.title('Paint')
o=window()

root.mainloop()


