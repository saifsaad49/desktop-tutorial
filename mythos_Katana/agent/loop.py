import argparse, pathlib, yaml, time
from .memory import Memory
from .tools import mock_fetch
from council.judge import judge_decision

def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument('--config', required=True)
    p.add_argument('--target')
    p.add_argument('--targets')
    p.add_argument('--engagement', required=True)
    p.add_argument('--mode', choices=['passive','active'], default='passive')
    p.add_argument('--max-iterations', type=int)
    return p.parse_args()

def main():
    args=parse_args()
    cfg=yaml.safe_load(open(args.config))
    max_iter=args.max_iterations or cfg['persistence_engine']['max_iterations']
    # determine targets: CLI overrides config
    targets=[]
    if args.target: targets=[args.target]
    elif args.targets: targets=[t.strip() for t in open(args.targets).read().splitlines() if t.strip()]
    else: targets=[cfg['scope']['target']]
    engagement_dir=pathlib.Path("reports")/args.engagement
    mem=Memory(engagement_dir)
    for target in targets:
        mem.add({"target": target, "mode": args.mode})
        for i in range(1, max_iter+1):
            ev=mock_fetch(target, args.mode)
            ev["iteration"]=i
            mem.add(ev)
            dec=judge_decision(ev, mem.all())
            if dec=="CONFIRMED":
                break
    report=mem.save_report()
    print(f"Done. Report: {report}")

if __name__=="__main__":
    main()
