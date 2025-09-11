import xgboost as xgb
import tiktoken
from tokenizers import Tokenizer
import torchdata.datapipes as dp
import sentencepiece as spm
import scipy
import numpy as np
import hdbscan
import jenkspy
import lightgbm as lgb
import ml_dtypes
import autovizwidget
import bottleneck as bn
import cloudpickle
import contourpy
import cutadapt
import graphviz
from pandas import to_datetime
import gensim
import dask
from dask import delayed
import hnswlib
import imagecodecs
import iminuit
import ipykernel
import ipywidgets as widgets
import jupyter
from jupyter_core.paths import jupyter_path
import matplotlib
from PIL import Image
import nbconvert
import nbformat
from notebook import notebookapp
import numba
import numexpr
from pyiceberg.schema import Schema, NestedField
from pyiceberg.types import LongType, StringType
import pywt
from skimage import data, filters
import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm



X = np.random.rand(100, 1)
y = 3 * X.squeeze() + np.random.randn(100)
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())

df=pd.DataFrame({'a':[1,2,3],'b':[10,20,30]})
print(DataFrameMapper([(['a'], StandardScaler()), (['b'], StandardScaler())]).fit_transform(df))



# scikit-image =>skimage
img = data.coins(); edges = filters.sobel(img)
print('Edges shape:', edges.shape)


#pywavelets => pywt
data=[1,2,3,4]
cA,cD=pywt.dwt(data,'db1')
print('Approximation:', cA, 'Detail:', cD)

# Create a schema and unpack fields
schema = Schema(
    NestedField(1, 'id', LongType(), required=True),
    NestedField(2, 'name', StringType(), required=True)
)

# Print schema info
print('Table schema:', [(f.field_id, f.name, type(f.field_type).__name__) for f in schema.fields])


#For numexpr
print(numexpr.evaluate('2+3'))

print(callable(numba.njit))

print(hasattr(notebookapp, 'list_running_servers'))

nb_str = '{\"cells\":[],\"metadata\":{},\"nbformat\":4,\"nbformat_minor\":5}'
nb = nbformat.reads(nb_str, as_version=4)
print(nb['nbformat'])

print(hasattr(nbconvert, 'exporters'))

print(Image.OPEN.keys())

matplotlib.use('Agg')

print(jupyter_path())

print(jupyter.__file__)

#ipywidgets
w = widgets.Label("ipywidgets imported successfully")
print(type(w))


#ipykernel
x = ipykernel.connect.__name__
print("ipykernel worked : ",x)

#iminuit
iminuit.util.describe(lambda x, y: x + y)
print("Iminuit worked")

#imagecodecs
imagecodecs.zlib_encode(b"hello world")
print("Imagecodec worked")

#hnswlib
hnswlib.Index(space='l2', dim=2).init_index(max_elements=5, ef_construction=100, M=16)
print("hnswlib worked")

#using h5py
#[f.create_dataset("data", data=[1,2,3]) or print(list(f.keys())) for f in [h5py.File("test.h5", "w")]]

# using dask
print(delayed(lambda x: x*2)(5).compute())

# Using fiona
#print(list(fiona.listlayers("https://github.com/freemap-io/openstreetmap-carto/raw/master/tests/data/countries.shp")))
#fiona.Env()

# genism
tokens = gensim.utils.simple_preprocess("Hello world, this is a test!")
print(tokens)

# Convert a string date to a pandas Timestamp
print(to_datetime("2025-09-08"))


#  xgboost simple DMatrix creation
data = np.random.rand(5, 5)
label = np.random.randint(2, size=5)
dtrain = xgb.DMatrix(data, label=label)
print("xgboost DMatrix created:", dtrain.num_row())

#  tiktoken simple encoding
enc = tiktoken.get_encoding("cl100k_base")
print("tiktoken encoding:", enc.encode("Hello world"))

#  tokenizers (dummy tokenizer with whitespace)
tok = Tokenizer.from_pretrained("bert-base-uncased")
print("tokenizers encoding:", tok.encode("Hello world").tokens)

#  torchdata simple datapipes
dp1 = dp.iter.IterableWrapper([1, 2, 3])
print("torchdata example:", list(dp1))

# sentencepiece simple processor
# Using a mock model since real training is big; just check version
print("sentencepiece version:", spm.__version__)

# scipy simple linear algebra
mat = np.eye(3)
eigvals = scipy.linalg.eigvals(mat)
print("scipy eigenvalues:", eigvals)

#  numpy array creation
arr = np.array([1, 2, 3])
print("numpy sum:", np.sum(arr))

#  hdbscan clustering
clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
cluster_labels = clusterer.fit_predict([[1,2],[2,3],[10,10]])
print("hdbscan labels:", cluster_labels)

#  jenkspy natural breaks
values = [1, 2, 2, 3, 4, 10]
breaks = jenkspy.jenks_breaks(values, n_classes=3)
print("jenkspy breaks:", breaks)

#  lightgbm dataset creation
train_data = lgb.Dataset(data, label=label)
train_data.construct()  # initialize the dataset
print("lightgbm dataset created:", train_data.num_data())

#  ml_dtypes simple type usage
import ml_dtypes
a = [ml_dtypes.bfloat16(1), ml_dtypes.bfloat16(2)]
print("ml_dtypes array:", a)

#  autovizwidget check version
print("autovizwidget version:", autovizwidget.__version__)

#  bottleneck nanmean
print("bottleneck nanmean:", bn.nanmean([1, np.nan, 2]))

#  cloudpickle dump/load
dumped = cloudpickle.dumps(lambda x: x+1)
print("cloudpickle loaded fn:", cloudpickle.loads(dumped)(10))

#  contourpy simple path
from contourpy import contour_generator
cg = contour_generator(z=np.random.rand(3,3))
contours = cg.lines(0.5)
print("contourpy contours:", len(contours))

#  cutadapt version check
print("cutadapt version:", cutadapt.__version__)

#  graphviz simple graph
g = graphviz.Digraph()
g.node("A")
g.node("B")
g.edge("A", "B")
print("graphviz source:\n", g.source)


bn_mean = 1.5  # or bn.nanmean([1, 2])

# For numexpr
import numexpr as ne
ne_eval = ne.evaluate("2+3")

# For pandas datetime
import pandas as pd
date_val = pd.to_datetime("2025-09-08")

# For sklearn-pandas DataFrameMapper output
df = pd.DataFrame({'a': [1, 2, 3], 'b': [10, 20, 30]})
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import StandardScaler
mapper_output = DataFrameMapper([(['a'], StandardScaler()), (['b'], StandardScaler())]).fit_transform(df)

# For Pillow test
from PIL import Image
pillow_formats = Image.registered_extensions()

# For ipykernel test
ipykernel_worked = hasattr(__import__('ipykernel'), 'connect')


print("====== All Library imported and working fine ========")