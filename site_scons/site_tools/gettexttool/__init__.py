"""NVDA gettext tool for SCons.

This tool allows generation of gettext .mo compiled files,pot files from source code files
and pot files for merging.

Three new builders are added into the constructed environment:

- gettextMoFile: generates .mo file from .pot file using msgfmt.
- gettextPotFile: Generates .pot file from source code files.
- gettextMergePotFile: Creates a .pot file appropriate for merging into existing .po files.

To properly configure get text, define the following variables:

- gettext_package_bugs_address
- gettext_package_name
- gettext_package_version

"""

import os
from pathlib import Path
from SCons.Action import Action


def exists(env):
	return True


XGETTEXT_COMMON_ARGS = (
	"--msgid-bugs-address='$gettext_package_bugs_address' "
	"--package-name='$gettext_package_name' "
	"--package-version='$gettext_package_version' "
	"--keyword=pgettext:1c,2 "
	"-c -o $TARGET $SOURCES"
)


def _msgfmt_action_func(target, source, env):
	"""Custom action to compile .po to .mo only if needed.
	
	Skips compilation if:
	- Target .mo file already exists
	- Source .po file was not modified after the target .mo
	"""
	target_path = str(target[0])
	source_path = str(source[0])
	
	# Check if target exists
	if os.path.exists(target_path):
		target_mtime = os.path.getmtime(target_path)
		source_mtime = os.path.getmtime(source_path)
		# Skip if .mo is newer than .po
		if target_mtime >= source_mtime:
			print(f"Skipping {os.path.basename(target_path)} (already up to date)")
			return None  # No action needed
	
	# Proceed with compilation
	import subprocess
	result = subprocess.run(
		["msgfmt", "-o", target_path, source_path],
		capture_output=True,
		text=True
	)
	if result.returncode != 0:
		print(f"Error compiling {source_path}: {result.stderr}")
		return result.returncode
	return 0


def generate(env):
	env.SetDefault(gettext_package_bugs_address="example@example.com")
	env.SetDefault(gettext_package_name="")
	env.SetDefault(gettext_package_version="")

	# Create custom action that checks before compiling
	msgfmt_action = Action(_msgfmt_action_func, "Compiling translation $SOURCE")

	env["BUILDERS"]["gettextMoFile"] = env.Builder(
		action=msgfmt_action,
		suffix=".mo",
		src_suffix=".po",
	)

	env["BUILDERS"]["gettextPotFile"] = env.Builder(
		action=Action("xgettext " + XGETTEXT_COMMON_ARGS, "Generating pot file $TARGET"),
		suffix=".pot",
	)

	env["BUILDERS"]["gettextMergePotFile"] = env.Builder(
		action=Action(
			"xgettext " + "--omit-header --no-location " + XGETTEXT_COMMON_ARGS,
			"Generating pot file $TARGET",
		),
		suffix=".pot",
	)
