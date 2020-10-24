# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 19:29:11 2020

@author: stvyh
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 21:30:53 2020

@author: stvyh

see document "Planks - 2D Model.ipynb"

"""

# -*- coding: utf-8 -*-

import numpy as np
from matplotlib.figure import Figure
import matplotlib.patches as patches #polygon draw
from io import BytesIO
import base64
from collections import Counter

        
class Plank(object):
    
    def __init__(self, width):
        """
           position: 
           float in meters
           list [x,y] of point A
           width:
           float in meters
           plank: array [A,B,C,D,E]
           E added for frame corner/plank crash handling
           color: list of strings e.g. 'blue'
        """
        self.positionA = [0.,0.]
        self.plank_width = width
        self.plank_length = 0
        self.color = ''
        
        self.plank = np.array([[0.,0.], [0.,0.], [0.,0.], [0.,0.],[0.,0.]])
        
        
        
    def __str__(self):
        return (f'plank object: length: {self.plank_length} color: {self.color}')

    def plank_Length(self, tanfi):

        if self.plank[3][0] != self.plank[4][0] or self.plank[3][1] != self.plank[4][1]:
            xmin = (self.plank[1][0]+self.plank[0][0])/2
            ymin = (self.plank[1][1]+self.plank[0][1])/2
            xmax = max(self.plank[2][0],self.plank[3][0])
            ymax = max(self.plank[2][1],self.plank[3][1])
        else:
            xmax, ymax = self.plank.max(axis=0)
            xmin, ymin = self.plank.min(axis=0)
        a=round(math.sqrt((self.plank[3][0]-self.plank[0][0])**2+(self.plank[3][1]-self.plank[0][1])**2),3) 
        b=round(math.sqrt((self.plank[2][0]-self.plank[1][0])**2+(self.plank[2][1]-self.plank[1][1])**2),3)
        if a == b:
            self.plank_length = a + self.plank_width*tanfi
        else:
            self.plank_length = max(a, b)
            
        return self.plank_length

       
    def calculate_plank_Horizontal(self, frame_length, frame_height, x, y,
                                   tanFi, plankH, plankV, deltaH, deltaV):
        """
         calculate_plank_Horizontal
         x, y  starting position on the frame (deltaH,0):left-down corner ==> (frame_length,frame_height):upper-left corner
               continues on (previous x +plankH+deltaH) until y <= frame_height+plankH+deltaH
               possible positions intervals:
                         (0,0)<->(frame_length,0),
                         (0,0)<->(0,frame_height),
                         (0,0)<->(frame_length,frame_height)
                         
         returns np.array(A,B,C,D,E) rounded to 3 dec.points
        """

        Cx = frame_height/tanFi + x
        if Cx + plankH <= frame_length: # still fit to top
            self.plank[0] = [x,y]
            self.plank[1] = [x + plankH, y]
            self.plank[3] = [Cx,frame_height]
            self.plank[4] = self.plank[3]
            self.plank[2] = [Cx + plankH, frame_height]
            self.plank = np.round_(self.plank, decimals = 3)
            return True
        else:
            return False

                
    def calculate_plank_Left_Vertical(self, frame_length, frame_height, x, y, 
                                      tanFi, plankH, plankV, deltaH, deltaV):
        
        """
         calculate_plank_Left_Vertical
         x, y  starting position on the frame  (0,0):left-down corner ==> (0,frame_height) :upper-left corner
            continues on (0,previous+plankV+deltaV) until y <= frame_height + plankV + deltaV
               possible positions intervals:
                         (0,0)<->(0,0),
                         (0,0)<->(0,frame_height),
                                             
         returns np.array(A,B,C,D,E) rounded to 3 dec.points
        """

        Dx = (frame_height-y)/tanFi
        Cy = (frame_length-x)*tanFi
        if Dx  > frame_length:
            self.plank[2] = [frame_length, Cy+y] #frame_height-((Dx-frame_length)*tanFi)-deltaH]
            self.plank[3] = [frame_length, min(Cy + y + plankV,frame_height)] #frame_height-((Dx-frame_length)*tanFi)-deltaH]  #[frame_length, Cy+plankV] 
            self.plank[4] = [min(frame_length,Dx-plankH), min(Cy + y + plankV,frame_height)] #frame_height]
            self.plank[0] = [0, y + plankV]
            self.plank[1] = [0, y]
            self.plank = np.round_(self.plank, decimals = 3)
            return True
        elif Dx - plankH >= -plankH/2: # 0:
            if Dx - plankH <= 0:
                self.plank[3] =  [0, frame_height] # [Dx - plankH, frame_height]
                self.plank[4] = self.plank[3]
                self.plank[2] = [Dx, frame_height]
            else:
                self.plank[3] = [Dx - plankH, frame_height]
                self.plank[4] = self.plank[3]
                self.plank[2] = [Dx, frame_height]
            self.plank[0] = [0, y + plankV]
            self.plank[1] = [0, y]
            self.plank = np.round_(self.plank, decimals = 3)
            return True
        else:
            return False
    
    def calculate_plank_Right_Vertical(self,  frame_length, frame_height, x, y,
                                       tanFi, plankH, plankV, deltaH, deltaV):
        """
         calculate_plank_Right_Vertical
         x, y  starting position on the frame  (~frame_length,frame_height):lright-upper corner ==> (frame_length,0) : right-down corner
            continues on (0,previous-plankH-deltaH) until y => 0 + plankV + deltaV
               possible positions intervals:
                         (0,0)<->(0,0),
                         (0,0)<->(0,frame_height),
                                             
         returns np.array(A,B,C,D,E) rounded to 3 dec.points
        """


        Cy = (frame_length-x)*tanFi
        if Cy - plankV > -plankV/2: #0.01: # right down corner, plank wider than space
            if (Cy - plankV) <= 0:
                self.plank[0] = [x, 0]
                self.plank[1] = [frame_length, 0]   #[x+plankH, 0]
                self.plank[2] = [frame_length, 0]
                self.plank[3] = [frame_length, Cy] 
                self.plank[4] = self.plank[3]
                self.plank = np.round_(self.plank, decimals = 3)
                return True
            else:
                self.plank[0] = [x, 0]
                self.plank[1] = [x+plankH, 0]
                if Cy > frame_height:    # frame corner at middle of plank 
                    self.plank[2] = [frame_length, Cy - plankV]
                    self.plank[4] = [frame_length-((Cy-frame_height)/tanFi), frame_height]
                    self.plank[3] = [frame_length , frame_height]
                else:
                    self.plank[2] = [frame_length, Cy - plankV]
                    self.plank[3] = [frame_length, Cy] 
                    self.plank[4] = self.plank[3]
                    self.plank = np.round_(self.plank, decimals = 3)
                return True
        else:
            return False

    def calculate_plank_0(self, angle, frame_length, frame_height, x, y,
                          plank_width, space_width ):
        """
         for angle = 0 or 90  deg only
         returns np.array(A,B,C,D) rounded to 3 dec.points
        """
        if angle > 0:
            self.plank[0] = [x, 0]
            self.plank[1] = [x + plank_width, 0]
            self.plank[2] = [x + plank_width, frame_height]
            self.plank[3] = [x, frame_height]
            self.plank[4] = [x , frame_height]
            self.plank = np.round_(self.plank, decimals = 3)
            return True # for future use?
        else:
            self.plank[0] = [frame_length, y ]
            self.plank[1] = [0, y]
            self.plank[2] = [0, min(frame_height,y + plank_width)]
            self.plank[3] = [frame_length, min(frame_height,y + plank_width)] 
            self.plank[4] = [frame_length, min(frame_height,y + plank_width)]
            self.plank = np.round_(self.plank, decimals = 3)
            return True # for future use?
 
class fenceFrame(object):
    def __init__(self, frame_length, frame_height, frame_angle, plank_angle,
        plank_width, space_width, plank_color, show_frame, frame_width, frame_color, reserve_cut):
        """
        frame_length, frame_height, plank_width, space_width: float in meters
        angle: float in degrees
            frame_angle frame angle
            plank_angle planks slope
        """
        self.plank_orientation = (plank_angle >= 0)
        self.frame_length = frame_length
        self.frame_height = frame_height
        self.frame_width  = frame_width
        self.frame_angle  = frame_angle
        self.frame_color  = frame_color
        self.plank_angle  = abs(plank_angle)
        self.plank_width  = plank_width
        self.space_width  = space_width
        self.plank_color  = plank_color
        self.show_frame   = show_frame
        self.reserve_cut  = reserve_cut
        
        self.planksList = []
        self.planksLengths = []
        self.total_plank_length = 0
        
        
        if self.plank_angle in [0, 90]:
            self.tanFi   = 0
            self.cotanFi = 0
            self.deltaH = space_width # verical distance
            self.deltaV = space_width # horizontal distance
            self.plankH = plank_width # plank width (in  verical direction)
            self.plankV = plank_width # plank width (in horizontal direction)

        else:
            self.tanFi   = math.tan(math.radians(self.plank_angle))
            self.cotanFi = np.arctan(math.tan(math.radians(self.plank_angle)))
            self.deltaH  = ((space_width)/math.sin(math.radians(self.plank_angle))) # verical distance
            self.deltaV  = ((space_width)/math.cos(math.radians(self.plank_angle))) # horizontal distance
            self.plankH  = ((plank_width)/math.sin(math.radians(self.plank_angle))) # plank width (in  verical direction)
            self.plankV  = ((plank_width)/math.cos(math.radians(self.plank_angle))) # plank width (in horizontal direction)
            
        self.frame = []
        if self.show_frame:    
            xy=[(-1*self.frame_width, -1*self.frame_width), (-1*self.frame_width, 0.0),
                (self.frame_length+frame_width, 0), (self.frame_length+self.frame_width, -1*self.frame_width)]
            self.frame.append(xy)
            xy=[(-1*self.frame_width, self.frame_height), (-1*self.frame_width, self.frame_height+self.frame_width),
                (self.frame_length+frame_width, self.frame_height+self.frame_width), (self.frame_length+self.frame_width, self.frame_height)]
            self.frame.append(xy)
            xy=[(-1*self.frame_width, 0), (0, 0), (0,self.frame_height), (-1*self.frame_width, self.frame_height)]
            self.frame.append(xy)
            xy=[(self.frame_length, 0), (self.frame_length+self.frame_width, 0),
                (self.frame_length+frame_width,self.frame_height), (self.frame_length, self.frame_height)]
            self.frame.append(xy)
    
    def __str__(self):
        return(f' frame {self.frame_length}x{ self.frame_height} plank angle: {self.plank_angle}')
        
    def total_plank_Length(self):
        """
        Returns total length of planks including cutting reserve for each plank 
        -------
        total : TYPE
            DESCRIPTION.

        """
        total = 0
        for l in self.planksLengths:
            total += (l+self.reserve_cut)
        self.total_plank_length = round(total,3)
        return round(total,3)

    def generate_picture(self, xmax, ymax):
        self.total_plank_Length()  # calculating total
        fig = Figure(figsize=(self.frame_length, self.frame_height),  dpi=600)
        fig.set_size_inches(7,4)
        labeldegree = '$^\circ$' 
        str=f'[m]\n angle: {self.plank_angle}{labeldegree}, total planks: {len(self.planksList)}, total planks length: {self.total_plank_length} [m]'
        ax = fig.add_subplot(1,1,1)
        ax.set_xlabel(str, fontsize=8)
        ax.set_ylabel('[m]', fontsize=8)
        ax.tick_params(direction='out', length=6, width=2, colors='black') ####
        ax.set_xlim([-2*self.frame_width, xmax+2*self.frame_width])
        ax.set_ylim([-2*self.frame_width, ymax+2*self.frame_width])
        ax.set_title(f'Frame: {self.frame_length:.3f} x {self.frame_height:.3f}', size=8)
        col = 0
        for plank in self.planksList:  # adding single planks
            if self.plank_orientation:
                xy=list(tuple(map(tuple,plank.plank)))
            else:
                xy=list(tuple(map(tuple,(abs([self.frame_length,0]-plank.plank)))))
            ax.add_patch(patches.Polygon(xy, facecolor=self.plank_color[col]))
            col += 1
            if col > len(self.plank_color)-1:
                col = 0
            
        if self.show_frame:    
            for xy in self.frame:
                ax.add_patch(patches.Polygon(xy, facecolor=self.frame_color))
        fig.set_tight_layout(True)
        #.autolayout

        buffer = BytesIO()
        fig.savefig(buffer, format="png") 
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        return graphic

    def angle_0_90(self):
        if self.plank_angle:                  # 90 degrees
            x = 0
            y = 0
            i = 0
            plank=Plank(self.plank_width)
            while x < self.frame_length + self.space_width:
                plank.calculate_plank_0(self.plank_angle, self.frame_length, self.frame_height, x, y, self.plank_width, self.space_width)
                self.planksList.append(plank)
                self.planksLengths.append(self.frame_height)
                x += (self.plank_width + self.space_width)
                i += 1
                plank=Plank(self.plank_width)
        else:                                # 0 degrees
            x = 0
            y = self.space_width
            i = 0
            plank=Plank(self.plank_width)
            while y < self.frame_height+self.space_width:
                plank.calculate_plank_0(self.plank_angle, self.frame_length, self.frame_height, x, y, self.plank_width, self.space_width)
                self.planksList.append(plank)
                self.planksLengths.append(self.frame_length)
                y += (self.plank_width + self.space_width)
                i += 1
                plank=Plank(self.plank_width)
            
    def angle_normal(self):
        # Horizontal Left to Right
        x = self.deltaH
        y = 0.0
        i = 0
        plank=Plank(self.plank_width)
        ok = True
        while ok: 
            ok=plank.calculate_plank_Horizontal(self.frame_length, self.frame_height, x, y, 
                            self.tanFi, self.plankH, self.plankV, self.deltaH, self.deltaV)
            if ok:
                self.planksList.append(plank)
                self.planksLengths.append(plank.plank_Length(self.tanFi))
                i += 1
                x = plank.plank[1][0]+self.deltaH
                plank=Plank(self.plank_width)
       # print(f'Horizontal Left to Right  {i}')   
        
        if i > 0: 
            # Right vertical starting point is last B from Horizontal calculation (or max(s[1][0]))
            x = self.planksList[i-1].plank[1][0]+self.deltaH
            y = (self.frame_length-x)*self.tanFi-self.deltaV
        else:
            x = 0
            y = 0
        i = 0
        plank=Plank(self.plank_width)
        ok = True
        while ok: 
            ok=plank.calculate_plank_Right_Vertical(self.frame_length, self.frame_height, x, y, 
                              self.tanFi, self.plankH, self.plankV, self.deltaH, self.deltaV)
            if ok:
                self.planksList.append(plank)
                self.planksLengths.append(plank.plank_Length(self.tanFi))
                i += 1
                x = plank.plank[1][0]+self.deltaH
                y = (self.frame_length-x)*self.tanFi-self.deltaV
                plank=Plank(self.plank_width)
       # print(f'Right vertical {i}')
        
        
        # Left vertical
        x = 0.0
        y = 0.0 #self.deltaV
        i = 0
        plank=Plank(self.plank_width)
        ok = True
        while ok:
            ok=plank.calculate_plank_Left_Vertical(self.frame_length, self.frame_height, x, y, 
                              self.tanFi, self.plankH, self.plankV, self.deltaH, self.deltaV)
            if ok:
                self.planksList.append(plank)
                self.planksLengths.append(plank.plank_Length(self.tanFi))
                i += 1
                y = plank.plank[0][1]+self.deltaV
                plank=Plank(self.plank_width)

class Fence(object):
    def __init__(self):
        self.framesList = []

    def __str__(self):
        return f'Object Fence contains {len(self.framesList)} frames'
        
    
    def cumulateAndsortPlanksList(self):
        """ 
        Parameters
        ----------
        def cumulateAndsortPlanksList : 
       
        Returns
        -------
        sorted list desc by length of tuples: (plank length, number of planks given length)

        """
        allPlanks = []
        for frame in self.framesList:
            allPlanks.extend(frame.planksLengths)
        a = sorted(dict(Counter(j for j in allPlanks)).items(), key=lambda x: x, reverse=True) 
        return [[x,y] for (x,y) in a]
    

    def find_longest(self, rest, a_list):
        """
           rest: float
              rest of the plank after cut
           a_list: list
              list of planks to cut
           returns first available planck with length less then rest
        """
        for i in range(len(a_list)):
            #if a_list[i][0] <= rest:
            if a_list[i][0] <= rest:
                return i
        return -1


    def consumeSourcePlank(self, rest, a_list, reserve_cut):
        """
        rest: float
             rest/length of source plank
        a_list: list [[plank's length, number of planks given length],[],[],...]
                sorted by length descending
        reserve_cut: float
        
        returns updated a_list (used planks removed) and list of planks which
                                                  consumed source plank)
        """
        used = []
        min = a_list[len(a_list)-1][0]
        while rest > min:
            i = self.find_longest(rest, a_list) 
            if i >= 0:
                rest = rest-a_list[i][0]-reserve_cut
                used.append(a_list[i][0])
                a_list[i][1] -= 1
                if not a_list[i][1]:
                    del a_list[i]
                    if a_list:
                        min = a_list[len(a_list)-1][0]
                    else:
                        return a_list, used
            else:
                return a_list, used
        return a_list, used
    
    def calculateRawMaterialNeeds(self, raw_plank_length, reserve_cut):
        """
        

        Parameters
        ----------
        raw_plank_length : float
        reserve_cut: float
        
        Returns
        -------
        consumed : list
            list of lists [raw plank number, list[planks lengths cut from raw plank]]

        """
        a_list = self.cumulateAndsortPlanksList()
        consumed = []
        nr = 1
        while a_list:   
            a_list, used = self.consumeSourcePlank(raw_plank_length, a_list, reserve_cut)
            consumed.append([nr,used])
            nr +=1
        return consumed

