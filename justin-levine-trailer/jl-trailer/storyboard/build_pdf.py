"""Justin Levine (Shepherd) trailer storyboard PDF: one scene per A4-landscape page -> scene line, asset links, 16:9 stills,
2-3 sentences. Same format as the KSS storyboard (~/ks-kristina-build/storyboard/build_pdf.py)."""
import os, subprocess, html
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
ST, TH = os.path.join(ROOT, 'stills'), os.path.join(ROOT, 'pdf', 'thumbs')
OUT = os.path.expanduser('~/Downloads/Justin Levine (Shepherd) - Trailer Storyboard.pdf')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
DL = 'file://' + os.path.expanduser('~/Downloads/')
J = lambda t: (f'Justin · Riverside track ({t})', DL + 'justin_levine-a179b1a2-3441-4183-baa5-1-CFR.mp4')
N = lambda t: (f'Nic · Riverside track ({t})', DL + 'nic-1668c829-216b-48c0-ba6a-1-CFR.mp4')
LK = lambda t: (f'Luke · Riverside track ({t})', DL + 'luke_sophinos-75b8dd46-261d-4272-b601-1-CFR.mp4')
YT = lambda title, vid, s: (f'{title} ({int(s) // 60}:{int(s) % 60:02d})', f'https://www.youtube.com/watch?v={vid}&t={int(s)}s')
CM = 'https://commons.wikimedia.org/wiki/File:'
SHEP = ('Shepherd brand film · shepherdinsurance.com', 'https://www.shepherdinsurance.com/')
LUMI, BCTT, PROG, ORCL, OSHA, LLOY = 'uUZU8QoGUlE', 'U05_dLMiqOo', 'ZymdJ-SAWwQ', 'WkkgqXrg-Xg', 'HA6bixDzeLY', 'ugRFJv_93ZU'
PROG99 = 'P1THtGT82mw'
SHEPV = 'https://vimeo.com/1157667900'
TV = ('Sony KV-20FV300 TV · Commons', CM + 'Sony_FD_Trinitron_KV-20FV300.jpg')
LOGO = {'autodesk': ('Autodesk logo · Commons', CM + 'Autodesk_Logo_2021.svg'), 'procore': ('Procore logo · Commons', CM + 'Procore-logo.jpg'),
        'greenlight': ('Greenlight Re logo · greenlightre.com', 'https://greenlightre.com/wp-content/uploads/2021/08/logo.svg'),
        'intact': ('Intact logo · Commons', CM + 'Intact_Financial_logo.svg')}
y = lambda title, vid, s: (f'{title} {int(s) // 60}:{int(s) % 60:02d}', f'https://www.youtube.com/watch?v={vid}&t={int(s)}s')
EPJ, EPN, EPL = [DL + f for f in ('justin_levine-a179b1a2-3441-4183-baa5-1-CFR.mp4', 'nic-1668c829-216b-48c0-ba6a-1-CFR.mp4',
                                  'luke_sophinos-75b8dd46-261d-4272-b601-1-CFR.mp4')]
tc = lambda s: f'{int(s) // 3600:02d}:{int(s) % 3600 // 60:02d}:{int(s) % 60:02d}'
rj = lambda s: (f'Justin track {tc(s)}', EPJ); rn = lambda s: (f'Nic track {tc(s)}', EPN); rl = lambda s: (f'Luke track {tc(s)}', EPL)
# every still -> the exact footage / B-roll / asset in it (source and timestamp of that frame)
SRC = {
    '01a_hook': [rj(259.4)], '01b_zero_time': [rj(261.6)], '01c_100_orchestrating': [rj(263.0)],
    '02a_nic_today': [rn(4.6)], '02b_name_card': [('Shepherd film 0:01', SHEPV)], '02c_shepherd_card': [('Shepherd film 0:22', SHEPV)],
    '02d_founded': [rj(163.0), y('LumiCon film', LUMI, 28)], '02e_tradetapp': [y('TradeTapp film', BCTT, 15)],
    '02f_buildingconnected': [y('BuildingConnected film', BCTT, 1)], '02g_autodesk': [y('Autodesk Gallery film', 'k4-SC5YxZFo', 2)],
    '02h_top_one_percent': [rn(1847.0)], '02i_procore': [rn(1858.4), LOGO['procore']],
    '02j_greenlight': [rn(1858.4), LOGO['procore'], LOGO['greenlight']], '02k_intact': [y('Becoming Intact Insurance', 'aOjXSQGntWM', 142)],
    '03a_jobsite': [y('LumiCon film', LUMI, 5)], '03a2_luminode': [y('LumiSense Installation', 'FUPy-YfgGDs', 46)],
    '03b_sensor': [y('LumiCon film', LUMI, 14)], '03b2_sensor_cage': [y('LumiCon Mass Concrete', 'CfwENc84sQc', 31)],
    '03b3_sensor_phone': [y('LumiCon Concrete Sensors', 'jSVfpOEYbaU', 57)], '03c_better_rates': [rn(1116.8)],
    '04a_flash_frame': [rj(1227.0)], '04b_fifteen_percent': [rj(1227.0)],
    '05a_progressive_tv': [y('Progressive 90s spot', PROG, 28), TV], '05a2_progressive_tv': [y('Progressive 1999 spot', PROG99, 60), TV],
    '05b_fifty': [('graphic, no footage', '')], '05c_thousands': [('graphic, no footage', '')], '05d_commercial': [y('Oracle Abilene', ORCL, 44)],
    '05d1_cyrusone': [y('CyrusOne data center', 'IAnIk69PJvY', 33)], '05d2_intel': [y('Intel Ohio One fab', 'i2HLl0Ewiao', 66)],
    '05d3_aligned': [y('Aligned NEO-01', 'Xs4DNe-QwdU', 31)], '05d4_microsoft': [y('Microsoft Fairwater', 'dx1vrbGIbYw', 70)],
    '06a_risk_manager': [rj(1619.0)], '06b_inspector': [y('OSHA film', OSHA, 226)],
    '06b1_arrives': [y('OSHA film', OSHA, 56)], '06b2_checklist': [y('OSHA film', OSHA, 166)], '06b3_walkround': [y('OSHA film', OSHA, 230)],
    '06c_manufactured': [y('OSHA', OSHA, 14), y('OSHA', OSHA, 192), y('OSHA', OSHA, 96)],
    '07a_inception': [rj(2395.5)], '07b_calendar_11_months': [('Texturelabs Paper 316', 'https://texturelabs.org/textures/paper_316/')],
    '07c_record_pace': [rj(2398.3)],
    '08a_ai_bubble': [rl(3015.9)], '08b_no': [rj(3019.8)], '08c_underestimated': [rj(3034.5)],
    '08c2_ai_cloud': [('motion ref: Pinterest pin', 'https://pin.it/byqxYwpKP'), ('real AI images, links above', '')],
    '08c3_ai_cloud_big': [('motion ref: Pinterest pin', 'https://pin.it/byqxYwpKP'), ('real AI images, links above', '')],
    '09_underwriters': [y('Inside Lloyd’s', LLOY, 97)],
    '10a_split_question': [rn(3069.0), rj(3082.35), rl(3085.0)], '10b_we_did_this': [rn(3069.0), rj(3082.35), rl(3085.0)],
    '10c_breaking_news': [rn(3069.0), rj(3082.35), rl(3085.0)], '10d_cut_to_black': [('black', '')],
    '10e_title_card': [('Verticals cover art', 'https://podcasts.apple.com/us/podcast/verticals-a-weekly-biz-show/id1846867433')],
}

SCENES = [
    ('“Our engineering team spends zero time writing code and 100% of their time orchestrating how the code is written.”',
     ['01a_hook', '01b_zero_time', '01c_100_orchestrating'], [J('00:04:18')],
     'Open cold on Justin, tight, with UNDERWRITERS ARE NEXT on the very first frame beside his head. No music, only room tone '
     'and soft keyboard clicks under “writing code”. The words land one by one on the empty side, and “100%” sits behind him '
     'as the sub drone fades in under “orchestrating”.'),
    ('NIC: “Today we’re super excited to bring on Justin Levine. He is the co-founder and CEO of Shepherd.” JUSTIN: “I had founded a '
     'construction software business.” “We sold our business to Building Connected and then, together, to Autodesk.” NIC: “You guys strike '
     'me as top one percent of companies…” “Procore and Greenlight Re from the beginning, Intact later on.”',
     ['02a_nic_today', '02b_name_card', '02c_shepherd_card', '02d_founded', '02e_tradetapp', '02f_buildingconnected',
      '02g_autodesk', '02h_top_one_percent', '02i_procore', '02j_greenlight', '02k_intact'],
     [N('00:00:03'), J('00:02:38'), J('00:44:59'), N('00:30:36'), N('00:30:53'),
      ('Shepherd brand film · Vimeo (0:01 Justin, 0:22 office sign)', SHEPV), SHEP,
      YT('LumiCon film · rebar cage on site', LUMI, 28),
      YT('BuildingConnected · TradeTapp film', BCTT, 15), YT('BuildingConnected logo', BCTT, 1),
      YT('Autodesk · Autodesk Gallery film', 'k4-SC5YxZFo', 2), ('Procore logo', CM + 'Procore-logo.jpg'),
      ('Greenlight Re logo', 'https://greenlightre.com/wp-content/uploads/2021/08/logo.svg'),
      YT('Intact · Becoming Intact Insurance', 'aOjXSQGntWM', 142)],
     'Whip to Nic on “Today we’re” as track A comes in. Justin appears in Shepherd’s own film with his name behind him and the title in front, '
     'then the Shepherd office sign shrinks into a card inside a hairline grid. Justin, cut out over a live job site, says “construction”; TradeTapp’s '
     'real product and the BuildingConnected logo cut inside the same card. “Autodesk” lands on Autodesk’s own footage of their San Francisco '
     'Gallery, Procore and Greenlight Re pop up as badge cards behind Nic, and “Intact” lands on Intact’s own film of the letters on their office wall. '
     'One soft impact per hit, riser into the next scene.'),
    ('“Maybe you put a sensor on site and we’ll give you better rates, right?”',
     ['03a_jobsite', '03a2_luminode', '03b_sensor', '03b2_sensor_cage', '03b3_sensor_phone', '03c_better_rates'],
     [N('00:18:30'), YT('Brickeye LumiCon film · aerial job site', LUMI, 5), YT('LumiCon sensor going onto steel', LUMI, 14),
      YT('LumiSense Installation and Connection · sensor close-up', 'FUPy-YfgGDs', 46),
      YT('LumiCon Mass Concrete Monitoring · sensor on the column cage', 'CfwENc84sQc', 31),
      YT('LumiCon Concrete Sensors · phone reading the sensor on site', 'jSVfpOEYbaU', 57)],
     'Hard cut to a job site from the air, then a fast run of real sensor footage from Brickeye, Shepherd’s IoT partner, with “Maybe you put a” '
     'carried across the cuts. The LumiNode sensor up close, then the LumiCon sensor going onto steel inside the centre cell of a hairline grid, '
     'hard-cutting inside the same cell to a sensor on a column cage and a phone reading it on a live pour while “sensor / on site” holds. '
     'Back to Nic for “better rates, right?” as the riser peaks.'),
    ('“Worth your while is 15% difference on price.”', ['04a_flash_frame', '04b_fifteen_percent'], [J('00:20:22')],
     'A one-frame colour-negative flash takes us into Justin. On the beat drop, a huge “15%” slams in behind him in the gradient, '
     'with the rest of the line split around it.'),
    ('“Progressive was the one that started and said we’re gonna go from 50 data points per underwriting submission to thousands.” '
     '“And I just think we can do the same thing in commercial.”',
     ['05a_progressive_tv', '05a2_progressive_tv', '05b_fifty', '05c_thousands', '05d1_cyrusone', '05d2_intel', '05d3_aligned',
      '05d4_microsoft', '05d_commercial'],
     [J('00:23:28'), J('00:23:43'), YT('Progressive late-1990s TV spot', PROG, 28), YT('Progressive 1999 TV spot', PROG99, 60),
      ('Sony FD Trinitron KV-20FV300 (TV frame)', CM + 'Sony_FD_Trinitron_KV-20FV300.jpg'),
      YT('CyrusOne · data center build timelapse', 'IAnIk69PJvY', 33), YT('Intel Ohio One fab · aerial', 'i2HLl0Ewiao', 66),
      YT('Aligned Data Centers · NEO-01 build', 'Xs4DNe-QwdU', 31), YT('Microsoft Fairwater AI datacenter · aerial', 'dx1vrbGIbYw', 70),
      YT('Oracle Abilene build · aerial', ORCL, 44)],
     'Progressive’s own 90s TV spots play inside a real Sony Trinitron that fills the left of frame, cutting from the logo card to the 1999 '
     'progressive.com spot inside the screen, with the line stacked on the right. “50” lights fifty points on a graph-paper '
     'grid and the counter ticks until the whole grid glows for THOUSANDS. Then a fast run of five real commercial builds, a cut about '
     'every 0.4 s: CyrusOne, Intel Ohio, Aligned, Microsoft Fairwater, then Oracle’s Abilene site for “commercial”. The sentence builds across '
     'the cuts, each phrase in a new spot.'),
    ('“I used to work at a construction company as a risk manager, and I knew when the insurance company was coming to inspect the job site.” '
     '“It’s somewhat manufactured.”',
     ['06a_risk_manager', '06b1_arrives', '06b_inspector', '06b2_checklist', '06b3_walkround', '06c_manufactured'],
     [J('00:26:57'), J('00:27:11'), YT('OSHA · inspector arrives', OSHA, 56), YT('OSHA · inspector with clipboard', OSHA, 226),
      YT('OSHA · inspection checklist', OSHA, 166), YT('OSHA · walk-round', OSHA, 230), YT('OSHA · walkaround', OSHA, 14),
      YT('OSHA · tidy yard', OSHA, 96), YT('OSHA · inspectors on the high-rise', OSHA, 192)],
     'The music stops dead and we slow-push on Justin, with “risk manager” beside him. OSHA’s own inspection film plays as a card beside the line: '
     'the inspector arriving at reception, then with his clipboard on a spotless site, his checklist, and the walk-round, hard cuts inside the same '
     'card while the line builds. Then three inspection shots collapse into a collage and “manufactured.” crosses them, '
     'white over the photos and gradient over the ground, on one low boom.'),
    ('“From inception of the company to our first insurance products being offered in market was about eleven months, which was like record pace.”',
     ['07a_inception', '07b_calendar_11_months', '07c_record_pace'],
     [J('00:39:52'), ('Texturelabs Paper 316 (calendar pages)', 'https://texturelabs.org/textures/paper_316/')],
     'Hard cut back to Justin and track B kicks in on “inception”. Calendar pages on real paper tear away to month 11 over page-flip ticks, with '
     '11 MONTHS in a neon box, then “record pace.” If the trailer runs long, this is the beat to cut first.'),
    ('LUKE: “Do you think we’re in an AI bubble?” JUSTIN: “No.” “I just think that we have consistently underestimated how big AI is.”',
     ['08a_ai_bubble', '08b_no', '08c_underestimated', '08c2_ai_cloud', '08c3_ai_cloud_big'],
     [LK('00:50:14'), J('00:50:20'), J('00:50:32'), ('Motion ref · Pinterest pin', 'https://pin.it/byqxYwpKP'),
      ('Sam Altman · Commons', CM + 'Sam_Altman_TechCrunch_SF_2019_Day_2_Oct_3_(cropped).jpg'),
      ('Jensen Huang · Commons', CM + 'Jensen_Huang_Stanford_2026-04-30_010_(cropped).jpg'),
      ('Dario Amodei · Commons', CM + 'Dario_Amodei_at_TechCrunch_Disrupt_2023_07.jpg'),
      ('Sundar Pichai · Commons', CM + 'Vietnamese_IT_community_Meets_Google_CEO_Sundar_Pichai_at_Hanoi07.jpg'),
      ('Mark Zuckerberg · Commons', CM + 'Mark_Zuckerberg_F8_2019_Keynote_(47774200621).jpg'),
      YT('Mira Murati · Dartmouth talk', 'yUoj9B8OpR8', 2100), YT('Lisa Su · AMD CES 2023', 'OMxU4BDIm4M', 1475),
      YT('BMW humanoid robots', 'bCkl9hIEb6k', 15), YT('BMW humanoid robots', 'bCkl9hIEb6k', 28),
      ('Axios · OpenAI revenue nears $70B', 'https://www.axios.com/2026/09/29/scoop-openais-annual-recurring-revenue-nears-70b'),
      YT('Microsoft Fairwater AI datacenter', 'dx1vrbGIbYw', 70), YT('Oracle Stargate Abilene', ORCL, 44),
      YT('Aligned NEO-01', 'Xs4DNe-QwdU', 31), YT('CyrusOne', 'IAnIk69PJvY', 33), YT('Intel Ohio One', 'i2HLl0Ewiao', 66)],
     'Luke asks in a dark caption box beside his head, and the music cuts out. One second of silence, then a hard cut to Justin and a huge dry “No.” '
     'behind him. Justin says “consistently”, then the frame breaks into the photo cloud from your Pinterest ref as track B swells back in: a thin '
     'stream of tiny thumbnails across the middle, with real AI images bursting out of it (Altman, Huang, Amodei, Pichai, Murati, Lisa Su, BMW’s '
     'humanoid robots, the Axios OpenAI scoop and the AI data centers). It reshuffles every half second and grows on “how big AI is.”'),
    ('“And so I think underwriting is another profession that is moving in that direction.”', ['09_underwriters'],
     [J('00:04:26'), YT('Inside Lloyd’s · underwriting room', LLOY, 97)],
     'Underwriters at their desks in Lloyd’s, playing inside the centre cell of a full-frame grid while the whole layer slowly pushes in, '
     'with the words in the cells around it. The long riser starts here. UNDERWRITERS ARE NEXT is not repeated, because it opens the trailer.'),
    ('NIC: “When do you think we will see the first fully AI underwritten commercial policy?” JUSTIN: “We actually, like, we did this.” '
     'LUKE: “Breaking news. Breaking news.”',
     ['10a_split_question', '10b_we_did_this', '10c_breaking_news', '10d_cut_to_black', '10e_title_card'],
     [N('00:51:09'), J('00:51:16'), LK('00:51:24'),
      ('Verticals cover art (wordmark)', 'https://podcasts.apple.com/us/podcast/verticals-a-weekly-biz-show/id1846867433')],
     'A three-way split of Nic, Justin and Luke under letterbox bars: whoever talks is lit and their words sit in the bottom bar. The riser stops '
     'dead before “We actually”, Justin plays dry, a news sting lands on “Breaking news”, then cut to black and the Verticals title card with '
     'JUSTIN LEVINE, SHEPHERD.'),
]

CSS = """
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #15171a; }
.pg { width: 297mm; height: 210mm; padding: 10mm 13mm 9mm; page-break-after: always; display: flex; flex-direction: column; }
.pg:last-child { page-break-after: auto; }
.hd { display: flex; align-items: baseline; gap: 12px; }
.no { font-size: 13px; font-weight: 700; color: #0a2a9e; letter-spacing: 1px; white-space: nowrap; }
.ln { font-size: 14.5px; font-weight: 500; line-height: 1.35; }
.links { margin-top: 6px; display: flex; flex-wrap: wrap; gap: 4px 6px; }
.links a { font-size: 9.5px; color: #0a2a9e; text-decoration: none; border: 1px solid #c9d2ef; border-radius: 3px; padding: 2px 6px; background: #f4f6fd; }
.st { flex: 1; display: flex; justify-content: center; align-items: center; margin: 7px 0; min-height: 0; }
.st img { display: block; border-radius: 3px; width: 100%; }
figure { display: flex; flex-direction: column; }
figcaption { font-size: 7.6px; line-height: 1.3; margin-top: 1.1mm; height: 5.6mm; overflow: hidden; color: #5a5f69; }
figcaption a { color: #0a2a9e; text-decoration: none; }
figcaption b { color: #15171a; font-weight: 600; margin-right: 4px; }
.tx { font-size: 12.5px; line-height: 1.45; max-width: 240mm; margin: 0 auto; text-align: center; color: #2a2d33; }
"""


def grid_w(n, area_w=268.0, area_h=116.0, gap=2.2, cap=6.8):
    """16:9 stills + a source caption under each: the width that gives the biggest still while the grid fits (mm)"""
    best, bc = 0, 1
    for c in range(1, n + 1):
        r = -(-n // c)
        w = min((area_w - gap * (c - 1)) / c, ((area_h - gap * (r - 1)) / r - cap) * 16 / 9)
        if w > best: best, bc = w, c
    return best, bc


def page(i, line, stills, links, text):
    w, c = grid_w(len(stills))
    def cap(s):
        parts = [f"<a href='{html.escape(u)}'>{html.escape(t)}</a>" if u else html.escape(t) for t, u in SRC[s]]
        return f"<figcaption><b>{s[:3].rstrip('_')}</b>{' · '.join(parts)}</figcaption>"
    imgs = ''.join(f"<figure style='width:{w:.1f}mm'><img src='file://{TH}/{s}.jpg'>{cap(s)}</figure>" for s in stills)
    imgs = f"<div style='display:flex;flex-wrap:wrap;justify-content:center;gap:2.2mm;flex-shrink:0;width:{c * w + 2.2 * (c - 1) + 1:.1f}mm'>{imgs}</div>"
    ls = ''.join(f"<a href='{html.escape(u)}'>{html.escape(t)}</a>" for t, u in links)
    return (f"<div class='pg'><div class='hd'><div class='no'>SCENE {i:02d}</div><div class='ln'>{html.escape(line)}</div></div>"
            f"<div class='links'>{ls}</div><div class='st'>{imgs}</div><div class='tx'>{html.escape(text)}</div></div>")


os.makedirs(TH, exist_ok=True)
for _, stills, _, _ in SCENES:
    for s in stills:
        Image.open(os.path.join(ST, s + '.png')).convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(TH, s + '.jpg'), quality=90)
doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" + \
      ''.join(page(i + 1, *s) for i, s in enumerate(SCENES)) + "</body></html>"
src = os.path.join(ROOT, 'pdf', 'storyboard.html'); open(src, 'w').write(doc)
subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--no-pdf-header-footer',
                '--user-data-dir=' + os.path.join(ROOT, 'pdf', 'chrome_prof'),
                f'--print-to-pdf={OUT}', 'file://' + src], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print(OUT)
