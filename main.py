import functools

from utils_loading import read_items, load_items
from typing import Dict

import pandas as pd

from utils_schema import searchGraphV2

if __name__ == "__main__":
    
    directory = "data"
    sep = ";"
    items : Dict[str, pd.DataFrame] = {k[0] : k[1] for k in map(functools.partial(load_items, y=sep), 
                                                                read_items(directory))}
    schemaV2 = searchGraphV2(items)

    print(schemaV2)

    
