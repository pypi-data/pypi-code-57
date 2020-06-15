class MMT_Error_msg:
    # for motion file converter
    
    def sp_process(self):
        print("==========================================================")
        print("""
        Error method : [the sp_process]
        There is no flag that determines the data length.
        Add the following values to the csv file.
            - Device
            - Model Outputs
            - Trajectories
        """)
        print("==========================================================")


    # for MMT file converter

    def sp_process4MVC(self):
        print("==========================================================")
        print("""
        Error method : [the sp_process4MVC]
        There is no flag that determines the data length.
        Add the following values to the csv file.
            - Device 
            - Trajectories
            - Joints
            - Segments
        """)
        print("==========================================================")

