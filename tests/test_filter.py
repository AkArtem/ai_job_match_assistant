from src.matching.filters import hard_filter, german_to_rank
from src.matching.profile import CandidateProfile

profile = CandidateProfile(
    german_level="A2",
    english_level="C1",
    max_hours_per_week=20,
    skills=["Python"],
    summary="test")


def make_job(**changes):
    job = {
        "id": "001",
        "min_german": None,
        "employment_type": "Internship",
        "min_hours_per_week": None
    }
    job.update(changes)
    return job

def test_rank_cefr_levels():
    assert german_to_rank("A1") == 1
    assert german_to_rank("A2") == 2
    assert german_to_rank("B1") == 3
    assert german_to_rank("B2") == 4
    assert german_to_rank("C1") == 5
    assert german_to_rank("C2") == 6


def test_rank_words():
    assert german_to_rank("fließend") == 6
    assert german_to_rank("verhandlungssicher") == 6
    assert german_to_rank("sehr gut") == 5
    assert german_to_rank("gut") == 4


def test_rank_very_good():
    assert german_to_rank("very good") == 5
    assert german_to_rank("VERY GOOD") == 5


def test_rank_sehr_gut_is_higher_than_gut():
    assert german_to_rank("sehr gut") > german_to_rank("gut")


def test_rank_ignores_case_and_extra_text():
    assert german_to_rank("Deutsch B2") == 4
    assert german_to_rank("SEHR GUT") == 5


def test_rank_two_levels_takes_higher():
    assert german_to_rank("B1/B2") == 4


def test_rank_unknown_is_none():
    assert german_to_rank(None) is None
    assert german_to_rank("") is None
    assert german_to_rank("Grundkenntnisse") is None

def test_removes_job_if_german_too_high():
    kept, removed = hard_filter([make_job(min_german="C1")], profile)
    assert kept == []
    assert removed == [("001", "german_level")]


def test_keeps_job_if_german_equal_to_profile():
    kept, removed = hard_filter([make_job(min_german="A2")], profile)
    assert len(kept) == 1
    assert removed == []


def test_keeps_job_if_german_unknown():
    kept, removed = hard_filter([make_job(min_german=None)], profile)
    assert len(kept) == 1
    assert removed == []


def test_removes_full_time():
    kept, removed = hard_filter([make_job(employment_type="Full-time")], profile)
    assert kept == []
    assert removed == [("001", "employment_type")]


def test_removes_full_time_any_case():
    kept, removed = hard_filter([make_job(employment_type="FULL-TIME")], profile)
    assert kept == []


def test_removes_full_time_underscore_and_german_vollzeit():
    jobs = [
        make_job(id="001", employment_type="FULL_TIME"),
        make_job(id="002", employment_type="Vollzeit"),
    ]
    kept, removed = hard_filter(jobs, profile)
    assert kept == []
    assert removed == [("001", "employment_type"), ("002", "employment_type")]


def test_keeps_part_time_or_full_time():
    kept, removed = hard_filter([make_job(employment_type="Part Time/Full Time")], profile)
    assert len(kept) == 1


def test_keeps_mixed_vollzeit_and_teilzeit():
    kept, removed = hard_filter(
        [make_job(employment_type="Vollzeit, Teilzeit")], profile
    )
    assert len(kept) == 1
    assert removed == []


def test_keeps_job_if_employment_type_missing():
    kept, removed = hard_filter([make_job(employment_type=None)], profile)
    assert len(kept) == 1


def test_removes_job_if_min_hours_too_high():
    kept, removed = hard_filter([make_job(min_hours_per_week=25)], profile)
    assert kept == []
    assert removed == [("001", "max_hours_per_week")]


def test_keeps_job_if_min_hours_equal_to_max():
    kept, removed = hard_filter([make_job(min_hours_per_week=20)], profile)
    assert len(kept) == 1


def test_keeps_job_if_hours_unknown():
    kept, removed = hard_filter([make_job(min_hours_per_week=None)], profile)
    assert len(kept) == 1


def test_mixed_list_splits_correctly():
    jobs = [
        make_job(id="001"),
        make_job(id="002", min_german="C1"),
        make_job(id="003", employment_type="Full-time"),
        make_job(id="004", min_hours_per_week=30),
    ]
    kept, removed = hard_filter(jobs, profile)
    assert [j["id"] for j in kept] == ["001"]
    assert removed == [
        ("002", "german_level"),
        ("003", "employment_type"),
        ("004", "max_hours_per_week"),
    ]


def test_first_matching_reason_is_recorded():
    job = make_job(min_german="C1", employment_type="Full-time")
    kept, removed = hard_filter([job], profile)
    assert removed == [("001", "german_level")]
    
def test_german_or_english_alternatives_are_not_required():
    assert german_to_rank("Deutsch oder Englisch") is None
    assert german_to_rank("English or German") is None
    kept, removed = hard_filter(
        [make_job(min_german="C1 oder Englisch")], profile
    )
    assert len(kept) == 1
    assert removed == []
