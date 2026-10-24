# Generate base URL from date and hour


import urllib
import re
import datetime 
import pathlib


def download_dasc_png(
        time_range:tuple[datetime.datetime, datetime.datetime], 
        download_dir:pathlib.Path, 
        overwrite:bool=False,
        verbose:bool=False,
        ):
    """
    Download UAF DASC PNG files from the specified time range.

    Parameters:
    -----------
    time_range : tuple of datetime.datetime
        Start and end times for the files to download.
    download_dir : pathlib.Path
        Directory to save the downloaded files.
    overwrite : bool, optional
        If True, overwrite existing files.
    verbose : bool, optional
        If True, print progress messages.
    """
    # Discover matching PNG filenames from the directory listing at `baseurl`.
    resp = urllib.request.urlopen(_png_url(time_range[0]))
    html = resp.read().decode('utf-8')  # errors='ignore'

    # Find greenline files
    pattern = r'PFRR_\d{8}_\d{6}_0558\.png'
    filelist = sorted(set(re.findall(pattern, html)))
    
    start_time, end_time = time_range
    valid_file_paths = []
    for f in filelist:
        ft = _filename_to_datetime(f)
        if ft is not None and start_time <= ft <= end_time:
            valid_file_paths.append(download_dir /f)
    filelist = valid_file_paths

    if not valid_file_paths:
        raise FileNotFoundError(f'No matching files found at {_png_url(time_range[0])} within {time_range}.')

    for filename in valid_file_paths:
        url = _png_url(time_range[0]) + filename.name
        if not filename.exists() or overwrite:
            if verbose:
                print('Downloading data file... '+filename.name, end='\r')
            urllib.request.urlretrieve(url, filename)
        else:
            if verbose:
                print(f"{filename.name} already downloaded and {overwrite=}.")
    return filelist


def _png_url(time):
    yyyymmdd = f'{time.year}{time.month:02d}{time.day:02d}'
    hh = f'{time.hour:02d}'
    return f'https://optics.gi.alaska.edu/amisr_archive/PKR/DASC/PNG/{time.year}/{yyyymmdd}/{hh}/'


def _filename_to_datetime(fn: str):
    """
    Convert a DASC PNG filename to a datetime object.

    Parameters:
    -----------
    fn: str
        Filename to convert.

    Returns:
    --------
    datetime.datetime or None
        Datetime object corresponding to the filename, or None if the filename doesn't match the 
        expected pattern.
    """
    m = re.search(r'PFRR_(\d{8})_(\d{6})_0558\.png', fn)
    if not m:
        return None
    return datetime.datetime.strptime(m.group(1) + m.group(2), '%Y%m%d%H%M%S')