Some simple image editing automation tools. <br>
Made with Python 3, compiled with PyInstaller.

---

---

`bulk_image_converter` : A quick tool to convert a folder full of images to a different format. <br>
        Even works with mixed input formats, also a prefix can be added optionally. <br>
        It will automatically skip non-images and images that are already in the target format. <br>
        Input formats: PNG, JPEG, WebP, BMP, GIF, HEIC <br>
        Output formats: PNG, JPEG, WebP, BMP, GIF <br>
        for example: <br> <br>
          before <br>
                folder_with_images <br>
                  ┝ image001.jpeg <br>
                  ┝ someOtherImage.png <br>
                  ┕ AnotherImage.bmp <br> <br>
          after <br>
                folder_with_images <br>
                  ┝ image001.jpeg <br>
                  ┝ convert_image001.png <br>
                  ┝ someOtherImage.png       `will not generate a duplicate because it is already in the target format` <br>
                  ┝ AnotherImage.bmp <br>
                  ┕ convert_AnotherImage.png <br>

---

`image_cropper` : A simple tool to crop an image to a set aspect ratio, this tool only works with a single image at a time. <br>
        Useful for website design where a lot of images need to be the same aspect ratio. <br>
        It will ask for some information, if you don't know what it means, just press ENTER, there's a default for everything. <br>
        Input formats: PNG, JPEG, WebP, BMP, GIF (It isn't specified in-code, more formats may work, but may not. HEIC will not work, use bulk_image_converter for it) <br>
        Output formats: PNG, JPEG, WebP (Use bulk_image_converter for BMP or GIF output)
