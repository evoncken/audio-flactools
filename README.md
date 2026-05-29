# audio-flactools

Some Python scripts I wrote to help me manage hundreds of CDs ripped
into FLAC files. Mostly used dBpoweramp with AccurateRip / Secure
Rip so the scripts make some assumptions about metadata (because
written by dBpoweramp).

* pyAccurateRipReport
  * scan all FLAC files, generate report with AccurateRip / Secure status for each track
* pyFixAlbumArt
  * scan all Folder.jpg files, reduce them to max. 600kB in size for Bluesound streamer

## Known issues

* None

## Future improvements

* Generate JSON reports for automated processing
* Generate more specific output / reports (JSON might make this superfluous, filter JSON)
- 
