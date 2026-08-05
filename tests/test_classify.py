from app.classify import Category, classify


def test_classifies_rfi():
    result = classify("RFI-042: Chiller nameplate voltage", "Please confirm the design voltage for Chiller 2.")
    assert result.category == Category.RFI


def test_classifies_ncr():
    result = classify("NCR-11 issued", "Non-conformance found: hi-pot test failed on switchgear bus.")
    assert result.category == Category.NCR


def test_classifies_test_report():
    result = classify("IST results attached", "Functional performance test results for AHU-3 are attached.")
    assert result.category == Category.TEST_REPORT


def test_classifies_schedule():
    result = classify("Schedule update", "We are two weeks behind schedule on the switchgear delivery milestone.")
    assert result.category == Category.SCHEDULE


def test_falls_back_to_general_question():
    result = classify("Quick question", "What time works for a call tomorrow?")
    assert result.category == Category.GENERAL_QUESTION
    assert result.matched_keywords == ()


def test_picks_category_with_most_matches():
    # Contains one schedule keyword and two test-report keywords -- should
    # pick test_report since it has the stronger signal.
    result = classify(
        "Update",
        "Test results (hi-pot, megger) are in, slightly behind schedule.",
    )
    assert result.category == Category.TEST_REPORT
