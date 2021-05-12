# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 11:51:33 2020

@author: stvyh
"""


from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


COLORS = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('red', 'Red'),
    ('black', 'Black'),
    ('brown', 'Brown'),
    ('yellow', 'Yellow')
    ]

    
class FenceDefinitionForm(forms.Form):
    
   
    # framesList = [
    # [2.80,1.71],[2.81,0.90],[2.81,0.90],
    # [2.81,0.90],[2.60,1.71],[2.81,1.71]
    #             ]

    frames_dimensions = forms.CharField(required=True, 
                    label='Frames Dimensions:',
                    help_text="One Frame per Line in the format e.g. 3.125x2.869 in meters. No other characters are valid!",
                    widget=forms.Textarea(attrs={'rows': '6', 'cols': '15'}))
    plank_width  = forms.FloatField(label='Plank Width:',required=True,help_text = "Perpendicular width of the plank in meters.")
    space_width  = forms.FloatField(label='Distance:',
                    required=True,help_text = "Perpendicular distance between planks in meters.")
    plank_angle  = forms.FloatField(label='Plank Angle:',
                    required=True,help_text = "Plank angle in degrees.")
    reserve_cut  = forms.FloatField(label='Reserve Cut:',
                    required=True,help_text = "Reserve cut.")
    plank_colors = forms.MultipleChoiceField(label='Plank Colors:',
                    required=False,
                    widget=forms.SelectMultiple(),
                    choices=COLORS,
                    help_text = "Plank color, select one or more for alternation.")
    show_frame   = forms.BooleanField(label='Show Frame:',
                    required=False,help_text='Check, if you want to see frame.')
    frame_width  = forms.FloatField(label='Frame Width:',
                    required=True,help_text = "Frame width in meters.")
    frame_color  = forms.ChoiceField(label='Frame Color:',
        required=False,
        choices=COLORS,
        help_text = "Select frame color."
    )
    raw_plank_length = forms.FloatField(label='Raw Plank Length:',required=False,
                    help_text = "The length of the board from which planks will be cut in meters.")
    apply_corr       = forms.BooleanField(label='Apply correction:',
                    required=False,help_text='Check, if you want to apply correction in plank length calculation as reserve for cut.')
    print_plank_name   = forms.BooleanField(label='Print plank name:',
                    required=False,help_text='Check, if you want to print plank name in image')
    # frame_angle = 90  # frame angle not implemented yet
    

    def clean_plank_width(self):
        data  = self.cleaned_data['plank_width']
      #  data1 = self.cleaned_data['frame_length']
        if data <= 0: # or data >= data1:
            raise ValidationError(_('Plank Width must be > 0 and less than Frame Length!!!'))
        return data
            
    def clean_plank_angle(self):
        data = self.cleaned_data['plank_angle']
        if abs(data) > 90:
            raise ValidationError(_('Angle must be between 0 and 90 degrees incl.!!!'))
        return data
    
    def clean_plank_colors(self):
        color = self.cleaned_data['plank_colors']
        if not color:
            raise forms.ValidationError(_("Please select at least one color for plank."))
        return color

    def clean_raw_plank_length(self):
        lght = self.cleaned_data['raw_plank_length']
        if lght and lght <= 0 :
            raise forms.ValidationError(_("Please check raw plank length."))
        return lght
    
    
    def clean_frames_dimensions(self):
        """
        converts output from frames_dimensions form
        to list
        
        Parameters
        ----------
        s : input from frames_dimensions form
    
        Returns
        -------
        list
            list of frames dimensions.
        string
            string with format error
    
        """
        xx = self.cleaned_data['frames_dimensions']
        s=(":".join("{:02x}".format(ord(c)) for c in xx))
        s=s.replace(':',"")
        s=s.replace(' ',"")
        s=bytearray.fromhex(s).decode()
        l=[]
        x=0
        y=0
        while len(s)>0:
            i = s.find('x')
            try:
                x=float(s[:i])
            except:
               raise forms.ValidationError(_(f"Something went wrong in input. See: =>{s}<="))
            s=s[i+1:]
            i = s.find('\r\n')
            if i <= 0:
                i=len(s)
            try:
                y=float(s[:i])
            except:
               raise forms.ValidationError(_(f"Something went wrong in input. See: =>{s}<="))
            s=s[i+2:]
            l.append([x,y])
        return l
        