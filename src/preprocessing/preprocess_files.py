import base64
from io import BytesIO
from PIL import Image
import logging
import fitz
from typing import List




class FileProcessor:
    def __init__(self, file_path:str) -> None:
        self.file_path  = file_path

    def pdf2image(self):
        pass

    def extract_plots(self):
        pass

    def extract_results(self):
        pass



def convert_pdf_bytes_to_images(pdf_bytes: bytes) -> List[Image.Image]:
    """Converts PDF bytes into a list of PIL images."""
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    return [
        Image.frombytes(
            "RGB",
            [page.get_pixmap().width, page.get_pixmap().height],
            page.get_pixmap().samples,
        )
        for page in pdf_document
    ]

class DataPreprocessor:
    def __init__(self, doc_data: bytes, img_size: tuple = (1024, 1024)):
        """- doc_data:
        - img_size: New img size as a tuple (width, height)"""
        self.doc_data = doc_data
        self.img_size = img_size

    @staticmethod
    def convert_pdf_to_img(pdf_content):
        """Transforms input pdf bytes into a list of PIL images"""
        return convert_pdf_bytes_to_images(pdf_content)

    @staticmethod
    def bytes_to_pil_image(image_bytes):
        """Converts bytes image into PIL Image"""
        image_stream = BytesIO(image_bytes)
        image = Image.open(image_stream)
        return image

    def resize_images(self):
        """
        Resize images to the specified size.
        """
        self.resized_imgs = [img.resize(self.img_size) for img in self.imgs]

    def encode_images(self):
        """Encodes images to base64 format, as required by OpenAI. Returns a list of encoded images, one for each page in the .pdf"""
        self.encoded_imgs = []
        for img in self.resized_imgs:
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            self.encoded_imgs.append(
                base64.b64encode(buffered.getvalue()).decode("utf-8")
            )

    def __call__(self):
        self.imgs = (
            self.convert_pdf_to_img(self.doc_data)
            if self.doc_data[:4] == b"%PDF"
            else [self.bytes_to_pil_image(self.doc_data)]
        )
        self.resize_images()
        self.encode_images()
        return self.encoded_imgs