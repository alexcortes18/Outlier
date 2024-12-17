class ArticleManager:
    def __init__(self, article_text, options=None):
        if options is None:
            options = {}
        
        self.article_text = article_text
        
        self.pages = []
        self.words = []
        # Set the Options objects variables either from the Options itself or the default 12 and 20 values.
        # Also for the payment_structure.
        self.options = {
            'words_per_line': options.get('words_per_line', 12),
            'lines_per_page': options.get('lines_per_page', 20),
            'payment_structure': options.get('payment_structure', {
                0: 0,
                1: 30,
                2: 30,
                3: 60,
                4: 60,
                'default': 100,
            })
        }

    def split_into_pages(self):
        # First check if 'article_text' is a string and if not, raise an error.
        if not isinstance(self.article_text, str):
            raise Exception("The input article must be a string! Please try again.")
        
        words_per_line = self.options['words_per_line']
        lines_per_page = self.options['lines_per_page']
        
        current_page = []
        current_line = []
        word_count = 0
    
        # Process the article in chunks of 960 words at a time, which are 4 pages.
        chunk_size = 960 
        words = self.article_text.split()
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            for word in chunk:
                current_line.append(word)
                word_count += 1
                # If we reach the max words per line, finalize the line
                if len(current_line) == words_per_line:
                    current_page.append(" ".join(current_line))
                    current_line = []
                # If the page is full, save it and start a new page
                if len(current_page) == lines_per_page:
                    self.pages.append("\n".join(current_page))
                    current_page = []
        # Handle any remaining words/lines
        if current_line:
            current_page.append(" ".join(current_line))
        if current_page:
            self.pages.append("\n".join(current_page))

        print(f"Processed {word_count} words into {len(self.pages)} page(s).")

    def calculate_payment(self):
        payment_structure = self.options['payment_structure']
        total_pages = len(self.pages)

        # Find the payment for the total number of pages
        payment = payment_structure.get(total_pages, payment_structure['default'])
        return payment

    def display_pages(self):
        payment = self.calculate_payment()

        print(f"Total Pages: {len(self.pages)}")
        print(f"Payment Due: ${payment}")

        for index, page in enumerate(self.pages):
            print(f"\nPage {index + 1}:\n{page}\n")

    def process_article(self):
        self.split_into_pages()
        self.display_pages()

# Example usage
article_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore
et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Ut enim ad 
minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non 
proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Here is some more text just to test if it is 
working correctly. Your it to gave life whom as. Favourable dissimilar resolution led for and had. At play much to time
four many. Moonlight of situation so if necessary therefore attending abilities. Calling looking enquire up me to in 
removal. Park fat she nor does play deal our. Procured sex material his offering humanity laughing moderate can. 
Unreserved had she nay dissimilar admiration interested. Departure performed exquisite rapturous so ye me resources. 
As absolute is by amounted repeated entirely ye returned. These ready timed enjoy might sir yet one since. Years drift 
never if could forty being no. On estimable dependent as suffering on my. Rank it long have sure in room what as he. 
Possession travelling sufficient yet our. Talked vanity looked in to. Gay perceive led believed endeavor. Rapturous no
of estimable oh therefore direction up. Sons the ever not fine like eyes all sure."""

article_manager = ArticleManager(article_text)
article_manager.process_article()