"""Download books from the website in html, text, doc, and pdf format. 
Compress these books using Hoffman coding technique. Find the compression ratio."""


import os
import heapq
import PyPDF2
import docx
from bs4 import BeautifulSoup
from collections import defaultdict

class FileProcessor:
    def __init__(self):
        pass

    def read_file(self, file_path):
        # Determine file type based on extension
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".txt":
            return self.process_txt(file_path)
        elif file_extension == ".pdf":
            return self.process_pdf(file_path)
        elif file_extension == ".docx":
            return self.process_docx(file_path)
        elif file_extension == ".html":
            return self.process_html(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def process_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def process_pdf(self, file_path):
        text_content = ""
        with open(file_path, 'rb', encoding='utf-8') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                text_content += page.extract_text()
        return text_content

    def process_docx(self, file_path):
        document = docx.Document(file_path)
        text_content = ""
        for paragraph in document.paragraphs:
            text_content += paragraph.text + "\n"
        return text_content

    def process_html(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, "html.parser")
            return soup.get_text()
    
class TreeNode:
    def __init__ (self, character, frequency):
        self.character = character
        self.frequency = frequency
        self.left = self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency
    
class HuffmanEncoder:
    def build_tree(self, content_string):
        if not content_string:
            raise ValueError("Input file empty")
        if not all (ord(char) < 128 for char in content_string):
            raise ValueError("Contains non ASCII characters")
        
        unique_chars = list(set(content_string)) #set contains only unique characters
        freq_dict = {{char : content_string.count(char) for char in unique_chars}}

        heap = [TreeNode(char, freq) for char, freq in freq_dict.items()]
        heapq.heapify(heap)

        #merge all nodes until there is one tree
        while len(heap)> 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            combined_freq = left.frequency + right.frequency
            merged_node = TreeNode(None, combined_freq)
            merged_node.left = left
            merged_node.right = right
            heapq.heappush(heap, merged_node)

        return heap[0]

    def create_codebook(self,node, prefix="", codebook = None):
        if codebook is None:
            codebook = {}

        if node is not None:
            if node.character is not None:
                codebook[node.character] = prefix
            else:
                self.create_codebook(node.left, prefix+"0",codebook)
                self.create_codebook(node.right, prefix+"1", codebook)
        return codebook
    
    def calc_encodedSize(self, content_string, codebook):
        frequency = {char: content_string(char) for char in set(content_string)}
        total_bits = sum(frequency[char]*len(codebook[char]) for char in frequency)
        return total_bits
    
    def decode(self, encoded_data, huffman_tree_root):
        decoded_string = ""
        current_node = huffman_tree_root
        for bit in encoded_data:
            current_node = current_node.left if bit == "0" else current_node.right
            if current_node.left is None and current_node.right is None:
                decoded_string += current_node.character
                current_node = huffman_tree_root
            return decoded_string

if __name__ == "__main__":
    file_processor = FileProcessor()
    encoder = HuffmanEncoder()

    file_paths = [
        'da_vinci.txt',
        'lorem.py',
        'aggtm.docx',
        'test.cpp'
    ]

    for file_path in file_paths:
        print(f"\nProcessing file: {file_path}")
        print("-" * 35)
        try:
            content = file_processor.read_file(file_path)
            huffman_tree_root = encoder.build_tree(content)
            huffman_codes = encoder.create_codebook(huffman_tree_root)
            encoded_data = "".join(huffman_codes[char] for char in content)
            
            original_size = len(content) * 8  # Original size in bits
            encoded_size = encoder.calculate_encoded_size(content, huffman_codes)
            
            print("Huffman Codes:", huffman_codes)
            print(f"Original Size (bits): {original_size}")
            print(f"Encoded Size (bits): {encoded_size}")
            print(f"Compression Ratio: {(encoded_size / original_size) * 100:.2f}%")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
