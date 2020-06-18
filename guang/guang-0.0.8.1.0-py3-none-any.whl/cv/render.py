import cv2
import numpy as np
import matplotlib.pyplot as plt
from vispy.color import (get_colormap, get_colormaps, Colormap)


class Render:
    ''' pass '''
    def __init__(self):
        pass
#         self.load = False

    def load_brush(self, brush):
        '''
            brush: 4 channel array
        '''
        self.B, self.G, self.R, self.A = cv2.split(brush)
        self.a_trans = self.A

    def load_A_channel(self, A):
        self.A = A
        self.a_trans = self.A

    def show_img(self):

        plt.imshow(cv2.merge((self.R, self.G, self.B)))
        plt.show()

    def emboss(self, img, intensity):
        '''input: 
        	img: 4D BGRA
        	The intensity of emboss
        '''
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        (H, L, S) = cv2.split(cv2.cvtColor(img, cv2.COLOR_RGB2HLS))

        # Normalisation：For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255].
        H, L, S = H / 179., L / 255., S / 255.
        H, L, S = H, L, S
        # Apply the convolution kernel to channel L：
        p, q, s, t = 0., 0., intensity, 0.
        # p,q,s control the intensity of the relief in three directions
        # The value of matrix center controls the overall brightness, here sets 1.0
        kernel = np.array([[-q, -s, t], [-p, 1.0, p], [-t, s, q]],
                          dtype=np.float32)
        #         kernel = np.array([[ 0, -1,-2],
        #                            [ 1, 0, -1],
        #                            [ 2,  1, 0]], dtype=np.float32)

        L = cv2.filter2D(L, -1, kernel)
        L = np.clip(L, 0, 1)
        H, L, S = H * 179., L * 255., S * 255.

        H, L, S = H.astype('uint8'), L.astype('uint8'), S.astype('uint8')
        #-------------------------------------------------------------------
        # If in the previous step makes the brightness too large, please re-limit the brightness here
        # H,L,S = H, Gamma_trans(L, 255, 1.2), Gamma_trans(S, 255, 1)
        # H,L,S = H, MaxMinNormal(L, 1, 150), MaxMinNormal(S, 0,255)
        #-------------------------------------------------------------------
        # Merge each channel
        res = cv2.merge((H, L, S))
        res = cv2.cvtColor(res, cv2.COLOR_HLS2RGB)
        return cv2.cvtColor(res, cv2.COLOR_RGB2BGRA)

    @classmethod
    def colorMapInterp(cls, colors, N):
        '''
        colors: a list of RGB color array/list/tuple
                For example: colors = ([1,0,0],[0,1,0],...) 
                or colors = ('r','g') 
        N: number of interpolation 
        return: rgb interpolation array. type: float [0,1]
        '''
        rm = Colormap(colors)
        rgb_interp = rm[np.linspace(0, 1, N)].rgb  #* 255
        # show colors
        # plt.imshow(rgb_interp.reshape(1,N,3).astype('uint8'))
        # plt.axis('off')
        return rgb_interp  # float [0,1]

    @classmethod
    def ramp(cls, c1, c2, c3, c4, h0=None, w0=None):
        '''
        input:
            c: Color of four vertices
        return:
            2D color bgr map array. type: float [0,1]
        '''
        if h0 == None:
            h0, w0 = cls.A.shape
        # scale = 20
        # h, w =  h0//scale+1, w0//scale+1 # h, w can be replace others and then we interpolate the output image
        h, w = 20, 20
        rec1 = cls.colorMapInterp((c1, c2), h)

        rec3 = cls.colorMapInterp((c3, c4), h)

        color_mat = np.zeros((h, w, 3))
        for i in range(h):
            color_mat[i, :, :] = cls.colorMapInterp(
                (rec1[i, :], rec3[h - i - 1, :]), w)
        # show it
        # plt.imshow(color_mat)
        color_mat[:, :, [0, 2]] = color_mat[:, :, [2, 0]]  # rgb -> bgr

        return cv2.resize(color_mat, (w0, h0))  # float [0,1]

    @staticmethod
    def get_random_color(bgr, sigma):
        '''
        rgb: [b, g, r] float value
        sigma: [sigma_b, sigma_g, sigma_r] float range
        return rgb color
        '''
        #         color = [np.random.normal(bgr[2], sigma[0]), np.random.normal(bgr[1], sigma[1]), np.random.normal(bgr[0], sigma[2])]
        color = [
            bgr[2] + sigma[0] * (np.random.rand() - 1 / 2),
            bgr[1] + sigma[1] * np.random.rand(),
            bgr[0] * sigma[2] + np.random.rand()
        ]
        return np.clip(color, 0, 1)

    @classmethod
    def gen_colormap(cls, h, w, c1, sigma=[0.5, 0.5, 0.1]):
        '''
        c1: [b, g, r] float value
        sigma: [sigma_r, sigma_g, sigma_b] float range
        '''
        c2 = Render.get_random_color(c1, sigma)
        c3 = Render.get_random_color(c1, sigma)
        c4 = Render.get_random_color(c1, sigma)
        color = Render.ramp(c1, c2, c3, c4, h, w)
        return color

    def get_fore_back(self, canvas, brush):
        '''
        Get foreground and background of canvas and brush
        '''
        # brush = cv2.bilateralFilter(brush,15, 35,35)
        H, W = canvas.shape[:2]  # canvas shape
        h_brush, w_brush = brush.shape[:2]

        h_coef = h_brush / w_brush  # keep the same shape of brush
        scale = 0.4  # scale coefficient for roi
        h, w = int(H * h_coef * scale), int(W * scale)  # roi shape
        # Attention! cv2.resize(img, (w,h)) NOT (h, w)
        brush = cv2.resize(brush, (w, h), interpolation=cv2.INTER_AREA)
        #         plt.figure(figsize=(12,12))
        #         plt.subplot(231)
        #         plt.imshow(cv2.cvtColor(brush, cv2.COLOR_BGR2RGB)); plt.title('brush(padding)')
        # padding
        brush = cv2.copyMakeBorder(brush,
                                   int(np.ceil((H - h) / 2)),
                                   int(np.floor((H - h) / 2)),
                                   int(np.ceil((W - w) / 2)),
                                   int(np.floor((W - w) / 2)),
                                   cv2.BORDER_CONSTANT,
                                   value=[255, 255, 255])
        #         print(canvas.shape, brush.shape)
        #         plt.figure(figsize=(12,12))
        #         plt.subplot(231)
        #         plt.imshow(cv2.cvtColor(brush, cv2.COLOR_BGR2RGB)); plt.title('brush(padding)')

        brush = cv2.bilateralFilter(
            brush, 15, 35,
            35)  # this step can be delete if input image is 'clean'.
        brushgray = cv2.cvtColor(brush, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(
            brushgray, 250, 255,
            cv2.THRESH_BINARY)  #ret is thresh（250）mask is Binary image

        mask_inv = cv2.bitwise_not(mask)
        #plt.subplot(232);plt.imshow(mask);plt.title('mask')
        #plt.subplot(233);plt.imshow(mask_inv);plt.title('mask_inv')

        canvas_bg = cv2.bitwise_and(
            canvas, brush,
            mask=mask)  # 将mask去掉，可以看出 _and操作是取数值更低（更黑）的元素,而mask是将mask对应元素置于0
        brush_bg = cv2.bitwise_and(canvas, canvas, mask=mask_inv)
        #plt.subplot(234);plt.imshow(cv2.cvtColor(canvas_bg, cv2.COLOR_BGR2RGB));plt.title('canvas_brush_mask_and')
        #plt.subplot(235);plt.imshow(cv2.cvtColor(brush_bg, cv2.COLOR_BGR2RGB));plt.title('brush_brush_mask_inv_and')

        brush_fg = cv2.bitwise_and(brush, brush, mask=mask_inv)
        #plt.subplot(236);plt.imshow(cv2.cvtColor(brush_fg, cv2.COLOR_BGR2RGB));plt.title('brush_fg')

        return canvas_bg, brush_bg, brush_fg  # dtype: uint8

    def rotate_origin_img(self, img, theta):
        '''
        theta: Counterclockwise Angle
        This function is going to rotate and pad the image to the right size
        '''
        h_origin, w_origin = img.shape[:2]

        # padding
        size = int(np.ceil(np.sqrt(w_origin**2 + h_origin**2)))
        top = int(np.ceil((size - h_origin) / 2))
        bottom = int(np.ceil((size - h_origin) / 2))
        left = int(np.ceil((size - w_origin) / 2))
        right = int(np.ceil((size - w_origin) / 2))
        padding_img = cv2.copyMakeBorder(img,
                                         top,
                                         bottom,
                                         left,
                                         right,
                                         cv2.BORDER_CONSTANT,
                                         value=[0, 0, 0])

        rotate_origin = ((size - 1) / 2, (size - 1) / 2)
        M = cv2.getRotationMatrix2D(rotate_origin, theta, 1)
        rotated_img = cv2.warpAffine(padding_img,
                                     M, (size, size),
                                     flags=cv2.INTER_LANCZOS4)

        assert rotated_img.dtype == 'uint8'
        return rotated_img, dict([('h_origin', h_origin),
                                  ('w_origin', w_origin), ('theta', theta),
                                  ('top', top), ('bottom', bottom),
                                  ('left', left), ('right', right),
                                  ('rotate_origin', rotate_origin)])

    def inv_rotate_padding_img(self, padding_img, dic):

        h, w = padding_img.shape[:2]
        M_inv = cv2.getRotationMatrix2D(dic['rotate_origin'], -dic['theta'], 1)
        inv_rot_padding_img = cv2.warpAffine(padding_img,
                                             M_inv, (h, w),
                                             flags=cv2.INTER_LANCZOS4)

        # clip
        inv_rot_img = inv_rot_padding_img[dic['top'] - 1:-dic['bottom'],
                                          dic['left'] - 1:-dic['right'],
                                          ]  # if dimension>2, add ':'

        inv_rot_img = cv2.resize(inv_rot_img,
                                 (dic['w_origin'], dic['h_origin']),
                                 interpolation=cv2.INTER_LANCZOS4)

        assert inv_rot_img.shape[:2] == (dic['h_origin'], dic['w_origin'])
        assert inv_rot_img.dtype == 'uint8'
        return inv_rot_img

    def transp_mat(self, size, alpha_min, alpha_max, rate):
        '''
        Args:
            size: rotated image shape
        give the transparent matrix.
        '''
        N = 50
        mat = np.ones((N, N))
        x = np.linspace(1 - alpha_max, 1 - alpha_min, N)
        alpha = ((1 - utils.Gamma_trans(x, rate)) * (alpha_max - alpha_min) +
                 alpha_min)
        for i in range(N):
            mat[i, :] = alpha[i] * mat[i, :]
        mat = cv2.resize(mat, (size))
        return mat

    def transparency_rotate(self, theta=0, alpha_min=0.3, alpha_max=1, rate=1):
        '''
        Apply transparency to channel A.
        Args
            a: channel A
            
        '''
        a = self.A
        a, coord_dic = self.rotate_origin_img(a, theta)
        a_trans = a * self.transp_mat(a.shape, alpha_min, alpha_max, rate)
        a_trans = self.inv_rotate_padding_img(a_trans.astype('uint8'),
                                              coord_dic)
        self.a_trans = a_trans

    def transparency_love(self, love_mat):
        h, w = self.A.shape
        love_mat = cv2.resize(love_mat, (w, h)) * 255
        self.a_trans = love_mat.astype('uint8')

    def overlay_with_transparency(self, bgimg, xmin=0, ymin=0):
        '''
        bgimg: a 4 channel image, use as background
        xmin, ymin: a corrdinate in bgimg. from where the fgimg will be put
        trans_percent: transparency of fgimg. [0.0,1.0]
        '''
        trans_percent = 1
        fgimg = cv2.merge((self.B, self.G, self.R, self.a_trans))

        #create roi and black mask
        roi = bgimg[ymin:ymin + fgimg.shape[0], xmin:xmin + fgimg.shape[1]]
        roi_black = np.zeros(fgimg.shape).astype(bgimg.dtype)

        #convert alpha to [0,1] and reshape it so that we can to math operation later
        alpha = np.expand_dims((self.a_trans.astype('float32') / 255.),
                               axis=-1)
        alpha_inv = 1. - alpha

        roi_bg_black = (roi * alpha_inv).astype(bgimg.dtype)
        roi_bg_trans = cv2.addWeighted(roi, 1 - trans_percent, roi_bg_black,
                                       trans_percent, 0)

        fg_black = (fgimg * alpha).astype(fgimg.dtype)
        fg_trans = cv2.addWeighted(roi_black, 1 - trans_percent, fg_black,
                                   trans_percent, 0)

        result = bgimg.copy()
        result[ymin:ymin + fgimg.shape[0],
               xmin:xmin + fgimg.shape[1]] = cv2.add(fg_trans, roi_bg_trans)

        return result
# -------------------------------------------------------------

    def over_layer(self, img1, img2, transp1=1, transp2=1):
        '''
        input: float bgra
            img1: foreground   img2: background
            transp1: foreground transparency
        output: float bgra
        '''
        b1, g1, r1, alpha1 = cv2.split(img1)
        b2, g2, r2, alpha2 = cv2.split(img2)
        # ----------
        alpha1 = transp1 * alpha1
        alpha2 = transp2 * alpha2
        # ----------
        alpha = alpha1 + alpha2 * (1 - alpha1)
        alpha = np.clip(alpha, 0, 1)

        def outRGB(c1, c2):
            c1[alpha == 0] = np.nan
            c2[alpha == 0] = np.nan
            c = (c1 * alpha1 + c2 * alpha2 * (1 - alpha1)) / alpha
            return np.nan_to_num(c)

        b = outRGB(b1, b2)
        g = outRGB(g1, g2)
        r = outRGB(r1, r2)
        b, g, r = np.clip(b, 0, 1), np.clip(g, 0, 1), np.clip(r, 0, 1)
        # b,g,r,alpha = utils.append1D(b,g,r,alpha)
        # bgra = np.concatenate([b,g,r,alpha], axis=2)
        bgra = cv2.merge([b, g, r, alpha])
        return bgra

    def overlay(self,
                img1,
                img2,
                xmin=0,
                ymin=0,
                transp_brush=1,
                transp_canvas=1):
        '''input: 
                float img1: foreground  img2: background
           return: float overlay
        '''
        roi = img2[ymin:ymin + img1.shape[0], xmin:xmin + img1.shape[1]]
        roi = self.over_layer(img1,
                              roi,
                              transp1=transp_brush,
                              transp2=transp_canvas)
        img2[ymin:ymin + img1.shape[0], xmin:xmin + img1.shape[1]] = roi
        return img2


# -------------------------------------------------------------

    @staticmethod
    def zeroAlpha2zeroRGB(img):  # this is not used
        '''
        input: 
            img: bgra 4d array, float
        return: bgra 4d array, float
        '''
        b, g, r, a = cv2.split(img)
        r[a == 0] = 0
        g[a == 0] = 0
        b[a == 0] = 0

        r, g, b, a = utils.append1D(r, g, b, a)
        return np.concatenate([b, g, r, a], axis=2)


class utils:
    @staticmethod
    def append1D(*array_list):
        ''' For exemple: 
                before: array.shape (5,2)
                after: array.shape  (5,2,1)
            '''
        out = []
        for array in array_list:
            out.append(array.reshape(array.shape + (1, )))
        if len(out) == 1:
            return out[0]
        else:
            return [i for i in out]

    @staticmethod
    def myplot(img, channel='bgr', figsize=6):
        ''' can show image channel(float/uint8) BGR,BGRA,HLS,HSV.
        if RGB, set channel = 0'''
        def cvt2rgb(img, channel='bgr'):
            '''it can convert image channel BGR,BGRA,HLS,HSV to RGB'''
            if channel == 'bgr' or channel == 'BGR':
                print('bgr', img.shape)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            elif channel == 'bgra' or channel == 'BGRA':
                print('bgra', img.shape)
                #                 b,g,r,a = cv2.split(img)
                #                 r,g,b,a = utils.append1D(r,g,b,a)
                #                 img = np.concatenate([r,g,b,a], axis=2)
                #                 img = np.c_[rgb, np.reshape(img[:,:,-1],rgb.shape[:2] +(1,))]
                img[:, :, [2, 0]] = img[:, :, [0, 2]]
            elif channel == 'HLS' or channel == 'hls':
                img = cv2.cvtColor(img, cv2.COLOR_HLS2RGB)
                print('hls', img.shape)
            elif channel == 'HSV' or channel == 'hsv':
                img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
                print('hsv', img.shape)
            else:
                return img
            return img

        if img.dtype == np.float or img.dtype == np.float32:
            img = np.uint8(img * 255)
        if channel:
            img = cvt2rgb(img, channel)
        plt.figure(figsize=(figsize, figsize))
        plt.imshow(img)
        plt.show()

    @staticmethod
    def Gamma_trans(I, gamma):
        '''
        param:
            gamma: if your intersted region is too bright, set gamma > 1 decreasing contrast.
               and if your intersted region is too dark, set 1> gamma > 0 to increase contrast.
            I_max: is the maximun of the channel of I.
        return:
            the map of I
        '''
        I_max = I.max()
        fI = I / I_max
        out = np.power(fI, gamma)
        out = out * I_max
        return out


if __name__ == '__main__':

    def test_overlay():
        canvas = cv2.imread('pic/brush_blue.png', -1)
        brush = cv2.imread('pic/pika_roi.png', -1)
        render = Render()
        canvas_ = render.overlay(brush / 255,
                                 canvas / 255,
                                 xmin=0,
                                 ymin=0,
                                 transp_brush=0.7)
        utils.myplot(canvas_, 'bgra')

    test_overlay()

    def test_ramp():
        render = Render()
        res = render.ramp('r', 'g', 'b', 'g')

    # =================================================================
#     render.load_brush(brush)
#     render.transparency_rotate(theta=0, alpha_min=0.2, alpha_max=0.99,rate=2)

#     res = render.overlay_with_transparency(canvas)
#     plt.imshow(cv2.cvtColor(res,cv2.COLOR_BGRA2RGB));plt.show()
#     res = render.emboss(res, 1)
#     plt.imshow(cv2.cvtColor(res,cv2.COLOR_BGRA2RGB));plt.show()
# =================================================================
