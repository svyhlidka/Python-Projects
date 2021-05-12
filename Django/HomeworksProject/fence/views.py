from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from fence.forms import FenceDefinitionForm
#import fence.calcFenceImgToBuffer 
from fence.calcFence import Plank, fenceFrame, Fence
from operator import itemgetter

from matplotlib.figure import Figure
import matplotlib.patches as patches #polygon draw
from io import BytesIO
import base64

#from collections import Counter

framesList = []
    # [2.80,1.71],[2.81,0.90],[2.81,0.90],
    # [2.81,0.90],[2.60,1.71],[2.81,1.71]
#          

class FenceDefinitionView(TemplateView):
    template_name = 'fence/fence.html'

    def get(self,request):

        #posts = Post.objects.all()      
        context = {}
        context['form'] = FenceDefinitionForm() #, 'posts':posts, 'users': users, 'friends': friends}
        return render(request, self.template_name, context)

    def generate_picture(self, ff, xmax, ymax, printName):
        """
        

        Parameters
        ----------
        ff : fenceFrame object
            
        xmax : float
            maximal frame length
        ymax : float
            maximal frame height
        printName : bool
            print plank name

        Returns
        -------
        graphic : TYPE
            DESCRIPTION.

        """
        ff.total_plank_Length()  # calculating total
        fig = Figure(figsize=(ff.frame_length, ff.frame_height),  dpi=600)
        fig.set_size_inches(7,4)
        labeldegree = '$^\circ$' 
        str=f'[m]\n angle: {ff.plank_angle}{labeldegree}, total planks: {len(ff.planksList)}, total planks length: {ff.total_plank_length} [m]'
        ax = fig.add_subplot(1,1,1)
        ax.set_xlabel(str, fontsize=8)
        ax.set_ylabel('[m]', fontsize=8)
        ax.tick_params(direction='out', length=6, width=2, colors='black') ####
        ax.set_xlim([-2*ff.frame_width, xmax+2*ff.frame_width])
        ax.set_ylim([-2*ff.frame_width, ymax+2*ff.frame_width])
        ax.set_title(f'Frame: {ff.frame_Id}  {ff.frame_length:.3f} x {ff.frame_height:.3f}', size=8)
        col = 0
        for plank in ff.planksList:  # adding single planks
            if ff.plank_orientation:
                xy=list(tuple(map(tuple,plank.plank)))
            else:
                xy=list(tuple(map(tuple,(abs([ff.frame_length,0]-plank.plank)))))
            ax.add_patch(patches.Polygon(xy, facecolor=ff.plank_color[col]))
            if printName:
                x = (plank.plank[2][0]-plank.plank[0][0])/2 + plank.plank[0][0]
                y = (plank.plank[2][1]-plank.plank[0][1])/2 + plank.plank[0][1]
                if plank.plank_name.find('/') > 0: s=plank.plank_name[plank.plank_name.index('/')+1:]  
                else: s = plank.plank_name
                ax.annotate(s, (x,y), color='w', weight='bold', 
                    fontsize=6, ha='center', va='center')

            col += 1
            if col > len(ff.plank_color)-1:
                col = 0
            
        if ff.show_frame:    
            for xy in ff.frame:
                ax.add_patch(patches.Polygon(xy, facecolor=ff.frame_color))
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

    
    def post(self, request):

        form = FenceDefinitionForm(request.POST,initial={'frame_color': 'black'}) # form initialization - blank
        if form.is_valid():
            framesList=form.cleaned_data['frames_dimensions']
            ################################################################
            images = []
            headers = []
            fence = Fence()
            xmax = max(framesList, key=itemgetter(0))[0]
            ymax = max(framesList, key=itemgetter(1))[1]
            frameNr = 0
            for item in framesList:
                frameNr += 1
                ff = fenceFrame(
                      str(frameNr),
                      item[0], #form.cleaned_data['frame_length'],
                      item[1], #form.cleaned_data['frame_height'],
                      45.0, #form.cleaned_data['frame_angle'],
                      form.cleaned_data['plank_angle'],
                      form.cleaned_data['plank_width'],
                      form.cleaned_data['space_width'],
                      form.cleaned_data['plank_colors'],
                      form.cleaned_data['show_frame'],
                      form.cleaned_data['frame_width'],
                      form.cleaned_data['frame_color'],
                      form.cleaned_data['reserve_cut'],
                      form.cleaned_data['apply_corr']
                      )   
                if int(ff.plank_angle) in [0, 90]:
                    ff.angle_0_90()
                else:
                    ff.angle_normal()
                raw_plank_length = form.cleaned_data['raw_plank_length']
                ################################################################

                graphic = self.generate_picture(ff, xmax, ymax, form.cleaned_data['print_plank_name'])
                headers.append( f'Frame: {ff.frame_length:.3f} x {ff.frame_height:.3f}')
                images.append(graphic)
                fence.framesList.append(ff)
            if raw_plank_length:
                rawList = fence.calculateRawMaterialNeeds(raw_plank_length, form.cleaned_data['reserve_cut'])
            else:
                rawList = []
            l = [(item[0],[(x[0].replace("'",""),x[1]) for x in item[1]]) for item in rawList]
            context = {'form':form, 'images': images, 'rawNum': len(rawList), 'rawList': l}    
            #context = {'form':form, 'image': graphic} #'/media/outputs/Figure212904.png'}
            return render(request, self.template_name, context)
            return redirect('fence:fence') 
        #graphic = ff.generate_picture()
        context = {'form':form} #'/media/outputs/Figure212904.png'}
        return render(request, self.template_name, context)
