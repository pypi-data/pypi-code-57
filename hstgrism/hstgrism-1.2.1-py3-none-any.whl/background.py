# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from polynomial2d.polynomial2d import Polynomial2D
import os
import json

class Background:
    def __init__(self,objname='None',gfile='None',tfile='None',extnum=1,
                 padxleft=5,xleft=100,xright=200,padxright=5,
                 padyup=5,halfdy=5,padylow=5,
                 adjustx=0,adjusty=0
                ):
        self.data = {'objname':objname,
                     'gfile':gfile,
                     'tfile':tfile,
                     'extnum':extnum,
                     'ROOTNAME':'None',
                    }
        self.data['ROOTNAME'] = self._rootname()
        self.trace = self._trace()
        self.bbox = {'padxleft':padxleft,'xleft':xleft,'xright':xright,'padxright':padxright,
                     'padyup':padyup,'halfdy':halfdy,'padylow':padylow,
                     'adjustx':adjustx,'adjusty':adjusty,
                     'bbox':None
                     }
        self.bbox['bbox'] = self._bbox()
        self.bkg = self._bkg()
    def _bkg(self):
        tmpdata = fits.open(self.data['gfile'])[self.data['extnum']].data
        bb0x,bb1x = self.bbox['bbox']['BBX']
        bb0y,bb1y = self.bbox['bbox']['BBY']
        xg,yg = self.bbox['bbox']['XG'],self.bbox['bbox']['YG']
        tmpp = tmpdata[bb0y:bb1y,bb0x:bb1x]
        ny,nx = tmpp.shape
        x1 = np.arange(nx)
        x2 = np.arange(ny)
        x1v,x2v = np.meshgrid(x1,x2)
        obj = Polynomial2D(x1v,x2v,tmpp)
        obj.data['MASK'] = self._mask(obj)
        return obj
    def _mask(self,obj):
        tmpmask = np.full_like(obj.data['Y'],False,dtype=bool)
        halfdy = self.bbox['halfdy']
        xgn = (self.bbox['bbox']['XG'] - self.bbox['bbox']['BBX'][0]).astype(int)
        ygn = (self.bbox['bbox']['YG'] - self.bbox['bbox']['BBY'][0]).astype(int)
        for i,ii in enumerate(xgn):
            tmpx,tmpy = int(xgn[i]),int(ygn[i])
            tmpmask[tmpy-halfdy:tmpy+halfdy,tmpx] = True
        return tmpmask
    def _rootname(self):
        tmp = fits.open(self.data['gfile'])[0].header['ROOTNAME']
        return tmp
    def _trace(self):
        tmp = pd.read_csv(self.data['tfile'])
        mdydx = np.isfinite(tmp['DYDX'].values)
        mdldp = np.isfinite(tmp['DLDP'].values)
        tmpp = {'XREF':tmp['XREF'].values[0],
                'YREF':tmp['YREF'].values[0],
                'XG':tmp['XG'].values,
                'YG':tmp['YG'].values,
                'WW':tmp['WW'].values,
                'DYDX':tmp['DYDX'].values[mdydx],
                'DLDP':tmp['DLDP'].values[mdldp]
               }
        return tmpp
    def _bbox(self):
        xref,yref = self.trace['XREF'],self.trace['YREF']
        maxy,miny = self.trace['YG'].max(),self.trace['YG'].min()
        bb0y,bb1y = int(miny-self.bbox['halfdy']-self.bbox['padylow']),int(maxy+self.bbox['halfdy']+self.bbox['padyup'])
        maxx,minx = self.trace['XG'].max(),self.trace['XG'].min()
        bb0x,bb1x = int(minx-self.bbox['padxleft']),int(maxx+self.bbox['padxright'])
        xg = np.arange(bb0x,bb1x)
        xh = xg - int(xref)
        dydx = self.trace['DYDX']
        dldp = self.trace['DLDP']
        yh = np.full_like(xh,0.,dtype=float)
        for i,ii in enumerate(dydx):
            yh += ii * np.power(xh,i)
        yg = yh + yref
        ww = np.full_like(xh,0.,dtype=float)
        for i,ii in enumerate(dldp):
            ww += ii * np.power(xh,i)
        return {'BBX':(bb0x,bb1x),'BBY':(bb0y,bb1y),'XG':xg,'YG':yg,'WW':ww}   
    ##########
    ##########
    ##########
    def saveinfo(self,savefolder='EXTRA'):
        os.system('mkdir {0}'.format(savefolder))
        # save bkg sub
        string = './{1}/{0}'.format(self.data['gfile'].split('/')[-1],savefolder)
        os.system('cp {0} ./{1}/'.format(self.data['gfile'],savefolder))
        tmpp = fits.open(string)
        tmppdata = tmpp[self.data['extnum']].data
        bb0x,bb1x = self.bbox['bbox']['BBX']
        bb0y,bb1y = self.bbox['bbox']['BBY']
        y,yfit = self.bkg.data['Y'],self.bkg.model['YFIT']
        ysub = y-yfit
        tmppdata[bb0y:bb1y,bb0x:bb1x] = ysub.copy()
        tmpp.writeto(string,overwrite=True)
        print('Save {0}'.format(string))
        # save bbox
        tmpp = {}
        for j in self.bbox:
            if j!='bbox':
                tmpp[j] = self.bbox[j]
            elif j=='bbox':
                tmpp['BBX'] = self.bbox[j]['BBX']
                tmpp['BBY'] = self.bbox[j]['BBY']
        tmppp = json.dumps(tmpp)
        string = './{1}/{0}_bbox.json'.format(self.data['ROOTNAME'],savefolder)
        f = open(string,'w')
        f.write(tmppp)
        f.close()
        print('Save {0}'.format(string))
    ##########
    ##########
    ##########
    def show_bkg2dsub(self,
                      save=False,savename_prefix='plot',saveformat='eps',
                      params={'figsize':(30,10),
                              'minmax_y':(10.,99.),
                              'minmax_ysub':(5.,99.),
                              'cmap':'rainbow',
                              'fontsize':12
                             }
                     ):
        figsize = params['figsize']
        minmax_y = params['minmax_y']
        minmax_ysub = params['minmax_ysub']
        cmap = params['cmap']
        fontsize = params['fontsize']
        y,yfit = self.bkg.data['Y'],self.bkg.model['YFIT']
        ysub = y-yfit
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1,3,1)
        vmin,vmax = np.percentile(y,minmax_y[0]),np.percentile(y,minmax_y[1])
        ax.imshow(y,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        ax.set_title(self.data['ROOTNAME'],fontsize=fontsize)
        ax = fig.add_subplot(1,3,2)
        ax.imshow(yfit,origin='lower',cmap=cmap)
        ax.set_title('fit',fontsize=fontsize)
        ax = fig.add_subplot(1,3,3)
        vmin,vmax = np.percentile(ysub,minmax_ysub[0]),np.percentile(ysub,minmax_ysub[1])
        ax.imshow(ysub,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        ax.set_title('sub',fontsize=fontsize)
        fig.tight_layout()               
        if save:
            string = '{0}_bkg2dsub.{1}'.format(savename_prefix,saveformat)
            plt.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
    def show_bkg3d(self,
                   save=False,savename_prefix='plot',saveformat='eps',
                   params={'figsize':(20,10),
                           'cmap':'rainbow',
                           'view_init_y':(90.,-90.),
                           'view_init_mask':(90.,-90.),
                           'fontsize':12
                          }
                  ):
        figsize = params['figsize']
        cmap = params['cmap']
        view_init_y = params['view_init_y']
        view_init_mask = params['view_init_mask']
        fontsize = params['fontsize']
        x1,x2,y,mask = self.bkg.data['X1'],self.bkg.data['X2'],self.bkg.data['Y'],self.bkg.data['MASK']
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1,2,1,projection='3d')
        ax.plot_surface(x1,x2,y,cmap=cmap)
        ax.view_init(*view_init_y)
        ax.set_title(self.data['ROOTNAME'],fontsize=fontsize)
        ax = fig.add_subplot(1,2,2,projection='3d')
        ax.plot_surface(x1,x2,mask,cmap=cmap)
        ax.view_init(*view_init_mask)
        ax.set_title('MASK',fontsize=fontsize)
        fig.tight_layout()               
        if save:
            string = '{0}_bkg3d.{1}'.format(savename_prefix,saveformat)
            plt.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
    def show_bkg2d(self,
                   save=False,savename_prefix='plot',saveformat='eps',
                   params={'figsize':(10,10),
                           'cmap_mask':'Greys',
                           'cmap_y':'viridis',
                           'alpha':0.4,
                           'color':'red',
                           'ls':'-',
                           'lw':2,
                           'fontsize':12
                          }
                  ):
        figsize = params['figsize']
        cmap_mask = params['cmap_mask']
        cmap_y = params['cmap_y']
        alpha = params['alpha']
        color = params['color']
        ls = params['ls']
        lw = params['lw']
        fontsize = params['fontsize']
        plt.figure(figsize=figsize)
        plt.imshow(self.bkg.data['MASK'],origin='lower',cmap=cmap_mask)
        plt.imshow(self.bkg.data['Y'],origin='lower',cmap=cmap_y,alpha=alpha)
        tmpx = self.bbox['bbox']['XG'] - self.bbox['bbox']['BBX'][0]
        tmpy = self.bbox['bbox']['YG'] - self.bbox['bbox']['BBY'][0]
        plt.plot(tmpx,tmpy,color=color,ls=ls,lw=lw)
        root = self.data['ROOTNAME']
        plt.title(root,fontsize=fontsize)
        plt.tight_layout()
        if save:
            string = '{0}_bkg2d.{1}'.format(savename_prefix,saveformat)
            plt.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
    def show_bbox2d(self,
                    save=False,savename_prefix='plot',saveformat='eps',
                    params={'figsize':(10,10),
                            'minmax':(10.,80.),
                            'tickperx':10,
                            'fontsize':12,
                            'rotation':30.,
                            'color':'r',
                            'cmap':'viridis',
                            'lw':2,
                            'ls':':',
                            'marker':'o',
                            'alpha':0.6,
                            'border_x':50,
                            'border_y':50
                           }
                   ):
        tmpdata = fits.open(self.data['gfile'])[self.data['extnum']].data
        minmax = params['minmax']
        cmap = params['cmap']
        figsize = params['figsize']
        color = params['color']
        ls = params['ls']
        lw = params['lw']
        alpha = params['alpha']
        border_x = params['border_x']
        border_y = params['border_y']
        fontsize = params['fontsize']
        tickperx = params['tickperx']
        marker = params['marker']
        rotation = params['rotation']
        vmin,vmax = np.percentile(tmpdata,minmax[0]),np.percentile(tmpdata,minmax[1])
        xg,yg,ww = self.bbox['bbox']['XG'],self.bbox['bbox']['YG'],self.bbox['bbox']['WW']
        bb0x,bb1x = self.bbox['bbox']['BBX']
        bb0y,bb1y = self.bbox['bbox']['BBY']
        plt.figure(figsize=figsize)
        plt.imshow(tmpdata,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax)
        plt.plot(xg,yg,color=color,ls=ls,lw=lw,alpha=alpha)
        for i,ii in enumerate(xg):
            if (i in {0,len(xg)-1}) or (np.mod(i,tickperx)==0):
                label = '{0}A'.format(int(ww[i]))
                plt.plot(xg[i],yg[i],color=color,marker=marker)
                plt.annotate(label,(xg[i],yg[i]),
                             textcoords='offset points',
                             xytext=(0,10),
                             ha='center',
                             fontsize=fontsize,
                             rotation=rotation,
                             color=color
                            )
        plt.plot([bb0x,bb1x,bb1x,bb0x,bb0x],[bb0y,bb0y,bb1y,bb1y,bb0y],color=color,ls='-')
        plt.xlim(bb0x-border_x,bb1x+border_x)
        plt.ylim(bb0y-border_y,bb1y+border_y)
        plt.title(self.data['ROOTNAME'],fontsize=fontsize) 
        plt.tight_layout()
        if save:
            string = '{0}_bbox2d.{1}'.format(savename_prefix,saveformat)
            plt.savefig(string,format=saveformat,bbox_inches='tight')
            print('Save {0}'.format(string))
            
            