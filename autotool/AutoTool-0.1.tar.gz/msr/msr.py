# this module will be imported in the into your flowgraph
import vxi11, time

def msr(msr_chb, ip_param, tx_gain):
    if msr_chb == False:
        return 0
    else:
        instr = vxi11.Instrument(ip_param)
        if not instr.ask("*IDN?"):
            print("Measurement connection error!")
        else:
            tx_gain_file = open(str(tx_gain)+".txt", 'w')
            OCBW = open("OCBW.txt", 'w')

            OCBW.write(str(tx_gain) + "\t\t" + "Channel Power" + "\t" + "Total Power" +"\n")
            print("Calculating. . .")
            
            CHP = instr.ask(":CALC:OCBW:CHP?")
            POW = instr.ask(":CALC:OCBW:POW?")
            time.sleep(2)
            print(CHP + '\t' + POW)

            OCBW.write(str(tx_gain) + "\t\t\t" + CHP + "\t\t" + POW + "\n")
            instr.write(':MMEM:STOR:SCR ' + str(tx_gain) + '.jpg', encoding='utf-8')
            tx_gain_file.write(str(tx_gain) + '\n')

            instr.close()
            OCBW.close()
            print("Measurement is done")
        return 1
