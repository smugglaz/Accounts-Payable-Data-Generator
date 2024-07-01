import random
import nltk
from nltk.corpus import words
import yaml
from typing import List, Dict

# Download required NLTK data
nltk.download('words', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


class DescriptionGenerator:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.templates = self.config['description_templates']
        self.adjectives = self.config['adjectives']
        self.nouns = self.config['nouns']
        self.verbs = self.config['verbs']
        self.brand_names = self.config['brand_names']
        self.model_prefixes = self.config['model_prefixes']
        self.model_suffixes = self.config['model_suffixes']

        self.word_list = set(words.words())

    def generate_description(self, category: str) -> str:
        template = random.choice(self.templates[category])
        description = self._fill_template(template, category)
        return description

    def _fill_template(self, template: str, category: str) -> str:
        words = template.split()
        filled_words = []

        for word in words:
            if word.startswith('{') and word.endswith('}'):
                placeholder = word[1:-1]
                if placeholder == 'ADJ':
                    filled_words.append(random.choice(self.adjectives[category]))
                elif placeholder == 'NOUN':
                    filled_words.append(random.choice(self.nouns[category]))
                elif placeholder == 'VERB':
                    filled_words.append(random.choice(self.verbs[category]))
                elif placeholder == 'BRAND':
                    filled_words.append(random.choice(self.brand_names[category]))
                elif placeholder == 'MODEL':
                    filled_words.append(self._generate_model_number())
                else:
                    filled_words.append(self._generate_random_word(placeholder))
            else:
                filled_words.append(word)

        return ' '.join(filled_words)

    def _generate_model_number(self) -> str:
        prefix = random.choice(self.model_prefixes)
        suffix = random.choice(self.model_suffixes)
        number = random.randint(100, 9999)
        return f"{prefix}{number}{suffix}"

    def _generate_random_word(self, pos: str) -> str:
        while True:
            word = random.choice(list(self.word_list))
            if nltk.pos_tag([word])[0][1].startswith(pos):
                return word

    def generate_item_description(self, category: str) -> Dict[str, str]:
        description = self.generate_description(category)
        brand = random.choice(self.brand_names[category])
        model = self._generate_model_number()

        return {
            "description": description,
            "brand": brand,
            "model": model
        }