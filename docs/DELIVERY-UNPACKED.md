# 交付：平台拒 zip 时的拆包上传

- 平台网页输入不接受 `.zip` 时，上传解包文件 + `DELIVERY_MANIFEST.json`（name/bytes/sha256）。
- 目录结构：`UPLOAD-PACKAGES/<task>/` 平铺文件，附 `README-UPLOAD.md`。
- 验证：文件数、bytes、sha256 与 manifest 一致；提交前跑 preflight。
- 不依赖 ZIP；独立文件卡 + manifest 是主路径。
