import csv
from faker import Faker
import random

fake = Faker()

property_types = ["Apartment", "House", "Villa", "Cabin", "Hotel", "Guesthouse", "Cave", "Farm"]
property_options = {
    "Apartment": ["An entire place", "A room", "A shared room"],
    "House": ["An entire place", "A room", "A shared room"],
    "Villa": ["An entire place", "A room", "A shared room"],
    "Cabin": ["An entire place", "A room"],
    "Hotel": ["An entire place", "A room", "A shared room"],
    "Guesthouse": ["An entire place", "A room", "A shared room"],
    "Cave": ["An entire place", "A room", "A shared room"],
    "Farm": ["An entire place", "A room", "A shared room"]
}
amenities_list = ["WiFi", "kitchen" "Swimming Pool", "excercise eqipment", "Free parking on premises", "paid parking on premises", "Air Conditioning", "Kitchen", "dedicated wokplace" "pool", "BBQ grill", "pool table", "TV", "outdoor shower", "beach access", "indore fire place", "piano", "ski-in/ski-out", "smoke alarm", "first aid kit", "fire extinguisher", "carbon monoxide alarm"]
bed_types = ["Single", "Double", "Queen", "King"]
neighborhoods = ["Downtown", "Suburb", "Waterfront", "Mountain View"]
guest_types = ["Any Airbnb guest", "An experienced guest"]

data = []

for _ in range(5000):  # Generate 100 fake property entries
    location = fake.city()
    latitude = fake.latitude()
    longitude = fake.longitude()
    property_type = random.choice(property_types)
    options = property_options[property_type]
    option = random.choice(options)
    guests = random.randint(1, 5)
    number_of_bedrooms = random.randint(1, 5)
    amenities = random.sample(amenities_list, random.randint(1, len(amenities_list)))
    seasonality = fake.random_element(elements=("Autumn", "Winter", "Summer"))
    base_price = random.uniform(50, 5000)
    bathrooms = number_of_bedrooms + random.randint(0, 4)
    bed_type = random.choice(bed_types)
    beds = number_of_bedrooms + random.randint(1, 4)
    neighborhood = random.choice(neighborhoods)
    guest_type = random.choice(guest_types)

    images = [fake.image_url(width=800, height=600) for _ in range(5)]
    title = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
    description = fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)

    data.append({
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "property_type": property_type,
        "option": option,
        "guests": guests,
        "number_of_bedrooms": number_of_bedrooms,
        "amenities": amenities,
        "seasonality": seasonality,
        "base_price": base_price,
        "bathrooms": bathrooms,
        "bed_type": bed_type,
        "beds": beds,
        "neighborhood": neighborhood,
        "guest_type": guest_type,
        "images": images,
        "title": title,
        "description": description,
    })

csv_file_path = "property_data.csv"

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = [
        "location", "latitude", "longitude", "property_type", "option", "guests", "number_of_bedrooms", "amenities",
        "seasonality", "base_price", "bathrooms", "bed_type","beds", "neighborhood", "guest_type", "images", "title", "description"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for entry in data:
        writer.writerow(entry)

print(f"CSV file '{csv_file_path}' generated successfully.")






