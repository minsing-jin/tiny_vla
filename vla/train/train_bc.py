from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from vla.train.dataset import EpisodeDataset


def train_bc(dataset_dir: str | Path, out_dir: str | Path, epochs: int = 1, batch_size: int = 32, lr: float = 1e-3):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    try:
        import torch
        import torch.nn as nn
        import torch.optim as optim
        from torch.utils.data import DataLoader
    except Exception as e:
        raise RuntimeError("torch is required for train") from e

    from vla.policy.model import TinyExecutorModel

    ds = EpisodeDataset(dataset_dir)
    if len(ds) == 0:
        raise RuntimeError("dataset is empty")

    loader = DataLoader(ds, batch_size=batch_size, shuffle=True)
    model = TinyExecutorModel()
    ce = nn.CrossEntropyLoss()
    mse = nn.MSELoss()
    opt = optim.Adam(model.parameters(), lr=lr)

    metrics_path = out / "metrics.jsonl"
    with metrics_path.open("w", encoding="utf-8") as m:
        for ep in range(epochs):
            total = 0
            correct = 0
            click_dist = []
            for img, skill_id, roi, action_id, xy in loader:
                logits, pred_xy = model(img.float(), skill_id.long(), roi.float())
                loss = ce(logits, action_id.long()) + 0.001 * mse(pred_xy, xy.float())
                opt.zero_grad()
                loss.backward()
                opt.step()

                pred = logits.argmax(dim=1)
                total += int(action_id.shape[0])
                correct += int((pred == action_id).sum().item())
                d = torch.norm(pred_xy.detach() - xy.float(), dim=1).mean().item()
                click_dist.append(float(d))

            row = {
                "epoch": ep + 1,
                "action_type_acc": (correct / total) if total else 0.0,
                "click_dist_px": float(np.mean(click_dist) if click_dist else 0.0),
                "heatmap_topk_hit@k": 0.0,
            }
            m.write(json.dumps(row) + "\n")

    torch.save(model.state_dict(), out / "model.pt")
    (out / "config_snapshot.json").write_text(json.dumps({"epochs": epochs, "batch_size": batch_size, "lr": lr}, indent=2), encoding="utf-8")
