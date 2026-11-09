# NZ XMLTV for Home Assistant

Custom integration that loads New Zealand TV guide data from [nzxmltv.com](https://nzxmltv.com).

- Providers: Freeview, Sky, ThreeNow, TVNZ+
- Pick the channels you care about; each gets
  - a **calendar** entity with the full schedule (~8 days)
  - a **"now" sensor** with the current programme and next-up details as attributes
- Guide refreshes every 6 hours.

## Install
Copy `custom_components/nzxmltv` into your HA `config/custom_components/` (or add this repo to HACS as a custom repository), restart, then **Settings → Devices & services → Add integration → NZ XMLTV**.
Add the integration once per provider. Use *Configure* on the entry to change channels.

## Notes
- "Fixed channel IDs" is the default so entity IDs survive channel renumbering.
- Sky's full guide is ~5 MB gzipped (~60 MB XML); it's parsed in an executor and filtered to your channels.
- Please be considerate of nzxmltv.com; no usage terms are published on the site.
