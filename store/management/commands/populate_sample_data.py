from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Populate the store with sample Apple products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample categories and products...'))

        # Create categories
        categories_data = [
            {
                'name': 'iPhone',
                'slug': 'iphone',
                'description': 'Революционные смартфоны Apple с передовыми технологиями'
            },
            {
                'name': 'iPad',
                'slug': 'ipad',
                'description': 'Планшеты Apple для работы, творчества и развлечений'
            },
            {
                'name': 'Mac',
                'slug': 'mac',
                'description': 'Мощные компьютеры и ноутбуки Apple для профессионалов'
            },
            {
                'name': 'Apple Watch',
                'slug': 'apple-watch',
                'description': 'Умные часы для здорового образа жизни'
            },
            {
                'name': 'AirPods',
                'slug': 'airpods',
                'description': 'Беспроводные наушники с превосходным качеством звука'
            },
            {
                'name': 'Аксессуары',
                'slug': 'accessories',
                'description': 'Оригинальные аксессуары Apple для ваших устройств'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # iPhone
            {
                'name': 'iPhone 15 Pro Max',
                'slug': 'iphone-15-pro-max',
                'category': 'iphone',
                'description': 'Самый продвинутый iPhone с титановым корпусом, чипом A17 Pro и потрясающей системой камер Pro.',
                'price': 129990,
                'availability': 'available',
                'featured': True,
                'specifications': {
                    'Экран': '6.7" Super Retina XDR',
                    'Чип': 'A17 Pro',
                    'Камера': 'Система Pro камер 48 Мп',
                    'Объем памяти': '128 ГБ',
                    'Цвет': 'Натуральный титан'
                }
            },
            {
                'name': 'iPhone 15',
                'slug': 'iphone-15',
                'category': 'iphone',
                'description': 'Новый iPhone 15 с инновационным дизайном, чипом A16 Bionic и улучшенной системой камер.',
                'price': 79990,
                'availability': 'available',
                'featured': True,
                'specifications': {
                    'Экран': '6.1" Super Retina XDR',
                    'Чип': 'A16 Bionic',
                    'Камера': 'Основная 48 Мп',
                    'Объем памяти': '128 ГБ',
                    'Цвет': 'Черный'
                }
            },
            {
                'name': 'iPhone 14',
                'slug': 'iphone-14',
                'category': 'iphone',
                'description': 'iPhone 14 с продвинутой системой камер и мощным чипом A15 Bionic.',
                'price': 69990,
                'availability': 'available',
                'featured': False,
                'specifications': {
                    'Экран': '6.1" Super Retina XDR',
                    'Чип': 'A15 Bionic',
                    'Камера': 'Основная 12 Мп',
                    'Объем памяти': '128 ГБ',
                    'Цвет': 'Синий'
                }
            },

            # iPad
            {
                'name': 'iPad Pro 12.9"',
                'slug': 'ipad-pro-12-9',
                'category': 'ipad',
                'description': 'Самый мощный iPad Pro с чипом M2, дисплеем Liquid Retina XDR и поддержкой Apple Pencil.',
                'price': 109990,
                'availability': 'available',
                'featured': True,
                'specifications': {
                    'Экран': '12.9" Liquid Retina XDR',
                    'Чип': 'Apple M2',
                    'Камера': 'Основная 12 Мп',
                    'Объем памяти': '128 ГБ',
                    'Подключение': 'Wi-Fi'
                }
            },
            {
                'name': 'iPad Air',
                'slug': 'ipad-air',
                'category': 'ipad',
                'description': 'Универсальный iPad Air с чипом M1 и потрясающим дисплеем Liquid Retina.',
                'price': 64990,
                'availability': 'available',
                'featured': False,
                'specifications': {
                    'Экран': '10.9" Liquid Retina',
                    'Чип': 'Apple M1',
                    'Камера': 'Основная 12 Мп',
                    'Объем памяти': '64 ГБ',
                    'Цвет': 'Голубой'
                }
            },

            # Mac
            {
                'name': 'MacBook Pro 14"',
                'slug': 'macbook-pro-14',
                'category': 'mac',
                'description': 'Профессиональный MacBook Pro с чипом M3 Pro, дисплеем Liquid Retina XDR и невероятной производительностью.',
                'price': 249990,
                'availability': 'available',
                'featured': True,
                'specifications': {
                    'Экран': '14.2" Liquid Retina XDR',
                    'Чип': 'Apple M3 Pro',
                    'Память': '18 ГБ объединенной памяти',
                    'Накопитель': 'SSD 512 ГБ',
                    'Цвет': 'Серый космос'
                }
            },
            {
                'name': 'MacBook Air M2',
                'slug': 'macbook-air-m2',
                'category': 'mac',
                'description': 'Невероятно тонкий и легкий MacBook Air с чипом M2 и дисплеем Liquid Retina.',
                'price': 134990,
                'availability': 'available',
                'featured': False,
                'specifications': {
                    'Экран': '13.6" Liquid Retina',
                    'Чип': 'Apple M2',
                    'Память': '8 ГБ объединенной памяти',
                    'Накопитель': 'SSD 256 ГБ',
                    'Цвет': 'Серебристый'
                }
            },

            # Apple Watch
            {
                'name': 'Apple Watch Series 9',
                'slug': 'apple-watch-series-9',
                'category': 'apple-watch',
                'description': 'Самые продвинутые Apple Watch с чипом S9, ярким дисплеем и расширенными функциями здоровья.',
                'price': 42990,
                'availability': 'available',
                'featured': True,
                'specifications': {
                    'Размер': '45 мм',
                    'Дисплей': 'Always-On Retina',
                    'Чип': 'S9 SiP',
                    'Датчики': 'ЭКГ, уровень кислорода в крови',
                    'Ремешок': 'Спортивный'
                }
            },
            {
                'name': 'Apple Watch SE',
                'slug': 'apple-watch-se',
                'category': 'apple-watch',
                'description': 'Доступные Apple Watch с основными функциями для здоровья и фитнеса.',
                'price': 29990,
                'availability': 'available',
                'featured': False,
                'specifications': {
                    'Размер': '40 мм',
                    'Дисплей': 'Retina',
                    'Чип': 'S8 SiP',
                    'Датчики': 'Пульсометр',
                    'Ремешок': 'Спортивный'
                }
            },

            # AirPods
            {
                'name': 'AirPods Pro (2-го поколения)',
                'slug': 'airpods-pro-2',
                'category': 'airpods',
                'description': 'Наушники AirPods Pro с активным шумоподавлением нового уровня и Пространственным звуком.',
                'price': 24990,
                'availability': 'available',
                'featured': True,
                'specifications': {
                    'Тип': 'Внутриканальные',
                    'Шумоподавление': 'Активное',
                    'Чип': 'H2',
                    'Время работы': 'До 6 часов',
                    'Зарядный футляр': 'MagSafe'
                }
            },
            {
                'name': 'AirPods (3-го поколения)',
                'slug': 'airpods-3',
                'category': 'airpods',
                'description': 'AirPods третьего поколения с Пространственным звуком и влагозащитой.',
                'price': 19990,
                'availability': 'available',
                'featured': False,
                'specifications': {
                    'Тип': 'Открытого типа',
                    'Чип': 'H1',
                    'Время работы': 'До 6 часов',
                    'Зарядный футляр': 'Lightning',
                    'Влагозащита': 'IPX4'
                }
            },

            # Accessories
            {
                'name': 'Magic Keyboard для iPad Pro',
                'slug': 'magic-keyboard-ipad-pro',
                'category': 'accessories',
                'description': 'Клавиатура Magic Keyboard с трекпадом и подсветкой клавиш для iPad Pro.',
                'price': 36990,
                'availability': 'available',
                'featured': False,
                'specifications': {
                    'Совместимость': 'iPad Pro 12.9"',
                    'Подсветка': 'Да',
                    'Трекпад': 'Да',
                    'Подключение': 'Smart Connector'
                }
            },
            {
                'name': 'Apple Pencil (2-го поколения)',
                'slug': 'apple-pencil-2',
                'category': 'accessories',
                'description': 'Стилус Apple Pencil второго поколения с беспроводной зарядкой и магнитным креплением.',
                'price': 13990,
                'availability': 'pre_order',
                'featured': False,
                'specifications': {
                    'Поколение': '2-е',
                    'Зарядка': 'Беспроводная',
                    'Крепление': 'Магнитное',
                    'Совместимость': 'iPad Pro, iPad Air'
                }
            }
        ]

        for product_data in products_data:
            category_slug = product_data.pop('category')
            product_data['category'] = categories[category_slug]
            
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {Category.objects.count()} categories '
                f'and {Product.objects.count()} products'
            )
        )