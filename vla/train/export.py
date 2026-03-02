from __future__ import annotations

from pathlib import Path


def export_onnx(model_pt: str | Path, out_path: str | Path) -> None:
    try:
        import torch
    except Exception as e:
        raise RuntimeError("torch is required for export") from e

    from vla.policy.model import TinyExecutorModel

    model = TinyExecutorModel()
    state = torch.load(model_pt, map_location="cpu")
    model.load_state_dict(state)
    model.eval()

    dummy_img = torch.zeros(1, 3, 256, 256)
    dummy_skill = torch.zeros(1, dtype=torch.long)
    dummy_roi = torch.zeros(1, 4)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.onnx.export(model, (dummy_img, dummy_skill, dummy_roi), str(out_path), input_names=["img", "skill", "roi"], output_names=["action_logits", "xy"])
