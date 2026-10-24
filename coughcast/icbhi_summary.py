"""Write results/icbhi_summary.json. Run: python -m coughcast.icbhi_summary"""
import json
from collections import Counter
from pathlib import Path

import soundfile as sf

from coughcast.icbhi import ROOT, load_cycles, split_overlap

PERCENTILES = [0.05, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]


def counts(df, split_col):
    """Count cycles per split and class.

    Input:  df (cycle table), split_col ('split' or 'official_split').
    Output: nested dict {split: {label: number of cycles}}, 0 where empty.
    """
    return df.groupby([split_col, "label"]).size().unstack(fill_value=0).to_dict("index")


def main():
    """Build the ICBHI summary and write results/icbhi_summary.json.

    Input:  none (reads data/icbhi).
    Output: none; writes the JSON with counts, length percentiles, sampling
            rates, devices and the patients moved out of test.
    """
    df = load_cycles()
    df["length_s"] = df["end"] - df["start"]
    files = df.drop_duplicates("file")
    rates = Counter(sf.info(ROOT / "audio_and_txt_files" / f"{f}.wav").samplerate
                    for f in files["file"])
    summary = {
        "n_cycles": len(df),
        "n_recordings": len(files),
        "n_patients": df["patient_id"].nunique(),
        "cycles_per_class_per_split": counts(df, "split"),
        "cycles_per_class_per_official_split": counts(df, "official_split"),
        "patients_in_both_official_train_and_test": split_overlap(df, "official_split"),
        "cycle_length_s_percentiles": {
            str(q): float(v) for q, v in df["length_s"].quantile(PERCENTILES).items()},
        "sampling_rates_hz_recordings_per_rate": {str(k): v for k, v in rates.items()},
        "recordings_per_device": files["device"].value_counts().to_dict(),
    }
    Path("results").mkdir(exist_ok=True)
    Path("results/icbhi_summary.json").write_text(json.dumps(summary, indent=2, default=int))


if __name__ == "__main__":
    main()
