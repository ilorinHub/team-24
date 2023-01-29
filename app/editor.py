import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
from app.contants import IMAGE_EXTENSIONS

from app.methods import splitext

# Create a Modified TextEdit Class
class TextEdit(qtw.QTextEdit):

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():

            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = gui.QImage(u.toLocalFile())
                    document.addResource(gui.QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return
        super(TextEdit, self).insertFromMimeData(source)
