from decimal import Decimal

from django.core.files import File
from django.core.management.base import BaseCommand

from store.models import Brand, Category, Product


CATEGORY_DATA = [
    ('Consoles', 'bi-controller', 'The latest and greatest gaming consoles from every major platform.'),
    ('Controllers', 'bi-joystick', 'Wired and wireless controllers for every console and PC.'),
    ('Headsets', 'bi-headset', 'Immersive gaming headsets with crystal clear audio and mic quality.'),
    ('Accessories', 'bi-usb-plug', 'Chargers, stands, cases, cooling and everything in between.'),
    ('Games', 'bi-disc', 'Physical and digital copies of the hottest game titles.'),
]

BRAND_NAMES = ['Sony', 'Microsoft', 'Nintendo', 'Razer', 'Logitech', 'SteelSeries', 'Astro', 'ValveTech', '8BitDo']


class Command(BaseCommand):
    help = 'Seed the database with sample categories, brands and products for GameHub.'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Delete existing products/categories/brands before seeding.')

    def handle(self, *args, **options):
        if options['flush']:
            Product.objects.all().delete()
            Category.objects.all().delete()
            Brand.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing catalog data.'))

        categories = {}
        for name, icon, desc in CATEGORY_DATA:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'icon': icon, 'description': desc})
            categories[name] = cat

        brands = {}
        for name in BRAND_NAMES:
            brand, _ = Brand.objects.get_or_create(name=name)
            brands[name] = brand

        def img(filename):
            path = f'/home/claude/gamehub/seed_images/{filename}'
            return File(open(path, 'rb'), name=filename)

        products = [
            dict(name='NovaPlay 5 Console', category='Consoles', brand='Sony', platform='PS',
                 price='499.99', discount=10, stock=25, featured=True, image='ps_console.jpg',
                 description='The flagship next-gen console with lightning-fast SSD loading, ray tracing and stunning 4K visuals.',
                 specs='Storage: 1TB SSD\nResolution: Up to 4K/120fps\nRay Tracing: Yes\nBackward Compatible: Yes\nIncludes: 1 wireless controller'),
            dict(name='NovaPlay 5 Digital Edition', category='Consoles', brand='Sony', platform='PS',
                 price='399.99', discount=5, stock=18, featured=False, image='ps_console.jpg',
                 description='All the power of NovaPlay 5, disc-free — for an all-digital gaming library.',
                 specs='Storage: 825GB SSD\nResolution: Up to 4K/120fps\nDisc Drive: None\nIncludes: 1 wireless controller'),
            dict(name='SeriesX Console', category='Consoles', brand='Microsoft', platform='XB',
                 price='499.99', discount=0, stock=30, featured=True, image='xbox_console.jpg',
                 description='The most powerful Xbox ever built, with 12 teraflops of processing power and Quick Resume.',
                 specs='Storage: 1TB SSD\nResolution: True 4K, up to 120fps\nQuick Resume: Yes\nIncludes: 1 wireless controller'),
            dict(name='SeriesS Console', category='Consoles', brand='Microsoft', platform='XB',
                 price='299.99', discount=8, stock=40, featured=True, image='xbox_console.jpg',
                 description='All-digital next-gen console, small in size but big on speed.',
                 specs='Storage: 512GB SSD\nResolution: Up to 1440p/120fps\nDisc Drive: None\nIncludes: 1 wireless controller'),
            dict(name='Switch OLED Console', category='Consoles', brand='Nintendo', platform='NS',
                 price='349.99', discount=0, stock=35, featured=True, image='switch_console.jpg',
                 description='Play at home or on the go with a vivid 7-inch OLED screen and enhanced audio.',
                 specs='Screen: 7" OLED\nStorage: 64GB\nBattery: Up to 9 hours\nIncludes: Dock, Joy-Con pair'),
            dict(name='Switch Lite Console', category='Consoles', brand='Nintendo', platform='NS',
                 price='199.99', discount=12, stock=22, featured=False, image='switch_console.jpg',
                 description='A compact, lightweight console dedicated to handheld play.',
                 specs='Screen: 5.5" LCD\nStorage: 32GB\nBattery: Up to 7 hours\nWeight: 275g'),
            dict(name='RetroStation Classic', category='Consoles', brand='Sony', platform='UN',
                 price='79.99', discount=0, stock=15, featured=False, image='retro_console.jpg',
                 description='A mini retro console pre-loaded with 20 classic titles for nostalgic fun.',
                 specs='Games included: 20\nOutput: HDMI 1080p\nControllers: 2 included'),
            dict(name='StreamDeck Handheld PC', category='Consoles', brand='ValveTech', platform='PC',
                 price='649.99', discount=15, stock=12, featured=True, image='handheld_console.jpg',
                 description='A handheld gaming PC that runs your whole library on the go.',
                 specs='Screen: 7" 1280x800\nStorage: 512GB NVMe SSD\nBattery: 2-8 hours\nOS: Custom Linux'),

            dict(name='DualSense Wireless Controller', category='Controllers', brand='Sony', platform='PS',
                 price='69.99', discount=0, stock=80, featured=True, image='controller1.jpg',
                 description='Haptic feedback and adaptive triggers deliver a deeply immersive experience.',
                 specs='Connectivity: Bluetooth / USB-C\nBattery: ~12 hours\nHaptics: Yes\nAdaptive Triggers: Yes'),
            dict(name='Xbox Wireless Controller', category='Controllers', brand='Microsoft', platform='XB',
                 price='59.99', discount=10, stock=90, featured=True, image='controller2.jpg',
                 description='Sculpted, ergonomic design with textured grip and a hybrid D-pad.',
                 specs='Connectivity: Bluetooth / USB-C\nBattery: AA x2 or rechargeable\nHybrid D-Pad: Yes'),
            dict(name='Joy-Con Pair (Neon)', category='Controllers', brand='Nintendo', platform='NS',
                 price='79.99', discount=0, stock=60, featured=False, image='controller3.jpg',
                 description='Detachable controllers with motion controls and HD rumble, sold as a pair.',
                 specs='Connectivity: Bluetooth\nMotion Controls: Yes\nHD Rumble: Yes\nColor: Neon Red/Blue'),
            dict(name='Razer Wolverine V2 Pro', category='Controllers', brand='Razer', platform='PS',
                 price='249.99', discount=5, stock=20, featured=True, image='controller4.jpg',
                 description='Pro-level wireless controller with remappable buttons and Hall Effect triggers.',
                 specs='Connectivity: Bluetooth / Wireless Dongle\nRemappable Buttons: 6\nTrigger Stops: Yes'),
            dict(name='8BitDo Pro 2 Controller', category='Controllers', brand='8BitDo', platform='UN',
                 price='49.99', discount=0, stock=45, featured=False, image='controller5.jpg',
                 description='A versatile controller compatible with Switch, PC, Android and Raspberry Pi.',
                 specs='Connectivity: Bluetooth / USB-C / 2.4G\nCompatibility: Multi-platform\nCustomization: Ultimate Software'),

            dict(name='Astro A50 Wireless Headset', category='Headsets', brand='Astro', platform='UN',
                 price='299.99', discount=10, stock=25, featured=True, image='headset1.jpg',
                 description='Premium wireless gaming headset with a base station for seamless charging and audio.',
                 specs='Connectivity: Wireless\nBattery: 15+ hours\nSurround Sound: Dolby Atmos\nMic: Detachable'),
            dict(name='SteelSeries Arctis Nova Pro', category='Headsets', brand='SteelSeries', platform='UN',
                 price='349.99', discount=0, stock=18, featured=True, image='headset2.jpg',
                 description='Hi-fi audio drivers and active noise cancellation for total immersion.',
                 specs='Connectivity: Wireless / Wired\nANC: Yes\nBattery: Hot-swappable\nMic: ClearCast Gen 2'),
            dict(name='Razer Kraken V3 X', category='Headsets', brand='Razer', platform='UN',
                 price='49.99', discount=15, stock=55, featured=False, image='headset3.jpg',
                 description='Lightweight headset with immersive 7.1 surround sound on a budget.',
                 specs='Connectivity: USB\nSurround: 7.1\nWeight: 250g\nMic: Cardioid, noise-cancelling'),
            dict(name='Logitech G Pro X Headset', category='Headsets', brand='Logitech', platform='UN',
                 price='129.99', discount=0, stock=30, featured=False, image='headset4.jpg',
                 description='Esports-grade headset with Blue Voice mic technology and pro-tuned drivers.',
                 specs='Connectivity: Wired / USB\nMic: Blue VO!CE\nDrivers: PRO-G 50mm\nComfort: Memory foam'),

            dict(name='Charging Dock Dual Slot', category='Accessories', brand='Sony', platform='PS',
                 price='29.99', discount=0, stock=70, featured=False, image='accessory1.jpg',
                 description='Charge two DualSense controllers simultaneously with LED status indicators.',
                 specs='Slots: 2\nCharge Time: ~2.5 hours\nConnector: USB-C'),
            dict(name='Xbox Play & Charge Kit', category='Accessories', brand='Microsoft', platform='XB',
                 price='24.99', discount=0, stock=65, featured=False, image='accessory2.jpg',
                 description='Rechargeable battery pack and USB-C cable to keep you in the game longer.',
                 specs='Battery Life: Up to 30 hours\nCable Length: 9 ft\nCompatibility: Xbox Series X|S'),
            dict(name='Console Cooling Stand', category='Accessories', brand='Logitech', platform='UN',
                 price='34.99', discount=20, stock=40, featured=False, image='accessory3.jpg',
                 description='Vertical stand with dual fans to keep your console cool during long sessions.',
                 specs='Fans: 2 quiet-running\nCompatibility: Most consoles\nExtra: Controller charging ports'),
            dict(name='Carrying Case for Switch', category='Accessories', brand='Nintendo', platform='NS',
                 price='19.99', discount=0, stock=90, featured=False, image='accessory4.jpg',
                 description='Protective hard-shell case with slots for games and cables.',
                 specs='Material: EVA hard shell\nGame Slots: 10\nCompatibility: Switch / OLED / Lite'),
            dict(name='4TB External Game Drive', category='Accessories', brand='SteelSeries', platform='UN',
                 price='109.99', discount=5, stock=33, featured=True, image='accessory5.jpg',
                 description='Expand your storage instantly — plug-and-play compatible with all major consoles.',
                 specs='Capacity: 4TB\nInterface: USB 3.0\nCompatibility: PS/Xbox/PC'),

            dict(name='Galaxy Frontier: Redux', category='Games', brand='ValveTech', platform='UN',
                 price='59.99', discount=0, stock=100, featured=True, image='game1.jpg',
                 description='An open-world sci-fi epic remastered with 4K textures and a new campaign chapter.',
                 specs='Genre: Open World RPG\nPlayers: 1\nRating: Teen'),
            dict(name='Street Rivals 7', category='Games', brand='Microsoft', platform='XB',
                 price='69.99', discount=10, stock=80, featured=True, image='game2.jpg',
                 description='The next chapter in the legendary fighting series with rollback netcode.',
                 specs='Genre: Fighting\nPlayers: 1-2 (Online 2-8)\nRating: Teen'),
            dict(name='Kingdom Quest: Origins', category='Games', brand='Nintendo', platform='NS',
                 price='49.99', discount=0, stock=75, featured=False, image='game3.jpg',
                 description='A charming adventure through a hand-painted world full of puzzles and secrets.',
                 specs='Genre: Adventure\nPlayers: 1\nRating: Everyone'),
        ]

        created_count = 0
        for p in products:
            if Product.objects.filter(name=p['name']).exists():
                continue
            product = Product(
                category=categories[p['category']],
                brand=brands[p['brand']],
                name=p['name'],
                platform=p['platform'],
                description=p['description'],
                specs=p['specs'],
                price=Decimal(p['price']),
                discount_percent=p['discount'],
                stock=p['stock'],
                is_featured=p['featured'],
                is_active=True,
            )
            product.image.save(p['image'], img(p['image']), save=False)
            product.save()
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete: {len(categories)} categories, {len(brands)} brands, {created_count} new products created.'
        ))
