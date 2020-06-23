"""
Required device info for the AVR128DA48 device
"""
from pymcuprog.deviceinfo.eraseflags import ChiperaseEffect

DEVICE_INFO = {
    'name': 'avr128da48',
    'architecture': 'avr8x',

    # eeprom
    'eeprom_address_byte': 0x00001400,
    'eeprom_size_bytes': 0x200,
    'eeprom_page_size_bytes': 0x1,
    'eeprom_read_size_bytes': 1,
    'eeprom_write_size_bytes': 1,
    'eeprom_chiperase_effect': ChiperaseEffect.CONDITIONALLY_ERASED_AVR,
    'eeprom_isolated_erase': True,

    # fuses
    'fuses_address_byte': 0x00001050,
    'fuses_size_bytes': 0x10,
    'fuses_page_size_bytes': 0x1,
    'fuses_read_size_bytes': 1,
    'fuses_write_size_bytes': 1,
    'fuses_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'fuses_isolated_erase': False,

    # internal_sram
    'internal_sram_address_byte': 0x4000,
    'internal_sram_size_bytes': 0x4000,
    'internal_sram_page_size_bytes': 1,
    'internal_sram_read_size_bytes': 1,
    'internal_sram_write_size_bytes': 1,
    'internal_sram_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    'internal_sram_isolated_erase': False,

    # lockbits
    'lockbits_address_byte': 0x00001040,
    'lockbits_size_bytes': 0x4,
    'lockbits_page_size_bytes': 0x1,
    'lockbits_read_size_bytes': 1,
    'lockbits_write_size_bytes': 1,
    'lockbits_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    'lockbits_isolated_erase': False,

    # flash
    'flash_address_byte': 0x00800000,
    'flash_size_bytes': 0x20000,
    'flash_page_size_bytes': 0x200, # 0x200 is the erase size (0x100 words), write size is actually 1 word (2 bytes)
    'flash_read_size_bytes': 2,
    'flash_write_size_bytes': 2,
    'flash_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    # Separate flash erase is supported by the device but not by pymcuprog
    'flash_isolated_erase': False,

    # user_row - this architecture/variant implements this as FLASH
    'user_row_address_byte': 0x00001080,
    'user_row_size_bytes': 0x20,
    'user_row_page_size_bytes': 2,
    'user_row_read_size_bytes': 1,
    'user_row_write_size_bytes': 2,
    'user_row_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'user_row_isolated_erase': True,

    # signatures
    'signatures_address_byte': 0x00001100,
    'signatures_size_bytes': 0x80,
    'signatures_page_size_bytes': 2,
    'signatures_read_size_bytes': 1,
    'signatures_write_size_bytes': 0, # SIGNATURES can't be written
    'signatures_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'signatures_isolated_erase': False,

    # Some extra AVR specific fields
    'nvmctrl_base': 0x00001000,
    'syscfg_base': 0x00000F00,
    'ocd_base': 0x00000F80,
    'interface': 'UPDI',
    'prog_clock_khz': 1800,
    'device_id': 0x1E9708,
    'address_size': '24-bit'
}
