#!/usr/bin/env python3
# Copyright (c) 2018-2020 Phase Advanced Sensor Systems, Inc.
import psdb.probes

import argparse
import time
import sys


def main(rv):
    # Dump all debuggers if requested.
    if rv.dump_debuggers:
        for p in psdb.probes.PROBES:
            p.show_info()

    # Probe the specified serial number (or find the default if no serial number
    # was specified.
    probe = psdb.probes.find_default(usb_path=rv.usb_path)
    f     = probe.set_tck_freq(rv.probe_freq)
    print('Probing with SWD frequency at %.3f MHz' % (f/1.e6))

    # Use the probe to detect a target platform.
    target = probe.probe(verbose=rv.verbose, connect_under_reset=True)
    f      = target.set_max_tck_freq()
    print('Set SWD frequency to %.3f MHz' % (f/1.e6))

    # Find the RCC.
    rcc = target.devs['RCC']

    # Configure DMA0.0 to handle transfers from TIM17.1.
    rcc.enable_device('DMAMUX')
    rcc.enable_device('DMA1')
    dmamux = target.devs['DMAMUX']
    dma1   = target.devs['DMA1']
    tim17  = target.devs['TIM17']
    sram1  = target.devs['SRAM1']
    target.ahb_ap.write_bulk(b'\xAA'*sram1.size, sram1.dev_base)
    dmamux._C0CR = 84
    dma1._CCR1   = 0x00000A82
    dma1._CNDTR1 = 100
    dma1._CPAR1  = tim17._CCR1.addr
    dma1._CMAR1  = sram1.dev_base
    dma1._CCR1   = 0x00000A82 | 1

    # Enable HSE.
    rcc._CR.HSEON = 1
    while not rcc._CR.HSERDY:
        time.sleep(0.1)

    # Configure TIM17 to capture HSE/256 and trigger a DMA request each time.
    rcc.enable_device('TIM17')
    tim17._CR1            = 0
    tim17._OR1.HSE32EN    = 1  # Enable HSE/32 input
    tim17._TISEL.TI1SEL   = 3  # TI1 input is HSE/32
    tim17._CCMR1_I.CC1S   = 1  # CC1 in input capture mode
    tim17._CCMR1_I.IC1PSC = 3  # CC1 is TI1/8 == HSE/256
    tim17._DIER.CC1DE     = 1  # CC1 DMA request enabled
    tim17._ARR            = 0xFFFF
    tim17._CNT            = 0
    tim17._CR1            = 1
    tim17._CCER           = 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump-debuggers', '-d', action='store_true')
    parser.add_argument('--usb-path')
    parser.add_argument('--probe-freq', type=int, default=1000000)
    parser.add_argument('--verbose', '-v', action='store_true')
    rv = parser.parse_args()

    try:
        main(rv)
    except psdb.ProbeException as e:
        print(e)
        sys.exit(1)
