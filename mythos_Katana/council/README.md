# Council Members
- attacker.py: يقترح فرضية اختبار واحدة
- defender.py: يفند الفرضية
- auditor.py: يطلب دليل ويتحقق
- judge.py: يحسم القرار
- researcher.py: بحث OSINT مقيد (3/جولة، cache)
- persister_strategist.py: يمنع التوقف ويقترح مسار بديل عند الفشل

كل عضو يجب أن يكون LLM prompt منفصل يعيد JSON: {role, verdict, reasoning, next_step}
