import unittest
from PIL import Image
import io

class TestImageResize(unittest.TestCase):
    def test_resize_image_success(self):
        original_image = Image.new('RGB', (800, 600), color='red')
        resized_image = self.resize_image(original_image, (400, 300))
        self.assertEqual(resized_image.size, (400, 300))

    def test_resize_image_invalid_format(self):
        original_image = Image.new('P', (800, 600), color='red')
        with self.assertRaises(ValueError):
            self.resize_image(original_image, (400, 300))

    def resize_image(self, image, size):
        if image.mode not in ['RGB', 'RGBA']:
            raise ValueError("Image cannot be written in JPEG format")
        return image.resize(size)

if __name__ == '__main__':
    unittest.main()