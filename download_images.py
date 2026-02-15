import os
import requests

# Mapping of filenames to image URLs (Using reliable placeholder/demo images)
# In a real scenario, these would be actual book cover URLs. 
# We use a placeholder service that generates images with text for robustness.
images = {
    "gatsby.jpg": "https://covers.openlibrary.org/b/id/8432047-L.jpg",
    "1984.jpg": "https://covers.openlibrary.org/b/id/7222246-L.jpg",
    "mockingbird.jpg": "https://covers.openlibrary.org/b/id/12617750-L.jpg",
    "pride.jpg": "https://covers.openlibrary.org/b/id/8259447-L.jpg",
    "catcher.jpg": "https://covers.openlibrary.org/b/id/10582855-L.jpg",
    "hobbit.jpg": "https://covers.openlibrary.org/b/id/6979861-L.jpg"
}

save_dir = "website/static/images"
os.makedirs(save_dir, exist_ok=True)

def download_images():
    print("Downloading book covers...")
    for filename, url in images.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(os.path.join(save_dir, filename), 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {filename} (Status: {response.status_code})")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

if __name__ == "__main__":
    download_images()
