"""
Upload and optimize images to Cloudinary
Run this script to upload all public images to Cloudinary with proper public IDs
"""
import os
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Configure Cloudinary (set these in your environment)
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', 'dmwulp3dl'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Image mappings: local file -> Cloudinary public_id
IMAGES_TO_UPLOAD = {
    # Background images
    'public/hero.png': 'synelweb/backgrounds/hero',
    'public/contact.png': 'synelweb/backgrounds/contact',
    'public/contactpage.png': 'synelweb/backgrounds/contactpage',
    'public/packages.png': 'synelweb/backgrounds/packages',
    'public/packagespage.png': 'synelweb/backgrounds/packagespage',
    'public/projects.png': 'synelweb/backgrounds/projects',
    'public/projectspage.png': 'synelweb/backgrounds/projectspage',
    'public/review.png': 'synelweb/backgrounds/review',
    'public/reviewpage.png': 'synelweb/backgrounds/reviewpage',
    
    # Logos
    'public/darklogo.png': 'synelweb/logos/darklogo',
    'public/lightlogo.png': 'synelweb/logos/lightlogo',
    'public/logo.png': 'synelweb/logos/logo',
    'public/logo-192.png': 'synelweb/logos/logo-192',
    'public/logo-512.png': 'synelweb/logos/logo-512',
}

def upload_image(local_path, public_id):
    """Upload a single image to Cloudinary with optimizations"""
    try:
        print(f"Uploading {local_path} -> {public_id}...")
        
        result = cloudinary.uploader.upload(
            local_path,
            public_id=public_id,
            overwrite=True,
            resource_type="image",
            # Optimization settings
            quality="auto:good",
            fetch_format="auto",
            flags=["progressive", "lossy"],
            # Generate responsive breakpoints
            responsive_breakpoints={
                "create_derived": True,
                "bytes_step": 20000,
                "min_width": 320,
                "max_width": 1920,
                "max_images": 6
            }
        )
        
        print(f"✅ Uploaded: {result['secure_url']}")
        return result
        
    except Exception as e:
        print(f"❌ Error uploading {local_path}: {str(e)}")
        return None

def main():
    """Main upload function"""
    print("Starting Cloudinary image upload...")
    print("=" * 60)
    
    # Get the frontend directory
    frontend_dir = Path(__file__).parent
    
    uploaded = 0
    failed = 0
    
    for local_path, public_id in IMAGES_TO_UPLOAD.items():
        full_path = frontend_dir / local_path
        
        if not full_path.exists():
            print(f"⚠️  File not found: {full_path}")
            failed += 1
            continue
            
        result = upload_image(str(full_path), public_id)
        if result:
            uploaded += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Upload complete: {uploaded} successful, {failed} failed")
    
    if uploaded > 0:
        print("\n✅ Images are now available at:")
        print("https://res.cloudinary.com/dmwulp3dl/image/upload/")

if __name__ == "__main__":
    main()
