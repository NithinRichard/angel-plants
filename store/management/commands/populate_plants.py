import os
import random
import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.files.temp import NamedTemporaryFile
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Populate the database with plant data'

    def handle(self, *args, **options):
        # Create categories if they don't exist
        categories_data = [
            {
                'name': 'Indoor Plants',
                'slug': 'indoor-plants',
                'description': 'Beautiful plants that thrive indoors',
                'image_url': 'https://images.pexels.com/photos/1402409/pexels-photo-1402409.jpeg'  # Indoor Plants
            },
            {
                'name': 'Outdoor Plants',
                'slug': 'outdoor-plants',
                'description': 'Perfect plants for your garden',
                'image_url': 'https://images.pexels.com/photos/1454288/pexels-photo-1454288.jpeg'  # Outdoor Plants
            },
            {
                'name': 'Succulents',
                'slug': 'succulents',
                'description': 'Low-maintenance and beautiful succulents',
                'image_url': 'https://images.pexels.com/photos/1903965/pexels-photo-1903965.jpeg'  # Succulents
            },
            {
                'name': 'Flowering Plants',
                'slug': 'flowering-plants',
                'description': 'Bright and colorful flowering plants',
                'image_url': 'https://images.pexels.com/photos/1086178/pexels-photo-1086178.jpeg'  # Flowering Plants
            },
        ]

        plants_data = [
            # Indoor Plants
            {
                'name': 'Snake Plant',
                'slug': 'snake-plant',
                'description': 'A hardy, low-maintenance plant that thrives in low light conditions.',
                'price': 599.00,
                'stock': 50,
                'image_url': 'https://images.pexels.com/photos/4503752/pexels-photo-4503752.jpeg',  # Snake Plant
                'category_slug': 'indoor-plants'
            },
            {
                'name': 'ZZ Plant',
                'slug': 'zz-plant',
                'description': 'A tough plant that can survive with very little water and light.',
                'price': 799.00,
                'stock': 45,
                'image_url': 'https://images.pexels.com/photos/4503751/pexels-photo-4503751.jpeg',  # ZZ Plant
                'category_slug': 'indoor-plants'
            },
            {
                'name': 'Pothos',
                'slug': 'pothos',
                'description': 'A versatile and easy-to-care-for trailing plant.',
                'price': 449.00,
                'stock': 60,
                'image_url': 'https://images.pexels.com/photos/4503753/pexels-photo-4503753.jpeg',  # Pothos
                'category_slug': 'indoor-plants'
            },
            # Outdoor Plants
            {
                'name': 'Lavender',
                'slug': 'lavender',
                'description': 'Fragrant purple flowers that attract pollinators.',
                'price': 349.00,
                'stock': 35,
                'image_url': 'https://images.pexels.com/photos/4503754/pexels-photo-4503754.jpeg',  # Lavender
                'category_slug': 'outdoor-plants'
            },
            {
                'name': 'Boxwood',
                'slug': 'boxwood',
                'description': 'Evergreen shrub perfect for hedges and topiaries.',
                'price': 899.00,
                'stock': 25,
                'image_url': 'https://images.pexels.com/photos/4503755/pexels-photo-4503755.jpeg',  # Boxwood
                'category_slug': 'outdoor-plants'
            },
            # Succulents
            {
                'name': 'Echeveria',
                'slug': 'echeveria',
                'description': 'Rosette-forming succulents with beautiful colors.',
                'price': 249.00,
                'stock': 80,
                'image_url': 'https://images.pexels.com/photos/4503756/pexels-photo-4503756.jpeg',  # Echeveria
                'category_slug': 'succulents'
            },
            {
                'name': 'Aloe Vera',
                'slug': 'aloe-vera',
                'description': 'Healing plant with soothing gel inside its leaves.',
                'price': 299.00,
                'stock': 40,
                'image_url': 'https://images.pexels.com/photos/4503757/pexels-photo-4503757.jpeg',  # Aloe Vera
                'category_slug': 'succulents'
            },
            # Flowering Plants
            {
                'name': 'Orchid',
                'slug': 'orchid',
                'description': 'Elegant flowering plant with long-lasting blooms.',
                'price': 799.00,
                'stock': 30,
                'image_url': 'https://images.pexels.com/photos/4503758/pexels-photo-4503758.jpeg',  # Orchid
                'category_slug': 'flowering-plants'
            },
            {
                'name': 'Peace Lily',
                'slug': 'peace-lily',
                'description': 'Beautiful white flowers that help purify the air.',
                'price': 599.00,
                'stock': 35,
                'image_url': 'https://images.pexels.com/photos/4503759/pexels-photo-4503759.jpeg',  # Peace Lily
                'category_slug': 'flowering-plants'
            },
            {
                'name': 'African Violet',
                'slug': 'african-violet',
                'description': 'Charming flowering plant with velvety leaves.',
                'price': 449.00,
                'stock': 45,
                'image_url': 'https://images.pexels.com/photos/4503760/pexels-photo-4503760.jpeg',  # African Violet
                'category_slug': 'flowering-plants'
            },
        ]

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
        for plant_data in plants_data:
            category = categories.get(plant_data['category_slug'])
            if not category:
                self.stderr.write(f"Category {plant_data['category_slug']} not found")
                continue

            plant, created = Product.objects.get_or_create(
                slug=plant_data['slug'],
                defaults={
                    'name': plant_data['name'],
                    'description': plant_data['description'],
                    'price': plant_data['price'],
                    'stock': plant_data['stock'],
                    'category': category
                }
            )

            # Download and save plant image
            if not plant.image:
                self.download_image(plant, plant_data['image_url'], 'products')

            self.stdout.write(f'Added plant: {plant.name} (${plant.price})')

        self.stdout.write('\nDatabase population completed successfully!')

    def download_image(self, obj, url, folder):
        try:
            # Create a temporary file
            img_temp = NamedTemporaryFile(suffix='.jpg')
            
            # Download the image
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
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
            
            # Close and remove the temporary file
            img_temp.close()
            
            return True
            
        except Exception as e:
            self.stderr.write(f"Error downloading image: {e}")
            if 'img_temp' in locals():
                img_temp.close()
            return False
