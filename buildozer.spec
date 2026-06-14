[app]
title = QR Generator
package.name = qrgenerator
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,json,ico
version = 0.1
requirements = python3,kivy,qrcode,pypng

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_missing_dependencies = True
