#!/usr/bin/env python

import os
from ctypes import CDLL, c_int, byref, create_string_buffer
from io import BytesIO
import base64
import click
from PIL import Image, ImageDraw


def build_barcode(fcc_value, dpid_value, customer_value=None):
    """
    Builds a barcode, type will be determined by the fcc_value.

    :param fcc_value:
    :param dpid_value:
    :param customer_value
    :return:
    """
    fcc_values = ['11', '59', '62']
    if str(fcc_value) not in fcc_values:
        raise ValueError(f'fcc [{fcc_value}] is not a supported australia post fcc type.')
    if len(str(dpid_value)) != 8:
        raise ValueError(f'fcc [{len(dpid_value)}] must be 8 character long and must be a number.')
    aus_post = CDLL(os.path.join(os.path.dirname(__file__), 'auspost.so'))
    result = create_string_buffer(b'\000' * 67)
    fcc = create_string_buffer(b'\000' * 2)
    fcc.value = fcc_value.encode('utf-8')
    dpid = create_string_buffer(b'\000' * 8)
    dpid.value = str(dpid_value).encode('utf-8')
    customer = create_string_buffer(b'\000' * 10)
    if customer_value is not None:
        customer.value = str(customer_value).encode('utf-8')
    length = c_int()
    aus_post.BuildBarcode(fcc, dpid, customer_value, result, byref(length))
    return result.value.decode('utf-8')


def write_barcode_to_image(barcode):
    """
    Writes out the barcode to a file.

    :param barcode:
    :param out_file:
    :param kwargs:
    :return:
    """
    h_padding = 20
    x_padding = 60
    tad_height = 42
    bar_width = 5
    bar_qty = len(barcode)
    total_height = h_padding * 2 + tad_height
    total_width = x_padding * 2 + bar_width * 2 * bar_qty
    img = Image.new('RGB', (total_width, total_height), color='white')
    d = ImageDraw.Draw(img)
    for i in range(0, bar_qty):
        h_start = x_padding + i * bar_width * 2
        line_types = {
            '0': (0, 0),
            '1': (0, 16),
            '2': (16, 0),
            '3': (16, 16)
        }
        offset_t, offset_b = line_types.get(barcode[i])
        d.line(
            (h_start, h_padding + offset_t) + (h_start, total_height - h_padding - offset_b),
            fill=256,
            width=bar_width
        )
    return img


def write_barcode_to_image_file(barcode, out_file, **kwargs):
    """
    writes out barcode to image file.

    :param barcode:
    :param out_file:
    :param kwargs:
    :return:
    """
    img = write_barcode_to_image(barcode)
    img.save(out_file, **kwargs)


def write_barcode_to_image_base64(barcode):
    """
    writes out barcode to base64 string.

    :param barcode:
    :return:
    """
    img = write_barcode_to_image(barcode)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())


@click.command()
@click.option('--fcc', prompt="Enter the FCC code", type=click.Choice(['11', '59', '62']), required=True)
@click.option('--dpid', prompt="Enter the DPID value", required=True, type=click.IntRange(10000000, 99999999))
@click.option('--cust-no', prompt="Enter the customer value if required", default='')
@click.option('--save-to', prompt="Save the image location and name", required=True)
def write_image(fcc, dpid, cust_no, save_to):
    barcode = build_barcode(fcc, dpid, cust_no)
    write_barcode_to_image_file(barcode, save_to, dpi=(300, 300))


if __name__ == '__main__':
    write_image()