import sys
import math

def section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def require(cond, msg):
    if not cond:
        print(f"[FAIL] {msg}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[OK] {msg}")

def main():
    section("1) Import and version")
    try:
        import torch
        import torchaudio
        from torchaudio import transforms as aT
        print(f"torch     : {torch.__version__}")
        print(f"torchaudio: {torchaudio.__version__}")
    except Exception as e:
        print("Import failed:", e, file=sys.stderr)
        sys.exit(1)

    section("2) Generate sine wave and resample")
    try:
        sr_in = 16000
        duration = 1.0
        t = torch.linspace(0, duration, int(sr_in * duration), dtype=torch.float32)
        freq = 440.0  # A4
        waveform = torch.sin(2 * math.pi * freq * t)[None, :]  # (1, T)

        resampler = aT.Resample(orig_freq=sr_in, new_freq=8000)
        waveform_8k = resampler(waveform)

        require(waveform.ndim == 2, "Original waveform shape is (channels, time)")
        require(waveform_8k.shape[1] < waveform.shape[1], "Resampled length is shorter (8k < 16k)")
        print(f"Waveform: {tuple(waveform.shape)}, Resampled: {tuple(waveform_8k.shape)}")
    except Exception as e:
        print("Waveform/resample test failed:", e, file=sys.stderr)
        sys.exit(1)

    section("3) Spectrograms and MFCC")
    try:
        spec = aT.Spectrogram(n_fft=256)(waveform_8k)
        melspec = aT.MelSpectrogram(sample_rate=8000, n_fft=256, n_mels=40)(waveform_8k)
        mfcc = aT.MFCC(sample_rate=8000, n_mfcc=13, melkwargs={"n_mels": 40, "n_fft": 256})(waveform_8k)

        require(spec.dim() == 3, "Spectrogram has 3 dims (channel, freq, time)")
        require(melspec.size(1) == 40, "MelSpectrogram has n_mels=40")
        require(mfcc.size(1) == 13, "MFCC has n_mfcc=13")
        print(f"Spec: {tuple(spec.shape)}, Mel: {tuple(melspec.shape)}, MFCC: {tuple(mfcc.shape)}")
    except Exception as e:
        print("Spectrogram/MFCC test failed:", e, file=sys.stderr)
        sys.exit(1)

    section("4) Tiny Conv1d on MFCC (forward/backward)")
    try:
        class TinyAudioNet(torch.nn.Module):
            def __init__(self, in_ch=13, num_classes=2):
                super().__init__()
                self.net = torch.nn.Sequential(
                    torch.nn.Conv1d(in_ch, 32, kernel_size=3, padding=1),
                    torch.nn.ReLU(),
                    torch.nn.Conv1d(32, 32, kernel_size=3, padding=1),
                    torch.nn.ReLU(),
                    torch.nn.AdaptiveAvgPool1d(1),
                )
                self.fc = torch.nn.Linear(32, num_classes)

            def forward(self, x):
                x = self.net(x)       # (B, 32, 1)
                x = x.squeeze(-1)     # (B, 32)
                return self.fc(x)     # (B, C)

        # Make a small batch by duplicating MFCC
        mfcc_batch = torch.cat([mfcc, mfcc], dim=0)  # (2, 13, T)
        labels = torch.tensor([0, 1])

        model = TinyAudioNet(in_ch=mfcc_batch.size(1), num_classes=2)
        opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        loss_fn = torch.nn.CrossEntropyLoss()

        logits = model(mfcc_batch)
        loss = loss_fn(logits, labels)
        opt.zero_grad()
        loss.backward()
        opt.step()

        require(math.isfinite(loss.item()), "Training loss is finite")
        print(f"TinyAudioNet loss: {loss.item():.4f}")
    except Exception as e:
        print("TinyAudioNet test failed:", e, file=sys.stderr)
        sys.exit(1)

    section("All torchaudio checks passed")
    sys.exit(0)

if __name__ == "__main__":
    main()