def judge_decision(evidence, history):
    # منطق مبسط: يحتاج دليل حقيقي ليعتبر CONFIRMED
    # في النسخة الكاملة هنا يتم استدعاء LLM لكل عضو
    if "high_confidence" in str(evidence):
        return "CONFIRMED"
    if len(history) < 3:
        return "NEEDS_MORE_TESTING"
    return "REJECTED"
