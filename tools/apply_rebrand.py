from pathlib import Path
import json
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream")

OLD_PACKAGE = "fr.madu59.ptp"
NEW_PACKAGE = "dev.fixpot47.seeyourtrajectory"
NEW_MOD_ID = "seeyourtrajectory"

# Build properties: use the final Minecraft 26.3 release, not the RC value
# from the upstream port commit.
props_path = root / "gradle.properties"
props = props_path.read_text(encoding="utf-8")
replacements = {
    r"(?m)^minecraft_version=.*$": "minecraft_version=26.3",
    r"(?m)^loader_version=.*$": "loader_version=0.19.5",
    r"(?m)^mod_version=.*$": "mod_version=1.1.0",
    r"(?m)^maven_group=.*$": "maven_group=dev.fixpot47",
    r"(?m)^archives_base_name=.*$": "archives_base_name=see-your-trajectory",
    r"(?m)^fabric_version=.*$": "fabric_version=0.160.5+26.3",
}
for pattern, repl in replacements.items():
    props = re.sub(pattern, repl, props)
props_path.write_text(props, encoding="utf-8")

# Repackage every Java source so this fork can coexist with the original PTP jar.
for java_path in root.glob("src/**/*.java"):
    text = java_path.read_text(encoding="utf-8")
    text = text.replace(OLD_PACKAGE, NEW_PACKAGE)
    java_path.write_text(text, encoding="utf-8")

# Fabric metadata
fabric_path = root / "src/main/resources/fabric.mod.json"
data = json.loads(fabric_path.read_text(encoding="utf-8"))
data["id"] = NEW_MOD_ID
data["name"] = "See your Trajectory!"
data["description"] = "Preview the trajectory of arrows, snowballs, eggs, tridents, ender pearls and other supported projectiles."
data["authors"] = [
    "fixpot47",
    "maDU59_ (original ProjectilesTrajectoryPreview author)"
]
data["contact"] = {
    "homepage": "https://github.com/fixpot47/see-your-trajectory",
    "sources": "https://github.com/fixpot47/see-your-trajectory",
    "issues": "https://github.com/fixpot47/see-your-trajectory/issues"
}
data["license"] = "MIT"
data["icon"] = "assets/ptp/icon.png"
data.setdefault("depends", {})["fabricloader"] = ">=0.19.4"
data["depends"]["minecraft"] = "26.3"
data["depends"]["java"] = ">=25"
data["depends"]["fabric-api"] = "*"

# Point all Java entrypoints at the fork's own package namespace.
for entrypoint_name, entries in data.get("entrypoints", {}).items():
    if isinstance(entries, list):
        data["entrypoints"][entrypoint_name] = [
            entry.replace(OLD_PACKAGE, NEW_PACKAGE) if isinstance(entry, str) else entry
            for entry in entries
        ]

fabric_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Internal mod/config/networking namespace.
ptp_path = root / "src/main/java/fr/madu59/ptp/Ptp.java"
text = ptp_path.read_text(encoding="utf-8")
text = re.sub(
    r'public\s+static\s+final\s+String\s+MOD_ID\s*=\s*"ptp"\s*;',
    'public static final String MOD_ID = "seeyourtrajectory";',
    text,
)
text = text.replace('[PTP] Sending handshake to player...', '[See your Trajectory!] Sending handshake to player...')
text = text.replace('Hello Fabric world!', 'See your Trajectory! initialized.')
ptp_path.write_text(text, encoding="utf-8")

# 26.3 changed the key input API. The upstream 26.3 commit already contains
# that migration; here we additionally isolate our key mapping IDs so PTP and
# See your Trajectory! can be installed together without duplicate-key crashes.
client_path = root / "src/client/java/fr/madu59/ptp/PtpClient.java"
text = client_path.read_text(encoding="utf-8")
text = text.replace('LogManager.getLogger("ptpClient")', 'LogManager.getLogger("SeeYourTrajectoryClient")')
text = text.replace('Identifier.fromNamespaceAndPath("ptp", "ptp")', 'Identifier.fromNamespaceAndPath(Ptp.MOD_ID, Ptp.MOD_ID)')
text = text.replace('"ptp.key.item_drop_trajectory"', '"seeyourtrajectory.key.item_drop_trajectory"')
text = text.replace('"ptp.key.toggle"', '"seeyourtrajectory.key.toggle"')
text = text.replace('[PTP]', '[See your Trajectory!]')
client_path.write_text(text, encoding="utf-8")

# Isolate the client command and rebrand the config title as well.
config_screen_path = root / "src/client/java/fr/madu59/ptp/config/configscreen/PtpConfigScreen.java"
if config_screen_path.exists():
    text = config_screen_path.read_text(encoding="utf-8")
    text = text.replace('Component.literal("Projectile Trajectory Preview Config")', 'Component.literal("See your Trajectory! Config")')
    text = text.replace('literal("ptpConfig")', 'literal("seeTrajectoryConfig")')
    config_screen_path.write_text(text, encoding="utf-8")

# Rebrand visible text. Keep existing ptp.* config translation keys because the
# upstream config UI still references them, but add unique keybind/category keys
# for this fork so it can coexist with the original mod.
lang_dir = root / "src/main/resources/assets/ptp/lang"
if lang_dir.exists():
    for path in lang_dir.glob("*.json"):
        try:
            lang = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        for key, value in list(lang.items()):
            if not isinstance(value, str):
                continue
            new_value = value
            for old in (
                "Projectiles Trajectory Prediction",
                "Projectile Trajectory Prediction",
                "Projectiles Trajectory Preview",
                "Projectile Trajectory Preview",
            ):
                new_value = new_value.replace(old, "See your Trajectory!")
            if value.strip() == "PTP":
                new_value = "See your Trajectory!"
            lang[key] = new_value

        lang["key.category.seeyourtrajectory.seeyourtrajectory"] = "See your Trajectory!"
        lang["seeyourtrajectory.key.item_drop_trajectory"] = lang.get(
            "ptp.key.item_drop_trajectory", "Show item drop trajectory"
        )
        lang["seeyourtrajectory.key.toggle"] = lang.get(
            "ptp.key.toggle", "Toggle trajectories"
        )
        path.write_text(json.dumps(lang, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Preserve attribution inside the built jar.
notice = root / "src/main/resources/NOTICE.md"
notice.write_text(
    "# Notice\n\n"
    "See your Trajectory! is based on ProjectilesTrajectoryPreview / Projectiles Trajectory Prediction by maDU59_.\n\n"
    "Original source: https://github.com/maDU59/ProjectilesTrajectoryPreview\n\n"
    "Minecraft 26.3 port is based on upstream commit d4fc4d7084f192113f96fad95ba16d09c098c700.\n\n"
    "Licensed under the MIT License. Fork maintained by fixpot47.\n",
    encoding="utf-8",
)

print("Applied See your Trajectory! 1.1.0 Minecraft 26.3 patch to", root)
