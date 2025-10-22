import os
from PIL import Image, ImageDraw, ImageFont
import segno

# Configurações principais
OUTPUT_DIR = "output"
LOGO_PATH = "assets/logo.png"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
IMAGE_SIZE = int(os.environ.get("IMAGE_SIZE", 500))
COUNT = int(os.environ.get("COUNT", 64))

# Cores
PRIMARY_RGB = (26, 19, 163)   # Faixa do rótulo (#1a13a3)
SECONDARY_RGB = (0, 26, 63)   # Borda ao redor do card (#001a3f)
LABEL_TEXT_RGB = (255, 255, 255)
BG_RGB = (255, 255, 255)      # Fundo geral

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_qrcode(text: str):
    """Gera QR Code preto puro, fundo branco (100% legível)"""
    qr = segno.make(text, micro=False)
    buffer_path = os.path.join(OUTPUT_DIR, f"tmp_{text}.png")
    qr.save(buffer_path, scale=10, border=0, dark='black', light='white')
    img = Image.open(buffer_path).convert("RGBA")
    os.remove(buffer_path)
    return img


def add_logo_to_qr(qr_image: Image.Image, logo_path: str, logo_scale=0.25):
    """Adiciona logo central, máximo 25% do QR"""
    if not os.path.exists(logo_path):
        return qr_image
    logo = Image.open(logo_path).convert("RGBA")
    qr_w, qr_h = qr_image.size
    logo_size = int(qr_w * logo_scale)
    logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
    lx = (qr_w - logo.width) // 2
    ly = (qr_h - logo.height) // 2
    qr_image.paste(logo, (lx, ly), logo)
    return qr_image


def compose_card(qr_with_logo, label_text):
    """Cria card com borda azul, faixa de rótulo e fundo branco"""
    border = int(IMAGE_SIZE * 0.05)  # borda ao redor
    label_height = int(IMAGE_SIZE * 0.25)
    canvas_w = IMAGE_SIZE + border * 2
    canvas_h = IMAGE_SIZE + label_height + border * 2

    # Fundo branco geral
    canvas = Image.new("RGB", (canvas_w, canvas_h), BG_RGB)

    # Borda azul escuro ao redor do card (QR + rótulo)
    border_rect = Image.new(
        "RGB", (IMAGE_SIZE + border, IMAGE_SIZE +
                label_height + border), SECONDARY_RGB
    )
    canvas.paste(border_rect, (border // 2, border // 2))

    # Área interna (QR + rótulo)
    inner = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE + label_height), BG_RGB)
    canvas.paste(inner, (border, border))

    # QR Code centralizado
    qr_resized = qr_with_logo.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
    canvas.paste(qr_resized, (border, border), qr_resized)

    # Faixa do rótulo
    label_area = Image.new("RGB", (IMAGE_SIZE, label_height), PRIMARY_RGB)
    canvas.paste(label_area, (border, border + IMAGE_SIZE))

    # Texto do rótulo centralizado
    draw = ImageDraw.Draw(canvas)
    font_size = max(22, int(label_height * 0.45))
    font = ImageFont.truetype(
        FONT_PATH, font_size) if FONT_PATH else ImageFont.load_default()
    try:
        bbox = draw.textbbox((0, 0), label_text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        w, h = draw.textsize(label_text, font=font)
    tx = (canvas_w - w) // 2
    ty = border + IMAGE_SIZE + (label_height - h) // 2
    draw.text((tx, ty), label_text, fill=LABEL_TEXT_RGB, font=font)

    return canvas


def main():
    for i in range(1, COUNT + 1):
        label = f"MESA - {i:02d}"
        print(f"Gerando {label}...")
        qr = generate_qrcode(str(i))
        with_logo = add_logo_to_qr(qr, LOGO_PATH)
        final = compose_card(with_logo, label)
        output_path = os.path.join(OUTPUT_DIR, f"mesa_{i:02d}.png")
        final.save(output_path, "PNG")
    print("✅ Todos os QR Codes foram gerados em:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
