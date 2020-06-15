# this module will be imported in the into your flowgraph
def copy_data(get_scr_chb, ip_param):
    if get_scr_chb == False:
        return 0
    else:
        instr = vxi11.Instrument(ip_param)
        instr.write(':MMEM:CDIR LOCAL', encoding='utf-8')
        instr.write(':MMEM:DEST USB', encoding='utf-8')
        tx_gain_file = open("tx_gain.txt", 'r')
        for line in tx_gain_file:
            instr.write(':MMEM:COPY ' + str(line) + '.txt', encoding='utf-8')
        instr.close()
        tx_gain_file.close()
        return 1
        
