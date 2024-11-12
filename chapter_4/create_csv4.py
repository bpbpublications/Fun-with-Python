import pandas as pd
import numpy as np

data = [
    ("icecream", 15, ""),
    ("water", 3.2, "it was hot day, no"),
    ("bread", 1.3, "my favorite one"),
]

output_filename = "output_file.csv"
headers = ("name", "amount", "comment")

df = pd.DataFrame(np.array(data), columns=headers)
df.to_csv(output_filename, index=False)
