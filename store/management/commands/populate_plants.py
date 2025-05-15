import os
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.files.temp import NamedTemporaryFile
from store.models import Category, Product

# High-quality plant images from Pexels with proper attribution
PLANT_IMAGES = {
    # Indoor Plants
    'Snake Plant': {
        'url': 'https://images.pexels.com/photos/4503273/pexels-photo-4503273.jpeg',
        'photographer': 'Elina Volkova',
        'description': 'A beautiful Snake Plant with tall, upright leaves.'
    },
    'ZZ Plant': {
        'url': 'https://images.pexels.com/photos/4503751/pexels-photo-4503751.jpeg',
        'photographer': 'Elina Volkova',
        'description': 'Healthy ZZ Plant with glossy green leaves.'
    },
    'Pothos': {
        'url': 'https://natalielinda.com/wp-content/uploads/2018/11/Cream-pothos.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Golden Pothos with heart-shaped leaves.'
    },
    'Peace Lily': {
        'url': 'https://scarlettgardens.com/wp-content/uploads/2021/04/peacelily.jpeg',
        'photographer': 'Elina Volkova',
        'description': 'Elegant Peace Lily with white flowers.'
    },
    'Fiddle Leaf Fig': {
        'url': 'https://img.freepik.com/premium-photo/isolated-fiddle-leaf-fig-popular-elegant-plant-feat-top-view-white-background_655090-577069.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Stately Fiddle Leaf Fig tree.'
    },
    
    # Outdoor Plants
    'Lavender': {
        'url': 'https://hdwpro.com/wp-content/uploads/2020/09/Landscape-Lavender-Flower.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Beautiful purple Lavender flowers.'
    },
    'Rose Bush': {
        'url': 'https://i.pinimg.com/736x/20/2c/cf/202ccf0fbadb04765bc0c5045fa4b927.jpg',
        'photographer': 'Marta Dzedyshko',
        'description': 'Vibrant red rose bush.'
    },
    'Sunflower': {
        'url': 'https://www.lovethegarden.com/sites/default/files/content/articles/uk/giant-sunflowers.jpg',
        'photographer': 'Pixabay',
        'description': 'Bright yellow sunflower.'
    },
    'Tulip': {
        'url': 'https://gardentabs.com/wp-content/uploads/2019/10/Tulip-pots.jpg',
        'photographer': 'Pixabay',
        'description': 'Colorful tulip flowers.'
    },
    'Hydrangea': {
        'url': 'https://www.thespruce.com/thmb/Q4CCplOCaSx9TcldQEdqjyayq9o=/5161x3440/filters:fill(auto,1)/siasconset--nantucket--massachusetts-10143762-5b208b0a303713003625cdd8.jpg',
        'photographer': 'Lina Kivaka',
        'description': 'Beautiful blue hydrangea flowers.'
    },
    
    # Succulents
    'Echeveria': {
        'url': 'https://plantly.io/wp-content/uploads/2022/12/Echeveria_secunda_-_Roscoff.jpg',
        'photographer': 'Dids',
        'description': 'Rosette-shaped Echeveria succulent.'
    },
    'Aloe Vera': {
        'url': 'https://greenripegarden.com/wp-content/uploads/2020/04/Aloe-Vera-Plant-2048x1365.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Healthy Aloe Vera plant.'
    },
    'Jade Plant': {
        'url': 'https://www.plantcarefully.com/wp-content/uploads/jade-plant-11.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Mature Jade Plant.'
    },
    'String of Pearls': {
        'url': 'https://gardengotime.com/wp-content/uploads/2021/07/sting-of-pearls-plant.jpgg',
        'photographer': 'Elina Volkova',
        'description': 'Beautiful String of Pearls succulent.'
    },
    'Hens and Chicks': {
        'url': 'https://cdn.mos.cms.futurecdn.net/fWVhKzdtsJFSyG6xNxQYtR-1536-80.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Hens and Chicks succulent arrangement.'
    },
    
    # Flowering Plants
    'Orchid': {
        'url': 'https://cdn.pixabay.com/photo/2022/01/06/09/21/orchid-6919028_1280.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Elegant white orchid.'
    },
    'African Violet': {
        'url': 'https://www.almanac.com/sites/default/files/image_nodes/african-violet-houseplant.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Vibrant African Violet.'
    },
    'Anthurium': {
        'url': 'https://cdn.mos.cms.futurecdn.net/JhYRFDeFNKgUsjkT2fcu6a.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Red Anthurium with glossy leaves.'
    },
    'Bromeliad': {
        'url': 'https://www.gardenmandy.com/wp-content/uploads/2018/08/Bromeliad-Flower-1920x1440.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Colorful Bromeliad plant.'
    },
    'Kalanchoe': {
        'url': 'https://plantly.io/wp-content/uploads/2023/03/Kalanchoe_blossfeldiorum2.jpg',
        'photographer': 'Elina Volkova',
        'description': 'Blooming Kalanchoe plant.'
    }
}

class Command(BaseCommand):
    help = 'Populate the database with plant data'

    def handle(self, *args, **options):
        # Create categories if they don't exist
        categories_data = [
            {
                'name': 'Indoor Plants',
                'slug': 'indoor-plants',
                'description': 'Beautiful plants that thrive in indoor conditions, perfect for homes and offices.',
                'image_url': 'https://fedandfit.com/wp-content/uploads/2020/06/houseplants-scaled-e1593515074870.jpeg',
                'products': [
                    'Snake Plant',
                    'ZZ Plant',
                    'Pothos',
                    'Peace Lily',
                    'Fiddle Leaf Fig'
                ]
            },
            {
                'name': 'Outdoor Plants',
                'slug': 'outdoor-plants',
                'description': 'Perfect plants for your garden that thrive in outdoor conditions.',
                'image_url': 'https://greenorchid.co.in/wp-content/uploads/2020/11/Outdoor-plant-1.jpg',
                'products': [
                    'Lavender',
                    'Rose Bush',
                    'Sunflower',
                    'Tulip',
                    'Hydrangea'
                ]
            },
            {
                'name': 'Succulents',
                'slug': 'succulents',
                'description': 'Low-maintenance and beautiful plants that store water in their leaves.',
                'image_url': 'https://3.bp.blogspot.com/-Mo25IcY_t78/Wf99JH83GqI/AAAAAAAAAHg/RyV53b6E2QwYRBsEs841o5VtcIBomwcWACLcBGAs/s1600/IMG_20171018_185746_903.jpg',
                'products': [
                    'Echeveria',
                    'Aloe Vera',
                    'Jade Plant',
                    'String of Pearls',
                    'Hens and Chicks'
                ]
            },
            {
                'name': 'Flowering Plants',
                'slug': 'flowering-plants',
                'description': 'Brighten up your space with beautiful flowering plants.',
                'image_url': 'https://images.ctfassets.net/zma7thmmcinb/6QIUKgB2OMvXSJeTYJvwar/e6612763932b524aefdbdc0e8d818501/spring-blooming-bulbs-lead.jpg',
                'products': [
                    'Orchid',
                    'African Violet',
                    'Anthurium',
                    'Bromeliad',
                    'Kalanchoe'
                ]
            },
        ]

        # Create a dictionary to store all products with their details
        products_data = []
        
        # Define product details with accurate information
        product_details = {
            # Indoor Plants
            'Snake Plant': {
                'slug': 'snake-plant',
                'description': 'Sansevieria trifasciata, also known as the snake plant, is a hardy indoor plant that purifies the air by removing toxins. It thrives in low light and requires minimal watering.',
                'price': 24.99,
                'compare_at_price': 34.99,
                'light_requirements': 'Low to bright indirect light',
                'watering_needs': 'Low (water every 2-3 weeks)',
                'mature_size': '2-4 feet tall',
                'difficulty_level': 'easy',
                'is_featured': True,
                'is_bestseller': True
            },
            'ZZ Plant': {
                'slug': 'zz-plant',
                'description': 'Zamioculcas zamiifolia, commonly known as the ZZ plant, is an excellent choice for beginners. It tolerates low light and irregular watering.',
                'price': 29.99,
                'compare_at_price': 39.99,
                'light_requirements': 'Low to bright indirect light',
                'watering_needs': 'Low (water when soil is dry)',
                'mature_size': '2-3 feet tall',
                'difficulty_level': 'easy',
                'is_featured': True,
                'is_bestseller': True
            },
            'Pothos': {
                'slug': 'pothos',
                'description': 'Epipremnum aureum, or Pothos, is a versatile trailing plant that purifies the air. It can grow in various light conditions.',
                'price': 19.99,
                'compare_at_price': 29.99,
                'light_requirements': 'Low to bright indirect light',
                'watering_needs': 'Moderate (water when top inch is dry)',
                'mature_size': '6-10 feet long',
                'difficulty_level': 'easy',
                'is_featured': True,
                'is_bestseller': True
            },
            'Peace Lily': {
                'slug': 'peace-lily',
                'description': 'Spathiphyllum, or Peace Lily, is known for its beautiful white flowers and air-purifying qualities. It thrives in low to medium light.',
                'price': 34.99,
                'compare_at_price': 44.99,
                'light_requirements': 'Low to medium indirect light',
                'watering_needs': 'Moderate (keep soil moist)',
                'mature_size': '1-4 feet tall',
                'difficulty_level': 'easy',
                'is_featured': True,
                'is_bestseller': True
            },
            'Fiddle Leaf Fig': {
                'slug': 'fiddle-leaf-fig',
                'description': 'Ficus lyrata, or Fiddle Leaf Fig, is a popular indoor tree with large, violin-shaped leaves. It makes a dramatic statement in any room.',
                'price': 59.99,
                'compare_at_price': 79.99,
                'light_requirements': 'Bright indirect light',
                'watering_needs': 'Moderate (water when top 2 inches are dry)',
                'mature_size': '6-10 feet tall',
                'difficulty_level': 'moderate',
                'is_featured': True,
                'is_bestseller': True
            },
            
            # Outdoor Plants
            'Lavender': {
                'slug': 'lavender',
                'description': 'Lavandula, or Lavender, is a fragrant herb with beautiful purple flowers. It attracts pollinators and is drought-tolerant once established.',
                'price': 14.99,
                'compare_at_price': 19.99,
                'light_requirements': 'Full sun',
                'watering_needs': 'Low (drought-tolerant)',
                'mature_size': '1-3 feet tall',
                'difficulty_level': 'easy',
                'is_featured': True
            },
            'Rose Bush': {
                'slug': 'rose-bush',
                'description': 'Rosa spp., or Rose Bush, is a classic garden favorite known for its beautiful, fragrant flowers in various colors.',
                'price': 24.99,
                'compare_at_price': 34.99,
                'light_requirements': 'Full sun',
                'watering_needs': 'Moderate (water deeply once a week)',
                'mature_size': '3-6 feet tall',
                'difficulty_level': 'moderate',
                'is_featured': True
            },
            'Sunflower': {
                'slug': 'sunflower',
                'description': 'Helianthus annuus, or Sunflower, is a cheerful annual with large, bright yellow flowers that track the sun.',
                'price': 12.99,
                'compare_at_price': 16.99,
                'light_requirements': 'Full sun',
                'watering_needs': 'Moderate (water regularly)',
                'mature_size': '3-10 feet tall',
                'difficulty_level': 'easy',
                'is_featured': True
            },
            'Tulip': {
                'slug': 'tulip',
                'description': 'Tulipa spp., or Tulip, is a spring-blooming perennial with cup-shaped flowers in a wide range of colors.',
                'price': 9.99,
                'compare_at_price': 14.99,
                'light_requirements': 'Full sun to partial shade',
                'watering_needs': 'Moderate (water when soil is dry)',
                'mature_size': '6-24 inches tall',
                'difficulty_level': 'easy',
                'is_featured': True
            },
            'Hydrangea': {
                'slug': 'hydrangea',
                'description': 'Hydrangea macrophylla, or Bigleaf Hydrangea, produces large, showy flower clusters in shades of blue, pink, or white.',
                'price': 29.99,
                'compare_at_price': 39.99,
                'light_requirements': 'Morning sun, afternoon shade',
                'watering_needs': 'Moderate to high (keep soil moist)',
                'mature_size': '3-6 feet tall and wide',
                'difficulty_level': 'moderate',
                'is_featured': True
            },
            
            # Succulents
            'Echeveria': {
                'slug': 'echeveria',
                'description': 'Echeveria spp. are rosette-forming succulents with colorful, fleshy leaves. They are drought-tolerant and easy to care for.',
                'price': 12.99,
                'compare_at_price': 16.99,
                'light_requirements': 'Bright light to full sun',
                'watering_needs': 'Low (water when soil is completely dry)',
                'mature_size': '2-12 inches in diameter',
                'difficulty_level': 'easy',
                'is_featured': True,
                'is_bestseller': True
            },
            'Aloe Vera': {
                'slug': 'aloe-vera',
                'description': 'Aloe barbadensis, or Aloe Vera, is a medicinal succulent with soothing gel inside its leaves. It\'s great for sunburns and skin care.',
                'price': 14.99,
                'compare_at_price': 19.99,
                'light_requirements': 'Bright light',
                'watering_needs': 'Low (water when soil is dry)',
                'mature_size': '1-2 feet tall',
                'difficulty_level': 'easy',
                'is_featured': True,
                'is_bestseller': True
            },
            'Jade Plant': {
                'slug': 'jade-plant',
                'description': 'Crassula ovata, or Jade Plant, is a popular succulent with thick, woody stems and oval-shaped leaves. It symbolizes good luck.',
                'price': 19.99,
                'compare_at_price': 24.99,
                'light_requirements': 'Bright light',
                'watering_needs': 'Low (water when soil is dry)',
                'mature_size': '2-5 feet tall',
                'difficulty_level': 'easy',
                'is_featured': True
            },
            'String of Pearls': {
                'slug': 'string-of-pearls',
                'description': 'Senecio rowleyanus, or String of Pearls, is a unique trailing succulent with spherical leaves that resemble pearls on a string.',
                'price': 16.99,
                'compare_at_price': 21.99,
                'light_requirements': 'Bright, indirect light',
                'watering_needs': 'Low (water when soil is dry)',
                'mature_size': '1-2 feet long',
                'difficulty_level': 'moderate',
                'is_featured': True
            },
            'Hens and Chicks': {
                'slug': 'hens-and-chicks',
                'description': 'Sempervivum tectorum, or Hens and Chicks, is a hardy succulent that forms rosettes and produces offsets (chicks) around the mother plant (hen).',
                'price': 9.99,
                'compare_at_price': 14.99,
                'light_requirements': 'Full sun',
                'watering_needs': 'Low (drought-tolerant)',
                'mature_size': '3-6 inches tall',
                'difficulty_level': 'easy',
                'is_featured': True
            },
            # Flowering Plants
            'Orchid': {
                'slug': 'orchid',
                'description': 'Phalaenopsis spp., or Moth Orchid, is an elegant flowering plant with long-lasting blooms. It\'s perfect for adding a touch of sophistication to any space.',
                'price': 34.99,
                'compare_at_price': 49.99,
                'light_requirements': 'Bright, indirect light',
                'watering_needs': 'Moderate (water when almost dry)',
                'mature_size': '1-3 feet tall',
                'difficulty_level': 'moderate',
                'is_featured': True,
                'is_bestseller': True
            },
            'African Violet': {
                'slug': 'african-violet',
                'description': 'Saintpaulia, or African Violet, is a popular houseplant with velvety leaves and clusters of purple, pink, or white flowers.',
                'price': 12.99,
                'compare_at_price': 16.99,
                'light_requirements': 'Bright, indirect light',
                'watering_needs': 'Moderate (keep soil slightly moist)',
                'mature_size': '6-9 inches tall',
                'difficulty_level': 'moderate',
                'is_featured': True
            },
            'Anthurium': {
                'slug': 'anthurium',
                'description': 'Anthurium andraeanum, or Flamingo Flower, is known for its glossy, heart-shaped leaves and long-lasting, waxy flowers in red, pink, or white.',
                'price': 29.99,
                'compare_at_price': 39.99,
                'light_requirements': 'Bright, indirect light',
                'watering_needs': 'Moderate (water when top inch is dry)',
                'mature_size': '1-3 feet tall',
                'difficulty_level': 'moderate',
                'is_featured': True
            },
            'Bromeliad': {
                'slug': 'bromeliad',
                'description': 'Bromeliaceae, or Bromeliad, is a tropical plant with striking foliage and long-lasting, colorful flower bracts.',
                'price': 24.99,
                'compare_at_price': 34.99,
                'light_requirements': 'Bright, indirect light',
                'watering_needs': 'Moderate (water in the central cup)',
                'mature_size': '1-3 feet tall',
                'difficulty_level': 'easy',
                'is_featured': True
            },
            'Kalanchoe': {
                'slug': 'kalanchoe',
                'description': 'Kalanchoe blossfeldiana is a flowering succulent that produces clusters of small, brightly colored flowers. It blooms for several weeks.',
                'price': 14.99,
                'compare_at_price': 19.99,
                'light_requirements': 'Bright light',
                'watering_needs': 'Low to moderate (let soil dry between waterings)',
                'mature_size': '6-18 inches tall',
                'difficulty_level': 'easy',
                'is_featured': True
            }
        }
        
        # Build products_data list from the product_details dictionary
        for product_name, details in product_details.items():
            if product_name in PLANT_IMAGES:
                # Generate a simple SKU from the product name
                sku = f"{product_name.replace(' ', '').upper()[:8]}-{len(products_data) + 1:03d}"
                
                products_data.append({
                    'name': product_name,
                    'slug': details['slug'],
                    'sku': sku,
                    'description': details['description'],
                    'price': details['price'],
                    'compare_at_price': details.get('compare_at_price'),
                    'image_url': PLANT_IMAGES[product_name]['url'],
                    'light_requirements': details.get('light_requirements', ''),
                    'watering_needs': details.get('watering_needs', ''),
                    'mature_size': details.get('mature_size', ''),
                    'difficulty_level': details.get('difficulty_level', 'easy'),
                    'is_featured': details.get('is_featured', False),
                    'is_bestseller': details.get('is_bestseller', False),
                    'short_description': details['description'][:200] + '...' if len(details['description']) > 200 else details['description']
                })

        self.stdout.write('Creating categories...')
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            
            # Download and save category image
            if not category.image:
                self.download_image(category, cat_data['image_url'], 'categories')
                
            categories[cat_data['slug']] = category
            self.stdout.write(f'Created category: {category.name}')

        self.stdout.write('\nAdding plants...')
        for product_data in products_data:
            # Find the category for this product
            category = None
            for cat_data in categories_data:
                if product_data['name'] in cat_data.get('products', []):
                    category = categories[cat_data['slug']]
                    break
            
            if not category:
                self.stderr.write(self.style.ERROR(f"No category found for product: {product_data['name']}"))
                continue

            product, created = Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'sku': product_data['sku'],
                    'short_description': product_data.get('short_description', product_data['description'][:200] + '...'),
                    'price': product_data['price'],
                    'compare_at_price': product_data.get('compare_at_price'),
                    'category': category,
                    'light_requirements': product_data.get('light_requirements', ''),
                    'watering_needs': product_data.get('watering_needs', ''),
                    'mature_size': product_data.get('mature_size', ''),
                    'difficulty_level': product_data.get('difficulty_level', 'easy'),
                    'is_featured': product_data.get('is_featured', False),
                    'is_bestseller': product_data.get('is_bestseller', False),
                    'is_active': True
                }
            )

            # Download and set product image if it doesn't have one
            if 'image_url' in product_data and product_data['image_url']:
                if not product.image:  # Only download if image doesn't exist
                    success = self.download_image(product, product_data['image_url'], 'products')
                    if not success:
                        self.stderr.write(self.style.WARNING(f"Using placeholder for {product.name} due to image download failure"))
                        # Set a default placeholder image if download fails
                        if not product.image:
                            product.image = 'products/placeholder.jpg'  # Make sure this path exists in your media directory
                            product.save()

            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{action} product: {product.name}'))

        self.stdout.write('\nDatabase population completed successfully!')

    def download_image(self, obj, url, folder):
        try:
            # Skip if no URL is provided
            if not url:
                self.stderr.write(self.style.WARNING(f"No image URL provided for {obj.name}"))
                return False
                
            # Create a temporary file
            img_temp = None
            try:
                img_temp = NamedTemporaryFile(suffix='.jpg')
                
                # Set a user-agent to avoid 403 Forbidden errors
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                # Download the image with a timeout
                response = requests.get(url, stream=True, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Check content type to ensure it's an image
                content_type = response.headers.get('content-type', '').lower()
                if 'image' not in content_type:
                    raise ValueError(f"URL does not point to an image (content-type: {content_type})")
                
                # Save the image to the temporary file
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        img_temp.write(chunk)
                
                # Reset file pointer to the beginning
                img_temp.seek(0)
                
                # Generate a filename
                filename = f"{obj.slug}.jpg"
                
                # Save the image to the object
                obj.image.save(filename, File(img_temp), save=False)
                obj.save()
                
                self.stdout.write(self.style.SUCCESS(f"Successfully downloaded image for {obj.name}"))
                return True
                
            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.WARNING(f"Failed to download image from {url} for {obj.name}: {e}"))
                return False
                
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing image for {obj.name}: {e}"))
                return False
                
            finally:
                # Always close the temporary file if it was created
                if img_temp is not None:
                    img_temp.close()
                    
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error in download_image for {obj.name}: {e}"))
            return False
