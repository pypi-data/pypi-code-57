# this module will be imported in the into your flowgraph
import vxi11, time
def config(config_chb, ip_param, params):
    messages = {
        ':CALC:OCBW:STAT ON',
        ':FREQ:CENT' + params['CFREQ'],
        ':FREQ:SPAN' + params['SPAN'],
        ':OCBW:BAND' + params['OCBW_BAND'],
        ':OCBW:PERC' + params['OCBW_PERC'],
        ':OCBW:SPAC' + params['OCBW_SPACE'],
        }
    if config_chb == False:
        return 0
    else:
        instr =  vxi11.Instrument(ip_param)
        if not instr.ask("*IDN?"):
            print("Configurating connection error!")
        else:
            print("Configurating . . .")
            for mes in messages:
                instr.write(mes, encoding='utf-8')
                time.sleep(1)
            instr.close()
            print("Configurating is done")
            return 1
            
