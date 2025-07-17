import time

import polib
from googletrans import Translator

translator = Translator()


def translate_text(text):
    try:
        translated = translator.translate(text, src="en", dest="es")
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # fallback to original


def auto_translate_po(file_path, output_path):
    po = polib.pofile(file_path)
    for entry in po.untranslated_entries():
        if entry.msgid.strip():
            entry.msgstr = translate_text(entry.msgid)
            time.sleep(0.5)  # pause for 0.5 seconds
    po.save(output_path)
    print(f"Translated file saved as {output_path}")


if __name__ == "__main__":
    auto_translate_po("messages.po", "translated.po")
# 🔧 Usage
# auto_translate_po("messages.po", "translated.po")
