import yaml, time, pathlib
from memory import Memory
from council.judge import judge_decision

def load_config(path="config/config.yaml"):
    return yaml.safe_load(open(path))

def main():
    cfg = load_config()
    mem = Memory()
    print(f"[mythos_Katana] الهدف: {cfg['scope']['target']} | النمط: {cfg['persistence_engine']['mode']}")
    for i in range(1, cfg['persistence_engine']['max_iterations']+1):
        print(f"\n--- Iteration {i} ---")
        # 1. Planner: اختبار واحد فقط (مثال دفاعي)
        hypothesis = f"فحص إعدادات الأمان للهدف - جولة {i}"
        # 2. Executor: أدوات آمنة فقط (مثال: فحص headers بدون هجوم)
        evidence = {"hypothesis": hypothesis, "note": "passive check only - no exploit"}
        mem.add(evidence)
        # 3. Council review (مبسط)
        decision = judge_decision(evidence, mem.all())
        print(f"Council decision: {decision}")
        if decision == "CONFIRMED":
            mem.save_report("reports/final_report.md")
            break
        if decision == "NEEDS_MORE_TESTING":
            continue
        time.sleep(cfg['research']['delay_seconds'])
    else:
        mem.save_report("reports/final_report.md")
        print("وصلنا للحد الأقصى، تم حفظ التقرير.")

if __name__ == "__main__":
    main()
