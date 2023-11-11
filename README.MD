# Enables multiprocessing with caching, eliminating the need for __main__, and ensuring unique results without duplicates

## pip install multiprocca


## Tested against Python 3.11 / Windows 10


```python
import sys
from a_cv_imwrite_imread_plus import open_image_in_cv
from locate_pixelcolor_c import search_colors
import subprocess
import numpy as np
import cv2
from list_all_files_recursively import get_folder_file_complete_path
from multiprocca import start_multiprocessing
from multiprocca.proclauncher import MultiProcExecution 

def function_subxxx(x):
    exec("import cv2", globals())
    exec("import numpy as np", globals())

    pic = cv2.imread(x)
    b, g, r = pic[..., 0], pic[..., 1], pic[..., 2]
    return np.where(((b == 255) & (g == 255) & (r == 255)))


def function_sub1(file):
    exec("import subprocess", globals())
    exec("import numpy as np", globals())

    with open(file, mode="rb") as f:
        da = f.read()
    p = subprocess.run(
        [
            r"""C:\Program Files\Tesseract-OCR\tesseract.exe""",
            "-c",
            "tessedit_create_tsv=1",
            "-l",
            "por",
            "-",
            "stdout",
        ],
        input=da,
        capture_output=True,
    )
    return p.stderr, p.stdout


def function_sub(pic, colors):
    try:
        exec("""import sys""", globals())
        exec("""import numpy as np""", globals())
        exec("""import cv2""", globals())
        exec("""from locate_pixelcolor_c import search_colors""", globals())
        exec("""from a_cv_imwrite_imread_plus import open_image_in_cv""", globals())
        colorsrev = np.array([list(q) for q in (map(reversed, colors))], dtype=np.uint8)

        pic = open_image_in_cv(pic, channels_in_output=3)
        sc = search_colors(pic=pic, colors=colorsrev)
        if len(sc) == 1:
            if np.sum(sc) == 0:
                if not (pic[0, 0]) in colorsrev:
                    sc = np.array([[-1, -1]], dtype=np.int32)
        return sc
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.stderr.flush()
        return np.array([[-1, -1]], dtype=np.int32)


colors1 = (
    (69, 71, 66),
    (255, 255, 255),
    (153, 155, 144),
    (55, 57, 52),
    (136, 138, 127),
    (56, 58, 53),
    (54, 56, 51),
    (0, 180, 252),
)
allpi = [
    x.path
    for x in get_folder_file_complete_path(r"C:\testfolderall")
    if x.ext == ".png"
]
f = [
    MultiProcExecution(fu=function_sub, args=(o, colors1), kwargstuple=())
    for o in allpi
]
formated_data, raw_data = start_multiprocessing(
    it=f,
    usecache=True,
    processes=5,
    chunks=1,
    print_stdout=False,
    print_stderr=False,
)


def start_multiprocessing(
    it,
    usecache=True,
    processes=5,
    chunks=1,
    print_stdout=False,
    print_stderr=True,
):
    r"""
    Initiates parallel processing on the given iterable using multiprocessing.

    Args:
        it (iterable): The iterable containing data to be processed in parallel.
        usecache (bool, optional): Flag indicating whether to enable caching of results.
                                   Defaults to True.
        processes (int, optional): The number of parallel processes to be spawned.
                                   Defaults to 5.
        chunks (int, optional): The number of items to be processed in each task chunk.
                                Defaults to 1.
        print_stdout (bool, optional): Flag indicating whether to print stdout of subprocesses.
                                       Defaults to False.
        print_stderr (bool, optional): Flag indicating whether to print stderr of subprocesses.
                                       Defaults to True.

    Returns:
        tuple: A tuple containing two elements:
            1. A dictionary mapping input indices to corresponding processed results.
            2. A list containing essential data, including hash_and_result, hash_int_map_small,
               original_object, and mapping_dict.


```