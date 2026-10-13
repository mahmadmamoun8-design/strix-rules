# Strix Sigma Rules

حزمة من **19 قاعدة Sigma لخوادم الويب**: 13 قاعدة من SigmaHQ مثبتة على commit `42478221b1a062411b8185732c82caa439271122`، و6 قواعد مملوكة لـStrix تغطي فجوات عملية إضافية. نُقلت قواعد SigmaHQ دون تعديل؛ يسجل [`MANIFEST.json`](MANIFEST.json) المصدر والبصمات SHA-256 وprovenance لكل قاعدة.

## الترخيص والإسناد

قواعد YAML مرخّصة بموجب **Detection Rule License (DRL) 1.1**. أُرفق النص الكامل في [`LICENSE.Detection.Rules.md`](LICENSE.Detection.Rules.md)، مع إشعار SigmaHQ الأصلي في [`NOTICE.SigmaHQ`](NOTICE.SigmaHQ). حُفظت حقول المؤلف الأصلية، ويُظهر Strix الإسناد في التنبيهات المطابقة. ملف [`LICENSE`](LICENSE) يحدد نطاق ترخيص مواد الربط والوثائق، ولا يغيّر ترخيص القواعد.

هذا المستودع **ليس نسخة كاملة من SigmaHQ**. قواعد SigmaHQ فيه منفصلة عن قواعد Strix-owned، ولم تُنشر قواعد `rules/sigma-core-generated/` ذات الـ1200 قاعدة؛ الترخيص المحلي يمنع إعادة توزيعها أو نشرها كحزمة مستقلة دون إذن مكتوب. واستُبعدت قواعد الجذر وYARA ذات المنشأ/الترخيص غير المثبتين.

## التوافق مع Strix Core

في بناء Core الحالي، حُمّلت القواعد الـ19 كلها مع `rejected=0`. واختبرنا عشر حالات تمثيلية فعليًا من خلال CLI على سجلات Apache مؤقتة، تشمل القواعد الـ13 الأصلية والقواعد الجديدة الست؛ وظهر إسناد المؤلف في كل تنبيه. تتضمن القواعد الجديدة كشف الملفات الحساسة، traversal المرمّز، حقن الأوامر، رفع webshell، نقاط debug المكشوفة، وSSRF إلى metadata. يتضمن Core دعم الحقول المستخدمة مثل `cs-uri-query` و`cs-method` و`cs-user-agent` و`sc-status`، وقوائم `keywords`/`selection_keywords`، وقيود `logsource` لخوادم الويب. راجع [تحديث Strix Core](https://github.com/mahmadmamoun8-design/strix/pull/1) إذا كانت نسختك أقدم.

بعد مراجعة اتفاقية Strix وقبولها صراحةً، أعد الاختبار هكذا:

```bash
STRIX_EULA_ACCEPTED=1 STRIX_BIN=/path/to/strix \
  python3 scripts/test_strix_compat.py
```

يتحقق الاختبار من بصمات manifest، ويشغّل المسح في HOME وقاعدة بيانات مؤقتين، ويتوقع تحميل جميع القواعد المسجلة في manifest دون رفض ومطابقة الحالات الأربع. لا يغيّر إعداد المستخدم ولا يقبل الاتفاقية تلقائيًا.

## الربط المباشر

```bash
git clone https://github.com/mahmadmamoun8-design/strix-rules.git \
  "$HOME/.local/share/strix/strix-rules"
cd "$HOME/.local/share/strix/strix-rules"
./scripts/configure_strix.sh
```

يضبط السكربت `detectors.sigma_rules_path` على `rules/web/webserver_generic/`، وهو المجلد الذي يقرأ منه محمل Strix الحالي ملفات YAML مباشرة. بعد تنزيل تحديثات، نفّذ `git pull --ff-only` ثم أعد تشغيل السكربت. التحديث يدوي؛ لا يوجد سحب دوري أو تنزيل تلقائي بالخلفية.

## English

A pack of **19 web-server Sigma rules**: 13 unmodified SigmaHQ rules pinned to commit `42478221b1a062411b8185732c82caa439271122`, plus 6 Strix-owned rules covering additional operational gaps. [`MANIFEST.json`](MANIFEST.json) records provenance and SHA-256 digests for every rule.

The rules are licensed under **Detection Rule License (DRL) 1.1**. The full text is included in [`LICENSE.Detection.Rules.md`](LICENSE.Detection.Rules.md), along with SigmaHQ's original notice in [`NOTICE.SigmaHQ`](NOTICE.SigmaHQ). Original author fields are preserved, and Strix includes author attribution in matching alerts. The root [`LICENSE`](LICENSE) scopes the license for packaging/documentation materials and does not replace the rules' license.

This is **not a full SigmaHQ mirror**. SigmaHQ rules are separated from the Strix-owned additions. Strix Core's 1,200 `rules/sigma-core-generated/` rules are excluded because their local license prohibits standalone redistribution or publication without written permission. Root-level and YARA rules with unverified provenance were also excluded.

All 19 rules load in the current Strix Core build with zero rejected. Ten representative detections covering the 13 SigmaHQ rules and the 6 Strix-owned additions were exercised through CLI against temporary Apache logs; each emitted author attribution. For older Core builds, see [Strix Core PR #1](https://github.com/mahmadmamoun8-design/strix/pull/1).

After reviewing and accepting the Strix EULA, reproduce the isolated test with `STRIX_EULA_ACCEPTED=1 STRIX_BIN=/path/to/strix python3 scripts/test_strix_compat.py`. It checks the manifest hashes, expects 13/13 loaded and four matching alerts, and isolates HOME/config/database/secrets. It does not accept the EULA automatically.

Clone the repository and run `scripts/configure_strix.sh` to point `detectors.sigma_rules_path` to `rules/web/webserver_generic/`. Updates are manual (`git pull --ff-only`, then rerun the script); no background fetch is performed.
