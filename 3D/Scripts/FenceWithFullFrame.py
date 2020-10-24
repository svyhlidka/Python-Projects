import bpy
import numpy as np
from collections import Counter

framesList = [[2.80, 1.71, 45, 0.5, 1]]    #frame length, frame height, plank_angle, space between frames, planks over frame = 1
       
#    [2.81,0.90, 45, 0.0],[2.81,0.90,-45, 1.0],
#    [2.80,1.71, 45, 0.0],[2.80,1.71, -45, 1.0],[2.81,0.90, 45, 0.],[2.81,0.90, -45,1]
#     ]

plank_width = 0.088 # perpendicular width of the plank
plank_thickness = 0.018
space_width = 0.015  #perpendicular distance between planks
#plank_angle = 45
reserve_cut = 0.02
show_frame = True#
frame_width_x = 0.04
frame_width_y = 0.04
frame_width_z = 0.04
steel_thickness = 0.004
Lframe_width_x=0.035
Lframe_width_y=0.03
apply_corr = False
over = 1


    

frame_angle = 90  # frame angle not implemented yet
plank_colors = [(0.0, 0.3, 0.0, 1)]
frame_color = (0.1, 0.4, 0.5, 1)
xyz = [0.0,0.0,0.0]   #starting position left-down corner


# ===================beginning of future import lib calcFence.py =========================================================== 
#class Plank(object):
#    
#    def __init__(self, width):
#        """
#           position: 
#           float in meters
#           list [x,y] of point A
#           width:
#           float in meters
#           plank: array [A,B,C,D,E]
#           E added for frame corner/plank crash handling
#           color: list of strings e.g. 'blue'
#        """
#        self.positionA = [0.,0.]
#        self.plank_width = width
#        self.plank_length = 0
#        self.color = ''
#        
#        self.plank = np.array([[0.,0.], [0.,0.], [0.,0.], [0.,0.],[0.,0.]])
#        
#        
#        
#    def __str__(self):
#        return (f'plank object: length: {self.plank_length} color: {self.color}')

#    def plank_Length(self):
#        if self.plank[3][0] != self.plank[4][0] or self.plank[3][1] != self.plank[4][1]:
#            xmin = (self.plank[1][0]+self.plank[0][0])/2
#            ymin = (self.plank[1][1]+self.plank[0][1])/2
#            xmax = max(self.plank[2][0],self.plank[3][0])
#            ymax = max(self.plank[2][1],self.plank[3][1])
#        else:
#            xmax, ymax = self.plank.max(axis=0)
#            xmin, ymin = self.plank.min(axis=0)
#        self.plank_length = round(np.sqrt((xmax-xmin)**2+(ymax-ymin)**2),3)   
#        return self.plank_length

#       
#    def calculate_plank_Horizontal(self, frame_length, frame_height, x, y,
#                                   tanFi, plankH, plankV, deltaH, deltaV):
#        """
#         calculate_plank_Horizontal
#         x, y  starting position on the frame (deltaH,0):left-down corner ==> (frame_length,frame_height):upper-left corner
#               continues on (previous x +plankH+deltaH) until y <= frame_height+plankH+deltaH
#               possible positions intervals:
#                         (0,0)<->(frame_length,0),
#                         (0,0)<->(0,frame_height),
#                         (0,0)<->(frame_length,frame_height)
#                         
#         returns np.array(A,B,C,D,E) rounded to 3 dec.points
#        """

#        Cx = frame_height/tanFi + x
#        if Cx + plankH <= frame_length: # still fit to top
#            self.plank[0] = [x,y]
#            self.plank[1] = [x + plankH, y]
#            self.plank[3] = [Cx,frame_height]
#            self.plank[4] = self.plank[3]
#            self.plank[2] = [Cx + plankH, frame_height]
#            self.plank = np.round_(self.plank, decimals = 3)
#            return True
#        else:
#            return False

#                
#    def calculate_plank_Left_Vertical(self, frame_length, frame_height, x, y, 
#                                      tanFi, plankH, plankV, deltaH, deltaV):
#        
#        """
#         calculate_plank_Left_Vertical
#         x, y  starting position on the frame  (0,0):left-down corner ==> (0,frame_height) :upper-left corner
#            continues on (0,previous+plankV+deltaV) until y <= frame_height + plankV + deltaV
#               possible positions intervals:
#                         (0,0)<->(0,0),
#                         (0,0)<->(0,frame_height),
#                                             
#         returns np.array(A,B,C,D,E) rounded to 3 dec.points
#        """

#        Dx = (frame_height-y)/tanFi
#        Cy = (frame_length-x)*tanFi
#        if Dx  > frame_length:
#            self.plank[2] = [frame_length, Cy+y] #frame_height-((Dx-frame_length)*tanFi)-deltaH]
#            self.plank[3] = [frame_length, min(Cy + y + plankV,frame_height)] #frame_height-((Dx-frame_length)*tanFi)-deltaH]  #[frame_length, Cy+plankV] 
#            self.plank[4] = [min(frame_length,Dx-plankH), min(Cy + y + plankV,frame_height)] #frame_height]
#            self.plank[0] = [0, y + plankV]
#            self.plank[1] = [0, y]
#            self.plank = np.round_(self.plank, decimals = 3)
#            return True
#        elif Dx - plankH >= -plankH/2: # 0:
#            if Dx - plankH <= 0:
#                self.plank[3] =  [0, frame_height] # [Dx - plankH, frame_height]
#                self.plank[4] = self.plank[3]
#                self.plank[2] = [Dx, frame_height]
#            else:
#                self.plank[3] = [Dx - plankH, frame_height]
#                self.plank[4] = self.plank[3]
#                self.plank[2] = [Dx, frame_height]
#            if (y + plankV) >  frame_height:
#                self.plank[0] = [0, frame_height]
#            else:
#                self.plank[0] = [0, y + plankV]
#            self.plank[1] = [0, y]
#            self.plank = np.round_(self.plank, decimals = 3)
#            return True
#        else:
#            return False
#    
#    def calculate_plank_Right_Vertical(self,  frame_length, frame_height, x, y,
#                                       tanFi, plankH, plankV, deltaH, deltaV):
#        """
#         calculate_plank_Right_Vertical
#         x, y  starting position on the frame  (~frame_length,frame_height):lright-upper corner ==> (frame_length,0) : right-down corner
#            continues on (0,previous-plankH-deltaH) until y => 0 + plankV + deltaV
#               possible positions intervals:
#                         (0,0)<->(0,0),
#                         (0,0)<->(0,frame_height),
#                                             
#         returns np.array(A,B,C,D,E) rounded to 3 dec.points
#        """


#        Cy = (frame_length-x)*tanFi
#        if Cy - plankV > -plankV/2: #0.01: # right down corner, plank wider than space
#            if (Cy - plankV) <= 0:
#                self.plank[0] = [x, 0]
#                self.plank[1] = [frame_length, 0]   #[x+plankH, 0]
#                self.plank[2] = [frame_length, 0]
#                self.plank[3] = [frame_length, Cy] 
#                self.plank[4] = self.plank[3]
#                self.plank = np.round_(self.plank, decimals = 3)
#                return True
#            else:
#                self.plank[0] = [x, 0]
#                self.plank[1] = [x+plankH, 0]
#                if Cy > frame_height:    # frame corner at middle of plank 
#                    self.plank[2] = [frame_length, Cy - plankV]
#                    self.plank[4] = [frame_length-((Cy-frame_height)/tanFi), frame_height]
#                    self.plank[3] = [frame_length , frame_height]
#                else:
#                    self.plank[2] = [frame_length, Cy - plankV]
#                    self.plank[3] = [frame_length, Cy] 
#                    self.plank[4] = self.plank[3]
#                    self.plank = np.round_(self.plank, decimals = 3)
#                return True
#        else:
#            return False

#    def calculate_plank_0(self, angle, frame_length, frame_height, x, y,
#                          plank_width, space_width ):
#        """
#         for angle = 0 or 90  deg only
#         returns np.array(A,B,C,D) rounded to 3 dec.points
#        """
#        if angle > 0:
#            self.plank[0] = [x, 0]
#            self.plank[1] = [x + plank_width, 0]
#            self.plank[2] = [x + plank_width, frame_height]
#            self.plank[3] = [x, frame_height]
#            self.plank[4] = [x , frame_height]
#            self.plank = np.round_(self.plank, decimals = 3)
#            return True # for future use?
#        else:
#            self.plank[0] = [frame_length, y ]
#            self.plank[1] = [0, y]
#            self.plank[2] = [0, min(frame_height,y + plank_width)]
#            self.plank[3] = [frame_length, min(frame_height,y + plank_width)] 
#            self.plank[4] = [frame_length, min(frame_height,y + plank_width)]
#            self.plank = np.round_(self.plank, decimals = 3)
#            return True # for future use?
# 
#class fenceFrame(object):
#    def __init__(self, frame_length, frame_height, frame_angle, plank_angle,
#        plank_width, space_width, plank_color, show_frame, frame_width, frame_color, reserve_cut):
#        """
#        frame_length, frame_height, plank_width, space_width: float in meters
#        angle: float in degrees
#            frame_angle frame angle
#            plank_angle planks slope
#        """
#        self.plank_orientation = (plank_angle >= 0)
#        self.frame_length = frame_length
#        self.frame_height = frame_height
#        self.frame_width  = frame_width
#        self.frame_angle  = frame_angle
#        self.frame_color  = frame_color
#        self.plank_angle  = abs(plank_angle)
#        self.plank_width  = plank_width
#        self.space_width  = space_width
#        self.plank_color  = plank_color
#        self.show_frame   = show_frame
#        self.reserve_cut  = reserve_cut
#        
#        self.planksList = []
#        self.planksLengths = []
#        self.total_plank_length = 0
#        
#        
#        if self.plank_angle in [0, 90]:
#            self.tanFi   = 0
#            self.cotanFi = 0
#            self.deltaH = space_width # verical distance
#            self.deltaV = space_width # horizontal distance
#            self.plankH = plank_width # plank width (in  verical direction)
#            self.plankV = plank_width # plank width (in horizontal direction)

#        else:
#            self.tanFi   = np.tan(np.radians(self.plank_angle))
#            self.cotanFi = np.arctan(np.tan(np.radians(self.plank_angle)))
#            self.deltaH  = ((space_width)/np.sin(np.radians(self.plank_angle))) # verical distance
#            self.deltaV  = ((space_width)/np.cos(np.radians(self.plank_angle))) # horizontal distance
#            self.plankH  = ((plank_width)/np.sin(np.radians(self.plank_angle))) # plank width (in  verical direction)
#            self.plankV  = ((plank_width)/np.cos(np.radians(self.plank_angle))) # plank width (in horizontal direction)
#            
#        self.frame = []
#        if self.show_frame:    
#            xy=[(-1*self.frame_width, -1*self.frame_width), (-1*self.frame_width, 0.0),
#                (self.frame_length+frame_width, 0), (self.frame_length+self.frame_width, -1*self.frame_width)]
#            self.frame.append(xy)
#            xy=[(-1*self.frame_width, self.frame_height), (-1*self.frame_width, self.frame_height+self.frame_width),
#                (self.frame_length+frame_width, self.frame_height+self.frame_width), (self.frame_length+self.frame_width, self.frame_height)]
#            self.frame.append(xy)
#            xy=[(-1*self.frame_width, 0), (0, 0), (0,self.frame_height), (-1*self.frame_width, self.frame_height)]
#            self.frame.append(xy)
#            xy=[(self.frame_length, 0), (self.frame_length+self.frame_width, 0),
#                (self.frame_length+frame_width,self.frame_height), (self.frame_length, self.frame_height)]
#            self.frame.append(xy)
#    
#    def __str__(self):
#        return(f' frame {self.frame_length}x{ self.frame_height} plank angle: {self.plank_angle}')
#        
#    def total_plank_Length(self):
#        """
#        Returns total length of planks including cutting reserve for each plank 
#        -------
#        total : TYPE
#            DESCRIPTION.

#        """
#        total = 0
#        for l in self.planksLengths:
#            total += (l+self.reserve_cut)
#        self.total_plank_length = round(total,3)
#        return round(total,3)


#    def angle_0_90(self):
#        if self.plank_angle:                  # 90 degrees
#            x = 0
#            y = 0
#            i = 0
#            plank=Plank(self.plank_width)
#            while x < self.frame_length + self.space_width:
#                plank.calculate_plank_0(self.plank_angle, self.frame_length, self.frame_height, x, y, self.plank_width, self.space_width)
#                self.planksList.append(plank)
#                self.planksLengths.append(self.frame_height)
#                x += (self.plank_width + self.space_width)
#                i += 1
#                plank=Plank(self.plank_width)
#        else:                                # 0 degrees
#            x = 0
#            y = self.space_width
#            i = 0
#            plank=Plank(self.plank_width)
#            while y < self.frame_height+self.space_width:
#                plank.calculate_plank_0(self.plank_angle, self.frame_length, self.frame_height, x, y, self.plank_width, self.space_width)
#                self.planksList.append(plank)
#                self.planksLengths.append(self.frame_length)
#                y += (self.plank_width + self.space_width)
#                i += 1
#                plank=Plank(self.plank_width)
#            
#    def angle_normal(self):
#        # Horizontal Left to Right
#        x = self.deltaH
#        y = 0.0
#        i = 0
#        plank=Plank(self.plank_width)
#        ok = True
#        while ok: 
#            ok=plank.calculate_plank_Horizontal(self.frame_length, self.frame_height, x, y, 
#                            self.tanFi, self.plankH, self.plankV, self.deltaH, self.deltaV)
#            if ok:
#                self.planksList.append(plank)
#                self.planksLengths.append(plank.plank_Length())
#                i += 1
#                x = plank.plank[1][0]+self.deltaH
#                plank=Plank(self.plank_width)
#       # print(f'Horizontal Left to Right  {i}')   
#        
#        if i > 0: 
#            # Right vertical starting point is last B from Horizontal calculation (or max(s[1][0]))
#            x = self.planksList[i-1].plank[1][0]+self.deltaH
#            y = (self.frame_length-x)*self.tanFi-self.deltaV
#        else:
#            x = 0
#            y = 0
#        i = 0
#        plank=Plank(self.plank_width)
#        ok = True
#        while ok: 
#            ok=plank.calculate_plank_Right_Vertical(self.frame_length, self.frame_height, x, y, 
#                              self.tanFi, self.plankH, self.plankV, self.deltaH, self.deltaV)
#            if ok:
#                self.planksList.append(plank)
#                self.planksLengths.append(plank.plank_Length())
#                i += 1
#                x = plank.plank[1][0]+self.deltaH
#                y = (self.frame_length-x)*self.tanFi-self.deltaV
#                plank=Plank(self.plank_width)
#       # print(f'Right vertical {i}')
#        
#        
#        # Left vertical
#        x = 0.0
#        y = 0.0 #self.deltaV
#        i = 0
#        plank=Plank(self.plank_width)
#        ok = True
#        while ok:
#            ok=plank.calculate_plank_Left_Vertical(self.frame_length, self.frame_height, x, y, 
#                              self.tanFi, self.plankH, self.plankV, self.deltaH, self.deltaV)
#            if ok:
#                self.planksList.append(plank)
#                self.planksLengths.append(plank.plank_Length())
#                i += 1
#                y = plank.plank[0][1]+self.deltaV
#                plank=Plank(self.plank_width)


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

    # def plank_Length(self):
    #     if self.plank[3][0] != self.plank[4][0] or self.plank[3][1] != self.plank[4][1]:
    #         xmin = (self.plank[1][0]+self.plank[0][0])/2
    #         ymin = (self.plank[1][1]+self.plank[0][1])/2
    #         xmax = max(self.plank[2][0],self.plank[3][0])
    #         ymax = max(self.plank[2][1],self.plank[3][1])
    #     else:
    #         xmax, ymax = self.plank.max(axis=0)
    #         xmin, ymin = self.plank.min(axis=0)
    #     self.plank_length = round(np.sqrt((xmax-xmin)**2+(ymax-ymin)**2),3)   
    #     return self.plank_length
    def plank_Length(self, apply_corr, corr):
        """
        
        Parameters
        ----------
        apply_corr: boolean
               if true, correction applied
        corr : float 
               tanFi*plank_width
               correction for total needed length

        Returns
        -------
        float
            length of plank

        """

        if self.plank[3][0] != self.plank[4][0] or self.plank[3][1] != self.plank[4][1]:
            xmin = (self.plank[1][0]+self.plank[0][0])/2
            ymin = (self.plank[1][1]+self.plank[0][1])/2
            xmax = max(self.plank[2][0],self.plank[3][0])
            ymax = max(self.plank[2][1],self.plank[3][1])
        else:
            xmax, ymax = self.plank.max(axis=0)
            xmin, ymin = self.plank.min(axis=0)
        a=round(np.sqrt(np.sum((self.plank[3] - self.plank[0]) ** 2)),3)
        b=round(np.sqrt(np.sum((self.plank[2] - self.plank[1]) ** 2)),3)
        if a == b:
            self.plank_length = a + apply_corr*corr
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
            if (y + plankV) >  frame_height:
                self.plank[0] = [0, frame_height]
            else:
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
        plank_width, space_width, plank_color, show_frame, frame_width, frame_color, reserve_cut, apply_corr):
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
        self.apply_corr   = apply_corr
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
            self.tanFi   = np.tan(np.radians(self.plank_angle))
            self.cotanFi = np.arctan(np.tan(np.radians(self.plank_angle)))
            self.deltaH  = ((space_width)/np.sin(np.radians(self.plank_angle))) # verical distance
            self.deltaV  = ((space_width)/np.cos(np.radians(self.plank_angle))) # horizontal distance
            self.plankH  = ((plank_width)/np.sin(np.radians(self.plank_angle))) # plank width (in  verical direction)
            self.plankV  = ((plank_width)/np.cos(np.radians(self.plank_angle))) # plank width (in horizontal direction)
            
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
                self.planksLengths.append(plank.plank_Length(self.apply_corr, self.tanFi*self.plank_width))
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
                self.planksLengths.append(plank.plank_Length(self.apply_corr, self.tanFi*self.plank_width))
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
                self.planksLengths.append(plank.plank_Length(self.apply_corr, self.tanFi*self.plank_width))
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




#=============== end of future lib calcFence.py ================================================================

def calculateFrame(
      frame_length,
      frame_height,
      frame_angle,
      plank_angle,
      plank_width,
      space_width,
      plank_colors,
      show_frame,
      frame_width,
      frame_color,
      reserve_cut,
      apply_corr,
      xyz):  
      
      
    ff = fenceFrame(
          frame_length,
          frame_height,
          frame_angle,
          plank_angle,
          plank_width,
          space_width,
          plank_colors,
          show_frame,
          frame_width,
          frame_color,
          reserve_cut,
          apply_corr)  

    if int(ff.plank_angle) in [0, 90]:
        ff.angle_0_90()
    else:
        ff.angle_normal()

    planks = []      # this is what createMesh expects!!!!!!!!!!!!!!!!

      
    for p in ff.planksList:
        if plank_angle < 0:
            pp = (abs([frame_length,0]-p.plank))
        else:
            pp = p.plank

        planks.append(np.round(pp+[xyz[0],xyz[1]],3).tolist())
        
    return planks




# ============================================================================== 

#class FenceProject(bpy.types.Operator):
#    
#    bl_idname  = "object.fence_frame"
#    bl_label   = "Fence Project - Frame"
#    bl_options = {'REGISTER', 'UNDO'} 


def createFrameMesh(a, c, lx, ly, lz, xyz): 
    """
       a,c frame cross section
       a - x coord
       c - z coord
       lx frame length in x ..
       xyz - zero position .
       returns 
    """
    verts = []
    edges = []
    faces = []
    v = [0,0,0,0]

   
    v[0] = np.array([
        [0.,0.,0], [a,0.,a], 
        [a,c,a], [0.,c,0.]
        ])
    v[0] += xyz        
    v[1] = np.array([
        [lx-a,0,a], [lx,0,0],
        [lx,c,0], [lx-a,c,a]
        ]) 
    v[1] += xyz 
    v[2] = np.array([
        [lx-a,0,lz-a], [lx,0,lz],
        [lx,c,lz], [lx-a,c,lz-a]
        ]) 
    v[2] += xyz 

    v[3] = np.array([
        [0,0,lz], [a,0,lz-a], 
        [a,c,lz-a], [0,c,lz]
        ])
    v[3] += xyz        
    
    edges = [
        [0,1], [1,2], [2,3], [3,0], 
        [4,5], [5,6], [6,7], [7,4],
        [8,9], [9,10], [10,11], [11,8],
        [12,13], [13,14], [14,15], [15,12],
        [0,5], [1,4], [2,7], [3,6],
        [4,8], [5,9], [6,10], [7,11],
        [8,13], [9,12], [11,14], [10,15],
        [12,0], [13,1], [15,3], [14,2]
        ]
    
    #faces = [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]]
    
    verts=[list(iitem) for item in v for iitem in item]
    
    faces = [
        [0,5,4,1], [0,5,6,3], [1,4,7,2], [6,7,2,3],
        [4,8,9,5], [5,6,10,9], [6,10,11,7], [4,7,11,8],
        [8,9,12,13], [11,10,15,14], [9,10,15,12], [8,11,14,13],
        [0,1,13,12], [2,14,15,3], [1,2,14,13], [0,3,15,12]
         ]
    
    #faces = [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]]
    
    verts=[list(iitem) for item in v for iitem in item]
    
    return verts, edges, faces

    

def createMesh(plank, z, xyz):
    """
       
       z - z-coordinate
       xyz - zero position
       returns 
    """
    verts = []
    edges = []
    faces = []
    
#base = bpy.ops.mesh.primitive_plain_add()
    pl = []     #removing duplicates vertices (possible numbers 3, 4, 5)
    for item in plank:
        pl.append(item)
            
    j = len(pl) 

    for i in range(j):
        verts.append([ pl[i][0], xyz[2], pl[i][1]]) #swapping y to z
    for i in range(j):
        verts.append([ pl[i][0], xyz[2]+z, pl[i][1]]) #swapping y to z
    
    if j == 5:
        edges = [[0,1], [1,2], [2,3], [3,4], [4,0], [5,6], [6,7], [7,8], [8,9],[9,5],[0,5],[1,6],[2,7],[3,8],[4,9]]
    elif j == 4:
        edges = [[0,1], [1,2], [2,3], [3,0], [4,5], [5,6], [6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]
    else:
        edges = [[0,1], [1,2], [2,0], [3,4], [4,5], [5,3], [0,3], [1,4], [2,5]]


    if j == 5:
        faces = [
            [0,1,2,3,4],[5,6,7,8,9],  
            [0,1,6,5],[1,2,7,6],[2,3,8,7],[3,4,9,8],[4,0,5,9]
        ]
    elif j == 4:
        faces = [
            [0,1,2,3],[4,5,6,7],
            [0,1,5,4],[1,2,6,5],[2,3,7,6] ,[3,0,4,7]
        ]
    else:
        faces = [[0,1,2], [3,4,5], [0,1,4,3], [1,2,5,4], [0,2,5,3]]
        
    return verts, edges, faces


last_frame_length = 0.0
last_frame_height = 0.0
f = 0
for frame in framesList:
    f += 1
    frame_length = frame[0]
    frame_height = frame[1]
    over = frame[4]
#    print('f: ',f, frame_length, frame_height)
    
    frame_mat = bpy.data.materials.new(name = "Frame Material")
    
    xyz0 = [0,0,0]
    xyz0[0] = xyz[0] + frame_width_x
    xyz0[1] = xyz[1] - steel_thickness
    xyz0[2] = xyz[2] + frame_width_x


    vert, edg , fac = createFrameMesh(steel_thickness, Lframe_width_x, frame_length-2*frame_width_x, 0, frame_height-2*frame_width_x, xyz0)
    nameF1 = f'Frame1 Nr.{f}'
    meshF1 = bpy.data.meshes.new(nameF1) 
    meshF1.from_pydata(vert, edg , fac)  
    objF1  = bpy.data.objects.new(nameF1, meshF1)
    bpy.context.collection.objects.link(objF1)
    bpy.context.view_layer.objects.active = objF1
    s0 = bpy.context.active_object
    s0.data.materials.append(frame_mat)
    bpy.context.object.active_material.diffuse_color = frame_color #change color

    xyz0[1] += steel_thickness

    vert, edg , fac = createFrameMesh(Lframe_width_y, steel_thickness, frame_length-2*frame_width_x, 0, frame_height-2*frame_width_x, xyz0)
    nameF2 = f'Frame2 Nr.{f}'
    meshF2 = bpy.data.meshes.new(nameF2) 
    meshF2.from_pydata(vert, edg , fac)  
    objF2  = bpy.data.objects.new(nameF2, meshF2)
    bpy.context.collection.objects.link(objF2)
    bpy.context.view_layer.objects.active = objF2
    s1 = bpy.context.active_object
    s1.data.materials.append(frame_mat)
    bpy.context.object.active_material.diffuse_color = frame_color #change color


    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()

    vert, edg , fac  = createFrameMesh(frame_width_x, frame_width_y, frame_length, 0, frame_height, xyz)
    nameF = f'Frame Nr.{f}'
    meshF = bpy.data.meshes.new(nameF) 
    meshF.from_pydata(vert, edg , fac)  
    objF  = bpy.data.objects.new(nameF, meshF)
    bpy.context.collection.objects.link(objF)
    bpy.context.view_layer.objects.active = objF
    so = bpy.context.active_object
    so.data.materials.append(frame_mat)
    bpy.context.object.active_material.diffuse_color = frame_color #change color



#    vert, edg , fac  = createFrameMesh(frame_width_x, frame_width_y, frame_length, 0, frame_height, np.array(xyz))
#    nameF = f'Frame Nr.{f}'
#    meshF = bpy.data.meshes.new(nameF) 
#    meshF.from_pydata(vert, edg , fac)  
#    objF  = bpy.data.objects.new(nameF, meshF)
#    bpy.context.collection.objects.link(objF)
#    bpy.context.view_layer.objects.active = objF
#    so = bpy.context.active_object
#    so.data.materials.append(frame_mat)
#    bpy.context.object.active_material.diffuse_color = frame_color #change color
#     
    if over:
        xyz[1] += 0.001
        xyz[0] += last_frame_length
        xyz[2]  =  -1*plank_thickness
        fl = frame_length
        fh = frame_height
    else:
        xyz[1] +=  frame_width_z  + steel_thickness
        xyz[0] += last_frame_length + frame_width_x + steel_thickness
        xyz[2]  = plank_thickness #frame_width_z + steel_thickness  
        
        fl = frame_length - 2*(frame_width_x + steel_thickness)
        fh = frame_height -2*(frame_width_z + steel_thickness)

        
        
    last_frame_length = frame[3] + frame_length
    last_frame_height = frame_height
    
    
    planks = calculateFrame(
                  fl,
                  fh,
                  frame_angle,
                  frame[2],
                  plank_width,
                  space_width,
                  plank_colors,
                  show_frame,
                  frame_width_x,
                  frame_color,
                  reserve_cut,
                  apply_corr,
                  xyz 
            ) 
             
    i=1
    for plank in planks:
        verts, edges, faces = createMesh(plank,plank_thickness, xyz) 
        name = f'Fr:{f} Plank Nr.{i}'
        mesh = bpy.data.meshes.new(name) 
        mesh.from_pydata(verts, edges, faces)    
        obj  = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        if i==1:
            new_mat = bpy.data.materials.new(name = "Plank Material")
        so = bpy.context.active_object
        so.data.materials.append(new_mat)
        bpy.context.object.active_material.diffuse_color = plank_colors[0] #change color
        i += 1
#        return {'FINISHED'}
