import rize 
class rize_blocks():
    def __init__(self, blockly, color_input, color_output):
        self.blockly = blockly
        self.color_input =  color_input
        self.color_output = color_output
        
    

    def generate(self):
        onlyfiles = rize.getFiles("primitives")
        for file_ in onlyfiles:
            self.generatePrimitive(file_)


    def generatePrimitive(self, file_):
        # Get file name
        path = "primitives"
        name_file =  file_.split('.')[0]
        # Read json definition of primitives
        json_data = rize.readJSON(path + "/" + file_)
        data = rize.json2dict(json_data)
        # Tranform JS definitions in blockly Javascript definitions
        block, name = self.dict2block(name_file,data)

        # Have the primitive optional parameters?
        options = False
        if "options" in data:
            options = True
            
   
        print (name)
        # Add XML definition to toolbox
        self.blockly.add_toolbox_xml(name,data['type'])

        # Get the auto generated code needed to define a primitive.
        code = self.code_generator(name_file, options)  

        # Add the code to the generator file
        self.blockly.add_code_generator(code)
        # Add the block definition to the block file
        self.blockly.add_block_definition(block)
        # Add block to database
        self.blockly.add_database(name_file,data)


    def code_generator(self, block_name, options):
        """ Default code generator for primitive blocks.

        Parameters
        ----------

        block_name : string
            Primitive/Block name
            
        options: bool
            True is primitive requires additional parameters

        """
        new_line = "\n"
        init = "Blockly.Python['" + str(block_name) + "'] = function(block) {" + new_line
        text_input = ""
        block_input = ""
        code_value = ""
        final = ""
        
        text_input = "var text = block.getFieldValue('inp_1');" + new_line
        option_feld = ""
        
        if options:
            text_input = text_input + "var options_dic = block.getFieldValue('inp_2');" + new_line
            text_input  = text_input + 'options_dic = rizeBlockly.formatOptions(options_dic) '  + new_line 
            option_feld = """'"options":' + options_dic + '}';"""

        else:
            option_feld = """'"options":"none"}';"""

        coma = '+","+' 
        dictionary_start =   "var code  = '{"
        primitive_field = '"primitive":"' +  str(block_name) + '"' + "'"
        input_field = """ '"input":' + '"' + text + '"'"""
        code_value = dictionary_start + primitive_field + coma + input_field + coma + option_feld + new_line
        final = "return [code, Blockly.Python.ORDER_NONE];"

        return init + text_input +  block_input + code_value +  final + new_line + "};"  

    def dict2block(self, block_name, block_description):
        """
        Define new block from a description
        """

        # Primitive name
        main_text =  block_description["primitive"]
        # Primitive type
        primitive_type = block_description["type"]
        # User description of the primitive
        description = block_description["description"]

        # Additional parameters
        options = False
        if "options" in block_description:
            options = True

        # New block creator
        d = block_creator(block_name, description)

        # New dummy input
        dummy_input = d.set_input("dummy_input")

        # Set the primitive name in a Label
        d.add_text_field(main_text)
        
        #Add field for main description
        d.add_text_input_field()
        if options:
            # Add options label
            d.add_text_field(" options")
            # Add field for options
            d.add_text_input_field()
            
        # Add image to open modal
        d.add_configuration_image()
        # Get all fields
        fields_region = d.get_fields()
        # Set color of the block
                
        if primitive_type == "output":
            conf_zone = d.set_block_configuration(block_color = self.color_input, connections = "left", allowed_types = ["action"])
        elif primitive_type == "input":
            conf_zone = d.set_block_configuration(block_color = self.color_output, connections = "left", allowed_types =["condition"])
        else:
            print("block type non allowed")

        block = d.init + dummy_input + fields_region + conf_zone  + d.final
        return block,block_name


class toolbox_creator:
    def __init__(self, name_toolbox, color_inputs, color_outputs):
        """Creates a new blockly toolbox
            
            Parameters
            ----------
            name_toolbox: string
                USe this parameter to set the Javascript variable name
        """

        self.color_inputs = color_inputs
        self.color_outputs = color_outputs
        self.categories = {} # This variabel saves the XML definitions of the blocks in a string 
        self.name_toolbox = name_toolbox
    
    def add_xml_block(self,block_name,category):
        """ Add a new block definition to the toolbox and set the category
            
            Parameters
            ----------

            block_name : string 
                Name of the block
            category : string 
                Category of the block
        """

        if category in self.categories:
            # Concatenate a block in the XML definition (in a string) of the category
            self.categories[category] = self.categories[category] +  self.name_toolbox + " +='    <block type=" +'"'+ str(block_name) +'"' + "></block>';\n"
        else:
            # Start the XML definition (in a string) of a category
            self.categories[category] =  self.name_toolbox + " +='    <block type=" +'"'+ str(block_name) +'"' + "></block>';\n"
            

    def __add_category(self, category_name, color = "#F62459"):
        category_name = category_name.replace("_", " ")
        value =  self.name_toolbox + " += '" +  '<category name="' + str(category_name) + '"' + ' colour="' +  color + '"' + """>'\n"""
        return value

    def get_blocks(self):

        outputs = self.__add_category("Set robot actions",self.color_outputs ) + self.categories["output"] +  self.name_toolbox + """ += '  </category>';\n"""
        inputs = self.__add_category("Set event triggers",self.color_inputs ) + self.categories["input"] +  self.name_toolbox + """ += '  </category>';\n"""

        return outputs, inputs


class blockly_files:
    """
        Write and save the javascript files needed to define a blockly enviroment

        Parameters
        ----------

        name_file: string
            name of the blockly files that will be generated (block definition and code generator)
    """

    def __init__(self, name_file, path_, color_input = "#009688" , color_output = "#2196f3"):

         # -------------- Set folder paths ---------------
        self.path_developer = path_ + "/developer"
        self.path_blockly = path_+ "/blockly"
        self.path_databases = self.path_developer + "/databases"
        self.path_toolbox = path_+ "/toolbox"
        
        # -------------- Files to configurate ---------------
        # Toolbox name
        self.name_toolbox = "toolbox"
        # Blocks files
        self.file_b = open(self.path_blockly + "/blocks/" + name_file + ".js","w")
        # Generator files
        self.file_g = open(self.path_blockly + "/generators/python/" + name_file + ".js","w")
        # Toolbox file input
        self.file_input = open(  self.path_toolbox + "/blocks_inputs.js","w") 
        # Toolbox file ouput
        self.file_output = open(  self.path_toolbox + "/blocks_outputs.js","w") 
        self.database={}

        # --------------- Definition of primitives ------------
        # Define start of blocks file
        blocks_init = "goog.provide('Blockly.Blocks." + name_file + "');\ngoog.require('Blockly.Blocks');\n"
        # Define start of generator file
        generator_init = "'use strict'\ngoog.provide('Blockly.Python."+ name_file +"');\ngoog.require('Blockly.Python');"
        
        self.file_b.write(blocks_init)
        self.file_g.write(generator_init)

        # Define toobox creator file
        self.toolbox = toolbox_creator(self.name_toolbox, color_input, color_output)


    def add_code_generator(self,code):
        """ Add the code that will be generated the a block
        
            Parameters
            ----------

            code:string
                javascript and python code to be added
        """
        self.file_g.write("\n\n") 
        self.file_g.write(code)

        
    def add_block_definition(self,block):
        """ Add the javascript block definition
        
            Parameters
            ----------

            block:string
                javascript that define the design, inputs and outputs of a block
        """

        self.file_b.write("\n\n") 
        self.file_b.write(block)

    def add_toolbox_xml(self,name,block_type):
        """ This function add a new block description to a XML file that define the blockly toolbox.
        """
        self.toolbox.add_xml_block(name,block_type)

    def add_database(self, name_file, data):
        """ Add database values for each primitive
        
            Parameters
            ----------

            name_file: string
                Name of the file that describes the primitive

            data:dictionary
                dictionary with the description of the primitive
        """

        self.database[name_file] = data        

    def close_files(self):
        """ This function close the files created, code generators, toolbox and blocks.
        """
       
        out, inp = self.toolbox.get_blocks()
        self.file_output.write(out)
        self.file_input.write(inp)
        self.file_output.close()
        self.file_input.close()
        
        self.file_b.close()
        self.file_g.close()
        rize.saveJSON(self.path_databases, "primitives", self.database)
        


class block_creator:
    def __init__(self, block_name, description):
        """
            Class used to create JavaScript definitions of primitives blocks

            Parameters
            ----------
            block_name : string
                Name of the behavioral block
            
            block_description : dictionary
                User-friendly description of what the block will do 
        """
        
        # New line string definition
        self.new_line = "\n"

        # Get block info
        self.block_name = block_name
        self.block_description = description

        # Set initial and final JavaScript code.
        self.init = 'Blockly.Blocks["'+ self.block_name + '"] = {' + self.new_line + 'init: function() {' + self.new_line
        self.final =  '\n\tthis.setTooltip("'+ str(self.block_description) + '");' + self.new_line + ' \tthis.setHelpUrl("");' + self.new_line + '}};'

        # Fields of the block 
        self.fields = ""

        # Counter: Number of inputs
        self.inp_num = 0


    def code_generator(self, block_name, options):
        """ Default code generator for primitive blocks.

        Parameters
        ----------

        block_name : string
            Primitive/Block name
            
        options: bool
            True is primitive requires additional parameters

        """
        self.new_line = "\n"
        self.init = "Blockly.Python['" + str(block_name) + "'] = function(block) {" + self.new_line
        self.text_input = ""
        self.block_input = ""
        self.code_value = ""
        self.final = ""
        
        self.text_input = "var text = block.getFieldValue('inp_1');" + self.new_line
        option_feld = ""
        
        if options:
            self.text_input = self.text_input + "var options_dic = block.getFieldValue('inp_2');" + self.new_line
            self.text_input  = self.text_input + 'options_dic = rize.formatOptions(options_dic) '  + self.new_line 
            option_feld = """'"options":' + options_dic + '}';"""

        else:
            option_feld = """'"options":"none"}';"""

        coma = '+","+' 
        dictionary_start =   "var code  = '{"
        primitive_field = '"primitive":"' +  str(block_name) + '"' + "'"
        input_field = """ '"input":' + '"' + text + '"'"""
        self.code_value = dictionary_start + primitive_field + coma + input_field + coma + option_feld + self.new_line
        self.final = "return [code, Blockly.Python.ORDER_NONE];"

        return self.init + self.text_input +  self.block_input + self.code_value +  self.final + self.new_line + "};"


    def set_input(self, input_type):
        """ Add a new input region to the block

            Parameters
            ----------
            input_type : string
                Type of input that will be added. It can be "dummy_input" or "value_input"

            Returns
            ----------
            
            block_input : string
                Block input JavaScript code
        """
        
        if input_type == "dummy_input":
            block_input = '\tthis.appendDummyInput()' + self.new_line
        if input_type == "value_input":
            block_input = '\tthis.appendValueInput("block_input")' + self.new_line + '\t\t.setCheck("primitive")' + self.new_line
        return block_input   

    def add_dropdown_field(self,name):

        """ Add a new dropdown field to the block

            Parameters
            ----------
            name : string
                Name of the global variable thta have the option of the dropdown

            Returns
            ----------
            
            block_input : string
                Block input JavaScript code
        """

                
        value = '\t\t.appendField(new Blockly.FieldDropdown(input_' + name + '["options"]), "drop_input" )' + self.new_line
        self.fields = self.fields +  value
                
        
        
    def add_text_field(self,text):
        """
            Add a text field (Label) to the block. The user can not change this label.

            Parameters
            ----------
            text : string
                Text to add to the field

        """
        value = '\t\t.appendField("' + text + '")' + self.new_line
        self.fields = self.fields +  value

    def add_configuration_image(self):
        """
        Add button image which executes the function edit_primitive Javascript function (form-based interface for edit primitives).
        """
        value = '\t\t.appendField(new Blockly.FieldImage(configuration_image, 16, 16, "*", edit_primitive))'
        self.fields = self.fields +  value 

    def add_text_input_field(self, default_text = "edit"):
        """
            Add a textbox field, which user can fill.

            Parameters
            ----------
            default_text : string
                Default text shown in the input 

        """
        self.inp_num = self.inp_num + 1
        value ='\t\t.appendField(new Blockly.FieldTextInput("' + str(default_text) + '"), "inp_' + str(self.inp_num)+ '")' +  self.new_line
        self.fields = self.fields +  value

    def get_fields(self):
        """ Return all fields definitions
        """
        if self.fields != "":
            value =  self.fields + "\t\t;" + self.new_line
        return value


    def set_block_configuration(self, block_color , connections, allowed_types =  ["primitive", "statement", "behavior"] ):
        """
            Define the block configuration zone (color of the block, outputs and allowed connections types)

            Parameters
            ----------
            color : int
                color value
                
            connection : string
                connection type of the block, can be "top_down" or "left"

            allowed_types: list of strings
                this parameter defines which blocks inputs/outputs types can be connected this block

        """

        color = '\tthis.setColour(' + str(block_color) + ');'+ self.new_line

        if (connections == "top_down"):
            connection = '\tthis.setPreviousStatement(true,' + str(allowed_types) +');' + self.new_line + '\tthis.setNextStatement(true, null);' + self.new_line
        elif (connections == "left"):
            connection = '\tthis.setOutput(true,'+ str(allowed_types) +');' + self.new_line

        conf_zone = color + connection
        return conf_zone
