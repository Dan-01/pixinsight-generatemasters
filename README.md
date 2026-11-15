# GenerateMasters for PixInsight

GenerateMasters turns astrophotography light frames and calibration frames into calibrated, registered and integrated **linear master images** in PixInsight. Choose your image folders, review the detected inputs, and work through frame and master review before saving the results. Your original images remain unchanged.

## What it does

- **Finds your frames:** scans folders and subfolders, reading FITS headers to identify the target, filters, exposure times and camera settings.
- **Matches calibration:** selects compatible darks, flats and dark-flats. Light darks match the light exposure; flats match the filter; dark-flats match the flat exposure. Camera settings, image dimensions, binning and sensor temperature are checked.
- **Reuses or builds calibration masters:** uses matching existing master darks, or prepares calibration masters from compatible raw frames.
- **Calibrates and reviews lights:** measures frame quality and lets you inspect and accept or exclude frames before integration.
- **Aligns and stacks:** registers accepted lights to a common reference and integrates them into a master for each filter and exposure group.
- **Supports optional 2× drizzle:** produces masters at twice the width and height, with normal masters retained for comparison, when supported by your PixInsight build.
- **Resumes interrupted work:** keeps processing records and verifies completed stages so a resumed run can reuse valid results.

The results include linear masters in XISF format, low and high rejection maps, and processing records. GenerateMasters pauses for final master review before saving the approved results. The masters are ready for subsequent image processing; they are not stretched or finished images.

## Requirements and compatibility

- macOS or Linux.
- PixInsight 1.9.4 or later, with support for the native processes required by the selected workflow.
- Node.js **24**, installed separately. The GenerateMasters update includes its supporting JavaScript libraries.
- Sufficient free space for working images and final masters.

**PixInsight 1.9.6 build 1718:** installation, launch and a small synthetic integration have been verified. Frame measurement, local normalization and drizzle remain blocked by GenerateMasters' existing compatibility checks on this build. A complete automatic masters run requiring those steps is not yet supported on that build.

## Install and update

1. Install Node.js 24.
2. In PixInsight, open **Resources → Updates → Manage Repositories → Add** and enter this address, including the final slash:

   ```text
   https://raw.githubusercontent.com/Dan-01/pixinsight-generatemasters/master/updates/
   ```

3. Choose **Resources → Updates → Check for Updates** and apply GenerateMasters.
4. Exit PixInsight, confirm installation of the downloaded update, and restart.
5. Open **GenerateMasters** from the **Script** menu. If Node.js 24 is not detected, select its executable under **Advanced**.

Future versions arrive through the same **Check for Updates** command. Current releases are unsigned, so PixInsight may ask you to confirm the download.

If GenerateMasters is missing from the menu, use **Script → Feature Scripts** to add `<PixInsight>/src/scripts/GenerateMasters/pixinsight/`. An earlier manually registered copy may produce a duplicate menu entry; use the copy installed by the updater for automatic updates.

## Use GenerateMasters

1. Choose the **Lights folder** for one target.
2. Choose the **Darks / flats folder** containing compatible calibration frames or existing master darks. Subfolders are searched, and calibration frames beside the lights are also found.
3. Optionally choose **Save masters to**. Leaving it blank creates a masters folder outside the input folders.
4. Select **Review inputs** to check the detected groups, matching calibration and storage requirements.
5. Select **Generate / resume masters**, review the measured frames when prompted, and inspect the resulting masters and rejection maps before accepting them.

Mixed light exposures are handled separately. For example, 600-second luminance and 300-second colour frames use their own matching darks. When building calibration masters from raw frames, provide at least three compatible darks per required exposure, plus three flats and three matching dark-flats per filter.

Keep personal configuration, source frames and saved masters outside the installation folder.
