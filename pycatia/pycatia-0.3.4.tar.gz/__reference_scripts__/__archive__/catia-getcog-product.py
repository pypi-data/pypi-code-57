import csv
import datetime
from win32com.client import Dispatch

cat_script_language = 1


def write_csv(csv_data, csv_name):

    with open(csv_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['instance name', 'body name', 'cog x', 'cog y', 'cog z'])
        for row in csv_data:
            csv_writer.writerow([row[0], row[1], row[2][0], row[2][1], row[2][2]])


def convert_to_imperial(__input__, decimal_places=4):
    # takes a list() or tuple of int()s and converts to inches.
    # it is assumed the input is millimeters.
    output = list()
    for item in __input__:
        item = item / 25.4
        item = round(item, decimal_places)
        output.append(item)
    return output


def is_product(product):
    """

    :param product:
    :return:
    """
    name = product.ReferenceProduct.Parent.Name
    try:
        if '.CATProduct' in name:
            return True
    except:
        return False


def get_bodies(part):
    bodies = part.Bodies

    bodies_list = list()

    for i in range(0, bodies.Count):
        body = bodies.Item(i + 1)
        bodies_list.append(body)

    return bodies


def create_measurable_from_body(document, part, body):
    """

    :param document:
    :param part:
    :param body:
    :return:  'Measurable' COM object
    """

    spa_workbench = document.GetWorkbench("SPAWorkbench")
    reference = part.CreateReferenceFromObject(body)
    measurable = spa_workbench.GetMeasurable(reference)

    return measurable


def run_system_service(measurable, cat_script_language):
    """

    :param measurable:
    :return:
    """
    centre_of_gravity_metric = Dispatch('CATIA.Application').SystemService.Evaluate(
        centre_of_gravity_vba_code(),
        cat_script_language,
        "create_cog",
        [measurable]
    )

    return centre_of_gravity_metric


def centre_of_gravity_vba_code():
    """

    :return:
    """
    return '''
        Public Function create_cog(measurable)
            Dim coord(2)
            measurable.GetCOG coord
            create_cog = coord
        End Function
        '''


def get_products(product, document, csv_data):
    num_products = product.Products.Count
    for i in range(0, num_products):

        current_product = product.Products.Item(i + 1)
        print(f'Scanning ... {current_product.Name}')

        bodies = list()
        part = None

        if is_product(current_product):
            get_products(current_product, document, csv_data)
        else:
            part = current_product.GetMasterShapeRepresentation(True).Part
            bodies = get_bodies(part)

        if len(bodies) > 0 and part:

            for body in bodies:

                centre_of_gravity = (0,0,0)

                body_name = body.name
                do_not_measure = False

                if 'CAGE' not in body_name:
                    body_name = None
                    do_not_measure = True

                if body.Shapes.Count > 0 and not do_not_measure:

                    measurable = create_measurable_from_body(document, part, body)
                    centre_of_gravity = run_system_service(measurable, cat_script_language)
                    centre_of_gravity = convert_to_imperial(centre_of_gravity, decimal_places=4)

                if body_name:
                    csv_data.append([current_product.Name, body_name, centre_of_gravity])

    return csv_data


if __name__ == '__main__':
    CATIA = Dispatch('CATIA.Application')
    document = CATIA.ActiveDocument
    product = document.Product

    print('\n** Product must be in design mode. **')
    # puts product in design mode.
    # product.ApplyWorkMode(0)
    csv_data = list()
    csv_data = get_products(product, document, csv_data)

    csv_name = product.Name + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv'
    print(f'\n** Writing CSV {csv_name}. **')
    write_csv(csv_data, csv_name)
