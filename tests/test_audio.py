import numpy as np
import soundfile as sf

from coughcast.audio import bandpass, load_audio


def tone_amplitude(x, sr, freq):
    """Amplitude of one frequency in x, read off the FFT."""
    spectrum = np.abs(np.fft.rfft(x)) * 2 / len(x)
    return spectrum[int(round(freq * len(x) / sr))]


def test_bandpass_keeps_inside_removes_outside():
    sr = 8000
    t = np.arange(2 * sr) / sr
    x = np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 500 * t)
    y = bandpass(x, sr, low=300, high=800)
    assert tone_amplitude(y, sr, 500) > 0.9   # kept
    assert tone_amplitude(y, sr, 50) < 0.01   # removed


def test_bandpass_does_not_shift_in_time():
    sr = 8000
    t = np.arange(sr) / sr
    x = np.sin(2 * np.pi * 500 * t)
    y = bandpass(x, sr, low=300, high=800)
    mid = slice(sr // 4, 3 * sr // 4)  # ignore filter edges
    assert np.max(np.abs(x[mid] - y[mid])) < 0.05


def test_load_audio_mono_float32_resampled(tmp_path):
    sr = 16000
    stereo = np.random.default_rng(0).uniform(-0.5, 0.5, size=(sr, 2))  # 1 s
    path = tmp_path / "a.wav"
    sf.write(path, stereo, sr)
    x = load_audio(path, 8000)
    assert x.ndim == 1
    assert x.dtype == np.float32
    assert len(x) == 8000
