from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("YSE_App", "0003_surveyobservation_priority"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="transient",
            index=models.Index(fields=["name"], name="yse_trans_name_idx"),
        ),
        migrations.AddIndex(
            model_name="transient",
            index=models.Index(fields=["disc_date"], name="yse_trans_disc_idx"),
        ),
        migrations.AddIndex(
            model_name="transient",
            index=models.Index(fields=["ra", "dec"], name="yse_trans_radec_idx"),
        ),
        migrations.AddIndex(
            model_name="transient",
            index=models.Index(fields=["status", "disc_date"], name="yse_trans_stat_disc_idx"),
        ),
        migrations.AddIndex(
            model_name="surveyfield",
            index=models.Index(fields=["field_id"], name="yse_sfield_id_idx"),
        ),
        migrations.AddIndex(
            model_name="surveyfield",
            index=models.Index(fields=["ra_cen", "dec_cen"], name="yse_sfield_radec_idx"),
        ),
        migrations.AddIndex(
            model_name="surveyfield",
            index=models.Index(fields=["obs_group", "instrument", "active"], name="yse_sfield_scope_idx"),
        ),
        migrations.AddIndex(
            model_name="surveyobservation",
            index=models.Index(fields=["survey_field", "obs_mjd"], name="yse_sobs_field_obs_idx"),
        ),
        migrations.AddIndex(
            model_name="surveyobservation",
            index=models.Index(fields=["survey_field", "mjd_requested"], name="yse_sobs_field_req_idx"),
        ),
        migrations.AddIndex(
            model_name="transientphotdata",
            index=models.Index(fields=["photometry", "obs_date"], name="yse_tphot_obs_idx"),
        ),
        migrations.AddIndex(
            model_name="transientphotdata",
            index=models.Index(fields=["photometry", "discovery_point", "obs_date"], name="yse_tphot_disc_idx"),
        ),
        migrations.AddIndex(
            model_name="hostphotdata",
            index=models.Index(fields=["photometry", "obs_date"], name="yse_hphot_obs_idx"),
        ),
        migrations.AddIndex(
            model_name="transientspecdata",
            index=models.Index(fields=["spectrum", "wavelength"], name="yse_tspec_wave_idx"),
        ),
        migrations.AddIndex(
            model_name="hostspecdata",
            index=models.Index(fields=["spectrum", "wavelength"], name="yse_hspec_wave_idx"),
        ),
    ]
