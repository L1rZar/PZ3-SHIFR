import string

ru_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
en_letters = "abcdefghijklmnopqrstuvwxyz"
# доп. символы
extra_chars = " " + string.digits + string.punctuation

class cipher_text_base:
    """
    __set__: принимает открытый текст -> шифрует -> кладёт шифртекст в obj._<имя>
    __get__: берёт obj._<имя> (шифртекст) -> дешифрует -> возвращает открытый текст
    """

    def __init__(self, ru: str, en: str, extra: str):
        # отдельные алфавиты под каждый язык и регистр
        self._ru_low = ru.lower()
        self._ru_up = ru.upper()
        self._en_low = en.lower()
        self._en_up = en.upper()
        self._sym = extra
        # сюда запишется "_имя"
        self._storage_name = None

    def __set_name__(self, owner, name):
        self._storage_name = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        ciphertext = getattr(obj, self._storage_name, "")
        return self.decrypt(ciphertext)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError("можно присваивать только строку (str).")
        setattr(obj, self._storage_name, self.encrypt(value))

    def ciphertext(self, obj) -> str:
        return getattr(obj, self._storage_name, "")

    def encrypt(self, text: str) -> str:
        raise NotImplementedError("encrypt() должен быть реализован в наследнике.")

    def decrypt(self, text: str) -> str:
        raise NotImplementedError("decrypt() должен быть реализован в наследнике.")

    @staticmethod
    def _shift_char(ch: str, alphabet: str, step: int):
        # цезарь: сдвиг по кругу
        if ch not in alphabet:
            return None
        i = alphabet.index(ch)
        return alphabet[(i + step) % len(alphabet)]

    @staticmethod
    def _mirror_char(ch: str, alphabet: str):
        # атбаш: отражение от конца алфавита
        if ch not in alphabet:
            return None
        i = alphabet.index(ch)
        return alphabet[len(alphabet) - 1 - i]


class caesar_text(cipher_text_base):
    # цезарь: encrypt = +shift, decrypt = -shift
    def __init__(self, ru: str, en: str, extra: str, shift: int):
        super().__init__(ru, en, extra)
        self._shift = int(shift)

    def encrypt(self, text: str) -> str:
        return self._walk_and_shift(text, step=self._shift)

    def decrypt(self, text: str) -> str:
        return self._walk_and_shift(text, step=-self._shift)

    def _walk_and_shift(self, text: str, step: int) -> str:
        out = []
        for ch in text:
            r = self._shift_char(ch, self._ru_low, step)
            if r is not None:
                out.append(r); continue
            r = self._shift_char(ch, self._ru_up, step)
            if r is not None:
                out.append(r); continue
            r = self._shift_char(ch, self._en_low, step)
            if r is not None:
                out.append(r); continue
            r = self._shift_char(ch, self._en_up, step)
            if r is not None:
                out.append(r); continue
            r = self._shift_char(ch, self._sym, step)
            if r is not None:
                out.append(r); continue

            # неизвестный символ не трогаем
            out.append(ch)

        return "".join(out)


class atbash_text(cipher_text_base):
    # атбаш: encrypt и decrypt одинаковые
    def encrypt(self, text: str) -> str:
        return self._walk_and_mirror(text)

    def decrypt(self, text: str) -> str:
        return self._walk_and_mirror(text)

    def _walk_and_mirror(self, text: str) -> str:
        out = []
        for ch in text:
            r = self._mirror_char(ch, self._ru_low)
            if r is not None:
                out.append(r); continue
            r = self._mirror_char(ch, self._ru_up)
            if r is not None:
                out.append(r); continue
            r = self._mirror_char(ch, self._en_low)
            if r is not None:
                out.append(r); continue
            r = self._mirror_char(ch, self._en_up)
            if r is not None:
                out.append(r); continue
            r = self._mirror_char(ch, self._sym)
            if r is not None:
                out.append(r); continue
            # неизвестный символ не трогаем
            out.append(ch)

        return "".join(out)


class message:
    # можно поменять shift на нужный
    caesar = caesar_text(ru_letters, en_letters, extra_chars, shift=5)
    atbash = atbash_text(ru_letters, en_letters, extra_chars)

    def caesar_ciphertext(self) -> str:
        return message.caesar.ciphertext(self)

    def atbash_ciphertext(self) -> str:
        return message.atbash.ciphertext(self)


def main():
    print("напиши строку, я покажу шифровку и дешифровку для цезаря и атбаша.")
    text = input("текст: ")

    m = message()

    # --- цезарь ---
    m.caesar = text
    print("\nцезарь:")
    print("шифртекст :", m.caesar_ciphertext())
    print("дешифровка:", m.caesar)  # чтение возвращает расшифрованное

    # --- атбаш ---
    m.atbash = text
    print("\nатбаш:")
    print("шифртекст :", m.atbash_ciphertext())
    print("дешифровка:", m.atbash)


if __name__ == "__main__":
    main()
