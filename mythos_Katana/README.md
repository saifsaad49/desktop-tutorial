# mythos_Katana — مجلس التفكير المستمر

وكيل مستقل (Persistent Agent) للأمن السيبراني الدفاعي ودراسة سلوك التفكير المستمر.
يعمل فقط داخل Scope محدد مسبقاً (Sandbox / Lab) بإذن كامل.

## الفلسفة
Think → Act → Observe → Council Review → Persist
لا يتوقف عند أول فشل، بل يعيد التخطيط عبر مجلس استشاري.

## المكونات
- **الوكيل الأصلي (agent/loop.py)**: الحلقة المستمرة
- **المجلس (council/)**: 6 عقول (مهاجم، مدافع، محقق، قاضي، باحث، موجه/استراتيجي)
- **الذاكرة (agent/memory.py)**: حفظ كل التجارب
- **التقارير (reports/)**: توثيق تلقائي

> يعمل فقط على أهداف تملكها. احترام Rate Limit و robots.txt إجباري.

## التشغيل
```bash
pip install -r requirements.txt
python agent/loop.py --config config/config.yaml
```
