import platform
import subprocess
import sys
import multiprocessing
import os
import dill

use_cache_dict = False
iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
        "cwd": os.getcwd(),
    }
else:
    invisibledict = {}


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


    """
    multidict = {}

    multidict["procdata"] = it
    multidict["processes"] = processes
    multidict["chunks"] = chunks
    multidict["usecache"] = usecache

    v = dill.dumps(multidict, protocol=dill.HIGHEST_PROTOCOL)
    osenv = os.environ.copy()
    osenv["___START___MULTIPROCESSING___"] = "1"
    p = subprocess.run(
        [sys.executable, __file__],
        **invisibledict,
        env=osenv,
        capture_output=True,
        input=b"STARTDATASTARTDATASTARTDATA" + v + b"ENDDATAENDDATAENDDATAENDDATA",
    )
    if print_stderr:
        for ste in p.stderr.decode("utf-8", "backslashreplace"):
            sys.stderr.write(ste)
            sys.stderr.flush()
    d = dill.loads(
        p.stdout.split(b"ENDEND1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1ENDEND")[1].split(
            b"DNE1YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYDNE1"
        )[0]
    )
    if print_stdout:
        print(d)
    (
        hash_and_result,
        hash_int_map_small,
        original_object,
        mapping_dict,
    ) = d
    return {
        k: hash_and_result.get(v, None)
        for k, v in sorted(mapping_dict.items(), key=lambda p: p[0])
    }, [
        hash_and_result,
        hash_int_map_small,
        original_object,
        mapping_dict,
    ]


def init_worker(use_cache_d):
    global use_cache_dict
    use_cache_dict = use_cache_d


def get_right_key(i):
    try:
        return hash(("VARVAR", i, "VARVAR"))
    except Exception:
        if isinstance(i, list):
            return hash("LIST" + str(i) + "LIST")
        if isinstance(i, dict):
            return hash("DICT" + str(i) + "DICT")
        if isinstance(i, set):
            return hash("SET" + str(i) + "SET")

        typestring = str(type(i)).lower()
        try:
            if "numpy" in typestring:
                return hash(b"NUMPY" + i.tobytes())
        except Exception:
            pass
        try:
            if "pandas" in typestring:
                return hash(b"PANDAS" + i.to_records(index=False).tobytes())
        except Exception:
            pass
        return hash(f"{i}{repr(i)}{typestring}")


def multifu(ini_value, shared_dict_cache_dict_input_data_outputdata_each_one):
    ini, value = ini_value
    (
        shared_dict,
        cache_dict,
        input_data,
        outputdata_each_one,
    ) = shared_dict_cache_dict_input_data_outputdata_each_one

    if use_cache_dict:
        rk = get_right_key((value.data_for_hash()))

        if rk not in cache_dict:
            cache_dict[rk] = value()
            shared_dict[rk] = ini
            input_data[rk] = value
        outputdata_each_one[ini] = rk
    else:
        outputdata_each_one[ini] = value()


if __name__ == "__main__":
    if int(os.environ.get("___START___MULTIPROCESSING___", 0)):
        allmydata = []
        for xxxa in iter(sys.stdin.buffer.readline, b""):
            allmydata.append(xxxa)
        initdict = dill.loads(
            b"".join(allmydata)
            .split(b"STARTDATASTARTDATASTARTDATA")[1]
            .split(b"ENDDATAENDDATAENDDATAENDDATA")[0]
        )
        processes = initdict["processes"]
        chunks = initdict["chunks"]
        md = initdict["procdata"]
        usecachedir = initdict["usecache"]

    with multiprocessing.Manager() as manager:
        shared_dict = manager.dict()
        cache_dict = manager.dict()
        input_data = manager.dict()
        outputdata_each_one = manager.dict()
        with multiprocessing.Pool(
            processes=processes,
            initializer=init_worker,
            initargs=(usecachedir,),
        ) as pool:
            pool.starmap(
                multifu,
                (
                    (
                        [ini, value],
                        [shared_dict, cache_dict, input_data, outputdata_each_one],
                    )
                    for ini, value in enumerate(md)
                ),
                chunksize=chunks,
            )
            cdi = {k: v for k, v in cache_dict.items()}
            sdi = {k: v for k, v in shared_dict.items()}
            idi = {k: v for k, v in input_data.items()}
            odi = {k: v for k, v in outputdata_each_one.items()}
            outd = dill.dumps(
                [
                    cdi,
                    sdi,
                    idi,
                    odi,
                ],
                protocol=dill.HIGHEST_PROTOCOL,
            )
            sys.stdout.buffer.write(
                b"\n\n\nENDEND1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1ENDEND"
                + outd
                + b"DNE1YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYDNE1\n\n\n"
            )
            sys.stdout.buffer.flush()
