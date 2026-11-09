# NZ XMLTV for Home Assistant

![Pre-release](https://img.shields.io/badge/status-pre--release-orange)

What's on tonight? NZ XMLTV brings New Zealand TV guide data from [nzxmltv.com](https://nzxmltv.com) into Home Assistant, so what's on Freeview, Sky, ThreeNow and TVNZ+ is available to your dashboards, automations and voice assistants. Pick the channels you care about and each one gets a calendar and a "now playing" sensor.

## What you get

- **A calendar per channel**, with the full schedule (usually about 8 days ahead), so it works with the Calendar card and the calendar panel.
- **A "now" sensor per channel.** The state is the programme on air; its attributes carry the description, category, episode, start and end times, and what's on next.
- **Four providers:** Freeview, Sky, ThreeNow and TVNZ+. Add the integration once per provider.
- **Stable entities.** The default "Fixed channel IDs" guide keeps your entity IDs the same when channel numbers change.
- **Light on your network.** The guide refreshes every 6 hours, and only the channels you pick are kept.

## Installation

Needs a recent Home Assistant. NZ XMLTV is a **pre-release** and isn't in the HACS default repository, so it's added as a custom repository.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Greminn&repository=ha-nzxmltv&category=integration)

1. Click the button above, or in HACS choose **⋮ → Custom repositories**, paste `https://github.com/Greminn/ha-nzxmltv` and set **Type** to **Integration**.
2. Install **NZ XMLTV**.
3. Restart Home Assistant, then **Settings → Devices & Services → Add Integration → NZ XMLTV**.

Prefer to copy files by hand? Put `custom_components/nzxmltv/` into your `/config/custom_components/`.

## Quick start

1. Add the integration and choose a **provider** (for example Freeview).
2. Leave the guide type on **Fixed channel IDs (recommended)**. The other options are *Standard* and *Lite* (no images).
3. Choose your **channels** from the list.
4. Repeat for any other provider. To change channels later, open the integration and select **Configure**.

## Using it in automations and dashboards

Each channel's sensor is named after the channel, for example `sensor.tvnz_1_now`. Its attributes include `next_title`, `next_start` and `next_end`:

```yaml
triggers:
  - trigger: state
    entity_id: sensor.three_now
    to: "The Block NZ"
actions:
  - action: notify.notify
    data:
      message: "The Block is on Three. Next up: {{ state_attr('sensor.three_now', 'next_title') }}"
```

The calendar entities work with the usual calendar triggers, so you can also start an automation a few minutes before a programme begins.

## Channels

These are the channels in each provider's *Fixed channel IDs* guide when this README was written (145 in all, from the feeds on 10 November 2026). Providers add and remove channels over time, so what you see when you set it up is the source of truth. The same channel can appear under several providers.

<details>
<summary><strong>Freeview</strong> (35 channels)</summary>

| Channel | ID |
| --- | --- |
| Al Jazeera | `aljazeera` |
| Bravo | `bravo` |
| Bravo Plus 1 | `bravoplus1` |
| C33 | `ch33` |
| CH200 | `ch200` |
| eden | `eden` |
| Firstlight | `firstlight` |
| GeorgeFM | `georgefm` |
| HGTV | `hgtv` |
| Hope Channel | `hopechannel` |
| Juice TV | `juicetv` |
| Life FM | `lifefm` |
| Parliament TV | `parliamenttv` |
| Radio Aotearoa | `radioaotearoa` |
| RadioNZ Concert | `rnzconcert` |
| RadioNZ National | `rnznational` |
| Rhema | `rhema` |
| Rush | `rush` |
| Sanctuary | `sanctuary` |
| Shine TV | `shinetv` |
| SKYOPEN | `skyopen` |
| Stream Test | `freeviewstreamtest` |
| Te Reo | `tereo` |
| Three | `three` |
| ThreePlus1 | `threeplus1` |
| Trackside 1 | `trackside1` |
| Trackside 2 | `trackside2` |
| TVNZ 1 | `tvnz1` |
| TVNZ 1 +1 | `tvnz1plus1` |
| TVNZ 2 | `tvnz2` |
| TVNZ 2 +1 | `tvnz2plus1` |
| TVNZ DUKE | `tvnzduke` |
| TVNZ DUKE +1 | `tvnzdukeplus1` |
| Wairarapa TV | `wairarapatv` |
| Whakaata Māori | `maoritv` |

</details>

<details>
<summary><strong>Sky</strong> (85 channels)</summary>

| Channel | ID |
| --- | --- |
| Ad Tracks | `sdmadtracks` |
| Al Jazeera | `aljazeera` |
| Animal Planet | `animalplanet` |
| Auxiliary | `skyaux1` |
| BBC Earth | `bbcearth` |
| BBC First | `bbcfirst` |
| BBC UKTV | `bbcuktv` |
| BBC World News | `bbcworldnews` |
| Blues | `sdmblues` |
| Bravo | `bravo` |
| Bravo +1 | `bravoplus1` |
| CBeebies | `cbeebies` |
| CGTN Documentary | `cgtndocumentary` |
| CGTN: China Global Television Network | `cgtn` |
| CH 999 | `ch999` |
| Ch83 | `facetv` |
| CNBC | `cnbc` |
| CNN | `cnn` |
| Colors | `colors` |
| Country TV | `countrytv` |
| DAYSTAR | `daystar` |
| Discovery | `discovery` |
| Discovery Turbo | `discoveryturbo` |
| eden | `eden` |
| ESPN | `espn` |
| ESPN2 | `espn2` |
| Firstlight | `firstlight` |
| Fox News | `foxnews` |
| HGTV | `hgtv` |
| Hope Channel | `hopechannel` |
| ID | `id` |
| J2 | `j2` |
| JONES! | `jones` |
| Juice TV | `juicetv` |
| Living | `living` |
| News24 | `skynews` |
| Parliament | `parliamenttv` |
| Real Crime | `realcrime` |
| Real History | `realhistory` |
| Rialto | `rialto` |
| RNZ Concert | `rnzconcert` |
| RNZ National | `rnznational` |
| Rush | `rush` |
| SHINE | `shinetv` |
| Sky Arena | `skyarena` |
| Sky Arts | `skyarts` |
| Sky Comedy | `skycomedy` |
| Sky Drama | `skydrama` |
| Sky Factual | `skyfactual` |
| Sky Justice | `sky5` |
| Sky Kids | `skykids` |
| Sky Movies Action | `skymoviesaction` |
| Sky Movies Classics | `skymoviesclassics` |
| Sky Movies Comedy | `skymoviescomedy` |
| Sky Movies Family | `skymoviesfamily` |
| Sky Movies Greats | `skymoviesgreats` |
| Sky Movies Premiere | `skymoviespremiere` |
| Sky Open | `skyopen` |
| Sky Sport 1 | `skysport1` |
| Sky Sport 2 | `skysport2` |
| Sky Sport 3 | `skysport3` |
| Sky Sport 4 | `skysport4` |
| Sky Sport 5 | `skysport5` |
| Sky Sport 6 | `skysport6` |
| Sky Sport 7 | `skysport7` |
| Sky Sport 9 | `skysport9` |
| Sky Sport Premier League | `skysport8` |
| Sky Sport Select | `skysportselect` |
| Sky Suspect | `vibe` |
| Star Gold | `stargold` |
| Star Plus Hindi | `starhindi` |
| Tahu FM | `tahufm` |
| Three | `three` |
| Three +1 | `threeplus1` |
| TLC | `tlc` |
| Trackside 1 | `trackside1` |
| Trackside 2 | `trackside2` |
| TVNZ 1 | `tvnz1` |
| TVNZ 1 +1 | `tvnz1plus1` |
| TVNZ 2 | `tvnz2` |
| TVNZ 2 +1 | `tvnz2plus1` |
| TVNZ DUKE | `tvnzduke` |
| TVNZ DUKE +1 | `tvnzdukeplus1` |
| Universal | `universal` |
| Whakaata Māori | `maoritv` |

</details>

<details>
<summary><strong>ThreeNow</strong> (15 channels)</summary>

| Channel | ID |
| --- | --- |
| Below Deck Vault | `threenowfast3` |
| Bravo | `bravo` |
| CNN Headlines International | `threenowptcn` |
| eden | `eden` |
| HGTV | `hgtv` |
| MovieSphere | `threenowptms` |
| MythBusters | `threenowptmb` |
| Rush | `rush` |
| Sky Open | `skyopen` |
| Three | `three` |
| Warner Bros TV Deadliest Catch | `threenowfast2` |
| Warner Bros TV House Hunters | `threenowfast6` |
| Warner Bros TV Motorheads | `threenowfast1` |
| Warner Bros TV Paranormal | `threenowfast5` |
| Warner Bros TV True Crime | `threenowfast4` |

</details>

<details>
<summary><strong>TVNZ+</strong> (10 channels)</summary>

| Channel | ID |
| --- | --- |
| BIG BROTHER AUSTRALIA LIVE STREAM | `tvnzbigbrotherau` |
| Bloomberg Originals | `tvnzbloombergoriginals` |
| Bloomberg TV+ | `tvnzbloombergtvplus` |
| FIFA+ | `tvnzfifa` |
| TVNZ 1 | `tvnz1` |
| TVNZ 2 | `tvnz2` |
| TVNZ DUKE | `tvnzduke` |
| TVNZ Popup 3 | `tvnzpopup3` |
| TVNZ Popup 4 | `tvnzpopup4` |
| TVNZ Popup 5 | `tvnzpopup5` |

</details>

## Status

**Pre-release.** Early days: it hasn't yet been tested across the wide variety of Home Assistant setups a stable release should handle, and entities or options may still change between releases.

Found a bug, or have an idea? Please [open an issue](https://github.com/Greminn/ha-nzxmltv/issues). Problems and feature ideas are equally welcome, not just polished bug reports.

## Credits

All guide data comes from [nzxmltv.com](https://nzxmltv.com), a separate project that isn't affiliated with this integration. The site publishes no usage terms, so please be considerate of it. Its service status is at <https://nzxmltv.statuspage.io>.
