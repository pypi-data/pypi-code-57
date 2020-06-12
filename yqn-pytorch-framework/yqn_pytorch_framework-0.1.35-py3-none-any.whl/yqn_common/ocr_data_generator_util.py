import pathlib
import os
import numpy as np
import cv2
import glob
def origin_text_coordiction_map(origin_text,scale):
    '''
    从pdf解析的在pdf上的坐标，映射到图片上的坐标
    :param origin_text:dict
    :param scale: float
    :return: dict
    '''
    maped_origin_text=origin_text.copy()
    text_infos=origin_text["text_infos"]
    maped_text_infos=[]
    for text_info in text_infos:
        maped_text_info={}
        maped_text_rectangle={}
        text_rectangle=text_info["text_rectangle"]
        text=text_info["text"]
        llx=text_rectangle["llx"]
        lly=text_rectangle["lly"]
        urx=text_rectangle["urx"]
        ury=text_rectangle["ury"]
        maped_llx=int(llx*scale)
        maped_lly=int(lly*scale)
        maped_urx=int(urx*scale)
        maped_ury=int(ury*scale)
        maped_text_rectangle["llx"]=maped_llx
        maped_text_rectangle["lly"]=maped_lly
        maped_text_rectangle["urx"]=maped_urx
        maped_text_rectangle["ury"]=maped_ury
        maped_text_info["text"]=text
        maped_text_info["text_rectangle"]=maped_text_rectangle
        maped_text_infos.append(maped_text_info)
    maped_origin_text["text_infos"]=maped_text_infos
    return maped_origin_text

def coordition_four_map_eight(text_rectangle):
    '''
    从4坐标映射到8坐标
    :param text_rectangle:
    :return: []
    '''
    llx=text_rectangle["llx"]
    lly=text_rectangle["lly"]
    urx=text_rectangle["urx"]
    ury=text_rectangle["ury"]
    x1,y1=llx,lly
    x2,y2=urx,lly
    x3,y3=urx,ury
    x4,y4=llx,ury
    return [x1,y1,x2,y2,x3,y3,x4,y4]
def generator_data_from_origin_text(origin_text,scale,file_name,page_num,save_dir="/data-hdd/LingYue/ocr_data/txt"):
    '''
    从pdf解析结果 生成ocr训练数据
    :param origin_text:
    :return:
    '''
    origin_text=origin_text_coordiction_map(origin_text,scale)
    text_infos=origin_text["text_infos"]
    write_file_path=os.path.join(save_dir,file_name+"_"+str(page_num)+".txt")
    if os.path.exists(write_file_path):
        os.remove(write_file_path)
    with open(write_file_path,mode="a+",encoding="utf-8") as f:
        for text_info in text_infos:
            text=text_info["text"]
            text_rectangle=text_info["text_rectangle"]
            text_rectangle=coordition_four_map_eight(text_rectangle)
            text_rectangle=np.array(text_rectangle).astype(str)
            in_file_text=",".join(text_rectangle)+","+text
            f.write(in_file_text)
            f.write("\n")
def draw_rect_to_img(origin_text_path,img_path,save_dir="/data-hdd/LingYue/ocr_data"):
    d=pathlib.Path(origin_text_path)
    file_name=d.stem
    bboxes=[]
    texts=[]
    with open(origin_text_path,encoding="utf-8") as f:
        lines=f.readlines()
        for line in lines:
            if len(line)>0:
                splited_line=line.split(",")
                if len(splited_line)>0:
                    box=list(map(int,splited_line[:8]))
                    bboxes.append(box)
                    text=str(splited_line[8])
                    texts.append(text)
    img=cv2.imread(img_path)
    real_write_file_path=os.path.join(save_dir,"img",file_name+".jpg")
    cv2.imwrite(real_write_file_path,img)
    for box in bboxes:
        box=np.reshape(box,(4,2))
        cv2.drawContours(img, [box],-1, (255, 0, 0), 2)
    bboxes_write_file_path=os.path.join(save_dir,"mask",file_name+"_result.jpg")
    print(file_name)
    cv2.imwrite(bboxes_write_file_path,img)


def analysis_bbox_to_img(ocr_text_dir):
    for path in glob.glob(os.path.join(ocr_text_dir,"*.txt"),recursive=True):
        d=pathlib.Path(path)
        file_name=d.stem
        splited_file_name=file_name.split("_")
        ship_company=splited_file_name[0]
        img_name=splited_file_name[1]
        page_num=splited_file_name[2]
        img_dir=os.path.join("/data-hdd/LingYue/booking_confirmation/base_class",ship_company,"doc2img")
        real_img_name=str(page_num)+"#"+str(img_name)+".jpg"
        img_path=os.path.join(img_dir,real_img_name)
        draw_rect_to_img(path,img_path)
        print("deal end ",path)
def from_file_find_bboxes_and_text(file_path):
    bboxes=[]
    texts=[]
    with open(file_path,encoding="utf-8") as file:
        lines=file.readlines()
        for line in lines:
            if len(line) > 0:
                splited_line = line.split(",")
                if len(splited_line) > 0:
                    box = list(map(int, splited_line[:8]))
                    bboxes.append(box)
                    text = str(splited_line[8]).strip("\n")
                    texts.append(text)
    return bboxes,texts

def generator_crnn_data_from_box_to_img(ocr_data_dir):
    save_lable_path=os.path.join(ocr_data_dir,"crnn_less_20_txt","gen.txt")
    save_img_dir=os.path.join(ocr_data_dir,"crnn_less_20_img")
    text_dir=os.path.join(ocr_data_dir,"txt")
    img_dir=os.path.join(ocr_data_dir,"img")
    with open(save_lable_path,"a+",encoding="utf-8") as f:
        for path in glob.glob(os.path.join(text_dir,"*.txt"),recursive=True):
            d=pathlib.Path(path)
            file_name=d.stem
            img_path=os.path.join(img_dir,file_name+".jpg")
            img=cv2.imread(img_path)
            bboxes,texts=from_file_find_bboxes_and_text(path)
            for i in range(len(bboxes)):
                box=bboxes[i]
                text=texts[i]

                img_id=i+1
                if len(text) <= 71:
                    try:
                        cropped_img, (topleft_x, topleft_y, bot_right_x, bot_right_y)=crop_4(img,box)
                        this_img_path=os.path.join(save_img_dir,file_name+"_croped_"+str(img_id)+".jpg")
                        cv2.imwrite(this_img_path,cropped_img)
                        f.write(file_name+"_croped_"+str(img_id)+".jpg★✿★"+text)
                        f.write("\n")
                    except Exception as e:
                        continue
            print("deal end "+path)




def crop_4(img,bbox):
    img_h,img_w=img.shape[:2]
    bbox = np.reshape(bbox,(4,2))
    topleft_x = np.min(bbox[:, 0])
    topleft_y = np.min(bbox[:, 1])
    bot_right_x = np.max(bbox[:, 0])
    bot_right_y = np.max(bbox[:, 1])
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#测试使用
    topleft_x=topleft_x-1 if (topleft_x-1)>0 else 0
    bot_right_x=bot_right_x+1 if (bot_right_x+1)<img_w else img_w
    topleft_y=topleft_y-3 if (topleft_y-3)>0 else 0
    bot_right_y=bot_right_y+3 if (bot_right_y+3)<img_h else img_h
    cropped_img = img[topleft_y:bot_right_y, topleft_x:bot_right_x]
    h, w, _ = cropped_img.shape
    # print("h,w",h,w)
    if h>32.0:
        scale=h/32.0
        new_w,new_h=int(w/scale),int(h/scale)
        # print(new_w,new_h)
        if new_w>720:
            cropped_img=cv2.resize(cropped_img,(0,0),fx=720/w,fy=new_h/h,interpolation=cv2.INTER_AREA)
        else:
            cropped_img = cv2.resize(cropped_img, (0, 0), fx=new_w / w, fy=new_h / h, interpolation=cv2.INTER_AREA)
            cropped_img = cv2.copyMakeBorder(cropped_img, 0, 0, 0, (720 - new_w), cv2.BORDER_CONSTANT,
                                             value=(255, 255, 255))
    else:
        top_dis=int((32-h)/2)
        bot_dis=(32-h)-top_dis
        cropped_img = cv2.copyMakeBorder(cropped_img, top_dis, bot_dis, 0, 0, cv2.BORDER_CONSTANT,
                                         value=(255, 255, 255))
        if w>720:
            cropped_img=cv2.resize(cropped_img,(0,0),fx=720/w,fy=1,interpolation=cv2.INTER_AREA)
        else:
            cropped_img = cv2.copyMakeBorder(cropped_img, 0, 0, 0, (720 - w), cv2.BORDER_CONSTANT,
                                             value=(255, 255, 255))

    return cropped_img, (topleft_x, topleft_y, bot_right_x, bot_right_y)
def remove_no_parse_file(save_dir,no_parse_list):
    img_dir=os.path.join(save_dir,"crnn_img_resize")
    save_path=os.path.join(save_dir,"crnn_txt_resize","gen_cleared.txt")
    txt_path=os.path.join(save_dir,"crnn_txt_resize","gen.txt")
    for no_parse_info in no_parse_list:
        img_name=no_parse_info.split("★✿★")[0]
        img_path=os.path.join(img_dir,img_name)
        if os.path.exists(img_path):
            os.remove(img_path)
            print("删除图片:"+img_path)
    cleared_txt=[]
    with open(txt_path,encoding="utf-8") as f:
        lines=f.readlines()
        for no_parse_info in no_parse_list:
            if no_parse_info in lines:
                lines.remove(no_parse_info)
                print("删除信息："+no_parse_info)
        with open(save_path,"a+",encoding="utf-8") as file:
            for line in lines:
                line=line.strip("\n")
                file.write(line)
                file.write("\n")



if __name__=="__main__":
    # remove_no_parse_file("/data-hdd/LingYue/ocr_data",['emc_0e8cd06ab65248f2b4522cfc5b2a536e_1_croped_51.jpg★✿★/40© HI-CUBE\n', 'maersk_2086459_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'emc_1bc1b66baeb241058679d2770a93ddd9_2_croped_9.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'cma_0c1b2ddddad74e27a226705e3d30f57d_1_croped_66.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_0c1b2ddddad74e27a226705e3d30f57d_1_croped_67.jpg★✿★• The name\n', 'cma_0c1b2ddddad74e27a226705e3d30f57d_1_croped_68.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_0c1b2ddddad74e27a226705e3d30f57d_1_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_0b9c4993fc3140bfb5aed728f6c5f0e7_2_croped_9.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'maersk_2146271_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'emc_2c2e212c89c84e4282950917b140fd4f_2_croped_9.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'emc_1fee5be6a2794ee28de514f115d88103_1_croped_49.jpg★✿★/40© HI-CUBE\n', 'emc_1c86c7d6fb2740b6b1763f041d008a96_2_croped_8.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'emc_1b0c4b9d70ea46cea18e6f0379947cbb_2_croped_14.jpg★✿★相关费率请至ªwww.master-agency.com.cn---->费率---->提单各项费用º查询。\n', 'emc_1b0c4b9d70ea46cea18e6f0379947cbb_2_croped_14.jpg★✿★相关费率请至ªwww.master-agency.com.cn---->费率---->提单各项费用º查询。\n', 'cma_5b75b8a96ba542d98844ea282bfc51bb_2_croped_57.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_5b75b8a96ba542d98844ea282bfc51bb_2_croped_59.jpg★✿★• The name\n', 'cma_5b75b8a96ba542d98844ea282bfc51bb_2_croped_62.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_5b75b8a96ba542d98844ea282bfc51bb_2_croped_64.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'maersk_2075207_1_croped_56.jpg★✿★运输方式\xa0船名\n', 'emc_1b0c4b9d70ea46cea18e6f0379947cbb_1_croped_52.jpg★✿★/40© HI-CUBE\n', 'cma_7e17ae524af94f71836904fc28878025_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_7e17ae524af94f71836904fc28878025_2_croped_64.jpg★✿★• The name\n', 'cma_7e17ae524af94f71836904fc28878025_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_7e17ae524af94f71836904fc28878025_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'maersk_2279463_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2026074_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2026074_1_croped_82.jpg★✿★❤重要提示：\n', 'cma_23218e1256ca485bb4fbc6aacf4adc65_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_23218e1256ca485bb4fbc6aacf4adc65_2_croped_64.jpg★✿★• The name\n', 'cma_23218e1256ca485bb4fbc6aacf4adc65_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_23218e1256ca485bb4fbc6aacf4adc65_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'cma_3472b11cb89c40e9bffa226413c42037_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_3472b11cb89c40e9bffa226413c42037_2_croped_64.jpg★✿★• The name\n', 'cma_3472b11cb89c40e9bffa226413c42037_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_3472b11cb89c40e9bffa226413c42037_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_01d27221106f44548b1642e7359d449a_1_croped_42.jpg★✿★/40© HI-CUBE\n', 'maersk_2305321_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2086459_2_croped_2.jpg★✿★❤重要提示：\n', 'emc_0a0201f857884c50adf375fb7a52f2db_1_croped_46.jpg★✿★/40© HI-CUBE\n', 'cma_761a46d5b640498f8d15843349a81cb9_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_761a46d5b640498f8d15843349a81cb9_2_croped_64.jpg★✿★• The name\n', 'cma_761a46d5b640498f8d15843349a81cb9_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_761a46d5b640498f8d15843349a81cb9_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'cma_3199176333f4419d9116bd5fe108e3fe_1_croped_70.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_3199176333f4419d9116bd5fe108e3fe_1_croped_71.jpg★✿★• The name\n', 'cma_3199176333f4419d9116bd5fe108e3fe_1_croped_72.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_3199176333f4419d9116bd5fe108e3fe_1_croped_73.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_0d5161f592ec48e2b87f171e702e9005_1_croped_68.jpg★✿★/40© STANDARD DRY\n', 'emc_1bc1b66baeb241058679d2770a93ddd9_1_croped_46.jpg★✿★/20© STANDARD DRY\n', 'maersk_2076946_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2076946_1_croped_81.jpg★✿★❤重要提示：\n', 'emc_2bd8aab2ca8747408a6fe393d0696164_1_croped_34.jpg★✿★:LEXUS PART©S ACCESSORIES CO.LTD\n', 'emc_2bd8aab2ca8747408a6fe393d0696164_1_croped_48.jpg★✿★/40© HI-CUBE\n', 'maersk_2305326_1_croped_27.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2305326_1_croped_80.jpg★✿★❤重要提示：\n', 'hpl_0fc573ec9d7b4f159a7584bdf31fb5db_1_croped_227.jpg★✿★Nicolás\n', 'emc_2cf311e18a124fb0b48cd19fbfb1bfbe_1_croped_34.jpg★✿★:LEXUS PART©S ACCESSORIES CO.LTD\n', 'emc_2cf311e18a124fb0b48cd19fbfb1bfbe_1_croped_48.jpg★✿★/40© HI-CUBE\n', 'emc_0dc23387b6204ca28613fcc13462e35b_1_croped_48.jpg★✿★/40© HI-CUBE\n', 'emc_0fdaa0b32c514630a07c41ceea1fbad5_1_croped_46.jpg★✿★/40© HI-CUBE\n', 'maersk_2004842_1_croped_79.jpg★✿★❤重要提示：\n', 'maersk_2056172_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2056172_1_croped_82.jpg★✿★❤重要提示：\n', 'cma_5b4ade6e4d534734aaaec9ed9b127598_1_croped_65.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_5b4ade6e4d534734aaaec9ed9b127598_1_croped_66.jpg★✿★• The name\n', 'cma_5b4ade6e4d534734aaaec9ed9b127598_1_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_5b4ade6e4d534734aaaec9ed9b127598_1_croped_68.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'hpl_1c1369e9d96a40728ff9250b656ede45_1_croped_45.jpg★✿★✖\n', 'emc_1aa947b72aff47c4a1cee350b0bf0bbf_1_croped_46.jpg★✿★/40© HI-CUBE\n', 'hpl_1fa5c07ee92b43538c622d55b435a9b9_1_croped_51.jpg★✿★✖\n', 'emc_1c86c7d6fb2740b6b1763f041d008a96_1_croped_46.jpg★✿★/20© STANDARD DRY\n', 'maersk_2049122_1_croped_31.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'emc_0dc23387b6204ca28613fcc13462e35b_2_croped_9.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'maersk_2146271_2_croped_2.jpg★✿★❤重要提示：\n', 'maersk_2023161_2_croped_9.jpg★✿★❤重要提示：\n', 'maersk_2070396_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2070396_1_croped_81.jpg★✿★❤重要提示：\n', 'mcc_7174bb7657c04a6aacbbac465b00b193_1_croped_32.jpg★✿★\xa0\xa0\xa0\n', 'mcc_7174bb7657c04a6aacbbac465b00b193_1_croped_32.jpg★✿★\xa0\xa0\xa0\n', 'mcc_7174bb7657c04a6aacbbac465b00b193_1_croped_32.jpg★✿★\xa0\xa0\xa0\n', 'emc_2bd8aab2ca8747408a6fe393d0696164_2_croped_9.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'emc_2cf311e18a124fb0b48cd19fbfb1bfbe_2_croped_9.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'cma_24dece82863f4bb1b6ee747f72e7ed24_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_24dece82863f4bb1b6ee747f72e7ed24_2_croped_64.jpg★✿★• The name\n', 'cma_24dece82863f4bb1b6ee747f72e7ed24_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_24dece82863f4bb1b6ee747f72e7ed24_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_0ad46a3b2cd74e2b943f26624aa17936_1_croped_46.jpg★✿★/40© HI-CUBE\n', 'cma_26a1fcf190444fd4baf37778da8175c8_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_26a1fcf190444fd4baf37778da8175c8_2_croped_64.jpg★✿★• The name\n', 'cma_26a1fcf190444fd4baf37778da8175c8_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_26a1fcf190444fd4baf37778da8175c8_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_0fdaa0b32c514630a07c41ceea1fbad5_2_croped_8.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'cma_0e22cf28dc5447608fc29d419335edff_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_0e22cf28dc5447608fc29d419335edff_2_croped_64.jpg★✿★• The name\n', 'cma_0e22cf28dc5447608fc29d419335edff_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_0e22cf28dc5447608fc29d419335edff_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'hpl_0fc573ec9d7b4f159a7584bdf31fb5db_2_croped_426.jpg★✿★Nicolás\n', 'maersk_2048145_1_croped_31.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.export@safmarine.com\n', 'maersk_2048145_1_croped_63.jpg★✿★运输方式\xa0船名\n', 'emc_1db69441bcd44dfc8f7f4005d8114f3f_1_croped_51.jpg★✿★/40© HI-CUBE\n', 'cma_933ca7cd667741ad837040427e0744d9_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_933ca7cd667741ad837040427e0744d9_2_croped_64.jpg★✿★• The name\n', 'cma_933ca7cd667741ad837040427e0744d9_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_933ca7cd667741ad837040427e0744d9_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_2d1f1b30244b407190bf8d2726983e69_1_croped_48.jpg★✿★/40© STANDARD DRY\n', 'cma_36ebff9647df4b9b8024735e56e43647_2_croped_62.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_36ebff9647df4b9b8024735e56e43647_2_croped_64.jpg★✿★• The name\n', 'cma_36ebff9647df4b9b8024735e56e43647_2_croped_67.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_36ebff9647df4b9b8024735e56e43647_2_croped_69.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'hpl_1cba18c4ba0e40d282dce9a15a38d551_1_croped_45.jpg★✿★✖\n', 'emc_1dd096d2429b4f289e6a7ef11b81235a_1_croped_34.jpg★✿★:LEXUS PART©S ACCESSORIES CO.LTD\n', 'emc_1dd096d2429b4f289e6a7ef11b81235a_1_croped_50.jpg★✿★/40© HI-CUBE\n', 'cma_8c3e93ea9b7a480181a2a16906f05315_2_croped_57.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_8c3e93ea9b7a480181a2a16906f05315_2_croped_59.jpg★✿★• The name\n', 'cma_8c3e93ea9b7a480181a2a16906f05315_2_croped_62.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_8c3e93ea9b7a480181a2a16906f05315_2_croped_64.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'cma_64d01129d0194a6f9b8c5fdbe55cb2de_2_croped_53.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_64d01129d0194a6f9b8c5fdbe55cb2de_2_croped_55.jpg★✿★• The name\n', 'cma_64d01129d0194a6f9b8c5fdbe55cb2de_2_croped_58.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_64d01129d0194a6f9b8c5fdbe55cb2de_2_croped_60.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'hpl_0fc573ec9d7b4f159a7584bdf31fb5db_3_croped_208.jpg★✿★Nicolás\n', 'cma_6a44381bace9402e945a132e121e6bcd_2_croped_53.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_6a44381bace9402e945a132e121e6bcd_2_croped_55.jpg★✿★• The name\n', 'cma_6a44381bace9402e945a132e121e6bcd_2_croped_58.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_6a44381bace9402e945a132e121e6bcd_2_croped_60.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_1e536c150b844858900c5afc7164fc06_1_croped_42.jpg★✿★:AND COUNT ARRASADOR 75.7 SG(GLYPHOSATE 75.7 SG)CUSTOMER©S REF.STK01796\n', 'emc_1e536c150b844858900c5afc7164fc06_1_croped_52.jpg★✿★/40© HI-CUBE\n', 'emc_1fee5be6a2794ee28de514f115d88103_2_croped_9.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'emc_0dcf14eb93534f78acaccb2c514389a7_1_croped_46.jpg★✿★/20© STANDARD DRY\n', 'maersk_2069643_1_croped_62.jpg★✿★运输方式\xa0船名\n', 'maersk_2049122_2_croped_2.jpg★✿★❤重要提示：\n', 'maersk_2066349_1_croped_28.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2066349_1_croped_82.jpg★✿★❤重要提示：\n', 'cma_2f31721f7e384a9da949e011f82b96c7_2_croped_59.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_2f31721f7e384a9da949e011f82b96c7_2_croped_61.jpg★✿★• The name\n', 'cma_2f31721f7e384a9da949e011f82b96c7_2_croped_64.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_2f31721f7e384a9da949e011f82b96c7_2_croped_66.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_0cb2f5768bb447f39c6f1fd057794ecb_1_croped_47.jpg★✿★/40© HI-CUBE\n', 'maersk_2006751_1_croped_32.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'maersk_2006751_1_croped_92.jpg★✿★❤重要提示：\n', 'maersk_2283907_1_croped_30.jpg★✿★❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com\n', 'emc_1c69f888269f4b2bb07e7b5328b5b7c9_1_croped_37.jpg★✿★:SHIPPER©S LOAD\n', 'emc_1c69f888269f4b2bb07e7b5328b5b7c9_1_croped_46.jpg★✿★/40© HI-CUBE\n', 'emc_01d27221106f44548b1642e7359d449a_2_croped_8.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'emc_1b257d0da7654660913f9548e33fa742_1_croped_42.jpg★✿★:1X40©HC(FCL) CY-CY S.T.C.115 CTNS OF SKD-108RAINBOW251 CTNS OF SKD-05 \n', 'emc_1b257d0da7654660913f9548e33fa742_1_croped_56.jpg★✿★/40© HI-CUBE\n', 'emc_2cd541f517cb44df9da0a852a13f8fa6_1_croped_21.jpg★✿★(8) Point and Country of Origin (for the Merchant＇\n', 'emc_2cd541f517cb44df9da0a852a13f8fa6_1_croped_48.jpg★✿★(M³)\n', 'emc_2cd541f517cb44df9da0a852a13f8fa6_1_croped_60.jpg★✿★GLDU5746415/20©/EMCWCX6728/14 PALLETS\n', 'emc_2cd541f517cb44df9da0a852a13f8fa6_1_croped_61.jpg★✿★1 X 20©\n', 'emc_2cd541f517cb44df9da0a852a13f8fa6_1_croped_65.jpg★✿★SHIPPER©S LOAD & COUNT\n', 'emc_2c2e212c89c84e4282950917b140fd4f_1_croped_34.jpg★✿★:LEXUS PART©S ACCESSORIES CO.LTD\n', 'emc_2c2e212c89c84e4282950917b140fd4f_1_croped_48.jpg★✿★/40© HI-CUBE\n', 'emc_0b9c4993fc3140bfb5aed728f6c5f0e7_1_croped_46.jpg★✿★/40© HI-CUBE\n', 'cma_0c9667e2e899465590d4921ba7688e7b_1_croped_64.jpg★✿★• Part or all of the cargo actually stuffed inside the container is dangerous cargo\n', 'cma_0c9667e2e899465590d4921ba7688e7b_1_croped_65.jpg★✿★• The name\n', 'cma_0c9667e2e899465590d4921ba7688e7b_1_croped_66.jpg★✿★• The cargo is declared as general cargo at the time of booking but is requested to be amended to dangerous cargo after our release of the empty container.\n', 'cma_0c9667e2e899465590d4921ba7688e7b_1_croped_67.jpg★✿★• The cargo is discovered or determined by any domestic or foreign authority (including but not limited to customs\n', 'emc_0fec96bc01104e19811c2ef5d7b6039a_1_croped_46.jpg★✿★/40© HI-CUBE\n', 'emc_0c0cadfeadca40e9aadd8a19ce1230c5_2_croped_9.jpg★✿★CHINA SAILING INT©L SHIPPING AGENCY LTD\n', 'emc_0c0cadfeadca40e9aadd8a19ce1230c5_1_croped_34.jpg★✿★:LEXUS PART©S ACCESSORIES CO.LTD\n', 'emc_0c0cadfeadca40e9aadd8a19ce1230c5_1_croped_48.jpg★✿★/40© HI-CUBE\n'])
    generator_crnn_data_from_box_to_img("/data-hdd/LingYue/ocr_data")
    # analysis_bbox_to_img("/data-hdd/LingYue/ocr_data/txt")
#     # origin_text={'file_id': 4490793, 'file_name': 'daca63b122a6460697c36d3bd170aafc.jpg', 'file_type': 'PDF_GROUP', 'file_url': 'http://sruserfiletest.oss-cn-hangzhou.aliyuncs.com/oms/file_convert/daca63b122a6460697c36d3bd170aafc.jpg?Expires=1586924447&OSSAccessKeyId=LTAI4FufopNQTpwzS98ThU38&Signature=XLpF4Scx4MQAbGGeLUzZTtw6c4c%3D', 'page_index': 1, 'page_width': 595.0, 'page_height': 842.0, 'image_info': {'page_index': 1, 'image_file_id': 4490793, 'height': 3508, 'width': 2479, 'image_path': 'http://sruserfiletest.oss-cn-hangzhou.aliyuncs.com/oms/file_convert/daca63b122a6460697c36d3bd170aafc.jpg?Expires=1586924447&OSSAccessKeyId=LTAI4FufopNQTpwzS98ThU38&Signature=XLpF4Scx4MQAbGGeLUzZTtw6c4c%3D'}, 'text_infos': [{'text': 'BOOKING AMENDMENT', 'text_rectangle': {'llx': 344.82, 'lly': 30.0339, 'urx': 534.036, 'ury': 47.6339, 'height': 17.6, 'width': 189.216}}, {'text': '订舱号:', 'text_rectangle': {'llx': 30.278, 'lly': 77.23805, 'urx': 56.502, 'ury': 86.03805, 'height': 8.799995, 'width': 26.223999}}, {'text': '打印时间：', 'text_rectangle': {'llx': 402.572, 'lly': 76.8018, 'urx': 442.572, 'ury': 85.6018, 'height': 8.799995, 'width': 40.0}}, {'text': '2019-10-21 08:46 UTC', 'text_rectangle': {'llx': 453.603, 'lly': 77.3873, 'urx': 534.243, 'ury': 86.1873, 'height': 8.800003, 'width': 80.639984}}, {'text': '587093467', 'text_rectangle': {'llx': 112.493, 'lly': 75.2284, 'urx': 181.289, 'ury': 88.4284, 'height': 13.199997, 'width': 68.796005}}, {'text': '订舱人:', 'text_rectangle': {'llx': 28.3502, 'lly': 94.436, 'urx': 54.5742, 'ury': 103.236, 'height': 8.800003, 'width': 26.223999}}, {'text': 'YUEHAI SUPPLY CHAIN SERVICE CO LTD', 'text_rectangle': {'llx': 108.439, 'lly': 94.397, 'urx': 253.223, 'ury': 103.197, 'height': 8.799995, 'width': 144.784}}, {'text': '交接方式:', 'text_rectangle': {'llx': 311.852, 'lly': 94.436, 'urx': 346.076, 'ury': 103.236, 'height': 8.800003, 'width': 34.224}}, {'text': 'CY/CY', 'text_rectangle': {'llx': 384.003, 'lly': 94.397, 'urx': 405.891, 'ury': 103.197, 'height': 8.799995, 'width': 21.888}}, {'text': '联系人:', 'text_rectangle': {'llx': 28.3502, 'lly': 105.776, 'urx': 54.5742, 'ury': 114.576, 'height': 8.799995, 'width': 26.223999}}, {'text': 'BESS LI', 'text_rectangle': {'llx': 108.439, 'lly': 105.256, 'urx': 135.935, 'ury': 114.056, 'height': 8.800003, 'width': 27.495995}}, {'text': '收货地:', 'text_rectangle': {'llx': 311.852, 'lly': 105.776, 'urx': 338.076, 'ury': 114.576, 'height': 8.799995, 'width': 26.223999}}, {'text': 'From:', 'text_rectangle': {'llx': 311.852, 'lly': 105.776, 'urx': 332.74, 'ury': 114.576, 'height': 8.799995, 'width': 20.888}}, {'text': 'Shanghai,Shanghai,China', 'text_rectangle': {'llx': 384.003, 'lly': 105.737, 'urx': 473.627, 'ury': 114.537, 'height': 8.800003, 'width': 89.62402}}, {'text': '订舱人参考号:', 'text_rectangle': {'llx': 28.2651, 'lly': 117.201, 'urx': 78.4891, 'ury': 126.001, 'height': 8.800003, 'width': 50.224}}, {'text': '交货地:', 'text_rectangle': {'llx': 311.852, 'lly': 117.116, 'urx': 338.076, 'ury': 125.916, 'height': 8.800003, 'width': 26.223999}}, {'text': 'To:', 'text_rectangle': {'llx': 311.852, 'lly': 117.116, 'urx': 323.412, 'ury': 125.916, 'height': 8.800003, 'width': 11.559998}}, {'text': 'Sydney,New South Wales,Australia', 'text_rectangle': {'llx': 384.003, 'lly': 117.078, 'urx': 505.427, 'ury': 125.878, 'height': 8.799995, 'width': 121.42401}}, {'text': '合约号:', 'text_rectangle': {'llx': 28.3502, 'lly': 128.456, 'urx': 54.5742, 'ury': 137.256, 'height': 8.800003, 'width': 26.223999}}, {'text': '54963584', 'text_rectangle': {'llx': 108.439, 'lly': 128.418, 'urx': 143.383, 'ury': 137.218, 'height': 8.800003, 'width': 34.943993}}, {'text': 'Customer Commodity:', 'text_rectangle': {'llx': 311.852, 'lly': 128.456, 'urx': 391.42, 'ury': 137.256, 'height': 8.800003, 'width': 79.56802}}, {'text': '54963584', 'text_rectangle': {'llx': 394.351, 'lly': 128.418, 'urx': 429.295, 'ury': 137.218, 'height': 8.800003, 'width': 34.944}}, {'text': '合约客户:', 'text_rectangle': {'llx': 28.3502, 'lly': 139.796, 'urx': 62.5742, 'ury': 148.596, 'height': 8.799988, 'width': 34.224}}, {'text': 'YUEHAI SUPPLY CHAIN SERVICE CO LTD', 'text_rectangle': {'llx': 108.439, 'lly': 139.7863, 'urx': 253.223, 'ury': 148.5863, 'height': 8.800003, 'width': 144.784}}, {'text': '受理订舱分公司:', 'text_rectangle': {'llx': 311.852, 'lly': 139.796, 'urx': 370.076, 'ury': 148.596, 'height': 8.799988, 'width': 58.224}}, {'text': 'Business Unit:', 'text_rectangle': {'llx': 311.852, 'lly': 139.796, 'urx': 362.98, 'ury': 148.596, 'height': 8.799988, 'width': 51.12802}}, {'text': 'Maersk China Shipping (Qingdao)', 'text_rectangle': {'llx': 384.003, 'lly': 139.758, 'urx': 502.091, 'ury': 148.558, 'height': 8.800003, 'width': 118.08801}}, {'text': '参考号:', 'text_rectangle': {'llx': 28.3502, 'lly': 151.136, 'urx': 54.5742, 'ury': 159.936, 'height': 8.800003, 'width': 26.223999}}, {'text': 'Commodity Description:', 'text_rectangle': {'llx': 311.795, 'lly': 150.966, 'urx': 396.699, 'ury': 159.766, 'height': 8.800003, 'width': 84.90399}}, {'text': 'Chemical products, nos', 'text_rectangle': {'llx': 397.271, 'lly': 151.2113, 'urx': 479.255, 'ury': 160.0113, 'height': 8.800003, 'width': 81.98401}}, {'text': 'We request you to review the specific parameters, viz. Service Contract, Price Owner, Named account customer and', 'text_rectangle': {'llx': 29.1723, 'lly': 163.728, 'urx': 550.8923, 'ury': 172.528, 'height': 8.800003, 'width': 521.72}}, {'text': 'Commodity description. In case there are any changes required to these parameters, please send us a request before', 'text_rectangle': {'llx': 29.1723, 'lly': 173.328, 'urx': 557.9403, 'ury': 182.128, 'height': 8.800003, 'width': 528.768}}, {'text': 'any containers(s) are picked up.', 'text_rectangle': {'llx': 29.1723, 'lly': 182.928, 'urx': 175.2603, 'ury': 191.728, 'height': 8.800003, 'width': 146.088}}, {'text': '"***************** [截操作时间参考] *****************', 'text_rectangle': {'llx': 33.4037, 'lly': 202.1591, 'urx': 228.6407, 'ury': 212.0591, 'height': 9.899994, 'width': 195.237}}, {'text': '❤ 如有任何疑问，请联系我司客服邮箱 cn.east.export@maersk.com', 'text_rectangle': {'llx': 30.9017, 'lly': 224.9531, 'urx': 302.7647, 'ury': 234.8531, 'height': 9.900009, 'width': 271.863}}, {'text': '航线:', 'text_rectangle': {'llx': 30.9017, 'lly': 247.7461, 'urx': 51.4037, 'ury': 257.6461, 'height': 9.899994, 'width': 20.502003}}, {'text': 'DRAGON ', 'text_rectangle': {'llx': 171.4997, 'lly': 247.7461, 'urx': 213.5027, 'ury': 257.6461, 'height': 9.899994, 'width': 42.003006}}, {'text': '开港参考时间(CY-Open):', 'text_rectangle': {'llx': 30.9017, 'lly': 259.1431, 'urx': 130.9097, 'ury': 269.0431, 'height': 9.899994, 'width': 100.007996}}, {'text': '请以码头网站时间为准', 'text_rectangle': {'llx': 168.4397, 'lly': 259.1431, 'urx': 258.4397, 'ury': 269.0431, 'height': 9.899994, 'width': 90.0}}, {'text': '截港时间(CY-CUTOFF):', 'text_rectangle': {'llx': 30.9017, 'lly': 270.5401, 'urx': 127.3907, 'ury': 280.4401, 'height': 9.899994, 'width': 96.489}}, {'text': 'TUE 08:00(请在此时间前完成集装箱进港并取得海关放行)', 'text_rectangle': {'llx': 134.8967, 'lly': 270.5401, 'urx': 363.9107, 'ury': 280.4401, 'height': 9.899994, 'width': 229.014}}, {'text': 'VGM截止时间(VGM Deadline):MON 17:00(请在此时间前提交VGM信息)', 'text_rectangle': {'llx': 30.9017, 'lly': 281.9371, 'urx': 316.9307, 'ury': 291.8371, 'height': 9.899994, 'width': 286.029}}, {'text': '样单截至参考时间(SI-CUT):', 'text_rectangle': {'llx': 30.9017, 'lly': 293.3331, 'urx': 141.3947, 'ury': 303.2331, 'height': 9.899994, 'width': 110.493}}, {'text': 'MON 00:00 (需要申报欧盟/美国及加拿大海关提前舱单的货物， ', 'text_rectangle': {'llx': 168.9167, 'lly': 293.3331, 'urx': 423.4367, 'ury': 303.2331, 'height': 9.899994, 'width': 254.52}}, {'text': '请严格按照此时间提交提单样本，及完整信息:包括所有品名的6位HS商品编码，托运人和收货人（或通知方）公司名称，街道地址，城', 'text_rectangle': {'llx': 30.9017, 'lly': 304.7301, 'urx': 563.9087, 'ury': 314.6301, 'height': 9.899994, 'width': 533.007}}, {'text': '市等)', 'text_rectangle': {'llx': 30.9017, 'lly': 316.1271, 'urx': 51.8987, 'ury': 326.0271, 'height': 9.899994, 'width': 20.997002}}, {'text': '* 以上信息供您参考, 如遇船舶操作时间变动,请以客户通知为准.', 'text_rectangle': {'llx': 30.9017, 'lly': 327.5241, 'urx': 280.9127, 'ury': 337.4241, 'height': 9.899994, 'width': 250.01099}}, {'text': '* 如预配船期中母船第一卸货港为亚洲中转港(如TPP), 样单截止参考时间为船开前发送即可.', 'text_rectangle': {'llx': 30.9017, 'lly': 338.9201, 'urx': 391.9097, 'ury': 348.8201, 'height': 9.899994, 'width': 361.008}}, {'text': '危险品上船表格截止时间:', 'text_rectangle': {'llx': 30.9017, 'lly': 350.3171, 'urx': 132.4037, 'ury': 360.2171, 'height': 9.899994, 'width': 101.502}}, {'text': 'Final MDGF cut off (for MSC only):', 'text_rectangle': {'llx': 30.9017, 'lly': 361.7141, 'urx': 169.4297, 'ury': 371.6141, 'height': 9.899994, 'width': 138.528}}, {'text': 'Final MDGF cut off (for ML and other VSA):FRI 11:00', 'text_rectangle': {'llx': 30.9017, 'lly': 373.1111, 'urx': 243.4817, 'ury': 383.0111, 'height': 9.899994, 'width': 212.58}}, {'text': 'Special remarks(注意事项):', 'text_rectangle': {'llx': 30.9017, 'lly': 395.9041, 'urx': 139.9097, 'ury': 405.8041, 'height': 9.899994, 'width': 109.007996}}, {'text': 'For DG Barge: 请在驳船开船前2个工作日的上午10:00前发送带有箱封号的Final DG ', 'text_rectangle': {'llx': 30.9017, 'lly': 407.3011, 'urx': 364.4507, 'ury': 417.2011, 'height': 9.900024, 'width': 333.549}}, {'text': 'form(并于MSDS合并为一个文件)到我司邮箱cn.east.export@maersk.com, 若Final DG form未能及时提供, 将可能影响箱子装船, ', 'text_rectangle': {'llx': 30.9017, 'lly': 418.6981, 'urx': 536.5847, 'ury': 428.5981, 'height': 9.900024, 'width': 505.683}}, {'text': '由此产生的相关费用需由Shipper承担, 请知悉.', 'text_rectangle': {'llx': 30.9017, 'lly': 430.0951, 'urx': 213.4217, 'ury': 439.9951, 'height': 9.899994, 'width': 182.52}}, {'text': '我们谨此通知您，对于所有出口至加蓬的货物，在提交提单补料时必须提供BIETC货物跟踪单号, ', 'text_rectangle': {'llx': 30.9017, 'lly': 452.8881, 'urx': 413.4107, 'ury': 462.7881, 'height': 9.899994, 'width': 382.509}}, {'text': '如未能及时提供跟踪单号，货物将无法装船， 缺失正确的BIETC货物跟踪单号可能存在货物到港后无法卸货， ', 'text_rectangle': {'llx': 30.9017, 'lly': 464.2851, 'urx': 467.4107, 'ury': 474.1851, 'height': 9.899994, 'width': 436.509}}, {'text': '原船回运以及海关罚款和扣货的风险。', 'text_rectangle': {'llx': 30.9017, 'lly': 475.6821, 'urx': 183.9017, 'ury': 485.5821, 'height': 9.899994, 'width': 153.0}}, {'text': 'We hereby inform you that all Cargo export to Gabon will require to submit BIETC Number on Shipping Instruction, Failure to comply ', 'text_rectangle': {'llx': 30.9017, 'lly': 487.0781, 'urx': 560.1017, 'ury': 496.9781, 'height': 9.899994, 'width': 529.2}}, {'text': 'with this requirements will lead to our inability to load your cargo at Origin Port, Load without BIETC number will result in possible ', 'text_rectangle': {'llx': 30.9017, 'lly': 498.4751, 'urx': 546.0887, 'ury': 508.3751, 'height': 9.899994, 'width': 515.187}}, {'text': 'retention on board, return back to origin, seizure of the cargo and settlement of fines before release.', 'text_rectangle': {'llx': 30.9017, 'lly': 509.8721, 'urx': 428.1077, 'ury': 519.7721, 'height': 9.899994, 'width': 397.206}}, {'text': '开顶柜,框架箱,超高超宽超长货物及冷冻柜:', 'text_rectangle': {'llx': 30.9017, 'lly': 532.6651, 'urx': 200.4077, 'ury': 542.5651, 'height': 9.900024, 'width': 169.506}}, {'text': '最晚提箱时间(for MSC only):', 'text_rectangle': {'llx': 30.9017, 'lly': 544.0621, 'urx': 145.4087, 'ury': 553.9621, 'height': 9.900024, 'width': 114.507}}, {'text': '最晚提箱时间(for ML and other VSA):FRI 11:00', 'text_rectangle': {'llx': 30.9017, 'lly': 555.4591, 'urx': 219.4607, 'ury': 565.3591, 'height': 9.899963, 'width': 188.55899}}, {'text': '* 超高超宽超长货物(OOG): ', 'text_rectangle': {'llx': 30.9017, 'lly': 578.2531, 'urx': 140.9087, 'ury': 588.1531, 'height': 9.899963, 'width': 110.007}}, {'text': '请在特种柜提柜截止时间前安排提柜，同时请确保在装箱后确认实际的货物尺寸和重量,如实际货物的超限尺寸和重量与订舱信息不符或', 'text_rectangle': {'llx': 30.9017, 'lly': 589.6491, 'urx': 564.4037, 'ury': 599.5491, 'height': 9.899963, 'width': 533.502}}, {'text': '者有任何尺寸和重量的更改申请,请在提箱后把柜号及其对应尺寸尽快发送到：CN.EAST.EXPORT@maersk.com ', 'text_rectangle': {'llx': 30.9017, 'lly': 601.0461, 'urx': 478.5617, 'ury': 610.9461, 'height': 9.900024, 'width': 447.66}}, {'text': '以避免后续更改可能导致货物被拒上船,由此产生的责任与费用将由客户全责承担. (SOC ', 'text_rectangle': {'llx': 30.9017, 'lly': 612.4431, 'urx': 378.4097, 'ury': 622.3431, 'height': 9.899963, 'width': 347.508}}, {'text': 'OOG-货主自有箱承载的超限货物也需在此时间前及时告知箱号及尺寸信息，如在订舱时已注明箱号并且箱号及对应尺寸没有更改的则', 'text_rectangle': {'llx': 30.9017, 'lly': 623.8401, 'urx': 558.9047, 'ury': 633.7401, 'height': 9.900024, 'width': 528.00305}}, {'text': '不需另外通知我司).', 'text_rectangle': {'llx': 30.9017, 'lly': 635.2361, 'urx': 108.4007, 'ury': 645.1361, 'height': 9.900024, 'width': 77.49901}}, {'text': '***危险品***', 'text_rectangle': {'llx': 30.9017, 'lly': 658.0301, 'urx': 78.9077, 'ury': 667.9301, 'height': 9.900024, 'width': 48.006}}, {'text': '1)如需更改危险品相关信息，请务必在箱子进港之前提出申请，任何更改都需要重新进行危险品审批，有可能会导致货物不能及时装船.', 'text_rectangle': {'llx': 30.9017, 'lly': 669.4271, 'urx': 563.4047, 'ury': 679.3271, 'height': 9.899963, 'width': 532.50305}}, {'text': '2)头程船涉及驳船运输的危险品，如需更改，请务必在箱子进港之前提出。另外请在驳船开船前2个工作日的上午10:00前发送带有箱封', 'text_rectangle': {'llx': 30.9017, 'lly': 680.8231, 'urx': 561.4247, 'ury': 690.7231, 'height': 9.899963, 'width': 530.523}}, {'text': '号的Final DG.', 'text_rectangle': {'llx': 30.9017, 'lly': 692.2201, 'urx': 86.9087, 'ury': 702.1201, 'height': 9.900024, 'width': 56.007}}, {'text': '3)请确保危险品货物的正确申报。重柜还场后凡发现危险品错报、瞒报、漏报的情况（包括但不止于更改货物属性，增加或修改UN号码', 'text_rectangle': {'llx': 30.9017, 'lly': 703.6171, 'urx': 564.8987, 'ury': 713.5171, 'height': 9.899963, 'width': 533.997}}, {'text': 'This document is subject to following:', 'text_rectangle': {'llx': 28.3502, 'lly': 716.767, 'urx': 128.8982, 'ury': 723.367, 'height': 6.5999756, 'width': 100.54799}}, {'text': '- This booking and carriage are subject to the Maersk Line Terms and Conditions of Carriage which are available upon request from the carrier or his representatives and are furthermore accessible on the', 'text_rectangle': {'llx': 28.3502, 'lly': 723.967, 'urx': 566.7482, 'ury': 730.567, 'height': 6.6000366, 'width': 538.398}}, {'text': 'Maersk Line website "<http://www.maerskline.com>" under "Services" / "General Business Terms".', 'text_rectangle': {'llx': 28.3502, 'lly': 731.167, 'urx': 291.8702, 'ury': 737.767, 'height': 6.6000366, 'width': 263.52002}}, {'text': '- The shipment is subject to tariff rates unless a correct and applicable service contract number is available', 'text_rectangle': {'llx': 28.3502, 'lly': 738.367, 'urx': 311.5382, 'ury': 744.967, 'height': 6.5999756, 'width': 283.18802}}, {'text': "- The carrier's right to substitute the named and/or performing vessel(s) with another vessel or vessels at any time.", 'text_rectangle': {'llx': 28.3502, 'lly': 745.567, 'urx': 334.5122, 'ury': 752.167, 'height': 6.5999756, 'width': 306.16202}}, {'text': '- Arrival, berthing, departure and transit times are estimated and given without guarantee and subject to change without prior notice', 'text_rectangle': {'llx': 28.3502, 'lly': 752.767, 'urx': 380.8502, 'ury': 759.367, 'height': 6.5999756, 'width': 352.5}}, {'text': '- All dates/times are given as reasonable estimates only and subject to change without prior notice.', 'text_rectangle': {'llx': 28.3502, 'lly': 759.967, 'urx': 292.1462, 'ury': 766.567, 'height': 6.6000366, 'width': 263.79602}}, {'text': 'Shipments destined for or carried/transhipped via the USA:', 'text_rectangle': {'llx': 28.3502, 'lly': 767.167, 'urx': 184.5602, 'ury': 773.767, 'height': 6.6000366, 'width': 156.20999}}, {'text': '- This document is given subject to the customer providing the correct cargo description in accordance with U.S. law, including U.S. Customs requirements as described in Customs Rules and Regulations,', 'text_rectangle': {'llx': 28.3502, 'lly': 774.367, 'urx': 565.7582, 'ury': 780.967, 'height': 6.5999756, 'width': 537.40796}}, {'text': '19 CFR Parts 4, 113 and 178 of October 31, 2002', 'text_rectangle': {'llx': 28.3502, 'lly': 781.567, 'urx': 159.3542, 'ury': 788.167, 'height': 6.5999756, 'width': 131.004}}, {'text': 'Page', 'text_rectangle': {'llx': 249.255, 'lly': 789.303, 'urx': 266.311, 'ury': 798.103, 'height': 8.800049, 'width': 17.056}}, {'text': '1/3', 'text_rectangle': {'llx': 276.556, 'lly': 789.359, 'urx': 288.348, 'ury': 798.159, 'height': 8.799988, 'width': 11.791992}}], 'cells_text': []}
#     # scale=4.1663
#     # file_name="2028230"
#     # page_id=1
#     # generator_data_from_origin_text(origin_text,scale,file_name,page_id)
#     draw_rect_to_img("/data-hdd/LingYue/ocr_data/2028230_1.txt","/data-hdd/LingYue/booking_confirmation/base_class/maersk/doc2img/12028230.jpg","/data-hdd/LingYue/ocr_data/img")


