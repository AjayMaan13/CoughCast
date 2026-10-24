import numpy as np
import soundfile as sf
import librosa
from scipy.signal import butter, sosfiltfilt


def load_audio(path, target_sr):
    """Read an audio file as mono float32 at the sampling rate you ask for.

    Input:  path (str or Path to a wav/flac/ogg file), target_sr (int, Hz).
    Output: 1-D float32 numpy array of samples at target_sr.
    """
    x, sr = sf.read(path, dtype="float32", always_2d=True)
    x = x.mean(axis=1)  # stereo -> mono by averaging channels
    if sr != target_sr:
        x = librosa.resample(x, orig_sr=sr, target_sr=target_sr)
    return x.astype(np.float32)


def bandpass(x, sr, low, high, order=4):
    """Keep frequencies between low and high, remove the rest.

    Input:  x (1-D array), sr (sampling rate, Hz), low and high (cutoffs, Hz,
            high must be below sr/2), order (filter steepness, default 4).
    Output: 1-D float32 array, same length as x.

    Butterworth band-pass in second-order sections, zero-phase. sosfiltfilt runs
    the filter forwards then backwards, so the output is not shifted in time
    (lfilter would delay it, which matters when cutting cycles at exact times).
    Filtering twice also doubles the effective order.
    """
    sos = butter(order, [low, high], btype="band", fs=sr, output="sos")
    return sosfiltfilt(sos, x).astype(np.float32)
