from PIL import Image
from pathlib import Path

WORKDIR = Path.cwd()
result = {
    'oldSize': 0,
    'newSize': 0
}


def transparencyCheck(image: Image):
    try:
        alpha_channel = image.getchannel('A').getcolors()
    except ValueError:
        return image, False
    if len(alpha_channel) == 1 and alpha_channel[0][1] == 255:
        return image, False
    else:
        return image, True


def changeFileExtension(filename: str, ext: str):
    ext = ext.lower().strip('.').strip('')
    return filename.split('.')[0] + '.' + ext


def getFilesToConvert(filenames: list):
    toConvert = []
    for filename in filenames:
        image = Image.open(filename)
        image, transparent = transparencyCheck(image)
        if not transparent and image.mode != 'P':
            toConvert.append(image)
    return toConvert


PNGFiles = [pngImage.name for pngImage in WORKDIR.glob('*.png')]
toConvert = getFilesToConvert(PNGFiles)
print(f'{len(PNGFiles)} PNG Files in dir, {len(toConvert)} to compress')

if len(PNGFiles) == 0:
    print('No PNG files in dir!')
elif len(toConvert) == 0:
    print('Nothing to convert!')
else:
    for pngImage in toConvert:
        pngImagePath = WORKDIR.joinpath(pngImage.filename)
        pngImageSize = round(pngImagePath.stat().st_size / 1024, 2)
        result['oldSize'] += pngImageSize
        jpgImage = pngImage.convert('RGB')
        newFilename = changeFileExtension(pngImage.filename, 'jpg')
        jpgImage.save(newFilename, optimize=True)
        sizeAfter = round(WORKDIR.joinpath(newFilename).stat().st_size / 1024, 2)
        result['newSize'] += sizeAfter
        pngImagePath.unlink()
        print(f'Convert {pngImage.filename} /// Compress from {pngImageSize} kB to {sizeAfter} kB')

    print('=' * 30)
    print(f'All files compressed from {result["oldSize"]} kB to {result["newSize"]} kB')
