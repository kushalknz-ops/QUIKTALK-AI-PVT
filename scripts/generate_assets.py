"""
scripts/generate_assets.py
Generates all optimized responsive images, WebP variants, favicons,
apple-touch-icon, and OpenGraph social share image for Quiktalk AI (QTK-014, QTK-022).
"""

import os
from PIL import Image, ImageDraw, ImageFont

SRC_LOGO = os.path.join('scripts', 'assets-src', 'logo-master.png')
ASSETS_DIR = 'assets'
ROOT_DIR = '.'

def generate_assets():
    if not os.path.exists(SRC_LOGO):
        print(f"Error: {SRC_LOGO} not found.")
        return

    img = Image.open(SRC_LOGO).convert("RGBA")
    print(f"Loaded master logo: {img.size}, format: {img.format}")

    # 1. Favicon PNGs
    f16 = img.resize((16, 16), Image.Resampling.LANCZOS)
    f16.save(os.path.join(ASSETS_DIR, 'favicon-16x16.png'), 'PNG')
    
    f32 = img.resize((32, 32), Image.Resampling.LANCZOS)
    f32.save(os.path.join(ASSETS_DIR, 'favicon-32x32.png'), 'PNG')

    f48 = img.resize((48, 48), Image.Resampling.LANCZOS)

    # 2. Multi-resolution favicon.ico in root and assets
    f32.save(os.path.join(ROOT_DIR, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    f32.save(os.path.join(ASSETS_DIR, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print("Created favicon.ico and PNGs")

    # 3. Apple Touch Icon (180x180 with dark background padding)
    touch_bg = Image.new("RGBA", (180, 180), (6, 6, 8, 255))
    touch_logo = img.resize((140, 140), Image.Resampling.LANCZOS)
    touch_bg.paste(touch_logo, (20, 20), touch_logo)
    touch_bg.convert("RGB").save(os.path.join(ASSETS_DIR, 'apple-touch-icon.png'), 'PNG')
    touch_bg.convert("RGB").save(os.path.join(ROOT_DIR, 'apple-touch-icon.png'), 'PNG')
    print("Created apple-touch-icon.png")

    # 4. Optimized logo sizes in WebP and PNG
    for size in [(64, 64), (192, 192), (384, 384)]:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        w, h = size
        # WebP
        webp_path = os.path.join(ASSETS_DIR, f'logo-{w}.webp')
        resized.save(webp_path, 'WEBP', quality=90)
        # PNG
        png_path = os.path.join(ASSETS_DIR, f'logo-{w}.png')
        resized.save(png_path, 'PNG', optimize=True)
        print(f"Saved logo-{w}.webp ({os.path.getsize(webp_path)} bytes) & logo-{w}.png ({os.path.getsize(png_path)} bytes)")

    # 5. OpenGraph Card (1200x630)
    og = Image.new("RGB", (1200, 630), (6, 6, 8))
    draw = ImageDraw.Draw(og)

    # Draw subtle ambient gold radial/linear glow
    for r in range(400, 0, -20):
        alpha = int(18 * (1 - r / 400))
        glow_box = [600 - r, 315 - r, 600 + r, 315 + r]
        # Draw concentric soft rounded boxes
        draw.rounded_rectangle(glow_box, radius=r//2, outline=(229, 193, 88), width=1)

    # Place logo on left/center
    og_logo = img.resize((180, 180), Image.Resampling.LANCZOS)
    og.paste(og_logo, (80, 225), og_logo)

    # Text rendering (using default font with fallback sizes)
    # Eyebrow
    draw.text((300, 210), "24/7 AI VOICE RECEPTIONIST · NEW ZEALAND & AUSTRALIA", fill=(229, 193, 88))
    # Title
    draw.text((300, 245), "Quiktalk AI", fill=(255, 255, 255))
    # Tagline
    draw.text((300, 310), "Never miss another call. Answers 24/7 & books the job.", fill=(248, 250, 252))
    draw.text((300, 350), "Built for trades, healthcare, legal, and professional services.", fill=(161, 161, 170))
    # Domain
    draw.text((300, 410), "www.quiktalkai.com", fill=(229, 193, 88))

    og_path = os.path.join(ASSETS_DIR, 'og-image.jpg')
    og.save(og_path, 'JPEG', quality=92)
    print(f"Created og-image.jpg ({os.path.getsize(og_path)} bytes)")

if __name__ == '__main__':
    generate_assets()
