# stegnographer
A lightweight Python tool that hides and extracts secret text messages inside PNG images using Least Significant Bit (LSB) steganography.

---

## Features

* **Lossless Encoding:** Embeds payload bits directly into image pixel data without noticeable distortion.
* **Header-Length Architecture:** Stores message length as a 32-bit header at the start of the file, removing the need for end-of-message delimiters.
* **UTF-8 Support:** Handles standard ASCII characters, unicode text, and special symbols.

---

## How It Works

1. The input string is converted into a continuous stream of UTF-8 bits.
2. A 32-bit binary integer representing the total bit length is prefixed to the payload.
3. The script traverses image pixels and replaces the least significant bit (LSB) of the red channel byte with payload bits:
   `channel = (channel & ~1) | bit`
4. When decoding, the tool reads the first 32 bits to determine payload size, extracts only the required bits, and reconstructs the original string.

> **Note:** Only lossless formats like **PNG** preserve the modified bits. Lossy compression formats (such as JPEG) will overwrite LSB data.

---

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/suhaggggg/stegnographer.git](https://github.com/suhaggggg/stegnographer.git)
   cd stegnographer
