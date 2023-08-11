from typing import Callable, List
import os 


import re

import pandas as pd



spot_id : Callable[[str], bool] = lambda x: re.search(r"/(?i)(^id\s?$)|(^id_)|(_id\s?$)", x) is not None
load_items : Callable[[str], pd.DataFrame] = lambda x, y: (re.search(r"/[^/]*\.csv", x).group(0)[1:-4], pd.read_csv(x, sep=y))
read_items : Callable[[str], List[str]] = lambda x : ["{}/{}".format(x, i) for i in os.listdir(x)] 