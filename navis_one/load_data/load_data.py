import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadData:
    def __init__(self):
        session = Session()
        session.auth = HTTPBasicAuth('Robot', 'Robot')
        transport = Transport(session=session, timeout=600)
        settings = Settings(xml_huge_tree=True)
        self.client = Client('http://192.168.75.45/live/ws/navis_hort?wsdl', transport=transport,
                             settings=settings)

        self.conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="navis_one",
            user="torsion_prog",
            password="sdr%7ujK")

    def load_products(self):
        products = self.client.service.GetData('products_navis')
        data = base64.b64decode(products)
        file = open('cache/products.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE navis_product_buffer (
            source_id character varying(300),
            source_commercial character varying(300),
            source_category character varying(300),
            name_ru character varying(500),
            name_uk character varying(500),
            name_en character varying(500),
            name_pl character varying(500),
            article character varying(300),
            specification character varying(300),
            advanced_description_ru text,
            advanced_description_uk text,  
            advanced_description_en text,
            advanced_description_pl text   );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/products.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'navis_product_buffer',
                          columns=(
                              'source_id', 'source_commercial', 'source_category', 'name_ru', 'name_uk', 'name_en', 'name_pl',
                              'article', 'specification', 'advanced_description_ru',
                              'advanced_description_uk', 'advanced_description_en',  'advanced_description_pl'),
                          sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO navis_product (source_id, slug)
        SELECT source_id, article FROM navis_product_buffer
        WHERE source_id NOT IN (SELECT source_id FROM navis_product WHERE source_id IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM navis_product
        WHERE source_id NOT IN (SELECT source_id FROM navis_product_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE navis_product p
            SET  
                source_commercial = b.source_commercial,
                source_category = b.source_category,         
                name_ru = b.name_ru,
                name_uk = b.name_uk,
                name_en = b.name_en,
                name_pl = b.name_pl,
                article = b.article,
                slug = b.article,
                specification = b.specification,
                advanced_description_ru = b.advanced_description_ru,
                advanced_description_uk = b.advanced_description_uk,
                advanced_description_en = b.advanced_description_en,
                advanced_description_pl = b.advanced_description_pl                                       
            FROM navis_product_buffer b
            WHERE p.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE navis_product p
                    SET category_id = c.id
                    FROM navis_category c
                    WHERE p.source_category = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE navis_product p
                    SET commercial_id = c.id
                    FROM navis_commercial c
                    WHERE p.source_commercial = c.source_commercial;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_cross(self):
        cross = self.client.service.GetData('cross_navis')
        data = base64.b64decode(cross)
        file = open('cache/cross.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE navis_cross_buffer (
            product character varying(300),
            brand character varying(300),                
            article_nr character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/cross.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'navis_cross_buffer',
                          columns=('product', 'brand', 'article_nr'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO navis_cross (product)
                SELECT product FROM navis_cross_buffer
                WHERE product NOT IN (SELECT product FROM navis_cross WHERE product IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM navis_cross
                WHERE product NOT IN (SELECT product FROM navis_cross_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE navis_cross p
            SET
                brand = b.brand,
                article_nr = b.article_nr                      
            FROM navis_cross_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE navis_cross s
            SET product_id_id = c.id                               
            FROM navis_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_description(self):
        description = self.client.service.GetData('description_navis')
        data = base64.b64decode(description)
        file = open('cache/description.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE navis_description_buffer (
            product character varying(300),
            property character varying(300), 
            value text );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/description.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'navis_description_buffer',
                          columns=('product', 'property', 'value'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO navis_description (product)
                        SELECT product FROM navis_description_buffer
                        WHERE product NOT IN (SELECT product FROM navis_description WHERE product IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM navis_description
                        WHERE product NOT IN (SELECT product FROM navis_description_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE navis_description p
            SET
                property = b.property,
                value = b.value                         
            FROM navis_description_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE navis_description d
            SET product_id_id = c.id                               
            FROM navis_product c
            WHERE d.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_applicability(self):
        applicability = self.client.service.GetData('applicability_navis')
        data = base64.b64decode(applicability)
        file = open('cache/applicability.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE navis_applicability_buffer (
            product character varying(300),
            vehicle character varying(300),
            modification character varying(300), 
            engine character varying(300), 
            year character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/applicability.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'navis_applicability_buffer',
                          columns=('product', 'vehicle', 'modification', 'engine', 'year'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO navis_applicability (product)
                        SELECT product FROM navis_applicability_buffer
                        WHERE product NOT IN (SELECT product FROM navis_applicability WHERE product IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM navis_applicability
                        WHERE product NOT IN (SELECT product FROM navis_applicability_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE navis_applicability p
            SET
                vehicle = b.vehicle,
                modification = b.modification,
                engine = b.engine,
                year = b.year                         
            FROM navis_applicability_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE navis_applicability a
            SET product_id_id = c.id                               
            FROM navis_product c
            WHERE a.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_product_images(self):
        product_images = self.client.service.GetData('product_images_navis')
        data = base64.b64decode(product_images)
        file = open('cache/product_images.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE navis_productimage_buffer (
                    source_product character varying(300),
                    image_url character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/product_images.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'navis_productimage_buffer',
                          columns=('source_product', 'image_url'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO navis_productimage (source_product)
                        SELECT source_product FROM navis_productimage_buffer
                        WHERE source_product NOT IN (SELECT source_product FROM navis_productimage 
                        WHERE source_product IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM navis_productimage
                        WHERE source_product NOT IN (SELECT source_product FROM navis_productimage_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE navis_productimage p
                    SET
                        image_url = b.image_url                         
                    FROM navis_productimage_buffer b
                    WHERE p.source_product = b.source_product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE navis_productimage a
                    SET product_id = c.id                               
                    FROM navis_product c
                    WHERE a.source_product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()


LoadData = LoadData()
LoadData.load_products()
print('Load Products')

LoadData.load_cross()
print('Load Cross')

LoadData.load_description()
print('Load Description')

LoadData.load_applicability()
print('Load Applicability')

LoadData.load_product_images()
print('Load Images')
