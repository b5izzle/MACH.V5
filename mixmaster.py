#!/usr/bin/env python3
import argparse
import os
import sys
import numpy as np
import librosa
from pydub import AudioSegment, effects
from pydub.silence import detect_nonsilent
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from tempfile import mktemp
import warnings
warnings.filterwarnings("ignore")

class MixMasterCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='5UPREME Audio Mixing and Mastering Console',
            formatter_class=argparse.RawTextHelpFormatter
        )
        self.setup_arguments()
        self.args = self.parser.parse_args()
        self.target_lufs = -14
        self.max_true_peak = -1.0
        self.eq_presets = {
            'vocal': [(100, 3), (1000, 4), (5000, 5), (10000, 2)],
            'bass': [(60, 6), (120, 4), (800, -3), (3000, 1)],
            'master': [(80, 2), (200, 1), (2000, 3), (10000, 4)]
        }

    def setup_arguments(self):
        self.parser.add_argument('input', help='Input audio file path')
        self.parser.add_argument('output', help='Output audio file path')
        self.parser.add_argument('--normalize', action='store_true')
        self.parser.add_argument('--eq', choices=list(self.eq_presets.keys()))
        self.parser.add_argument('--compress', type=float, default=0)
        self.parser.add_argument('--silence', action='store_true')
        self.parser.add_argument('--analyze', action='store_true')
        self.parser.add_argument('--visual', action='store_true')
        self.parser.add_argument('--bitrate', type=int, default=256, choices=[128, 192, 256, 320])

    def run(self):
        print(f"🔥 5UPREME FLAMECHAIN AUDIO PROCESSOR 🔥")
        print(f"Loading: {self.args.input}")
        try:
            audio = AudioSegment.from_file(self.args.input)
            original = audio

            if self.args.silence:
                audio = self.remove_silence(audio)
            if self.args.eq:
                audio = self.apply_eq(audio, self.args.eq)
            if self.args.compress > 0:
                audio = self.apply_compression(audio, self.args.compress)
            if self.args.normalize:
                audio = self.normalize_audio(audio)

            self.export_audio(audio)

            if self.args.analyze:
                self.analyze_audio(original, audio)
            if self.args.visual:
                self.create_visualization(original, audio)

            print(f"\n✅ Processing complete: {self.args.output}")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            sys.exit(1)

    def remove_silence(self, audio):
        print("🔇 Removing silence...")
        nonsilent_ranges = detect_nonsilent(audio, min_silence_len=500, silence_thresh=-40)
        if not nonsilent_ranges:
            return audio
        processed = AudioSegment.empty()
        for start, end in nonsilent_ranges:
            processed += audio[start:end]
        return processed

    def apply_eq(self, audio, preset_name):
        print(f"🎛 Applying {preset_name.upper()} EQ profile...")
        samples = np.array(audio.get_array_of_samples())
        sr = audio.frame_rate
        for freq, gain in self.eq_presets[preset_name]:
            nyquist = 0.5 * sr
            normal_freq = freq / nyquist
            b, a = butter(2, normal_freq, btype='band')
            samples = lfilter(b, a, samples)
            samples = samples * (10 ** (gain / 20))
        return AudioSegment(
            samples.astype(np.int16).tobytes(),
            frame_rate=sr,
            sample_width=audio.sample_width,
            channels=audio.channels
        )

    def apply_compression(self, audio, ratio):
        print(f"📉 Applying compression (1:{ratio})...")
        return effects.compress_dynamic_range(audio, ratio)

    def normalize_audio(self, audio):
        print("📏 Normalizing to industry standard...")
        tmp_path = mktemp(suffix='.wav')
        audio.export(tmp_path, format="wav")
        y, sr = librosa.load(tmp_path, sr=None)
        lufs = librosa.loudness(y)
        gain_db = self.target_lufs - lufs
        print(f"  Measured LUFS: {lufs:.1f}, Applying gain: {gain_db:.1f}dB")
        return audio.apply_gain(gain_db)

    def export_audio(self, audio):
        format = os.path.splitext(self.args.output)[1][1:]
        print(f"💾 Exporting as {format.upper()} at {self.args.bitrate}kbps...")
        audio.export(self.args.output, format=format, bitrate=f"{self.args.bitrate}k")

    def analyze_audio(self, original, processed):
        print("\n🔬 Audio Analysis Report:")
        print("-" * 40)
        orig_stats = self.get_audio_stats(original)
        print("ORIGINAL:")
        print(f"  Duration: {orig_stats['duration']:.1f}s")
        print(f"  LUFS: {orig_stats['lufs']:.1f}")
        print(f"  Dynamic Range: {orig_stats['dr']:.1f}dB")
        proc_stats = self.get_audio_stats(processed)
        print("\nPROCESSED:")
        print(f"  Duration: {proc_stats['duration']:.1f}s")
        print(f"  LUFS: {proc_stats['lufs']:.1f}")
        print(f"  Dynamic Range: {proc_stats['dr']:.1f}dB")
        print("\nDIFFERENCES:")
        print(f"  Loudness Change: {proc_stats['lufs'] - orig_stats['lufs']:.1f}dB")
        print(f"  DR Change: {proc_stats['dr'] - orig_stats['dr']:.1f}dB")
        print(f"  Duration Change: {proc_stats['duration'] - orig_stats['duration']:.1f}s")
        print("-" * 40)

    def get_audio_stats(self, audio):
        tmp_path = mktemp(suffix='.wav')
        audio.export(tmp_path, format="wav")
        y, sr = librosa.load(tmp_path, sr=None)
        lufs = librosa.loudness(y)
        rms = librosa.feature.rms(y=y)
        dr = 20 * np.log10(np.max(rms) / np.min(rms))
        return {
            'duration': len(y) / sr,
            'lufs': lufs,
            'dr': dr
        }

    def create_visualization(self, original, processed):
        print("📊 Generating waveform visualization...")
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 1, 1)
        samples = np.array(original.get_array_of_samples())
        time = np.arange(len(samples)) / original.frame_rate
        plt.plot(time, samples, color='blue', alpha=0.7)
        plt.title('Original Waveform')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True, alpha=0.3)
        plt.subplot(2, 1, 2)
        samples = np.array(processed.get_array_of_samples())
        time = np.arange(len(samples)) / processed.frame_rate
        plt.plot(time, samples, color='red', alpha=0.7)
        plt.title('Processed Waveform')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        vis_path = os.path.splitext(self.args.output)[0] + '_waveform.png'
        plt.savefig(vis_path, dpi=150)
        print(f"  Visualization saved: {vis_path}")

if __name__ == "__main__":
    cli = MixMasterCLI()
    cli.run()