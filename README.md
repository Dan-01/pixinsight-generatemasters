# GenerateMasters for PixInsight

This repository distributes only GenerateMasters and the runtime files it needs. It does not contain ProcessMasters, the DanAstroPhoto launcher, or the development repository/history.

## Install and update

The first release becomes available when its release PR is merged into `master`. Before that, the update URL will not have a feed.

1. Install Node.js **24** for your operating system. The update package includes its JavaScript libraries, but does not install Node itself. PixInsight **1.9.4 or later** is required. This feed targets macOS and Linux; Windows is not supported by this package.
2. In PixInsight, open **Resources → Updates → Manage Repositories → Add**, then enter this directory URL, including its final slash:

   `https://raw.githubusercontent.com/Dan-01/pixinsight-generatemasters/master/updates/`

3. Select **Resources → Updates → Check for Updates**, apply GenerateMasters, exit PixInsight and confirm update installation, then restart.
4. Open **Script → DanAstroPhoto → GenerateMasters**. If Node 24 is not found automatically, select its executable in the setup dialog's advanced settings. On Linux this may require its absolute path.
5. Use the same **Check for Updates** command for future releases.

The updater installs under `<PixInsight>/src/scripts/GenerateMasters/`. If the menu entry is missing, use **Script → Feature Scripts** to add that folder's `pixinsight` subfolder. Remove any previously registered manual GenerateMasters copy to avoid duplicate menu entries. Keep personal configuration and data outside the installation folder.

Releases are currently **unsigned**. PixInsight's script security settings may require an explicit trust decision. Check the repository and package before trusting it. Hash checks establish file integrity; they do not provide a developer signature. Native PixInsight GUI installation and real image processing still need a host smoke test; automated tests verify package integrity and isolated synthetic FITS inventory.

## Release contents and review

`updates/updates.xri` is the native PixInsight index. Its SHA-1 describes the final ZIP bytes; `updates/SHA256SUMS` adds SHA-256 checks for that ZIP and the feed. Each ZIP includes a `release-manifest.json` listing every installed runtime file with its size and SHA-256. ZIP names contain the application version and a unique UTC timestamp. Previous ZIPs remain available for clients with cached manifests.

Release automation opens a PR containing only the ZIP, feed and checksum file. Review its validation check before merging. The public workflow has read-only permissions and never checks out development code or uses publication credentials.

To verify a checked-out release with Python 3.10 or later:

```sh
python3 tools/test-release.py
python3 tools/validate-repository.py updates
```

Signing can be added when the maintainer has a PixInsight developer identity: sign scripts before building the ZIP, and sign the final feed afterward. The validator currently intentionally accepts only the unsigned format; it must be extended and tested before signed releases are introduced. Never commit signing keys.
