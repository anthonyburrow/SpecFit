from pathlib import Path
import requests


DATA_DIR = Path(__file__).parents[0].absolute() / 'SpecFit' / 'data'


def download(url: str, out_filename: Path):
    if out_filename.is_file():
        print(f'{out_filename} already retrieved.')

    DATA_DIR.mkdir(exist_ok=True)

    response = requests.get(url)

    try:
        with open(out_filename, 'wb') as file:
            file.write(response.content)
    except Exception:
        f'{url} could not be retrieved.'


def get_gaunt():
    url = 'https://data.nublado.org/gauntff/gauntff.dat'
    download(url, DATA_DIR / 'gauntff.dat')

    # url = 'https://data.nublado.org/gauntff/gauntff_nonav.dat'
    # download(url, DATA_DIR / 'gauntff_nonav.dat')


if __name__ == '__main__':
    get_gaunt()
