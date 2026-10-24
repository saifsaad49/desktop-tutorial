import argparse, pathlib, sys, yaml
from .memory import Memory
from .tools_registry import run_tool, list_tools
from .validator import validate_target
from council.judge import judge_decision

def parse_args():
    p = argparse.ArgumentParser(description="mythos_Katana - Council that never sleeps")
    p.add_argument('--config', required=True, help='path to config.yaml')
    p.add_argument('--target', help='single target you own')
    p.add_argument('--targets', help='file with targets you own')
    p.add_argument('--engagement', required=True, help='engagement ID, e.g. eng-001')
    p.add_argument('--mode', choices=['passive', 'active'], default='passive')
    p.add_argument('--max-iterations', type=int, default=None)
    p.add_argument('--timeout', type=int, default=30, help='per-tool timeout seconds (must be > 0)')
    p.add_argument('--i-own-target', action='store_true')
    p.add_argument('--agree-risk', action='store_true')
    p.add_argument('--yes', action='store_true')
    return p.parse_args()

def require_consent(args, mode):
    if mode == 'passive':
        return True
    if args.i_own_target and args.agree_risk:
        return True
    if args.yes and args.i_own_target:
        return True
    print("\n[!] ACTIVE mode requires consent:")
    print("    You must own the target or have written permission.")
    print("    Re-run with: --i-own-target --agree-risk")
    try:
        ans = input("Type 'I OWN THIS TARGET' to continue (or Ctrl+C to abort): ").strip()
        return ans == "I OWN THIS TARGET"
    except (EOFError, KeyboardInterrupt):
        return False

def load_config(path):
    try:
        with open(path) as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: config file not found: {path}", file=sys.stderr)
        raise SystemExit(1)
    except yaml.YAMLError as e:
        print(f"Error: invalid YAML in {path}: {e}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(cfg, dict):
        print(f"Error: config {path} must be a mapping", file=sys.stderr)
        raise SystemExit(1)
    return cfg

def main():
    args = parse_args()
    if args.timeout is not None and args.timeout <= 0:
        print(f"Error: --timeout must be > 0 (got {args.timeout})", file=sys.stderr)
        raise SystemExit(2)
    cfg = load_config(args.config)
    max_iter = args.max_iterations
    if max_iter is None:
        max_iter = (cfg.get('persistence_engine') or {}).get('max_iterations', 20)
    if not isinstance(max_iter, int) or max_iter < 1:
        print(f"Error: --max-iterations must be >= 1 (got {args.max_iterations})", file=sys.stderr)
        raise SystemExit(2)
    # resolve raw targets
    if args.target is not None:
        raw_targets = [args.target]
    elif args.targets:
        try:
            with open(args.targets) as f:
                raw_targets = [t.strip() for t in f.read().splitlines() if t.strip()]
        except FileNotFoundError:
            print(f"Error: targets file not found: {args.targets}", file=sys.stderr)
            raise SystemExit(1)
    else:
        scope = cfg.get('scope') or {}
        if not scope.get('target'):
            print("Error: no target given - use --target/--targets or set scope.target in config", file=sys.stderr)
            raise SystemExit(2)
        raw_targets = [scope.get('target')]
    allowed_hosts = (cfg.get('scope') or {}).get('allowed_hosts')
    # validate each target
    targets = []
    for t in raw_targets:
        try:
            targets.append(validate_target(t, allowed_hosts))
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            raise SystemExit(2)
    if not require_consent(args, args.mode):
        print("Aborted. No scan performed.")
        raise SystemExit(2)
    engagement_dir = pathlib.Path("reports") / args.engagement
    try:
        mem = Memory(engagement_dir)
    except OSError as e:
        print(f"Error: cannot write reports dir {engagement_dir}: {e}", file=sys.stderr)
        raise SystemExit(1)
    for target in targets:
        mem.add({"target": target, "mode": args.mode, "consent": True})
        for i in range(1, max_iter + 1):
            tool_name = list_tools()[(i - 1) % len(list_tools())]
            ev = run_tool(tool_name, target, allowed_hosts=allowed_hosts)
            ev["iteration"] = i
            try:
                mem.add(ev)
            except OSError as e:
                print(f"Error: cannot record evidence: {e}", file=sys.stderr)
                raise SystemExit(1)
            dec = judge_decision(ev, mem.all())
            if dec == "CONFIRMED":
                break
    try:
        report = mem.save_report()
    except OSError as e:
        print(f"Error: cannot write report: {e}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Done. Report: {report} | Mode: {args.mode} | Engagement: {args.engagement}")

if __name__ == "__main__":
    main()
