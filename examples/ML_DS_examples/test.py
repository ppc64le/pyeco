import unittest
import ml_ds_example as ex  # Use variables & imports from example.py


class TestAllLibraries(unittest.TestCase):
    def test_xgboost(self):
        self.assertTrue(ex.dtrain.num_row() > 0)

    def test_tiktoken(self):
        self.assertTrue(len(ex.enc.encode("Hello")) > 0)

    def test_tokenizers(self):
        self.assertTrue(len(ex.tok.encode("Hello world").tokens) > 0)

    def test_sentencepiece(self):
        self.assertTrue(hasattr(ex.spm, "__version__"))

    def test_scipy(self):
        self.assertTrue(len(ex.eigvals) > 0)

    def test_numpy(self):
        self.assertEqual(int(ex.arr.sum()), 6)

    def test_hdbscan(self):
        self.assertTrue(len(ex.cluster_labels) > 0)

    def test_jenkspy(self):
        self.assertTrue(len(ex.breaks) > 0)

    def test_ml_dtypes(self):
        self.assertTrue(all(isinstance(i, ex.ml_dtypes.bfloat16) for i in ex.a))

    def test_autovizwidget(self):
        self.assertTrue(hasattr(ex.autovizwidget, "__version__"))

    def test_bottleneck(self):
        self.assertEqual(ex.bn_mean, 1.5)

    def test_cloudpickle(self):
        self.assertEqual(ex.cloudpickle.loads(ex.dumped)(5), 6)

    def test_contourpy(self):
        self.assertTrue(len(ex.contours) > 0)

    def test_cutadapt(self):
        self.assertTrue(hasattr(ex.cutadapt, "__version__"))

    def test_graphviz(self):
        self.assertIn("A", ex.g.source)

    def test_gensim(self):
        self.assertIn("hello", [t.lower() for t in ex.tokens])

    def test_dask(self):
        self.assertEqual(ex.delayed(lambda x: x + 1)(1).compute(), 2)

    def test_hnswlib(self):
        self.assertTrue(hasattr(ex.hnswlib.Index(space='l2', dim=2), "init_index"))

    def test_imagecodecs(self):
        self.assertTrue(callable(ex.imagecodecs.zlib_encode))

    def test_iminuit(self):
        self.assertTrue(hasattr(ex.iminuit.util, "describe"))

    def test_ipywidgets(self):
        self.assertTrue(isinstance(ex.w, ex.widgets.Label))

    def test_jupyter(self):
        self.assertTrue("jupyter" in ex.jupyter.__file__)

    def test_jupyter_core(self):
        self.assertTrue(len(ex.jupyter_path()) > 0)

    def test_matplotlib(self):
        self.assertTrue(hasattr(ex.matplotlib, "use"))

    def test_nbconvert(self):
        self.assertTrue(hasattr(ex.nbconvert, "exporters"))

    def test_nbformat(self):
        self.assertEqual(ex.nb['nbformat'], 4)

    def test_numba(self):
        self.assertTrue(callable(ex.numba.njit))

    def test_numexpr(self):
        self.assertEqual(int(ex.ne_eval), 5)

    def test_pyiceberg(self):
        self.assertEqual(len(ex.schema.fields), 2)

    def test_pywt(self):
        self.assertTrue(len(ex.cA) > 0 and len(ex.cD) > 0)

    def test_skimage(self):
        self.assertTrue(ex.edges.shape[0] > 0)

    def test_statsmodels(self):
        self.assertTrue(hasattr(ex.model, "summary"))

    def test_pandas_datetime(self):
        self.assertEqual(str(ex.date_val), "2025-09-08 00:00:00")


if __name__ == "__main__":
    unittest.main()