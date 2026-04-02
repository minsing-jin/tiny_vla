from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vla.policy.model import TinyExecutorModel
from vla.train.dataset import EpisodeDataset


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train until loss plateaus using an existing dataset")
    p.add_argument("--dataset", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--max-epochs", type=int, default=50)
    p.add_argument("--patience", type=int, default=5)
    p.add_argument("--min-samples", type=int, default=10)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        import torch
        import torch.nn as nn
        import torch.optim as optim
        from torch.utils.data import DataLoader
    except Exception as e:
        raise RuntimeError("torch is required") from e

    dataset_root = Path(args.dataset)
    if not (dataset_root / "episodes").exists():
        raise RuntimeError(f"dataset not found or invalid: {dataset_root}")

    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)

    ds = EpisodeDataset(dataset_root)
    if len(ds) < args.min_samples:
        raise RuntimeError(
            f"insufficient dataset samples: {len(ds)} < {args.min_samples}. "
            "Use real recorded episodes (record/build-dataset) before running this loop."
        )

    loader = DataLoader(ds, batch_size=min(32, len(ds)), shuffle=True)
    model = TinyExecutorModel()
    ce = nn.CrossEntropyLoss()
    mse = nn.MSELoss()
    opt = optim.Adam(model.parameters(), lr=1e-3)

    best_loss = float("inf")
    losses: list[float] = []
    no_improve = 0

    for _ in range(args.max_epochs):
        epoch_loss = 0.0
        count = 0
        for img, skill_id, roi, action_id, xy in loader:
            logits, pred_xy = model(img.float(), skill_id.long(), roi.float())
            loss = ce(logits, action_id.long()) + 0.001 * mse(pred_xy, xy.float())
            opt.zero_grad()
            loss.backward()
            opt.step()
            epoch_loss += float(loss.item())
            count += 1

        avg = epoch_loss / max(count, 1)
        losses.append(avg)

        if avg < best_loss - 1e-6:
            best_loss = avg
            no_improve = 0
        else:
            no_improve += 1

        if no_improve >= args.patience:
            break

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    history = {
        "dataset": str(dataset_root),
        "samples": len(ds),
        "losses": losses,
        "first_loss": losses[0],
        "best_loss": best_loss,
        "epochs_ran": len(losses),
        "stopped_early": len(losses) < args.max_epochs,
    }
    (out / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")

    assert history["best_loss"] <= history["first_loss"]
    print("train_until_min_loss_from_dataset: ok", history)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
