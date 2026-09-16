# See your Trajectory!

**See your Trajectory!** is a Fabric mod for Minecraft **26.3** that previews projectile trajectories for bows, snowballs, eggs, tridents, ender pearls and other supported projectiles.

This project is based on **ProjectilesTrajectoryPreview / Projectiles Trajectory Prediction** by **maDU59_**. The upstream project is licensed under the MIT License and attribution is preserved here.

## Build

This repository pins the upstream Minecraft 26.3 source, applies the See your Trajectory! rebrand/maintenance patch during CI, and builds a ready Fabric `.jar`.

The 1.1.0 port also isolates the mod's package, networking namespace, key mappings, config file and client command so it can coexist with the original PTP mod without duplicate key/network registrations.

## Compatibility

- Minecraft **26.3**
- Fabric Loader **0.19.4+**
- Java **25+**
- Fabric API
- Mod Menu optional

In singleplayer and LAN worlds the trajectory preview is enabled locally. On normal multiplayer servers, the upstream handshake design requires the corresponding mod to be present server-side before the preview is enabled.

## Credits

- **maDU59_** — original ProjectilesTrajectoryPreview author
- **fixpot47** — See your Trajectory! fork and maintenance

Original project: https://github.com/maDU59/ProjectilesTrajectoryPreview

## Buy us a Cookie! 🍪

If you like the mod and want to support future updates, you can support us here:

[Support us on DonationAlerts](https://www.donationalerts.com/r/fixpot47)

## License

MIT License. See `LICENSE` and `NOTICE.md`.
