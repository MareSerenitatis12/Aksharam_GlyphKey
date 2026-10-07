#!/usr/bin/env bash
set -euo pipefail

BUILD_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$BUILD_DIR/src"
TESTS="$BUILD_DIR/tests"
PACKAGE="$BUILD_DIR/package"
GENERATED="$BUILD_DIR/generated"
LINUX="$BUILD_DIR/linux_ubuntu"
WINDOWS="$BUILD_DIR/windows"
MAC="$BUILD_DIR/mac"

mkdir -p "$GENERATED" "$PACKAGE" "$LINUX" "$WINDOWS" "$MAC"
rm -f "$GENERATED/aksharam_glyphkey.kmn"       "$GENERATED/registry_report.json"       "$GENERATED/keyman_core_probe"       "$GENERATED/kmc_keyboard.log"       "$GENERATED/kmc_package.log"       "$PACKAGE/aksharam_glyphkey.kmx"       "$LINUX/aksharam_glyphkey.kmp"       "$WINDOWS/aksharam_glyphkey.kmp"       "$MAC/aksharam_glyphkey.kmp"

python3 "$SRC/generate_keyboard.py"

kmc build "$GENERATED/aksharam_glyphkey.kmn"     -o "$PACKAGE/aksharam_glyphkey.kmx"     | tee "$GENERATED/kmc_keyboard.log"

kmc build "$PACKAGE/aksharam_glyphkey.kps"     -o "$LINUX/aksharam_glyphkey.kmp"     | tee "$GENERATED/kmc_package.log"

# Windows and macOS use the same compiled .kmx keyboard engine, but their packages
# must not carry Linux-only xbindkeys/Python selection helpers.
python3 "$SRC/generate_desktop_kps.py"     "$PACKAGE/aksharam_glyphkey.kps"     "$PACKAGE/aksharam_glyphkey_desktop.kps"

kmc build "$PACKAGE/aksharam_glyphkey_desktop.kps"     -o "$WINDOWS/aksharam_glyphkey.kmp"     | tee "$GENERATED/kmc_windows_package.log"

cp "$WINDOWS/aksharam_glyphkey.kmp" "$MAC/aksharam_glyphkey.kmp"

cc -std=c11 "$TESTS/keyman_core_probe.c"     -o "$GENERATED/keyman_core_probe"     $(pkg-config --cflags --libs keyman_core)

python3 "$TESTS/validate_keyboard.py"
python3 "$TESTS/full_keyboard_conformance.py"

# Build intermediates are disposable. Keep only reusable source/package assets and
# the finalized platform installers.
rm -rf "$GENERATED"
rm -f "$PACKAGE/aksharam_glyphkey.kmx" \
      "$PACKAGE/aksharam_glyphkey.kps" \
      "$PACKAGE/aksharam_glyphkey_desktop.kps" \
      "$PACKAGE/selection_math_map.json"
find "$BUILD_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true

printf 'Linux/Ubuntu installer: %s\n' "$LINUX/aksharam_glyphkey.kmp"
printf 'Windows installer: %s\n' "$WINDOWS/aksharam_glyphkey.kmp"
printf 'macOS installer: %s\n' "$MAC/aksharam_glyphkey.kmp"
