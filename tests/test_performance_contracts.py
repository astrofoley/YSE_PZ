import pathlib
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def read_text(relative_path):
    return (REPO_ROOT / relative_path).read_text()


class PerformanceContractTests(unittest.TestCase):
    def test_query_annotations_exposes_shared_helpers(self):
        text = read_text("YSE_App/query_annotations.py")
        self.assertIn("def annotate_recent_mag(", text)
        self.assertIn("def annotate_recent_magdate(", text)
        self.assertIn("def annotate_days_since_disc(", text)
        self.assertIn("def annotate_transient_search_fields(", text)

    def test_yse_views_uses_shared_recent_mag_annotation(self):
        text = read_text("YSE_App/yse_views.py")
        self.assertIn("from .query_annotations import annotate_days_since_disc, annotate_recent_mag", text)
        self.assertNotIn("recent_mag_raw_query =", text)
        self.assertNotIn("SELECT pd.mag", text)

    def test_views_use_shared_annotation_helpers(self):
        text = read_text("YSE_App/views.py")
        self.assertIn("annotate_recent_mag(", text)
        self.assertIn("annotate_recent_magdate(", text)
        self.assertNotIn("transients = transients.annotate(last_mag=RawSQL", text)

    def test_migration_adds_expected_hot_path_indexes(self):
        text = read_text("YSE_App/migrations/0004_performance_indexes.py")
        for index_name in (
            "yse_trans_name_idx",
            "yse_trans_radec_idx",
            "yse_sfield_radec_idx",
            "yse_sobs_field_obs_idx",
            "yse_tphot_obs_idx",
            "yse_tspec_wave_idx",
        ):
            self.assertIn(index_name, text)

    def test_transient_api_queryset_is_eager_loaded(self):
        text = read_text("YSE_App/api_views.py")
        self.assertIn("class TransientViewSet", text)
        self.assertIn("def get_queryset(self):", text)
        self.assertIn(".select_related(", text)
        self.assertIn(".prefetch_related('tags')", text)

    def test_view_utils_recent_phot_helpers_use_first(self):
        text = read_text("YSE_App/view_utils.py")
        self.assertIn("return photdata.order_by('-obs_date').first()", text)
        self.assertIn("return photdata.filter(mag__isnull=False).first()", text)
        self.assertNotIn("for p in allowed_phot:", text)


if __name__ == "__main__":
    unittest.main()
