from googletrans import Translator


def translate(text, source_language, dest_language):
    translator = Translator()
    try:
        result = translator.translate(text, src=source_language, dest=dest_language)
        return result.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text  # fallback: return original
