"""One waveform + spectrogram per class. Run: python -m coughcast.icbhi_figure"""
from pathlib import Path

import librosa
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from coughcast.audio import bandpass, load_audio
from coughcast.icbhi import ROOT, cut_cycle, load_cycles

SR = 8000
# PLACEHOLDER cutoffs: replace with values from a cited paper and write the reason here.
LOW, HIGH = 100, 2000
N_FFT, HOP = 512, 128  # 64 ms window, 16 ms hop at 8 kHz
CLASSES = ["normal", "crackle", "wheeze"]


def pick_cycle(df, label):
    """Pick one example cycle of a class, the same one every run.

    Input:  df (cycle table), label ('normal', 'crackle' or 'wheeze').
    Output: one row (pandas Series): a random (seed 0) 2-5 s training cycle.
    """
    pool = df[(df["split"] == "train") & (df["label"] == label)
              & (df["end"] - df["start"]).between(2, 5)]
    return pool.sample(1, random_state=0).iloc[0]


def main():
    """Plot waveform and spectrogram of one cycle per class.

    Input:  none (reads data/icbhi).
    Output: none; saves figures/icbhi_examples.png and prints the chosen cycles.
    """
    df = load_cycles()
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    for col, label in enumerate(CLASSES):
        row = pick_cycle(df, label)
        x = load_audio(ROOT / "audio_and_txt_files" / f"{row['file']}.wav", SR)
        x = bandpass(x, SR, LOW, HIGH)  # filter the whole recording, then cut
        cycle = cut_cycle(x, SR, row["start"], row["end"])
        print(label, row["file"], row["start"], row["end"])
        t = np.arange(len(cycle)) / SR
        axes[0, col].plot(t, cycle, lw=0.5)
        axes[0, col].set_title(f"{label}  ({row['file']})", fontsize=9)
        db = librosa.amplitude_to_db(np.abs(librosa.stft(cycle, n_fft=N_FFT, hop_length=HOP)))
        axes[1, col].imshow(db, origin="lower", aspect="auto",
                            extent=[0, t[-1], 0, SR / 2])
        axes[1, col].set_xlabel("time (s)")
    axes[0, 0].set_ylabel("amplitude")
    axes[1, 0].set_ylabel("frequency (Hz)")
    Path("figures").mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig("figures/icbhi_examples.png", dpi=120)


if __name__ == "__main__":
    main()
