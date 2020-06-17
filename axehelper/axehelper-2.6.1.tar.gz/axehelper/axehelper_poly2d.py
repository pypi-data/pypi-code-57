# Kornpob Bhirombhakdi

import numpy as np
import matplotlib.pyplot as plt
import copy,glob,os
from astropy.io import fits
from polynomial2d.polynomial2d import Polynomial2D
from math import pi

class AXEhelper_POLY2D:
    def __init__(self,axehelperbkg):
        self.axehelperbkg = axehelperbkg
        self.obj = self._obj()
    ####################
    ####################
    ####################
    def saveflt(self,savepath='./EXTRA/'):
        self._check(savepath)
        fltflist = self.axehelperbkg.fltflist
        axeflist = self.axehelperbkg.axeflist
        OBJ = self.obj
        HEADERALL = self.axehelperbkg.headerall
        for ii,i in enumerate(fltflist):
            root = i.split('/')[-1].split('_')[0]
            string = '{0}_flt.fits'.format(root)
            string = savepath+string
            string2 = '{0}_bkg.fits'.format(root)
            string2 = savepath+string2
    
            os.system('cp {0} {1}'.format(i,string))
            os.system('cp {0} {1}'.format(i,string2))

            obj = OBJ[i]

            tmpheader = HEADERALL[axeflist[ii]]
            xref,yref = tmpheader['XYREF']
            pixx = tmpheader['PIXX']
            pixy = tmpheader['PIXY']
            ww = tmpheader['WW']
            cc0x,cc0y,cc1x,cc1y = tmpheader['CC']
            sectx = tmpheader['SECTX']
            secty = tmpheader['SECTY']

            tmp = fits.open(string)
            tmp[1].data[cc0y:cc1y,cc0x:cc1x] = obj.model['YSUB'].copy()
            tmp.writeto(string,overwrite=True)
            tmp.close()

            tmp = fits.open(string2)
            tmp[1].data[cc0y:cc1y,cc0x:cc1x] = obj.model['YFIT'].copy()
            tmp.writeto(string2,overwrite=True)
            tmp.close()
    def _check(self,savepath):
        try:
            os.mkdir(savepath)
        except:
            try:
                cwd = os.getcwd()
                os.chdir(savepath)
                os.chdir(cwd)
            except:
                raise ValueError('cannot mkdir {0}'.format(savepath))        
    ####################
    ####################
    ####################
    def fit(self,norder=4):
        OBJ = self.obj
        for ii,i in enumerate(OBJ):
            obj = OBJ[i]
            obj.model['NORDER'] = norder
            obj.fit()
            obj.compute()

            obj.model['YSUB'] = obj.data['Y'] - obj.model['YFIT']
            obj.model['YSUB_MASK'] = obj.model['YSUB'] * obj.data['MASKOBJ'].astype(int)
            obj.model['SUM'] = obj.model['YSUB_MASK'].sum(axis=0)

            OBJ[i] = copy.deepcopy(obj)   
        self.obj = OBJ
    ####################
    ####################
    ####################  
    def _obj(self):
        OBJ = {}
        axehelperbkg = self.axehelperbkg
        fltflist = axehelperbkg.fltflist
        axeflist = axehelperbkg.axeflist
        HEADERALL = axehelperbkg.headerall
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
        
            # MASKOBJ
            tmp = np.full_like(obj.data['MASK'],False,dtype=bool)
            bb0x = sectx[0]+sectx[1]
            bb1x = bb0x+sectx[2]
            bb0y = secty[0]
            bb1y = bb0y+secty[1]+secty[2]+secty[3]   
            tmp[bb0y:bb1y,bb0x:bb1x] = True
            obj.data['MASKOBJ'] = tmp.copy()
            
            # MASKFIT
            obj.model['MASKFIT'] = obj.data['MASKOBJ'] | obj.data['MASK']

            # output
            OBJ[i] = copy.deepcopy(obj)
        return OBJ     
    ####################
    ####################
    ####################
    def show2d(self,save=False,savefname='default'):
        OBJ = self.obj
        axeflist = self.axehelperbkg.axeflist
        HEADERALL = self.axehelperbkg.headerall
        for ii,i in enumerate(OBJ):
            obj = OBJ[i]
            tmpdata = obj.data['Y']
            tmpmask = obj.data['MASK']
            tmpheader = HEADERALL[axeflist[ii]]
            xref,yref = tmpheader['XYREF']
            pixx = tmpheader['PIXX']
            pixy = tmpheader['PIXY']
            ww = tmpheader['WW']
            cc0x,cc0y,cc1x,cc1y = tmpheader['CC']
            sectx = tmpheader['SECTX']
            secty = tmpheader['SECTY']

            # shift due to the cut
            tmpxref = xref - cc0x
            tmpyref = yref - cc0y
            tmppixx = pixx - cc0x
            tmppixy = pixy - cc0y

            fig,ax = plt.subplots(2,1,sharex=True)
            m = np.where(np.isfinite(tmpdata))
            vmin,vmax = np.percentile(tmpdata[m],5.),np.percentile(tmpdata[m],99.)
            ax[0].imshow(tmpdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
            ax[0].scatter(tmpxref,tmpyref,s=30,facecolor='red',edgecolor='None')
            ax[0].plot(tmppixx,tmppixy,'r-')
            ax[0].set_title('{0}'.format(i.split('/')[-1].split('_')[0]),fontsize=20)
            ax[0].set_ylabel('pixY + {0}'.format(cc0y),fontsize=20)

            bb0x = sectx[0]+sectx[1]
            bb1x = bb0x+sectx[2]
            bb0y = secty[0]
            bb1y = bb0y+secty[1]+secty[2]+secty[3]
            tmpx = [bb0x,bb1x,bb1x,bb0x,bb0x]
            tmpy = [bb0y,bb0y,bb1y,bb1y,bb0y]
            ax[0].plot(tmpx,tmpy,'r-')

            ax[1].plot(tmppixx,ww)
            ax[1].set_xlabel('pixX + {0}'.format(cc0x),fontsize=20)
            ax[1].set_ylabel('obs. wavelength (A)',fontsize=20)
            ax[1].grid()
            
            if save:
                if savefname=='default':
                    string = '/'.join(axeflist[ii].split('/')[0:-1])
                    string += '/{0}_axehelperpoly2dshow2d.png'.format(axeflist[ii].split('/')[-1].split('.')[0])
                else:
                    string = savefname
                fig.savefig(string,bbox_inches='tight')
    ####################
    ####################
    ####################
    def show3d(self,save=False,savefname='default'):
        OBJ = self.obj
        axeflist = self.axehelperbkg.axeflist
        for ii,i in enumerate(OBJ):
            obj = OBJ[i]
            string = i

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection='3d')
            tmp = copy.deepcopy(obj.data)
            ax.plot_surface(tmp['X1'],tmp['X2'],tmp['Y'],
                            cmap='rainbow',
                            alpha=0.6
                           )
            ax.set_xlabel('X1')
            ax.set_ylabel('X2')
            ax.set_zlabel('Y')
            ax.view_init(45,-45)
            ax.set_zlim(0.,5.)
            ax.set_title('{0}'.format(string.split('/')[-1].split('_')[0]),fontsize=20)
            
            if save:
                if savefname=='default':
                    string = '/'.join(axeflist[ii].split('/')[0:-1])
                    string += '/{0}_axehelperpoly2dshow3d.png'.format(axeflist[ii].split('/')[-1].split('.')[0])
                else:
                    string = savefname
                fig.savefig(string,bbox_inches='tight')
    ####################
    ####################
    ####################
    def showmask(self,save=False,savefname='default'):
        OBJ = self.obj
        axeflist = self.axehelperbkg.axeflist
        for ii,i in enumerate(OBJ):
            obj = OBJ[i]

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection='3d')
            tmp = copy.deepcopy(obj.data)
            ax.plot_surface(tmp['X1'],tmp['X2'],obj.data['MASKOBJ'].astype(int),
                            cmap='viridis'
                           )
            ax.set_xlabel('X1')
            ax.set_ylabel('X2')
            ax.set_zlabel('MASKOBJ = 1')
            ax.view_init(45,-45)
            ax.set_title('{0}'.format(i.split('/')[-1].split('_')[0]),fontsize=20)

            plt.figure(figsize=(10,10))
            tmp = obj.data['Y']*obj.data['MASKOBJ'].astype(int)
            m = np.where(np.isfinite(tmp))
            vmin,vmax = np.percentile(tmp[m],5.),np.percentile(tmp[m],99.)
            plt.imshow(obj.data['Y']*obj.data['MASKOBJ'].astype(int),
                       cmap='Greys',origin='lower',vmin=vmin,vmax=vmax
                      )

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection='3d')
            tmp = copy.deepcopy(obj.data)
            ax.plot_surface(tmp['X1'],tmp['X2'],obj.model['MASKFIT'].astype(int),
                            cmap='viridis'
                           )
            ax.set_xlabel('X1')
            ax.set_ylabel('X2')
            ax.set_zlabel('MASKFIT = 1')
            ax.view_init(45,-45)
            
            if save:
                if savefname=='default':
                    string = '/'.join(axeflist[ii].split('/')[0:-1])
                    string += '/{0}_axehelperpoly2dshowmask.png'.format(axeflist[ii].split('/')[-1].split('.')[0])
                else:
                    string = savefname
                fig.savefig(string,bbox_inches='tight')
    ####################
    ####################
    ####################
    def show3dfit(self,save=False,savefname='default'):
        OBJ = self.obj
        axeflist = self.axehelperbkg.axeflist
        for ii,i in enumerate(OBJ):
            obj = OBJ[i]
            tmp = obj.data.copy()

            fig = plt.figure()

            ax = fig.add_subplot(1,2,1,projection='3d')
            ax.plot_surface(tmp['X1'],tmp['X2'],obj.model['YFIT'],
                            cmap='Greys',
                            alpha=1.
                           )
            ax.plot_surface(tmp['X1'],tmp['X2'],tmp['Y'],
                            cmap='viridis',
                            alpha=0.6
                           )
            ax.set_xlabel('X1')
            ax.set_ylabel('X2')
            ax.set_zlabel('YFIT')
            ax.view_init(45,-45)
            ax.set_zlim(0.,5.)
            ax.set_title('{0}'.format(i.split('/')[-1].split('_')[0]),fontsize=20)


            ax = fig.add_subplot(1,2,2,projection='3d')
            tmp = obj.data.copy()
            ax.plot_surface(tmp['X1'],tmp['X2'],tmp['Y'] - obj.model['YFIT'],
                            cmap='rainbow'
                           )
            ax.set_xlabel('X1')
            ax.set_ylabel('X2')
            ax.set_zlabel('Y - YFIT')
            ax.view_init(45,-45)
            ax.set_zlim(0.,5.)
            
            if save:
                if savefname=='default':
                    string = '/'.join(axeflist[ii].split('/')[0:-1])
                    string += '/{0}_axehelperpoly2dshow3dfit.png'.format(axeflist[ii].split('/')[-1].split('.')[0])
                else:
                    string = savefname
                fig.savefig(string,bbox_inches='tight')    
    ####################
    ####################
    ####################
    def showsum(self,save=False,savefname='default'):
        # https://pythonmatplotlibtips.blogspot.com/2018/01/add-second-x-axis-at-top-of-figure-python-matplotlib-pyplot.html
        OBJ = self.obj
        HEADERALL = self.axehelperbkg.headerall
        axeflist = self.axehelperbkg.axeflist
        for ii,i in enumerate(OBJ):
            obj = OBJ[i]
            tmpdata = obj.data['Y']
            tmpmask = obj.data['MASK']
            tmpheader = HEADERALL[axeflist[ii]]
            xref,yref = tmpheader['XYREF']
            pixx = tmpheader['PIXX']
            pixy = tmpheader['PIXY']
            ww = tmpheader['WW']
            cc0x,cc0y,cc1x,cc1y = tmpheader['CC']
            sectx = tmpheader['SECTX']
            secty = tmpheader['SECTY']

            plt.figure(figsize=(10,10))

            ax1 = plt.subplot(2,1,1)
            ax1.imshow(obj.model['YSUB'],cmap='Greys',origin='lower',
                       vmin=-1,vmax=1
                      )

            bb0x = sectx[0]+sectx[1]
            bb1x = bb0x+sectx[2]
            bb0y = secty[0]
            bb1y = bb0y+secty[1]+secty[2]+secty[3]
            tmpx = [bb0x,bb1x,bb1x,bb0x,bb0x]
            tmpy = [bb0y,bb0y,bb1y,bb1y,bb0y]
            ax1.plot(tmpx,tmpy,'r-',alpha=0.6)
            ax1.set_frame_on(False)
            ax1.set_title(i.split('/')[-1].split('_')[0],fontsize=20)

            ax2 = plt.subplot(2,1,2,sharex=ax1)
            tmpx = np.arange(0,obj.model['SUM'].shape[0])
            ax2.plot(tmpx,obj.model['SUM'])
            ax2.set_ylabel('SUM',fontsize=20)
            ax2.set_frame_on(False)
            ax2.grid()

            numtick = 10
            ax22 = ax2.twiny()
            ax22.set_frame_on(False)
            tmpp = ww
            tmp = tmpp.astype(int).copy()
            newlabel = np.linspace(tmp[0],tmp[-1],numtick).astype(int)
            newpos = np.linspace(tmpx[0],tmpx[-1],numtick)
            ax22.set_xticks(newpos)
            ax22.set_xticklabels(newlabel)
            ax22.set_xlabel('obs. wavelength (A)',fontsize=15)
            ax22.set_xlim(ax2.get_xlim())

            if save:
                if savefname=='default':
                    string = '/'.join(axeflist[ii].split('/')[0:-1])
                    string += '/{0}_axehelperpoly2dshowsum.png'.format(axeflist[ii].split('/')[-1].split('.')[0])
                else:
                    string = savefname
                plt.savefig(string,bbox_inches='tight')    
