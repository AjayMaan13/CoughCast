# RA Signal Processing (221336) — Fit Report

Oct 16, 2026 · @Ajay

## Bottom line

Apply now. You are a stronger fit than you think: BreathCam's core is already a signal-processing pipeline (band-pass filtering, Welch spectral estimation, peak detection, sliding windows, a quality gate) validated against clinical annotations for 53 ICU patients.

Your real gaps are narrower than "no signal processing": no time-frequency analysis (spectrograms, MFCCs), almost no hand-crafted feature engineering, no audio, and no rare-event classification metrics. Those four are exactly what this project needs.

The single biggest move: RespiSentinel's public study page says it records children's coughing during the first two hours of sleep. Build a nocturnal cough and wheeze detector (proposal in Q5) and you answer every gap with the team's own signal.

One thing to fix today, before anyone reads your GitHub: your BreathCam "About" line claims a 3D CNN (r3d\_18) that your own README lists as future work. Details in Q3.

## Your ML evidence today

You have three real ML projects, and together they show more evaluation rigour than most student applicants. Figures below are from your bullet files and, for BreathCam, checked against the [public README](https://github.com/AjayMaan13/BreathCam).

| Project | What is real and defensible | Signal or time-series content | Flags |
| --- | --- | --- | --- |
| [BreathCam](https://github.com/AjayMaan13/BreathCam) | BIDMC, 53 ICU patients, 4,809 windows, patient-level CV. Welch MAE 1.16, 1D CNN 0.98 breaths/min (gap not significant, CI -0.57 to +0.18). Leakage experiment: random splits gave 0.46. Video MAE 0.11 to 0.18 on 26 windows. pytest suite, SQLite eval layer, face de-identification, TCPS 2 done. | High: filtering, Welch spectrum, peak detection, windowing, quality gate, 1D CNN on a physiological signal | 3D CNN and TensorFlow classifier not built (see Q3) |
| [gtsrb-traffic-classifier](https://github.com/AjayMaan13/gtsrb-traffic-classifier) | 3 CNNs compared on 43 classes; deep CNN 99.17% test accuracy at 401,387 params vs MobileNetV2 94.24%. Grad-CAM, per-class P/R/F1, tf.data, flip-free augmentation, live Gradio demo. | Low: images, but the CNN, augmentation and Grad-CAM skills carry straight over to spectrograms | Started from a CS50AI exercise; say so if asked |
| [LeaseLens](https://github.com/AjayMaan13/LeaseLens) | 3 extractors on one harness; 0.803 vs 0.313 micro-F1 on 40 hand-labelled leases. Bootstrap CI slice audit (0.747 long vs 0.851 medium). SARIMA cut MAPE 2.55% to 1.11% in an 8-fold rolling-origin backtest over 666 months. BERT NER in PyTorch. | Medium: time-series forecasting with honest backtesting; annotation of a gold set | Re-skim bootstrap.py before claiming deep stats fluency |

Verdict on ML depth: solid on model training, evaluation design and leakage; thin on classical ML (no tree models, no feature selection) and on classification of rare clinical events.

## Q1. Skills you are already good for

You already cover 9 of the posting's 12 technical and research asks at a strong level; the three partial ones are the title skills.

| Posting asks for | Your evidence | Fit |
| --- | --- | --- |
| Python and AI frameworks | PyTorch (BreathCam 1D CNN, LeaseLens BERT), TensorFlow/Keras (GTSRB), scikit-learn, pandas, NumPy, SciPy | Strong |
| ML / DL model development, training, evaluation | Patient-level 5-fold CV, bootstrap CIs, Bland-Altman, leakage test, 3-architecture comparison, slice audits | Strong |
| Clinically annotated datasets | BIDMC: 53 ICU patients scored against two annotators' breath marks | Strong |
| Preprocessing, annotation, feature extraction | LeaseLens: 40-document gold set built with your own labelling tool; BreathCam windowing pipeline | Strong |
| Literature reviews | BreathCam: 11 references audited against Crossref and arXiv, related-work doc | Strong |
| Prototype development, testing, debugging, integration | 8-month QA/SDET co-op; BreathCam pytest suite (8 to 38 tests), Streamlit demo verified end to end | Strong |
| Git version control | Every project; phase-by-phase history in BreathCam | Strong |
| Research ethics, privacy, human participant training | TCPS 2 CORE-2022 already completed; consent form and ethics statement written; de-identification tool | Strong, and already done |
| Technical reports and documentation | BreathCam two-page report; LeaseLens model card plus 7 docs | Strong |
| Signal processing | BreathCam filtering, Welch, peak detection, quality gate (one signal type, periodic only) | Partial |
| Feature engineering | FinSight's 4 engineered anomaly features; BreathCam uses Welch peaks, not a feature set | Partial |
| Planning, estimation, progress monitoring | Written phase plan in BreathCam; sprint work on the co-op | Partial |

The research-process half of this posting (ethics, literature, reports, Git, testing) is where you beat most applicants. Lead with it, not apologise around it.

## Q2. Skills that transfer

You said you are not familiar with signal processing. You are; you just learned it on one easy signal and never used the vocabulary. Use the middle column's words in your cover letter and interview.

| What you already did | What signal processing calls it | Where it reappears in respiratory work |
| --- | --- | --- |
| Band-pass filter on the chest-motion signal (SciPy) | Digital filter design | Isolating cough and wheeze energy from room noise |
| Welch spectrum to find the breathing rate | Power spectral density, frequency-domain features | Spectral features and short-time Fourier transforms (spectrograms) |
| Sliding windows over the signal | Framing and windowing | Same idea, shorter frames for audio |
| Quality gate that rejects noisy windows | Signal quality index | Rejecting talking, TV or movement at night |
| Peak detection | Event detection | Finding cough onsets in a long recording |
| 1D CNN on a respiration waveform | Learned features on raw signals | CNN on a spectrogram, which is your GTSRB CNN on a new image type |
| 1D and 2D Grad-CAM | Explainability | Showing which time-frequency region drove a wheeze call |
| Patient-level CV, leakage experiment | Subject-wise splitting | Respiratory datasets publish subject-wise train/test splits for this reason |
| Bootstrap CIs, Bland-Altman on rates | Agreement analysis | Cough-count studies report automated vs human count differences the same way |
| SARIMA with rolling-origin backtest (LeaseLens) | Temporal pattern analysis | Turning nightly counts into a weekly trend |
| Labelling tool and gold set (LeaseLens) | Annotation | Marking cough events and their start and end times |
| Face blurring and metadata stripping | Privacy engineering | Bedroom audio contains speech; strip it before storage |

The honest framing for an interview: "I have applied filtering, spectral estimation and event detection to a periodic physiological signal. I have not yet worked with transient signals like cough or wheeze, and that is what I am building now."

## Q3. The hiring manager's critique

If I were the PI: BreathCam gets you the interview. The gaps below decide whether you are productive on Nov 1 or after a month of ramp-up. The first one could end your candidacy outright.

1. **Your GitHub claims work you have not done.** The BreathCam About line says "compared with 1D and 3D CNNs (PyTorch, r3d\_18)". Your README's Future Work says the 3D video model is not trained yet. A PI clicks the repo, sees both, and stops trusting every number. Your bullet bank has the same problem: `Bo2b` (TensorFlow artifact classifier, 95%), the second `B10` (r3d\_18, 45%) and the second `B11` (92% chest attention) describe nothing in the repo, and two IDs are reused. In research, one invented number is disqualifying. Fix the About line and delete those three bullets today.
2. **Your signal processing is one trick deep.** A resting breath at 12 per minute is close to a sine wave, the friendliest signal in biomedicine. I see no spectrograms, no MFCCs, no wavelets, no resampling, and no reasoning about filter order or cutoffs. Can you explain why your band-pass edges are where they are?
3. **Feature engineering, a title skill, is nearly absent.** You jump from Welch straight to a CNN. Research teams want an interpretable baseline first: a hand-built feature set, feature selection, a gradient-boosted or random-forest model, and feature importances. Without it, a CNN result has nothing to beat.
4. **Everything clinical you have done is regression.** BreathCam reports MAE. This project predicts rare events: exacerbations, wheezes, coughs. I see no sensitivity and specificity, PR curves, class-imbalance handling, threshold choice or calibration on a clinical task. GTSRB's 99% on 43 balanced-ish classes doesn't count.
5. **No audio.** The only passive sensor RespiSentinel describes publicly is nocturnal cough recording. Zero audio work is your most visible gap for this team specifically.
6. **No multimodal or forward-looking prediction.** The project goal is to predict attacks before they happen by combining sources. SARIMA forecasts one series with no outside inputs. Nothing you have built fuses two data types or predicts a future clinical state.
7. **No children, no real-world noise.** n = 1 adult, metronome reference, quiet room. Your README says this plainly, which is a point in your favour. Keep doing that.

What you should not change: the leakage experiment, refusing to claim a CNN win inside its confidence interval, and TCPS 2 done before anyone asked. Those signal research judgment, which is rarer than any library.

## Q4. New skills to showcase, ranked

Ranked by how much the posting weights it times how fast you can show it. The top three are the ones to have on GitHub before an interview.

| Rank | Skill area | What to learn and show | Why the PI cares | Time to show it |
| --- | --- | --- | --- | --- |
| 1 | Time-frequency signal processing | STFT, log-mel spectrograms, MFCCs, resampling, pre-emphasis; librosa, scipy.signal, torchaudio | Title skill; every respiratory sound method starts here | 3 to 4 days |
| 2 | Feature engineering plus classical ML | Spectral centroid, bandwidth, roll-off, zero-crossing rate, band energies, MFCC statistics; feature selection; gradient boosting or random forest; SHAP or permutation importance | Second title skill; gives an interpretable baseline the CNN must beat | 2 to 3 days |
| 3 | Rare-event detection and clinical metrics | Event-level vs segment-level scoring, sensitivity, specificity, PR-AUC, class weighting, threshold tuning, calibration | Exacerbations, wheezes and coughs are all rare positives | 2 days |
| 4 | Pretrained audio models and mobile export | Embeddings from a pretrained audio network (for example PANNs or YAMNet); export to ONNX or TensorFlow Lite | RespiSentinel is a phone app; models must run small | 2 to 3 days |
| 5 | Robustness to real-world noise and devices | Noise mixing at set SNRs, SpecAugment-style masking, per-device evaluation | Home recordings are noisy and every phone mic differs | 2 days |
| 6 | Longitudinal and multimodal prediction | Nightly features rolled up to weekly trends, joined with air quality and weather, time-aware splits | The project's stated goal is predicting attacks before they happen | 3 to 4 days |
| 7 | Audio privacy | Extract features on device, never store raw speech | Pediatric bedroom audio; extends your de-identification work | 1 day |

Wavelets are worth one experiment (the respiratory-sound literature uses them alongside STFT), not a week.

## Q5. Project proposal: CoughCast

**CoughCast is a bedside listener that hears coughs and wheezes during sleep, turns each night into numbers, and turns weeks of nights into a trend a parent could act on.** It closes all seven Q4 gaps in one repo and speaks the team's own language.

### Why this one, for this team

- The [MoKA study](https://www.cheoresearch.ca/studies/mobile-health-in-kids-with-asthma-moka-study/), which runs on RespiSentinel and is coordinated by CHU Sainte-Justine, offers an optional feature that records coughing in the first two hours of sleep. You would be building a toy version of their pipeline.
- A 2020 ERS abstract by [Rassouli and colleagues](https://publications.ersnet.org/content/erj/56/suppl64/4569) found weekly nocturnal cough was associated with asthma control in the same week and the week after. That is the clinical reason to go from nights to weeks.
- A [Leiden study](https://scholarlypublications.universiteitleiden.nl/access/item%3A3421177/view) built a smartphone pediatric cough detector and notes that children's coughs vary more than adults', so robustness matters.

### Ideas borrowed from hackathons and research

| Source | What they built | What CoughCast steals |
| --- | --- | --- |
| [CoughNet](https://devpost.com/software/coughnet) (Devpost) | Browser mic to ML classifier in one hackathon session, with a visible flag when running a mock model | A live demo, and labelling demo mode honestly |
| [Edge Impulse cough tutorial](https://www.edgeimpulse.com/blog/cough-detection-arduino) (UN Covid Detect & Protect Challenge) | Real-time cough detection on an Arduino in under 20 kB of RAM | A hard model-size budget for phone deployment |
| [Achoo](https://achoo2020.carrd.co/) (#BuildForCOVID19) | Voice-assistant cough trigger; one hack was telling coughs from talking | Speech as an explicit negative class |
| [CoughDx](https://devpost.com/software/coughdx) (Devpost) | Passive at-home logging of cough events over time for a clinician | A longitudinal log and a clinician summary |
| [Respiri wheezo](https://www.mathworks.com/company/user_stories/respiri-develops-mobile-app-for-wheeze-detection-and-asthma-management.html) | Spectrogram-based wheeze candidates plus ambient-noise analysis, on-device | "Wheeze rate" as a metric and a noise gate |
| [Nocturnal asthmatic cough field study](https://digitalcommons.dartmouth.edu/facoa/4029) | Separated the patient's cough from a bed partner's | Stretch goal: "whose cough is it" (child vs sibling) |
| [Gamify Asthma](https://gamifyasthma.devpost.com/) (2013 hackathon) | Games for kids aged 5 to 12 with asthma | A kid-friendly morning card |

### The four modules

&#91;embedded content: CoughCast architecture · 3 data sources, 4 modules\]

Both models run inside the on-device boundary; only per-night numbers leave it, joined with air quality into the weekly trend.

1. **Wheeze Lab (signal plus features).** Use the [ICBHI 2017 Respiratory Sound Database](https://bhichallenge.med.auth.gr/ICBHI_2017_Challenge): 920 expert-annotated recordings from 126 subjects, 6,898 breathing cycles (3,642 normal, 1,864 crackles, 886 wheezes, 506 both), with an official subject-wise 60/40 split. Compare three models on one harness, LeaseLens-style: hand-crafted spectral features plus gradient boosting, a CNN on log-mel spectrograms (your GTSRB architecture), and pretrained audio embeddings with a small head. Report sensitivity, specificity and the ICBHI score; a published bagging k-NN method reached 0.670, 0.863 and 0.766, a [fair yardstick](https://kyutech.repo.nii.ac.jp/records/2001645). Add Grad-CAM on spectrograms.
2. **Night Listener (event detection).** Cough positives from [COUGHVID](https://zenodo.org/records/4048312) (30,000+ crowdsourced recordings, 2,000+ labelled by pulmonologists). Hard negatives from [ESC-50](https://github.com/karolpiczak/ESC-50): 2,000 five-second clips in 50 classes, including snoring, breathing, sneezing, laughing and crying baby. Mix events into long background audio at set signal-to-noise ratios with known timestamps to build synthetic two-hour "nights". Score event-level F1 and count error, then reuse your Bland-Altman code on counts. Record two or three of your own nights as a real-world check, same consent rules as BreathCam.
3. **Night-to-Week (pattern analysis and fusion).** Per night: cough count, cough clusters, time of first cough, wheeze rate. Roll up weekly, detect change points, and join Toronto air quality from your AirAware pipeline. State plainly that this is a working pipeline on simulated and self-recorded nights, not a validated predictor.
4. **Phone-Ready and Private.** Export to ONNX or TensorFlow Lite under a size budget. Compute log-mel features on device and drop speech frames so raw bedroom audio is never stored. Reuse your TCPS 2 ethics statement and consent form.

### Fun stretch goals

- A "night sky" visual: each cough a star placed by time and loudness, clusters drawn as constellations.
- Run the cough model on a microcontroller, per the Edge Impulse tutorial.
- Publish the Wheeze Lab baseline as a Kaggle notebook on the ICBHI data.

### What not to claim

No pediatric performance, no exacerbation prediction accuracy, no clinical validity. ESC-50's maintainers warn some clips were preprocessed in class-dependent ways, so note that leakage risk in your report, as you did in BreathCam.

## Build plan and application changes

Apply this weekend with what is real; build CoughCast in parallel and point to it in the interview. The start date is Nov 1, so waiting for the project costs you the job.

### Build plan (Oct 17 to 28)

1. **Today:** change BreathCam's About line to match the README; delete `Bo2b`, the second `B10` and the second `B11` from the bullet bank; confirm whether B01's optical flow is RAFT or Farnebäck.
2. **Oct 17 to 19:** Wheeze Lab data loader on the official split, spectral features, gradient-boosting baseline, first results table.
3. **Oct 20 to 22:** log-mel CNN and pretrained-embedding model, Grad-CAM, ICBHI score comparison.
4. **Oct 23 to 25:** Night Listener synthetic nights, event detection, count error and Bland-Altman.
5. **Oct 26 to 27:** Night-to-Week roll-up with AirAware join; ONNX export.
6. **Oct 28:** README with limitations and a two-page report.

Modules 1 and 2 are the must-haves before an interview; 3 and 4 can land after.

### Resume for this posting

- **Lead with BreathCam**, using only bullets the README backs: `B05` (53 ICU patients; 1.16 vs 1.62 vs 2.31 breaths/min), `B06` (1D CNN 0.98 vs Welch 1.16, gain inside its CI), `B07` (leakage: 0.46 vs 0.98, 2.1x inflation), `B12` (pytest 8 to 38 tests). Use `B03` (3,800 of 4,809 windows kept) only after you confirm the figure in the repo.
- **Then LeaseLens** bullets 3 (bootstrap slice audit, 0.747 vs 0.851 F1) and 6 (SARIMA MAPE 2.55% to 1.11%, 8-fold backtest), framed as evaluation and time-series work.
- **Then GTSRB** bullets 1 (99.17% at 401,387 params) and 3 (Grad-CAM).
- **Co-op:** only ID-tagged bullets with confirmed metrics. The untagged AI bullets in EXP-GovOnt (fine-tuned LLM at 92%, 1.2 million embeddings, 5,000 requests per second, RAGAS 0.94 and others) have no ledger rows; leave them out.
- **Skills line:** SciPy signal processing (filtering, Welch spectrum), PyTorch, TensorFlow/Keras, scikit-learn, pandas, NumPy, wfdb, OpenCV, MediaPipe, SQL/SQLite, pytest, Git. Add librosa or torchaudio only once CoughCast is pushed.

### Cover letter angle

Open with the MoKA nocturnal-cough feature and say you are building a cough and wheeze detector against public respiratory datasets. Use the honest framing from Q2. Mention TCPS 2 is already done. Since 221031 and 221336 are the same project, say you would contribute on either the video or the signal side.

### Interview prep

- Why are your band-pass cutoffs where they are?
- Welch vs a single FFT vs a spectrogram: what does each trade off?
- How would you score a cough detector: per window, per event, or per night?

## Sources

- [BreathCam README](https://github.com/AjayMaan13/BreathCam)
- [CHEO Research Institute: Mobile Health in Kids with Asthma (MoKA) Study](https://www.cheoresearch.ca/studies/mobile-health-in-kids-with-asthma-moka-study/)
- [CHU Sainte-Justine: MoKA study and RespiSentinel](https://research.chusj.org/en/Axes-de-recherche/Recrutement-Projets-de-recherche/Axe-Maladies-infectieuses-et-soins-aigus/Etude-MoKA-utilisation-de-la-sante-mobile-pour-p)
- [Rassouli et al., Smartphone-based cough detection predicts asthma control, ERJ 2020](https://publications.ersnet.org/content/erj/56/suppl64/4569)
- [Smartphone-based pediatric cough detection algorithm (Leiden)](https://scholarlypublications.universiteitleiden.nl/access/item%3A3421177/view)
- [Nocturnal asthmatic cough recognition and sex assignment (field study)](https://digitalcommons.dartmouth.edu/facoa/4029)
- [ICBHI 2017 Respiratory Sound Database](https://bhichallenge.med.auth.gr/ICBHI_2017_Challenge)
- [ICBHI class counts and official split (arXiv 2108.01991)](https://arxiv.org/pdf/2108.01991)
- [CRNN plus bagging k-NN on ICBHI (Kyutech)](https://kyutech.repo.nii.ac.jp/records/2001645)
- [COUGHVID dataset (Zenodo)](https://zenodo.org/records/4048312)
- [ESC-50 dataset](https://github.com/karolpiczak/ESC-50)
- [CoughNet (Devpost)](https://devpost.com/software/coughnet)
- [Edge Impulse: Cough detection with TinyML on Arduino](https://www.edgeimpulse.com/blog/cough-detection-arduino)
- [Achoo (#BuildForCOVID19)](https://achoo2020.carrd.co/)
- [CoughDx (Devpost)](https://devpost.com/software/coughdx)
- [Respiri wheeze detection (MathWorks user story)](https://www.mathworks.com/company/user_stories/respiri-develops-mobile-app-for-wheeze-detection-and-asthma-management.html)
- [Gamify Asthma hackathon (Devpost)](https://gamifyasthma.devpost.com/)
