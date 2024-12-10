import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Import dataset into Product model"

    def handle(self, *args, **kwargs):
        file_path = '../large_dataset.csv'

        # Load CSV using pandas
        try:
            data = pd.read_csv(file_path)
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(data)} rows from the CSV file."))
        except Exception as e:
            self.stderr.write(f"Error loading CSV file: {e}")
            return

        # Validate and clean the data
        try:
            data = data.dropna()  # Remove rows with missing values
            data = data[(data['price'] >= 0) & (data['stock'] >= 0)]  # Non-negative values
        except Exception as e:
            self.stderr.write(f"Error during validation: {e}")
            return

        # Convert to Product instances
        try:
            products = [
                Product(
                    name=row['name'],
                    category=row['category'],
                    price=row['price'],
                    stock=row['stock']
                )
                for _, row in data.iterrows()
            ]
        except Exception as e:
            self.stderr.write(f"Error during data preparation: {e}")
            return

        # Bulk insert
        try:
            Product.objects.bulk_create(products)
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(products)} products into the database."))
        except Exception as e:
            self.stderr.write(f"Error during database insertion: {e}")
