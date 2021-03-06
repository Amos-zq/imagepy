# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:10:17 2016

@author: yxl
"""

import wx
from core.draw import paint
from core.roi.operator import affine
from roi import ROI

class LineRoi(ROI):
    dtype = 'line'
    def __init__(self, body=None):
        self.body = body if body!=None else []
        self.update = body!=None
        self.infoupdate = body!=None
        self.box = [1000,1000,-1000,-1000]
        
    def addline(self, line):
        if len(line)!=2 or line[0] !=line[-1]:
            self.body.append(line)
            self.update, self.infoupdate = True, True
            return True
    
    def snap(self, x, y, lim):
        minl, idx = 1000, None
        for i in self.body:
            for j in i:
                d = (j[0]-x)**2+(j[1]-y)**2
                if d < minl:minl,idx = d,(i, i.index(j))
        return idx if minl**0.5<lim else None
        
    def countbox(self):
        self.box = [1000,1000,-1000,-1000]
        for i in self.body:
            for x,y in i:
                if x<self.box[0]:self.box[0]=x
                if x>self.box[2]:self.box[2]=x
                if y<self.box[1]:self.box[1]=y
                if y>self.box[3]:self.box[3]=y
        
    def get_box(self):
        if self.infoupdate:
            self.countbox()
            self.infoupdate=False
        return self.box
        
    def pick(self, x, y, lim):
        return self.snap(x, y, lim)

    def draged(self, ox, oy, nx, ny, i):
        i[0][i[1]] = (nx, ny)
        self.update, self.infoupdate = True, True
        
    def draw(self, dc, f):
        dc.SetPen(wx.Pen((255,255,0), width=1, style=wx.SOLID))
        for line in self.body:
            if len(line)>1:
                dc.DrawLines([f(*i) for i in line])
                for i in line:dc.DrawCircle(f(*i),2)
        #for i in self.buf:
        
    def affine(self, m, o):
        plg = LineRoi()
        plg.body = affine(self.body, m, o)
        plg.update = True
        plg.infoupdate = True
        return plg
        
    def sketch(self, img, w=1, color=None):
        pen = paint.Paint()
        for i in self.body:
            xs, ys = [x[0] for x in i], [x[1] for x in i]
            pen.draw_path(img, xs, ys, w, color)
            
    def fill(self, img, color=None):
        self.sketch(img, 1, color)