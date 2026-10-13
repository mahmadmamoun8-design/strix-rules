# Strix Sigma Rules

حزمة من **2303 قاعدة Sigma** متوافقة مع محمل Strix: 2297 قاعدة SigmaHQ اجتازت اختبار التحميل الفعلي، و6 قواعد مملوكة لـStrix. القواعد مثبتة على commit SigmaHQ محدد، ويسجل [`MANIFEST.json`](MANIFEST.json) مسار المصدر وروابط commit وبصمات SHA-256 وprovenance لكل قاعدة.

## الترخيص والإسناد

قواعد YAML مرخّصة بموجب **Detection Rule License (DRL) 1.1**. أُرفق النص الكامل في [`LICENSE.Detection.Rules.md`](LICENSE.Detection.Rules.md)، مع إشعار SigmaHQ الأصلي في [`NOTICE.SigmaHQ`](NOTICE.SigmaHQ). حُفظت حقول المؤلف الأصلية، ويُظهر Strix الإسناد في التنبيهات المطابقة. ملف [`LICENSE`](LICENSE) يحدد نطاق ترخيص مواد الربط والوثائق، ولا يغيّر ترخيص القواعد.

هذا المستودع **ليس نسخة كاملة من SigmaHQ**. قواعد SigmaHQ فيه منفصلة عن قواعد Strix-owned، ولم تُنشر قواعد `rules/sigma-core-generated/` ذات الـ1200 قاعدة؛ الترخيص المحلي يمنع إعادة توزيعها أو نشرها كحزمة مستقلة دون إذن مكتوب. واستُبعدت قواعد الجذر وYARA ذات المنشأ/الترخيص غير المثبتين.

## التوافق مع Strix Core

في بناء Core الحالي، حُمّلت القواعد الـ2303 كلها مع `rejected=0`. استُبعدت 857 قاعدة من snapshot نفسه لأنها رفضت schema أو syntax غير المدعوم في محمل Strix الحالي. واختبرنا عشر حالات تمثيلية من خلال CLI على سجلات Apache مؤقتة، وظهر إسناد المؤلف في كل تنبيه. يتضمن Core دعم الحقول المستخدمة مثل `cs-uri-query` و`cs-method` و`cs-user-agent` و`sc-status`، وقوائم `keywords`/`selection_keywords`، وقيود `logsource` لخوادم الويب. راجع [تحديث Strix Core](https://github.com/mahmadmamoun8-design/strix/pull/1) إذا كانت نسختك أقدم.

بعد مراجعة اتفاقية Strix وقبولها صراحةً، أعد الاختبار هكذا:

```bash
STRIX_EULA_ACCEPTED=1 STRIX_BIN=/path/to/strix \
  python3 scripts/test_strix_compat.py
```

يتحقق الاختبار من بصمات manifest، ويشغّل المسح في HOME وقاعدة بيانات مؤقتين، ويتوقع تحميل جميع القواعد المسجلة في manifest دون رفض ومطابقة الحالات العشر. لا يغيّر إعداد المستخدم ولا يقبل الاتفاقية تلقائيًا.

## الربط المباشر

```bash
git clone https://github.com/mahmadmamoun8-design/strix-rules.git \
  "$HOME/.local/share/strix/strix-rules"
cd "$HOME/.local/share/strix/strix-rules"
./scripts/configure_strix.sh
```

يضبط السكربت `detectors.sigma_rules_path` على `rules/web/webserver_generic/`، وهو المجلد الذي يقرأ منه محمل Strix الحالي ملفات YAML مباشرة. بعد تنزيل تحديثات، نفّذ `git pull --ff-only` ثم أعد تشغيل السكربت. التحديث يدوي؛ لا يوجد سحب دوري أو تنزيل تلقائي بالخلفية.

## English

A pack of **2,303 Strix-compatible Sigma rules**: 2,297 SigmaHQ rules that passed the actual loader and 6 Strix-owned rules. The pack is pinned to a specific SigmaHQ commit, and [`MANIFEST.json`](MANIFEST.json) records source paths, commit URLs, provenance, and SHA-256 digests for every rule.

The rules are licensed under **Detection Rule License (DRL) 1.1**. The full text is included in [`LICENSE.Detection.Rules.md`](LICENSE.Detection.Rules.md), along with SigmaHQ's original notice in [`NOTICE.SigmaHQ`](NOTICE.SigmaHQ). Original author fields are preserved, and Strix includes author attribution in matching alerts. The root [`LICENSE`](LICENSE) scopes the license for packaging/documentation materials and does not replace the rules' license.

This is **not a full SigmaHQ mirror**. SigmaHQ rules are separated from the Strix-owned additions. Strix Core's 1,200 `rules/sigma-core-generated/` rules are excluded because their local license prohibits standalone redistribution or publication without written permission. Root-level and YARA rules with unverified provenance were also excluded.

All 2,303 manifest rules load in the current Strix Core build with zero rejected. The 857 SigmaHQ rules rejected by the current loader were not vendored. Ten representative detections covering SigmaHQ and Strix-owned rules were exercised through CLI against temporary Apache logs; each emitted author attribution. For older Core builds, see [Strix Core PR #1](https://github.com/mahmadmamoun8-design/strix/pull/1).

After reviewing and accepting the Strix EULA, reproduce the isolated test with `STRIX_EULA_ACCEPTED=1 STRIX_BIN=/path/to/strix python3 scripts/test_strix_compat.py`. It checks the manifest hashes, expects all manifest rules loaded with zero rejected and ten matching alerts, and isolates HOME/config/database/secrets. It does not accept the EULA automatically.

Clone the repository and run `scripts/configure_strix.sh` to point `detectors.sigma_rules_path` to `rules/web/webserver_generic/`. Updates are manual (`git pull --ff-only`, then rerun the script); no background fetch is performed.
