import json
from decimal import Decimal
from faker import Faker
from django.utils.text import slugify
import random
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from django.db import transaction

fake = Faker()





def reset_model_data(model):
    """
    Completely resets all data in the given Django model.
    
    Args:
        model: Django model class to reset
    
    Returns:
        tuple: (number of objects deleted, dict with deletion counts)
    """
    try:
        with transaction.atomic():
            # Delete all objects in the model
            deletion_info = model.objects.all().delete()
            return deletion_info
    except Exception as e:
        # Handle any potential errors
        print(f"Error resetting model {model.__name__}: {str(e)}")
        raise
    
    

def print_model_objects(model, limit=50, fields=None):
    """
    Prints all objects in the given Django model for debugging.
    
    Args:
        model: Django model class
        limit: Maximum number of objects to display (default: 50)
        fields: Specific fields to display (None shows all fields)
    """
    queryset = model.objects.all()
    count = queryset.count()
    
    print(f"\n=== Debugging model: {model.__name__} ===")
    print(f"Total objects: {count}")
    
    if count == 0:
        print("No objects found in the model.")
        return
    
    print("\nFirst {} objects:".format(min(limit, count)))
    
    # Get field names if not specified
    if fields is None:
        fields = [field.name for field in model._meta.fields]
    
    # Print header
    header = " | ".join(fields)
    print("\n" + header)
    print("-" * len(header))
    
    # Print objects
    for obj in queryset[:limit]:
        values = []
        for field in fields:
            try:
                value = str(getattr(obj, field))
                values.append(value[:50] + "..." if len(value) > 50 else value)
            except AttributeError:
                values.append("<field error>")
        print(" | ".join(values))



def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # Convert Decimal to string
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")





def create_test_image():
    """Generate a simple test image in memory"""
    image = Image.new('RGB', (800, 600), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    return SimpleUploadedFile(
        name=f'test_image_{random.randint(1, 1000)}.jpg',
        content=buffer.getvalue(),
        content_type='image/jpeg'
    )


def load_bulk_products(num_records=50):
    # Make sure required models are imported
    from django.contrib.auth.models import User
    from product.models import Product, Category
    from django.utils.text import slugify
    import uuid
    
    products = []
    
    # Get or create some test categories if none exist
    if not Category.objects.exists():
        Category.objects.bulk_create([
            Category(name="Electronics", slug="electronics"),
            Category(name="Clothing", slug="clothing"),
            Category(name="Home & Garden", slug="home-garden"),
            Category(name="Books", slug="books"),
            Category(name="Toys", slug="toys"),
        ])
    
    # Get all categories and users
    categories = Category.objects.all()
    users = User.objects.all()
    
    if not users.exists():
        print("⚠️ No users found. Please create at least one user first.")
        return
    
    for _ in range(num_records):
        name = fake.text(max_nb_chars=50).rstrip('.')
        product = Product(
            name=name,
            price=Decimal(random.uniform(1.99, 999.99)).quantize(Decimal('0.00')),
            rating=Decimal(random.uniform(0.0, 5.0)).quantize(Decimal('0.0')),
            desc=fake.paragraph(nb_sentences=3),
            category=random.choice(categories),
            created_by=random.choice(users),
            image=create_test_image(),
            slug=f"{slugify(name)}-{str(uuid.uuid4())[:8]}",  # Generate slug manually
            uuid=uuid.uuid4(),  # Ensure UUID is set
        )
        products.append(product)
    
    Product.objects.bulk_create(products)
    print(f"✅ Successfully created {len(products)} product records with test images.")

# Usage example:
# load_bulk_products(100)