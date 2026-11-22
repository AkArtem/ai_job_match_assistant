from src.matching.filters import hard_filter, german_to_rank
from src.matching.profile import CandidateProfile

profile = CandidateProfile(
    german_level="A2",
    english_level="C1",
    max_hours_per_week=20,
    skills=['Python'],
    summary='test')

def make_job(**changes):
    job = {
        "id": 1,
        "min_german": None,
        "employment_type": "Internship",
        "min_hours_per_week": None
    }
    job.update(changes)
    return job

def test_hard_filter():
    kept, removed = hard_filter([make_job(min_german="C1")], profile)
    assert len(kept) == 0
    assert len(removed) == 1

    kept, removed = hard_filter([make_job(min_german=None)], profile)
    assert len(kept) == 1
    assert len(removed) == 0

    kept, removed = hard_filter([make_job(employment_type="Full-time")], profile)
    assert len(kept) == 0
    assert len(removed) == 1

    kept, removed = hard_filter([make_job(employment_type="Part Time/Full Time")], profile)
    assert len(kept) == 1
    assert len(removed) == 0

    kept, removed = hard_filter([make_job(min_hours_per_week=25)], profile)
    assert len(kept) == 0
    assert len(removed) == 1

    kept, removed = hard_filter([make_job(min_hours_per_week=None)], profile)
    assert len(kept) == 1
    assert len(removed) == 0