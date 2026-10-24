import argparse, pathlib, yaml
from .memory import Memory
from .tools import mock_fetch
from council.judge import judge_decision

def parse_args():
    p=argparse.ArgumentParser(description="mythos_Katana - Council that never sleeps")
    p.add_argument('--config', required=True, help='path to config.yaml')
    p.add_argument('--target', help='single target you own')
    p.add_argument('--targets', help='file with targets you own')
    p.add_argument('--engagement', required=True, help='engagement ID, e.g. eng-001')
    p.add_argument('--mode', choices=['passive','active'], default='passive')
    p.add_argument('--max-iterations', type=int)
    p.add_argument('--i-own-target', action='store_true', help='Confirm you own/have written permission for target(s)')
    p.add_argument('--agree-risk', action='store_true', help='Acknowledge use at your own risk')
    p.add_argument('--yes', action='store_true', help='Non-interactive consent (same as above flags)')
    return p.parse_args()

def require_consent(args, mode):
    if mode=='passive':
        return True
    # active mode requires explicit consent
    if args.i_own_target and args.agree_risk:
        return True
    if args.yes and args.i_own_target:
        return True
    print("\n[!] ACTIVE mode requires consent:")
    print("    You must own the target or have written permission.")
    print("    Re-run with: --i-own-target --agree-risk")
    print("    Use at your own risk - you are liable for misuse.\n")
    # interactive prompt if TTY
    try:
        ans=input("Type 'I OWN THIS TARGET' to continue (or Ctrl+C to abort): ").strip()
        return ans=="I OWN THIS TARGET"
    except (EOFError, KeyboardInterrupt):
        return False

def main():
    args=parse_args()
    cfg=yaml.safe_load(open(args.config))
    max_iter=args.max_iterations or cfg['persistence_engine']['max_iterations']
    targets=[]
    if args.target: targets=[args.target]
    elif args.targets: targets=[t.strip() for t in open(args.targets).read().splitlines() if t.strip()]
    else: targets=[cfg['scope']['target']]
    if not require_consent(args, args.mode):
        print("Aborted. No scan performed.")
        raise SystemExit(2)
    engagement_dir=pathlib.Path("reports")/args.engagement
    mem=Memory(engagement_dir)
    for target in targets:
        mem.add({"target": target, "mode": args.mode, "consent": True})
        for i in range(1, max_iter+1):
            ev=mock_fetch(target, args.mode)
            ev["iteration"]=i
            mem.add(ev)
            dec=judge_decision(ev, mem.all())
            if dec=="CONFIRMED":
                break
    report=mem.save_report()
    print(f"Done. Report: {report} | Mode: {args.mode} | Engagement: {args.engagement}")

if __name__=="__main__":
    main()
