from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupKFold

ROOT = Path("data/icbhi")
LABELS = {(0, 0): "normal", (1, 0): "crackle", (0, 1): "wheeze", (1, 1): "both"}


def parse_name(stem):
    """Split an ICBHI file name into its five parts.

    Input:  stem (str), e.g. '101_1b1_Al_sc_Meditron'.
    Output: dict with patient_id (int), recording, location, mode, device.
    """
    patient, recording, location, mode, device = stem.split("_")
    return {"patient_id": int(patient), "recording": recording,
            "location": location, "mode": mode, "device": device}


def read_cycles(txt_path):
    """Read one annotation file, one line per breathing cycle.

    Input:  txt_path (path to a .txt file; each line is start, end, crackle, wheeze).
    Output: list of (start_s, end_s, crackle, wheeze) tuples (float, float, int, int).
    """
    rows = []
    for line in Path(txt_path).read_text().splitlines():
        if line.strip():
            start, end, crackle, wheeze = line.split()
            rows.append((float(start), float(end), int(crackle), int(wheeze)))
    return rows


def read_split(split_path):
    """Read the official train/test file.

    Input:  split_path (path to official_split.txt; each line is 'file<TAB>train|test').
    Output: dict {file name: 'train' or 'test'}.
    """
    pairs = (l.split() for l in Path(split_path).read_text().splitlines() if l.strip())
    return {name: split for name, split in pairs}


def split_overlap(df, col="split"):
    """Find patients that appear in both train and test.

    Input:  df (cycle table with patient_id), col (which split column to check).
    Output: sorted list of patient ids; an empty list means no leakage.
    """
    train = set(df.loc[df[col] == "train", "patient_id"])
    test = set(df.loc[df[col] == "test", "patient_id"])
    return sorted(train & test)


def load_cycles(root=ROOT):
    """Build the table of all breathing cycles.

    Input:  root (folder with audio_and_txt_files/ and official_split.txt).
    Output: DataFrame, one row per cycle. Columns: file, patient_id, recording,
            location, mode, device, start, end, crackle, wheeze, label,
            wheeze_positive, official_split, split.

    `official_split` is the published split. The official file puts a few
    patients in both train and test, which leaks. `split` is the same except
    those patients are moved wholly to train.
    """
    root = Path(root)
    rows = []
    for file, official in read_split(root / "official_split.txt").items():
        meta = parse_name(file)
        for start, end, crackle, wheeze in read_cycles(root / "audio_and_txt_files" / f"{file}.txt"):
            rows.append({"file": file, **meta, "start": start, "end": end,
                         "crackle": crackle, "wheeze": wheeze,
                         "label": LABELS[(crackle, wheeze)],
                         "wheeze_positive": bool(wheeze), "official_split": official})
    df = pd.DataFrame(rows)
    df["split"] = df["official_split"]
    df.loc[df["patient_id"].isin(split_overlap(df, "official_split")), "split"] = "train"
    return df


def cut_cycle(x, sr, start, end):
    """Slice one breathing cycle out of a whole (already filtered) recording.

    Input:  x (1-D array, whole recording), sr (Hz), start and end (seconds).
    Output: 1-D array, the samples from start to end.
    """
    return x[int(round(start * sr)):int(round(end * sr))]


def patient_folds(df, n=5):
    """Make validation folds inside train where no patient is in two folds.

    Input:  df (cycle table with split and patient_id), n (number of folds).
    Output: list of n (fit_index, val_index) pairs, using df's own index labels.
    """
    train = df[df["split"] == "train"]
    folds = GroupKFold(n_splits=n).split(train, groups=train["patient_id"])
    return [(train.index[fit], train.index[val]) for fit, val in folds]
