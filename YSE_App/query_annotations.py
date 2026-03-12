from django.db.models import F, OuterRef, Subquery
from django.db.models.expressions import RawSQL

from YSE_App.models import TransientPhotData


def _recent_transient_photdata(
    include_bad_data=False,
    mag_only=False,
    transient_id_field="pk",
):
    queryset = TransientPhotData.objects.filter(
        photometry__transient_id=OuterRef(transient_id_field)
    )

    if not include_bad_data:
        queryset = queryset.exclude(data_quality__isnull=False)

    if mag_only:
        queryset = queryset.filter(mag__isnull=False)

    return queryset.order_by("-obs_date", "-pk")


def annotate_recent_mag(
    queryset,
    alias="recent_mag",
    include_bad_data=False,
    transient_id_field="pk",
):
    recent_mag = _recent_transient_photdata(
        include_bad_data=include_bad_data,
        mag_only=True,
        transient_id_field=transient_id_field,
    )
    return queryset.annotate(**{alias: Subquery(recent_mag.values("mag")[:1])})


def annotate_recent_magdate(
    queryset,
    alias="recent_magdate",
    include_bad_data=False,
    transient_id_field="pk",
):
    recent_magdate = _recent_transient_photdata(
        include_bad_data=include_bad_data,
        transient_id_field=transient_id_field,
    )
    return queryset.annotate(**{alias: Subquery(recent_magdate.values("obs_date")[:1])})


def annotate_recent_mag_and_date(
    queryset,
    include_bad_data=False,
    transient_id_field="pk",
):
    queryset = annotate_recent_mag(
        queryset,
        include_bad_data=include_bad_data,
        transient_id_field=transient_id_field,
    )
    return annotate_recent_magdate(
        queryset,
        include_bad_data=include_bad_data,
        transient_id_field=transient_id_field,
    )


def annotate_disc_mag(queryset, alias="disc_mag", transient_id_field="pk"):
    disc_mag = (
        TransientPhotData.objects.exclude(data_quality__isnull=False)
        .filter(
            photometry__transient_id=OuterRef(transient_id_field),
            discovery_point=True,
            mag__isnull=False,
        )
        .order_by("obs_date", "pk")
    )
    return queryset.annotate(**{alias: Subquery(disc_mag.values("mag")[:1])})


def annotate_transient_search_fields(queryset, transient_id_field="pk"):
    queryset = annotate_disc_mag(queryset, transient_id_field=transient_id_field)
    return queryset.annotate(
        obs_group_name=F("obs_group__name"),
        host_redshift=F("host__redshift"),
        spec_class=F("best_spec_class__name"),
        status_name=F("status__name"),
    )


def annotate_days_since_disc(queryset, alias="days_since_disc"):
    raw_query = """
SELECT DATEDIFF(curdate(), t.disc_date)
FROM YSE_App_transient t
WHERE YSE_App_transient.id = t.id
"""
    return queryset.annotate(**{alias: RawSQL(raw_query, ())})
