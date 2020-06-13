   
   
   
   
    # @property
    # def annotation(self):

    #     # TODO:
    #     # 1) colors per class
    #     # 2) write to png
        
    #     max_len = 150
    #     text = ""
    #     for paragraph in self.paragraphs:
    #         paragraph_text = ""
    #         current_len = 0
    #         for token in paragraph.tokens:
                
    #             if token.label["ac"] != "None":
    #                 strin_to_add = Back.GREEN + token.text + " " + Style.RESET_ALL
    #             else:
    #                 strin_to_add = token.text + " "
                
    #             if current_len > max_len:
    #                 paragraph_text += "\n"
    #                 current_len = 0

    #             paragraph_text += strin_to_add
    #             current_len += len(token.text + " ")

    #         text += paragraph_text + "\n"

    #             # if token.text == ".":
    #             #     text += Style.RESET_ALL + "\n"

    #     # from PIL import Image, ImageDraw, ImageFont
    #     # image = Image.new(mode = "RGB", size = (1000,500), color = "black")
    #     # draw = ImageDraw.Draw(image)
    #     # fnt = ImageFont.load_default()
    #     # draw.text((50,50), self.text, font=fnt) #, fill=(255,255,0))        
    #     # image.save("test.png")
        
    #     return text