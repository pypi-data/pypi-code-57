"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

SmartFabric functions for Tile Grid configuration
"""

import os, ntpath
from chipbuilder.smartfabric.host import SF_Host
from chipbuilder.smartfabric.util import log_performance
from chipbuilder.smartfabric.util import IS_CLI_CMD, OPEN_HOST_ATTR


COMPARE_TG_FINAME  = "route_compare.log"


class SF_TileGrid(SF_Host):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


    def init(self):
        """
        Initialize the Smart Fabric. Run this command first before any register programming
        commands are used. However, ``init()`` is not required for OTP programming/scanning. 
        Function does nothing if already initialized. This function is supported on the CLI script.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_init_tg()
        
        return ret


    def chipid(self):
        """
        Scan ZIP's chip chipID. 
        This function is supported on the CLI script.

        Returns:
            list. List of ints with the ZIP's chip chipID from MSB to LSB.
        """

        chipId = self._zip_read_chipid()
        chipIdStr = ["%04x" % idx for idx in chipId]
        sysVer = 0xff & chipId[1]
        sysNum = (chipId[0] << 8) | (chipId[1] >> 8)
        # print("CHIP_ID: 0x%s" % " ".join(chipIdStr))
        print("ChipBuilder system: %d" % sysNum)
        print("System version: %d" % sysVer)
        print("ZIP ID: %d" % chipId[3])
        
        return chipId


    #########################
    ###    TILE ACCESS    ###   
    #########################

    def tile_read(self, row:int, col:int):
        """
        Read from specific tile. 
        This function is supported on the CLI script.

        Args:
            row (int): Row index of specific tile (0 - 63).
            col (int): Col index of specific tile (0 - 43).

        Returns:
            int. The tile's register value.
        """

        mmdrVal = self._zip_read_tile(row, col)
        print("tile@ row:%d,col:%d,data:0x%x" % (row, col, mmdrVal))
        
        return mmdrVal


    def tile_write(self, row:int, col:int, data:int):
        """
        Write to specific tile. 
        This function is supported on the CLI script.

        Args:
            row (int): Row index of specific tile (0 - 63).
            col (int): Col index of specific tile (0 - 43).
            data (int): 16b data to write.

        Returns:
            int. The tile's register value.
        """

        self._zip_write_tile(row, col, data)
        mmdrVal = self.tile_read(row, col)
        if data == mmdrVal:
            print("Success!")

        return mmdrVal


    @log_performance
    def tile_clear(self):
        """
        Clear ZIP's tile grid registers. 
        This function is supported on the CLI script.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_clear_tiles()
        print("Cleared tile grid")

        return ret


    #########################
    ###   TILE IO ACCESS  ###   
    #########################

    def tileio_read(self, side:int, row:int):
        """
        Read from specific tile IO. 
        This function is supported on the CLI script.

        Args:
            side (int): Tile IO bank side (left=1, right=2).
            row (int): Row index of specific tile IO (0 - 63).

        Returns:
            int. The tile IO's register value.
        """

        mmdrVal = self._zip_read_tileio(side, row)
        print("tileio@ side:%d,row:%d,data:0x%x" % (side, row, mmdrVal))
        
        return mmdrVal


    def tileio_write(self, side:int, row:int, data:int):
        """
        Write to specific tile IO. 
        This function is supported on the CLI script.

        Args:
            side (int): Tile IO bank side (left=1, right=2).
            row (int): Row index of specific tile IO (0 - 63).
            data (int): 16b data to write.

        Returns:
            int. The tile IO's register value after writting.
        """

        self._zip_write_tileio(side, row, data)
        mmdrVal = self.tileio_read(side, row)
        if data == mmdrVal:
            print("Success!")

        return mmdrVal


    @log_performance
    def tileio_clear(self):
        """
        Clear ZIP's tile IO registers. 
        This function is supported on the CLI script.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_clear_tio()
        print("Cleared tile IOs")

        return ret


    #########################
    ###    VRAIL ACCESS   ###   
    #########################

    def vrail_read(self, side:int, index:int):
        """
        Read from specific Vrail switch from zGlue's ZIP. 
        This function is supported on the CLI script.
        
        Args:
            side (int): Vrail bank side (left=1, right=2).
            index (int): Index of specific Vrail switch (0 - 15).

        Returns:
            int. The Vrail's register value.
        """

        mmdrVal = self._zip_read_vrail(side, index)
        print("vrail@ side:%d,index:%d,data:0x%x" % (side, index, mmdrVal))
        
        return mmdrVal


    def vrail_write(self, side:int, index:int, data:int):
        """
        Write to specific Vrail switch of zGlue's ZIP.
        This function is supported on the CLI script.

        Args:
            side (int): Vrail bank side (left=1, right=2).
            index (int): Index of specific Vrail switch (0 - 15).
            data (int): 16b data to write.

        Returns:
            int. The Vrail's register value after writting.
        """

        self._zip_write_vrail(side, index, data)
        mmdrVal = self.vrail_read(side, index)
        if data == mmdrVal:
            print("Success!")

        return mmdrVal


    @log_performance
    def vrail_clear(self):
        """
        Clear zGlue's ZIP VRAIL registers. 
        This function is supported on the CLI script.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_clear_vrail()
        print("Cleared vrails")

        return ret


    #########################
    ###    BATCH ACCESS   ###   
    #########################

    @log_performance
    def reg_program(self, rFiName:str):
        """
        Program a routing file to zGlue's ZIP. 
        This function is supported on the CLI script.

        Args:
            rFiName (str): Input routing file name.
                To download a routing file for your specific ZIP, 
                click ``Menu > Outputs > Routing`` on that system's ChipBuilder page.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_route(rFiName)

        return ret


    @log_performance
    def reg_compare(self, rFiName:str, oFiName:str = None):
        """
        Compare a routing file with the current ZIP programming.
        The differences will be saved in the file specified by oFiName.
        If ``None`` is passed, the file ``route_compare.log`` will be saved in the current working directory.
        This function is supported on the CLI script.

        Args:
            rFiName (str): Input routing file name to compare.
                To download a routing file for your specific ZIP, 
                click ``Menu > Outputs > Routing`` on that system's ChipBuilder page.
            oFiName (str, optional): Output file with programming differences.

        Returns:
            dict. Dictionary showing routing differences::

                {
                    addr:{
                        'expected':val,
                        'actual':val
                    }
                }

        """

        if oFiName == None:
            oFiName = COMPARE_TG_FINAME

        # Filter repeated addresses
        routeDataFiltered = []
        fiPath = os.path.dirname(rFiName)
        fiName = ntpath.basename(rFiName).split(".")[0]
        tmpFiName = os.path.join(fiPath, fiName + "_tmp.txt")
        routeData = open(rFiName, "r").read().split("\n")
        # print(tmpFiName)

        for reg in routeData:
            addr = reg.split(",")[0]

            for regFiltered in routeDataFiltered:
                if addr in regFiltered:
                    # print("OUTDATED - %s" % regFiltered)
                    routeDataFiltered.remove(regFiltered)

            routeDataFiltered.append(reg)

        filteredFi = open(tmpFiName, "w")
        filteredFi.write("\n".join(routeDataFiltered))
        filteredFi.close()
        diff = self._zip_compare_route(tmpFiName, oFiName, sync=1)
        os.remove(tmpFiName)

        # for regAddr in diff.keys():
        #     regExp = diff[regAddr]["expected"]
        #     regVal = diff[regAddr]["actual"]
        #     print("addr:0x{0:x},exp:0x{1:x},val:0x{2:x}".format(regAddr, regExp, regVal))

        if len(diff) == 0:
            print("ZIP Programming matches routing file")
        else:
            print("%d differences found in: %s" % (len(diff), oFiName))

        return diff


    @log_performance
    def tgrid_clear(self):
        """
        Clear all of SmartFabric's routing register space.
        This function is supported on the CLI script.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_clear_tiles()
        ret |= self._zip_clear_tio()
        ret |= self._zip_clear_vrail()
        print("Cleared all")

        return ret


    setattr(init, IS_CLI_CMD, True)
    setattr(chipid, IS_CLI_CMD, True)
    setattr(tile_read, IS_CLI_CMD, True)
    setattr(tile_write, IS_CLI_CMD, True)
    setattr(tile_clear, IS_CLI_CMD, True)
    setattr(tileio_read, IS_CLI_CMD, True)
    setattr(tileio_write, IS_CLI_CMD, True)
    setattr(tileio_clear, IS_CLI_CMD, True)
    setattr(vrail_read, IS_CLI_CMD, True)
    setattr(vrail_write, IS_CLI_CMD, True)
    setattr(vrail_clear, IS_CLI_CMD, True)
    setattr(reg_program, IS_CLI_CMD, True)
    setattr(reg_compare, IS_CLI_CMD, True)
    setattr(tgrid_clear, IS_CLI_CMD, True)

    setattr(init, OPEN_HOST_ATTR, True)
    setattr(chipid, OPEN_HOST_ATTR, True)
    setattr(tile_read, OPEN_HOST_ATTR, True)
    setattr(tile_write, OPEN_HOST_ATTR, True)
    setattr(tile_clear, OPEN_HOST_ATTR, True)
    setattr(tileio_read, OPEN_HOST_ATTR, True)
    setattr(tileio_write, OPEN_HOST_ATTR, True)
    setattr(tileio_clear, OPEN_HOST_ATTR, True)
    setattr(vrail_read, OPEN_HOST_ATTR, True)
    setattr(vrail_write, OPEN_HOST_ATTR, True)
    setattr(vrail_clear, OPEN_HOST_ATTR, True)
    setattr(reg_program, OPEN_HOST_ATTR, True)
    setattr(reg_compare, OPEN_HOST_ATTR, True)
    setattr(tgrid_clear, OPEN_HOST_ATTR, True)

