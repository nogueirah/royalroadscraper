from ebooklib import epub


class EpubBook():
    epub_file = epub.EpubBook()

    def __init__(self, title: str, author: str) -> None:
        self.epub_file.set_title(title)
        self.epub_file.add_author(author)
        self.epub_file.add_item(epub.EpubNcx())        
        self.epub_file.add_item(epub.EpubNcx())
        self.epub_file.add_item(epub.EpubNav())
        self.epub_file.spine = ["nav"]        

    def new_chapter(self, chapter_title: str, chapter_content: str):
        chapter = epub.EpubHtml(title=chapter_title,
                                file_name=sanitize_filename(chapter_title +
                                                            ".xhtml"),
                                lang="hr")
        chapter.content = (chapter_content)
        self.epub_file.add_item(chapter)
        self.epub_file.spine = self.epub_file.spine + [chapter]

    def write_file(self):
        epub.write_epub(sanitize_filename(self.epub_file.title + ".epub"),
                        self.epub_file, {})

def sanitize_filename(filename) -> str:
    return "".join(x for x in filename if x.isalnum() or x in(" ", "."))
