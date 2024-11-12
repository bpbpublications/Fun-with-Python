# install

```bash
$ pip install numpy scipy scikit-learn quandl
```

# stock

## load

```python
import quandl

df = quandl.get("WIKI/GOOGL")
df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
```
## modules

```bash
`$ pip install xlsxwriter
```
