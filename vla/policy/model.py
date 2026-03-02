from __future__ import annotations


try:
    import torch
    import torch.nn as nn
except Exception:
    torch = None
    nn = None


if nn is not None:
    class TinyExecutorModel(nn.Module):
        def __init__(self, num_skills: int = 16, num_actions: int = 8):
            super().__init__()
            self.backbone = nn.Sequential(
                nn.Conv2d(3, 16, 3, stride=2, padding=1),
                nn.ReLU(),
                nn.Conv2d(16, 32, 3, stride=2, padding=1),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d((1, 1)),
            )
            self.skill_emb = nn.Embedding(num_skills, 8)
            self.head = nn.Sequential(
                nn.Linear(32 + 8 + 4, 64),
                nn.ReLU(),
            )
            self.action_type = nn.Linear(64, num_actions)
            self.xy = nn.Linear(64, 2)

        def forward(self, img, skill_id, roi_bbox):
            feat = self.backbone(img).flatten(1)
            s = self.skill_emb(skill_id)
            h = self.head(torch.cat([feat, s, roi_bbox], dim=1))
            return self.action_type(h), self.xy(h)
else:
    class TinyExecutorModel:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise RuntimeError("torch is required for TinyExecutorModel")
