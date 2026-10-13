# Strix Sigma Rules

حزمة من **13 قاعدة Sigma لخوادم الويب** من مجلد `rules/web/webserver_generic` في مستودع SigmaHQ، مثبتة على commit `42478221b1a062411b8185732c82caa439271122`. نُقلت ملفات YAML دون تعديل؛ يسجل [`MANIFEST.json`](MANIFEST.json) مسارات المصدر وروابط commit والمؤلفين وبصمات SHA-256.

## الترخيص والإسناد

قواعد YAML مرخّصة بموجب **Detection Rule License (DRL) 1.1**. أُرفق النص الكامل في [`LICENSE.Detection.Rules.md`](LICENSE.Detection.Rules.md)، مع إشعار SigmaHQ الأصلي في [`NOTICE.SigmaHQ`](NOTICE.SigmaHQ). حُفظت حقول المؤلف الأصلية، ويُظهر Strix الإسناد في التنبيهات المطابقة. ملف [`LICENSE`](LICENSE) يحدد نطاق ترخيص مواد الربط والوثائق، ولا يغيّر ترخيص القواعد.

هذا المستودع **ليس نسخة كاملة من SigmaHQ** ولا يحتوي قواعد Strix الخاصة. لم تُنشر قواعد `rules/sigma-core-generated/` ذات الـ1200 قاعدة؛ الترخيص المحلي يمنع إعادة توزيعها أو نشرها كحزمة مستقلة دون إذن مكتوب. واستُبعدت قواعد الجذر وYARA ذات المنشأ/الترخيص غير المثبتين.

## التوافق مع Strix Core

في بناء Core الحالي، حُمّلت القواعد الـ13 كلها مع `rejected=0`. كما اختبرنا أربع حالات تمثيلية فعليًا من خلال CLI على سجلات Apache مؤقتة: اجتياز المسار، حقن SQL، وكيل مستخدم مشبوه، وأوامر webshell في Windows؛ وظهر إسناد المؤلف في كل تنبيه. يتضمن Core دعم الحقول المستخدمة مثل `cs-uri-query` و`cs-method` و`cs-user-agent` و`sc-status`، وقوائم `keywords`/`selection_keywords`، وقيود `logsource` لخوادم الويب. راجع [تحديث Strix Core](https://github.com/mahmadmamoun8-design/strix/pull/1) إذا كانت نسختك أقدم.

بعد مراجعة اتفاقية Strix وقبولها صراحةً، أعد الاختبار هكذا:

```bash
STRIX_EULA_ACCEPTED=1 STRIX_BIN=/path/to/strix \
  python3 scripts/test_strix_compat.py
```

يتحقق الاختبار من بصمات manifest، ويشغّل المسح في HOME وقاعدة بيانات مؤقتين، ويتوقع تحميل `13/13` دون رفض ومطابقة الحالات الأربع. لا يغيّر إعداد المستخدم ولا يقبل الاتفاقية تلقائيًا.

## الربط المباشر

```bash
git clone https://github.com/mahmadmamoun8-design/strix-rules.git \
  "$HOME/.local/share/strix/strix-rules"
cd "$HOME/.local/share/strix/strix-rules"
./scripts/configure_strix.sh
```

يضبط السكربت `detectors.sigma_rules_path` على `rules/web/webserver_generic/`، وهو المجلد الذي يقرأ منه محمل Strix الحالي ملفات YAML مباشرة. بعد تنزيل تحديثات، نفّذ `git pull --ff-only` ثم أعد تشغيل السكربت. التحديث يدوي؛ لا يوجد سحب دوري أو تنزيل تلقائي بالخلفية.

## English

A pack of **13 web-server Sigma rules** from SigmaHQ's `rules/web/webserver_generic`, pinned to commit `42478221b1a062411b8185732c82caa439271122`. The YAML files are unmodified; [`MANIFEST.json`](MANIFEST.json) records upstream paths, commit URLs, authors, and SHA-256 digests.

The rules are licensed under **Detection Rule License (DRL) 1.1**. The full text is included in [`LICENSE.Detection.Rules.md`](LICENSE.Detection.Rules.md), along with SigmaHQ's original notice in [`NOTICE.SigmaHQ`](NOTICE.SigmaHQ). Original author fields are preserved, and Strix includes author attribution in matching alerts. The root [`LICENSE`](LICENSE) scopes the license for packaging/documentation materials and does not replace the rules' license.

This is **not a full SigmaHQ mirror** and contains no Strix-owned rules. Strix Core's 1,200 `rules/sigma-core-generated/` rules are excluded because their local license prohibits standalone redistribution or publication without written permission. Root-level and YARA rules with unverified provenance were also excluded.

All 13 rules loaded in the current Strix Core build with zero rejected. Four representative detections—path traversal, SQL injection, suspicious user-agent, and Windows webshell command—were exercised through CLI against temporary Apache logs; each emitted author attribution. For older Core builds, see [Strix Core PR #1](https://github.com/mahmadmamoun8-design/strix/pull/1).

After reviewing and accepting the Strix EULA, reproduce the isolated test with `STRIX_EULA_ACCEPTED=1 STRIX_BIN=/path/to/strix python3 scripts/test_strix_compat.py`. It checks the manifest hashes, expects 13/13 loaded and four matching alerts, and isolates HOME/config/database/secrets. It does not accept the EULA automatically.

Clone the repository and run `scripts/configure_strix.sh` to point `detectors.sigma_rules_path` to `rules/web/webserver_generic/`. Updates are manual (`git pull --ff-only`, then rerun the script); no background fetch is performed.
