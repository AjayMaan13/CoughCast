import numpy as np
import pandas as pd

from coughcast.icbhi import (cut_cycle, load_cycles, parse_name,
                             patient_folds, split_overlap)


def make_root(tmp_path):
    """A tiny fake ICBHI folder. Patient 2 is in both train and test."""
    (tmp_path / "audio_and_txt_files").mkdir()
    files = {"1_1b1_Al_sc_Meditron": "train", "2_1b1_Ar_sc_Meditron": "train",
             "2_1b2_Tc_sc_Meditron": "test", "3_1b1_Pl_sc_Meditron": "test"}
    annotations = "0.0\t1.0\t0\t0\n1.0\t2.5\t1\t0\n2.5\t4.0\t0\t1\n4.0\t5.0\t1\t1\n"
    for name in files:
        (tmp_path / "audio_and_txt_files" / f"{name}.txt").write_text(annotations)
    (tmp_path / "official_split.txt").write_text(
        "\n".join(f"{n}\t{s}" for n, s in files.items()))
    return tmp_path


def test_parse_name():
    assert parse_name("101_1b1_Al_sc_Meditron") == {
        "patient_id": 101, "recording": "1b1", "location": "Al",
        "mode": "sc", "device": "Meditron"}


def test_labels_and_wheeze_positive(tmp_path):
    df = load_cycles(make_root(tmp_path))
    one = df[df["file"] == "1_1b1_Al_sc_Meditron"]
    assert list(one["label"]) == ["normal", "crackle", "wheeze", "both"]
    assert list(one["wheeze_positive"]) == [False, False, True, True]
    assert len(df) == 16  # 4 files x 4 cycles


def test_no_patient_in_both_train_and_test(tmp_path):
    df = load_cycles(make_root(tmp_path))
    assert split_overlap(df, "official_split") == [2]   # the fake data does leak
    assert split_overlap(df, "split") == []             # and we fixed it
    assert set(df.loc[df["patient_id"] == 2, "split"]) == {"train"}
    assert set(df.loc[df["patient_id"] == 3, "split"]) == {"test"}


def test_cut_cycle_returns_right_number_of_samples():
    sr = 8000
    x = np.arange(10 * sr, dtype=np.float32)
    cycle = cut_cycle(x, sr, start=1.0, end=3.5)
    assert len(cycle) == int(2.5 * sr)
    assert cycle[0] == x[sr]


def test_patient_folds_never_share_a_patient():
    patients = np.repeat(np.arange(10), 3)  # 10 train patients, 3 cycles each
    df = pd.DataFrame({"patient_id": patients, "split": "train"})
    folds = patient_folds(df, n=5)
    assert len(folds) == 5
    seen = []
    for fit, val in folds:
        assert not set(df.loc[fit, "patient_id"]) & set(df.loc[val, "patient_id"])
        seen += list(val)
    assert sorted(seen) == list(df.index)  # every row is validated exactly once
