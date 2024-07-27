from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass
from typing import Tuple, Optional
import logging
from pathlib import Path
from enum import Enum, auto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextAlignment(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()

@dataclass
class TextConfig:
    text: str
    font_size: int
    position: Tuple[int, int]
    alignment: TextAlignment = TextAlignment.LEFT
    color: str = "#000000"
    max_width: Optional[int] = None

class ParkingPermit:
    def __init__(self, size: Tuple[int, int], bg_color: str = '#FFFFFF'):
        self.width, self.height = size
        self.image = Image.new('RGB', size, bg_color)
        self.draw = ImageDraw.Draw(self.image)
        self.font_path = Path("arial.ttf")

    def fit_text(self, text: str, font_size: int, max_width: int) -> ImageFont.FreeTypeFont:
        font = ImageFont.truetype(str(self.font_path), font_size)
        while self.draw.textbbox((0, 0), text, font=font)[2] > max_width:
            font_size -= 1
            if font_size <= 0:
                raise ValueError("Text cannot fit within the specified width")
            font = ImageFont.truetype(str(self.font_path), font_size)
        return font

    def add_logo(self, logo_path: Path, size: Tuple[int, int], position: Tuple[int, int]):
        try:
            with Image.open(logo_path) as logo:
                logo = logo.convert('RGBA')
                logo.thumbnail(size)
                self.image.paste(logo, position, logo)
        except FileNotFoundError:
            logger.error(f"Logo file not found: {logo_path}")

    def add_text(self, config: TextConfig):
        font = (
            self.fit_text(config.text, config.font_size, config.max_width)
            if config.max_width
            else ImageFont.truetype(str(self.font_path), config.font_size)
        )
        bbox = self.draw.textbbox((0, 0), config.text, font=font)
        text_width = bbox[2] - bbox[0]
        x, y = config.position

        if config.alignment == TextAlignment.CENTER:
            x -= text_width // 2
        elif config.alignment == TextAlignment.RIGHT:
            x -= text_width

        self.draw.text((x, y), config.text, fill=config.color, font=font)

    def save(self, filename: Path):
        self.image.save(filename)
        logger.info(f"Image saved as {filename}")

    def show(self):
        self.image.show()

def create_parking_permit(name: str, position: str, permit_number: str, valid_until: str) -> ParkingPermit:
    permit = ParkingPermit((900, 650), bg_color='#FFFFFF')

    permit.add_logo(Path('logo.png'), (100, 100), (50, 50))

    text_configs = [
        TextConfig("Stampus Studentförening", 48, (450, 60), TextAlignment.CENTER, "#000000", 800),
        TextConfig("PARKERINGSTILLSTÅND", 36, (450, 130), TextAlignment.CENTER, "#666666", 800),
        TextConfig("Namn", 24, (50, 250), TextAlignment.LEFT, "#999999", 800),
        TextConfig(name, 32, (50, 280), TextAlignment.LEFT, "#000000", 800),
        TextConfig("Befattning", 24, (50, 350), TextAlignment.LEFT, "#999999", 800),
        TextConfig(position, 32, (50, 380), TextAlignment.LEFT, "#000000", 800),
        TextConfig("Tillståndsnr", 24, (50, 450), TextAlignment.LEFT, "#999999", 800),
        TextConfig(permit_number, 32, (50, 480), TextAlignment.LEFT, "#000000", 800),
        TextConfig("Giltigt till", 24, (450, 450), TextAlignment.LEFT, "#999999", 800),
        TextConfig(valid_until, 32, (450, 480), TextAlignment.LEFT, "#000000", 800),
        TextConfig("Detta tillstånd måste vara synligt i fordonet", 18, (450, 600), TextAlignment.CENTER, "#666666", 800),
    ]

    for config in text_configs:
        permit.add_text(config)

    return permit

if __name__ == "__main__":
    permit = create_parking_permit("Måns Alklint", "Vice Ordförande", "001234", "31/12/2024")
    permit.save(Path('parkeringstillstand.png'))