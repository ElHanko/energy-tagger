from __future__ import annotations

import numpy as np
import librosa


def compute_energy_score(path: str) -> int | None:
    """
    Compute a rough energy score from 1 to 10 for an audio file.

    This is intentionally heuristic and not meant to reproduce Rekordbox.
    """
    try:
        # Load only the first 120 seconds for speed and consistency
        y, sr = librosa.load(path, mono=True, duration=120)

        if y.size == 0:
            print(f"[ERROR] {path}: empty audio data")
            return None

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rms = float(np.mean(librosa.feature.rms(y=y)))
        spectral_centroid = float(
            np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        )
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onset_rate = float(np.mean(onset_env))
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y=y)))

        # Rough normalization to 0..1
        tempo_n = min(float(tempo) / 150.0, 1.0)
        rms_n = min(rms * 10.0, 1.0)
        centroid_n = min(spectral_centroid / 5000.0, 1.0)
        onset_n = min(onset_rate / 5.0, 1.0)
        zcr_n = min(zcr * 10.0, 1.0)

        score = (
            tempo_n * 0.25
            + rms_n * 0.25
            + onset_n * 0.20
            + centroid_n * 0.20
            + zcr_n * 0.10
        )

        energy = int(np.clip(round(score * 10), 1, 10))
        return energy

    except Exception as exc:
        print(f"[ERROR] {path}: {exc}")
        return None
