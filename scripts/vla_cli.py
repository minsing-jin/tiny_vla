from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def _default_run_name(prefix: str) -> str:
    return f"runs/{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def cmd_record(args):
    from vla.backend.local_macos import LocalMacOSBackend
    from vla.record.recorder import record_run

    out = args.out or _default_run_name("record")
    backend = LocalMacOSBackend()
    path = record_run(backend=backend, out_dir=out, duration=args.duration, fps=args.fps, capture_inputs=not args.no_inputs)
    print(path)


def cmd_tag(args):
    from vla.record.tagging import interactive_tagging

    interactive_tagging(args.run)


def cmd_replay(args):
    from vla.backend.local_macos import LocalMacOSBackend
    from vla.replay.replayer import replay_actions
    from vla.replay.viewer import view_run

    run_dir = args.run
    if args.pack:
        run_dir = args.pack
    if args.view:
        view_run(run_dir, wait_ms=args.wait_ms)
    else:
        backend = LocalMacOSBackend() if args.inject else None
        replay_actions(run_dir, backend=backend, speed=args.speed)


def cmd_build_dataset(args):
    import glob
    from vla.record.segment import build_dataset_from_runs

    runs = [Path(x) for x in sorted(glob.glob(args.runs_glob))]
    out = Path(args.out)
    ds = build_dataset_from_runs(
        runs=runs,
        out_dir=out,
        align_tolerance_sec=args.align_tolerance,
        drop_unaligned=not args.keep_unaligned,
        include_move_events=not args.drop_move,
    )
    print(ds)


def cmd_train(args):
    from vla.train.train_bc import train_bc

    train_bc(args.dataset, args.out, epochs=args.epochs, batch_size=args.batch_size, lr=args.lr)
    print(args.out)


def cmd_rollout(args):
    from vla.backend.local_macos import LocalMacOSBackend
    from vla.eval.rollout import run_rollout
    from vla.policy.baseline import BaselinePolicy

    backend = LocalMacOSBackend()
    policy = BaselinePolicy()
    out = args.out or _default_run_name("rollout")
    summary = run_rollout(backend, policy, args.command_source, out)
    print(json.dumps(summary, indent=2))


def cmd_dagger_collect(args):
    from vla.dagger.collector import collect_corrections

    out = collect_corrections(args.pack, args.out)
    print(out)


def cmd_dagger_merge(args):
    from vla.dagger.merge import merge_corrections

    out = merge_corrections(args.dataset, args.corrections, args.out)
    print(out)


def cmd_export(args):
    from vla.train.export import export_onnx

    export_onnx(args.model, args.out)
    print(args.out)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vla", description="Executor-VLA framework CLI")
    sp = p.add_subparsers(dest="command", required=True)

    p_record = sp.add_parser("record", help="record demo")
    p_record.add_argument("--out", type=str, default=None)
    p_record.add_argument("--duration", type=float, default=60.0)
    p_record.add_argument("--fps", type=int, default=10)
    p_record.add_argument("--no-inputs", action="store_true")
    p_record.set_defaults(func=cmd_record)

    p_tag = sp.add_parser("tag", help="interactive tagger")
    p_tag.add_argument("--run", type=str, required=True)
    p_tag.set_defaults(func=cmd_tag)

    p_replay = sp.add_parser("replay", help="replay run or failure pack")
    p_replay.add_argument("--run", type=str, default=None)
    p_replay.add_argument("--pack", type=str, default=None)
    p_replay.add_argument("--inject", action="store_true")
    p_replay.add_argument("--speed", type=float, default=1.0)
    p_replay.add_argument("--view", action="store_true")
    p_replay.add_argument("--wait-ms", type=int, default=30)
    p_replay.set_defaults(func=cmd_replay)

    p_build = sp.add_parser("build-dataset", help="build dataset from runs")
    p_build.add_argument("--runs_glob", type=str, required=True)
    p_build.add_argument("--out", type=str, required=True)
    p_build.add_argument("--align-tolerance", type=float, default=0.1)
    p_build.add_argument("--keep-unaligned", action="store_true")
    p_build.add_argument("--drop-move", action="store_true")
    p_build.set_defaults(func=cmd_build_dataset)

    p_train = sp.add_parser("train", help="train behavior cloning")
    p_train.add_argument("--dataset", type=str, required=True)
    p_train.add_argument("--out", type=str, required=True)
    p_train.add_argument("--epochs", type=int, default=1)
    p_train.add_argument("--batch-size", type=int, default=32)
    p_train.add_argument("--lr", type=float, default=1e-3)
    p_train.set_defaults(func=cmd_train)

    p_roll = sp.add_parser("rollout", help="rollout commands")
    p_roll.add_argument("--command_source", type=str, required=True)
    p_roll.add_argument("--out", type=str, default=None)
    p_roll.set_defaults(func=cmd_rollout)

    p_dagger = sp.add_parser("dagger", help="dagger commands")
    sp_d = p_dagger.add_subparsers(dest="dagger_cmd", required=True)

    p_dc = sp_d.add_parser("collect", help="collect corrections from failure pack")
    p_dc.add_argument("--pack", type=str, required=True)
    p_dc.add_argument("--out", type=str, required=True)
    p_dc.set_defaults(func=cmd_dagger_collect)

    p_dm = sp_d.add_parser("merge", help="merge corrections into dataset")
    p_dm.add_argument("--dataset", type=str, required=True)
    p_dm.add_argument("--corrections", type=str, required=True)
    p_dm.add_argument("--out", type=str, required=True)
    p_dm.set_defaults(func=cmd_dagger_merge)

    p_export = sp.add_parser("export", help="export ONNX")
    p_export.add_argument("--model", type=str, required=True)
    p_export.add_argument("--out", type=str, required=True)
    p_export.set_defaults(func=cmd_export)

    p_cmd = sp.add_parser("commands-peek", help="debug command source")
    p_cmd.add_argument("--command_source", type=str, required=True)
    p_cmd.set_defaults(func=lambda a: [print(c.to_dict()) for c in __import__("vla.command.source", fromlist=["iter_commands"]).iter_commands(a.command_source)])

    return p


def main():
    parser = _build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
