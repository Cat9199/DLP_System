import re
from cryptography.fernet import Fernet

class CreditCardProcessor:
    def __init__(self, content: str):
        self.content = content
        self.lines = self.content.splitlines()
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def search_credit_cards(self) -> list:
        matches = []
        for i, line in enumerate(self.lines):
            for match in re.finditer(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b', line):
                matches.append((match.group(), i))
        return matches

    def encrypt_credit_card(self, credit_card: str) -> str:
        encrypted_cc = self.cipher_suite.encrypt(credit_card.encode())
        return encrypted_cc.decode()

    def update_content_with_encrypted_ccs(self, encrypted_ccs: list) -> str:
        for encrypted_cc, line_index in encrypted_ccs:
            self.lines[line_index] = re.sub(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b', encrypted_cc, self.lines[line_index], count=1)
        return '\n'.join(self.lines)

    def process_content(self) -> None:
        credit_cards = self.search_credit_cards()
        if credit_cards:
            encrypted_ccs = [(self.encrypt_credit_card(cc), idx) for cc, idx in credit_cards]
            updated_content = self.update_content_with_encrypted_ccs(encrypted_ccs)
            print("\nUpdated Content:\n")
            print(updated_content)
            print("\nEncryption Key:")
            print(self.key.decode())
        else:
            print("No credit card numbers found.")

if __name__ == '__main__':
    with open('test.txt', 'r') as file:
        content = file.read()
    processor = CreditCardProcessor(content)
    processor.process_content()
