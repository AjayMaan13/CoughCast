# CoughCast build plan

A bedside listener that finds wheezes and coughs in audio, turns each night into numbers, and turns weeks of nights into a trend.

Written 2026-10-16 for the Seneca RespiSentinel RA posting 221336. Target: phases 0 to 2 done by Oct 21 (first real numbers for an interview), everything done by Oct 30.

---

## How to use this file

Every phase has the same seven parts:

1. **Goal**: one sentence.
2. **Done when**: a checklist. Don't move on until every box is ticked.
3. **Learn first**: the concepts, where to learn them, and self-check questions. Do this before any code. If you can't answer the questions, the AI's code will be a black box you can't defend in an interview.
4. **Steps**: what to build, in order, and how.
5. **AI does / You do**: who owns each part. The AI never runs git.
6. **Prompts**: copy-paste prompts for Claude Code.
7. **Pitfalls**: the mistakes that usually happen here.

Work one phase at a time. Read a phase completely before starting it.

---

## Scope: what CoughCast is, and what it is not

### In scope (the whole project)

| Part | What it does | Data |
|---|---|---|
| Wheeze Lab | Classifies breathing cycles as normal, crackle, wheeze, or both | ICBHI 2017 |
| Cough detector | Says whether a 1-second window contains a cough | COUGHVID (coughs) + ESC-50 (everything else) |
| Night Listener | Slides the cough detector over a long recording, outputs cough events with times | Synthetic nights you generate, plus one self-recorded test session |
| Night-to-Week | Rolls nightly counts into weekly trends and flags a rise | Simulated weeks, clearly labelled |
| Demo app | Upload audio, see cough events on a timeline, see a weekly chart | Your files |

### Not in scope (do not build these, even if the AI suggests them)

- No Docker, no database, no cloud, no API server
- No experiment tracking tools (MLflow, Weights & Biases), no config frameworks (Hydra)
- No classes where a function works; no abstract base classes
- No CLI framework beyond `argparse`
- No mobile app, no ONNX export, no pretrained audio models, no Grad-CAM, no air-quality join until phase 7 is shipped (see Stretch at the end)
- No CI pipeline until phase 7 is shipped

If you notice yourself adding a layer "for later", stop. Later can add it.

### Your machine

MacBook Air M1, 8 GB RAM. That shapes three choices in this plan:

- Small datasets and subsets, not everything at once
- Small CNNs (a few hundred thousand parameters), trained on PyTorch's `mps` backend or CPU
- Features computed once and cached to disk as `.npz` files, so training never recomputes audio

---

## Ground rules: you and the AI

### The AI can

- Explain any concept, line of code, or error
- Write code into files in your working folder when you ask
- Write and run tests (`pytest`) and scripts
- Debug errors you paste
- Review code you wrote
- Draft README and report text, with `[ ]` blanks where numbers go

### The AI cannot

- Run any `git` command that changes history or the remote: no `git add`, `git commit`, `git push`, `git reset`, `git checkout`, `git rebase`
- Create or change anything on GitHub
- Write a number into the README, report, or resume. Numbers come only from files in `results/`, and you copy them in yourself
- Download datasets. It writes the download script; you run it, because you are the one accepting each dataset's terms
- Delete anything in `data/`
- Install packages globally. Only inside the project's virtual environment

### You always

- Read every diff before committing: `git diff`
- Run `pytest -q` before every commit
- Commit and push yourself
- Do the "explain-back" at the end of each phase: explain the phase's code out loud in under 2 minutes without looking. If you can't, ask the AI to walk you through it before moving on

### Your commit loop (every step)

```
1. Ask the AI for one small change
2. git diff                       # read every line
3. pytest -q                      # tests pass?
4. git add <files you checked>    # you, not the AI
5. git commit -m "..."            # you
6. git push                       # you, at the end of the session
```

Small commits. One idea per commit. The phase sections suggest commit messages.

---

## Timeline

| Phase | Dates | Hours | What you have at the end |
|---|---|---|---|
| 0. Setup and data | Oct 17 | 3 to 4 | Repo, rules, three datasets downloaded and checked |
| 1. Audio basics and ICBHI loader | Oct 18 to 19 | 5 to 6 | Breathing cycles cut, labelled and split by patient |
| 2. Features and gradient boosting | Oct 20 to 21 | 5 to 6 | **First real result**: Wheeze Lab baseline with ICBHI score |
| 3. Log-mel CNN | Oct 22 to 23 | 5 to 6 | CNN vs baseline comparison table |
| 4. Cough detector | Oct 24 to 25 | 5 to 6 | Window-level cough classifier |
| 5. Synthetic nights and event scoring | Oct 26 to 27 | 5 to 6 | Event-level F1 and count agreement |
| 6. Night-to-Week and demo app | Oct 28 | 3 to 4 | Weekly trend logic and Streamlit demo |
| 7. README, report, ship | Oct 29 to 30 | 4 to 5 | Public repo, report, resume bullets with real numbers |

If you fall behind, cut phase 3 (the CNN) before cutting anything else. Phases 0, 1, 2, 4, 5 are the core.

---

## Repo layout (final)

Keep it flat. This is the whole thing.

```
coughcast/
├── coughcast/
│   ├── __init__.py
│   ├── audio.py        # load, resample, band-pass, framing
│   ├── icbhi.py        # ICBHI files -> labelled cycles + patient split
│   ├── features.py     # hand-built features and log-mel
│   ├── metrics.py      # ICBHI score, event matching, bootstrap CI
│   ├── models.py       # one small CNN
│   ├── cough_data.py   # COUGHVID + ESC-50 -> 1-second windows
│   ├── nights.py       # synthetic night generator
│   ├── detect.py       # sliding-window detector -> events
│   ├── weekly.py       # nightly summary -> weekly trend + flag
│   ├── train_wheeze.py # script
│   └── train_cough.py  # script
├── app.py              # Streamlit demo
├── tests/
├── results/            # small JSON/CSV outputs from scripts (committed)
├── figures/            # PNGs for the README (committed)
├── data/               # datasets and caches (never committed)
├── docs/
│   ├── report.md
│   └── ethics.md
├── CLAUDE.md
├── .claude/settings.json
├── requirements.in
├── requirements.txt
├── .gitignore
└── README.md
```

Each module starts small and grows only when a phase needs it.

---

# Phase 0: Setup and data (Oct 17, 3 to 4 hours)

## Goal

An empty but correct repo, AI guardrails in place, and the three datasets downloaded and opened once.

## Done when

- [ ] Repo created on GitHub by you, cloned locally
- [ ] `CLAUDE.md` and `.claude/settings.json` in place (contents below)
- [ ] Virtual environment works; `pytest -q` runs (zero tests is fine)
- [ ] ICBHI, COUGHVID and ESC-50 downloaded into `data/`
- [ ] You opened one file from each dataset and listened to it
- [ ] `docs/ethics.md` written with the licence and terms of each dataset

## Learn first (45 min)

**Concepts**

- **What a digital audio file is:** a list of numbers (samples) plus a sampling rate (samples per second). 8,000 Hz means 8,000 numbers per second of sound.
- **Nyquist:** a sampling rate can only represent frequencies up to half of it. 8 kHz audio holds content up to 4 kHz.
- **Dataset licences and terms:** what you're allowed to do with each dataset, and what you must cite.

**Where to learn**

- 3Blue1Brown, "But what is the Fourier Transform? A visual introduction" (YouTube, about 20 min). Watch it now; it pays off in phase 1.
- Each dataset's own page (links in Sources). Read the "how to cite" and licence sections.

**Self-check**

1. A file has 40,000 samples at 8 kHz. How long is it?
2. Why can't 8 kHz audio contain a 5 kHz tone?
3. Which of the three datasets has a non-commercial licence? What does that mean for your portfolio?

## Steps

1. **Create the repo (you).** On GitHub, create `coughcast` (public, no template), clone it.
2. **Add the guardrails (you paste, AI can draft).**
   - Copy `CLAUDE.md` from the separate file I gave you into the repo root.
   - Create `.claude/settings.json`:

     ```json
     {
       "permissions": {
         "deny": [
           "Bash(git add *)",
           "Bash(git commit *)",
           "Bash(git push *)",
           "Bash(git reset *)",
           "Bash(git checkout *)",
           "Bash(git rebase *)",
           "Bash(gh *)",
           "Bash(rm -rf *)"
         ]
       }
     }
     ```

     Deny rules are checked before allow rules, so these always win. One caveat from Claude Code's own docs: a Bash rule matches the command as written, not every way of running the same program (for example, `git -C . push` isn't matched). So these rules stop the normal case, and your rule of reading every permission prompt stops the rest. Don't run Claude Code in a mode that skips prompts on this repo.
3. **Environment (AI writes, you run).** Python 3.12 with `uv`, same as BreathCam.
   - `requirements.in`: `numpy`, `scipy`, `pandas`, `soundfile`, `librosa`, `scikit-learn`, `matplotlib`, `torch`, `torchaudio`, `streamlit`, `pytest`
   - `uv pip compile requirements.in -o requirements.txt`, then `uv pip install -r requirements.txt`
   - You also need `ffmpeg` (you already have it from BreathCam) because COUGHVID audio isn't plain WAV.
4. **`.gitignore` (AI writes).** Ignore `data/`, `.venv/`, `*.wav`, `*.webm`, `*.ogg`, `*.npz`, `*.pt`, `__pycache__/`, `.DS_Store`.
5. **Download scripts (AI writes, you run).**
   - **ICBHI 2017:** from the challenge page, the full database zip. You need the `.wav` files, the matching `.txt` annotation files, and the official train/test split file.
   - **ESC-50:** clone or download the GitHub repo; you need `audio/` and `meta/esc50.csv`.
   - **COUGHVID:** from Zenodo. Check the file size before downloading; use the version whose size you can handle. Read the metadata columns before writing any code: find the column that scores how likely a recording contains a cough, and read in the dataset paper what threshold the authors recommend.
6. **Look at the data (you).** Open one file from each in Audacity or a notebook, plot the waveform, listen. Write three sentences in `docs/ethics.md` per dataset: source, licence or terms, citation.
7. **First commit (you):** `chore: repo skeleton, AI guardrails, environment`.

## AI does / You do

| AI does | You do |
|---|---|
| Drafts `requirements.in`, `.gitignore`, download scripts | Creates the GitHub repo |
| Explains anything in the datasets' docs you don't follow | Pastes `CLAUDE.md` and `settings.json`, checks they load |
| | Runs the downloads, reads the licences, writes `docs/ethics.md` |
| | Listens to real files |
| | Commits |

## Prompts

> Read CLAUDE.md. Create requirements.in with: numpy, scipy, pandas, soundfile, librosa, scikit-learn, matplotlib, torch, torchaudio, streamlit, pytest. Create a .gitignore for a Python audio ML project where data/, audio files, .npz caches and model weights must never be committed. Don't run any git commands.

> Write scripts/download_esc50.sh and scripts/download_icbhi.sh that download into data/esc50 and data/icbhi and print what they found. Don't run them. Explain each line.

## Pitfalls

- Committing a dataset by accident. Run `git status` before every `git add` and check nothing under `data/` shows up.
- ESC-50 is licensed for non-commercial use. A public portfolio repo that doesn't redistribute the audio is fine; never commit its files.
- Starting to code before listening to the data. You will misread labels if you never heard a wheeze.

---

# Phase 1: Audio basics and the ICBHI loader (Oct 18 to 19, 5 to 6 hours)

## Goal

Turn ICBHI recordings into a clean table of labelled breathing cycles, split so that no patient appears in both train and test.

## Done when

- [ ] `audio.py`: load any file as mono float32 at a target rate; band-pass filter
- [ ] `icbhi.py`: one row per breathing cycle (patient, recording, start, end, crackle, wheeze, label, split)
- [ ] A test proves no patient is in both train and test
- [ ] A test proves cycle cutting returns the right number of samples
- [ ] `results/icbhi_summary.json`: number of cycles per class per split, written by a script
- [ ] A figure: one waveform and spectrogram each of a normal, crackle and wheeze cycle (`figures/`)
- [ ] Explain-back done

## Learn first (90 min)

**Concepts**

- **Resampling:** changing the sampling rate. ICBHI files were recorded at different rates (4 kHz to 44.1 kHz), so everything must be brought to one rate. This plan uses **8 kHz**, a common choice for lung sounds, which also matches the pediatric SPRSound dataset if you extend later.
- **Band-pass filter:** keeps a range of frequencies, removes the rest. You already used one in BreathCam. Lung-sound papers often band-pass to reduce heart sounds and high-frequency hiss. Choose your cutoffs from a paper you cite, and write the reason in a code comment. Don't copy a number without a reason.
- **Zero-phase filtering (`sosfiltfilt`):** filters forwards and backwards so the signal doesn't shift in time. Matters when you cut cycles at exact times.
- **Spectrogram:** the Fourier transform applied to short overlapping slices of audio, stacked over time. The x-axis is time, the y-axis is frequency, and brightness is energy.
- **What the labels sound and look like:** wheezes are continuous, musical tones, which show up as horizontal lines in a spectrogram. Crackles are short, explosive, non-musical clicks, which show up as thin vertical streaks.
- **Patient-level splitting:** the same leakage lesson as your BreathCam experiment.

**Where to learn**

- Valerio Velardo, "Audio Signal Processing for Machine Learning" (YouTube playlist, The Sound of AI). Watch the episodes on sampling, the Fourier transform, and the short-time Fourier transform.
- librosa documentation, the getting-started tutorial (librosa.org).
- SciPy documentation, `scipy.signal.butter` and `scipy.signal.sosfiltfilt`.
- The ICBHI database paper: Rocha et al., 2019, *Physiological Measurement* 40 035001. Read the sections on annotation and the official split.

**Self-check**

1. Why must every file be resampled to the same rate before you compare features?
2. In a spectrogram, what does a wheeze look like? A crackle?
3. What goes wrong if a patient's cycles appear in both train and test?
4. Why `sosfiltfilt` and not `lfilter`?

## Steps

1. **`audio.py` (AI writes, you review):**
   - `load_audio(path, target_sr)`: read with `soundfile`, convert to mono, resample with `librosa.resample` if needed, return a float32 array.
   - `bandpass(x, sr, low, high, order)`: Butterworth in second-order sections, applied with `sosfiltfilt`.
   - Tests: a synthetic 50 Hz + 500 Hz sine through a band-pass that should keep only one of them. Check the energy at each frequency after filtering.
2. **Parse annotations (AI writes, you review).** Each ICBHI `.txt` has one line per cycle: start (s), end (s), crackle (0/1), wheeze (0/1). The file name encodes patient ID, recording index, chest location, acquisition mode, and device. Parse those into columns too; device and chest location become useful later.
3. **Label mapping:** `normal` (0,0), `crackle` (1,0), `wheeze` (0,1), `both` (1,1). Add `wheeze_positive` = wheeze or both.
4. **Split:** use the official train/test split file. Then write the test: the set of patient IDs in train and in test must not overlap. If the test fails, find out why before doing anything else.
5. **Validation split:** inside train, use `GroupKFold` with patient ID as the group, so tuning never sees a test patient.
6. **Cycle cutting:** `cut_cycle(x, sr, start, end)` returns the slice. Cycle lengths vary a lot; don't pad or crop yet. Record the length distribution in the summary JSON. Phase 3 decides how to handle it.
7. **Summary script (AI writes, you run):** counts per class per split, cycle length percentiles, sampling rates found, devices found. Save to `results/icbhi_summary.json`.
8. **Figure (AI writes, you run and look):** waveform and spectrogram of one cycle per class. Look at it. Can you see the wheeze lines?

Commits (you): `feat(audio): load, resample, band-pass`, `feat(icbhi): parse cycles and patient split`, `test: no patient overlap`, `docs: ICBHI summary and example spectrograms`.

## AI does / You do

| AI does | You do |
|---|---|
| Writes `audio.py`, `icbhi.py` and their tests | Picks the band-pass cutoffs from a paper and writes the reason |
| Writes the summary and figure scripts | Runs them; reads every number in the summary |
| Explains any line you ask about | Listens to a few cycles of each class and checks their labels by ear and by spectrogram |
| | Explain-back: how a recording becomes a labelled, split cycle |

## Prompts

> Read CLAUDE.md. In coughcast/audio.py write load_audio(path, target_sr) and bandpass(x, sr, low, high, order=4) using soundfile, librosa.resample and scipy.signal butter + sosfiltfilt. Keep each function under 25 lines. Write tests in tests/test_audio.py using synthetic sine waves; no real data in tests. Run pytest and show me the output. Then explain sosfiltfilt vs lfilter in 5 lines.

> In coughcast/icbhi.py, parse ICBHI annotation files and file names into a pandas DataFrame with one row per breathing cycle. Columns: patient_id, recording, location, mode, device, start, end, crackle, wheeze, label, wheeze_positive, split. Use the official split file in data/icbhi. Add a test that fails if any patient_id is in both train and test. Don't pad or crop cycles.

## Pitfalls

- Assuming every file has the same sampling rate. It doesn't.
- Stereo files: average to mono.
- Trusting the official split blindly: test it.
- Filtering after cutting cycles. Filter the whole recording, then cut, so the filter has no edge effects at cycle boundaries.

---

# Phase 2: Features and gradient boosting (Oct 20 to 21, 5 to 6 hours)

## Goal

A classical, explainable baseline: hand-built audio features per cycle, a gradient-boosted classifier, and an honest score with a confidence interval. This is your **first real result**.

## Done when

- [ ] `features.py`: a fixed-length feature vector for any cycle, regardless of its length
- [ ] Features cached to `data/cache/icbhi_features.npz`
- [ ] `metrics.py`: sensitivity, specificity and ICBHI score, with a test on a hand-made example
- [ ] Bootstrap 95% CI resampling **patients**, not cycles
- [ ] `results/wheeze_baseline.json`: Se, Sp, ICBHI score, CI, wheeze-positive recall, confusion matrix
- [ ] `figures/wheeze_baseline_importance.png`: top 15 features by permutation importance
- [ ] Explain-back done

## Learn first (90 min)

**Concepts**

- **Framing:** short windows (tens of ms) with overlap. Features are computed per frame, then summarised per cycle (mean and standard deviation). That's how a cycle of any length becomes a fixed-length vector.
- **MFCCs:** a compact description of the spectrum's shape. Mel scale, then log, then a cosine transform. Deltas capture how they change over time.
- **Spectral features:**
  - **Centroid:** the "centre of mass" of the spectrum
  - **Bandwidth:** how spread out it is
  - **Roll-off:** the frequency below which most energy sits
  - **Flatness:** tonal (low) vs noise-like (high). A useful candidate for spotting musical wheezes.
  - **Zero-crossing rate:** how often the signal changes sign. Rises with noisiness and high-frequency content.
  - **RMS energy:** loudness.
- **Gradient boosting:** many small decision trees, each correcting the last. scikit-learn's `HistGradientBoostingClassifier` is fast and needs no scaling.
- **Class imbalance:** about half of ICBHI cycles are normal. Use class weights, and never report accuracy alone.
- **ICBHI metrics:**
  - Sensitivity = correctly classified abnormal cycles (crackle, wheeze, both) ÷ all abnormal cycles
  - Specificity = correctly classified normal cycles ÷ all normal cycles
  - ICBHI score = the average of the two
- **Permutation importance:** shuffle one feature, see how much the score drops.

**Where to learn**

- Valerio Velardo's playlist: episodes on MFCCs and on time/frequency-domain audio features.
- librosa feature docs: `mfcc`, `spectral_centroid`, `spectral_bandwidth`, `spectral_rolloff`, `spectral_flatness`, `zero_crossing_rate`, `rms`.
- scikit-learn User Guide: "Histogram-Based Gradient Boosting", "Permutation feature importance", "Cross-validation" (`GroupKFold`).

**Self-check**

1. Why summarise per-frame features with mean and standard deviation instead of using all frames?
2. Why would spectral flatness help separate wheezes from normal breathing?
3. A model predicts "normal" for everything. What are its sensitivity, specificity and ICBHI score?
4. Why resample patients, not cycles, when bootstrapping?

## Steps

1. **Frame settings at 8 kHz:** `n_fft=512` (64 ms), `hop_length=128` (16 ms). Write them as constants at the top of `features.py` with a comment on what they mean in milliseconds.
2. **`cycle_features(x, sr)` (AI writes, you review):**
   - 13 MFCCs + 13 deltas → mean and std each (52 numbers)
   - centroid, bandwidth, roll-off, flatness, ZCR, RMS → mean and std each (12 numbers)
   - cycle duration (1 number)
   - Return a 1-D array and a matching list of feature names.
3. **Cache:** compute features for every cycle once, save `X`, `y`, `patient_id`, `split` and the feature names to `.npz`. Training loads the cache.
4. **`metrics.py` (AI writes, you check by hand):** `icbhi_scores(y_true, y_pred)` returning Se, Sp, score. Test it on a 10-example case you work out on paper first.
5. **Bootstrap (AI writes):** `patient_bootstrap_ci(df, metric_fn, n=1000, seed=0)` that resamples patient IDs with replacement and recomputes the metric. Reuse the idea from BreathCam.
6. **Train (`train_wheeze.py --model hgb`):**
   - `HistGradientBoostingClassifier(class_weight="balanced", random_state=0)`
   - Tune 2 or 3 settings only (`learning_rate`, `max_depth`, `max_iter`) with `GroupKFold(5)` on train.
   - Fit on all of train, evaluate **once** on test.
   - Write `results/wheeze_baseline.json`.
7. **Permutation importance** on the test set; plot the top 15.
8. **Compare with the published yardstick:** a CRNN plus bagging k-NN method reported Se 0.670, Sp 0.863 and ICBHI score 0.766 on ICBHI. Your baseline will probably score lower. That's fine; you're building an honest baseline, not chasing a leaderboard.

Commits (you): `feat(features): cycle features and cache`, `feat(metrics): ICBHI score and patient bootstrap`, `exp: gradient boosting baseline`.

## AI does / You do

| AI does | You do |
|---|---|
| Writes features, metrics, bootstrap, training script and tests | Works out the 10-example metric test by hand first |
| Explains each feature in one sentence when you ask | Decides the 2 or 3 settings to tune and why |
| Writes the plotting code | Runs training; copies numbers from the JSON into your notes |
| | Looks at the confusion matrix: which class gets confused with which? Write 3 sentences on why |

## Prompts

> Read CLAUDE.md. In coughcast/features.py write cycle_features(x, sr) returning (vector, names) with: 13 MFCC + 13 deltas (mean and std), and mean/std of spectral centroid, bandwidth, rolloff, flatness, zero-crossing rate and RMS, plus duration. n_fft=512, hop=128 as named constants with a comment in ms. Test that two cycles of different lengths give vectors of the same length.

> In coughcast/metrics.py write icbhi_scores(y_true, y_pred) for labels normal/crackle/wheeze/both, using the ICBHI definitions of sensitivity and specificity. I will give you a hand-worked example for the test. Then write patient_bootstrap_ci that resamples patients with replacement.

> Write coughcast/train_wheeze.py with --model hgb. Load the feature cache, tune only learning_rate, max_depth and max_iter with GroupKFold(5) by patient on train, refit on train, evaluate once on test, write results/wheeze_baseline.json including a 95% patient bootstrap CI. Don't print a summary that rounds numbers; I'll read the JSON.

## Pitfalls

- Fitting any scaler or feature selection on all data. Fit only on train.
- Looking at the test score, changing something, looking again. You get **one** test run per model. Tune on validation folds.
- Reporting accuracy. With about half the cycles normal, accuracy hides failure on wheezes.

---

# Phase 3: Log-mel CNN (Oct 22 to 23, 5 to 6 hours)

## Goal

A small CNN on log-mel spectrograms, compared fairly with the gradient-boosting baseline on the same split and metrics.

## Done when

- [ ] Fixed-length log-mel input per cycle, with the length decision written down
- [ ] Normalisation statistics computed on train only
- [ ] `models.py`: one small CNN, parameter count printed
- [ ] Training with class-weighted loss, early stopping on validation ICBHI score, fixed seed
- [ ] Time and frequency masking augmentation on train only
- [ ] `results/wheeze_cnn.json` with the same fields as the baseline
- [ ] `results/wheeze_comparison.csv`: baseline vs CNN, with CIs and the paired difference
- [ ] Explain-back done

## Learn first (60 min)

**Concepts**

- **Log-mel spectrogram:** a spectrogram with the frequency axis warped to the mel scale and energy put on a log scale. It's an image, so your GTSRB CNN skills apply directly.
- **Fixed length:** CNNs in batches need equal-sized inputs. Choose a length that covers most cycles (look at your phase 1 percentiles). Crop longer cycles; pad shorter ones by repeating the cycle. Repeat-padding is common for lung sounds because zero-padding inserts fake silence.
- **SpecAugment-style masking:** blank out random time strips and frequency bands during training so the model can't rely on one narrow cue.
- **Paired comparison:** both models scored on the same test cycles; bootstrap the **difference**. You did this in BreathCam (CNN vs Welch).

**Where to learn**

- torchaudio docs: `MelSpectrogram`, `AmplitudeToDB`, `FrequencyMasking`, `TimeMasking`.
- Park et al., 2019, "SpecAugment" (arXiv). Read the abstract and the figure showing the masks.
- Your own GTSRB code: reread your model and training loop before asking the AI for a new one.

**Self-check**

1. Why compute normalisation statistics only on train?
2. Why repeat-pad instead of zero-pad?
3. What does "the difference's CI includes zero" mean, in plain English?

## Steps

1. **Length decision (you):** look at the cycle-length percentiles; pick a fixed length (for example, the 90th percentile, rounded). Write the choice and the percent of cycles cropped into the README notes.
2. **Log-mel (AI writes):** 64 mel bands, the same `n_fft` and hop as phase 2, `AmplitudeToDB`. Cache to `.npz`.
3. **CNN (AI writes, you review against your GTSRB model):** 3 or 4 conv blocks (conv → batch norm → ReLU → max pool), global average pooling, one linear layer to 4 classes. Aim for a few hundred thousand parameters.
4. **Training loop:** Adam, cross-entropy with class weights, batch size 32 or 64, device `mps` if available else `cpu`, early stopping (patience 5) on validation ICBHI score, `torch.manual_seed(0)`.
5. **Augmentation:** one frequency mask and one time mask per training example. Never on validation or test.
6. **Evaluate once on test.** Same metrics, same bootstrap.
7. **Comparison table:** baseline vs CNN, plus the paired bootstrap difference in ICBHI score.

Commits (you): `feat(features): cached log-mel`, `feat(models): small CNN`, `exp: CNN vs gradient boosting`.

## AI does / You do

| AI does | You do |
|---|---|
| Writes log-mel caching, CNN, training loop | Chooses the fixed length from your data |
| Adds `mps` device handling | Checks the parameter count is small |
| Writes the comparison script | Runs training (watch the laptop's heat; train in short runs) |
| | Decides what the comparison means and writes 3 sentences |

## Prompts

> Read CLAUDE.md. Here is my GTSRB model [paste]. Write coughcast/models.py with a smaller version for 1x64xT log-mel input and 4 classes, using global average pooling. Print the parameter count. No other model classes.

> Write the training path in train_wheeze.py for --model cnn: class-weighted cross-entropy, Adam, early stopping on validation ICBHI score with patience 5, seed 0, device mps if available. FrequencyMasking and TimeMasking on train only. Evaluate once on test and write results/wheeze_cnn.json in the same format as the baseline.

## Pitfalls

- The CNN wins on one seed and loses on another. If you have time, run 3 seeds and report the range, not the best.
- Data loading eating all 8 GB: load from the cache; use `num_workers=0` on macOS if loading hangs.
- Calling a gap a win when its CI includes zero. You already know this one from BreathCam.

---

# Phase 4: Cough detector (Oct 24 to 25, 5 to 6 hours)

## Goal

A model that says "cough" or "not cough" for any 1-second window, trained so it doesn't fire on snoring, breathing, laughing or household noise.

## Done when

- [ ] `cough_data.py`: 1-second windows at 16 kHz, labelled, split
- [ ] Positives from COUGHVID, using the metadata's cough-likelihood column and the threshold the authors recommend
- [ ] Negatives from all ESC-50 classes except "coughing"
- [ ] ESC-50's own "coughing" clips held out as an extra test of coughs from a different source
- [ ] Gradient boosting (phase 2 features) and the CNN (phase 3 model) both trained
- [ ] `results/cough_window.json`: precision, recall, F1, PR-AUC on test, plus recall on the held-out ESC-50 coughs
- [ ] Explain-back done

## Learn first (60 min)

**Concepts**

- **Why 16 kHz here:** coughs carry energy higher than lung sounds recorded through a stethoscope, and phone recordings capture it. 16 kHz is a common rate for general sound-event models.
- **Hard negatives:** non-cough sounds that look like coughs (sneezing, laughing, door knocks). They teach the model the boundary.
- **Precision vs recall, PR-AUC:** with rare positives, the precision-recall curve is more honest than ROC.
- **Out-of-distribution test:** a test set from a different source than training. If the model only learned "COUGHVID-style recording", it fails here.
- **Grouping:** ESC-50 comes pre-split into 5 folds that keep clips from the same source recording together; respect the folds. For COUGHVID, split by recording.

**Where to learn**

- Orlandic et al., 2021, "The COUGHVID crowdsourcing dataset..." (*Scientific Data*). Read the metadata and the cough-detection sections.
- Piczak, 2015, "ESC: Dataset for Environmental Sound Classification". Read the dataset description and the folds.
- scikit-learn User Guide: "Precision-Recall".

**Self-check**

1. Why hold out ESC-50 coughs instead of training on them?
2. Your detector reaches 0.98 F1 on test but 0.60 recall on ESC-50 coughs. What happened?
3. Why does a random split of ESC-50 clips leak information?

## Steps

1. **Convert COUGHVID (AI writes, you run):** use `ffmpeg` to convert to 16 kHz mono WAV in `data/coughvid_wav/`. Start with a subset (for example, 1,500 recordings above the threshold) to stay inside 8 GB.
2. **Extract cough windows:** in each recording, take the 1-second window with the highest RMS energy, and optionally a second one if it's clearly separate. Keep it simple; one per recording is enough for v1.
3. **ESC-50 negatives:** each 5-second clip → five 1-second windows. Drop silent windows (RMS below a threshold you print and choose).
4. **Splits:**
   - ESC-50: folds 1 to 3 train, fold 4 validation, fold 5 test
   - COUGHVID: random by recording, 60/20/20, seed 0
   - ESC-50 "coughing": all folds, never trained on, only tested
5. **Features:** reuse `cycle_features` and the log-mel code at 16 kHz. Cache.
6. **Train both models**, tune on validation, evaluate once on test and once on the held-out ESC-50 coughs.
7. **Choose a threshold** on validation that gives the precision you want (start by maximising F1). Save it in `results/cough_window.json`; phase 5 uses it.

Commits (you): `feat(cough): windows from COUGHVID and ESC-50`, `exp: cough window classifier`.

## AI does / You do

| AI does | You do |
|---|---|
| Writes conversion, windowing, splits, training | Reads the COUGHVID paper's metadata section and picks the threshold |
| Writes the precision-recall plot | Listens to 10 false positives and 10 false negatives, and writes what they are |
| | Chooses which model goes into phase 5, and writes why |

## Prompts

> Read CLAUDE.md. Write coughcast/cough_data.py that builds 1-second 16 kHz windows: COUGHVID positives (highest-RMS window per recording, recordings above a threshold I'll give you from the metadata column), ESC-50 negatives from every class except coughing, and a separate held-out set of ESC-50 coughing windows. Use ESC-50 folds 1-3/4/5 for train/val/test. Seed 0. Cache to data/cache/cough_windows.npz.

> Write train_cough.py reusing features.py and models.py. Train hgb and cnn, pick a threshold that maximises F1 on validation, evaluate once on test and on the held-out ESC-50 coughs, write results/cough_window.json and a precision-recall plot.

## Pitfalls

- The model learns the recording device, not the cough. That's why the ESC-50 cough test exists.
- No speech in the negatives. ESC-50 has no talking. Note it as a limitation, or (stretch) add a few minutes of your own speech, recorded by you.
- Silent ESC-50 windows labelled "not cough" are too easy; drop them so the score isn't inflated.

---

# Phase 5: Synthetic nights and event scoring (Oct 26 to 27, 5 to 6 hours)

## Goal

Turn the window classifier into a detector that finds cough **events** with start times in a long recording, and score it the way sound-event research does.

## Done when

- [ ] `nights.py`: generates a night of audio plus a ground-truth CSV of cough onsets, from a seed
- [ ] Nights built only from test-split audio (no clip used in training appears in a test night)
- [ ] `detect.py`: sliding window → probabilities → events
- [ ] Event matching with an onset tolerance, one detection per true cough, unit-tested
- [ ] `results/night_events.json`: precision, recall, F1 overall and per signal-to-noise ratio, count error per night
- [ ] `figures/night_counts_bland_altman.png`
- [ ] `figures/night_timeline_example.png`: one night with true and detected coughs marked
- [ ] One self-recorded 10-minute test session scored (see step 7)
- [ ] Explain-back done

## Learn first (75 min)

**Concepts**

- **Sliding-window detection:** run the classifier on 1-second windows every 0.25 s; consecutive windows above the threshold merge into one event.
- **Event-based vs segment-based scoring:** event-based asks "did you find each cough, at about the right time?"; segment-based asks "was each second labelled right?". For counting coughs, event-based is the right one.
- **Onset tolerance:** a detection counts as correct if its onset is within, say, ±0.5 s of a true onset. State the tolerance; results depend on it.
- **Signal-to-noise ratio (SNR) in dB:** how loud the cough is relative to the background. 20 dB is a clear cough; 0 dB is as loud as the noise.
- **Count agreement:** for each night, detected count vs true count. Bland-Altman, which you already know.

**Where to learn**

- Mesaros, Heittola and Virtanen, 2016, "Metrics for Polyphonic Sound Event Detection" (*Applied Sciences*). Read the event-based metrics section.
- Your BreathCam Bland-Altman code.

**Self-check**

1. Two detections both overlap one true cough. How many true positives, how many false positives?
2. Why must night audio come only from test-split clips?
3. Your F1 is 0.9 at 20 dB and 0.4 at 0 dB. Which number goes in a bullet, and how do you word it honestly?

## Steps

1. **Night generator `make_night(seed, minutes, cough_clips, background_clips)` (AI writes, you review):**
   - Length is a parameter. Use **10 minutes** while developing; a few 2-hour nights for the final run if your laptop handles it.
   - Background: concatenate test-split ESC-50 clips from quiet household classes (for example breathing, snoring, clock tick, rain, washing machine), plus low-level noise.
   - Insert a random number of coughs at random times, at least 2 s apart, each scaled to an SNR drawn from {0, 5, 10, 20} dB.
   - Save audio to `data/nights/` and ground truth to CSV: onset, offset, SNR.
2. **`detect.py`:** window 1 s, hop 0.25 s, run the phase 4 model, threshold, merge consecutive positives, drop events shorter than a minimum, return a list of (onset, offset, max probability).
3. **Event matching in `metrics.py`:** greedy one-to-one matching within the tolerance. Test with tiny hand-made cases: an exact match, a near miss, a double detection, a missed cough.
4. **Validation nights vs test nights:** generate 20 nights from validation clips to re-tune the threshold and minimum event length; generate a separate 20 to 50 nights from test clips and score them once.
5. **Scoring script:** overall and per-SNR precision, recall and F1; per-night true vs detected counts; Bland-Altman.
6. **Timeline figure:** one test night's waveform with true onsets and detections marked.
7. **Self-recorded session (you):** a 10-minute recording in your room, **only you present**, where you cough at times you note down (for example every 1 to 2 minutes), talk a little, and leave some normal background sound. Write the cough times in a CSV. Score it. Keep the raw audio out of the repo; commit only the CSV and the score. Delete the raw audio once you've scored it, as BreathCam's ethics note does.

Commits (you): `feat(nights): synthetic night generator`, `feat(detect): sliding-window event detector`, `test: event matching`, `exp: event-level scores on synthetic nights`.

## AI does / You do

| AI does | You do |
|---|---|
| Writes generator, detector, matching and tests | Works out the four matching test cases on paper first |
| Writes scoring and figures | Chooses the tolerance and writes why |
| | Records and annotates the self-test session, alone |
| | Looks at the worst night and writes what went wrong |

## Prompts

> Read CLAUDE.md. Write coughcast/nights.py with make_night(seed, minutes, cough_clips, background_clips, snrs=(0,5,10,20)) that returns audio and a DataFrame of cough onset, offset, snr. Coughs at least 2 s apart. Only takes clips passed in; the caller ensures they are test-split. Tests: same seed gives the same night; every onset is inside the audio; measured SNR of an inserted cough is within 1 dB of the requested value.

> Write match_events(true_onsets, detected_onsets, tolerance) in metrics.py: greedy one-to-one matching, returns TP, FP, FN. I'll give you four hand-worked cases for tests.

## Pitfalls

- Using the same cough clip in many nights and in training. Keep the test pool separate, and allow reuse within test nights only if you say so.
- Tuning the threshold on test nights. Use validation nights.
- Reporting only the 20 dB result. Report the full table.

---

# Phase 6: Night-to-Week and demo app (Oct 28, 3 to 4 hours)

## Goal

Show the last step of the idea, nights rolled into a weekly trend with a simple flag, and a demo anyone can click.

## Done when

- [ ] `weekly.py`: nightly summary → weekly summary → flag
- [ ] A simulation test: planted rises are flagged, flat periods mostly aren't, reported as numbers
- [ ] `app.py`: upload a WAV (up to 10 minutes), see detected coughs on a timeline and a count; second tab shows a simulated 6-week chart
- [ ] The app processes audio in memory and saves nothing
- [ ] Explain-back done

## Learn first (30 min)

**Concepts**

- **Nightly features:** cough count, coughs per hour, cough clusters (coughs closer together than a gap you choose), time of first cough.
- **Personal baseline:** compare this week with this person's own previous weeks, not with other people.
- **Simple flag:** this week's mean nightly count is above the previous two weeks' mean by more than a set number of standard deviations (or a set percent). Keep it this simple.
- **Why this matters clinically:** a 2020 ERS abstract by Rassouli and colleagues found weekly nocturnal cough was associated with asthma control in the same and the following week. You're building the plumbing that would make that usable, not proving it.

**Where to learn**

- The Rassouli et al. abstract (link in Sources).
- Streamlit docs: `file_uploader`, `pyplot`, `tabs`.

**Self-check**

1. Why compare with a personal baseline instead of a population average?
2. What does your simulation test prove, and what doesn't it prove?

## Steps

1. **`weekly.py` (AI writes):** `nightly_summary(events, night_minutes)`, `weekly_summary(nights_df)`, `flag_weeks(weekly_df, k)`.
2. **Simulation (AI writes, you design):** many simulated 6-week "people", each night's count drawn from a Poisson rate. Half the people get a planted rise in week 5; half stay flat. Report: share of planted rises flagged in week 5, share of flat people flagged anywhere. This tests the flag rule only. Label it as simulation everywhere.
3. **`app.py` (AI writes, you test by hand):** tab 1 upload and timeline; tab 2 simulated weekly chart. Process the upload in memory; write nothing to disk. One-line disclaimer at the top: research prototype, not a medical device.

Commits (you): `feat(weekly): nightly and weekly summaries with a flag`, `exp: flag rule on simulated cohorts`, `feat(app): Streamlit demo`.

## AI does / You do

| AI does | You do |
|---|---|
| Writes `weekly.py`, the simulation and `app.py` | Designs the simulation: rates, size of the planted rise, number of people |
| | Tests the app with your self-recorded CSV session (or a test night) |
| | Checks nothing gets written to disk while the app runs |

## Prompts

> Read CLAUDE.md. Write coughcast/weekly.py with nightly_summary, weekly_summary and flag_weeks(weekly_df, k) where a week is flagged if its mean nightly count exceeds the mean of the previous two weeks by k standard deviations. Then a script that simulates N people over 6 weeks with Poisson nightly counts, plants a rise in week 5 for half of them, and writes results/weekly_flag_sim.json with the flag rate for planted and flat people. Label everything as simulation.

## Pitfalls

- Presenting simulated weeks as if they were real data. They aren't, and the README must say so in the first sentence of that section.
- Over-building the app. Two tabs, one upload, one chart each.

---

# Phase 7: README, report, ship (Oct 29 to 30, 4 to 5 hours)

## Goal

A repo a PI can read in 5 minutes, a 2-page report, and resume bullets with real numbers.

## Done when

- [ ] README: one-line summary, demo GIF or image, how to run, results tables, limitations, ethics, data sources
- [ ] Every number in the README is copied from a file in `results/`, and the file is named next to the table
- [ ] `docs/report.md`: question, data, methods, results, limitations, what you'd do with real pediatric data
- [ ] `pytest -q` passes from a fresh clone (you test this in a new folder)
- [ ] GitHub About line matches the README exactly. No feature listed that isn't built.
- [ ] 2 to 3 resume bullets with numbers from `results/`

## Learn first (30 min)

- Reread your BreathCam README; reuse its structure: limitations first-class, n stated plainly.
- Reread Q3 of the fit report: the BreathCam About-line problem. Don't repeat it.

## Steps

1. **AI drafts the README with `[ ]` blanks** for every number. You fill each blank from `results/` and check the file it came from.
2. **Limitations section (you write, AI can edit wording):**
   - Wheeze model: adult-heavy stethoscope data, not phone audio, not children
   - Cough detector: crowdsourced coughs; no speech negatives (unless added); split by recording, so if one person submitted several recordings they could land in both train and test
   - Nights: synthetic; one self-recorded session, n = 1
   - Weekly flag: tested on simulation only
   - Not a medical device
3. **Report (AI drafts from your notes, you edit):** 2 pages max.
4. **Fresh-clone test (you):** clone into a new folder, set up the environment from `requirements.txt`, run `pytest -q`. Fix anything that only worked on your machine.
5. **Push and set the About line (you).** Suggested About line once everything is built: "Wheeze and cough detection from audio with event-level evaluation on synthetic nights; research prototype".
6. **Resume bullets (you, with AI help on wording only).** Shapes, blanks filled from `results/`:
   - Built a wheeze classifier on ICBHI 2017 ([ ] cycles, [ ] patients) comparing hand-built spectral features with gradient boosting against a log-mel CNN, reaching an ICBHI score of [ ] (95% patient bootstrap CI [ ] to [ ]).
   - Built a cough event detector trained on COUGHVID with ESC-50 hard negatives, reaching [ ] event-level F1 on [ ] synthetic nights (±[ ] s onset tolerance) and [ ] F1 at 0 dB signal-to-noise.
   - Evaluated nightly cough-count agreement with Bland-Altman limits of [ ] to [ ] coughs per night, and validated a weekly trend flag that caught [ ] of planted rises with [ ] false flags in simulation.

Commits (you): `docs: README with results and limitations`, `docs: report`.

## AI does / You do

| AI does | You do |
|---|---|
| Drafts README and report with blanks | Fills every number from `results/` |
| Suggests clearer wording | Writes limitations; edits for honesty |
| | Fresh-clone test, push, About line, resume bullets |

## Prompts

> Read CLAUDE.md and the results/ folder. Draft README.md with sections: summary, demo, install and run, results (one table per results file, with [ ] for every number and the source file named under each table), limitations, ethics, data and citations. Do not write any number. Do not claim pediatric performance or clinical validity.

---

## Stretch (only after phase 7 is pushed)

Each is one weekend at most. Pick at most two.

| Stretch | Why | Size |
|---|---|---|
| Speech-free test | Remove speech-like frames for privacy, measure the drop in cough F1: a privacy-vs-accuracy result | 1 day |
| Grad-CAM on log-mel | You know Grad-CAM; shows where the CNN listens | Half a day |
| Pretrained audio embeddings | Compare a pretrained audio network's embeddings with your features | 1 day |
| SPRSound test | Run the wheeze model on the pediatric SPRSound dataset; this is LittleLungs in miniature | 1 to 2 days |
| AirAware join | Put air quality next to the weekly chart in the app | Half a day |
| GitHub Actions | Run `pytest` on push (you set it up and push it) | 1 hour |

---

## Interview prep: questions to answer out loud

Practise each in under 2 minutes, without notes.

1. Walk me through how a raw recording becomes a prediction.
2. Why gradient boosting before a CNN?
3. How did you prevent leakage? Show me the test.
4. What is the ICBHI score, and why not accuracy?
5. Why event-based scoring for coughs? What tolerance, and why?
6. Your detector at 0 dB is much worse than at 20 dB. What would you try next?
7. What would change with real children's bedroom recordings?
8. What did the AI write, and how did you check it? (Answer honestly: it drafted code, you reviewed every diff, wrote the tests' expected values by hand, ran every experiment, and wrote the limitations.)

---

## Glossary

| Term | Meaning |
|---|---|
| Sampling rate | Samples per second of audio |
| Band-pass filter | Keeps a frequency range, removes the rest |
| Spectrogram | Energy by frequency over time |
| Log-mel spectrogram | Spectrogram on a perceptual frequency scale with log energy |
| MFCC | Compact numbers describing the spectrum's shape |
| Spectral flatness | Tone-like (low) vs noise-like (high) |
| Breathing cycle | One inhale and exhale, as annotated in ICBHI |
| Sensitivity | Share of true positives found |
| Specificity | Share of true negatives correctly rejected |
| ICBHI score | Average of ICBHI sensitivity and specificity |
| PR-AUC | Area under the precision-recall curve |
| SNR (dB) | Loudness of the signal relative to background |
| Event-based F1 | F1 counting whole events matched within a time tolerance |
| Bland-Altman | Plot of differences vs means to show agreement and its limits |
| Hard negative | A non-target example that resembles the target |

---

## Sources

- [ICBHI 2017 Respiratory Sound Database](https://bhichallenge.med.auth.gr/ICBHI_2017_Challenge)
- [COUGHVID on Zenodo](https://zenodo.org/records/4048312)
- [ESC-50](https://github.com/karolpiczak/ESC-50)
- [Kyutech: CRNN plus bagging k-NN on ICBHI (published yardstick)](https://kyutech.repo.nii.ac.jp/records/2001645)
- [Rassouli et al., ERJ 2020: smartphone nocturnal cough and asthma control](https://publications.ersnet.org/content/erj/56/suppl64/4569)
- [CHEO: MoKA study (RespiSentinel cough recording during sleep)](https://www.cheoresearch.ca/studies/mobile-health-in-kids-with-asthma-moka-study/)
- [Claude Code: configure permissions](https://code.claude.com/docs/en/permissions.md)
- Papers to find by title: Rocha et al. 2019 (ICBHI database); Orlandic et al. 2021 (COUGHVID); Piczak 2015 (ESC-50); Mesaros, Heittola and Virtanen 2016 (sound event detection metrics); Park et al. 2019 (SpecAugment)
