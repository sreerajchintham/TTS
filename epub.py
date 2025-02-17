
from ebooklib import epub
from bs4 import BeautifulSoup
import os

def create_epub(novel_title, chapters):
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('000001')
    book.set_title(novel_title)
    book.set_language('en')
    book.add_author('Sreeraj')

    # List to store chapter objects
    epub_chapters = []

    for i, (title, content) in enumerate(chapters):
        chapter = epub.EpubHtml(title=title, file_name=f'chap_{i+1}.xhtml', lang='en')
        chapter.content = f"<h1>{title}</h1><p>{content}</p>"

        book.add_item(chapter)
        epub_chapters.append(chapter)

    # Define Table of Contents
    book.toc = (epub_chapters)

    # Add default navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define spine (reading order)
    book.spine = ['nav'] + epub_chapters

    # Write to file
    epub.write_epub(f"{novel_title}.epub", book, {})

    print(f"EPUB file '{novel_title}.epub' created successfully!")

# Example: Creating an EPUB from multiple chapters
example_chapters = [
    ("Chapter 1: The Beginning", "This is the first chapter content."),
    ("Chapter 2: A New Journey", "This is the second chapter content."),
    ("Chapter 3: The Conflict", "This is the third chapter content.")
]

create_epub("My Novel", example_chapters)
