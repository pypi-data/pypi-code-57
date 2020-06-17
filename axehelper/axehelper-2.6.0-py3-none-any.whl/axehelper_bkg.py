# Kornpob Bhirombhakdi

import numpy as np
import matplotlib.pyplot as plt
import copy,glob,os
from astropy.io import fits
from math import pi

class AXEhelper_BKG:
    def __init__(self,axeflist=None,fltflist=None,
                 padxleft=5,padxright=5,
                 padylow=10,halfdy=3,padyup=10,
                 adjusty=1.2
                ):
        self.axeflist = axeflist
        self.fltflist = fltflist
        self.params = (padxleft,padxright,padylow,halfdy,padyup,adjusty)
        self.headerall = self._headerall()
    ####################
    ####################
    ####################
    def make_poly2d(self):
        OBJ = {}
        fltflist = self.fltflist
        axeflist = self.axeflist
        HEADERALL = self.headerall
        for ii,i in enumerate(fltflist):
            # image
            tmp = fits.open(i)
            tmpdata = tmp[1].data.copy()
            tmpdq = tmp['DQ'].data.copy()

            # header & prep
            tmpheader = HEADERALL[axeflist[ii]]
            xref,yref = tmpheader['XYREF']
            pixx = tmpheader['PIXX']
            pixy = tmpheader['PIXY']
            cc0x,cc0y,cc1x,cc1y = tmpheader['CC']
            sectx = tmpheader['SECTX']
            secty = tmpheader['SECTY']

            # Polynomial2D
            x1 = np.arange(cc0x,cc1x)
            x2 = np.arange(cc0y,cc1y)
            x1,x2 = np.meshgrid(x1,x2)

            obj = Polynomial2D()
            obj.data['X1'] = x1.copy()
            obj.data['X2'] = x2.copy()
            obj.data['Y'] = tmpdata[cc0y:cc1y,cc0x:cc1x]
        #     print(x1.shape,x2.shape,obj.data['Y'].shape)    

            # data['MASK']
            tmp = np.full_like(tmpdq,True,dtype=bool)
            m = np.where(tmpdq==0)
            tmp[m] = False
            obj.data['MASK'] = tmp[cc0y:cc1y,cc0x:cc1x]
        #     print(obj.data['Y'].shape,obj.data['MASK'].shape)  

            OBJ[i] = copy.deepcopy(obj)
        return OBJ
    ####################
    ####################
    ####################
    def _headerall(self):
        axeflist = self.axeflist
        fltflist = self.fltflist
        padxleft,padxright,padylow,halfdy,padyup,adjusty = self.params
        
        tmp = {}
        for i in axeflist:
            # read from header
            HEADER = copy.deepcopy(fits.open(i)[1].header)
            xref,yref = HEADER['REFPNTX'],HEADER['REFPNTY']
            bb0x,bb1x = HEADER['BB0X'],HEADER['BB1X']
            orient = HEADER['ORIENT']
            cpointx,cpointy = HEADER['CPOINTX'],HEADER['CPOINTY']
            dldx0,dldx1 = HEADER['DLDX0'],HEADER['DLDX1']

            # manually adjust offset
            yref += adjusty

            # trace and wavelength
            fny = lambda x : np.tan((90.+orient)*pi/180.) * (x - cpointx) + yref
            fnw = lambda x : dldx1 * (x - cpointx) + dldx0

            pixx = np.array([round(xref),round(bb1x)],dtype=int)
            pixy = np.round(fny(pixx)).astype(int)
            ww = fnw(pixx)
            
            # section
            pixywidth = pixy[-1] - pixy[0] + 1
            sectx = (padxleft,round(bb0x-xref),round(bb1x-bb0x),padxright)
            secty = (padylow,halfdy,pixywidth,halfdy,padyup)

            # cut box
            cc0x = round(xref)-padxleft
            cc1x = round(bb1x)+padxright
            cc0y = int(fny(cc0x))-halfdy-padylow
            cc1y = int(fny(cc1x))+halfdy+padyup

            # output 
            tmp[i] = {}
            tmp[i]['XYREF'] = (xref,yref)
            tmp[i]['DLDX'] = (dldx0,dldx1)
            tmp[i]['BBX'] = (bb0x,bb1x)
            tmp[i]['PIXX'] = pixx.copy()
            tmp[i]['PIXY'] = pixy.copy()
            tmp[i]['WW'] = ww.copy()
            tmp[i]['SECTX'] = copy.deepcopy(sectx)
            tmp[i]['SECTY'] = copy.deepcopy(secty)
            tmp[i]['CC'] = (cc0x,cc0y,cc1x,cc1y)

        return copy.deepcopy(tmp)
    ####################
    ####################
    ####################
    def show(self,save=False,savefname='default'):
        fltflist = self.fltflist
        axeflist = self.axeflist
        HEADERALL = self.headerall

        for ii,i in enumerate(fltflist):
            tmp = fits.open(i)
            tmpdata = tmp[1].data.copy()

            tmpheader = HEADERALL[axeflist[ii]]
            xref,yref = tmpheader['XYREF']
            pixx = tmpheader['PIXX']
            pixy = tmpheader['PIXY']
            ww = tmpheader['WW']
            cc0x,cc0y,cc1x,cc1y = tmpheader['CC']
            sectx = tmpheader['SECTX']
            secty = tmpheader['SECTY']

            fig,ax = plt.subplots(2,1,sharex=True)
            fig.tight_layout()
            m = np.where(np.isfinite(tmpdata))
            vmin,vmax = np.percentile(tmpdata[m],5.),np.percentile(tmpdata[m],99.)
            ax[0].imshow(tmpdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
            ax[0].scatter(xref,yref,s=30,facecolor='red',edgecolor='None')
            ax[0].plot(pixx,pixy,'r-')
            ax[0].set_xlim(cc0x,cc1x)
            ax[0].set_ylim(cc0y,cc1y)
            ax[0].set_title('{0}'.format(i.split('/')[-1].split('_')[0]),fontsize=20)
            ax[0].set_ylabel('pixY',fontsize=20)

            bb0x = cc0x+sectx[0]+sectx[1]
            bb1x = bb0x+sectx[2]
            bb0y = cc0y+secty[0]
            bb1y = bb0y+secty[1]+secty[2]+secty[3]
            tmpx = [bb0x,bb1x,bb1x,bb0x,bb0x]
            tmpy = [bb0y,bb0y,bb1y,bb1y,bb0y]
            ax[0].plot(tmpx,tmpy,'r-')

            ax[1].plot(pixx,ww)
            ax[1].set_xlabel('pixX',fontsize=20)
            ax[1].set_ylabel('obs. wavelength (A)',fontsize=20)
            ax[1].grid()
            
            if save:
                if savefname=='default':
                    string = '/'.join(axeflist[ii].split('/')[0:-1])
                    string += '/{0}_axehelperbkg.png'.format(axeflist[ii].split('/')[-1].split('.')[0])
                else:
                    string = savefname
                fig.savefig(string,bbox_inches='tight')
            
    