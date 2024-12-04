import csv
import re
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from Webtote.models import (
    Customer, DeliveryInformation, Discount, PaymentMethod, ShipmentMethod,
    ShipmentStatus, PaymentStatus, Order, ProductCategory, Product, Cart,
    CartItems, ProductImage, OrderDetail, ReviewProduct )


class Command(BaseCommand):
    help = 'Import data from WebforSale.csv into Django models.'

    @staticmethod
    def row_to_dict(row, header):
        if len(row) < len(header):
            row += [''] * (len(header) - len(row))
        return dict([(header[i], row[i]) for i, head in enumerate(header) if head])

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['csv']

        m = re.compile(r'content: (\w+)')
        header = None
        models = dict()
        try:
            with open(file_path) as csvfile:
                model_data = csv.reader(csvfile)
                for i, row in enumerate(model_data):
                    if max([len(cell.strip()) for cell in row[1:] + ['']]) == 0 and m.match(row[0]):
                        model_name = m.match(row[0]).groups()[0]
                        models[model_name] = []
                        header = None
                        continue

                    if header is None:
                        header = row
                        continue

                    row_dict = self.row_to_dict(row, header)
                    if set(row_dict.values()) == {''}:
                        continue
                    models[model_name].append(row_dict)

        except FileNotFoundError:
            raise CommandError('File "{}" does not exist'.format(options['csv']))

        total = 0
        created_num = 0
        for row in models.get('Category', []):
            total += 1
            c = ProductCategory.objects.create(
                Category_Name=row['Category_Name']
            )

            if c:
                created_num += 1
                print(f'Created Category: {c.Category_Name}')

        print(f'Category: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('Product', []):
            total += 1
            category = ProductCategory.objects.get(id=row['Category'])
            p = Product.objects.create(
                Product_Name=row['Product_Name'],
                Description=row['Description'],
                Unit_Price=row['Unit_price'],
                Date_Edited=timezone.now().date(),
                Date_Created=timezone.now().date(),
                Quantity=row['Quantity'],
                Category=category,
                Color=row['Color']
            )

            if p:
                created_num += 1
                print(f'Created Product: {p.Product_Name}')

        print(f'Product: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('Discount', []):
            total += 1
            d = Discount.objects.create(
                Discount_Code=row['Discount_Code'],
                Discount_Value=row['Discount_Value'],
                Start_Date=row['Start_Date'],
                End_Date=row['End_Date'],
                Description=row['Description']
            )

            if d:
                created_num += 1
                print(f'Created Discount: {d.Discount_Code}')

        print(f'Discount: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('ProductImage', []):
            total += 1
            product = Product.objects.get(id=row['Product'])
            pi = ProductImage.objects.create(
                Is_Primary=row['Is_Primary'] == "TRUE",
                Image_Url=row['Image_Url'],
                Alt_Text=row['Alt_Text'],
                Product=product
            )

            if pi:
                created_num += 1
                print(f'Created ProductImage: {pi.Alt_Text}')

        print(f'ProductImage: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('Customer', []):
            total += 1
            c = Customer.objects.create(
                Name=row['Name'],
                UserName=row['UserName'],
                Password=row['Password'],
                Email=row['Email']
            )

            if c:
                created_num += 1
                print(f'Created Customer: {c.Name}')

        print(f'Customer: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('PaymentStatus', []):
            total += 1
            ps = PaymentStatus.objects.create(
                Payment_Status=row['Payment_Status']
            )

            if ps:
                created_num += 1
                print(f'Created PaymentStatus: {ps.Payment_Status}')

        print(f'PaymentStatus: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('ShipmentStatus', []):
            total += 1
            ss = ShipmentStatus.objects.create(
                Tracking_Number=row['Tracking_Number'],
                Shipment_Status=row['Shipment_Status']
            )

            if ss:
                created_num += 1
                print(f'Created ShipmentStatus: {ss.Shipment_Status}')

        print(f'ShipmentStatus: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('PaymentMethod', []):
            total += 1
            pm =  PaymentMethod.objects.create(
                Method_Name=row['Method_Name']
            )

            if pm:
                created_num += 1
                print(f'Created PaymentMethod: {pm.Method_Name}')

        print(f'PaymentMethod: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('ShipmentMethod', []):
            total += 1
            sm = ShipmentMethod.objects.create(
                Method_Name=row['Method_Name'],
                Method_Cost=row['Method_Cost'],
                Expected_Date=row['Expected_Date']
            )

            if sm:
                created_num += 1
                print(f'Created ShipmentMethod: {sm.Method_Name}')

        print(f'ShipmentMethod: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('DeliveryInformation', []):
            total += 1
            customer = Customer.objects.get(id=row['Customer'])
            di = DeliveryInformation.objects.create(
                Name=row['Name'],
                Phone_Number=row['Phone_Number'],
                Address=row['Address'],
                Customer=customer
            )

            if di:
                created_num += 1
                print(f'Created DeliveryInformation: {di.Name}')

        print(f'DeliveryInformation: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('Cart', []):
            total += 1
            customer = Customer.objects.get(id=row['User'])
            c = Cart.objects.create(
                User=customer,
                Create_at=row['Created_at'],
                Updated_at=row['Updated_at']
            )

            if c:
                created_num += 1
                print(f'Created Cart')

        print(f'Cart: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('CartItems', []):
            total += 1
            cart = Cart.objects.get(id=row['Cart'])
            product = Product.objects.get(id=row['Product'])
            ci = CartItems.objects.create(
                Cart=cart,
                Product=product,
                Quantity=row['Quantity'],
                Subtotal=int(row['Quantity']) * product.Unit_Price
            )

            if ci:
                created_num += 1
                print(f'Created CartItems')

        print(f'CartItems: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('Order', []):
            total += 1
            customer = Customer.objects.get(id=row['Customer'])
            discount = Discount.objects.get(id=row['Discount']) if row['Discount'] else None
            payment_method = PaymentMethod.objects.get(id=row['Payment_Method']) if row[
                'Payment_Method'] else None
            shipment_method = ShipmentMethod.objects.get(id=row['Shipment_Method']) if row[
                'Shipment_Method'] else None
            payment_status = PaymentStatus.objects.get(pk=row['Payment_Status']) if row[
                'Payment_Status'] else None
            delivery_info = DeliveryInformation.objects.get(id=row['Delivery_Infor']) if row[
                'Delivery_Infor'] else None

            order_id = row['Order_ID']

            print(row['Order_Date'])
            print(row['Time_Refund_Money'])
            o = Order.objects.create(
                Order_ID=order_id,
                Order_Date=row['Order_Date'],
                Order_Status=row['Order_Status'],
                Total_Price=0,
                Discount=discount,
                Payment_Method=payment_method,
                Shipment_Method=shipment_method,
                Shipment_Status=ShipmentStatus.objects.get(pk=row['Shipment_Status']) if row['Shipment_Status'] else None,
                Payment_Status=payment_status,
                Delivery_Infor=delivery_info,
                Reason=row['Reason'],
                Refund_Date=row['Refund_Date_Product'] if row['Refund_Date_Product'] else None,
                Time_Refund_Money=row['Time_Refund_Money'] if row['Time_Refund_Money'] else None,
                Customer=customer,
            )

            if o:
                created_num += 1
                print(f'Created Order: {o.Order_ID}')

        print(f'Order: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('OrderDetail', []):
            total += 1
            order = Order.objects.get(pk=row['Order'])
            product = Product.objects.get(id=row['Product'])
            od = OrderDetail.objects.create(
                Order=order,
                Product=product,
                Quantity=row['Quantity'],
                Subtotal=int(row['Quantity']) * product.Unit_Price
            )

            if od:
                created_num += 1
                print(f'Created OrderDetail')

        print(f'OrderDetail: {created_num} / {total}')
        print('---------')
        total = 0
        created_num = 0

        for row in models.get('ReviewProduct', []):
            total += 1
            order_detail = OrderDetail.objects.get(id=row['OrderDetail_ID'])
            rp = ReviewProduct.objects.create(
                Rating=row['Rating'],
                Content=row['Content'],
                Date_Created=row['Date_Created'] if row['Date_Created'] else timezone.now().date(),
                Date_Edited=row['Date_Edited'] if row['Date_Edited'] else None,
                Order_Detail=order_detail
            )

            if rp:
                created_num += 1
                print(f'Created ReviewProducts')

        print(f'ReviewProduct: {created_num} / {total}')
        print('---------')

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
