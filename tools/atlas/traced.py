"""Pictogram outlines traced from the TSRGD diagrams (Crown copyright, OGL v3.0).

Each entry is an SVG path (fill-rule evenodd) in face units, traced from the
statutory diagram rendered at 800 dpi (SI 2016/362 unless noted), with
cv2.findContours + approxPolyDP (epsilon about 1 px at 800 dpi). Only symbols are
traced; legend words are drawn with the Schedule 17 stand-in (atlas.lettering),
never traced, so no DfT font outlines ship here. Generated in QA round 6; the
source of each entry is in SOURCE.

Page refs: "printed pN" is the page number printed on the SI page and is the same
in every copy. Each "PDF pN" names its file: tsrgd2016.pdf (refs/tsrgd2016.pdf,
a local copy with an extra cover note: PDF = printed + 1); refs/si2016.pdf (the legislation.gov.uk
file: PDF = printed); refs/si2002.pdf (PDF = printed = si2002-pages/p-NNN.png).
"""
from __future__ import annotations

SOURCE: dict[str, str] = {
    '2701': "SI 2016/362 Sch 13 Pt 6, diagrams 2701 and 2701.1 (printed p397 = tsrgd2016.pdf PDF p398): 2701 flag-type plate, black border, chevron and house symbol traced; 'Oak Farm Estate' example legend stand-in",
    '531.1A': 'SI 2016/362 Sch 2 Pt 4 item 3, diagram 531.1A (printed p56 = tsrgd2016.pdf PDF p57): black arch and headroom pointer traced; first alternative legend 12\'-6" in stand-in lettering (the SI also shows 3.8 m)',
    '551': 'SI 2016/362 Sch 2 Pt 2 item 32, diagram 551 (printed p47 = tsrgd2016.pdf PDF p48): black deer symbol inside the warning triangle',
    '555': 'SI 2016/362 Sch 2 Pt 2, diagram 555 (printed p48 = tsrgd2016.pdf PDF p49): black quay edge, falling car and water',
    '619.1': 'SI 2016/362 Sch 3 Pt 2 item 18, diagram 619.1 (printed p71 = tsrgd2016.pdf PDF p72), 600 dpi, page upright (diagram column rotated -90 deg to read, as the legends of 622.4 confirm): black front-view car',
    '619.2': 'SI 2016/362 Sch 3 Pt 2 item 20, diagram 619.2 (printed p72 = tsrgd2016.pdf PDF p73), 600 dpi, page upright (diagram column rotated -90 deg to read, as the legends of 622.4 confirm): black motorcycle and rider',
    '622.2/black': 'SI 2016/362 Sch 3 Pt 2 item 14, diagram 622.2 (printed p71 = tsrgd2016.pdf PDF p72), 600 dpi, page upright (diagram column rotated -90 deg to read, as the legends of 622.4 confirm): black diagonal bands',
    '622.2/grey': 'SI 2016/362 Sch 3 Pt 2 item 14, diagram 622.2 (printed p71 = tsrgd2016.pdf PDF p72), 600 dpi, page upright (diagram column rotated -90 deg to read, as the legends of 622.4 confirm): grey ring and goods vehicle',
    '622.5': 'SI 2016/362 Sch 3 Pt 2 item 23, diagram 622.5 (printed p72 = tsrgd2016.pdf PDF p73), 600 dpi, page upright (diagram column rotated -90 deg to read, as the legends of 622.4 confirm): black horse-drawn cart',
    '622.6': 'SI 2016/362 Sch 3 Pt 2 item 24, diagram 622.6 (printed p72 = tsrgd2016.pdf PDF p73), 600 dpi, page upright (diagram column rotated -90 deg to read, as the legends of 622.4 confirm): black horse and rider',
    '622.8/black': 'SI 2016/362 Sch 3 Pt 2 item 16, diagram 622.8 (printed p71 = tsrgd2016.pdf PDF p72), page upright = page rotated 90 deg clockwise (diagram column printed sideways, as the legends of 622.4 confirm); r6 paths restored in 622.8-fix (r7 re-trace read the raw page and was rotated 90 deg): black burst detail and front-view vehicle below the burst',
    '622.8/orange': 'SI 2016/362 Sch 3 Pt 2 item 16, diagram 622.8 (printed p71 = tsrgd2016.pdf PDF p72), page upright = page rotated 90 deg clockwise (diagram column printed sideways, as the legends of 622.4 confirm); r6 paths restored in 622.8-fix (r7 re-trace read the raw page and was rotated 90 deg): orange burst above the vehicle (print sample #F89C22, drawn as palette amber)',
    '625.1': 'SI 2016/362 Sch 3 Pt 2 item 22, diagram 625.1 (printed p72 = tsrgd2016.pdf PDF p73), 600 dpi, page upright (diagram column rotated -90 deg to read, as the legends of 622.4 confirm): black walking pedestrian',
    '675A': 'SI 2016/362 Sch 10 Pt 2 item 6, diagram 675A (printed p179 = tsrgd2016.pdf PDF p180): 600 x 700 composite, 30 mph roundel over the Zone ENDS panel (grey 20 roundel, black end stripes); numerals and words stand-in',
    '770': 'SI 2016/362 Sch 2 Pt 2 item 51, diagram 770 (printed p51 = tsrgd2016.pdf PDF p52): black gate symbol',
    '771': 'SI 2016/362 Sch 2 Pt 2 item 52, diagram 771 (printed p51 = tsrgd2016.pdf PDF p52): black steam locomotive',
    '827.1': "SI 2016/362 Sch 11 Pt 2 item 66, diagram 827.1 (printed p213 = tsrgd2016.pdf PDF p214): blue plate, white H traced; 'No A & E' stand-in",
    '953.1': 'SI 2016/362 Sch 3 Pt 2 item 36, diagram 953.1 (printed p75 = tsrgd2016.pdf PDF p76): white tram on the blue disc',
    '958': 'SI 2016/362 Sch 11 Pt 2 item 37, diagram 958 (printed p201 = tsrgd2016.pdf PDF p202): frame, broken lane line and symbols traced; legends stand-in',
    '959B': 'SI 2016/362 Sch 9 Pt 4 item 10, diagram 959B (printed p144 = tsrgd2016.pdf PDF p145): frame, lane line, local-bus, motor cycle and pedal cycle symbols traced; legends stand-in',
    '960': 'SI 2016/362 Sch 9 Pt 4 item 8, diagram 960 (printed p143 = tsrgd2016.pdf PDF p144): frame, lane arrows, bus and pedal cycle traced',
    'MARKER': 'SI 2002/3113 Sch 7 Part VIII diagram 2717 (printed p275 = refs/si2002.pdf PDF p275, 150 dpi greyscale scan): telephone handset and arrow traced; route letters stand-in. 2717 is absent from SI 2016',
    '618': 'SI 2002/3113 diagram 618 (printed p81 = refs/si2002.pdf PDF p81), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '618.1': 'SI 2002/3113 diagram 618.1 (printed p81 = refs/si2002.pdf PDF p81), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '618.2': 'SI 2002/3113 diagram 618.2 (printed p82 = refs/si2002.pdf PDF p82), 300 dpi colour render, portrait page; diagram absent from SI 2016: red ring from render._ring_roundel; inner layers traced by colour (generator b2)',
    '618.3': 'SI 2002/3113 diagram 618.3 (printed p83 = refs/si2002.pdf PDF p83), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '618.3A': 'SI 2002/3113 diagram 618.3A (printed p84 = refs/si2002.pdf PDF p84), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '618.4': 'SI 2002/3113 diagram 618.4 (printed p85 = refs/si2002.pdf PDF p85), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '622.9': 'SI 2002/3113 diagram 622.9 (printed p88 = refs/si2002.pdf PDF p88), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '627.1': 'SI 2002/3113 diagram 627.1 (printed p89 = refs/si2002.pdf PDF p89), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '637.1': 'SI 2002/3113 diagram 637.1 (printed p91 = refs/si2002.pdf PDF p91), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '637.2': 'SI 2002/3113 diagram 637.2 (printed p92 = refs/si2002.pdf PDF p92), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '637.3': 'SI 2002/3113 diagram 637.3 (printed p93 = refs/si2002.pdf PDF p93), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '638': 'SI 2002/3113 diagram 638 (printed p93 = refs/si2002.pdf PDF p93), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '638.1': 'SI 2002/3113 diagram 638.1 (printed p93 = refs/si2002.pdf PDF p93), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '639': 'SI 2002/3113 diagram 639 (printed p93 = refs/si2002.pdf PDF p93), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '639.1B': 'SI 2002/3113 diagram 639.1B (printed p94 = refs/si2002.pdf PDF p94), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '640': 'SI 2002/3113 diagram 640 (printed p94 = refs/si2002.pdf PDF p94), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '640.2A': 'SI 2002/3113 diagram 640.2A (printed p95 = refs/si2002.pdf PDF p95), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '640.3': 'SI 2002/3113 diagram 640.3 (printed p96 = refs/si2002.pdf PDF p96), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '640.4': 'SI 2002/3113 diagram 640.4 (printed p96 = refs/si2002.pdf PDF p96), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '642.3': 'SI 2002/3113 diagram 642.3 (printed p97 = refs/si2002.pdf PDF p97), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '650.1': 'SI 2002/3113 diagram 650.1 (printed p98 = refs/si2002.pdf PDF p98), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '650.2': 'SI 2002/3113 diagram 650.2 (printed p99 = refs/si2002.pdf PDF p99), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '650.3': 'SI 2002/3113 diagram 650.3 (printed p99 = refs/si2002.pdf PDF p99), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '660.3': 'SI 2002/3113 diagram 660.3 (printed p100 = refs/si2002.pdf PDF p100), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '660.4': 'SI 2002/3113 diagram 660.4 (printed p101 = refs/si2002.pdf PDF p101), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '660.5': 'SI 2002/3113 diagram 660.5 (printed p101 = refs/si2002.pdf PDF p101), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '660.6': 'SI 2002/3113 diagram 660.6 (printed p102 = refs/si2002.pdf PDF p102), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '660.7': 'SI 2002/3113 diagram 660.7 (printed p103 = refs/si2002.pdf PDF p103), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '661.1': 'SI 2002/3113 diagram 661.1 (printed p104 = refs/si2002.pdf PDF p104), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '661.2A': 'SI 2002/3113 diagram 661.2A (printed p104 = refs/si2002.pdf PDF p104), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '661.3A': 'SI 2002/3113 diagram 661.3A (printed p104 = refs/si2002.pdf PDF p104), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b2); legends in stand-in lettering at measured positions',
    '661.4': 'SI 2002/3113 diagram 661.4 (printed p105 = refs/si2002.pdf PDF p105), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '662': 'SI 2002/3113 diagram 662 (printed p105 = refs/si2002.pdf PDF p105), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '675B': 'SI 2016/362 Sch 10 Pt 2, diagram 675B (printed p179 = tsrgd2016.pdf PDF p180), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '878': 'SI 2016/362 Sch 11 Pt 2, diagram 878 (printed p212 = tsrgd2016.pdf PDF p213), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '880': 'SI 2016/362 Sch 11 Pt 2, diagram 880 (printed p212 = tsrgd2016.pdf PDF p213), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '818.5': 'SI 2016/362 Sch 12 Pt 28, diagram 818.5 (printed p363 = tsrgd2016.pdf PDF p364), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '636': 'SI 2016/362 Sch 13 Pt 6, diagram 636 (printed p393 = tsrgd2016.pdf PDF p394), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3)',
    '640.1': 'SI 2016/362 Sch 13 Pt 6, diagram 640.1 (printed p394 = tsrgd2016.pdf PDF p395), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '622.4': 'SI 2016/362 Sch 3 Pt 2, diagram 622.4 (printed p71 = tsrgd2016.pdf PDF p72), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): red ring from render._ring_roundel; inner layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '640.5': 'SI 2016/362 Sch 7 Pt 2, diagram 640.5 (printed p111 = tsrgd2016.pdf PDF p112), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '647': 'SI 2016/362 Sch 7 Pt 2, diagram 647 (printed p111 = tsrgd2016.pdf PDF p112), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '667': 'SI 2016/362 Sch 7 Pt 2, diagram 667 (printed p113 = tsrgd2016.pdf PDF p114), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3)',
    '667.1': 'SI 2016/362 Sch 7 Pt 2, diagram 667.1 (printed p113 = tsrgd2016.pdf PDF p114), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '667.2': 'SI 2016/362 Sch 7 Pt 2, diagram 667.2 (printed p114 = tsrgd2016.pdf PDF p115), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3)',
    '668': 'SI 2016/362 Sch 7 Pt 2, diagram 668 (printed p113 = tsrgd2016.pdf PDF p114), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3)',
    '668.1': 'SI 2016/362 Sch 7 Pt 2, diagram 668.1 (printed p114 = tsrgd2016.pdf PDF p115), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '668.2': 'SI 2016/362 Sch 7 Pt 2, diagram 668.2 (printed p114 = tsrgd2016.pdf PDF p115), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3)',
    '618.3B': 'SI 2016/362 Sch 8 Pt 2, diagram 618.3B (printed p129 = tsrgd2016.pdf PDF p130), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '618.3C': 'SI 2016/362 Sch 8 Pt 2, diagram 618.3C (printed p130 = tsrgd2016.pdf PDF p131), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '651': 'SI 2016/362 Sch 9 Pt 4, diagram 651 (printed p140 = tsrgd2016.pdf PDF p141), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b3); legends in stand-in lettering at measured positions',
    '954': 'SI 2002/3113 diagram 954 (printed p146 = refs/si2002.pdf PDF p146), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '954.2': 'SI 2002/3113 diagram 954.2 (printed p146 = refs/si2002.pdf PDF p146), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '957': 'SI 2016/362 Sch 3 Pt 2, diagram 957 (printed p74 = tsrgd2016.pdf PDF p75), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): blue disc from render._mand; inner layers traced by colour (generator b4)',
    '513.1': 'SI 2002/3113 diagram 513.1 (printed p50 = refs/si2002.pdf PDF p50), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '532.3': 'SI 2002/3113 diagram 532.3 (printed p61 = refs/si2002.pdf PDF p61), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '548.1': 'SI 2002/3113 diagram 548.1 (printed p65 = refs/si2002.pdf PDF p65), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '553.2': 'SI 2002/3113 diagram 553.2 (printed p68 = refs/si2002.pdf PDF p68), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '573': 'SI 2002/3113 diagram 573 (printed p74 = refs/si2002.pdf PDF p74), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '575': 'SI 2002/3113 diagram 575 (printed p75 = refs/si2002.pdf PDF p75), 300 dpi colour render, portrait page; diagram absent from SI 2016: plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '775': 'SI 2016/362 Sch 11 Pt 2, diagram 775 (printed p213 = tsrgd2016.pdf PDF p214), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '783': 'SI 2016/362 Sch 11 Pt 2, diagram 783 (printed p214 = tsrgd2016.pdf PDF p215), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '786': 'SI 2016/362 Sch 11 Pt 2, diagram 786 (printed p215 = tsrgd2016.pdf PDF p216), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '787': 'SI 2016/362 Sch 11 Pt 2, diagram 787 (printed p215 = tsrgd2016.pdf PDF p216), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4)',
    '788': 'SI 2016/362 Sch 11 Pt 2, diagram 788 (printed p216 = tsrgd2016.pdf PDF p217), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4)',
    '883': 'SI 2016/362 Sch 11 Pt 2, diagram 883 (printed p199 = tsrgd2016.pdf PDF p200), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '884': 'SI 2016/362 Sch 11 Pt 2, diagram 884 (printed p198 = tsrgd2016.pdf PDF p199), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4)',
    '551.1': 'SI 2016/362 Sch 13 Pt 2, diagram 551.1 (printed p366 = tsrgd2016.pdf PDF p367), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): warning triangle from render._warn; symbol layers traced by colour (generator b4)',
    '773': 'SI 2016/362 Sch 14 Pt 2, diagram 773 (printed p446 = tsrgd2016.pdf PDF p447), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '544.2': 'SI 2016/362 Sch 2 Pt 2, diagram 544.2 (printed p45 = tsrgd2016.pdf PDF p46), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): warning triangle from render._warn; symbol layers traced by colour (generator b4)',
    '551.2': 'SI 2016/362 Sch 2 Pt 2, diagram 551.2 (printed p47 = tsrgd2016.pdf PDF p48), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): warning triangle from render._warn; symbol layers traced by colour (generator b4)',
    '581': 'SI 2016/362 Sch 2 Pt 2, diagram 581 (printed p49 = tsrgd2016.pdf PDF p50), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): warning triangle from render._warn; symbol layers traced by colour (generator b4)',
    '582': 'SI 2016/362 Sch 2 Pt 2, diagram 582 (printed p50 = tsrgd2016.pdf PDF p51), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): warning triangle from render._warn; symbol layers traced by colour (generator b4)',
    '772': 'SI 2016/362 Sch 2 Pt 2, diagram 772 (printed p51 = tsrgd2016.pdf PDF p52), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): warning triangle from render._warn; symbol layers traced by colour (generator b4)',
    '782': 'SI 2016/362 Sch 2 Pt 2, diagram 782 (printed p52 = tsrgd2016.pdf PDF p53), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): warning triangle from render._warn; symbol layers traced by colour (generator b4)',
    '513.2': 'SI 2016/362 Sch 2 Pt 3, diagram 513.2 (printed p53 = tsrgd2016.pdf PDF p54), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '530.1': 'SI 2016/362 Sch 2 Pt 5, diagram 530.1 (printed p58 = tsrgd2016.pdf PDF p59), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '531.2': 'SI 2016/362 Sch 2 Pt 5, diagram 531.2 (printed p58 = tsrgd2016.pdf PDF p59), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
    '572': 'SI 2016/362 Sch 2 Pt 5, diagram 572 (printed p60 = tsrgd2016.pdf PDF p61), 400 dpi, page rotated 90 deg clockwise to read (table printed sideways): plate silhouette and symbol layers traced by colour (generator b4); legends in stand-in lettering at measured positions',
}

PATHS: dict[str, str] = {
    '2701/0': (
        'M-1.5789,-0.383 -1.5789,0.383 -1.5614,0.4327 -1.5263,0.4708 -1.4912,0.4912 -1.4591,0.4971 1.2339'
        ',0.4971 1.2719,0.4883 1.307,0.4678 1.3392,0.4298 1.5673,0.0322 1.576,-0.0029 1.5673,-0.038 1.339'
        '2,-0.4357 1.2953,-0.4795 1.2661,-0.4942 1.2368,-0.5 -1.4737,-0.5 -1.5146,-0.4854 -1.5526,-0.4503'
        ' -1.5731,-0.4152Z'
    ),
    '2701/1': (
        'M-1.0965,0.0877 -1.0965,0.1871 -0.9357,0.1871 -0.9357,0.0877ZM-1.2895,0.0877 -1.2895,0.2719 -1.2'
        '164,0.2719 -1.2164,0.0877ZM-1.0965,-0.1053 -1.0965,-0.0088 -0.9357,-0.0088 -0.9357,-0.1053ZM-1.3'
        '129,-0.1053 -1.3129,-0.0088 -1.1959,-0.0088 -1.1959,-0.1053ZM-1.5058,-0.3801 -1.5058,0.3772 -1.5'
        '029,0.3889 -1.4883,0.4094 -1.4708,0.4211 -1.4561,0.424 1.2368,0.424 1.2602,0.4123 1.2778,0.3918 '
        '1.5029,0 1.2807,-0.3918 1.2485,-0.424 1.2281,-0.4298 -1.4532,-0.4298 -1.4678,-0.4269 -1.4912,-0.'
        '4123ZM-1.4094,-0.1784 -1.1082,-0.3099 -1.076,-0.3012 -0.9561,-0.2485 -0.9532,-0.3099 -0.883,-0.3'
        '099 -0.8801,-0.2164 -0.7953,-0.1784 -0.7982,-0.1491 -0.8392,-0.1491 -0.8392,0.3012 -1.3626,0.304'
        '1 -1.3655,-0.1491 -1.4064,-0.1491ZM0.9942,-0.3743 1.1988,-0.3743 1.4152,-0.0029 1.1988,0.3713 0.'
        '9912,0.3684 1.2047,0 0.9942,-0.3626Z'
    ),
    '531.1A/0': (
        'M-0.4159,0.3866 -0.2694,0.3866 -0.2694,0.2373 -0.2568,0.2233 -0.2122,0.1828 -0.1815,0.1619 -0.14'
        '66,0.1438 -0.0796,0.1214 -0.0391,0.1145 -0.0112,0.1131 0.0433,0.1158 0.0684,0.12 0.1158,0.134 0.'
        '141,0.1438 0.1759,0.1619 0.2066,0.1828 0.2331,0.2052 0.2638,0.2373 0.2638,0.3866 0.4104,0.3866 0'
        '.275,0.1521 0.261,0.1326 0.2303,0.1103 0.1954,0.0893 0.1563,0.0712 0.0824,0.0489 0.0433,0.0433 0'
        '.0028,0.0405 -0.0475,0.0433 -0.0879,0.0489 -0.1619,0.0712 -0.208,0.0935 -0.2359,0.1103 -0.2666,0'
        '.1326 -0.2764,0.1452ZM-0.0028,0.007 0.0042,-0.0014 0.0949,-0.1591 -0.0977,-0.1591Z'
    ),
    '551': (
        'M0.003,-0.188 -0.003,-0.188 -0.008,-0.184 -0.008,-0.128 -0.037,-0.124 -0.041,-0.137 -0.041,-0.16'
        '1 -0.043,-0.166 -0.052,-0.166 -0.057,-0.137 -0.07,-0.146 -0.079,-0.141 -0.077,-0.133 -0.055,-0.1'
        '1 -0.057,-0.104 -0.07,-0.108 -0.099,-0.137 -0.108,-0.135 -0.108,-0.124 -0.081,-0.092 -0.066,-0.0'
        '88 -0.008,-0.028 0.023,-0.012 0.066,-0.008 0.057,0.014 0.035,0.046 -0.035,0.05 -0.121,0.032 -0.1'
        '75,0.035 -0.219,0.057 -0.235,0.072 -0.242,0.092 -0.242,0.11 -0.237,0.126 -0.219,0.135 -0.206,0.1'
        '61 -0.177,0.195 -0.177,0.21 -0.193,0.231 -0.19,0.246 -0.182,0.253 -0.166,0.257 -0.159,0.264 -0.1'
        '46,0.286 -0.126,0.308 -0.115,0.333 -0.106,0.34 -0.106,0.355 -0.084,0.369 -0.072,0.369 -0.07,0.35'
        '5 -0.086,0.324 -0.104,0.304 -0.11,0.291 -0.108,0.288 -0.084,0.302 -0.072,0.317 -0.063,0.317 -0.0'
        '57,0.324 -0.063,0.349 -0.05,0.364 -0.048,0.382 -0.043,0.386 -0.028,0.386 -0.023,0.38 -0.03,0.36 '
        '-0.03,0.331 -0.01,0.268 -0.003,0.259 0.019,0.259 0.032,0.255 0.077,0.226 0.112,0.213 0.121,0.204'
        ' 0.124,0.186 0.119,0.182 0.075,0.164 0.07,0.157 0.081,0.146 0.092,0.141 0.095,0.128 0.104,0.11 0'
        '.126,0.079 0.13,0.059 0.157,0.048 0.186,0.048 0.197,0.035 0.202,0.019 0.199,0.012 0.179,0.006 0.'
        '161,-0.01 0.139,-0.021 0.133,-0.021 0.121,-0.03 0.148,-0.046 0.157,-0.059 0.157,-0.07 0.146,-0.0'
        '68 0.144,-0.075 0.135,-0.079 0.13,-0.066 0.126,-0.084 0.121,-0.088 0.115,-0.088 0.115,-0.061 0.1'
        '01,-0.048 0.088,-0.048 0.081,-0.055 0.09,-0.066 0.097,-0.086 0.09,-0.11 0.075,-0.13 0.066,-0.128'
        ' 0.066,-0.119 0.079,-0.097 0.079,-0.088 0.072,-0.075 0.063,-0.07 0.057,-0.072 0.035,-0.092 0.014'
        ',-0.128 0.008,-0.157 0.008,-0.179ZM0.003,0.231 0.01,0.21 0.03,0.188 0.077,0.199 0.026,0.226 0.01'
        ',0.226 0.006,0.233ZM-0.104,0.175 -0.063,0.188 -0.026,0.19 -0.021,0.195 -0.028,0.228 -0.046,0.239'
        ' -0.046,0.262 -0.039,0.264 -0.039,0.275 -0.048,0.295 -0.119,0.255 -0.144,0.233 -0.141,0.228 -0.1'
        '26,0.222 -0.119,0.215 -0.108,0.195 -0.108,0.179ZM0.008,-0.09 0.01,-0.092 0.021,-0.077 0.063,-0.0'
        '37 0.05,-0.032 0.032,-0.037 0.021,-0.05 0.021,-0.059ZM-0.03,-0.106 -0.003,-0.108 0.003,-0.101 -0'
        '.012,-0.099 0.003,-0.063 -0.001,-0.057 -0.006,-0.057 -0.026,-0.081 -0.032,-0.099Z'
    ),
    '555': (
        'M0.403,0.366 0.387,0.339 0.369,0.357 0.349,0.359 0.336,0.353 0.311,0.33 0.289,0.324 0.262,0.326 '
        '0.242,0.337 0.224,0.355 0.213,0.359 0.195,0.357 0.166,0.333 0.142,0.324 0.115,0.326 0.097,0.335 '
        '0.077,0.355 0.066,0.359 0.052,0.359 0.039,0.353 0.028,0.339 0.003,0.326 -0.039,0.326 -0.039,0.30'
        '6 -0.021,0.295 -0.001,0.297 0.026,0.321 0.05,0.33 0.068,0.33 0.084,0.326 0.126,0.295 0.146,0.297'
        ' 0.175,0.321 0.2,0.33 0.227,0.328 0.244,0.319 0.264,0.299 0.276,0.295 0.296,0.297 0.323,0.321 0.'
        '338,0.328 0.365,0.33 0.381,0.326 0.365,0.301 0.345,0.301 0.336,0.297 0.323,0.281 0.296,0.268 0.2'
        '69,0.268 0.256,0.272 0.224,0.299 0.213,0.304 0.191,0.299 0.171,0.279 0.146,0.268 0.113,0.27 0.09'
        '9,0.277 0.079,0.297 0.064,0.304 0.044,0.299 0.017,0.275 -0.001,0.268 -0.028,0.268 -0.037,0.272 -'
        '0.039,0.27 -0.039,0.25 -0.023,0.239 -0.006,0.239 0.003,0.243 0.023,0.263 0.044,0.272 0.059,0.275'
        ' 0.093,0.266 0.115,0.243 0.126,0.239 0.148,0.241 0.175,0.266 0.206,0.275 0.224,0.272 0.24,0.266 '
        '0.267,0.241 0.289,0.239 0.3,0.243 0.32,0.263 0.349,0.275 0.323,0.228 0.314,0.219 0.296,0.212 0.2'
        '6,0.214 0.247,0.221 0.227,0.241 0.218,0.246 0.198,0.246 0.189,0.241 0.175,0.225 0.148,0.212 0.11'
        '9,0.212 0.102,0.219 0.07,0.246 0.05,0.246 0.041,0.241 0.023,0.223 0.001,0.212 -0.039,0.212 -0.03'
        '9,0.027 -0.044,0.025 -0.039,0.02 -0.021,0.029 0.119,0.129 0.119,0.163 0.126,0.174 0.142,0.185 0.'
        '166,0.187 0.182,0.181 0.189,0.174 0.213,0.174 0.242,0.134 0.242,0.118 0.155,0.033 0.155,-0.04 0.'
        '148,-0.054 0.075,-0.107 0.044,-0.125 -0.001,-0.127 -0.068,-0.114 -0.095,-0.121 -0.106,-0.121 -0.'
        '146,-0.062 -0.104,-0.027 -0.106,0.002 -0.099,0.016 -0.088,0.025 -0.209,0.027 -0.416,0.386 -0.039'
        ',0.386 -0.039,0.362 -0.019,0.35 -0.01,0.35 0.006,0.357 0.019,0.373 0.048,0.386 0.073,0.386 0.09,'
        '0.379 0.117,0.355 0.128,0.35 0.151,0.355 0.171,0.375 0.195,0.386 0.229,0.384 0.242,0.377 0.264,0'
        '.355 0.276,0.35 0.298,0.355 0.316,0.373 0.343,0.386 0.376,0.384ZM0.155,0.127 0.166,0.129 0.177,0'
        '.143 0.175,0.156 0.162,0.167 0.148,0.165 0.137,0.152 0.142,0.136ZM-0.073,-0.029 -0.057,-0.027 -0'
        '.048,-0.016 -0.048,-0.002 -0.066,0.011 -0.075,0.009 -0.086,-0.002 -0.086,-0.016ZM0.084,-0.071 0.'
        '108,-0.058 0.14,-0.033 0.135,0.02 0.059,-0.033ZM-0.021,-0.092 0.03,-0.103 0.044,-0.103 0.075,-0.'
        '08 0.046,-0.042 -0.019,-0.087Z'
    ),
    '619.1': (
        'M-0.191,-0.274 -0.208,-0.257 -0.219,-0.235 -0.242,-0.088 -0.258,-0.083 -0.278,-0.063 -0.281,-0.0'
        '55 -0.281,0.091 -0.278,0.100 -0.258,0.119 -0.258,0.215 -0.228,0.232 -0.205,0.232 -0.180,0.221 -0'
        '.171,0.212 -0.171,0.128 -0.169,0.125 -0.073,0.128 -0.070,0.131 0.070,0.131 0.073,0.128 0.169,0.1'
        '25 0.171,0.128 0.171,0.212 0.183,0.223 0.205,0.232 0.228,0.232 0.258,0.215 0.258,0.119 0.275,0.1'
        '03 0.281,0.088 0.281,-0.052 0.275,-0.066 0.261,-0.080 0.242,-0.088 0.219,-0.232 0.208,-0.257 0.1'
        '83,-0.279 0.157,-0.288 -0.157,-0.288 -0.177,-0.282ZM-0.143,0.072 -0.140,0.069 0.140,0.069 0.143,'
        '0.083 0.124,0.088 -0.121,0.088 -0.124,0.086 -0.140,0.086ZM-0.143,0.027 -0.140,0.024 0.140,0.024 '
        '0.143,0.027 0.143,0.041 0.138,0.046 -0.140,0.046 -0.143,0.044ZM-0.143,-0.015 -0.140,-0.018 -0.10'
        '1,-0.018 -0.098,-0.021 0.104,-0.021 0.107,-0.018 0.140,-0.018 0.143,-0.004 0.140,-0.001 -0.140,-'
        '0.001ZM0.208,-0.058 0.228,-0.052 0.242,-0.038 0.247,-0.027 0.247,-0.007 0.242,0.004 0.219,0.021 '
        '0.191,0.018 0.177,0.007 0.169,-0.013 0.169,-0.024 0.177,-0.041 0.185,-0.049ZM-0.222,-0.055 -0.21'
        '1,-0.058 -0.185,-0.049 -0.177,-0.041 -0.169,-0.024 -0.169,-0.013 -0.174,0.001 -0.183,0.013 -0.19'
        '7,0.021 -0.219,0.021 -0.230,0.015 -0.247,-0.007 -0.244,-0.035ZM-0.205,-0.145 -0.202,-0.147 -0.19'
        '7,-0.192 -0.185,-0.212 -0.163,-0.232 -0.146,-0.237 -0.070,-0.240 -0.067,-0.243 0.067,-0.243 0.07'
        '0,-0.240 0.146,-0.237 0.171,-0.226 0.194,-0.198 0.205,-0.136 0.202,-0.128 0.183,-0.111 0.051,-0.'
        '114 0.048,-0.117 -0.048,-0.117 -0.051,-0.114 -0.183,-0.111 -0.202,-0.128Z'
    ),
    '619.2': (
        'M-0.331,0.044 -0.331,0.060 -0.334,0.063 -0.331,0.066 -0.331,0.088 -0.326,0.108 -0.315,0.128 -0.2'
        '81,0.159 -0.236,0.173 -0.199,0.170 -0.177,0.162 -0.143,0.133 -0.129,0.111 -0.121,0.086 -0.121,0.'
        '049 -0.132,0.015 -0.157,-0.015 -0.152,-0.021 -0.135,-0.004 -0.121,0.018 -0.112,0.044 -0.110,0.08'
        '8 -0.093,0.111 -0.070,0.119 0.121,0.119 0.152,0.153 0.188,0.170 0.205,0.170 0.208,0.173 0.239,0.'
        '170 0.281,0.150 0.301,0.131 0.315,0.105 0.320,0.086 0.320,0.069 0.323,0.066 0.340,0.066 0.340,0.'
        '044 0.323,-0.001 0.292,-0.035 0.264,-0.052 0.261,-0.072 0.250,-0.080 0.146,-0.080 0.138,-0.111 0'
        '.079,-0.176 0.039,-0.192 0.022,-0.195 0.017,-0.201 0.017,-0.209 0.028,-0.229 0.025,-0.251 0.014,'
        '-0.268 -0.003,-0.277 -0.034,-0.274 -0.053,-0.251 -0.056,-0.232 -0.051,-0.232 -0.045,-0.226 -0.04'
        '5,-0.195 -0.039,-0.187 -0.020,-0.178 -0.045,-0.133 -0.059,-0.119 -0.087,-0.100 -0.098,-0.111 -0.'
        '084,-0.167 -0.081,-0.192 -0.076,-0.206 -0.076,-0.215 -0.084,-0.215 -0.132,-0.133 -0.157,-0.108 -'
        '0.191,-0.094 -0.233,-0.094 -0.233,-0.049 -0.197,-0.046 -0.188,-0.038 -0.197,-0.035 -0.216,-0.041'
        ' -0.236,-0.041 -0.264,-0.035 -0.287,-0.024 -0.315,0.004ZM0.216,0.004 0.247,0.013 0.267,0.032 0.2'
        '75,0.052 0.275,0.080 0.267,0.100 0.250,0.117 0.236,0.125 0.205,0.128 0.183,0.119 0.163,0.100 0.1'
        '54,0.083 0.152,0.060 0.163,0.032 0.177,0.021 0.183,0.032 0.183,0.041 0.174,0.055 0.174,0.077 0.1'
        '83,0.094 0.199,0.105 0.213,0.108 0.236,0.103 0.253,0.083 0.256,0.058 0.250,0.044 0.236,0.029 0.2'
        '19,0.024 0.213,0.010ZM-0.236,0.004 -0.219,0.004 -0.216,0.010 -0.225,0.024 -0.253,0.032 -0.267,0.'
        '052 -0.267,0.080 -0.256,0.097 -0.230,0.108 -0.205,0.103 -0.188,0.083 -0.185,0.058 -0.191,0.041 -'
        '0.180,0.027 -0.166,0.052 -0.166,0.080 -0.171,0.094 -0.191,0.117 -0.216,0.128 -0.236,0.128 -0.258'
        ',0.119 -0.281,0.097 -0.289,0.074 -0.287,0.049 -0.272,0.024 -0.258,0.013ZM0.143,-0.021 0.146,-0.0'
        '15 0.126,0.004 0.107,0.049 0.104,0.046 0.104,-0.018 0.107,-0.021ZM0.028,-0.077 0.003,-0.041 -0.0'
        '08,-0.041 -0.073,-0.063 -0.062,-0.074 -0.003,-0.108 0.003,-0.108 0.008,-0.097Z'
    ),
    '622.2/black': (
        'M0.396,-0.303 -0.304,0.392 -0.284,0.406 0.408,-0.283ZM0.371,-0.333 -0.335,0.367 -0.326,0.375 -0.'
        '315,0.381 0.385,-0.317ZM0.343,-0.361 0.099,-0.123 -0.363,0.339 -0.346,0.356 0.357,-0.345ZM0.324,'
        '-0.381 0.312,-0.389 -0.388,0.308 -0.374,0.328 0.329,-0.373ZM0.284,-0.412 0.279,-0.412 -0.413,0.2'
        '77 -0.399,0.297 0.298,-0.401Z'
    ),
    '622.2/grey': (
        'M-0.237,0.322 -0.245,0.317 -0.315,0.384 -0.321,0.381 -0.310,0.389 -0.304,0.389ZM-0.268,0.297 -0.'
        '276,0.291 -0.346,0.359 -0.335,0.364ZM-0.301,0.263 -0.371,0.331 -0.366,0.336 -0.296,0.269ZM0.312,'
        '-0.162 0.304,-0.168 0.296,-0.168 0.018,0.109 0.130,0.109 0.136,0.115 0.141,0.137 0.158,0.154 0.1'
        '81,0.162 0.200,0.162 0.223,0.154 0.237,0.140 0.248,0.109 0.312,0.109 0.315,0.106 0.315,-0.154ZM0'
        '.183,0.081 0.203,0.084 0.217,0.104 0.211,0.120 0.197,0.132 0.178,0.129 0.164,0.112 0.167,0.095ZM'
        '0.254,-0.168 0.239,-0.168 -0.038,0.109 -0.024,0.112 -0.231,0.319ZM0.141,-0.168 0.127,-0.168 -0.1'
        '50,0.109 -0.136,0.109ZM0.029,-0.168 -0.133,-0.168 -0.144,-0.160 -0.144,-0.034 -0.147,-0.031 -0.1'
        '67,-0.031 -0.169,-0.034 -0.169,-0.112 -0.178,-0.120 -0.290,-0.120 -0.301,-0.115 -0.315,-0.090 -0'
        '.326,-0.014 -0.343,0.003 -0.343,0.022 -0.324,0.109 -0.298,0.109 -0.296,0.123 -0.287,0.140 -0.282'
        ',0.143 -0.262,0.123 -0.268,0.109 -0.265,0.095 -0.248,0.081 -0.234,0.081 -0.225,0.087ZM-0.284,-0.'
        '095 -0.223,-0.095 -0.220,-0.092 -0.220,-0.034 -0.223,-0.031 -0.296,-0.031 -0.298,-0.045 -0.296,-'
        '0.048 -0.293,-0.078ZM0.234,-0.221 -0.094,0.109 -0.080,0.109 0.197,-0.168 0.183,-0.171ZM0.410,-0.'
        '286 0.340,-0.213 0.354,-0.190 0.377,-0.140 0.396,-0.064 0.396,-0.048 0.399,-0.045 0.399,0.039 0.'
        '396,0.042 0.394,0.076 0.377,0.134 0.352,0.190 0.326,0.230 0.284,0.280 0.239,0.319 0.206,0.342 0.'
        '144,0.373 0.111,0.384 0.057,0.395 -0.038,0.398 -0.041,0.395 -0.091,0.389 -0.139,0.375 -0.167,0.3'
        '64 -0.211,0.339 -0.127,0.252 -0.282,0.409 -0.237,0.437 -0.189,0.459 -0.108,0.485 -0.055,0.490 -0'
        '.052,0.493 -0.018,0.493 -0.015,0.496 0.052,0.493 0.055,0.490 0.091,0.487 0.147,0.473 0.234,0.437'
        ' 0.307,0.389 0.380,0.319 0.424,0.258 0.466,0.171 0.489,0.090 0.492,0.056 0.494,0.053 0.494,0.017'
        ' 0.497,0.014 0.497,-0.025 0.494,-0.028 0.492,-0.081 0.475,-0.151 0.452,-0.210ZM0.388,-0.314 0.31'
        '8,-0.246 0.324,-0.238 0.396,-0.305ZM0.228,-0.328 -0.396,0.297 -0.391,0.311 -0.324,0.241 -0.324,0'
        '.235 -0.329,0.230 -0.259,0.160 -0.245,0.162 0.085,-0.168 0.071,-0.171ZM0.360,-0.347 0.293,-0.277'
        ' 0.298,-0.269 0.371,-0.336ZM0.332,-0.375 0.265,-0.305 0.270,-0.294 0.147,-0.171 0.338,-0.364ZM0.'
        '310,-0.392 0.301,-0.398 0.234,-0.331 0.239,-0.319 0.091,-0.171ZM0.276,-0.417 0.217,-0.451 0.136,'
        '-0.482 0.046,-0.499 -0.049,-0.499 -0.052,-0.496 -0.105,-0.490 -0.195,-0.462 -0.256,-0.431 -0.324'
        ',-0.384 -0.394,-0.311 -0.438,-0.244 -0.464,-0.190 -0.480,-0.143 -0.497,-0.062 -0.500,0.028 -0.49'
        '7,0.031 -0.497,0.056 -0.494,0.059 -0.494,0.076 -0.486,0.118 -0.458,0.199 -0.416,0.275 -0.346,0.2'
        '07 -0.346,0.202 -0.352,0.196 -0.382,0.129 -0.396,0.076 -0.399,0.042 -0.402,0.039 -0.402,-0.045 -'
        '0.399,-0.048 -0.396,-0.081 -0.377,-0.148 -0.354,-0.196 -0.324,-0.244 -0.293,-0.280 -0.256,-0.314'
        ' -0.189,-0.359 -0.139,-0.381 -0.060,-0.401 -0.038,-0.401 -0.035,-0.403 0.057,-0.401 0.141,-0.378'
        ' 0.200,-0.350 0.206,-0.345Z'
    ),
    '622.5': (
        'M0.258,0.128 0.253,0.133 0.253,0.150 0.261,0.156 0.272,0.156 0.281,0.147 0.281,0.133 0.275,0.128'
        'ZM0.076,0.128 0.070,0.133 0.070,0.150 0.079,0.156 0.096,0.153 0.098,0.133 0.093,0.128ZM0.250,0.0'
        '86 0.236,0.091 0.219,0.108 0.211,0.125 0.211,0.156 0.222,0.178 0.239,0.192 0.256,0.198 0.278,0.1'
        '98 0.303,0.187 0.317,0.170 0.323,0.156 0.323,0.128 0.315,0.108 0.292,0.088ZM0.247,0.103 0.278,0.'
        '100 0.287,0.103 0.303,0.119 0.309,0.133 0.309,0.150 0.303,0.164 0.289,0.178 0.275,0.184 0.256,0.'
        '184 0.244,0.178 0.230,0.164 0.225,0.153 0.225,0.131 0.233,0.114ZM0.067,0.086 0.053,0.091 0.031,0'
        '.117 0.028,0.156 0.037,0.176 0.056,0.192 0.073,0.198 0.096,0.198 0.121,0.187 0.135,0.170 0.140,0'
        '.156 0.140,0.128 0.132,0.108 0.110,0.088ZM0.070,0.100 0.096,0.100 0.107,0.105 0.121,0.119 0.126,'
        '0.131 0.126,0.150 0.121,0.164 0.107,0.178 0.093,0.184 0.073,0.184 0.062,0.178 0.048,0.164 0.042,'
        '0.153 0.045,0.122 0.056,0.108ZM0.365,-0.007 0.348,-0.010 0.323,-0.024 0.309,-0.038 0.287,-0.074 '
        '0.264,-0.094 0.225,-0.108 0.191,-0.108 0.171,-0.103 0.146,-0.088 0.124,-0.066 0.110,-0.044 0.084'
        ',-0.041 0.079,-0.046 0.076,-0.066 0.090,-0.074 0.090,-0.088 0.079,-0.114 0.062,-0.131 0.067,-0.1'
        '39 0.067,-0.153 0.056,-0.167 0.037,-0.167 0.025,-0.156 0.025,-0.136 0.031,-0.128 0.022,-0.117 0.'
        '020,-0.083 0.008,-0.074 -0.011,-0.072 -0.017,-0.063 -0.011,-0.055 0.008,-0.058 0.020,-0.063 0.02'
        '8,-0.060 0.003,-0.032 0.000,-0.024 0.000,0.029 -0.011,0.035 -0.008,0.044 -0.011,0.049 -0.017,0.0'
        '46 -0.020,0.018 -0.031,-0.027 -0.039,-0.046 -0.048,-0.055 -0.059,-0.055 -0.073,-0.046 -0.090,-0.'
        '052 -0.112,-0.052 -0.126,-0.046 -0.166,-0.044 -0.169,-0.041 -0.199,-0.046 -0.219,-0.063 -0.233,-'
        '0.086 -0.256,-0.111 -0.284,-0.128 -0.303,-0.150 -0.303,-0.128 -0.329,-0.105 -0.343,-0.080 -0.365'
        ',-0.058 -0.365,-0.041 -0.362,-0.038 -0.334,-0.038 -0.320,-0.052 -0.301,-0.055 -0.295,-0.049 -0.2'
        '92,-0.027 -0.298,-0.007 -0.298,0.027 -0.287,0.055 -0.295,0.088 -0.303,0.100 -0.301,0.105 -0.303,'
        '0.108 -0.303,0.122 -0.292,0.145 -0.289,0.176 -0.281,0.184 -0.278,0.192 -0.272,0.195 -0.272,0.209'
        ' -0.272,0.198 -0.264,0.170 -0.278,0.150 -0.278,0.105 -0.258,0.091 -0.256,0.094 -0.244,0.142 -0.2'
        '44,0.176 -0.250,0.184 -0.250,0.195 -0.228,0.190 -0.225,0.187 -0.228,0.181 -0.225,0.164 -0.230,0.'
        '153 -0.230,0.114 -0.213,0.072 -0.180,0.072 -0.177,0.069 -0.146,0.066 -0.129,0.088 -0.110,0.105 -'
        '0.135,0.153 -0.132,0.162 -0.138,0.173 -0.138,0.184 -0.118,0.176 -0.115,0.170 -0.118,0.164 -0.101'
        ',0.128 -0.084,0.108 -0.093,0.094 -0.090,0.091 -0.081,0.097 -0.067,0.114 -0.070,0.173 -0.079,0.18'
        '7 -0.079,0.192 -0.067,0.192 -0.053,0.187 -0.053,0.176 -0.048,0.170 -0.051,0.128 -0.045,0.111 -0.'
        '045,0.100 -0.070,0.072 -0.067,0.060 -0.048,0.063 -0.031,0.083 -0.020,0.083 -0.014,0.069 0.003,0.'
        '069 0.011,0.074 0.011,0.094 0.034,0.094 0.051,0.080 0.076,0.072 0.104,0.074 0.129,0.088 0.132,0.'
        '094 0.216,0.094 0.233,0.080 0.258,0.072 0.287,0.074 0.312,0.088 0.315,0.094 0.337,0.094 0.337,0.'
        '086 0.365,0.001ZM-0.062,-0.044 -0.056,-0.044 -0.048,-0.035 -0.042,-0.018 -0.042,0.032 -0.048,0.0'
        '44 -0.056,0.041 -0.051,0.021 -0.051,-0.004 -0.056,-0.024 -0.065,-0.035Z'
    ),
    '622.6': (
        'M-0.340,0.060 -0.323,0.074 -0.303,0.077 -0.289,0.072 -0.272,0.058 -0.258,0.035 -0.250,0.007 -0.2'
        '50,-0.035 -0.236,-0.058 -0.225,-0.066 -0.213,-0.069 -0.211,-0.063 -0.219,-0.041 -0.219,0.010 -0.'
        '205,0.046 -0.205,0.060 -0.208,0.069 -0.228,0.083 -0.228,0.167 -0.242,0.190 -0.256,0.184 -0.253,0'
        '.226 -0.228,0.223 -0.211,0.206 -0.213,0.178 -0.211,0.176 -0.208,0.136 -0.194,0.122 -0.191,0.103 '
        '-0.185,0.097 -0.140,0.077 -0.138,0.083 -0.149,0.103 -0.149,0.111 -0.132,0.142 -0.124,0.167 -0.11'
        '8,0.206 -0.096,0.212 -0.098,0.221 -0.093,0.237 -0.056,0.237 -0.056,0.226 -0.067,0.206 -0.090,0.1'
        '84 -0.098,0.181 -0.104,0.173 -0.107,0.139 -0.112,0.119 -0.112,0.111 -0.104,0.100 -0.098,0.080 -0'
        '.098,0.060 -0.084,0.044 -0.070,0.052 -0.062,0.052 -0.042,0.060 -0.014,0.066 0.008,0.066 0.011,0.'
        '069 0.067,0.066 0.098,0.058 0.107,0.060 0.104,0.066 0.107,0.094 0.090,0.122 0.087,0.150 0.084,0.'
        '153 0.084,0.176 0.073,0.195 0.073,0.206 0.084,0.215 0.073,0.235 0.081,0.237 0.112,0.237 0.121,0.'
        '232 0.118,0.221 0.101,0.195 0.101,0.173 0.143,0.105 0.143,0.088 0.152,0.072 0.160,0.063 0.166,0.'
        '066 0.233,0.128 0.247,0.156 0.250,0.176 0.256,0.181 0.242,0.195 0.242,0.201 0.253,0.223 0.261,0.'
        '226 0.275,0.204 0.281,0.173 0.256,0.125 0.256,0.114 0.247,0.094 0.194,0.041 0.191,0.032 0.199,0.'
        '007 0.199,-0.021 0.222,-0.058 0.230,-0.094 0.261,-0.074 0.258,-0.072 0.258,-0.058 0.270,-0.044 0'
        '.272,-0.049 0.284,-0.044 0.292,-0.046 0.298,-0.060 0.298,-0.077 0.292,-0.094 0.292,-0.119 0.289,'
        '-0.122 0.292,-0.153 0.284,-0.178 0.287,-0.181 0.301,-0.181 0.287,-0.190 0.289,-0.198 0.287,-0.20'
        '4 0.258,-0.192 0.208,-0.192 0.180,-0.184 0.157,-0.173 0.121,-0.145 0.101,-0.125 0.081,-0.128 0.0'
        '45,-0.156 0.045,-0.181 0.037,-0.226 0.031,-0.240 0.020,-0.251 0.034,-0.263 0.034,-0.279 0.045,-0'
        '.282 0.045,-0.285 0.037,-0.294 0.034,-0.305 0.025,-0.316 -0.003,-0.319 -0.017,-0.302 -0.017,-0.2'
        '77 -0.014,-0.263 -0.008,-0.254 -0.028,-0.237 -0.037,-0.221 -0.048,-0.178 -0.051,-0.139 -0.048,-0'
        '.136 -0.045,-0.094 -0.048,-0.091 -0.056,-0.097 -0.079,-0.103 -0.121,-0.105 -0.124,-0.103 -0.157,'
        '-0.100 -0.188,-0.086 -0.194,-0.088 -0.228,-0.088 -0.253,-0.083 -0.278,-0.060 -0.292,-0.035 -0.29'
        '8,-0.007 -0.298,0.018 -0.309,0.049 -0.326,0.060ZM0.039,-0.125 0.042,-0.128 0.059,-0.119 0.070,-0'
        '.105 0.056,-0.094Z'
    ),
    '622.8/black': (
        'M-0.138,-0.034 -0.153,-0.011 -0.169,0.093 -0.184,0.099 -0.197,0.116 -0.197,0.217 -0.191,0.229 -0.182'
        ',0.236 -0.18,0.305 -0.157,0.316 -0.138,0.314 -0.125,0.307 -0.119,0.301 -0.117,0.242 0.115,0.242 0.11'
        '7,0.303 0.142,0.316 0.161,0.314 0.174,0.307 0.18,0.301 0.18,0.236 0.188,0.227 0.195,0.213 0.195,0.12'
        '4 0.188,0.105 0.165,0.091 0.153,0.002 0.144,-0.023 0.129,-0.038 0.106,-0.046 -0.108,-0.046 -0.129,-0'
        '.04ZM-0.1,0.204 0.094,0.202 0.096,0.211 0.079,0.215 -0.085,0.215 -0.098,0.213ZM-0.1,0.173 0.094,0.17'
        '1 0.096,0.183 -0.096,0.185 -0.1,0.181ZM-0.1,0.145 -0.089,0.141 0.087,0.141 0.096,0.145 0.096,0.152 -'
        '0.098,0.154ZM0.14,0.116 0.157,0.12 0.165,0.128 0.169,0.139 0.165,0.156 0.148,0.168 0.132,0.166 0.123'
        ',0.16 0.117,0.149 0.119,0.131 0.129,0.12ZM-0.151,0.116 -0.132,0.12 -0.119,0.139 -0.123,0.156 -0.14,0'
        '.168 -0.157,0.166 -0.167,0.158 -0.172,0.149 -0.169,0.131ZM-0.142,0.053 -0.138,0.027 -0.129,0.008 -0.'
        '111,-0.006 -0.056,-0.013 0.054,-0.013 0.089,-0.011 0.113,-0.004 0.132,0.017 0.138,0.046 0.138,0.065 '
        '0.125,0.076 0.001,0.072 -0.129,0.076 -0.138,0.069ZM-0.085,-0.057 -0.075,-0.051 -0.047,-0.051 -0.035,'
        '-0.059 -0.043,-0.067 -0.075,-0.067ZM0.056,-0.074 0.052,-0.074 0.043,-0.065 0.054,-0.053 0.064,-0.063'
        'ZM0.188,-0.08 0.18,-0.082 0.079,-0.065 0.079,-0.057 0.098,-0.055 0.193,-0.065ZM-0.237,-0.063 -0.138,'
        '-0.053 -0.119,-0.053 -0.115,-0.061 -0.212,-0.084 -0.207,-0.078 -0.209,-0.072ZM-0.203,-0.131 -0.094,-'
        '0.069 -0.087,-0.08 -0.172,-0.141 -0.176,-0.141 -0.178,-0.131ZM0.062,-0.166 0.062,-0.149 0.085,-0.149'
        ' 0.085,-0.164ZM0.222,-0.177 0.079,-0.114 0.079,-0.101 0.083,-0.099 0.231,-0.137 0.216,-0.147ZM-0.231'
        ',-0.198 -0.249,-0.181 -0.249,-0.177 -0.212,-0.139 -0.197,-0.149 -0.226,-0.196ZM0.161,-0.211 0.159,-0'
        '.181 0.199,-0.183 0.199,-0.198ZM0.047,-0.086 0.052,-0.097 0.052,-0.114 0.043,-0.109 0.039,-0.114 0.0'
        '54,-0.143 0.054,-0.162 0.045,-0.154 0.033,-0.147 0.028,-0.149 0.035,-0.164 0.035,-0.183 0.028,-0.198'
        ' 0.014,-0.175 0.012,-0.177 0.016,-0.198 0.014,-0.217 0.007,-0.234 -0.005,-0.251 -0.001,-0.234 -0.003'
        ',-0.219 -0.012,-0.202 -0.022,-0.221 -0.028,-0.202 -0.028,-0.171 -0.031,-0.168 -0.037,-0.177 -0.043,-'
        '0.196 -0.049,-0.179 -0.052,-0.162 -0.049,-0.149 -0.041,-0.135 -0.043,-0.131 -0.064,-0.131 -0.075,-0.'
        '126 -0.081,-0.128 -0.191,-0.215 -0.212,-0.202 -0.092,-0.116 -0.079,-0.128 -0.058,-0.107 -0.043,-0.07'
        '6 -0.033,-0.065 -0.014,-0.055 -0.022,-0.082 -0.018,-0.084 -0.014,-0.08 -0.014,-0.105 -0.007,-0.116 -'
        '0.003,-0.109 0.003,-0.107 0.003,-0.099 -0.005,-0.086 0.005,-0.084 -0.009,-0.069 0.003,-0.067 -0.007,'
        '-0.057 0.005,-0.057 0.028,-0.065ZM-0.054,-0.267 -0.054,-0.259 -0.041,-0.242 -0.022,-0.242 -0.022,-0.'
        '267ZM0.184,-0.257 0.172,-0.269 0.165,-0.267 0.066,-0.192 0.073,-0.185ZM-0.167,-0.269 -0.092,-0.16 -0'
        '.083,-0.164 -0.134,-0.269 -0.138,-0.255ZM0.047,-0.274 0.033,-0.251 0.066,-0.24 0.079,-0.255 0.052,-0'
        '.274Z'
    ),
    '622.8/orange': (
        'M-0.271,-0.179 -0.271,-0.145 -0.266,-0.133 -0.256,-0.116 -0.243,-0.103 -0.245,-0.069 -0.241,-0.055 -'
        '0.231,-0.036 -0.216,-0.021 -0.188,-0.008 -0.157,-0.008 -0.148,-0.025 -0.136,-0.038 -0.113,-0.048 0.1'
        '11,-0.048 0.134,-0.038 0.151,-0.017 0.153,-0.008 0.165,-0.008 0.195,-0.023 0.212,-0.051 0.235,-0.053'
        ' 0.249,-0.061 0.264,-0.08 0.268,-0.095 0.266,-0.122 0.254,-0.141 0.268,-0.168 0.268,-0.187 0.26,-0.2'
        '06 0.249,-0.217 0.237,-0.223 0.207,-0.223 0.205,-0.253 0.199,-0.265 0.184,-0.278 0.172,-0.282 0.151,'
        '-0.282 0.132,-0.274 0.129,-0.288 0.121,-0.307 0.104,-0.322 0.087,-0.328 0.064,-0.328 0.052,-0.324 0.'
        '028,-0.301 0.018,-0.32 0.005,-0.333 -0.02,-0.343 -0.052,-0.341 -0.071,-0.331 -0.081,-0.32 -0.092,-0.'
        '297 -0.094,-0.28 -0.123,-0.295 -0.151,-0.295 -0.174,-0.284 -0.193,-0.261 -0.197,-0.242 -0.201,-0.238'
        ' -0.226,-0.234 -0.241,-0.225 -0.262,-0.202ZM-0.087,-0.057 -0.075,-0.069 -0.043,-0.069 -0.033,-0.059 '
        '-0.045,-0.048 -0.077,-0.048ZM0.054,-0.078 0.068,-0.065 0.056,-0.051 0.039,-0.063ZM0.197,-0.065 0.191'
        ',-0.061 0.083,-0.051 0.077,-0.055 0.075,-0.065 0.083,-0.069 0.174,-0.084 0.188,-0.084ZM-0.241,-0.063'
        ' -0.212,-0.074 -0.212,-0.088 -0.119,-0.065 -0.113,-0.059 -0.121,-0.048 -0.239,-0.059ZM-0.207,-0.131 '
        '-0.178,-0.133 -0.178,-0.143 -0.174,-0.145 -0.089,-0.086 -0.085,-0.078 -0.096,-0.067ZM0.058,-0.166 0.'
        '085,-0.168 0.087,-0.149 0.06,-0.147ZM0.226,-0.177 0.218,-0.147 0.233,-0.139 0.233,-0.135 0.087,-0.09'
        '7 0.077,-0.099 0.073,-0.112 0.077,-0.116 0.22,-0.179ZM-0.228,-0.202 -0.195,-0.149 -0.209,-0.137 -0.2'
        '54,-0.179ZM0.159,-0.213 0.163,-0.215 0.197,-0.202 0.201,-0.198 0.201,-0.181 0.159,-0.179ZM0.052,-0.0'
        '88 0.045,-0.078 0.026,-0.061 0.009,-0.055 -0.007,-0.055 -0.009,-0.057 0.001,-0.067 -0.014,-0.069 0.0'
        '01,-0.082 -0.009,-0.084 0.001,-0.101 0.001,-0.107 -0.003,-0.105 -0.007,-0.114 -0.012,-0.103 -0.012,-'
        '0.08 -0.018,-0.08 -0.009,-0.055 -0.016,-0.053 -0.028,-0.059 -0.047,-0.078 -0.058,-0.103 -0.077,-0.12'
        '4 -0.089,-0.112 -0.216,-0.202 -0.195,-0.217 -0.191,-0.217 -0.079,-0.131 -0.043,-0.135 -0.054,-0.156 '
        '-0.052,-0.183 -0.043,-0.198 -0.031,-0.173 -0.031,-0.206 -0.022,-0.223 -0.012,-0.206 -0.005,-0.223 -0'
        '.005,-0.255 0.005,-0.242 0.016,-0.221 0.018,-0.192 0.014,-0.179 0.028,-0.2 0.037,-0.185 0.037,-0.16 '
        '0.033,-0.152 0.054,-0.164 0.056,-0.162 0.056,-0.141 0.041,-0.112 0.052,-0.118 0.056,-0.116ZM-0.056,-'
        '0.267 -0.022,-0.269 -0.02,-0.242 -0.041,-0.24 -0.056,-0.257ZM0.188,-0.257 0.186,-0.253 0.079,-0.185 '
        '0.073,-0.183 0.064,-0.192 0.071,-0.2 0.172,-0.274ZM-0.169,-0.274 -0.142,-0.259 -0.138,-0.261 -0.134,'
        '-0.272 -0.129,-0.267 -0.081,-0.168 -0.085,-0.16 -0.092,-0.158 -0.104,-0.173 -0.172,-0.269ZM0.047,-0.'
        '278 0.081,-0.255 0.066,-0.238 0.039,-0.244 0.028,-0.251Z'
    ),
    '625.1': (
        'M0.022,-0.291 0.006,-0.282 -0.008,-0.263 -0.011,-0.240 0.000,-0.209 -0.003,-0.206 -0.031,-0.204 '
        '-0.067,-0.187 -0.107,-0.142 -0.132,-0.094 -0.146,-0.046 -0.149,-0.018 -0.157,-0.010 -0.154,0.010'
        ' -0.124,0.027 -0.107,0.024 -0.104,0.018 -0.104,-0.004 -0.107,-0.007 -0.104,-0.046 -0.093,-0.072 '
        '-0.070,-0.097 -0.067,-0.094 -0.067,-0.060 -0.070,-0.058 -0.070,-0.038 -0.079,0.001 -0.093,0.041 '
        '-0.124,0.100 -0.152,0.139 -0.208,0.195 -0.208,0.201 -0.185,0.243 -0.174,0.257 -0.160,0.263 -0.14'
        '0,0.263 -0.138,0.265 -0.129,0.263 -0.129,0.257 -0.146,0.240 -0.152,0.209 -0.073,0.131 -0.039,0.0'
        '80 -0.025,0.049 -0.020,0.046 0.017,0.097 0.051,0.162 0.076,0.226 0.093,0.291 0.180,0.254 0.183,0'
        '.243 0.180,0.240 0.132,0.237 0.124,0.232 0.118,0.178 0.101,0.114 0.059,0.032 0.051,0.004 0.048,-'
        '0.046 0.053,-0.074 0.056,-0.077 0.076,-0.049 0.107,-0.021 0.138,-0.004 0.163,0.004 0.177,0.004 0'
        '.185,0.010 0.197,0.010 0.205,-0.004 0.208,-0.032 0.205,-0.035 0.188,-0.032 0.163,-0.044 0.143,-0'
        '.058 0.118,-0.086 0.104,-0.111 0.093,-0.147 0.073,-0.176 0.053,-0.195 0.076,-0.218 0.084,-0.240 '
        '0.081,-0.263 0.070,-0.279 0.051,-0.291Z'
    ),
    '675A/0': (
        'M-0.4802,-0.7035 -0.4912,-0.6925 -0.5,-0.6727 -0.5,0.6727 -0.4912,0.6903 -0.4758,0.7046 -0.456,0'
        '.7112 0.4538,0.7112 0.4703,0.7068 0.4791,0.7013 0.4923,0.687 0.4989,0.6694 0.4989,-0.6716 0.4945'
        ',-0.6859 0.4901,-0.6925 0.4791,-0.7035 0.4604,-0.7123 -0.4615,-0.7123Z'
    ),
    '675A/1': (
        'M-0.5,0.6727 -0.5,0.7112 -0.4538,0.7112 -0.4626,0.7112 -0.4802,0.7024 -0.4912,0.6914 -0.4978,0.6'
        '804ZM0.4989,0.6694 0.4945,0.6848 0.4802,0.7013 0.4637,0.7101 0.4516,0.7112 0.4989,0.7112ZM-0.417'
        '5,0.6859 0.4571,0.6848 0.4703,0.6749 0.4747,0.6617 0.4736,0.3031 0.4692,0.2943 0.4648,0.2899 0.4'
        '549,0.2855 -0.0171,0.2855ZM-0.0358,0.2855 -0.0402,0.2855 -0.4417,0.6859 -0.4362,0.6859ZM-0.0578,'
        '0.2855 -0.0644,0.2855 -0.4615,0.6837 -0.4582,0.6848ZM-0.082,0.2855 -0.0875,0.2855 -0.4725,0.6694'
        ' -0.4714,0.6749ZM-0.1051,0.2855 -0.1117,0.2855 -0.4758,0.6496 -0.4758,0.6551ZM-0.1293,0.2855 -0.'
        '456,0.2855 -0.4659,0.2899 -0.4703,0.2943 -0.4747,0.3031 -0.4758,0.3141 -0.4758,0.632ZM-0.0149,-0'
        '.5462 -0.0347,-0.5451 -0.0677,-0.5396 -0.0985,-0.5319 -0.1293,-0.5209 -0.1623,-0.5044 -0.1964,-0'
        '.4824 -0.2272,-0.4571 -0.2547,-0.4285 -0.2767,-0.3999 -0.2921,-0.3746 -0.3086,-0.3405 -0.3185,-0'
        '.313 -0.3273,-0.2789 -0.3317,-0.2503 -0.3328,-0.192 -0.3273,-0.1469 -0.3185,-0.1128 -0.3031,-0.0'
        '732 -0.2921,-0.0512 -0.2756,-0.0248 -0.258,-0.0017 -0.2294,0.0292 -0.2118,0.0446 -0.1821,0.0666 '
        '-0.1623,0.0787 -0.1249,0.0963 -0.1007,0.1051 -0.0677,0.1139 -0.038,0.1183 0.0039,0.1205 0.0391,0'
        '.1183 0.0677,0.1139 0.0974,0.1062 0.1282,0.0952 0.1623,0.0787 0.1876,0.0633 0.2173,0.0402 0.2437'
        ',0.0149 0.2602,-0.0039 0.2778,-0.0281 0.2932,-0.0534 0.3086,-0.0842 0.3196,-0.115 0.3273,-0.1447'
        ' 0.3328,-0.1821 0.3339,-0.2206 0.3328,-0.2437 0.3273,-0.2811 0.3196,-0.3108 0.3086,-0.3416 0.292'
        '1,-0.3746 0.2767,-0.3999 0.258,-0.4252 0.2129,-0.4703 0.1843,-0.4912 0.1623,-0.5044 0.1238,-0.52'
        '31 0.0996,-0.5319 0.0677,-0.5396 0.0347,-0.5451ZM-0.4648,-0.6837 -0.4736,-0.6727 -0.4758,-0.654 '
        '-0.4758,0.2393 -0.4714,0.2514 -0.4648,0.258 -0.4516,0.2624 0.4505,0.2624 0.4571,0.2613 0.4692,0.'
        '2525 0.4747,0.2382 0.4747,-0.6639 0.4692,-0.6782 0.4637,-0.6837 0.4538,-0.6881 -0.4516,-0.6881ZM'
        '-0.0413,-0.6298 0.0402,-0.6298 0.0721,-0.6254 0.1106,-0.6166 0.1447,-0.6056 0.181,-0.5902 0.225,'
        '-0.5649 0.2646,-0.5363 0.2899,-0.5132 0.3196,-0.4813 0.3427,-0.4516 0.3669,-0.412 0.3911,-0.3592'
        ' 0.4021,-0.3251 0.4109,-0.2877 0.4153,-0.2547 0.4175,-0.2151 0.4153,-0.1711 0.4109,-0.1381 0.402'
        '1,-0.1007 0.3911,-0.0666 0.3779,-0.0358 0.3614,-0.0039 0.3416,0.027 0.3196,0.0556 0.2987,0.0787 '
        '0.2668,0.1084 0.2129,0.1469 0.1821,0.1634 0.1458,0.1788 0.1084,0.1909 0.0754,0.1986 0.0336,0.204'
        '1 -0.0105,0.2052 -0.0457,0.203 -0.0776,0.1986 -0.1106,0.1909 -0.1348,0.1832 -0.1744,0.1678 -0.21'
        '29,0.148 -0.2415,0.1293 -0.2723,0.1051 -0.3075,0.071 -0.324,0.0523 -0.3548,0.0094 -0.3724,-0.021'
        '5 -0.3933,-0.0666 -0.4043,-0.1007 -0.4131,-0.1414 -0.4175,-0.1744 -0.4175,-0.2514 -0.412,-0.291 '
        '-0.4043,-0.3251 -0.3933,-0.3592 -0.3779,-0.3944 -0.3537,-0.4373 -0.324,-0.478 -0.3075,-0.4967 -0'
        '.2679,-0.5352 -0.2305,-0.5627 -0.1909,-0.5858 -0.1546,-0.6023 -0.1194,-0.6144 -0.0743,-0.6254ZM0'
        '.4593,-0.7123 0.4626,-0.7123 0.4769,-0.7057 0.4901,-0.6936 0.4967,-0.6826 0.4989,-0.6716 0.4989,'
        '-0.7123ZM-0.4604,-0.7123 -0.5,-0.7123 -0.5,-0.6705 -0.4978,-0.6815 -0.4912,-0.6936 -0.478,-0.705'
        '7 -0.4725,-0.709Z'
    ),
    '675A/2': (
        'M-0.0171,-0.6298 -0.0721,-0.6243 -0.0974,-0.6188 -0.148,-0.6034 -0.1799,-0.5902 -0.2404,-0.555 -'
        '0.2701,-0.5319 -0.302,-0.5011 -0.3416,-0.4538 -0.3614,-0.423 -0.379,-0.3889 -0.3922,-0.3581 -0.4'
        '032,-0.324 -0.412,-0.2822 -0.4164,-0.2481 -0.4175,-0.2019 -0.4164,-0.1777 -0.412,-0.1436 -0.4043'
        ',-0.1062 -0.3922,-0.0677 -0.3779,-0.0347 -0.3603,-0.0017 -0.3394,0.0303 -0.3218,0.0534 -0.2888,0'
        '.0886 -0.247,0.1238 -0.214,0.1458 -0.1788,0.1645 -0.1469,0.1777 -0.1128,0.1887 -0.0754,0.1975 -0'
        '.0435,0.2019 0.0028,0.2041 0.0413,0.2019 0.0787,0.1964 0.1183,0.1865 0.1744,0.1656 0.2107,0.1469'
        ' 0.2404,0.1271 0.269,0.1051 0.2943,0.082 0.3174,0.0567 0.3394,0.0281 0.3537,0.0061 0.3779,-0.039'
        '1 0.39,-0.0677 0.401,-0.1018 0.4098,-0.1403 0.4142,-0.1733 0.4153,-0.2338 0.4098,-0.2855 0.4021,'
        '-0.3196 0.39,-0.3581 0.3768,-0.39 0.3603,-0.4219 0.3405,-0.4527 0.3174,-0.4824 0.2778,-0.5231 0.'
        '2426,-0.5517 0.2107,-0.5726 0.1755,-0.5913 0.1436,-0.6045 0.1095,-0.6155 0.0699,-0.6243 0.038,-0'
        '.6287ZM-0.0369,-0.5462 0.0369,-0.5462 0.1007,-0.533 0.1304,-0.522 0.1612,-0.5066 0.1832,-0.4934 '
        '0.2107,-0.4736 0.2338,-0.4527 0.2613,-0.423 0.2789,-0.3988 0.2954,-0.3713 0.3097,-0.3427 0.3207,'
        '-0.3119 0.3284,-0.2822 0.3339,-0.2481 0.3339,-0.1777 0.3284,-0.1436 0.3207,-0.1139 0.3097,-0.083'
        '1 0.2954,-0.0545 0.2778,-0.0259 0.2591,-0.0006 0.2393,0.0215 0.2129,0.0457 0.1898,0.0633 0.1612,'
        '0.0809 0.1293,0.0963 0.0985,0.1073 0.0688,0.115 0.0314,0.1205 -0.0314,0.1205 -0.0688,0.115 -0.09'
        '85,0.1073 -0.1337,0.0941 -0.1612,0.0809 -0.1909,0.0622 -0.2096,0.0479 -0.2349,0.0259 -0.2558,0.0'
        '028 -0.2778,-0.0259 -0.2954,-0.0545 -0.3086,-0.082 -0.3196,-0.1117 -0.3284,-0.1458 -0.3328,-0.17'
        '44 -0.335,-0.2085 -0.3328,-0.2514 -0.3284,-0.2811 -0.3196,-0.3141 -0.3086,-0.3438 -0.2954,-0.371'
        '3 -0.2767,-0.4021 -0.2591,-0.4252 -0.2404,-0.4461 -0.2118,-0.4725 -0.1612,-0.5066 -0.1271,-0.523'
        '1 -0.0996,-0.533 -0.0688,-0.5407Z'
    ),
    '675A/3': (
        'M-0.3482,0.5979 -0.3515,0.5968 -0.3746,0.6199 -0.3713,0.621ZM-0.3647,0.5858 -0.3878,0.6089 -0.38'
        '56,0.6111 -0.3625,0.5891ZM-0.3867,0.5616 -0.4098,0.5836 -0.4087,0.5869 -0.3856,0.5649ZM-0.2206,0'
        '.423 -0.2261,0.4241 -0.2558,0.4538 -0.258,0.4615 -0.2888,0.4923 -0.2899,0.4901 -0.2855,0.4835 -0'
        '.3493,0.5473 -0.3449,0.5484 -0.3735,0.577 -0.3768,0.5748 -0.3988,0.5968 -0.3966,0.6001 -0.4285,0'
        '.632ZM-0.313,0.5165 -0.3196,0.5231 -0.324,0.522 -0.3152,0.5154ZM-0.1315,0.3999 -0.1557,0.4241 -0'
        '.1469,0.4428 -0.1425,0.4604 -0.1403,0.4813 -0.1414,0.5033 -0.1458,0.5242 -0.1524,0.5407 -0.1645,'
        '0.5627 -0.1755,0.5759 -0.1909,0.5902 -0.2063,0.6012 -0.2327,0.6133 -0.2558,0.6188 -0.2811,0.6199'
        ' -0.2954,0.6188 -0.3152,0.6144 -0.3372,0.6056 -0.3603,0.6298 -0.3284,0.6441 -0.302,0.6507 -0.249'
        '2,0.6507 -0.2228,0.6441 -0.1887,0.6287 -0.1744,0.6188 -0.1557,0.6023 -0.1414,0.5858 -0.1326,0.57'
        '26 -0.1205,0.5484 -0.1139,0.5297 -0.1095,0.5077 -0.1084,0.4769 -0.1128,0.4461 -0.1216,0.4197ZM-0'
        '.1403,0.3867 -0.1634,0.4087 -0.1623,0.412 -0.1392,0.3889ZM-0.1975,0.3779 -0.28,0.4604 -0.2822,0.'
        '456 -0.3735,0.5473 -0.368,0.5473ZM-0.1612,0.3636 -0.1634,0.3614 -0.1865,0.3845 -0.1832,0.3856ZM-'
        '0.1876,0.3427 -0.2173,0.3284 -0.2503,0.3196 -0.3009,0.3196 -0.3372,0.3295 -0.3603,0.3405 -0.3779'
        ',0.3526 -0.3944,0.3669 -0.4076,0.3823 -0.4197,0.3999 -0.4307,0.4219 -0.4373,0.4406 -0.4417,0.462'
        '6 -0.4417,0.5088 -0.4351,0.5363 -0.4175,0.5737 -0.3944,0.5506 -0.4043,0.5286 -0.4098,0.5044 -0.4'
        '109,0.4802 -0.4098,0.4659 -0.4054,0.4461 -0.3988,0.4296 -0.3867,0.4076 -0.3669,0.3856 -0.3548,0.'
        '3757 -0.3372,0.3647 -0.3185,0.357 -0.2943,0.3515 -0.2569,0.3515 -0.2327,0.357 -0.2107,0.3669ZM-0'
        '.0578,0.2855 -0.148,0.3757 -0.1524,0.3735 -0.1744,0.3966 -0.1722,0.3988ZM-0.1117,0.2855 -0.2305,'
        '0.4043 -0.2008,0.3746 -0.1964,0.3757 -0.1733,0.3526 -0.1766,0.3504Z'
    ),
    '675A/4': (
        'M-0.4802,0.2701 -0.4802,0.6892 -0.0017,0.6892 -0.0017,0.687 -0.4186,0.6859 -0.016,0.2833 -0.0017'
        ',0.2833 -0.0017,0.2701ZM-0.0336,0.2844 -0.4362,0.687 -0.4428,0.6859 -0.0402,0.2844ZM-0.0567,0.28'
        '44 -0.4582,0.6859 -0.4626,0.6837 -0.0644,0.2844ZM-0.082,0.2833 -0.0809,0.2855 -0.4714,0.676 -0.4'
        '747,0.6705 -0.0875,0.2844ZM-0.1051,0.2833 -0.104,0.2855 -0.4758,0.6562 -0.4769,0.6496 -0.1117,0.'
        '2844ZM-0.1293,0.2833 -0.1282,0.2855 -0.4758,0.6331 -0.4769,0.3097 -0.4725,0.2954 -0.4659,0.2888 '
        '-0.4571,0.2844 -0.4494,0.2833Z'
    ),
    '770': (
        'M-0.27,0.141 -0.27,0.186 -0.254,0.188 -0.254,0.297 -0.27,0.3 -0.27,0.344 -0.254,0.346 -0.254,0.3'
        '86 -0.183,0.386 -0.18,0.344 -0.145,0.346 -0.145,0.386 -0.076,0.386 -0.076,0.349 -0.071,0.344 -0.'
        '036,0.346 -0.036,0.386 0.033,0.386 0.036,0.344 0.069,0.344 0.074,0.349 0.074,0.386 0.143,0.386 0'
        '.145,0.344 0.178,0.344 0.183,0.349 0.183,0.386 0.252,0.386 0.252,0.346 0.27,0.344 0.27,0.3 0.252'
        ',0.297 0.252,0.188 0.27,0.186 0.27,0.141 0.252,0.139 0.252,0.117 0.216,0.072 0.183,0.115 0.183,0'
        '.137 0.178,0.141 0.145,0.141 0.14,0.112 0.107,0.072 0.074,0.115 0.074,0.137 0.069,0.141 0.036,0.'
        '141 0.033,0.115 0,0.072 -0.033,0.112 -0.038,0.141 -0.071,0.141 -0.076,0.137 -0.076,0.115 -0.109,'
        '0.072 -0.145,0.117 -0.147,0.141 -0.18,0.141 -0.183,0.117 -0.218,0.072 -0.254,0.117 -0.254,0.139Z'
        'M0.145,0.186 0.178,0.186 0.183,0.19 0.183,0.295 0.178,0.3 0.143,0.297ZM0.036,0.186 0.069,0.186 0'
        '.074,0.19 0.074,0.295 0.069,0.3 0.033,0.297ZM-0.071,0.186 -0.036,0.188 -0.038,0.3 -0.071,0.3 -0.'
        '076,0.295 -0.076,0.19ZM-0.18,0.186 -0.145,0.188 -0.147,0.3 -0.183,0.297Z'
    ),
    '771': (
        'M-0.081,-0.101 -0.104,-0.075 -0.112,-0.039 -0.106,-0.003 -0.09,0.021 -0.07,0.037 -0.052,0.043 -0'
        '.019,0.046 -0.001,0.041 0.026,0.057 0.066,0.059 0.086,0.072 0.106,0.077 0.126,0.075 0.153,0.059 '
        '0.159,0.059 0.173,0.072 0.173,0.11 0.168,0.115 0.157,0.115 0.161,0.144 0.032,0.146 0.03,0.128 0.'
        '023,0.119 0.014,0.115 -0.026,0.115 -0.035,0.121 -0.041,0.146 -0.137,0.146 -0.139,0.11 -0.251,0.1'
        '1 -0.251,0.159 -0.215,0.161 -0.217,0.217 -0.277,0.217 -0.277,0.313 -0.262,0.315 -0.259,0.344 -0.'
        '251,0.362 -0.235,0.378 -0.222,0.384 -0.179,0.384 -0.164,0.375 -0.148,0.357 -0.141,0.342 -0.141,0'
        '.317 -0.135,0.313 -0.128,0.351 -0.106,0.378 -0.084,0.386 -0.059,0.386 -0.041,0.38 -0.023,0.364 -'
        '0.012,0.342 -0.012,0.317 -0.006,0.313 0.001,0.351 0.023,0.378 0.046,0.386 0.07,0.386 0.088,0.38 '
        '0.106,0.364 0.117,0.342 0.117,0.317 0.121,0.313 0.133,0.313 0.135,0.317 0.126,0.326 0.119,0.349 '
        '0.124,0.366 0.139,0.382 0.157,0.386 0.17,0.384 0.19,0.369 0.197,0.353 0.206,0.373 0.217,0.382 0.'
        '237,0.386 0.257,0.38 0.268,0.369 0.273,0.357 0.273,0.337 0.259,0.317 0.262,0.313 0.273,0.313 0.2'
        '73,0.264 0.253,0.262 0.253,0.146 0.222,0.144 0.226,0.115 0.21,0.112 0.21,0.081 0.197,0.032 0.177'
        ',-0.006 0.155,-0.03 0.139,-0.041 0.126,-0.046 0.106,-0.077 0.077,-0.095 0.052,-0.099 0.028,-0.09'
        '5 0.01,-0.108 -0.014,-0.117 -0.048,-0.117ZM0.184,0.313 0.213,0.315 0.204,0.326 0.197,0.344 0.188'
        ',0.324 0.182,0.317Z'
    ),
    '827.1/0': (
        'M-0.5,0.4505 -0.5,0.5081 -0.4442,0.5081 -0.4586,0.5063 -0.4784,0.4955 -0.5,0.4631ZM0.4982,0.4487'
        ' 0.4982,0.4631 0.4874,0.4847 0.4712,0.4991 0.4532,0.5081 0.4424,0.5081 0.4982,0.5081ZM-0.2302,-0'
        '.4182 -0.2302,0.1538 -0.1331,0.1538 -0.1313,-0.1052 0.1295,-0.1052 0.1313,0.1538 0.2302,0.1538 0'
        '.2302,-0.4182 0.1313,-0.4182 0.1295,-0.1915 -0.1313,-0.1915 -0.1331,-0.4182ZM-0.4748,-0.4847 -0.'
        '482,-0.4775 -0.4892,-0.4613 -0.491,-0.4487 -0.491,0.4469 -0.4892,0.4595 -0.4712,0.4865 -0.455,0.'
        '4955 -0.4317,0.5009 0.4299,0.5009 0.4478,0.4973 0.4676,0.4883 0.4784,0.4775 0.4874,0.4595 0.4892'
        ',0.4469 0.4892,-0.4469 0.4874,-0.4595 0.4802,-0.4757 0.464,-0.4919 0.4496,-0.4991 0.4371,-0.5009'
        ' -0.4406,-0.5009 -0.4514,-0.4991ZM-0.4532,-0.4739 -0.4388,-0.4793 0.4371,-0.4793 0.446,-0.4775 0'
        '.4604,-0.4649 0.4676,-0.4487 0.4676,0.4469 0.4658,0.4559 0.4568,0.4685 0.4353,0.4775 -0.4371,0.4'
        '775 -0.4496,0.4739 -0.4604,0.4667 -0.4694,0.4487 -0.4694,-0.4487 -0.4676,-0.4577ZM0.4406,-0.5099'
        ' 0.455,-0.5099 0.464,-0.5027 0.4712,-0.5009 0.4892,-0.4829 0.4982,-0.4649 0.4982,-0.4505 0.4982,'
        '-0.5099ZM-0.4442,-0.5099 -0.5,-0.5099 -0.5,-0.4523 -0.5,-0.4649 -0.4892,-0.4865 -0.4604,-0.5081Z'
    ),
    '953.1': (
        'M-0.395,-0.002 -0.395,0.117 -0.331,0.117 -0.329,0.131 -0.291,0.131 -0.281,0.151 -0.269,0.157 -0.'
        '255,0.157 -0.243,0.151 -0.234,0.131 -0.2,0.131 -0.19,0.151 -0.178,0.157 -0.164,0.157 -0.152,0.15'
        '1 -0.142,0.131 0.14,0.131 0.148,0.149 0.162,0.157 0.176,0.157 0.188,0.151 0.198,0.131 0.232,0.13'
        '1 0.238,0.147 0.251,0.157 0.267,0.157 0.281,0.149 0.289,0.131 0.327,0.131 0.329,0.117 0.393,0.11'
        '7 0.393,-0.002 0.371,-0.089 0.361,-0.103 0.349,-0.107 0.09,-0.107 0.077,-0.119 0.029,-0.119 0.02'
        '7,-0.121 0.082,-0.161 0.084,-0.165 0.023,-0.207 0.017,-0.213 0.017,-0.229 0.009,-0.237 -0.013,-0'
        '.237 -0.019,-0.229 -0.019,-0.213 -0.025,-0.207 -0.086,-0.165 -0.077,-0.155 -0.035,-0.127 -0.029,'
        '-0.121 -0.031,-0.119 -0.079,-0.119 -0.092,-0.107 -0.359,-0.105 -0.371,-0.095ZM0.313,-0.07 0.339,'
        '-0.072 0.347,-0.066 0.359,-0.02 0.359,-0.008 0.353,-0.002 0.315,-0.002 0.309,-0.008 0.309,-0.066'
        'ZM0.243,-0.072 0.277,-0.072 0.285,-0.064 0.285,0.095 0.279,0.101 0.24,0.101 0.236,0.095 0.236,-0'
        '.064ZM0.178,-0.072 0.212,-0.072 0.22,-0.066 0.22,0.095 0.214,0.101 0.176,0.101 0.17,0.095 0.17,-'
        '0.064ZM0.063,-0.066 0.071,-0.072 0.144,-0.072 0.152,-0.06 0.15,-0.008 0.144,-0.002 0.069,-0.002 '
        '0.063,-0.008ZM-0.045,-0.066 -0.037,-0.072 0.039,-0.07 0.043,-0.066 0.043,-0.008 0.037,-0.002 -0.'
        '039,-0.002 -0.045,-0.008ZM-0.152,-0.066 -0.146,-0.072 -0.069,-0.07 -0.065,-0.064 -0.065,-0.008 -'
        '0.071,-0.002 -0.146,-0.002 -0.154,-0.012ZM-0.214,-0.072 -0.18,-0.072 -0.172,-0.064 -0.172,0.095 '
        '-0.178,0.101 -0.216,0.101 -0.222,0.095 -0.222,-0.066ZM-0.279,-0.072 -0.245,-0.072 -0.238,-0.066 '
        '-0.238,0.095 -0.241,0.101 -0.281,0.101 -0.287,0.095 -0.287,-0.064ZM-0.341,-0.072 -0.319,-0.072 -'
        '0.311,-0.066 -0.311,-0.008 -0.317,-0.002 -0.355,-0.002 -0.361,-0.008 -0.361,-0.018 -0.349,-0.066'
        'ZM-0.003,-0.207 0.013,-0.199 0.061,-0.163 0.001,-0.121 -0.007,-0.123 -0.063,-0.163Z'
    ),
    '958/0': (
        'M0.4987,0.9075 0.4975,0.9163 0.4911,0.9303 0.4772,0.943 0.4683,0.948 0.4594,0.9493 0.4987,0.9493'
        'ZM-0.5,0.9075 -0.5,0.9493 -0.462,0.9493 -0.4785,0.9442 -0.4937,0.929 -0.4987,0.9176ZM-0.334,0.31'
        '69 -0.4265,0.3929 -0.4252,0.3967 -0.3973,0.4297 -0.3048,0.3523 -0.3048,0.3498ZM-0.1958,0.2003 -0'
        '.2883,0.2776 -0.2871,0.2814 -0.2592,0.3143 -0.1667,0.2357ZM-0.0577,0.0837 -0.1502,0.1622 -0.121,'
        '0.1977 -0.0285,0.1204 -0.0298,0.1166ZM0.0805,-0.0317 -0.012,0.0456 -0.012,0.0482 0.0171,0.0811 0'
        '.1096,0.0038ZM0.2186,-0.147 0.1261,-0.0697 0.1553,-0.0342 0.249,-0.1128ZM-0.064,-0.2586 -0.064,-'
        '0.2395 -0.0589,-0.2256 -0.0425,-0.2091 -0.0209,-0.2028 -0.0082,-0.2041 0.0082,-0.2117 0.0158,-0.'
        '218 0.0234,-0.2307 0.026,-0.2383 0.026,-0.2598 0.0209,-0.2725 0.0082,-0.2864 0.0095,-0.289 0.055'
        '1,-0.2586 0.0602,-0.2535 0.0602,-0.2433 0.0627,-0.2383 0.0716,-0.2307 0.083,-0.2307 0.0856,-0.22'
        '69 0.0817,-0.2256 0.0817,-0.2193 0.0856,-0.2193 0.0906,-0.2155 0.102,-0.2193 0.102,-0.2256 0.094'
        '4,-0.2256 0.0906,-0.2307 0.097,-0.2433 0.0995,-0.2446 0.102,-0.2421 0.1046,-0.2294 0.1109,-0.219'
        '3 0.1236,-0.2091 0.1439,-0.2028 0.1616,-0.2053 0.1755,-0.2129 0.1844,-0.2218 0.192,-0.2421 0.190'
        '7,-0.2624 0.1857,-0.2738 0.1768,-0.2839 0.1603,-0.2928 0.1362,-0.294 0.1299,-0.2915 0.1122,-0.32'
        '07 0.1147,-0.3295 0.1236,-0.3333 0.1261,-0.3371 0.1261,-0.3435 0.0843,-0.3435 0.0817,-0.3384 0.0'
        '856,-0.3346 0.102,-0.3308 0.0982,-0.3207 0.0184,-0.3207 0.0171,-0.3219 0.0196,-0.3321 0.0133,-0.'
        '3409 0.0323,-0.3422 0.0323,-0.3549 0.0095,-0.3549 0.0019,-0.3511 -0.0006,-0.3473 -0.0006,-0.3371'
        ' 0.007,-0.3283 -0.0019,-0.294 -0.0285,-0.294 -0.0399,-0.2902 -0.0539,-0.2788ZM0.0741,-0.2598 0.0'
        '83,-0.2598 0.0906,-0.2522 0.0894,-0.2433 0.0805,-0.237 0.0741,-0.2383 0.0678,-0.2446 0.0678,-0.2'
        '522ZM0.1248,-0.2712 0.1362,-0.2548 0.135,-0.2535 0.116,-0.2548 0.1198,-0.2649ZM0.0589,-0.2712 0.'
        '064,-0.2725 0.0665,-0.2674 0.0653,-0.2662ZM0.1413,-0.2801 0.1527,-0.2801 0.1654,-0.2738 0.1743,-'
        '0.2636 0.1781,-0.2535 0.1781,-0.2446 0.1717,-0.2307 0.1641,-0.2231 0.1527,-0.218 0.1413,-0.218 0'
        '.1312,-0.2218 0.121,-0.2307 0.116,-0.2408 0.1185,-0.2446 0.1502,-0.2446 0.1527,-0.2471 0.1527,-0'
        '.2522 0.1375,-0.2763ZM-0.0247,-0.2801 -0.0133,-0.2801 -0.007,-0.2763 -0.012,-0.2624 -0.0171,-0.2'
        '56 -0.0234,-0.2522 -0.0222,-0.2446 -0.0133,-0.2446 -0.0082,-0.2471 -0.0019,-0.2535 0.0019,-0.266'
        '2 0.0044,-0.2687 0.007,-0.2674 0.012,-0.256 0.012,-0.2408 0.0082,-0.2332 -0.0032,-0.2218 -0.0133'
        ',-0.218 -0.0247,-0.218 -0.0349,-0.2218 -0.045,-0.2319 -0.0501,-0.2446 -0.0488,-0.2586 -0.045,-0.'
        '2662 -0.0361,-0.275ZM0.1071,-0.3042 0.1185,-0.2852 0.1071,-0.2725 0.1033,-0.2649 0.102,-0.256 0.'
        '0982,-0.2535 0.0919,-0.2636 0.0919,-0.2674 0.1046,-0.3016ZM0.0133,-0.308 0.0919,-0.3093 0.0932,-'
        '0.3042 0.0805,-0.27 0.0754,-0.2674 0.0716,-0.2712 0.0767,-0.2725 0.0767,-0.2801 0.0564,-0.2801 0'
        '.0564,-0.275 0.0539,-0.2738 0.0133,-0.3029ZM-0.4075,-0.251 -0.4049,-0.2307 -0.3986,-0.2193 -0.38'
        '72,-0.2091 -0.3707,-0.2028 -0.3593,-0.2028 -0.3441,-0.2079 -0.3365,-0.2129 -0.3251,-0.2269 -0.32'
        '26,-0.2357 -0.3226,-0.2573 -0.3276,-0.2687 -0.3365,-0.2788 -0.3327,-0.2801 -0.3238,-0.2687 -0.31'
        '75,-0.251 -0.3175,-0.237 -0.315,-0.2319 -0.3086,-0.2269 -0.3023,-0.2243 -0.225,-0.2243 -0.2098,-'
        '0.2091 -0.1984,-0.2041 -0.1831,-0.2028 -0.1717,-0.2053 -0.1603,-0.2117 -0.154,-0.218 -0.1464,-0.'
        '2307 -0.1451,-0.2433 -0.1426,-0.2459 -0.1362,-0.2459 -0.1362,-0.2548 -0.1413,-0.27 -0.1565,-0.28'
        '77 -0.1667,-0.294 -0.1667,-0.2978 -0.1705,-0.3042 -0.2148,-0.3054 -0.2186,-0.3181 -0.2427,-0.343'
        '5 -0.2655,-0.3523 -0.2655,-0.3587 -0.263,-0.3612 -0.263,-0.3739 -0.2731,-0.384 -0.2833,-0.384 -0'
        '.2883,-0.3815 -0.2947,-0.3739 -0.2959,-0.365 -0.2921,-0.3638 -0.2921,-0.3523 -0.2871,-0.346 -0.2'
        '833,-0.346 -0.282,-0.3422 -0.2909,-0.327 -0.3074,-0.3131 -0.3124,-0.3156 -0.3035,-0.3587 -0.3074'
        ',-0.3599 -0.3226,-0.3321 -0.334,-0.3181 -0.3416,-0.3131 -0.3504,-0.3105 -0.3669,-0.3105 -0.3669,'
        '-0.2928 -0.3542,-0.2915 -0.3492,-0.2877 -0.3504,-0.2864 -0.3593,-0.289 -0.3707,-0.289 -0.3872,-0'
        '.2826 -0.4011,-0.2687ZM-0.1793,-0.27 -0.1705,-0.2649 -0.1654,-0.2586 -0.1616,-0.2484 -0.1629,-0.'
        '2383 -0.1743,-0.2243 -0.1819,-0.2218 -0.1946,-0.2218 -0.2034,-0.2269 -0.2085,-0.2332 -0.211,-0.2'
        '395 -0.211,-0.2535 -0.206,-0.2624 -0.2022,-0.2649 -0.1996,-0.2598 -0.1996,-0.256 -0.2034,-0.2522'
        ' -0.2022,-0.2383 -0.1971,-0.2319 -0.1907,-0.2294 -0.1793,-0.2307 -0.1743,-0.2345 -0.1705,-0.2408'
        ' -0.1705,-0.251 -0.173,-0.256 -0.1793,-0.2611 -0.1844,-0.2624 -0.1869,-0.2674 -0.1857,-0.2712ZM-'
        '0.3669,-0.2712 -0.3631,-0.2712 -0.3606,-0.2687 -0.3644,-0.2624 -0.3745,-0.2598 -0.3809,-0.251 -0'
        '.3809,-0.2408 -0.3758,-0.2332 -0.3682,-0.2294 -0.3606,-0.2294 -0.3542,-0.2319 -0.3479,-0.2421 -0'
        '.3479,-0.251 -0.3504,-0.256 -0.3466,-0.2611 -0.3428,-0.2586 -0.339,-0.2471 -0.3416,-0.2357 -0.34'
        '54,-0.2294 -0.358,-0.2218 -0.3745,-0.2231 -0.3859,-0.2332 -0.3885,-0.2383 -0.3885,-0.2548 -0.377'
        '1,-0.2674ZM-0.2161,-0.2814 -0.2148,-0.2788 -0.2237,-0.2687 -0.23,-0.2535 -0.2313,-0.2801ZM-0.261'
        '7,-0.3042 -0.2719,-0.289 -0.2769,-0.289 -0.3023,-0.2978 -0.2972,-0.3029 -0.2731,-0.3169 -0.2693,'
        '-0.3105ZM0.0146,-0.7351 0.0057,-0.7275 -0.0006,-0.7148 -0.0006,-0.7009 0.0019,-0.6933 0.012,-0.6'
        '819 0.0209,-0.6781 0.0323,-0.6768 0.0463,-0.6819 0.0551,-0.6907 0.0589,-0.6984 0.0602,-0.7085 0.'
        '0577,-0.7212 0.0526,-0.7288 0.0374,-0.7376 0.0222,-0.7376ZM0.026,-0.7224 0.0323,-0.7224 0.0374,-'
        '0.7199 0.0437,-0.711 0.0425,-0.7009 0.0323,-0.6933 0.0209,-0.6958 0.0146,-0.706 0.0158,-0.7148ZM'
        '-0.2795,-0.7376 -0.2883,-0.7338 -0.2947,-0.7288 -0.2985,-0.7224 -0.3023,-0.7085 -0.301,-0.6984 -'
        '0.2972,-0.6907 -0.2883,-0.6819 -0.2744,-0.6768 -0.2617,-0.6781 -0.2541,-0.6819 -0.244,-0.6933 -0'
        '.2414,-0.6984 -0.2414,-0.7174 -0.2465,-0.7262 -0.2541,-0.7338 -0.263,-0.7376ZM-0.2744,-0.7224 -0'
        '.2681,-0.7224 -0.2579,-0.7148 -0.2567,-0.7047 -0.2643,-0.6946 -0.2782,-0.6946 -0.2858,-0.7047 -0'
        '.2845,-0.7148ZM-0.3961,-0.8669 -0.3986,-0.7845 -0.4024,-0.7833 -0.4075,-0.7769 -0.4075,-0.7136 -'
        '0.4049,-0.706 -0.3948,-0.6984 -0.3074,-0.6984 -0.3086,-0.7136 -0.3023,-0.7288 -0.2921,-0.7389 -0'
        '.2769,-0.7452 -0.2605,-0.744 -0.249,-0.7376 -0.2414,-0.73 -0.2338,-0.7123 -0.2351,-0.6984 -0.007'
        ',-0.6984 -0.007,-0.7174 -0.0019,-0.7275 0.007,-0.7376 0.0234,-0.7452 0.0399,-0.744 0.0551,-0.735'
        '1 0.0665,-0.7148 0.0665,-0.7009 0.064,-0.6971 0.1958,-0.7224 0.1946,-0.8441 0.1882,-0.858 0.1781'
        ',-0.8682 0.1654,-0.8733 -0.3897,-0.8733ZM0.0919,-0.8403 0.0957,-0.8428 0.1527,-0.8428 0.1603,-0.'
        '8403 0.1667,-0.8352 0.1705,-0.8289 0.1717,-0.7959 0.1667,-0.7909 0.0932,-0.7921 0.0906,-0.7947ZM'
        '-0.3048,-0.8378 -0.2985,-0.8428 -0.23,-0.8416 -0.2262,-0.8365 -0.2275,-0.7947 -0.2313,-0.7909 -0'
        '.2997,-0.7909 -0.3048,-0.7959ZM-0.3631,-0.8428 -0.3378,-0.8428 -0.3327,-0.839 -0.3314,-0.8352 -0'
        '.3314,-0.725 -0.3327,-0.7212 -0.3378,-0.7174 -0.3631,-0.7174 -0.3695,-0.7262 -0.3695,-0.834ZM-0.'
        '4734,-0.9379 -0.4835,-0.929 -0.4899,-0.9189 -0.4937,-0.9011 -0.4937,0.8986 -0.4911,0.9037 -0.492'
        '4,0.9087 -0.4899,0.9176 -0.4759,0.9354 -0.4658,0.9404 -0.4531,0.943 0.4544,0.943 0.467,0.9392 0.'
        '4785,0.9316 0.4848,0.924 0.4911,0.9075 0.4911,-0.9087 0.4848,-0.9252 0.4721,-0.9379 0.4518,-0.94'
        '42 -0.4518,-0.9442ZM-0.4734,0.5044 -0.462,0.4905 -0.4531,0.488 0.4569,0.4892 0.462,0.4918 0.4721'
        ',0.5044 0.4708,0.91 0.462,0.9202 0.4531,0.924 -0.4531,0.924 -0.462,0.9214 -0.4708,0.9125 -0.4734'
        ',0.9062ZM-0.4594,-0.924 0.2617,-0.924 0.2617,-0.1876 0.3074,-0.1876 0.3074,-0.9227 0.3099,-0.925'
        '2 0.4531,-0.9252 0.467,-0.9176 0.4721,-0.9075 0.4721,0.4474 0.4696,0.4537 0.4607,0.4626 0.4544,0'
        '.4651 -0.4569,0.4651 -0.4708,0.4537 -0.4734,0.4487 -0.4734,-0.9087 -0.4721,-0.9125ZM0.4594,-0.95'
        '06 0.4759,-0.9455 0.4886,-0.9341 0.4962,-0.9227 0.4987,-0.9075 0.4987,-0.9506ZM-0.5,-0.91 -0.498'
        '7,-0.9202 -0.4937,-0.9303 -0.4823,-0.9417 -0.4658,-0.9506 -0.4582,-0.9506 -0.5,-0.9506Z'
    ),
    '959B/0': (
        'M0.499,0.666 0.498,0.6721 0.4928,0.6823 0.4847,0.6915 0.4734,0.6987 0.4612,0.7017 0.499,0.7017ZM'
        '-0.5,0.6629 -0.5,0.7017 -0.4642,0.7017 -0.4765,0.6977 -0.4867,0.6895 -0.498,0.6731ZM-0.0628,-0.0'
        '072 -0.0638,0.0072 -0.0618,0.0194 -0.0506,0.0368 -0.0373,0.046 -0.0169,0.0501 -0.0015,0.047 0.01'
        '07,0.0398 0.022,0.0266 0.026,0.0163 0.0271,-0.0041 0.025,-0.0123 0.0209,-0.0204 0.0087,-0.0327 0'
        '.0097,-0.0368 0.0618,-0.001 0.0608,0.0082 0.0638,0.0153 0.0689,0.0204 0.0741,0.0225 0.0843,0.022'
        '5 0.0863,0.0245 0.0863,0.0266 0.0832,0.0276 0.0832,0.0347 0.0884,0.0347 0.0904,0.0368 0.1016,0.0'
        '347 0.1016,0.0276 0.0945,0.0276 0.0904,0.0204 0.1006,0.0082 0.1027,0.0102 0.1067,0.0255 0.1118,0'
        '.0327 0.1261,0.0449 0.1353,0.048 0.1568,0.049 0.1639,0.047 0.1752,0.0409 0.1864,0.0286 0.1925,0.'
        '0143 0.1936,0.0041 0.1895,-0.0153 0.1834,-0.0245 0.1752,-0.0327 0.167,-0.0378 0.1578,-0.0409 0.1'
        '466,-0.0419 0.1343,-0.0388 0.1292,-0.0398 0.1129,-0.0684 0.1159,-0.0766 0.118,-0.0787 0.121,-0.0'
        '787 0.1272,-0.0848 0.1282,-0.0899 0.0843,-0.0899 0.0832,-0.0848 0.0863,-0.0817 0.0996,-0.0797 0.'
        '1037,-0.0776 0.0986,-0.0684 0.0189,-0.0684 0.0179,-0.0695 0.0199,-0.0797 0.0138,-0.0878 0.0158,-'
        '0.0899 0.0332,-0.0899 0.0332,-0.1021 0.0097,-0.1021 0.0015,-0.097 -0.0005,-0.0868 0.0026,-0.0807'
        ' 0.0066,-0.0776 0.0066,-0.0725 -0.0015,-0.0419 -0.0036,-0.0388 -0.0077,-0.0409 -0.0209,-0.0419 -'
        '0.0414,-0.0358 -0.0485,-0.0306 -0.0546,-0.0235ZM0.0761,-0.0072 0.0843,-0.0072 0.0914,0.001 0.090'
        '4,0.0092 0.0853,0.0143 0.0802,0.0163 0.0741,0.0143 0.0679,0.0061 0.07,-0.002ZM0.1261,-0.0184 0.1'
        '292,-0.0163 0.1374,-0.002 0.1364,-0.001 0.117,-0.002 0.12,-0.0112ZM0.0587,-0.0194 0.0638,-0.0204'
        ' 0.0669,-0.0174 0.0679,-0.0133 0.0669,-0.0123ZM0.1415,-0.0266 0.1537,-0.0266 0.166,-0.0215 0.173'
        '1,-0.0143 0.1793,0.001 0.1793,0.0082 0.1742,0.0215 0.1629,0.0317 0.1547,0.0347 0.1404,0.0347 0.1'
        '313,0.0306 0.121,0.0204 0.117,0.0112 0.119,0.0082 0.1517,0.0082 0.1537,0.0061 0.1517,-0.002 0.13'
        '84,-0.0235ZM-0.0209,-0.0276 -0.0066,-0.0245 -0.0117,-0.0092 -0.023,0.002 -0.023,0.0061 -0.0209,0'
        '.0082 -0.0169,0.0092 -0.0077,0.0051 0.0005,-0.0041 0.0046,-0.0163 0.0097,-0.0102 0.0128,-0.002 0'
        '.0128,0.0102 0.0077,0.0215 -0.0015,0.0306 -0.0148,0.0358 -0.025,0.0347 -0.0352,0.0306 -0.0434,0.'
        '0225 -0.0495,0.0102 -0.0495,0 -0.0444,-0.0133 -0.0332,-0.0235ZM0.1078,-0.0521 0.117,-0.0378 0.11'
        '9,-0.0317 0.1098,-0.0215 0.1047,-0.0123 0.1027,-0.002 0.0996,-0.001 0.0924,-0.0102 0.0924,-0.013'
        '3 0.1057,-0.0511ZM0.0128,-0.0511 0.0148,-0.0562 0.0945,-0.0552 0.0822,-0.0194 0.0792,-0.0153 0.0'
        '761,-0.0143 0.0741,-0.0153 0.073,-0.0194 0.0771,-0.0204 0.0771,-0.0266 0.0649,-0.0286 0.0618,-0.'
        '0266 0.0577,-0.0266 0.0577,-0.0215 0.0557,-0.0204ZM-0.4081,0.0041 -0.406,0.0215 -0.4019,0.0296 -'
        '0.3876,0.0439 -0.3754,0.049 -0.3672,0.0501 -0.3488,0.047 -0.3396,0.0419 -0.3315,0.0337 -0.3233,0'
        '.0184 -0.3223,0 -0.3294,-0.0174 -0.3376,-0.0255 -0.3345,-0.0276 -0.3253,-0.0174 -0.3192,-0.0031 '
        '-0.3172,0.0174 -0.309,0.0266 -0.2252,0.0276 -0.2201,0.0347 -0.2099,0.0439 -0.1925,0.0501 -0.1823'
        ',0.0501 -0.1711,0.047 -0.1588,0.0398 -0.1486,0.0266 -0.1456,0.0184 -0.1445,0.0082 -0.1364,0.0072'
        ' -0.1364,-0.001 -0.1425,-0.0184 -0.1558,-0.0337 -0.167,-0.0398 -0.167,-0.046 -0.1701,-0.0501 -0.'
        '1752,-0.0521 -0.215,-0.0521 -0.2181,-0.0644 -0.2416,-0.0899 -0.2661,-0.1001 -0.2661,-0.1052 -0.2'
        '63,-0.1103 -0.263,-0.1195 -0.2661,-0.1256 -0.2732,-0.1307 -0.2824,-0.1318 -0.2916,-0.1267 -0.295'
        '7,-0.1175 -0.2957,-0.1134 -0.2926,-0.1124 -0.2916,-0.0981 -0.2875,-0.094 -0.2814,-0.0919 -0.2926'
        ',-0.0725 -0.3069,-0.0603 -0.31,-0.0603 -0.3131,-0.0633 -0.3049,-0.1011 -0.3049,-0.1062 -0.308,-0'
        '.1062 -0.3274,-0.0725 -0.3345,-0.0654 -0.3488,-0.0582 -0.3672,-0.0572 -0.3672,-0.0398 -0.355,-0.'
        '0388 -0.3488,-0.0358 -0.3509,-0.0337 -0.3672,-0.0358 -0.3754,-0.0347 -0.3846,-0.0317 -0.3907,-0.'
        '0276 -0.4019,-0.0153 -0.406,-0.0061ZM-0.1864,-0.0184 -0.1772,-0.0163 -0.1711,-0.0123 -0.166,-0.0'
        '061 -0.1619,0.0061 -0.1639,0.0163 -0.1701,0.0255 -0.1803,0.0317 -0.1936,0.0317 -0.2038,0.0255 -0'
        '.2089,0.0194 -0.212,0.0112 -0.212,0.0031 -0.2089,-0.0051 -0.2028,-0.0123 -0.1997,-0.0051 -0.2038'
        ',0.0051 -0.2017,0.0153 -0.1956,0.0215 -0.1905,0.0235 -0.1834,0.0235 -0.1782,0.0215 -0.1711,0.012'
        '3 -0.1711,0.002 -0.1752,-0.0051 -0.1854,-0.0102 -0.1874,-0.0153ZM-0.3713,-0.0174 -0.3652,-0.0184'
        ' -0.3601,-0.0163 -0.3652,-0.0092 -0.3703,-0.0092 -0.3754,-0.0061 -0.3815,0.0031 -0.3805,0.0143 -'
        '0.3723,0.0225 -0.3611,0.0235 -0.3519,0.0174 -0.3488,0.0112 -0.3488,0.002 -0.3509,-0.002 -0.3468,'
        '-0.0082 -0.3447,-0.0072 -0.3407,0.001 -0.3407,0.0112 -0.3447,0.0215 -0.3519,0.0286 -0.359,0.0317'
        ' -0.3703,0.0317 -0.3764,0.0296 -0.3846,0.0225 -0.3897,0.0123 -0.3897,0.0031 -0.3876,-0.0041 -0.3'
        '784,-0.0143ZM-0.216,-0.0276 -0.215,-0.0255 -0.2252,-0.0133 -0.2283,-0.0031 -0.2314,0 -0.2324,-0.'
        '0266ZM-0.262,-0.0511 -0.2722,-0.0358 -0.2794,-0.0368 -0.3039,-0.046 -0.2732,-0.0644 -0.2712,-0.0'
        '633 -0.2681,-0.0562ZM0.022,-0.4862 0.0128,-0.4821 0.0015,-0.4688 -0.0005,-0.4597 0.0015,-0.4443 '
        '0.0128,-0.4311 0.0189,-0.428 0.0291,-0.4259 0.0393,-0.427 0.0516,-0.4341 0.0567,-0.4413 0.0608,-'
        '0.4525 0.0598,-0.4648 0.0526,-0.478 0.0393,-0.4862ZM0.0342,-0.4709 0.0424,-0.4648 0.0444,-0.4607'
        ' 0.0444,-0.4525 0.0373,-0.4433 0.0291,-0.4413 0.022,-0.4443 0.0169,-0.4494 0.0158,-0.4607 0.0169'
        ',-0.4637 0.024,-0.4699ZM-0.2835,-0.4852 -0.2906,-0.4811 -0.2967,-0.475 -0.3018,-0.4617 -0.3018,-'
        '0.4515 -0.2998,-0.4443 -0.2957,-0.4372 -0.2835,-0.428 -0.2722,-0.4259 -0.262,-0.427 -0.2518,-0.4'
        '331 -0.2457,-0.4402 -0.2416,-0.4494 -0.2416,-0.4637 -0.2446,-0.4719 -0.2559,-0.4831 -0.2681,-0.4'
        '872 -0.2763,-0.4872ZM-0.2753,-0.4709 -0.2651,-0.4699 -0.26,-0.4658 -0.2569,-0.4607 -0.2569,-0.45'
        '25 -0.26,-0.4474 -0.2651,-0.4433 -0.2722,-0.4413 -0.2814,-0.4454 -0.2865,-0.4545 -0.2845,-0.4637'
        'ZM-0.3968,-0.6149 -0.3999,-0.5332 -0.405,-0.5312 -0.4081,-0.526 -0.4081,-0.4607 -0.4019,-0.4505 '
        '-0.3927,-0.4464 -0.308,-0.4464 -0.308,-0.4648 -0.3039,-0.476 -0.2937,-0.4872 -0.2783,-0.4934 -0.'
        '264,-0.4934 -0.2497,-0.4872 -0.2416,-0.4791 -0.2354,-0.4668 -0.2354,-0.4464 -0.0056,-0.4464 -0.0'
        '066,-0.4627 -0.0015,-0.477 0.0097,-0.4883 0.023,-0.4934 0.0373,-0.4934 0.0444,-0.4913 0.0587,-0.'
        '4811 0.0659,-0.4678 0.0659,-0.4464 0.1956,-0.4709 0.1956,-0.5945 0.1905,-0.6057 0.1834,-0.6139 0'
        '.167,-0.6221 -0.3897,-0.6231 -0.3958,-0.618ZM0.0914,-0.5884 0.0955,-0.5914 0.1568,-0.5914 0.1609'
        ',-0.5894 0.1691,-0.5822 0.1731,-0.573 0.1721,-0.5434 0.1691,-0.5403 0.165,-0.5393 0.0975,-0.5393'
        ' 0.0935,-0.5414 0.0904,-0.5465ZM-0.3049,-0.5873 -0.3008,-0.5914 -0.2293,-0.5904 -0.2263,-0.5843 '
        '-0.2273,-0.5444 -0.2344,-0.5393 -0.3008,-0.5403 -0.3049,-0.5444ZM-0.3652,-0.5914 -0.3366,-0.5914'
        ' -0.3325,-0.5873 -0.3325,-0.4709 -0.3386,-0.4658 -0.3621,-0.4658 -0.3652,-0.4668 -0.3693,-0.4719'
        ' -0.3693,-0.5863ZM-0.4775,-0.6895 -0.4888,-0.6772 -0.4939,-0.6639 -0.4949,-0.6568 -0.4949,0.6588'
        ' -0.4877,0.6782 -0.4796,0.6874 -0.4724,0.6925 -0.4642,0.6956 -0.451,0.6977 0.453,0.6977 0.4663,0'
        '.6946 0.4796,0.6874 0.4877,0.6782 0.4949,0.6588 0.4949,-0.6568 0.4928,-0.668 0.4847,-0.6823 0.47'
        '55,-0.6905 0.4653,-0.6956 0.453,-0.6977 -0.453,-0.6977 -0.4622,-0.6966ZM-0.4745,0.2697 -0.4714,0'
        '.2635 -0.4653,0.2574 -0.4561,0.2533 0.454,0.2533 0.4622,0.2554 0.4704,0.2625 0.4745,0.2727 0.474'
        '5,0.6599 0.4663,0.6721 0.4551,0.6772 -0.4591,0.6762 -0.4653,0.6731 -0.4704,0.668 -0.4745,0.6599Z'
        'M0.311,-0.6782 0.452,-0.6782 0.4602,-0.6762 0.4653,-0.6731 0.4734,-0.6639 0.4745,-0.6588 0.4745,'
        '0.2114 0.4704,0.2206 0.4642,0.2268 0.4571,0.2298 0.309,0.2288 0.309,-0.6762ZM-0.4673,-0.6721 -0.'
        '4602,-0.6762 -0.452,-0.6782 0.262,-0.6782 0.264,-0.6762 0.263,0.2298 -0.4581,0.2298 -0.4642,0.22'
        '68 -0.4714,0.2196 -0.4745,0.2135 -0.4745,-0.6609ZM0.4571,-0.7028 0.4673,-0.7017 0.4796,-0.6956 0'
        '.4898,-0.6864 0.4959,-0.6772 0.499,-0.6691 0.499,-0.7028ZM-0.5,-0.6629 -0.4959,-0.6782 -0.4816,-'
        '0.6946 -0.4642,-0.7028 -0.4561,-0.7028 -0.5,-0.7028Z'
    ),
    '960/0': (
        'M1.1024,0.433 1.1006,0.4441 1.0912,0.4628 1.0726,0.4814 1.0428,0.4981 1.0317,0.4981 1.1024,0.498'
        '1ZM-1.1043,0.4255 -1.1043,0.4981 -1.0391,0.4981 -1.067,0.487 -1.0857,0.4702 -1.1024,0.4404ZM-0.1'
        '378,0.2542 -0.1378,0.2858 -0.1248,0.3156 -0.1117,0.3305 -0.0968,0.3417 -0.0801,0.3492 -0.0596,0.'
        '3529 -0.0372,0.351 -0.0149,0.3436 0.0074,0.325 0.0223,0.3007 0.0279,0.2784 0.0279,0.2579 0.0242,'
        '0.2412 0.0149,0.2225 -0.0056,0.202 -0.0037,0.1946 0.0894,0.2598 0.0894,0.2784 0.0968,0.2933 0.10'
        '61,0.3007 0.1173,0.3045 0.1341,0.3045 0.1359,0.3101 0.1285,0.3119 0.1285,0.325 0.1378,0.325 0.14'
        '34,0.3287 0.1639,0.325 0.1639,0.3119 0.1508,0.3119 0.1434,0.2989 0.1527,0.2896 0.1564,0.2803 0.1'
        '639,0.2784 0.1713,0.3045 0.1844,0.325 0.2086,0.3436 0.2272,0.351 0.2644,0.351 0.2775,0.3473 0.29'
        '98,0.3343 0.3128,0.3212 0.324,0.3026 0.3315,0.2691 0.3222,0.2318 0.3128,0.2169 0.2998,0.2039 0.2'
        '812,0.1927 0.2626,0.1872 0.2439,0.1853 0.216,0.1909 0.2123,0.1872 0.1844,0.1369 0.1881,0.1238 0.'
        '2011,0.1164 0.2123,0.1034 0.2086,0.0959 0.1322,0.0978 0.1304,0.1071 0.1341,0.1108 0.1601,0.1164 '
        '0.1657,0.1201 0.1583,0.1387 0.013,0.1387 0.013,0.1127 0.0037,0.1034 0.0037,0.0996 0.0391,0.0978 '
        '0.0391,0.0754 -0.0037,0.0754 -0.0186,0.0847 -0.0223,0.094 -0.0223,0.1052 -0.0186,0.1127 -0.0093,'
        '0.1201 -0.0093,0.1276 -0.0279,0.1909 -0.0372,0.1872 -0.0689,0.1872 -0.0931,0.1946 -0.1192,0.2151'
        ' -0.1341,0.2412ZM0.1192,0.2486 0.1341,0.2505 0.1415,0.2579 0.1453,0.2672 0.1415,0.2803 0.1341,0.'
        '2877 0.1248,0.2914 0.1117,0.2877 0.1024,0.2728 0.1043,0.2598ZM0.2086,0.2281 0.2123,0.23 0.2272,0'
        '.2542 0.2272,0.2598 0.1918,0.2579 0.1993,0.2374ZM0.0857,0.2281 0.095,0.2263 0.1024,0.2374 0.0968'
        ',0.2374ZM0.2346,0.2132 0.2588,0.2132 0.2737,0.2188 0.2942,0.2374 0.3035,0.2579 0.3035,0.2784 0.2'
        '924,0.3045 0.2719,0.3212 0.2514,0.3268 0.2216,0.3212 0.2011,0.3026 0.1918,0.284 0.1937,0.2784 0.'
        '2514,0.2784 0.2588,0.2728 0.2533,0.2561 0.2309,0.2188ZM-0.067,0.2132 -0.0428,0.2132 -0.0335,0.21'
        '88 -0.0447,0.2467 -0.0633,0.2654 -0.0633,0.2728 -0.0596,0.2765 -0.0521,0.2784 -0.0354,0.2709 -0.'
        '0205,0.2542 -0.013,0.2318 -0.0093,0.2337 0,0.2523 0.0019,0.2784 -0.0074,0.3007 -0.0168,0.3119 -0'
        '.0391,0.325 -0.0577,0.3268 -0.0857,0.3175 -0.1024,0.3007 -0.1099,0.2858 -0.1117,0.2616 -0.1061,0'
        '.243 -0.0875,0.2225ZM0.175,0.1667 0.1955,0.2039 0.1769,0.2244 0.1695,0.2393 0.1657,0.2579 0.1583'
        ',0.2598 0.1471,0.243 0.1471,0.2374 0.1695,0.1741ZM0.0019,0.1685 0.0074,0.1592 0.1508,0.1611 0.12'
        '66,0.23 0.1173,0.2356 0.1099,0.2281 0.1192,0.2263 0.1192,0.2132 0.108,0.2132 0.1043,0.2095 0.081'
        '9,0.2132 0.0819,0.2225 0.0782,0.2244ZM0.6164,0.0493 0.6164,0.2635 0.6145,0.2654 0.5624,0.2132 0.'
        '5624,0.2989 0.6462,0.3808 0.7281,0.2989 0.7281,0.2132 0.676,0.2654 0.6741,0.2635 0.6741,0.0493ZM'
        '0.6462,-0.1127 0.6238,-0.1015 0.6127,-0.0885 0.6052,-0.0698 0.6052,-0.0456 0.6145,-0.0251 0.622,'
        '-0.0158 0.6331,-0.0084 0.648,-0.0028 0.6778,-0.0047 0.6927,-0.0121 0.7095,-0.0307 0.7151,-0.0493'
        ' 0.7132,-0.0736 0.7039,-0.0922 0.6909,-0.1052 0.6704,-0.1127ZM0.6555,-0.0847 0.676,-0.0791 0.687'
        '2,-0.0624 0.6872,-0.0549 0.6816,-0.0419 0.6741,-0.0345 0.6648,-0.0307 0.6462,-0.0345 0.6369,-0.0'
        '438 0.6331,-0.0531 0.6369,-0.0717 0.6462,-0.081ZM0.095,-0.1127 0.0819,-0.1071 0.067,-0.094 0.057'
        '7,-0.0791 0.054,-0.0512 0.0633,-0.027 0.0745,-0.014 0.0968,-0.0028 0.121,-0.0028 0.1397,-0.0102 '
        '0.1546,-0.0233 0.1657,-0.0475 0.1657,-0.068 0.1527,-0.094 0.1397,-0.1052 0.121,-0.1127ZM0.1061,-'
        '0.0847 0.1155,-0.0847 0.1285,-0.0773 0.1359,-0.0642 0.1359,-0.0512 0.1322,-0.0438 0.1155,-0.0307'
        ' 0.0968,-0.0345 0.0857,-0.0456 0.0838,-0.0512 0.0857,-0.0698 0.0931,-0.0791ZM-0.5084,-0.2486 -0.'
        '6201,-0.1369 -0.6201,-0.0363 -0.5493,-0.1071 -0.5456,-0.1052 -0.5456,0.2486 -0.4711,0.2486 -0.47'
        '11,-0.1071 -0.4693,-0.1089 -0.3985,-0.0382 -0.3985,-0.1387ZM-0.8659,-0.2486 -0.9777,-0.1369 -0.9'
        '777,-0.0363 -0.9069,-0.1071 -0.9032,-0.1052 -0.9032,0.2486 -0.8305,0.2486 -0.8305,-0.1071 -0.826'
        '8,-0.1089 -0.7561,-0.0382 -0.7561,-0.1387ZM-0.1173,-0.351 -0.1229,-0.2058 -0.1248,-0.1965 -0.134'
        '1,-0.1927 -0.1378,-0.1872 -0.1378,-0.0642 -0.1341,-0.0549 -0.1229,-0.0438 -0.1117,-0.04 0.0447,-'
        '0.04 0.0428,-0.068 0.0503,-0.0922 0.0596,-0.1052 0.0819,-0.1201 0.1006,-0.1257 0.1173,-0.1257 0.'
        '1378,-0.1201 0.1508,-0.1127 0.1657,-0.0978 0.1769,-0.0698 0.175,-0.04 0.594,-0.04 0.5922,-0.0642'
        ' 0.6015,-0.094 0.6201,-0.1145 0.6499,-0.1257 0.6685,-0.1257 0.6834,-0.122 0.7002,-0.1127 0.7169,'
        '-0.0959 0.7263,-0.0736 0.7263,-0.04 0.9628,-0.0847 0.9628,-0.3007 0.9553,-0.325 0.9479,-0.3361 0'
        '.9274,-0.3529 0.9088,-0.3603 -0.108,-0.3603ZM0.73,-0.297 0.7374,-0.3045 0.8957,-0.3026 0.9125,-0'
        '.2877 0.9181,-0.2784 0.9218,-0.2635 0.9199,-0.2188 0.9162,-0.2132 0.9088,-0.2095 0.7393,-0.2095 '
        '0.73,-0.2169ZM0.5028,-0.297 0.5102,-0.3045 0.6853,-0.3045 0.6927,-0.297 0.6927,-0.2169 0.6816,-0'
        '.2095 0.514,-0.2095 0.5028,-0.2188ZM0.2756,-0.2952 0.2849,-0.3045 0.4581,-0.3045 0.4674,-0.2933 '
        '0.4674,-0.2207 0.46,-0.2114 0.4544,-0.2095 0.2868,-0.2095 0.2756,-0.2188ZM0.0484,-0.2952 0.0577,'
        '-0.3045 0.2309,-0.3045 0.2365,-0.3007 0.2402,-0.2914 0.2402,-0.2207 0.2328,-0.2114 0.2272,-0.209'
        '5 0.0596,-0.2095 0.0484,-0.2188ZM-0.0596,-0.3045 -0.0093,-0.3045 -0.0019,-0.297 -0.0019,-0.0829 '
        '-0.013,-0.0754 -0.0577,-0.0754 -0.0689,-0.0866 -0.0689,-0.2933ZM-1.0875,-0.446 -1.095,-0.4162 -1'
        '.095,0.4199 -1.0912,0.4367 -1.0764,0.4628 -1.0484,0.4832 -1.0317,0.4888 1.0279,0.4888 1.0428,0.4'
        '851 1.0633,0.4739 1.0801,0.4572 1.0875,0.4441 1.095,0.4143 1.095,-0.4125 1.0857,-0.4497 1.0652,-'
        '0.4739 1.0503,-0.4832 1.0186,-0.4907 -1.0205,-0.4907 -1.054,-0.4814 -1.0801,-0.459ZM-0.2328,-0.4'
        '516 1.0261,-0.4534 1.041,-0.446 1.0503,-0.4367 1.0577,-0.4199 1.0577,0.4199 1.0484,0.4385 1.0372'
        ',0.4479 1.0223,0.4534 -0.2309,0.4534ZM-1.0391,-0.4479 -1.0279,-0.4534 -0.3166,-0.4516 -0.3166,0.'
        '4497 -0.3203,0.4534 -1.0223,0.4534 -1.041,0.446 -1.0503,0.4367 -1.0577,0.4199 -1.0577,-0.4199 -1'
        '.0521,-0.4348ZM1.0279,-0.5 1.0447,-0.4981 1.0726,-0.4832 1.0857,-0.4702 1.0968,-0.4534 1.1024,-0'
        '.4348 1.1024,-0.5ZM-1.1043,-0.4274 -1.095,-0.4572 -1.0726,-0.4832 -1.0391,-0.5 -1.0261,-0.5 -1.1'
        '043,-0.5Z'
    ),
    'MARKER/0': (
        'M-0.3892,-2.4551 -0.3892,-2.4491 -0.2695,-2.3293 -0.2455,-2.3144 -0.1886,-2.2575 -0.009,-2.2605 '
        '-0.015,-2.2725 -0.1228,-2.3772 -0.1198,-2.3892 0.3832,-2.3892 0.3952,-2.3982 0.3952,-2.512 0.389'
        '2,-2.515 -0.1198,-2.515 -0.1257,-2.524 -0.009,-2.6407 -0.009,-2.6467 -0.1976,-2.6437ZM-0.2725,-3'
        '.6287 -0.3383,-3.5749 -0.3443,-3.5629 -0.3383,-3.5389 -0.1707,-3.3802 -0.1437,-3.3832 -0.1287,-3'
        '.3982 -0.1138,-3.4311 -0.0898,-3.4491 -0.0629,-3.4581 -0.0329,-3.4521 0.021,-3.3862 0.2006,-3.06'
        '59 0.2126,-3.0329 0.2186,-2.976 0.2126,-2.9162 0.2066,-2.9102 0.1347,-2.9192 0.0838,-2.8802 0.08'
        '38,-2.7126 0.1257,-2.6766 0.1377,-2.6737 0.2425,-2.6856 0.2784,-2.7006 0.3144,-2.7335 0.3383,-2.'
        '7725 0.3503,-2.8503 0.3383,-2.9491 0.3024,-3.0778 0.2934,-3.0898 0.2904,-3.1108 0.2425,-3.2216 0'
        '.2216,-3.2515 0.2066,-3.2874 0.1587,-3.3653 0.0868,-3.4581 -0.018,-3.5689 -0.0689,-3.6108 -0.110'
        '8,-3.6377 -0.1587,-3.6557 -0.2246,-3.6527ZM-0.5,-1.7305 0.5,-1.7305 0.5,3.6287 -0.5,3.6287Z'
    ),
    '618.1/0': (
        'M-0.6389,-0.4710 -0.6510,-0.4444 -0.6510,0.4420 -0.6389,0.4686 -0.6220,0.4855 -0.5930,0.4976 0.5906,'
        '0.4976 0.6196,0.4855 0.6341,0.4710 0.6486,0.4396 0.6486,-0.4420 0.6389,-0.4662 0.6220,-0.4855 0.5906'
        ',-0.5000 -0.5930,-0.5000 -0.6220,-0.4879Z'
    ),
    '618.1/1': (
        'M-0.6123,-0.4469 -0.6171,-0.4324 -0.6171,0.4300 -0.6123,0.4444 -0.6002,0.4565 -0.5906,0.4614 0.5882,'
        '0.4614 0.6075,0.4469 0.6123,0.4372 0.6123,-0.4372 0.5978,-0.4589 0.5857,-0.4638 -0.5906,-0.4638Z'
    ),
    '618.2/0': (
        'M-0.0873,-0.0463 -0.1122,-0.0178 -0.1336,0.0962 -0.1585,0.1140 -0.1656,0.1318 -0.1656,0.2280 -0.1585'
        ',0.2458 -0.1443,0.2600 -0.1443,0.3277 -0.1300,0.3419 -0.1193,0.3455 -0.0908,0.3384 -0.0801,0.3277 -0'
        '.0801,0.2671 -0.0766,0.2636 -0.0338,0.2636 -0.0303,0.2671 0.1799,0.2636 0.1834,0.2671 0.1834,0.3277 '
        '0.1906,0.3348 0.2369,0.3063 0.2475,0.2956 0.2475,0.2636 0.2689,0.2280 0.2689,0.1318 0.2654,0.1211 0.'
        '2369,0.0962 0.2119,-0.0249 0.1906,-0.0463 0.1656,-0.0534 -0.0623,-0.0534ZM-0.0588,0.2280 -0.0552,0.2'
        '173 0.1585,0.2173 0.1621,0.2208 0.1549,0.2315 0.1086,0.2315 0.1051,0.2351 -0.0018,0.2351ZM-0.0588,0.'
        '1888 -0.0552,0.1852 0.1585,0.1852 0.1621,0.1959 0.1585,0.1995 -0.0552,0.1995ZM-0.0588,0.1603 -0.0516'
        ',0.1532 -0.0018,0.1532 0.0018,0.1496 0.1549,0.1532 0.1621,0.1603 0.1549,0.1674 -0.0516,0.1674ZM0.197'
        '7,0.1247 0.2191,0.1211 0.2404,0.1389 0.2404,0.1638 0.2262,0.1781 0.2119,0.1817 0.1870,0.1674 0.1834,'
        '0.1460ZM-0.1158,0.1211 -0.0944,0.1247 -0.0801,0.1460 -0.0837,0.1674 -0.1086,0.1817 -0.1229,0.1781 -0'
        '.1371,0.1638 -0.1371,0.1389ZM-0.1051,0.0570 -0.0944,0.0107 -0.0623,-0.0142 -0.0481,-0.0178 0.1478,-0'
        '.0178 0.1799,-0.0071 0.1977,0.0107 0.2084,0.0677 0.1941,0.0819 0.0623,0.0784 0.0588,0.0748 -0.0908,0'
        '.0819 -0.1015,0.0748ZM-0.1656,-0.1710 -0.1656,-0.1354 -0.1514,-0.1069 -0.1300,-0.0890 -0.0980,-0.078'
        '4 -0.0623,-0.0855 -0.0303,-0.1140 -0.0160,-0.1638 -0.0089,-0.1318 0.0125,-0.1175 0.1514,-0.1175 0.17'
        '99,-0.0890 0.2119,-0.0784 0.2404,-0.0819 0.2654,-0.0962 0.2867,-0.1247 0.2903,-0.1496 0.3081,-0.1603'
        ' 0.3010,-0.1888 0.2903,-0.2066 0.2547,-0.2351 0.2440,-0.2565 0.2369,-0.2600 0.1692,-0.2600 0.1621,-0'
        '.2778 0.1122,-0.3277 0.0801,-0.3419 0.0873,-0.3562 0.0873,-0.3704 0.0730,-0.3811 0.0374,-0.3847 0.03'
        '03,-0.3776 0.0338,-0.3419 0.0516,-0.3241 0.0374,-0.2992 0.0089,-0.2707 -0.0018,-0.2743 0.0125,-0.331'
        '3 0.0053,-0.3384 -0.0445,-0.2743 -0.0659,-0.2671 -0.0908,-0.2671 -0.0980,-0.2600 -0.0980,-0.2422 -0.'
        '0801,-0.2315 -0.0837,-0.2280 -0.1158,-0.2244 -0.1407,-0.2101 -0.1585,-0.1888ZM-0.0232,-0.1888 -0.016'
        '0,-0.1781 -0.0196,-0.1638 -0.0267,-0.1781ZM0.1906,-0.1888 0.1977,-0.1817 0.1906,-0.1460 0.2119,-0.12'
        '47 0.2262,-0.1247 0.2440,-0.1425 0.2440,-0.1638 0.2226,-0.1817 0.2191,-0.1923 0.2333,-0.1959 0.2582,'
        '-0.1745 0.2618,-0.1425 0.2582,-0.1318 0.2404,-0.1140 0.2048,-0.1104 0.1941,-0.1140 0.1799,-0.1282 0.'
        '1727,-0.1603 0.1799,-0.1781ZM-0.1158,-0.1923 -0.1086,-0.1959 -0.0873,-0.1923 -0.0944,-0.1817 -0.1015'
        ',-0.1817 -0.1193,-0.1638 -0.1229,-0.1532 -0.1193,-0.1425 -0.1015,-0.1247 -0.0873,-0.1247 -0.0695,-0.'
        '1389 -0.0659,-0.1460 -0.0695,-0.1674 -0.0588,-0.1817 -0.0552,-0.1781 -0.0481,-0.1460 -0.0552,-0.1282'
        ' -0.0659,-0.1175 -0.0801,-0.1104 -0.1086,-0.1104 -0.1336,-0.1318 -0.1371,-0.1674ZM-0.0445,-0.2066 -0'
        '.0374,-0.2101 -0.0267,-0.1959 -0.0303,-0.1923ZM0.1692,-0.2137 0.1727,-0.2101 0.1478,-0.1781 0.1443,-'
        '0.2101ZM-0.0837,-0.2280 -0.0801,-0.2315 -0.0659,-0.2280 -0.0695,-0.2244ZM0.0873,-0.2565 0.0588,-0.22'
        '80 0.0160,-0.2458 0.0623,-0.2743 0.0695,-0.2743Z'
    ),
    '618.3A/0': (
        'M-0.4813,-1.1135 -0.4917,-1.1031 -0.5000,-1.0865 -0.5000,1.0823 -0.4937,1.0969 -0.4792,1.1115 -0.452'
        '1,1.1198 0.4500,1.1198 0.4688,1.1156 0.4771,1.1115 0.4917,1.0969 0.4979,1.0802 0.4979,-1.0844 0.4958'
        ',-1.0906 0.4813,-1.1115 0.4583,-1.1219 -0.4604,-1.1219Z'
    ),
    '618.3A/1': (
        'M-0.4729,0.1698 -0.4771,0.1802 -0.4771,0.7219 -0.4646,0.7385 -0.4604,0.7406 0.4583,0.7406 0.4708,0.7'
        '302 0.4750,0.7219 0.4750,0.1781 0.4625,0.1615 0.4583,0.1594 -0.4604,0.1594ZM-0.0187,-0.6198 -0.0688,'
        '-0.6115 -0.1042,-0.5990 -0.1521,-0.5719 -0.1979,-0.5302 -0.2250,-0.4927 -0.2396,-0.4635 -0.2500,-0.4'
        '344 -0.2583,-0.3865 -0.2583,-0.3469 -0.2500,-0.3010 -0.2333,-0.2573 -0.2083,-0.2177 -0.1708,-0.1781 '
        '-0.1333,-0.1510 -0.0896,-0.1302 -0.0375,-0.1177 0.0146,-0.1156 0.0667,-0.1240 0.1021,-0.1365 0.1313,'
        '-0.1510 0.1562,-0.1677 0.1979,-0.2073 0.2208,-0.2385 0.2354,-0.2656 0.2458,-0.2927 0.2562,-0.3427 0.'
        '2562,-0.3927 0.2479,-0.4365 0.2271,-0.4865 0.1979,-0.5281 0.1667,-0.5594 0.1313,-0.5844 0.0813,-0.60'
        '73 0.0354,-0.6177ZM-0.4646,-1.0969 -0.4729,-1.0885 -0.4771,-1.0781 -0.4771,0.1156 -0.4750,0.1219 -0.'
        '4646,0.1323 -0.4542,0.1365 0.4521,0.1365 0.4625,0.1323 0.4729,0.1219 0.4750,0.1156 0.4750,-1.0781 0.'
        '4688,-1.0906 0.4562,-1.0990 -0.4583,-1.0990ZM-0.0125,-0.6823 0.0521,-0.6781 0.1021,-0.6656 0.1625,-0'
        '.6385 0.2146,-0.6010 0.2437,-0.5719 0.2667,-0.5427 0.2938,-0.4948 0.3104,-0.4490 0.3208,-0.3865 0.31'
        '87,-0.3281 0.3146,-0.3031 0.3021,-0.2615 0.2833,-0.2198 0.2458,-0.1656 0.2125,-0.1323 0.1917,-0.1156'
        ' 0.1625,-0.0969 0.1292,-0.0802 0.0708,-0.0615 0.0000,-0.0531 -0.0646,-0.0594 -0.1167,-0.0740 -0.1646'
        ',-0.0969 -0.2146,-0.1323 -0.2583,-0.1781 -0.2771,-0.2052 -0.2958,-0.2406 -0.3125,-0.2865 -0.3229,-0.'
        '3510 -0.3208,-0.4073 -0.3125,-0.4490 -0.3021,-0.4802 -0.2771,-0.5302 -0.2479,-0.5698 -0.2146,-0.6031'
        ' -0.1688,-0.6365 -0.1271,-0.6573 -0.0750,-0.6740Z'
    ),
    '618.3A/2': (
        'M-0.4792,0.7823 -0.4792,1.0781 -0.4729,1.0885 -0.4604,1.0969 -0.4521,1.0990 0.4500,1.0990 0.4625,1.0'
        '948 0.4750,1.0823 0.4771,1.0740 0.4771,0.7865 0.4750,0.7781 0.4583,0.7635 0.4500,0.7615 -0.4542,0.76'
        '15 -0.4688,0.7677ZM-0.2729,0.8052 -0.2292,0.8052 -0.2062,0.8115 -0.1812,0.8240 -0.1646,0.8365 -0.145'
        '8,0.8573 -0.1333,0.8781 -0.1250,0.9031 -0.1229,0.9156 -0.1250,0.9573 -0.1333,0.9823 -0.1458,1.0031 -'
        '0.1625,1.0219 -0.1812,1.0365 -0.2062,1.0490 -0.2312,1.0552 -0.2812,1.0531 -0.3021,1.0469 -0.3250,1.0'
        '344 -0.3542,1.0073 -0.3688,0.9844 -0.3792,0.9531 -0.3812,0.9385 -0.3792,0.9073 -0.3688,0.8760 -0.354'
        '2,0.8531 -0.3333,0.8323 -0.3146,0.8198Z'
    ),
    '618.3A/3': (
        'M-0.2729,0.8052 -0.3146,0.8198 -0.3333,0.8323 -0.3542,0.8531 -0.3667,0.8719 -0.3771,0.8990 -0.3812,0'
        '.9219 -0.3792,0.9531 -0.3667,0.9885 -0.3542,1.0073 -0.3333,1.0281 -0.3146,1.0406 -0.2896,1.0510 -0.2'
        '729,1.0552 -0.2312,1.0552 -0.2062,1.0490 -0.1812,1.0365 -0.1458,1.0031 -0.1271,0.9656 -0.1229,0.9469'
        ' -0.1229,0.9135 -0.1292,0.8885 -0.1417,0.8635 -0.1583,0.8427 -0.1750,0.8281 -0.1958,0.8156 -0.2292,0'
        '.8052ZM-0.3396,0.8781 -0.3333,0.8719 -0.1917,1.0115 -0.2188,1.0260 -0.2375,1.0302 -0.2646,1.0302 -0.'
        '2896,1.0240 -0.3229,1.0031 -0.3396,0.9823 -0.3479,0.9656 -0.3542,0.9406 -0.3521,0.9094ZM-0.3104,0.84'
        '90 -0.2833,0.8344 -0.2646,0.8302 -0.2375,0.8302 -0.2083,0.8385 -0.1875,0.8510 -0.1646,0.8760 -0.1500'
        ',0.9115 -0.1500,0.9490 -0.1542,0.9635 -0.1688,0.9885 -0.1812,0.9781ZM-0.0125,-0.6844 -0.0750,-0.6760'
        ' -0.1271,-0.6594 -0.1688,-0.6385 -0.2146,-0.6052 -0.2500,-0.5698 -0.2792,-0.5302 -0.3042,-0.4802 -0.'
        '3146,-0.4490 -0.3229,-0.4073 -0.3250,-0.3510 -0.3146,-0.2865 -0.2979,-0.2406 -0.2854,-0.2156 -0.2604'
        ',-0.1781 -0.2146,-0.1302 -0.1646,-0.0948 -0.1167,-0.0719 -0.0646,-0.0573 0.0000,-0.0510 0.0708,-0.05'
        '94 0.1292,-0.0781 0.1625,-0.0948 0.1917,-0.1135 0.2125,-0.1302 0.2479,-0.1656 0.2854,-0.2198 0.3042,'
        '-0.2615 0.3125,-0.2865 0.3208,-0.3281 0.3229,-0.3865 0.3146,-0.4406 0.2958,-0.4948 0.2687,-0.5427 0.'
        '2458,-0.5719 0.2146,-0.6031 0.1625,-0.6406 0.1021,-0.6677 0.0521,-0.6802ZM-0.0187,-0.6177 0.0354,-0.'
        '6156 0.0813,-0.6052 0.1313,-0.5823 0.1667,-0.5573 0.1958,-0.5281 0.2250,-0.4865 0.2458,-0.4365 0.254'
        '2,-0.3927 0.2542,-0.3427 0.2437,-0.2927 0.2333,-0.2656 0.2188,-0.2385 0.1958,-0.2073 0.1562,-0.1698 '
        '0.1313,-0.1531 0.1021,-0.1385 0.0667,-0.1260 0.0146,-0.1177 -0.0375,-0.1198 -0.0896,-0.1323 -0.1333,'
        '-0.1531 -0.1708,-0.1802 -0.2062,-0.2177 -0.2312,-0.2573 -0.2479,-0.3010 -0.2562,-0.3469 -0.2562,-0.3'
        '865 -0.2479,-0.4344 -0.2375,-0.4635 -0.2229,-0.4927 -0.1958,-0.5302 -0.1521,-0.5698 -0.1042,-0.5969 '
        '-0.0688,-0.6094Z'
    ),
    '618.3A/4': (
        'M-0.3417,0.8781 -0.3542,0.9094 -0.3563,0.9406 -0.3500,0.9656 -0.3417,0.9823 -0.3229,1.0052 -0.2896,1'
        '.0260 -0.2646,1.0323 -0.2375,1.0323 -0.2188,1.0281 -0.1896,1.0115 -0.3333,0.8698ZM-0.3083,0.8448 -0.'
        '3125,0.8510 -0.1688,0.9906 -0.1604,0.9802 -0.1479,0.9490 -0.1500,0.9031 -0.1688,0.8677 -0.1875,0.849'
        '0 -0.2000,0.8406 -0.2375,0.8281 -0.2750,0.8302Z'
    ),
    '618.3A/5': (
        'M-0.4625,0.1344 -0.4583,0.1406 -0.4583,0.1531 -0.4625,0.1594 -0.4604,0.1573 0.4562,0.1573 0.4604,0.1'
        '594 0.4562,0.1531 0.4562,0.1406 0.4604,0.1344 0.4583,0.1365 -0.4604,0.1365Z'
    ),
    '618.4/0': (
        'M-0.4767,-0.8520 -0.4937,-0.8351 -0.5000,-0.8203 -0.5000,0.8161 -0.4937,0.8309 -0.4831,0.8436 -0.470'
        '4,0.8520 -0.4514,0.8562 -0.4493,0.8541 0.4619,0.8541 0.4725,0.8499 0.4894,0.8351 0.4979,0.8161 0.497'
        '9,-0.8203 0.4915,-0.8351 0.4810,-0.8478 0.4598,-0.8584 -0.4619,-0.8584Z'
    ),
    '618.4/1': (
        'M-0.4725,0.1522 -0.4746,0.1564 -0.4746,0.8140 -0.4641,0.8266 -0.4514,0.8309 0.4493,0.8309 0.4619,0.8'
        '266 0.4725,0.8140 0.4725,0.1564 0.4598,0.1416 0.4556,0.1395 -0.4577,0.1395ZM-0.2526,-0.0296 -0.2632,'
        '-0.0381 -0.4112,0.1099 -0.4070,0.1142 -0.3922,0.1142 -0.2526,-0.0254ZM-0.2780,-0.0507 -0.2886,-0.059'
        '2 -0.4598,0.1099 -0.4556,0.1142 -0.4408,0.1142ZM-0.3097,-0.0825 -0.3140,-0.0825 -0.4746,0.0782 -0.47'
        '46,0.0930 -0.4704,0.0973 -0.3013,-0.0719ZM-0.3330,-0.1099 -0.4746,0.0317 -0.4746,0.0465 -0.4704,0.05'
        '07 -0.3245,-0.0951 -0.3245,-0.0994ZM-0.1596,-0.1416 -0.2040,-0.0973 -0.1977,-0.0888 -0.1913,-0.0867 '
        '-0.1554,-0.1226 -0.1554,-0.1374ZM-0.1723,-0.1755 -0.2294,-0.1184 -0.2209,-0.1078 -0.1638,-0.1628ZM-0'
        '.0772,-0.1776 -0.0729,-0.1734 -0.0455,-0.1734 -0.0433,-0.1712 0.0412,-0.1712 0.0433,-0.1734 0.0793,-'
        '0.1734 0.0877,-0.1797 0.0877,-0.1839 0.0835,-0.1882 -0.0645,-0.1882ZM-0.0518,-0.2030 -0.0476,-0.1987'
        ' 0.0835,-0.1987 0.0877,-0.2030 0.0877,-0.2093 0.0835,-0.2135 -0.0412,-0.2135ZM-0.0899,-0.2030 -0.085'
        '6,-0.1987 -0.0793,-0.1987 -0.0687,-0.2093 -0.0729,-0.2135 -0.0856,-0.2135 -0.0899,-0.2093ZM-0.1744,-'
        '0.2220 -0.2526,-0.1438 -0.2526,-0.1395 -0.2442,-0.1311 -0.1702,-0.2030 -0.1702,-0.2178ZM-0.0243,-0.2'
        '304 -0.0201,-0.2262 0.0835,-0.2262 0.0877,-0.2347 0.0835,-0.2389 0.0603,-0.2389 0.0581,-0.2410 -0.01'
        '37,-0.2410ZM-0.0708,-0.2304 -0.0666,-0.2262 -0.0518,-0.2262 -0.0412,-0.2368 -0.0455,-0.2410 -0.0581,'
        '-0.2410ZM-0.1068,-0.2431 -0.1279,-0.2199 -0.1237,-0.2156 -0.1152,-0.2178 -0.1068,-0.2262 -0.1025,-0.'
        '2389ZM0.1152,-0.2622 0.1025,-0.2474 0.1025,-0.2304 0.1173,-0.2156 0.1364,-0.2156 0.1469,-0.2241 0.15'
        '12,-0.2326 0.1512,-0.2452 0.1469,-0.2537 0.1321,-0.2643ZM-0.1237,-0.2643 -0.1342,-0.2622 -0.1512,-0.'
        '2452 -0.1533,-0.2347 -0.1469,-0.2262 -0.1152,-0.2579ZM-0.1490,-0.2939 -0.2738,-0.1691 -0.2653,-0.156'
        '4 -0.1702,-0.2495 -0.1660,-0.2664 -0.1448,-0.2833 -0.1448,-0.2896ZM0.1152,-0.3531 0.1068,-0.3615 0.0'
        '433,-0.2981 0.0476,-0.2939 0.0772,-0.2939 0.0793,-0.2918 0.1152,-0.2939 0.1237,-0.3023 0.1237,-0.321'
        '4ZM0.0899,-0.3679 0.0856,-0.3721 0.0729,-0.3742 -0.0011,-0.3002 0.0032,-0.2960 0.0159,-0.2960ZM0.043'
        '3,-0.3700 0.0391,-0.3742 0.0243,-0.3742 -0.0518,-0.2981 -0.0476,-0.2939 -0.0328,-0.2939ZM-0.0032,-0.'
        '3700 -0.0074,-0.3742 -0.0222,-0.3742 -0.1004,-0.2960 -0.0962,-0.2918 -0.0793,-0.2939ZM-0.0539,-0.374'
        '2 -0.0687,-0.3742 -0.1237,-0.3192 -0.1258,-0.3044 -0.1216,-0.3002 -0.0497,-0.3700ZM0.1427,-0.4207 0.'
        '1385,-0.4249 0.1321,-0.4228 0.1237,-0.4249 0.0983,-0.3996 0.1131,-0.3911ZM0.1025,-0.4292 0.0920,-0.4'
        '397 0.0877,-0.4376 0.0518,-0.4017 0.0560,-0.3975 0.0708,-0.3975ZM0.0751,-0.4482 0.0708,-0.4524 0.056'
        '0,-0.4524 0.0053,-0.4017 0.0095,-0.3975 0.0243,-0.3975ZM0.0285,-0.4482 0.0243,-0.4524 0.0095,-0.4524'
        ' -0.0412,-0.4017 -0.0370,-0.3975 -0.0222,-0.3975ZM0.1152,-0.4630 0.1068,-0.4524 0.1195,-0.4461 0.130'
        '0,-0.4567 0.1258,-0.4609ZM0.1934,-0.4799 0.1871,-0.4757 0.1913,-0.4693 0.1977,-0.4757ZM0.1575,-0.503'
        '2 0.1533,-0.5032 0.1469,-0.4968 0.1490,-0.4863 0.1533,-0.4820 0.1660,-0.4926ZM0.1110,-0.5074 0.0941,'
        '-0.4884 0.0941,-0.4757 0.0983,-0.4715 0.1173,-0.4947ZM0.1342,-0.5159 0.1300,-0.5116 0.1342,-0.5074 0'
        '.1385,-0.5116ZM-0.1237,-0.5159 -0.1342,-0.5116 -0.1469,-0.4989 -0.1533,-0.4820 -0.1512,-0.4672 -0.14'
        '48,-0.4567 -0.1258,-0.4440 -0.1047,-0.4440 -0.0962,-0.4482 -0.0835,-0.4609 -0.0793,-0.4693 -0.0793,-'
        '0.4884 -0.0877,-0.5032 -0.0983,-0.4905 -0.0962,-0.4884 -0.0983,-0.4672 -0.1110,-0.4588 -0.1258,-0.46'
        '09 -0.1342,-0.4693 -0.1364,-0.4841 -0.1279,-0.4968 -0.1152,-0.5011 -0.1068,-0.5116 -0.1110,-0.5159ZM'
        '0.0941,-0.5307 0.0877,-0.5307 0.0708,-0.5137 0.0687,-0.4968 0.0729,-0.4926 0.0856,-0.5137 0.0983,-0.'
        '5264ZM0.2822,-0.5349 0.1237,-0.3784 0.1300,-0.3594 0.1427,-0.2854 0.1490,-0.2770 0.1554,-0.2748 0.16'
        '60,-0.2643 0.1681,-0.2579 0.1681,-0.1734 0.1533,-0.1543 0.1533,-0.0994 0.1364,-0.0888 0.1237,-0.0888'
        ' 0.1047,-0.0994 0.1047,-0.1501 0.1004,-0.1543 0.0666,-0.1501 -0.1025,-0.1522 -0.1068,-0.1480 -0.1068'
        ',-0.0994 -0.1237,-0.0888 -0.1385,-0.0888 -0.1554,-0.0994 -0.1765,-0.0782 -0.1723,-0.0719 -0.1152,-0.'
        '0444 -0.0708,-0.0317 -0.0307,-0.0254 0.0433,-0.0275 0.0793,-0.0338 0.1195,-0.0465 0.1681,-0.0698 0.2'
        '104,-0.0994 0.2442,-0.1311 0.2738,-0.1670 0.3013,-0.2135 0.3245,-0.2770 0.3330,-0.3256 0.3330,-0.393'
        '2 0.3288,-0.4228 0.3097,-0.4863 0.2907,-0.5243ZM0.2632,-0.5624 0.1977,-0.4989 0.1977,-0.4905 0.2040,'
        '-0.4820 0.2717,-0.5497 0.2717,-0.5539ZM0.0307,-0.5624 0.0137,-0.5772 0.0095,-0.5772 -0.0243,-0.5581 '
        '-0.0285,-0.5518 -0.0201,-0.5455 0.0053,-0.5370ZM0.2421,-0.5877 0.2378,-0.5877 0.1808,-0.5307 0.1808,'
        '-0.5264 0.1892,-0.5180 0.2505,-0.5772ZM0.2188,-0.6110 0.2146,-0.6110 0.1575,-0.5539 0.1575,-0.5455 0'
        '.1660,-0.5391 0.2273,-0.6004ZM0.2019,-0.6237 0.1892,-0.6321 0.1216,-0.5645 0.1258,-0.5603 0.1406,-0.'
        '5603ZM0.1702,-0.6469 0.1195,-0.6723 0.0687,-0.6871 0.0243,-0.6934 -0.0476,-0.6913 -0.0962,-0.6808 -0'
        '.1575,-0.6554 -0.1829,-0.6406 -0.2167,-0.6152 -0.2548,-0.5772 -0.2822,-0.5412 -0.3076,-0.4947 -0.324'
        '5,-0.4461 -0.3351,-0.3890 -0.3351,-0.3319 -0.3288,-0.2896 -0.3076,-0.2241 -0.2844,-0.1839 -0.1364,-0'
        '.3319 -0.1279,-0.3742 -0.1173,-0.3890 -0.1004,-0.3975 -0.0708,-0.3975 -0.0180,-0.4482 -0.0222,-0.452'
        '4 -0.0391,-0.4567 -0.0455,-0.4630 -0.0497,-0.4736 -0.0497,-0.4905 -0.0539,-0.5053 -0.0666,-0.5243 -0'
        '.0729,-0.5285 -0.0772,-0.5201 -0.0687,-0.5116 -0.0603,-0.4926 -0.0603,-0.4672 -0.0687,-0.4482 -0.077'
        '2,-0.4376 -0.0941,-0.4271 -0.1152,-0.4228 -0.1364,-0.4271 -0.1596,-0.4440 -0.1681,-0.4588 -0.1723,-0'
        '.4757 -0.1702,-0.4947 -0.1638,-0.5095 -0.1533,-0.5222 -0.1364,-0.5328 -0.1279,-0.5349 -0.0962,-0.532'
        '8 -0.0920,-0.5370 -0.0962,-0.5433 -0.1152,-0.5476 -0.1152,-0.5645 -0.0899,-0.5687 -0.0751,-0.5751 -0'
        '.0603,-0.5899 -0.0349,-0.6300 -0.0328,-0.6237 -0.0412,-0.5962 -0.0433,-0.5751 -0.0391,-0.5708 -0.030'
        '7,-0.5729 -0.0116,-0.5920 0.0011,-0.6131 0.0011,-0.6173 -0.0116,-0.6258 -0.0116,-0.6448 -0.0159,-0.6'
        '490 -0.0137,-0.6596 -0.0053,-0.6681 0.0095,-0.6702 0.0222,-0.6617 0.0264,-0.6512 0.0222,-0.6279 0.05'
        '18,-0.6131 0.0856,-0.5772 0.0877,-0.5666 0.0920,-0.5624 0.1744,-0.6427ZM0.4683,-0.7230 0.3414,-0.596'
        '2 0.3816,-0.5222 0.4027,-0.4588 0.4133,-0.3932 0.4133,-0.3277 0.4049,-0.2706 0.3816,-0.1987 0.3499,-'
        '0.1374 0.3118,-0.0867 0.2569,-0.0338 0.1913,0.0085 0.1321,0.0338 0.0624,0.0507 0.0222,0.0550 -0.0222'
        ',0.0550 -0.0983,0.0444 -0.1617,0.0233 -0.2125,-0.0021 -0.2336,-0.0169 -0.2378,-0.0169 -0.3647,0.1099'
        ' -0.3605,0.1142 0.4556,0.1142 0.4704,0.1015 0.4725,0.0973 0.4725,-0.7188ZM0.4683,-0.7696 0.3203,-0.6'
        '216 0.3309,-0.6110 0.4725,-0.7505 0.4725,-0.7653ZM0.4683,-0.8161 0.2992,-0.6490 0.3097,-0.6364 0.472'
        '5,-0.7992 0.4725,-0.8118ZM0.4514,-0.8351 0.4387,-0.8351 0.2759,-0.6702 0.2865,-0.6596 0.4556,-0.8288'
        'ZM0.4112,-0.8309 0.4070,-0.8351 0.3922,-0.8351 0.2505,-0.6913 0.2590,-0.6829 0.2632,-0.6829ZM0.3584,'
        '-0.8351 -0.4535,-0.8351 -0.4641,-0.8309 -0.4704,-0.8245 -0.4746,-0.8161 -0.4746,0.0000 -0.4704,0.004'
        '2 -0.3436,-0.1247 -0.3626,-0.1543 -0.3816,-0.1924 -0.4049,-0.2600 -0.4154,-0.3256 -0.4154,-0.3932 -0'
        '.4070,-0.4503 -0.3837,-0.5222 -0.3457,-0.5920 -0.3055,-0.6427 -0.2674,-0.6786 -0.2400,-0.6998 -0.174'
        '4,-0.7378 -0.1004,-0.7632 -0.0349,-0.7738 0.0349,-0.7738 0.1068,-0.7611 0.1617,-0.7421 0.2082,-0.718'
        '8 0.2336,-0.7019 0.3626,-0.8309Z'
    ),
    '618.4/2': (
        'M-0.1913,-0.0867 -0.2061,-0.0973 -0.2653,-0.0381 -0.2505,-0.0275ZM-0.2294,-0.1184 -0.2886,-0.0613 -0'
        '.2780,-0.0486 -0.2188,-0.1057ZM-0.2548,-0.1438 -0.3140,-0.0846 -0.3013,-0.0719 -0.2421,-0.1290ZM-0.1'
        '089,-0.1480 -0.1575,-0.0994 -0.1385,-0.0867 -0.1237,-0.0867 -0.1047,-0.0994 -0.1047,-0.1438ZM-0.2738'
        ',-0.1691 -0.3351,-0.1099 -0.3224,-0.0951 -0.2632,-0.1543ZM-0.0920,-0.2114 -0.1596,-0.1438 -0.1575,-0'
        '.1290 -0.1533,-0.1247 -0.0814,-0.1966ZM-0.0539,-0.2241 -0.0581,-0.2283 -0.0729,-0.2304 -0.0877,-0.21'
        '56 -0.0835,-0.2114 -0.0666,-0.2114ZM-0.1554,-0.2431 -0.1744,-0.2241 -0.1723,-0.2072 -0.1681,-0.2030 '
        '-0.1469,-0.2241 -0.1512,-0.2389ZM-0.0814,-0.2896 -0.0856,-0.2939 -0.1025,-0.2960 -0.1321,-0.2664 -0.'
        '1279,-0.2622 -0.1131,-0.2579ZM-0.0370,-0.2960 -0.0518,-0.2981 -0.1068,-0.2431 -0.1047,-0.2389 -0.108'
        '9,-0.2262 -0.1195,-0.2178 -0.1300,-0.2199 -0.1723,-0.1776 -0.1702,-0.1691 -0.1617,-0.1628 -0.0328,-0'
        '.2918ZM0.0159,-0.2939 0.0116,-0.2981 -0.0032,-0.3002 -0.0603,-0.2431 -0.0560,-0.2389 -0.0412,-0.2368'
        'ZM-0.1279,-0.3171 -0.1469,-0.2981 -0.1448,-0.2960 -0.1469,-0.2833 -0.1681,-0.2664 -0.1723,-0.2558 -0'
        '.1681,-0.2495 -0.1195,-0.2981 -0.1237,-0.3044 -0.1237,-0.3129ZM0.1237,-0.3784 0.1047,-0.3615 0.1152,'
        '-0.3488 0.1216,-0.3214 0.1216,-0.3023 0.1152,-0.2960 0.0793,-0.2939 0.0412,-0.2981 -0.0137,-0.2431 -'
        '0.0095,-0.2389 0.0835,-0.2368 0.0856,-0.2347 0.0835,-0.2283 -0.0243,-0.2283 -0.0264,-0.2304 -0.0412,'
        '-0.2156 -0.0370,-0.2114 0.0835,-0.2114 0.0856,-0.2093 0.0835,-0.2008 -0.0518,-0.2008 -0.0539,-0.2030'
        ' -0.0666,-0.1903 -0.0624,-0.1860 0.0835,-0.1860 0.0856,-0.1797 0.0793,-0.1755 0.0433,-0.1755 0.0412,'
        '-0.1734 -0.0433,-0.1734 -0.0793,-0.1776 -0.1025,-0.1543 -0.0983,-0.1501 0.0666,-0.1480 0.1004,-0.152'
        '2 0.1025,-0.1501 0.1025,-0.0994 0.1068,-0.0951 0.1237,-0.0867 0.1364,-0.0867 0.1554,-0.0994 0.1554,-'
        '0.1543 0.1702,-0.1734 0.1702,-0.2579 0.1681,-0.2643 0.1448,-0.2854 0.1321,-0.3594 0.1279,-0.3742ZM0.'
        '1152,-0.2600 0.1321,-0.2622 0.1448,-0.2537 0.1490,-0.2452 0.1490,-0.2326 0.1448,-0.2241 0.1364,-0.21'
        '78 0.1173,-0.2178 0.1068,-0.2262 0.1047,-0.2474ZM0.1131,-0.3911 0.0962,-0.3996 0.0729,-0.3763 0.0899'
        ',-0.3679ZM-0.0751,-0.3996 -0.1004,-0.3996 -0.1110,-0.3953 -0.1237,-0.3848 -0.1300,-0.3742 -0.1364,-0'
        '.3383 -0.1321,-0.3340 -0.0708,-0.3953ZM0.0708,-0.3953 0.0666,-0.3996 0.0518,-0.4017 0.0264,-0.3763 0'
        '.0307,-0.3721 0.0455,-0.3700ZM0.0243,-0.3953 0.0201,-0.3996 0.0032,-0.4017 -0.0222,-0.3763 -0.0180,-'
        '0.3721 -0.0011,-0.3700ZM-0.0222,-0.3953 -0.0264,-0.3996 -0.0433,-0.4017 -0.0687,-0.3763 -0.0645,-0.3'
        '721 -0.0476,-0.3700ZM0.1068,-0.4545 0.0899,-0.4397 0.1025,-0.4292 0.1195,-0.4440ZM0.0920,-0.4905 0.0'
        '560,-0.4545 0.0603,-0.4503 0.0772,-0.4482 0.0983,-0.4693 0.0962,-0.4863ZM0.1469,-0.4947 0.1152,-0.46'
        '51 0.1216,-0.4588 0.1300,-0.4545 0.1554,-0.4799ZM0.1956,-0.4989 0.1554,-0.4588 0.1575,-0.4567 0.1533'
        ',-0.4524 0.1512,-0.4545 0.1237,-0.4271 0.1300,-0.4207 0.1342,-0.4228 0.1427,-0.4207 0.1892,-0.4672 0'
        '.1871,-0.4693 0.1913,-0.4778 0.1998,-0.4757 0.2040,-0.4799 0.1998,-0.4947ZM0.0666,-0.5116 0.0095,-0.'
        '4545 0.0137,-0.4503 0.0307,-0.4482 0.0729,-0.4905 0.0708,-0.5074ZM0.1808,-0.5285 0.1554,-0.5053 0.16'
        '60,-0.4905 0.1913,-0.5159ZM0.1554,-0.5539 0.1110,-0.5095 0.1152,-0.4989 0.1110,-0.4905 0.1152,-0.486'
        '3 0.1342,-0.5053 0.1321,-0.5116 0.1342,-0.5137 0.1406,-0.5116 0.1681,-0.5391 0.1596,-0.5455ZM0.1342,'
        '-0.5624 0.1195,-0.5645 0.0877,-0.5328 0.0962,-0.5264 0.0772,-0.5032 0.0814,-0.4989 0.1385,-0.5581ZM0'
        '.3414,-0.5962 0.2801,-0.5370 0.3076,-0.4863 0.3266,-0.4228 0.3309,-0.3932 0.3309,-0.3256 0.3245,-0.2'
        '854 0.3118,-0.2431 0.2970,-0.2093 0.2717,-0.1670 0.2421,-0.1311 0.2104,-0.1015 0.1681,-0.0719 0.1195'
        ',-0.0486 0.0877,-0.0381 0.0433,-0.0296 -0.0307,-0.0275 -0.0708,-0.0338 -0.1258,-0.0507 -0.1786,-0.07'
        '82 -0.2378,-0.0190 -0.2294,-0.0106 -0.1617,0.0254 -0.0983,0.0465 -0.0222,0.0571 0.0222,0.0571 0.0624'
        ',0.0529 0.1321,0.0359 0.1913,0.0106 0.2569,-0.0317 0.3140,-0.0867 0.3520,-0.1374 0.3837,-0.1987 0.40'
        '70,-0.2706 0.4154,-0.3277 0.4154,-0.3932 0.4049,-0.4588 0.3837,-0.5222 0.3605,-0.5687ZM0.3203,-0.623'
        '7 0.2611,-0.5645 0.2717,-0.5518 0.3309,-0.6089 0.3288,-0.6152ZM0.2992,-0.6490 0.2400,-0.5899 0.2505,'
        '-0.5772 0.3097,-0.6342 0.3076,-0.6406ZM0.2759,-0.6723 0.2146,-0.6131 0.2273,-0.6004 0.2886,-0.6596ZM'
        '0.0180,-0.6681 0.0095,-0.6723 -0.0053,-0.6702 -0.0159,-0.6596 -0.0180,-0.6512 -0.0137,-0.6469 -0.013'
        '7,-0.6258 -0.0032,-0.6195 -0.0011,-0.6131 -0.0137,-0.5920 -0.0349,-0.5729 -0.0412,-0.5751 -0.0391,-0'
        '.5962 -0.0307,-0.6237 -0.0349,-0.6321 -0.0624,-0.5899 -0.0751,-0.5772 -0.0899,-0.5708 -0.1131,-0.568'
        '7 -0.1173,-0.5645 -0.1173,-0.5476 -0.1131,-0.5433 -0.0962,-0.5412 -0.0941,-0.5391 -0.0962,-0.5349 -0'
        '.1025,-0.5370 -0.1364,-0.5349 -0.1533,-0.5243 -0.1660,-0.5095 -0.1723,-0.4947 -0.1744,-0.4757 -0.166'
        '0,-0.4503 -0.1512,-0.4334 -0.1364,-0.4249 -0.1152,-0.4207 -0.0941,-0.4249 -0.0729,-0.4397 -0.0581,-0'
        '.4672 -0.0581,-0.4926 -0.0666,-0.5116 -0.0751,-0.5201 -0.0729,-0.5264 -0.0687,-0.5243 -0.0560,-0.505'
        '3 -0.0518,-0.4905 -0.0518,-0.4736 -0.0476,-0.4630 -0.0349,-0.4524 -0.0159,-0.4503 0.0941,-0.5603 0.0'
        '877,-0.5772 0.0518,-0.6152 0.0243,-0.6279 0.0285,-0.6512 0.0243,-0.6617ZM-0.1300,-0.5116 -0.1237,-0.'
        '5137 -0.1089,-0.5116 -0.1152,-0.5032 -0.1279,-0.4989 -0.1385,-0.4841 -0.1364,-0.4693 -0.1258,-0.4588'
        ' -0.1110,-0.4567 -0.1025,-0.4609 -0.0941,-0.4715 -0.0962,-0.4905 -0.0877,-0.5011 -0.0835,-0.4947 -0.'
        '0814,-0.4693 -0.0856,-0.4609 -0.1047,-0.4461 -0.1258,-0.4461 -0.1406,-0.4545 -0.1490,-0.4672 -0.1512'
        ',-0.4757 -0.1490,-0.4905 -0.1448,-0.4989ZM0.0285,-0.5624 0.0053,-0.5391 -0.0264,-0.5518 -0.0243,-0.5'
        '560 0.0095,-0.5751 0.0137,-0.5751ZM0.2548,-0.6892 0.2484,-0.6934 0.1892,-0.6321 0.2040,-0.6216 0.261'
        '1,-0.6808ZM0.2315,-0.7061 0.1617,-0.7442 0.1068,-0.7632 0.0349,-0.7759 -0.0349,-0.7759 -0.1004,-0.76'
        '53 -0.1744,-0.7400 -0.2400,-0.7019 -0.2844,-0.6660 -0.3224,-0.6258 -0.3626,-0.5687 -0.3943,-0.5011 -'
        '0.4091,-0.4503 -0.4154,-0.4123 -0.4175,-0.3256 -0.4070,-0.2600 -0.3837,-0.1924 -0.3499,-0.1311 -0.34'
        '14,-0.1247 -0.2822,-0.1839 -0.3055,-0.2241 -0.3182,-0.2579 -0.3288,-0.3002 -0.3330,-0.3319 -0.3330,-'
        '0.3890 -0.3224,-0.4461 -0.3055,-0.4947 -0.2801,-0.5412 -0.2526,-0.5772 -0.2167,-0.6131 -0.1829,-0.63'
        '85 -0.1364,-0.6638 -0.0814,-0.6829 -0.0307,-0.6913 0.0243,-0.6913 0.0687,-0.6850 0.1195,-0.6702 0.15'
        '96,-0.6512 0.1744,-0.6406 0.2357,-0.7019Z'
    ),
    '618.4/3': (
        'M-0.4577,0.1395 -0.4556,0.1374 0.4535,0.1374 0.4577,0.1395 0.4535,0.1332 0.4535,0.1205 0.4577,0.1142'
        ' 0.4535,0.1163 -0.3668,0.1163 -0.3689,0.1121 -0.2421,-0.0148 -0.2526,-0.0233 -0.3922,0.1163 -0.4133,'
        '0.1163 -0.4154,0.1121 -0.2674,-0.0359 -0.2780,-0.0465 -0.4408,0.1163 -0.4535,0.1163 -0.4535,0.1311ZM'
        '-0.2907,-0.0592 -0.3013,-0.0698 -0.4683,0.0994 -0.4577,0.1057ZM-0.3245,-0.0930 -0.4704,0.0529 -0.468'
        '3,0.0698 -0.3161,-0.0825ZM-0.1596,-0.1163 -0.1871,-0.0888 -0.1765,-0.0803 -0.1554,-0.1015 -0.1596,-0'
        '.1078ZM-0.3436,-0.1226 -0.4704,0.0063 -0.4683,0.0233 -0.3351,-0.1099ZM-0.1660,-0.1586 -0.2146,-0.109'
        '9 -0.2040,-0.0994 -0.1596,-0.1438ZM-0.1765,-0.1945 -0.2400,-0.1311 -0.2294,-0.1205 -0.1723,-0.1776 -'
        '0.1765,-0.1839ZM-0.1068,-0.2178 -0.0920,-0.2114 -0.0729,-0.2304 -0.0814,-0.2283 -0.0941,-0.2304ZM-0.'
        '0201,-0.2368 -0.0264,-0.2347 -0.0391,-0.2368 -0.0814,-0.1966 -0.0751,-0.1818ZM-0.1152,-0.2537 -0.149'
        '0,-0.2220 -0.1448,-0.2241 -0.1300,-0.2199 -0.1089,-0.2431ZM0.0497,-0.4482 0.0433,-0.4461 0.0307,-0.4'
        '482 -0.2611,-0.1564 -0.2526,-0.1459ZM0.0032,-0.4482 -0.0032,-0.4461 -0.0159,-0.4482 -0.2822,-0.1839 '
        '-0.2738,-0.1712ZM0.2717,-0.5476 0.0243,-0.3002 0.0285,-0.3023 0.0412,-0.2981 0.2780,-0.5349ZM0.2505,'
        '-0.5751 -0.0243,-0.3002 -0.0159,-0.3023 -0.0032,-0.3002 0.2590,-0.5624ZM0.2273,-0.5983 -0.0729,-0.29'
        '81 -0.0666,-0.3002 -0.0539,-0.2981 0.0264,-0.3763 0.2357,-0.5877ZM0.2125,-0.6110 0.2019,-0.6195 0.13'
        '85,-0.5581 0.0751,-0.4926 0.0793,-0.4778ZM0.1744,-0.6385 0.0941,-0.5603 0.0962,-0.5560 0.0941,-0.539'
        '1 0.1850,-0.6300ZM0.4662,-0.7421 0.3351,-0.6110 0.3414,-0.5983 0.4683,-0.7252ZM0.4662,-0.7907 0.3118'
        ',-0.6364 0.3203,-0.6258 0.4683,-0.7717ZM0.4577,-0.8266 0.2907,-0.6617 0.2992,-0.6512 0.4662,-0.8161Z'
        'M0.4323,-0.8309 0.4260,-0.8288 0.4133,-0.8309 0.2653,-0.6829 0.2759,-0.6744ZM0.3858,-0.8309 0.3795,-'
        '0.8288 0.3668,-0.8309 0.2400,-0.7019 0.2505,-0.6956Z'
    ),
    '622.9/0': (
        'M-1.0205,-0.4224 -1.0297,-0.3950 -1.0297,0.3904 -1.0114,0.4361 -0.9749,0.4726 -0.9475,0.4863 -0.9064'
        ',0.4954 0.8973,0.4954 0.9292,0.4909 0.9612,0.4772 0.9977,0.4452 1.0160,0.4132 1.0251,0.3813 1.0251,-'
        '0.3858 1.0160,-0.4178 0.9977,-0.4498 0.9795,-0.4680 0.9384,-0.4909 0.8973,-0.5000 -0.9018,-0.5000 -0'
        '.9658,-0.4817 -1.0068,-0.4452Z'
    ),
    '622.9/1': (
        'M-0.9612,-0.3950 -0.9658,-0.3813 -0.9658,0.3767 -0.9566,0.3995 -0.9201,0.4269 -0.9018,0.4315 0.8973,'
        '0.4315 0.9338,0.4178 0.9566,0.3904 0.9612,0.3721 0.9612,-0.3767 0.9475,-0.4087 0.9155,-0.4315 0.8973'
        ',-0.4361 -0.9064,-0.4361 -0.9384,-0.4224Z'
    ),
    '627.1/0': (
        'M-1.3128,-0.5000 -1.3128,0.3851 -1.3043,0.4149 -1.2787,0.4532 -1.2319,0.4872 -1.1979,0.4957 1.1851,0'
        '.4957 1.2106,0.4915 1.2489,0.4745 1.2745,0.4532 1.3000,0.4149 1.3085,0.3851 1.3085,-0.5000Z'
    ),
    '627.1/1': (
        'M-1.2447,-0.3638 -1.2489,-0.3213 -1.2489,0.3596 -1.2362,0.3979 -1.2149,0.4191 -1.1936,0.4277 1.1894,'
        '0.4277 1.2106,0.4191 1.2319,0.3979 1.2404,0.3766 1.2404,-0.3638 1.2106,-0.4021 1.1894,-0.4106 -1.193'
        '6,-0.4106 -1.2149,-0.4021Z'
    ),
    '627.1/2': (
        'M-1.3128,-0.4957 -1.3128,0.3936 -1.2830,0.4489 -1.2319,0.4872 -1.2064,0.4957 1.1979,0.4957 1.2489,0.'
        '4745 1.2872,0.4362 1.3000,0.4149 1.3085,0.3894 1.3085,-0.4957 1.3000,-0.5043 1.2277,-0.5043 1.2149,-'
        '0.4915 1.1766,-0.4787 -1.1766,-0.4787 -1.1979,-0.4830 -1.2319,-0.5043 -1.3043,-0.5043ZM-1.2447,-0.35'
        '96 -1.2191,-0.3979 -1.1894,-0.4106 1.1851,-0.4106 1.2021,-0.4064 1.2319,-0.3809 1.2404,-0.3638 1.240'
        '4,0.3766 1.2319,0.3979 1.2149,0.4149 1.1851,0.4277 -1.1894,0.4277 -1.2064,0.4234 -1.2362,0.3979 -1.2'
        '447,0.3766Z'
    ),
    '637.1/0': (
        'M-0.5152,-0.4724 -0.5235,-0.4530 -0.5235,0.4530 -0.5180,0.4669 -0.5014,0.4862 -0.4793,0.4972 0.4738,'
        '0.4972 0.4876,0.4917 0.5041,0.4779 0.5152,0.4586 0.5207,0.4337 0.5207,-0.4365 0.5097,-0.4724 0.4931,'
        '-0.4890 0.4682,-0.5000 -0.4738,-0.5000 -0.4959,-0.4917Z'
    ),
    '637.1/1': (
        'M-0.4931,-0.4558 -0.4986,-0.4420 -0.4986,0.4392 -0.4931,0.4530 -0.4738,0.4696 0.4682,0.4696 0.4876,0'
        '.4530 0.4903,0.4448 0.4903,-0.4475 0.4765,-0.4669 0.4655,-0.4724 -0.4682,-0.4724 -0.4820,-0.4669ZM-0'
        '.2058,-0.3895 -0.1644,-0.3895 -0.1229,-0.3812 -0.0843,-0.3646 -0.0483,-0.3398 -0.0262,-0.3177 -0.001'
        '4,-0.2818 0.0152,-0.2431 0.0235,-0.2044 0.0235,-0.1575 0.0152,-0.1188 -0.0041,-0.0746 -0.0235,-0.047'
        '0 -0.0511,-0.0193 -0.0843,0.0028 -0.1229,0.0193 -0.1616,0.0276 -0.2058,0.0276 -0.2472,0.0193 -0.2859'
        ',0.0028 -0.3218,-0.0221 -0.3467,-0.0470 -0.3660,-0.0746 -0.3798,-0.1022 -0.3936,-0.1575 -0.3936,-0.2'
        '044 -0.3854,-0.2431 -0.3660,-0.2873 -0.3439,-0.3177 -0.3246,-0.3370 -0.2859,-0.3646 -0.2472,-0.3812Z'
    ),
    '637.1/2': (
        'M-0.3191,-0.2790 -0.3301,-0.2680 -0.3439,-0.2403 -0.3550,-0.1934 -0.3494,-0.1354 -0.3191,-0.0746 -0.'
        '2914,-0.0470 -0.2666,-0.0304 -0.2113,-0.0110 -0.1450,-0.0138 -0.1202,-0.0221 -0.0898,-0.0387 -0.0843'
        ',-0.0470ZM-0.2749,-0.3232 -0.2859,-0.3122 -0.0511,-0.0773 -0.0318,-0.1050 -0.0207,-0.1354 -0.0152,-0'
        '.1630 -0.0152,-0.1961 -0.0262,-0.2403 -0.0539,-0.2873 -0.0787,-0.3122 -0.1202,-0.3370 -0.1616,-0.348'
        '1 -0.2224,-0.3453 -0.2500,-0.3370Z'
    ),
    '637.1/3': (
        'M-0.2058,-0.3895 -0.2472,-0.3812 -0.2859,-0.3646 -0.3273,-0.3343 -0.3550,-0.3039 -0.3798,-0.2597 -0.'
        '3936,-0.2072 -0.3936,-0.1547 -0.3798,-0.1022 -0.3660,-0.0746 -0.3439,-0.0442 -0.3108,-0.0138 -0.2859'
        ',0.0028 -0.2472,0.0193 -0.2086,0.0276 -0.1616,0.0276 -0.1229,0.0193 -0.0843,0.0028 -0.0456,-0.0249 -'
        '0.0152,-0.0580 0.0097,-0.1022 0.0235,-0.1547 0.0235,-0.2072 0.0097,-0.2597 -0.0041,-0.2873 -0.0290,-'
        '0.3204 -0.0594,-0.3481 -0.0843,-0.3646 -0.1229,-0.3812 -0.1616,-0.3895ZM-0.3273,-0.2680 -0.3191,-0.2'
        '762 -0.0870,-0.0442 -0.1202,-0.0249 -0.1450,-0.0166 -0.2113,-0.0138 -0.2500,-0.0249 -0.2914,-0.0497 '
        '-0.3163,-0.0746 -0.3412,-0.1188 -0.3494,-0.1464 -0.3522,-0.1685 -0.3494,-0.2127 -0.3412,-0.2403ZM-0.'
        '2749,-0.3204 -0.2500,-0.3343 -0.2224,-0.3425 -0.1616,-0.3453 -0.1367,-0.3398 -0.1036,-0.3260 -0.0787'
        ',-0.3094 -0.0566,-0.2873 -0.0290,-0.2403 -0.0180,-0.1961 -0.0180,-0.1630 -0.0318,-0.1105 -0.0511,-0.'
        '0801 -0.2831,-0.3122Z'
    ),
    '637.1/4': (
        'M-0.4986,-0.4365 -0.5124,-0.4227 -0.5124,0.4199 -0.4986,0.4337Z'
    ),
    '637.2/0': (
        'M-0.4780,-0.6401 -0.4918,-0.6236 -0.5000,-0.6016 -0.5000,0.6016 -0.4863,0.6291 -0.4698,0.6429 -0.447'
        '8,0.6511 0.4451,0.6511 0.4725,0.6401 0.4863,0.6264 0.4973,0.6044 0.4973,-0.6044 0.4863,-0.6291 0.467'
        '0,-0.6456 0.4451,-0.6538 -0.4478,-0.6538Z'
    ),
    '637.2/1': (
        'M-0.4588,-0.6181 -0.4725,-0.5962 -0.4725,0.5934 -0.4670,0.6071 -0.4560,0.6181 -0.4423,0.6236 0.4396,'
        '0.6236 0.4533,0.6181 0.4643,0.6071 0.4698,0.5934 0.4698,-0.5962 0.4643,-0.6099 0.4478,-0.6236 -0.450'
        '5,-0.6236ZM-0.0577,-0.2005 -0.0302,-0.2060 0.0275,-0.2060 0.0769,-0.1923 0.0989,-0.1813 0.1429,-0.14'
        '84 0.1621,-0.1264 0.1951,-0.0604 0.2005,-0.0357 0.2005,0.0275 0.1923,0.0604 0.1731,0.1016 0.1593,0.1'
        '209 0.1236,0.1566 0.0989,0.1731 0.0522,0.1923 0.0220,0.1978 -0.0275,0.1978 -0.0659,0.1896 -0.0989,0.'
        '1758 -0.1319,0.1538 -0.1593,0.1264 -0.1786,0.0989 -0.1978,0.0549 -0.2060,0.0165 -0.2060,-0.0247 -0.1'
        '978,-0.0632 -0.1786,-0.1071 -0.1593,-0.1346 -0.1319,-0.1621 -0.1071,-0.1786Z'
    ),
    '637.2/2': (
        'M-0.1346,-0.0989 -0.1511,-0.0769 -0.1621,-0.0495 -0.1676,-0.0220 -0.1676,0.0137 -0.1538,0.0632 -0.13'
        '19,0.0989 -0.0879,0.1374 -0.0604,0.1511 -0.0302,0.1593 0.0000,0.1621 0.0385,0.1566 0.0632,0.1484 0.0'
        '879,0.1346 0.0962,0.1236 -0.1264,-0.0962ZM-0.0962,-0.1401 -0.1016,-0.1346 0.1291,0.0934 0.1511,0.060'
        '4 0.1621,0.0247 0.1621,-0.0330 0.1511,-0.0687 0.1319,-0.1016 0.0962,-0.1374 0.0797,-0.1484 0.0247,-0'
        '.1676 -0.0027,-0.1703 -0.0302,-0.1676 -0.0604,-0.1593Z'
    ),
    '637.2/3': (
        'M-0.0357,-0.2060 -0.0824,-0.1923 -0.1126,-0.1758 -0.1346,-0.1593 -0.1676,-0.1236 -0.1923,-0.0797 -0.'
        '2060,-0.0247 -0.2033,0.0330 -0.1923,0.0714 -0.1676,0.1154 -0.1346,0.1511 -0.1126,0.1676 -0.0742,0.18'
        '68 -0.0330,0.1978 0.0440,0.1951 0.0714,0.1868 0.1126,0.1648 0.1676,0.1099 0.1896,0.0687 0.1978,0.041'
        '2 0.2033,0.0000 0.2005,-0.0357 0.1896,-0.0769 0.1731,-0.1099 0.1593,-0.1291 0.1126,-0.1731 0.0714,-0'
        '.1951 0.0330,-0.2060 0.0055,-0.2060 0.0027,-0.2088ZM-0.1401,-0.0907 -0.1346,-0.0962 -0.1264,-0.0934 '
        '0.0934,0.1264 0.0632,0.1456 0.0385,0.1538 -0.0027,0.1593 -0.0604,0.1484 -0.1071,0.1209 -0.1291,0.098'
        '9 -0.1456,0.0742 -0.1593,0.0412 -0.1648,0.0137 -0.1621,-0.0385ZM-0.0989,-0.1346 -0.0604,-0.1566 -0.0'
        '055,-0.1676 0.0385,-0.1621 0.0632,-0.1538 0.0962,-0.1346 0.1346,-0.0934 0.1484,-0.0687 0.1593,-0.033'
        '0 0.1593,0.0247 0.1484,0.0604 0.1291,0.0907Z'
    ),
    '637.3/0': (
        'M-0.9577,-0.4462 -0.9615,-0.4346 -0.9615,0.4346 -0.9462,0.4654 -0.9115,0.4923 -0.9000,0.4962 0.8962,'
        '0.4962 0.9231,0.4846 0.9538,0.4462 0.9577,0.4346 0.9577,-0.4346 0.9385,-0.4731 0.9038,-0.4962 0.8923'
        ',-0.5000 -0.9000,-0.5000 -0.9346,-0.4808Z'
    ),
    '637.3/1': (
        'M-0.9231,-0.4308 -0.9231,0.4269 -0.9154,0.4423 -0.8808,0.4615 0.8769,0.4615 0.8962,0.4538 0.9192,0.4'
        '269 0.9192,-0.4308 0.8885,-0.4615 -0.8923,-0.4615ZM-0.0231,-0.3885 0.0269,-0.3846 0.0692,-0.3615 0.0'
        '962,-0.3269 0.1077,-0.2923 0.1077,-0.2577 0.0885,-0.2115 0.0577,-0.1808 0.0192,-0.1654 -0.0308,-0.16'
        '54 -0.0654,-0.1808 -0.0962,-0.2077 -0.1154,-0.2500 -0.1192,-0.2731 -0.1154,-0.3038 -0.1000,-0.3385 -'
        '0.0692,-0.3692Z'
    ),
    '637.3/2': (
        'M-0.0769,-0.3269 -0.0885,-0.3154 -0.0962,-0.2923 -0.0962,-0.2577 -0.0808,-0.2231 -0.0538,-0.1962 -0.'
        '0269,-0.1846 0.0000,-0.1808 0.0385,-0.1923 0.0500,-0.2038ZM-0.0500,-0.3577 -0.0577,-0.3462 0.0692,-0'
        '.2192 0.0885,-0.2538 0.0885,-0.2962 0.0731,-0.3308 0.0538,-0.3500 0.0154,-0.3692 -0.0192,-0.3692Z'
    ),
    '637.3/3': (
        'M-0.0269,-0.3885 -0.0692,-0.3692 -0.1000,-0.3385 -0.1192,-0.2846 -0.1154,-0.2462 -0.0962,-0.2077 -0.'
        '0615,-0.1769 -0.0115,-0.1615 0.0231,-0.1654 0.0577,-0.1808 0.0885,-0.2115 0.1077,-0.2538 0.1077,-0.2'
        '962 0.0923,-0.3346 0.0654,-0.3654 0.0192,-0.3885ZM-0.0846,-0.3154 -0.0731,-0.3231 0.0462,-0.2038 0.0'
        '231,-0.1885 0.0000,-0.1846 -0.0269,-0.1885 -0.0538,-0.2000 -0.0769,-0.2231 -0.0923,-0.2577 -0.0923,-'
        '0.2923ZM-0.0500,-0.3538 -0.0192,-0.3654 0.0154,-0.3654 0.0423,-0.3538 0.0692,-0.3308 0.0846,-0.2962 '
        '0.0846,-0.2538 0.0692,-0.2231 -0.0538,-0.3462Z'
    ),
    '637.3/4': (
        'M-0.8615,0.4615 -0.8423,0.4808 0.8385,0.4808 0.8577,0.4615Z'
    ),
    '638.1/0': (
        'M-0.6036,-0.4845 -0.6140,-0.4689 -0.6192,-0.4508 -0.6192,0.4456 -0.6140,0.4637 -0.6010,0.4819 -0.585'
        '5,0.4922 -0.5622,0.4974 0.5596,0.4974 0.5751,0.4948 0.5907,0.4870 0.6062,0.4715 0.6140,0.4560 0.6166'
        ',0.4404 0.6166,-0.4456 0.6062,-0.4767 0.5933,-0.4896 0.5725,-0.5000 -0.5751,-0.5000Z'
    ),
    '638.1/1': (
        'M0.3653,0.0155 0.3497,0.0181 0.3446,0.0285 0.3549,0.0363 0.3653,0.0337 0.3705,0.0285 0.3705,0.0207ZM'
        '-0.5881,-0.4560 -0.5907,-0.4508 -0.5907,0.4456 -0.5803,0.4611 -0.5622,0.4689 0.5570,0.4689 0.5699,0.'
        '4663 0.5855,0.4508 0.5881,0.4404 0.5881,-0.4456 0.5829,-0.4585 0.5674,-0.4715 -0.5699,-0.4715ZM-0.15'
        '28,0.3420 -0.0777,0.2694 -0.0078,0.2694 -0.0052,0.2720 -0.0466,0.3135 -0.0415,0.3187 0.1477,0.3187 0'
        '.1503,0.3212 0.1503,0.3679 0.1477,0.3705 -0.0415,0.3705 -0.0466,0.3756 -0.0052,0.4171 -0.0078,0.4197'
        ' -0.0777,0.4197ZM0.4119,-0.0233 0.4145,-0.0259 0.4352,-0.0233 0.4508,-0.0285 0.4689,-0.0207 0.4845,-'
        '0.0285 0.4974,-0.0285 0.5104,-0.0233 0.5207,-0.0104 0.5207,0.0466 0.5181,0.0492 0.5026,0.0466 0.5026'
        ',0.0052 0.4948,-0.0078 0.4845,-0.0078 0.4767,0.0000 0.4767,0.0466 0.4585,0.0492 0.4560,0.0466 0.4560'
        ',0.0000 0.4482,-0.0078 0.4404,-0.0078 0.4326,0.0000 0.4326,0.0466 0.4145,0.0492 0.4119,0.0466ZM0.334'
        '2,-0.0233 0.3497,-0.0285 0.3731,-0.0285 0.3886,-0.0181 0.3912,0.0311 0.3990,0.0389 0.3912,0.0518 0.3'
        '808,0.0518 0.3756,0.0466 0.3627,0.0518 0.3446,0.0518 0.3264,0.0389 0.3238,0.0337 0.3264,0.0130 0.336'
        '8,0.0052 0.3653,0.0000 0.3705,-0.0052 0.3653,-0.0104 0.3368,-0.0052 0.3290,-0.0155Z'
    ),
    '638.1/2': (
        'M-0.0907,0.4041 -0.0751,0.4197 -0.0078,0.4197 -0.0466,0.3782 -0.0518,0.3912 -0.0622,0.4016 -0.0803,0'
        '.4067ZM-0.1399,0.3342 -0.1503,0.3446 -0.1399,0.3549 -0.1425,0.3523ZM-0.0389,0.3212 -0.0285,0.3368 -0'
        '.0285,0.3523 -0.0389,0.3679 0.1477,0.3679 0.1477,0.3212ZM-0.0907,0.2850 -0.0803,0.2824 -0.0622,0.287'
        '6 -0.0518,0.2979 -0.0466,0.3109 -0.0078,0.2720 -0.0777,0.2720ZM0.4145,-0.0233 0.4145,0.0466 0.4301,0'
        '.0466 0.4301,0.0000 0.4404,-0.0104 0.4508,-0.0104 0.4585,0.0000 0.4585,0.0466 0.4741,0.0466 0.4741,0'
        '.0000 0.4845,-0.0104 0.4948,-0.0104 0.5026,-0.0026 0.5052,0.0466 0.5181,0.0466 0.5181,-0.0104 0.5130'
        ',-0.0181 0.4974,-0.0259 0.4845,-0.0259 0.4715,-0.0181 0.4508,-0.0259 0.4352,-0.0207ZM0.3342,-0.0207 '
        '0.3316,-0.0155 0.3368,-0.0078 0.3653,-0.0130 0.3731,-0.0026 0.3679,0.0026 0.3368,0.0078 0.3290,0.013'
        '0 0.3264,0.0181 0.3290,0.0389 0.3446,0.0492 0.3627,0.0492 0.3705,0.0440 0.3808,0.0492 0.3912,0.0492 '
        '0.3964,0.0389 0.3886,0.0337 0.3860,-0.0181 0.3731,-0.0259 0.3497,-0.0259ZM0.3420,0.0233 0.3497,0.015'
        '5 0.3679,0.0130 0.3731,0.0181 0.3731,0.0311 0.3679,0.0363 0.3549,0.0389 0.3420,0.0311Z'
    ),
    '640.2A/0': (
        'M-0.4839,-0.6159 -0.4940,-0.6038 -0.5000,-0.5837 -0.5000,0.5817 -0.4960,0.5978 -0.4879,0.6099 -0.459'
        '7,0.6240 0.4577,0.6240 0.4718,0.6200 0.4839,0.6119 0.4919,0.6018 0.4980,0.5837 0.4980,-0.5877 0.4899'
        ',-0.6079 0.4798,-0.6179 0.4597,-0.6260 -0.4617,-0.6260Z'
    ),
    '640.2A/1': (
        'M-0.0383,-0.3639 -0.0464,-0.3599 -0.0484,-0.3518 -0.0605,-0.3518 -0.0645,-0.3478 -0.0625,-0.3337 -0.'
        '0504,-0.3236 -0.0343,-0.3256 -0.0242,-0.3377 -0.0262,-0.3538ZM-0.3427,-0.3639 -0.3548,-0.3558 -0.358'
        '9,-0.3478 -0.3589,-0.3397 -0.3488,-0.3256 -0.3327,-0.3236 -0.3185,-0.3357 -0.3165,-0.3458 -0.3286,-0'
        '.3619ZM-0.3669,-0.4849 -0.3750,-0.4768 -0.3810,-0.4385 -0.3770,-0.4345 -0.3266,-0.4345 -0.3226,-0.43'
        '85 -0.3226,-0.4808 -0.3266,-0.4849ZM-0.4657,-0.6038 -0.4798,-0.5877 -0.4798,0.5837 -0.4778,0.5897 -0'
        '.4597,0.6038 0.4577,0.6038 0.4637,0.6018 0.4738,0.5917 0.4778,0.5817 0.4778,-0.5857 0.4758,-0.5917 0'
        '.4637,-0.6038 0.4577,-0.6058 -0.4597,-0.6058ZM-0.1169,0.5030 -0.0585,0.4466 -0.0081,0.4466 -0.0060,0'
        '.4486 -0.0403,0.4808 -0.0363,0.4869 0.1149,0.4869 0.1169,0.4889 0.1169,0.5212 0.1149,0.5232 -0.0363,'
        '0.5232 -0.0403,0.5272 -0.0081,0.5595 -0.0101,0.5615 -0.0605,0.5615ZM-0.3528,-0.3760 -0.3286,-0.3780 '
        '-0.3165,-0.3720 -0.3065,-0.3599 -0.3024,-0.3458 -0.3044,-0.3317 -0.3085,-0.3236 -0.3266,-0.3095 -0.3'
        '488,-0.3095 -0.3569,-0.3135 -0.3710,-0.3296 -0.3730,-0.3377 -0.3710,-0.3579ZM-0.4052,-0.4143 -0.3931'
        ',-0.4244 -0.3831,-0.4829 -0.3770,-0.4909 -0.3690,-0.4950 -0.2984,-0.4950 -0.2944,-0.4909 -0.2944,-0.'
        '4385 -0.2903,-0.4345 -0.2742,-0.4345 -0.2702,-0.4385 -0.2702,-0.5232 -0.2661,-0.5272 0.0323,-0.5272 '
        '0.0383,-0.5192 0.0383,-0.3478 0.0363,-0.3458 -0.0040,-0.3458 -0.0101,-0.3397 -0.0141,-0.3236 -0.0323'
        ',-0.3095 -0.0444,-0.3075 -0.0645,-0.3135 -0.0746,-0.3236 -0.0786,-0.3417 -0.0827,-0.3458 -0.2944,-0.'
        '3458 -0.3024,-0.3679 -0.3185,-0.3821 -0.3306,-0.3861 -0.3468,-0.3861 -0.3609,-0.3800 -0.3750,-0.3659'
        ' -0.3810,-0.3478 -0.3911,-0.3458 -0.4032,-0.3921ZM0.2359,-0.5655 0.2782,-0.5655 0.3145,-0.5554 0.348'
        '8,-0.5353 0.3750,-0.5091 0.3871,-0.4909 0.4012,-0.4546 0.4052,-0.4325 0.4052,-0.4042 0.3992,-0.3740 '
        '0.3770,-0.3296 0.3548,-0.3054 0.3387,-0.2933 0.3105,-0.2792 0.2823,-0.2712 0.2621,-0.2712 0.2601,-0.'
        '2692 0.2319,-0.2712 0.1935,-0.2833 0.1694,-0.2974 0.1431,-0.3216 0.1310,-0.3377 0.1190,-0.3619 0.110'
        '9,-0.3881 0.1089,-0.4022 0.1109,-0.4466 0.1190,-0.4748 0.1371,-0.5071 0.1552,-0.5272 0.1794,-0.5454 '
        '0.2097,-0.5595Z'
    ),
    '640.2A/2': (
        'M0.1613,-0.4909 0.1532,-0.4829 0.1391,-0.4506 0.1351,-0.4284 0.1351,-0.4083 0.1431,-0.3740 0.1532,-0'
        '.3538 0.1653,-0.3377 0.1915,-0.3155 0.2117,-0.3054 0.2319,-0.2994 0.2500,-0.2974 0.2782,-0.2994 0.30'
        '44,-0.3075 0.3226,-0.3175 0.3286,-0.3236ZM0.1915,-0.5212 0.1855,-0.5131 0.3528,-0.3478 0.3690,-0.374'
        '0 0.3770,-0.4103 0.3730,-0.4506 0.3528,-0.4909 0.3206,-0.5212 0.2964,-0.5333 0.2702,-0.5393 0.2298,-'
        '0.5373 0.2056,-0.5292Z'
    ),
    '640.2A/3': (
        'M0.2480,-0.5675 0.2218,-0.5635 0.1976,-0.5554 0.1673,-0.5373 0.1452,-0.5171 0.1310,-0.4990 0.1149,-0'
        '.4647 0.1089,-0.4385 0.1089,-0.3982 0.1129,-0.3780 0.1250,-0.3478 0.1411,-0.3236 0.1613,-0.3034 0.18'
        '15,-0.2893 0.2137,-0.2752 0.2419,-0.2692 0.2722,-0.2692 0.3004,-0.2752 0.3327,-0.2893 0.3528,-0.3034'
        ' 0.3770,-0.3296 0.3992,-0.3720 0.4052,-0.4002 0.4052,-0.4365 0.3952,-0.4748 0.3851,-0.4950 0.3750,-0'
        '.5091 0.3468,-0.5373 0.3246,-0.5514 0.2984,-0.5615 0.2661,-0.5675ZM0.1552,-0.4829 0.1613,-0.4889 0.3'
        '266,-0.3236 0.3165,-0.3155 0.2944,-0.3054 0.2782,-0.3014 0.2500,-0.2994 0.2117,-0.3075 0.1915,-0.317'
        '5 0.1754,-0.3296 0.1593,-0.3478 0.1452,-0.3740 0.1371,-0.4083 0.1391,-0.4425 0.1452,-0.4627ZM0.1915,'
        '-0.5192 0.2056,-0.5272 0.2298,-0.5353 0.2702,-0.5373 0.2964,-0.5312 0.3206,-0.5192 0.3508,-0.4909 0.'
        '3690,-0.4567 0.3750,-0.4284 0.3710,-0.3861 0.3528,-0.3498 0.1875,-0.5131Z'
    ),
    '640.2A/4': (
        'M-0.0464,-0.5010 -0.0464,-0.4950 -0.0423,-0.4909 -0.0262,-0.4909 -0.0222,-0.4950 -0.0222,-0.5010 -0.'
        '0262,-0.5050 -0.0423,-0.5050Z'
    ),
    '640.2A/5': (
        'M-0.0786,0.5433 -0.0605,0.5615 -0.0060,0.5615 -0.0403,0.5272 -0.0444,0.5353 -0.0565,0.5454 -0.0665,0'
        '.5474ZM-0.1048,0.4909 -0.1169,0.5030 -0.1048,0.5171 -0.1089,0.5111 -0.1089,0.4970ZM-0.0363,0.4869 -0'
        '.0302,0.4970 -0.0302,0.5111 -0.0383,0.5232 0.1169,0.5232 0.1169,0.4869ZM-0.0766,0.4647 -0.0645,0.460'
        '7 -0.0544,0.4627 -0.0383,0.4788 -0.0060,0.4466 -0.0585,0.4466ZM-0.0081,-0.3438 -0.0181,-0.3458 -0.02'
        '62,-0.3518 -0.0242,-0.3377 -0.0383,-0.3236 -0.0544,-0.3256 -0.0645,-0.3377 -0.0645,-0.3478 -0.0706,-'
        '0.3438 -0.0786,-0.3438 -0.0786,-0.3337 -0.0746,-0.3236 -0.0645,-0.3135 -0.0444,-0.3075 -0.0242,-0.31'
        '35 -0.0141,-0.3236ZM-0.2964,-0.3538 -0.2944,-0.3458 -0.2782,-0.3458 -0.2863,-0.3458ZM0.0383,-0.3619 '
        '0.0363,-0.3558 0.0282,-0.3478 0.0161,-0.3458 0.0383,-0.3458ZM-0.3528,-0.3760 -0.3710,-0.3579 -0.3730'
        ',-0.3498 -0.3710,-0.3296 -0.3629,-0.3175 -0.3488,-0.3095 -0.3266,-0.3095 -0.3185,-0.3135 -0.3044,-0.'
        '3317 -0.3024,-0.3458 -0.3065,-0.3599 -0.3165,-0.3720 -0.3286,-0.3780ZM-0.3427,-0.3639 -0.3286,-0.361'
        '9 -0.3165,-0.3458 -0.3185,-0.3357 -0.3327,-0.3236 -0.3488,-0.3256 -0.3589,-0.3397 -0.3589,-0.3478 -0'
        '.3548,-0.3558ZM-0.4012,-0.3861 -0.3931,-0.3478 -0.3810,-0.3458 -0.3750,-0.3659 -0.3649,-0.3760 -0.37'
        '70,-0.3720 -0.3891,-0.3740ZM-0.0302,-0.4889 -0.0423,-0.4889 -0.0423,-0.4748 -0.0403,-0.4808ZM-0.3931'
        ',-0.4264 -0.3831,-0.4345 -0.3750,-0.4345 -0.3810,-0.4365 -0.3810,-0.4466 -0.3750,-0.4768 -0.3669,-0.'
        '4849 -0.3246,-0.4849 -0.3226,-0.4829 -0.3226,-0.4385 -0.3085,-0.4425 -0.2944,-0.4385 -0.2944,-0.4909'
        ' -0.2984,-0.4950 -0.3690,-0.4950 -0.3770,-0.4909 -0.3851,-0.4768ZM0.0161,-0.5272 0.0282,-0.5252 0.03'
        '63,-0.5171 0.0383,-0.5111 0.0363,-0.5252ZM-0.0645,-0.5272 -0.0524,-0.5252 -0.0444,-0.5171 -0.0403,-0'
        '.5071 -0.0222,-0.5071 -0.0181,-0.5171 -0.0101,-0.5252 0.0020,-0.5272ZM-0.2702,-0.5111 -0.2681,-0.517'
        '1 -0.2601,-0.5252 -0.2480,-0.5272 -0.2661,-0.5272 -0.2702,-0.5232Z'
    ),
    '650.1/0': (
        'M-0.6051,-0.4730 -0.6171,-0.4489 -0.6171,0.4459 -0.6051,0.4700 -0.5901,0.4850 -0.5631,0.4970 0.5571,'
        '0.4970 0.5811,0.4880 0.5991,0.4730 0.6141,0.4399 0.6141,-0.4429 0.6051,-0.4670 0.5931,-0.4820 0.5571'
        ',-0.5000 -0.5601,-0.5000 -0.5901,-0.4880Z'
    ),
    '650.1/1': (
        'M-0.5871,-0.4429 -0.5871,0.4399 -0.5691,0.4610 -0.5511,0.4670 0.5450,0.4670 0.5601,0.4640 0.5751,0.4'
        '520 0.5841,0.4279 0.5841,-0.4309 0.5781,-0.4520 0.5661,-0.4640 0.5541,-0.4700 -0.5571,-0.4700 -0.566'
        '1,-0.4670ZM-0.0225,-0.4099 0.0165,-0.4099 0.0405,-0.4009 0.0706,-0.3739 0.0856,-0.3408 0.0856,-0.301'
        '8 0.0736,-0.2718 0.0465,-0.2447 0.0165,-0.2327 -0.0195,-0.2327 -0.0495,-0.2447 -0.0736,-0.2658 -0.09'
        '16,-0.3048 -0.0916,-0.3378 -0.0796,-0.3679 -0.0495,-0.3979Z'
    ),
    '650.1/2': (
        'M-0.0225,-0.4099 -0.0495,-0.3979 -0.0796,-0.3679 -0.0916,-0.3378 -0.0916,-0.3048 -0.0736,-0.2658 -0.'
        '0495,-0.2447 -0.0195,-0.2327 0.0165,-0.2327 0.0495,-0.2477 0.0736,-0.2718 0.0856,-0.2988 0.0886,-0.3'
        '198 0.0856,-0.3438 0.0706,-0.3739 0.0405,-0.4009 0.0165,-0.4099ZM-0.0405,-0.2658 -0.0045,-0.3018 0.0'
        '015,-0.3018 0.0375,-0.2628 0.0135,-0.2508 -0.0165,-0.2508 -0.0345,-0.2568ZM0.0556,-0.3619 0.0676,-0.'
        '3408 0.0706,-0.3228 0.0646,-0.2928 0.0556,-0.2808 0.0165,-0.3198ZM-0.0586,-0.3619 -0.0195,-0.3198 -0'
        '.0586,-0.2808 -0.0736,-0.3108 -0.0706,-0.3438ZM-0.0405,-0.3769 -0.0345,-0.3859 -0.0165,-0.3919 0.010'
        '5,-0.3919 0.0375,-0.3799 0.0015,-0.3408 -0.0045,-0.3408Z'
    ),
    '650.1/3': (
        'M-0.0435,-0.2658 -0.0345,-0.2538 -0.0165,-0.2477 0.0135,-0.2477 0.0405,-0.2628 0.0015,-0.3048 -0.004'
        '5,-0.3048ZM0.0556,-0.3649 0.0135,-0.3228 0.0556,-0.2778 0.0676,-0.2928 0.0736,-0.3198 0.0706,-0.3408'
        ' 0.0646,-0.3559ZM-0.0586,-0.3649 -0.0676,-0.3559 -0.0766,-0.3318 -0.0736,-0.2988 -0.0586,-0.2778 -0.'
        '0165,-0.3198ZM-0.0345,-0.3889 -0.0435,-0.3769 -0.0045,-0.3378 0.0015,-0.3378 0.0405,-0.3799 0.0105,-'
        '0.3949 -0.0165,-0.3949Z'
    ),
    '650.3/0': (
        'M-0.6278,-0.4779 -0.6435,-0.4495 -0.6467,-0.4306 -0.6467,0.4306 -0.6404,0.4558 -0.6246,0.4779 -0.586'
        '8,0.4968 0.5836,0.4968 0.6151,0.4842 0.6309,0.4685 0.6435,0.4401 0.6435,-0.4432 0.6309,-0.4716 0.615'
        '1,-0.4874 0.5868,-0.5000 -0.5868,-0.5000 -0.6120,-0.4905Z'
    ),
    '650.3/1': (
        'M-0.6088,-0.4495 -0.6151,-0.4306 -0.6151,0.4306 -0.6088,0.4464 -0.5962,0.4590 -0.5836,0.4653 0.5804,'
        '0.4653 0.5899,0.4621 0.6088,0.4432 0.6120,0.4338 0.6120,-0.4369 0.6088,-0.4464 0.5899,-0.4653 0.5804'
        ',-0.4685 -0.5836,-0.4685ZM-0.0189,-0.4054 0.0189,-0.4054 0.0536,-0.3896 0.0757,-0.3675 0.0915,-0.332'
        '8 0.0915,-0.2918 0.0757,-0.2571 0.0473,-0.2319 0.0126,-0.2192 -0.0284,-0.2224 -0.0662,-0.2445 -0.078'
        '9,-0.2603 -0.0946,-0.3013 -0.0915,-0.3360 -0.0726,-0.3738 -0.0505,-0.3927Z'
    ),
    '650.3/2': (
        'M-0.0599,-0.3580 -0.0726,-0.3454 -0.0789,-0.3233 -0.0789,-0.3013 -0.0662,-0.2697 -0.0410,-0.2445 -0.'
        '0158,-0.2350 0.0158,-0.2350 0.0379,-0.2445 0.0442,-0.2539ZM-0.0473,-0.3738 0.0599,-0.2666 0.0726,-0.'
        '2823 0.0789,-0.3076 0.0757,-0.3328 0.0662,-0.3549 0.0410,-0.3801 0.0032,-0.3927 -0.0221,-0.3896Z'
    ),
    '650.3/3': (
        'M-0.0347,-0.4022 -0.0599,-0.3864 -0.0883,-0.3486 -0.0946,-0.3265 -0.0946,-0.2981 -0.0883,-0.2760 -0.'
        '0631,-0.2413 -0.0315,-0.2224 0.0189,-0.2192 0.0379,-0.2256 0.0757,-0.2571 0.0883,-0.2792 0.0946,-0.3'
        '076 0.0883,-0.3454 0.0789,-0.3644 0.0505,-0.3927 0.0315,-0.4022 0.0032,-0.4085ZM-0.0694,-0.3454 -0.0'
        '599,-0.3549 0.0410,-0.2508 0.0158,-0.2382 -0.0158,-0.2382 -0.0410,-0.2476 -0.0631,-0.2697 -0.0726,-0'
        '.2886 -0.0757,-0.3233ZM-0.0221,-0.3864 0.0032,-0.3896 0.0410,-0.3770 0.0631,-0.3549 0.0726,-0.3328 0'
        '.0757,-0.3076 0.0662,-0.2760 0.0599,-0.2697 -0.0442,-0.3738Z'
    ),
    '660.3/0': (
        'M-0.8576,-0.4690 -0.8669,-0.4474 -0.8669,0.4443 -0.8545,0.4690 -0.8359,0.4845 -0.7957,0.4969 0.7926,'
        '0.4969 0.8328,0.4845 0.8545,0.4628 0.8638,0.4412 0.8638,-0.4443 0.8483,-0.4752 0.8297,-0.4907 0.7988'
        ',-0.5000 -0.8050,-0.5000 -0.8390,-0.4876Z'
    ),
    '660.3/1': (
        'M-0.4489,-0.1718 -0.6502,-0.1718 -0.6563,-0.1656 -0.6563,0.1749 -0.6502,0.1811 -0.5851,0.1811 -0.578'
        '9,0.1749 -0.5789,0.0449 -0.5759,0.0418 -0.4489,0.0418 -0.4211,0.0294 -0.4025,0.0108 -0.3901,-0.0170 '
        '-0.3901,-0.1099 -0.4056,-0.1440 -0.4211,-0.1594ZM-0.5789,-0.1099 -0.5759,-0.1130 -0.4892,-0.1130 -0.'
        '4768,-0.1068 -0.4675,-0.0913 -0.4706,-0.0325 -0.4923,-0.0170 -0.5759,-0.0170 -0.5789,-0.0201ZM-0.829'
        '7,-0.4474 -0.8328,-0.4412 -0.8328,0.4381 -0.8204,0.4536 -0.8080,0.4598 0.8050,0.4598 0.8235,0.4443 0'
        '.8297,0.4319 0.8297,-0.4350 0.8266,-0.4443 0.8080,-0.4628 -0.8111,-0.4628ZM0.5975,0.1749 0.6037,0.17'
        '18 0.7554,0.1718 0.7709,0.1842 0.7740,0.1935 0.7740,0.3793 0.7647,0.3978 0.7523,0.4040 0.6068,0.4040'
        ' 0.5882,0.3885 0.5882,0.1873ZM0.5789,-0.1285 0.7895,-0.1285 0.7926,-0.1254 0.7926,0.1223 0.7895,0.12'
        '54 0.5789,0.1254 0.5759,0.1223 0.5759,-0.1254ZM-0.7616,-0.2276 -0.7430,-0.2337 -0.3467,-0.2337 -0.32'
        '20,-0.2214 -0.3158,-0.2090 -0.3158,0.2059 -0.3313,0.2245 -0.3375,0.2276 -0.7554,0.2276 -0.7709,0.215'
        '2 -0.7740,0.2090 -0.7740,-0.2121ZM0.5697,-0.4164 0.7926,-0.4164 0.7957,-0.4133 0.7957,-0.1656 0.7926'
        ',-0.1625 0.5697,-0.1625 0.5666,-0.1656 0.5666,-0.4133Z'
    ),
    '660.3/2': (
        'M-0.5820,-0.1099 -0.5820,-0.0201 -0.5759,-0.0139 -0.4923,-0.0139 -0.4675,-0.0325 -0.4644,-0.0913 -0.'
        '4768,-0.1099 -0.4892,-0.1161 -0.5759,-0.1161ZM-0.7616,-0.2307 -0.7771,-0.2121 -0.7771,0.2090 -0.7740'
        ',0.2152 -0.7554,0.2307 -0.3375,0.2307 -0.3313,0.2276 -0.3127,0.2059 -0.3127,-0.2090 -0.3189,-0.2214 '
        '-0.3282,-0.2307 -0.3467,-0.2368 -0.7430,-0.2368ZM-0.4211,-0.1563 -0.4087,-0.1440 -0.3932,-0.1099 -0.'
        '3932,-0.0170 -0.4056,0.0108 -0.4211,0.0263 -0.4489,0.0387 -0.5759,0.0387 -0.5820,0.0449 -0.5820,0.17'
        '49 -0.5851,0.1780 -0.6502,0.1780 -0.6533,0.1749 -0.6533,-0.1656 -0.6502,-0.1687 -0.4489,-0.1687Z'
    ),
    '660.3/3': (
        'M0.7926,0.1006 0.7895,0.1099 0.7771,0.1223 0.7585,0.1254 0.7926,0.1254ZM0.5759,0.1006 0.5759,0.1254 '
        '0.6099,0.1254 0.5913,0.1223 0.5789,0.1099ZM0.7585,-0.1285 0.7771,-0.1254 0.7895,-0.1130 0.7926,-0.10'
        '37 0.7926,-0.1285ZM0.5759,-0.1037 0.5789,-0.1130 0.5913,-0.1254 0.6099,-0.1285 0.5759,-0.1285ZM0.795'
        '7,-0.1873 0.7926,-0.1780 0.7802,-0.1656 0.7616,-0.1625 0.7957,-0.1625ZM0.5666,-0.1873 0.5666,-0.1625'
        ' 0.6006,-0.1625 0.5820,-0.1656 0.5697,-0.1780ZM0.7616,-0.4164 0.7802,-0.4133 0.7926,-0.4009 0.7957,-'
        '0.3916 0.7957,-0.4164ZM0.5666,-0.3916 0.5697,-0.4009 0.5820,-0.4133 0.6006,-0.4164 0.5666,-0.4164Z'
    ),
    '660.5/0': (
        'M-0.4799,-0.7409 -0.4909,-0.7318 -0.5000,-0.7117 -0.5000,0.7099 -0.4927,0.7281 -0.4818,0.7391 -0.467'
        '2,0.7445 0.4653,0.7445 0.4799,0.7391 0.4891,0.7318 0.4982,0.7135 0.4982,-0.7153 0.4927,-0.7281 0.481'
        '8,-0.7391 0.4635,-0.7464 -0.4653,-0.7464Z'
    ),
    '660.5/1': (
        'M-0.4763,0.1131 -0.4799,0.1204 -0.4799,0.7099 -0.4690,0.7226 -0.4653,0.7245 0.4653,0.7245 0.4763,0.7'
        '153 0.4781,0.7117 0.4781,0.1186 0.4708,0.1095 0.4635,0.1058 -0.4653,0.1058ZM-0.3047,-0.1533 -0.3084,'
        '-0.1496 -0.3047,-0.1460 -0.3011,-0.1496ZM-0.3230,-0.1533 -0.3266,-0.1496 -0.3193,-0.1442 -0.3157,-0.'
        '1478ZM-0.2080,-0.1624 -0.2135,-0.1569 -0.2099,-0.1533 -0.2044,-0.1588ZM-0.2117,-0.1770 -0.2153,-0.17'
        '34 -0.2099,-0.1679 -0.2062,-0.1715ZM-0.4161,-0.1770 -0.4234,-0.1697 -0.4252,-0.1606 -0.4179,-0.1533 '
        '-0.4142,-0.1569 -0.4197,-0.1642 -0.4106,-0.1734 -0.4069,-0.1697 -0.4051,-0.1588 -0.4069,-0.1569 -0.4'
        '033,-0.1533 -0.3923,-0.1697 -0.3960,-0.1734 -0.3996,-0.1697 -0.4069,-0.1770 -0.4106,-0.1734ZM-0.2354'
        ',-0.1788 -0.2391,-0.1752 -0.2245,-0.1533 -0.2208,-0.1569 -0.2226,-0.1588 -0.2208,-0.1624 -0.2245,-0.'
        '1679 -0.2190,-0.1734 -0.2226,-0.1770 -0.2281,-0.1679ZM-0.3321,-0.1880 -0.3358,-0.1843 -0.3212,-0.171'
        '5 -0.3175,-0.1752ZM-0.2938,-0.1898 -0.3102,-0.1752 -0.3066,-0.1715 -0.2901,-0.1861ZM-0.2737,-0.2044 '
        '-0.2774,-0.2007 -0.2719,-0.1953 -0.2682,-0.1989ZM-0.2883,-0.2026 -0.2920,-0.2062 -0.3029,-0.1953 -0.'
        '3139,-0.1898 -0.3248,-0.1953 -0.3339,-0.2044 -0.3376,-0.2007 -0.3230,-0.1880 -0.3212,-0.1898 -0.3175'
        ',-0.1861 -0.3139,-0.1898 -0.3102,-0.1861 -0.2993,-0.1916ZM-0.2847,-0.2299 -0.2883,-0.2263 -0.2774,-0'
        '.2172 -0.2737,-0.2208ZM-0.2299,-0.2336 -0.2354,-0.2299 -0.2427,-0.2354 -0.2464,-0.2318 -0.2354,-0.22'
        '63 -0.2336,-0.2226 -0.2391,-0.2153 -0.2372,-0.2135 -0.2464,-0.2099 -0.2573,-0.2153 -0.2609,-0.2117 -'
        '0.2573,-0.2080 -0.2536,-0.2099 -0.2427,-0.2044 -0.2573,-0.1898 -0.2646,-0.1971 -0.2682,-0.1934 -0.26'
        '28,-0.1880 -0.2609,-0.1898 -0.2591,-0.1880 -0.2628,-0.1807 -0.2737,-0.1898 -0.2774,-0.1861 -0.2701,-'
        '0.1788 -0.2701,-0.1752 -0.2938,-0.1569 -0.2901,-0.1533 -0.2828,-0.1533 -0.2792,-0.1569 -0.2810,-0.15'
        '88 -0.2609,-0.1752 -0.2464,-0.1916 -0.2409,-0.1880 -0.2427,-0.1843 -0.2391,-0.1807 -0.2354,-0.1843 -'
        '0.2391,-0.1880 -0.2372,-0.1916 -0.2409,-0.2026 -0.2299,-0.2190 -0.2318,-0.2208 -0.2263,-0.2299ZM-0.4'
        '033,-0.2518 -0.4069,-0.2482 -0.4015,-0.2372 -0.3978,-0.2409ZM-0.2245,-0.2555 -0.2281,-0.2518 -0.2245'
        ',-0.2482 -0.2299,-0.2427 -0.2263,-0.2391 -0.2226,-0.2427 -0.2263,-0.2464 -0.2208,-0.2518ZM-0.2920,-0'
        '.2372 -0.3066,-0.2555 -0.3157,-0.2628 -0.3285,-0.2445 -0.3467,-0.2263 -0.3650,-0.2153 -0.3613,-0.211'
        '7 -0.3449,-0.2208 -0.3139,-0.2555 -0.2956,-0.2336ZM-0.4051,-0.2628 -0.4088,-0.2591 -0.4051,-0.2555 -'
        '0.4015,-0.2591ZM-0.3029,-0.2938 -0.3066,-0.2901 -0.2956,-0.2701 -0.2719,-0.2445 -0.2609,-0.2372 -0.2'
        '573,-0.2409 -0.2682,-0.2482 -0.2865,-0.2664ZM-0.3449,-0.3011 -0.3577,-0.2901 -0.3540,-0.2865 -0.3412'
        ',-0.2974ZM-0.2883,-0.3102 -0.2920,-0.3066 -0.2883,-0.2993 -0.2774,-0.2883 -0.2701,-0.2847 -0.2664,-0'
        '.2883 -0.2755,-0.2938ZM-0.3942,-0.3102 -0.3978,-0.3066 -0.3942,-0.2993 -0.3832,-0.2883 -0.3759,-0.28'
        '47 -0.3723,-0.2883 -0.3814,-0.2938ZM-0.3394,-0.3120 -0.3431,-0.3084 -0.3394,-0.3047 -0.3358,-0.3084Z'
        'M-0.2336,-0.3139 -0.2409,-0.2993 -0.2518,-0.2901 -0.2482,-0.2865 -0.2354,-0.2974 -0.2318,-0.3047 -0.'
        '2336,-0.3066 -0.2299,-0.3102ZM-0.2500,-0.3449 -0.2536,-0.3412 -0.2391,-0.3285 -0.2336,-0.3175 -0.229'
        '9,-0.3212 -0.2336,-0.3248 -0.2318,-0.3266 -0.2336,-0.3303ZM-0.2719,-0.3449 -0.2883,-0.3321 -0.2901,-'
        '0.3285 -0.2865,-0.3248 -0.2774,-0.3358 -0.2682,-0.3412ZM-0.3139,-0.3449 -0.3175,-0.3412 -0.3212,-0.3'
        '193 -0.3175,-0.3157 -0.3230,-0.3102 -0.3212,-0.3084 -0.3248,-0.3047 -0.3230,-0.3029 -0.3266,-0.2993 '
        '-0.3248,-0.2974 -0.3285,-0.2938 -0.3266,-0.2920 -0.3449,-0.2628 -0.3686,-0.2427 -0.3887,-0.2318 -0.3'
        '978,-0.2336 -0.4015,-0.2299 -0.3942,-0.2208 -0.3978,-0.2172 -0.3887,-0.2007 -0.3905,-0.1953 -0.3887,'
        '-0.1898 -0.3923,-0.1861 -0.3887,-0.1825 -0.3850,-0.1861 -0.3869,-0.1898 -0.3832,-0.1916 -0.3613,-0.1'
        '697 -0.3504,-0.1624 -0.3449,-0.1533 -0.3376,-0.1533 -0.3339,-0.1569 -0.3485,-0.1661 -0.3595,-0.1770 '
        '-0.3504,-0.1861 -0.3485,-0.1843 -0.3449,-0.1880 -0.3412,-0.1843 -0.3376,-0.1880 -0.3412,-0.1916 -0.3'
        '449,-0.1880 -0.3485,-0.1916 -0.3650,-0.1807 -0.3704,-0.1861 -0.3668,-0.1898 -0.3650,-0.1880 -0.3485,'
        '-0.2026 -0.3522,-0.2062 -0.3704,-0.1898 -0.3759,-0.1916 -0.3850,-0.2044 -0.3832,-0.2080 -0.3960,-0.2'
        '226 -0.3869,-0.2299 -0.3850,-0.2281 -0.3668,-0.2372 -0.3412,-0.2591 -0.3230,-0.2883 -0.3248,-0.2901 '
        '-0.3212,-0.2938 -0.3230,-0.2956 -0.3157,-0.3102 -0.3193,-0.3139 -0.3139,-0.3193 -0.3120,-0.3175 -0.3'
        '139,-0.3139 -0.3102,-0.3102 -0.3120,-0.3066 -0.3084,-0.3029 -0.3047,-0.3066 -0.3102,-0.3175 -0.3084,'
        '-0.3212 -0.3102,-0.3412ZM-0.3558,-0.3449 -0.3595,-0.3412 -0.3412,-0.3230 -0.3376,-0.3266 -0.3394,-0.'
        '3303ZM-0.3777,-0.3449 -0.3942,-0.3321 -0.3960,-0.3285 -0.3942,-0.3266 -0.3978,-0.3230 -0.3942,-0.319'
        '3 -0.3869,-0.3321 -0.3741,-0.3412ZM-0.3266,-0.3631 -0.3303,-0.3668 -0.3358,-0.3613 -0.3394,-0.3650 -'
        '0.3431,-0.3613 -0.3394,-0.3577 -0.3339,-0.3631 -0.3303,-0.3595ZM-0.2245,-0.3704 -0.2281,-0.3668 -0.2'
        '245,-0.3613 -0.2208,-0.3650ZM-0.3193,-0.3668 -0.3157,-0.3613 -0.3084,-0.3650 -0.2974,-0.3595 -0.2938'
        ',-0.3631 -0.2974,-0.3668 -0.3011,-0.3650 -0.3120,-0.3704ZM-0.4033,-0.3704 -0.4088,-0.3668 -0.4051,-0'
        '.3613 -0.3996,-0.3668ZM-0.2500,-0.6569 -0.2664,-0.6606 -0.3741,-0.6606 -0.3777,-0.6569 -0.3777,-0.45'
        '99 -0.3741,-0.4562 -0.3376,-0.4562 -0.3339,-0.4599 -0.3339,-0.5328 -0.3321,-0.5347 -0.2555,-0.5365 -'
        '0.2391,-0.5456 -0.2299,-0.5566 -0.2245,-0.5693 -0.2245,-0.6259 -0.2336,-0.6442ZM-0.3339,-0.6241 -0.3'
        '321,-0.6259 -0.2810,-0.6259 -0.2701,-0.6168 -0.2682,-0.6113 -0.2701,-0.5785 -0.2755,-0.5730 -0.2847,'
        '-0.5693 -0.3321,-0.5693 -0.3339,-0.5712ZM-0.4799,-0.7117 -0.4799,0.0712 -0.4690,0.0839 -0.4653,0.085'
        '8 0.4653,0.0858 0.4763,0.0766 0.4781,0.0730 0.4781,-0.7135 0.4708,-0.7226 0.4617,-0.7263 -0.4635,-0.'
        '7263 -0.4690,-0.7245ZM-0.4398,-0.3905 -0.4325,-0.3942 -0.1953,-0.3942 -0.1843,-0.3869 -0.1807,-0.377'
        '7 -0.1807,-0.1442 -0.1825,-0.1387 -0.1934,-0.1296 -0.4343,-0.1296 -0.4434,-0.1369 -0.4471,-0.1460 -0'
        '.4471,-0.3759ZM-0.4380,-0.6916 -0.4325,-0.6934 -0.1934,-0.6934 -0.1843,-0.6861 -0.1807,-0.6788 -0.18'
        '07,-0.4453 -0.1843,-0.4361 -0.1934,-0.4288 -0.4325,-0.4288 -0.4434,-0.4361 -0.4471,-0.4471 -0.4471,-'
        '0.6752 -0.4434,-0.6861Z'
    ),
    '660.5/2': (
        'M-0.4398,-0.3923 -0.4471,-0.3832 -0.4489,-0.3759 -0.4489,-0.1460 -0.4453,-0.1369 -0.4343,-0.1277 -0.'
        '1934,-0.1277 -0.1807,-0.1387 -0.1788,-0.1442 -0.1788,-0.3777 -0.1825,-0.3869 -0.1898,-0.3942 -0.1953'
        ',-0.3960 -0.4325,-0.3960ZM-0.2920,-0.1569 -0.2847,-0.1624 -0.2774,-0.1569 -0.2792,-0.1551ZM-0.3504,-'
        '0.1569 -0.3449,-0.1624 -0.3358,-0.1569 -0.3376,-0.1551ZM-0.2336,-0.1697 -0.2318,-0.1715 -0.2281,-0.1'
        '679 -0.2263,-0.1697 -0.2190,-0.1569 -0.2281,-0.1551 -0.2299,-0.1569 -0.2263,-0.1606ZM-0.4033,-0.1715'
        ' -0.3978,-0.1661 -0.4015,-0.1606 -0.3978,-0.1569 -0.3996,-0.1551 -0.4088,-0.1569 -0.4051,-0.1606ZM-0'
        '.2682,-0.1752 -0.2664,-0.1807 -0.2628,-0.1770 -0.2664,-0.1734ZM-0.2591,-0.1880 -0.2573,-0.1898 -0.25'
        '18,-0.1880 -0.2555,-0.1825ZM-0.3777,-0.1880 -0.3759,-0.1898 -0.3704,-0.1880 -0.3741,-0.1843ZM-0.3887'
        ',-0.1916 -0.3850,-0.2007 -0.3796,-0.1934 -0.3869,-0.1898ZM-0.2427,-0.2026 -0.2409,-0.2007 -0.2427,-0'
        '.1916 -0.2482,-0.1953ZM-0.2391,-0.2117 -0.2372,-0.2080 -0.2409,-0.2044 -0.2445,-0.2080ZM-0.3923,-0.2'
        '117 -0.3905,-0.2135 -0.3832,-0.2080 -0.3887,-0.2044ZM-0.3996,-0.2299 -0.3978,-0.2318 -0.3923,-0.2281'
        ' -0.3960,-0.2245ZM-0.2299,-0.2336 -0.2281,-0.2299 -0.2318,-0.2226 -0.2372,-0.2281ZM-0.3139,-0.3431 -'
        '0.3102,-0.3157 -0.3175,-0.3120 -0.3193,-0.3193ZM-0.2245,-0.3686 -0.2226,-0.3668 -0.2245,-0.3613 -0.2'
        '281,-0.3650ZM-0.3193,-0.3650 -0.3157,-0.3686 -0.3102,-0.3668 -0.3139,-0.3613ZM-0.4069,-0.3668 -0.403'
        '3,-0.3686 -0.4015,-0.3650 -0.4051,-0.3613ZM-0.3358,-0.6241 -0.3358,-0.5712 -0.3321,-0.5675 -0.2847,-'
        '0.5675 -0.2755,-0.5712 -0.2682,-0.5785 -0.2664,-0.6113 -0.2682,-0.6168 -0.2810,-0.6277 -0.3321,-0.62'
        '77ZM-0.4380,-0.6934 -0.4453,-0.6861 -0.4489,-0.6752 -0.4489,-0.4471 -0.4453,-0.4361 -0.4380,-0.4288 '
        '-0.4325,-0.4270 -0.1934,-0.4270 -0.1825,-0.4361 -0.1788,-0.4453 -0.1788,-0.6788 -0.1825,-0.6861 -0.1'
        '934,-0.6953 -0.4325,-0.6953ZM-0.2500,-0.6551 -0.2354,-0.6442 -0.2263,-0.6259 -0.2263,-0.5693 -0.2318'
        ',-0.5566 -0.2391,-0.5474 -0.2555,-0.5383 -0.3321,-0.5365 -0.3358,-0.5328 -0.3358,-0.4599 -0.3376,-0.'
        '4580 -0.3741,-0.4580 -0.3759,-0.4599 -0.3759,-0.6569 -0.3741,-0.6588 -0.2664,-0.6588Z'
    ),
    '660.5/3': (
        'M0.4690,0.0839 0.4635,0.0876 -0.4653,0.0876 -0.4672,0.0858 -0.4653,0.1004 -0.4690,0.1058 -0.4635,0.1'
        '040 0.4635,0.1040 0.4690,0.1077 0.4653,0.1022 0.4653,0.0894Z'
    ),
    '661.1/0': (
        'M-0.6809,-0.4742 -0.6886,-0.4561 -0.6886,0.4535 -0.6835,0.4690 -0.6680,0.4871 -0.6473,0.4974 0.6447,'
        '0.4974 0.6576,0.4922 0.6757,0.4767 0.6860,0.4561 0.6860,-0.4561 0.6783,-0.4742 0.6680,-0.4871 0.6421'
        ',-0.5000 -0.6447,-0.5000 -0.6628,-0.4922Z'
    ),
    '661.1/1': (
        'M-0.3320,-0.3140 -0.3501,-0.3191 -0.5078,-0.3191 -0.5129,-0.3140 -0.5129,-0.0323 -0.5078,-0.0271 -0.'
        '4561,-0.0271 -0.4509,-0.0323 -0.4509,-0.1382 -0.4483,-0.1408 -0.3475,-0.1408 -0.3217,-0.1512 -0.3036'
        ',-0.1693 -0.2959,-0.1873 -0.2959,-0.2726 -0.3062,-0.2933ZM-0.4509,-0.2674 -0.4483,-0.2700 -0.3708,-0'
        '.2674 -0.3579,-0.2519 -0.3605,-0.2028 -0.3708,-0.1925 -0.3786,-0.1899 -0.4483,-0.1899 -0.4509,-0.192'
        '5ZM-0.6602,-0.4535 -0.6602,0.4509 -0.6447,0.4690 -0.6370,0.4716 0.6344,0.4716 0.6421,0.4690 0.6550,0'
        '.4561 0.6602,0.4432 0.6602,-0.4432 0.6550,-0.4587 0.6447,-0.4690 0.6318,-0.4742 -0.6344,-0.4742 -0.6'
        '473,-0.4690ZM-0.6008,-0.3630 -0.5879,-0.3682 -0.2597,-0.3682 -0.2442,-0.3630 -0.2339,-0.3501 -0.2339'
        ',-0.0039 -0.2442,0.0090 -0.2494,0.0116 -0.5956,0.0116 -0.6085,0.0013 -0.6137,-0.0116 -0.6137,-0.3424'
        ' -0.6085,-0.3553Z'
    ),
    '661.1/2': (
        'M-0.4535,-0.2674 -0.4535,-0.1925 -0.4483,-0.1873 -0.3786,-0.1873 -0.3708,-0.1899 -0.3579,-0.2028 -0.'
        '3553,-0.2519 -0.3708,-0.2700 -0.4483,-0.2726ZM-0.6008,-0.3656 -0.6111,-0.3553 -0.6163,-0.3424 -0.616'
        '3,-0.0116 -0.6111,0.0013 -0.5956,0.0142 -0.2494,0.0142 -0.2442,0.0116 -0.2313,-0.0039 -0.2313,-0.350'
        '1 -0.2442,-0.3656 -0.2597,-0.3708 -0.5879,-0.3708ZM-0.3320,-0.3114 -0.3088,-0.2933 -0.2984,-0.2726 -'
        '0.2984,-0.1873 -0.3062,-0.1693 -0.3217,-0.1537 -0.3475,-0.1434 -0.4483,-0.1434 -0.4535,-0.1382 -0.45'
        '35,-0.0323 -0.4561,-0.0297 -0.5078,-0.0297 -0.5103,-0.0323 -0.5103,-0.3140 -0.5078,-0.3165 -0.3501,-'
        '0.3165Z'
    ),
    '661.3A/0': (
        'M-0.9657,-0.4458 -0.9693,-0.4314 -0.9693,0.4278 -0.9513,0.4675 -0.9152,0.4928 -0.9007,0.4964 0.9007,'
        '0.4964 0.9332,0.4819 0.9621,0.4458 0.9657,0.4314 0.9657,-0.4350 0.9513,-0.4675 0.9332,-0.4856 0.9007'
        ',-0.5000 -0.9007,-0.5000 -0.9404,-0.4819Z'
    ),
    '661.3A/1': (
        'M-0.4819,-0.3231 -0.7166,-0.3231 -0.7238,-0.3159 -0.7238,0.0740 -0.7166,0.0812 -0.6444,0.0812 -0.637'
        '2,0.0740 -0.6372,-0.0704 -0.6336,-0.0740 -0.4819,-0.0776 -0.4567,-0.0884 -0.4278,-0.1173 -0.4170,-0.'
        '1426 -0.4170,-0.2545 -0.4278,-0.2834 -0.4567,-0.3123ZM-0.6372,-0.2545 -0.6336,-0.2581 -0.5433,-0.258'
        '1 -0.5217,-0.2509 -0.5072,-0.2365 -0.5036,-0.2256 -0.5036,-0.1787 -0.5108,-0.1606 -0.5289,-0.1462 -0'
        '.6336,-0.1462 -0.6372,-0.1498ZM-0.9260,-0.4350 -0.9296,-0.4206 -0.9296,0.4170 -0.9224,0.4386 -0.9043'
        ',0.4531 -0.8935,0.4567 0.8935,0.4567 0.9079,0.4495 0.9260,0.4278 0.9260,-0.4314 0.9043,-0.4567 0.889'
        '9,-0.4603 -0.8899,-0.4603 -0.9116,-0.4531ZM-0.8574,-0.3736 -0.8357,-0.3917 -0.3556,-0.3917 -0.3484,-'
        '0.3881 -0.3303,-0.3664 -0.3303,0.1101 -0.3375,0.1245 -0.3556,0.1354 -0.8357,0.1354 -0.8430,0.1318 -0'
        '.8610,0.1101 -0.8610,-0.3664Z'
    ),
    '661.3A/2': (
        'M-0.6408,-0.2545 -0.6408,-0.1498 -0.6336,-0.1426 -0.5289,-0.1426 -0.5072,-0.1606 -0.5000,-0.1787 -0.'
        '5000,-0.2256 -0.5036,-0.2365 -0.5217,-0.2545 -0.5433,-0.2617 -0.6336,-0.2617ZM-0.8430,-0.3917 -0.864'
        '6,-0.3664 -0.8646,0.1101 -0.8610,0.1173 -0.8357,0.1390 -0.3556,0.1390 -0.3412,0.1318 -0.3267,0.1101 '
        '-0.3267,-0.3664 -0.3303,-0.3736 -0.3556,-0.3953 -0.8357,-0.3953ZM-0.4567,-0.3087 -0.4314,-0.2834 -0.'
        '4206,-0.2545 -0.4206,-0.1426 -0.4314,-0.1173 -0.4567,-0.0921 -0.4819,-0.0812 -0.6336,-0.0776 -0.6408'
        ',-0.0704 -0.6408,0.0740 -0.6444,0.0776 -0.7166,0.0776 -0.7202,0.0740 -0.7202,-0.3159 -0.7166,-0.3195'
        ' -0.4819,-0.3195Z'
    ),
    '661.4/0': (
        'M-1.1615,-0.4381 -1.1659,-0.4204 -1.1659,0.4159 -1.1482,0.4558 -1.1261,0.4779 -1.0996,0.4912 -1.0774'
        ',0.4956 1.0730,0.4956 1.1217,0.4779 1.1482,0.4513 1.1615,0.4204 1.1615,-0.4292 1.1438,-0.4646 1.1040'
        ',-0.4956 1.0907,-0.5000 -1.0951,-0.5000 -1.1305,-0.4823Z'
    ),
    '661.4/1': (
        'M-0.5907,-0.2434 -0.8606,-0.2434 -0.8695,-0.2345 -0.8695,0.2434 -0.8606,0.2522 -0.7721,0.2522 -0.763'
        '3,0.2434 -0.7633,0.0619 -0.7588,0.0575 -0.5863,0.0575 -0.5509,0.0442 -0.5155,0.0088 -0.5022,-0.0221 '
        '-0.5022,-0.1637 -0.5155,-0.1947 -0.5465,-0.2257ZM-0.7633,-0.1549 -0.7588,-0.1593 -0.6350,-0.1593 -0.'
        '6128,-0.1416 -0.6040,-0.1106 -0.6040,-0.0708 -0.6128,-0.0442 -0.6350,-0.0265 -0.7588,-0.0265 -0.7633'
        ',-0.0310ZM-1.1173,-0.4248 -1.1217,-0.4071 -1.1217,0.3982 -1.1128,0.4248 -1.0819,0.4469 1.0774,0.4469'
        ' 1.0951,0.4381 1.1128,0.4159 1.1128,-0.4204 1.0863,-0.4513 1.0730,-0.4558 -1.0774,-0.4558 -1.0907,-0'
        '.4513ZM-1.0066,-0.3230 -0.4226,-0.3230 -0.4049,-0.3097 -0.3960,-0.2920 -0.3960,0.2832 -0.4137,0.3097'
        ' -0.4226,0.3142 -1.0111,0.3142 -1.0376,0.2832 -1.0376,-0.2876 -1.0332,-0.3009Z'
    ),
    '661.4/2': (
        'M-0.7677,-0.1549 -0.7677,-0.0310 -0.7588,-0.0221 -0.6350,-0.0221 -0.6084,-0.0442 -0.5996,-0.0708 -0.'
        '5996,-0.1106 -0.6084,-0.1416 -0.6350,-0.1637 -0.7588,-0.1637ZM-1.0376,-0.3009 -1.0420,-0.2876 -1.042'
        '0,0.2832 -1.0111,0.3186 -0.4226,0.3186 -0.4137,0.3142 -0.3916,0.2832 -0.3916,-0.2920 -0.4004,-0.3097'
        ' -0.4226,-0.3274 -1.0066,-0.3274ZM-0.5465,-0.2212 -0.5199,-0.1947 -0.5066,-0.1637 -0.5066,-0.0221 -0'
        '.5199,0.0088 -0.5509,0.0398 -0.5863,0.0531 -0.7588,0.0531 -0.7677,0.0619 -0.7677,0.2434 -0.7721,0.24'
        '78 -0.8606,0.2478 -0.8650,0.2434 -0.8650,-0.2345 -0.8606,-0.2389 -0.5907,-0.2389Z'
    ),
    '662/0': (
        'M-0.5267,-0.4802 -0.5327,-0.4663 -0.5327,0.4644 -0.5267,0.4782 -0.5188,0.4881 -0.4990,0.4980 0.4950,'
        '0.4980 0.5069,0.4941 0.5228,0.4802 0.5307,0.4545 0.5307,-0.4564 0.5287,-0.4683 0.5188,-0.4861 0.4990'
        ',-0.4980 0.4891,-0.5000 -0.4931,-0.5000 -0.5149,-0.4921Z'
    ),
    '662/1': (
        'M-0.2653,-0.1376 -0.2752,-0.1396 -0.3960,-0.1396 -0.4000,-0.1356 -0.4000,0.0782 -0.3960,0.0822 -0.35'
        '64,0.0822 -0.3525,0.0782 -0.3525,-0.0010 -0.3505,-0.0030 -0.2673,-0.0050 -0.2515,-0.0129 -0.2356,-0.'
        '0327 -0.2317,-0.0723 -0.2337,-0.1040 -0.2416,-0.1198 -0.2535,-0.1317ZM-0.3525,-0.1000 -0.3505,-0.102'
        '0 -0.2950,-0.1020 -0.2871,-0.0980 -0.2792,-0.0822 -0.2832,-0.0505 -0.2891,-0.0446 -0.3010,-0.0406 -0'
        '.3505,-0.0406 -0.3525,-0.0426ZM-0.5089,-0.4663 -0.5109,-0.4624 -0.5109,0.4604 -0.5089,0.4663 -0.4970'
        ',0.4762 0.4931,0.4762 0.5069,0.4644 0.5089,0.4584 0.5089,-0.4584 0.5050,-0.4683 0.4990,-0.4743 0.491'
        '1,-0.4782 -0.4950,-0.4782ZM-0.4614,-0.1752 -0.2000,-0.1752 -0.1901,-0.1693 -0.1861,-0.1614 -0.1861,0'
        '.1000 -0.1941,0.1099 -0.2079,0.1139 -0.4535,0.1139 -0.4653,0.1099 -0.4713,0.1040 -0.4752,0.0921 -0.4'
        '752,-0.1554 -0.4713,-0.1673Z'
    ),
    '662/2': (
        'M-0.3545,-0.1000 -0.3545,-0.0426 -0.3505,-0.0386 -0.3010,-0.0386 -0.2891,-0.0426 -0.2812,-0.0505 -0.'
        '2772,-0.0822 -0.2792,-0.0901 -0.2871,-0.1000 -0.2950,-0.1040 -0.3505,-0.1040ZM-0.4733,-0.1673 -0.477'
        '2,-0.1554 -0.4772,0.0921 -0.4733,0.1040 -0.4653,0.1119 -0.4535,0.1158 -0.2079,0.1158 -0.1941,0.1119 '
        '-0.1842,0.1000 -0.1842,-0.1614 -0.1881,-0.1693 -0.2000,-0.1772 -0.4614,-0.1772ZM-0.2653,-0.1356 -0.2'
        '535,-0.1297 -0.2436,-0.1198 -0.2356,-0.1040 -0.2337,-0.0723 -0.2376,-0.0327 -0.2515,-0.0149 -0.2673,'
        '-0.0069 -0.3505,-0.0050 -0.3545,-0.0010 -0.3545,0.0782 -0.3564,0.0802 -0.3960,0.0802 -0.3980,0.0782 '
        '-0.3980,-0.1356 -0.3960,-0.1376 -0.2752,-0.1376Z'
    ),
    '675B/0': (
        'M-0.4781,-0.7029 -0.4912,-0.6897 -0.5000,-0.6678 -0.5000,0.6678 -0.4912,0.6875 -0.4781,0.7007 -0.451'
        '8,0.7094 0.4474,0.7094 0.4605,0.7072 0.4737,0.7007 0.4890,0.6853 0.4978,0.6568 0.4978,-0.6612 0.4868'
        ',-0.6919 0.4781,-0.7007 0.4649,-0.7072 0.4452,-0.7116 -0.4496,-0.7116Z'
    ),
    '675B/1': (
        'M-0.4013,0.5954 -0.4737,0.6678 -0.4693,0.6721 -0.3969,0.5998ZM-0.3509,0.5450 -0.3772,0.5713 -0.3728,'
        '0.5757 -0.3465,0.5493ZM-0.1908,0.4550 -0.2325,0.4967 -0.2325,0.5055 -0.2281,0.5143 -0.2149,0.5252 -0'
        '.1974,0.5230 -0.1842,0.5077 -0.1820,0.4682ZM-0.1579,0.4221 -0.1711,0.4353 -0.1601,0.4529 -0.1557,0.4'
        '704 -0.1557,0.4989 -0.1667,0.5296 -0.1776,0.5406 -0.1908,0.5471 -0.2149,0.5493 -0.2259,0.5471 -0.241'
        '2,0.5384 -0.2500,0.5252 -0.2566,0.5208 -0.3377,0.6020 -0.3333,0.6064 -0.3004,0.6173 -0.2785,0.6195 -'
        '0.2522,0.6173 -0.2127,0.6042 -0.1930,0.5910 -0.1667,0.5647 -0.1513,0.5384 -0.1404,0.4989 -0.1425,0.4'
        '550 -0.1513,0.4287ZM-0.1754,0.3936 -0.1864,0.4046 -0.1820,0.4090 -0.1711,0.3980ZM-0.2171,0.3607 -0.2'
        '675,0.3476 -0.3004,0.3498 -0.3421,0.3651 -0.3640,0.3805 -0.3816,0.3980 -0.3947,0.4178 -0.4057,0.4419'
        ' -0.4123,0.4792 -0.4057,0.5252 -0.3991,0.5406 -0.3925,0.5471 -0.3728,0.5274 -0.3728,0.5208 -0.3553,0'
        '.5099 -0.3092,0.4638 -0.3114,0.4529 -0.3202,0.4441 -0.3377,0.4419 -0.3487,0.4529 -0.3531,0.4682 -0.3'
        '750,0.4682 -0.3772,0.4550 -0.3706,0.4375 -0.3575,0.4243 -0.3465,0.4200 -0.3202,0.4178 -0.3004,0.4243'
        ' -0.2851,0.4397 -0.2127,0.3673ZM-0.4167,0.6809 -0.4123,0.6853 0.4496,0.6853 0.4561,0.6831 0.4693,0.6'
        '721 0.4737,0.6590 0.4737,0.3081 0.4715,0.2993 0.4561,0.2840 -0.0197,0.2840 -0.1338,0.3980 -0.1162,0.'
        '4353 -0.1096,0.4726 -0.1096,0.4923 -0.1162,0.5318 -0.1316,0.5669 -0.1447,0.5866 -0.1732,0.6151 -0.21'
        '05,0.6371 -0.2500,0.6480 -0.3026,0.6480 -0.3355,0.6393 -0.3618,0.6261ZM-0.0658,0.2840 -0.1535,0.3717'
        ' -0.1491,0.3761 -0.0614,0.2884ZM-0.1382,0.2840 -0.4583,0.2840 -0.4737,0.2971 -0.4759,0.3015 -0.4759,'
        '0.6217 -0.4715,0.6261 -0.4167,0.5713 -0.4298,0.5471 -0.4386,0.5186 -0.4408,0.4594 -0.4298,0.4200 -0.'
        '4189,0.3980 -0.4013,0.3739 -0.3618,0.3410 -0.3289,0.3257 -0.3026,0.3191 -0.2390,0.3213 -0.2105,0.330'
        '0 -0.1886,0.3432 -0.1338,0.2884ZM0.3596,-0.4156 -0.2061,0.1480 -0.2018,0.1546 -0.1557,0.1765 -0.0811'
        ',0.1985 -0.0263,0.2050 0.0504,0.2029 0.1118,0.1897 0.1864,0.1612 0.2368,0.1305 0.2654,0.1086 0.3004,'
        '0.0757 0.3421,0.0252 0.3772,-0.0362 0.3991,-0.0932 0.4145,-0.1721 0.4145,-0.2511 0.4057,-0.3059 0.38'
        '82,-0.3629 0.3728,-0.3980ZM0.1952,-0.5800 0.1754,-0.5910 0.1184,-0.6129 0.0570,-0.6261 0.0154,-0.630'
        '5 -0.0197,-0.6305 -0.0877,-0.6217 -0.1535,-0.6020 -0.2127,-0.5735 -0.2632,-0.5384 -0.3180,-0.4857 -0'
        '.3443,-0.4529 -0.3640,-0.4221 -0.3904,-0.3673 -0.4123,-0.2950 -0.4189,-0.2467 -0.4189,-0.1765 -0.412'
        '3,-0.1305 -0.3925,-0.0625 -0.3750,-0.0230 -0.3640,-0.0077 0.2018,-0.5735Z'
    ),
    '675B/2': (
        'M-0.3531,0.5932 -0.3750,0.6151 -0.3706,0.6195 -0.3487,0.5976ZM-0.3640,0.5822 -0.3882,0.6064 -0.3838,'
        '0.6107 -0.3596,0.5866ZM-0.3772,0.5713 -0.4013,0.5954 -0.3969,0.5998 -0.3728,0.5757ZM-0.3882,0.5581 -'
        '0.4123,0.5822 -0.4079,0.5866 -0.3838,0.5625ZM-0.2851,0.5252 -0.3026,0.5428 -0.2982,0.5471 -0.2807,0.'
        '5296ZM-0.3026,0.5208 -0.3268,0.5450 -0.3224,0.5493 -0.2982,0.5252ZM-0.3246,0.5186 -0.3487,0.5428 -0.'
        '3443,0.5471 -0.3202,0.5230ZM-0.3640,0.5121 -0.3750,0.5208 -0.3706,0.5274 -0.3596,0.5164ZM-0.2939,0.4'
        '879 -0.3136,0.5077 -0.3092,0.5121 -0.2895,0.4923ZM-0.2368,0.4770 -0.2632,0.5033 -0.2588,0.5077 -0.23'
        '25,0.4814ZM-0.2851,0.4550 -0.3728,0.5428 -0.3684,0.5471 -0.2807,0.4594ZM-0.1689,0.4353 -0.1908,0.455'
        '0 -0.1842,0.4682 -0.1842,0.5011 -0.1886,0.5121 -0.2018,0.5230 -0.2193,0.5208 -0.2346,0.4989 -0.2566,'
        '0.5208 -0.2478,0.5340 -0.2346,0.5450 -0.2149,0.5515 -0.1996,0.5515 -0.1776,0.5428 -0.1645,0.5296 -0.'
        '1535,0.4989 -0.1535,0.4704 -0.1579,0.4529ZM-0.1996,0.4178 -0.2632,0.4814 -0.2588,0.4857 -0.1952,0.42'
        '21ZM-0.2237,0.4178 -0.2610,0.4550 -0.2566,0.4594 -0.2193,0.4221ZM-0.2851,0.4397 -0.3004,0.4221 -0.32'
        '02,0.4156 -0.3465,0.4178 -0.3575,0.4221 -0.3728,0.4375 -0.3794,0.4550 -0.3794,0.4660 -0.3750,0.4704 '
        '-0.3531,0.4704 -0.3487,0.4660 -0.3465,0.4529 -0.3377,0.4441 -0.3202,0.4463 -0.3070,0.4638ZM-0.1338,0'
        '.3980 -0.1579,0.4221 -0.1447,0.4550 -0.1425,0.4989 -0.1491,0.5274 -0.1689,0.5647 -0.1930,0.5888 -0.2'
        '281,0.6086 -0.2522,0.6151 -0.2785,0.6173 -0.3180,0.6107 -0.3377,0.6020 -0.3618,0.6261 -0.3575,0.6305'
        ' -0.3355,0.6414 -0.3026,0.6502 -0.2390,0.6480 -0.1930,0.6305 -0.1732,0.6173 -0.1425,0.5866 -0.1294,0'
        '.5669 -0.1140,0.5318 -0.1075,0.4923 -0.1075,0.4726 -0.1140,0.4353 -0.1272,0.4046ZM-0.1535,0.3717 -0.'
        '1754,0.3936 -0.1711,0.3980 -0.1491,0.3761ZM-0.1645,0.3586 -0.1886,0.3827 -0.1842,0.3871 -0.1601,0.36'
        '29ZM-0.1776,0.3476 -0.2018,0.3717 -0.1974,0.3761 -0.1732,0.3542ZM-0.1930,0.3366 -0.2105,0.3279 -0.25'
        '00,0.3169 -0.3026,0.3169 -0.3289,0.3235 -0.3618,0.3388 -0.3860,0.3564 -0.4035,0.3739 -0.4211,0.3980 '
        '-0.4320,0.4200 -0.4430,0.4594 -0.4408,0.5186 -0.4320,0.5471 -0.4167,0.5735 -0.3925,0.5493 -0.4035,0.'
        '5252 -0.4101,0.4792 -0.4035,0.4419 -0.3925,0.4178 -0.3794,0.3980 -0.3640,0.3827 -0.3421,0.3673 -0.30'
        '04,0.3520 -0.2829,0.3498 -0.2522,0.3520 -0.2281,0.3586 -0.2105,0.3673 -0.1864,0.3432ZM-0.4649,-0.683'
        '1 -0.4759,-0.6700 -0.4759,0.1985 -0.4781,0.2007 -0.4781,0.2357 -0.4737,0.2489 -0.4583,0.2621 0.4539,'
        '0.2621 0.4627,0.2577 0.4693,0.2511 0.4737,0.2401 0.4737,-0.6656 0.4693,-0.6743 0.4539,-0.6875 -0.456'
        '1,-0.6875ZM-0.0197,-0.6283 0.0417,-0.6261 0.1184,-0.6107 0.1886,-0.5822 0.2281,-0.5581 0.2719,-0.525'
        '2 0.3114,-0.4857 0.3289,-0.4638 0.3706,-0.3980 0.3991,-0.3235 0.4123,-0.2511 0.4123,-0.1721 0.3969,-'
        '0.0932 0.3816,-0.0515 0.3618,-0.0099 0.3180,0.0537 0.2654,0.1064 0.2368,0.1283 0.1864,0.1590 0.1118,'
        '0.1875 0.0768,0.1963 0.0219,0.2029 -0.0548,0.2007 -0.1162,0.1875 -0.1557,0.1743 -0.2061,0.1502 -0.27'
        '41,0.1020 -0.3268,0.0471 -0.3728,-0.0230 -0.4013,-0.0954 -0.4101,-0.1305 -0.4167,-0.1765 -0.4167,-0.'
        '2467 -0.4101,-0.2950 -0.4013,-0.3300 -0.3882,-0.3673 -0.3618,-0.4221 -0.3421,-0.4529 -0.3158,-0.4857'
        ' -0.2763,-0.5252 -0.2434,-0.5515 -0.1798,-0.5888 -0.1535,-0.5998 -0.0877,-0.6195Z'
    ),
    '675B/3': (
        'M-0.0241,0.2884 -0.0373,0.2884 -0.4298,0.6809 -0.4167,0.6809ZM-0.0482,0.2884 -0.0614,0.2884 -0.4518,'
        '0.6787 -0.4408,0.6809ZM-0.0702,0.2884 -0.0855,0.2884 -0.4671,0.6721 -0.4605,0.6765ZM-0.0943,0.2884 -'
        '0.1075,0.2884 -0.2807,0.4594 -0.4715,0.6524 -0.4715,0.6656ZM-0.1184,0.2884 -0.1316,0.2884 -0.4715,0.'
        '6283 -0.4715,0.6414Z'
    ),
    '878/0': (
        'M-0.4638,-0.6292 -0.4871,-0.6059 -0.5000,-0.5749 -0.5000,0.5698 -0.4974,0.5827 -0.4845,0.6059 -0.461'
        '2,0.6266 -0.4225,0.6370 0.4199,0.6370 0.4587,0.6266 0.4845,0.6034 0.4922,0.5879 0.4974,0.5646 0.4974'
        ',-0.5672 0.4948,-0.5853 0.4871,-0.6034 0.4612,-0.6292 0.4276,-0.6395 -0.4302,-0.6395Z'
    ),
    '878/1': (
        'M-0.1357,-0.3424 -0.1641,-0.3346 -0.1925,-0.3062 -0.2054,-0.2752 -0.2054,-0.2519 -0.1925,-0.2209 -0.'
        '1667,-0.1951 -0.1331,-0.1848 -0.1202,-0.1848 -0.0814,-0.1977 -0.0633,-0.2158 -0.0504,-0.2416 -0.0478'
        ',-0.2778 -0.0607,-0.3088 -0.0840,-0.3320 -0.1047,-0.3398ZM-0.1615,-0.3088 -0.1382,-0.3191 -0.1150,-0'
        '.3191 -0.0943,-0.3114 -0.0788,-0.2959 -0.0685,-0.2752 -0.0685,-0.2545 -0.0762,-0.2364 -0.0917,-0.218'
        '3 -0.1098,-0.2106 -0.1408,-0.2106 -0.1563,-0.2158 -0.1744,-0.2339 -0.1822,-0.2494 -0.1822,-0.2778 -0'
        '.1770,-0.2907ZM-0.0426,-0.5052 -0.0659,-0.4819 -0.0685,-0.4509 -0.0452,-0.4225 -0.0065,-0.4225 0.016'
        '8,-0.4535 0.0168,-0.4742 -0.0039,-0.5026 -0.0220,-0.5078ZM-0.0349,-0.4897 -0.0168,-0.4897 -0.0065,-0'
        '.4845 -0.0013,-0.4716 -0.0039,-0.4483 -0.0116,-0.4406 -0.0245,-0.4354 -0.0401,-0.4406 -0.0504,-0.450'
        '9 -0.0504,-0.4587 -0.0556,-0.4638 -0.0504,-0.4690 -0.0478,-0.4819ZM-0.4406,-0.5956 -0.4561,-0.5801 -'
        '0.4612,-0.5646 -0.4612,0.5594 -0.4535,0.5801 -0.4380,0.5930 -0.4276,0.5956 0.4251,0.5956 0.4432,0.58'
        '79 0.4535,0.5775 0.4587,0.5568 0.4587,-0.5620 0.4509,-0.5853 0.4380,-0.5956 0.4199,-0.6008 -0.4225,-'
        '0.6008ZM0.2442,-0.3915 0.2468,-0.3889 0.2468,-0.2649 0.2442,-0.2623 0.1873,-0.2623 0.1822,-0.2571 0.'
        '1822,-0.2028 0.1796,-0.2003 0.0814,-0.2003 0.0788,-0.2028 0.0814,-0.2261 0.1537,-0.2261 0.1589,-0.23'
        '13 0.1589,-0.4251 0.1615,-0.4276 0.1822,-0.4251 0.1822,-0.3966 0.1873,-0.3915ZM0.1202,-0.4587 0.1434'
        ',-0.4561 0.1434,-0.2442 0.1408,-0.2416 0.1176,-0.2442 0.1176,-0.4561ZM0.0814,-0.4716 0.1021,-0.4690 '
        '0.1021,-0.2442 0.0995,-0.2416 0.0788,-0.2442 0.0788,-0.4690ZM-0.2235,-0.5362 -0.2106,-0.5362 -0.2028'
        ',-0.5413 0.0116,-0.5413 0.0194,-0.5362 0.0323,-0.5362 0.0530,-0.5207 0.0633,-0.4974 0.0633,-0.1796 0'
        '.0556,-0.1615 0.0452,-0.1486 0.0116,-0.1357 -0.2028,-0.1357 -0.2313,-0.1460 -0.2442,-0.1589 -0.2519,'
        '-0.1796 -0.2519,-0.5000 -0.2442,-0.5181Z'
    ),
    '878/2': (
        'M-0.1537,-0.1899 -0.1434,-0.1744 -0.1434,-0.1589 -0.1486,-0.1486 -0.1615,-0.1382 -0.0917,-0.1382 -0.'
        '1047,-0.1486 -0.1098,-0.1589 -0.1098,-0.1744 -0.0995,-0.1899 -0.1253,-0.1822ZM0.2468,-0.2829 0.2442,'
        '-0.2752 0.2313,-0.2649 0.2468,-0.2649ZM0.1822,-0.2623 0.1718,-0.2649 0.1615,-0.2752 0.1589,-0.2829 0'
        '.1589,-0.2261 0.1563,-0.2235 0.0788,-0.2235 0.0788,-0.2028 0.1796,-0.2028 0.1796,-0.2597ZM-0.2494,-0'
        '.3010 -0.2494,-0.2261 -0.2339,-0.2416 -0.2209,-0.2442 -0.2003,-0.2364 -0.2054,-0.2468 -0.2054,-0.280'
        '4 -0.2003,-0.2907 -0.2209,-0.2829 -0.2339,-0.2855ZM0.2313,-0.3889 0.2442,-0.3786 0.2468,-0.3708 0.24'
        '68,-0.3889ZM0.1796,-0.4251 0.1589,-0.4251 0.1589,-0.3708 0.1615,-0.3786 0.1718,-0.3889 0.1822,-0.391'
        '5 0.1796,-0.3941ZM0.1176,-0.4587 0.1176,-0.2442 0.1408,-0.2442 0.1408,-0.4587ZM0.0788,-0.4716 0.0788'
        ',-0.2442 0.0995,-0.2442 0.0995,-0.4716ZM-0.0349,-0.4897 -0.0478,-0.4793 -0.0530,-0.4612 -0.0478,-0.4'
        '483 -0.0375,-0.4406 -0.0220,-0.4380 -0.0039,-0.4483 -0.0013,-0.4716 -0.0039,-0.4793 -0.0194,-0.4897Z'
        'M-0.0685,-0.5388 -0.0556,-0.5284 -0.0504,-0.5181 -0.0504,-0.5026 -0.0401,-0.5078 -0.0142,-0.5078 -0.'
        '0065,-0.5052 0.0116,-0.4871 0.0194,-0.4716 0.0194,-0.4561 0.0116,-0.4432 0.0323,-0.4509 0.0452,-0.44'
        '83 0.0607,-0.4328 0.0607,-0.5000 0.0530,-0.5181 0.0297,-0.5362 0.0142,-0.5388Z'
    ),
    '880/0': (
        'M-0.4751,-0.8832 -0.4907,-0.8676 -0.5000,-0.8396 -0.5000,0.8364 -0.4907,0.8645 -0.4720,0.8832 -0.450'
        '2,0.8894 0.4470,0.8894 0.4688,0.8832 0.4844,0.8707 0.4969,0.8458 0.4969,-0.8489 0.4907,-0.8645 0.468'
        '8,-0.8863 0.4470,-0.8925 -0.4502,-0.8925Z'
    ),
    '880/1': (
        'M-0.0514,0.0763 -0.1044,0.0888 -0.1636,0.1168 -0.2103,0.1511 -0.2632,0.2103 -0.2944,0.2664 -0.3131,0'
        '.3255 -0.3193,0.3816 -0.3162,0.4346 -0.2975,0.5062 -0.2726,0.5561 -0.2508,0.5872 -0.2009,0.6371 -0.1'
        '667,0.6620 -0.0981,0.6931 -0.0421,0.7056 0.0389,0.7056 0.1044,0.6900 0.1573,0.6651 0.1978,0.6371 0.2'
        '445,0.5903 0.2850,0.5280 0.3037,0.4782 0.3131,0.4346 0.3131,0.3972 0.3162,0.3941 0.3131,0.3474 0.297'
        '5,0.2819 0.2664,0.2196 0.2352,0.1791 0.1791,0.1293 0.1168,0.0950 0.0670,0.0794 0.0234,0.0732ZM-0.038'
        '9,-0.0202 -0.1293,-0.0016 -0.1947,0.0265 -0.2601,0.0701 -0.3224,0.1324 -0.3660,0.1978 -0.3972,0.2757'
        ' -0.4128,0.3598 -0.4128,0.4221 -0.3972,0.5062 -0.3816,0.5498 -0.3567,0.5997 -0.3193,0.6526 -0.2601,0'
        '.7118 -0.2009,0.7523 -0.1168,0.7866 -0.0327,0.8022 0.0296,0.8022 0.1137,0.7866 0.1978,0.7523 0.2570,'
        '0.7118 0.3193,0.6495 0.3629,0.5841 0.3941,0.5062 0.4097,0.4190 0.4097,0.3629 0.3941,0.2757 0.3598,0.'
        '1916 0.3193,0.1324 0.2570,0.0701 0.1916,0.0265 0.1044,-0.0078 0.0358,-0.0202ZM-0.0047,-0.0047 0.0826'
        ',0.0047 0.1511,0.0265 0.2103,0.0576 0.2664,0.1012 0.3069,0.1449 0.3411,0.1947 0.3754,0.2757 0.3910,0'
        '.3505 0.3910,0.4283 0.3754,0.5062 0.3411,0.5841 0.2975,0.6464 0.2539,0.6900 0.1978,0.7305 0.1542,0.7'
        '523 0.1106,0.7679 0.0296,0.7835 -0.0327,0.7835 -0.1137,0.7679 -0.1947,0.7336 -0.2539,0.6931 -0.3037,'
        '0.6433 -0.3442,0.5841 -0.3660,0.5405 -0.3816,0.4938 -0.3941,0.4221 -0.3910,0.3318 -0.3723,0.2570 -0.'
        '3442,0.1947 -0.2913,0.1231 -0.2227,0.0639 -0.1542,0.0265 -0.0857,0.0047ZM-0.1854,-0.4938 -0.2165,-0.'
        '4813 -0.2477,-0.4533 -0.2664,-0.4159 -0.2695,-0.3816 -0.2632,-0.3536 -0.2539,-0.3349 -0.2290,-0.3069'
        ' -0.1916,-0.2882 -0.1511,-0.2850 -0.1044,-0.3037 -0.0794,-0.3287 -0.0607,-0.3692 -0.0607,-0.4097 -0.'
        '0763,-0.4470 -0.1075,-0.4782 -0.1449,-0.4938ZM-0.1978,-0.4595 -0.1822,-0.4657 -0.1386,-0.4626 -0.116'
        '8,-0.4502 -0.0919,-0.4159 -0.0888,-0.3754 -0.0950,-0.3567 -0.1075,-0.3380 -0.1324,-0.3193 -0.1604,-0'
        '.3131 -0.1947,-0.3193 -0.2072,-0.3255 -0.2290,-0.3474 -0.2414,-0.3816 -0.2352,-0.4221 -0.2259,-0.437'
        '7ZM-0.0483,-0.7118 -0.0639,-0.7056 -0.0857,-0.6838 -0.0950,-0.6620 -0.0950,-0.6402 -0.0857,-0.6184 -'
        '0.0670,-0.5997 -0.0421,-0.5903 -0.0265,-0.5903 -0.0016,-0.5997 0.0171,-0.6184 0.0265,-0.6371 0.0265,'
        '-0.6651 0.0140,-0.6900 -0.0047,-0.7056 -0.0202,-0.7118ZM-0.0545,-0.6807 -0.0327,-0.6869 -0.0140,-0.6'
        '807 -0.0047,-0.6713 0.0016,-0.6495 -0.0109,-0.6246 -0.0234,-0.6184 -0.0421,-0.6184 -0.0514,-0.6215 -'
        '0.0639,-0.6340 -0.0670,-0.6620ZM-0.3785,-0.7928 -0.3847,-0.7773 -0.3847,-0.1978 -0.3816,-0.1885 -0.3'
        '598,-0.1698 0.3567,-0.1698 0.3785,-0.1854 0.3816,-0.1947 0.3816,-0.7835 0.3660,-0.8022 0.3598,-0.805'
        '3 -0.3629,-0.8053ZM0.3224,-0.5561 0.3255,-0.5530 0.3255,-0.3910 0.3224,-0.3879 0.2445,-0.3879 0.2383'
        ',-0.3816 0.2383,-0.3100 0.2352,-0.3069 0.1075,-0.3069 0.1044,-0.3100 0.1075,-0.3411 0.2040,-0.3411 0'
        '.2103,-0.3474 0.2103,-0.5997 0.2134,-0.6028 0.2383,-0.5997 0.2383,-0.5623 0.2445,-0.5561ZM0.1604,-0.'
        '6433 0.1854,-0.6402 0.1854,-0.3660 0.1822,-0.3629 0.1573,-0.3660 0.1573,-0.6402ZM0.1075,-0.6620 0.13'
        '55,-0.6589 0.1355,-0.3660 0.1324,-0.3629 0.1044,-0.3660 0.1044,-0.6589ZM-0.3006,-0.7399 -0.2819,-0.7'
        '492 0.0327,-0.7492 0.0483,-0.7430 0.0701,-0.7243 0.0826,-0.6900 0.0826,-0.2850 0.0732,-0.2570 0.0576'
        ',-0.2383 0.0327,-0.2259 -0.2788,-0.2259 -0.2944,-0.2321 -0.3162,-0.2508 -0.3287,-0.2757 -0.3287,-0.6'
        '994 -0.3162,-0.7243Z'
    ),
    '880/2': (
        'M-0.1698,-0.4688 -0.2009,-0.4595 -0.2290,-0.4346 -0.2414,-0.4065 -0.2414,-0.3723 -0.2290,-0.3442 -0.'
        '2040,-0.3224 -0.1822,-0.3131 -0.1480,-0.3131 -0.1293,-0.3193 -0.1012,-0.3442 -0.0919,-0.3598 -0.0857'
        ',-0.3910 -0.0981,-0.4315 -0.1199,-0.4533 -0.1449,-0.4657ZM0.3224,-0.5561 0.2445,-0.5561 0.2414,-0.55'
        '92 0.2414,-0.5997 0.2352,-0.6059 0.2134,-0.6059 0.2072,-0.5997 0.2072,-0.3474 0.2040,-0.3442 0.1106,'
        '-0.3442 0.1044,-0.3380 0.1044,-0.3100 0.1106,-0.3037 0.2352,-0.3037 0.2414,-0.3100 0.2414,-0.3847 0.'
        '2445,-0.3879 0.3224,-0.3879 0.3287,-0.3941 0.3287,-0.5498ZM0.1636,-0.6464 0.1573,-0.6402 0.1573,-0.3'
        '692 0.1636,-0.3629 0.1822,-0.3629 0.1885,-0.3692 0.1885,-0.6402 0.1822,-0.6464ZM0.1106,-0.6651 0.104'
        '4,-0.6589 0.1044,-0.3692 0.1106,-0.3629 0.1293,-0.3629 0.1355,-0.3692 0.1355,-0.6589 0.1293,-0.6651Z'
        'M-0.0421,-0.6869 -0.0514,-0.6838 -0.0639,-0.6713 -0.0701,-0.6589 -0.0701,-0.6464 -0.0545,-0.6215 -0.'
        '0327,-0.6153 -0.0140,-0.6215 0.0016,-0.6402 0.0016,-0.6620 -0.0171,-0.6838ZM-0.3037,-0.7399 -0.3224,'
        '-0.7181 -0.3318,-0.6900 -0.3318,-0.2882 -0.3193,-0.2539 -0.2975,-0.2321 -0.2695,-0.2227 0.0202,-0.22'
        '27 0.0545,-0.2352 0.0701,-0.2508 0.0826,-0.2757 0.0826,-0.6994 0.0732,-0.7212 0.0514,-0.7430 0.0296,'
        '-0.7523 -0.2757,-0.7523ZM-0.1729,-0.4938 -0.1386,-0.4907 -0.1012,-0.4720 -0.0763,-0.4439 -0.0670,-0.'
        '4252 -0.0607,-0.3972 -0.0670,-0.3536 -0.0826,-0.3255 -0.1075,-0.3037 -0.1449,-0.2882 -0.1854,-0.2882'
        ' -0.2165,-0.3006 -0.2508,-0.3318 -0.2664,-0.3692 -0.2664,-0.4097 -0.2445,-0.4564 -0.2196,-0.4782 -0.'
        '2009,-0.4875ZM-0.0389,-0.7118 -0.0140,-0.7087 -0.0016,-0.7025 0.0171,-0.6838 0.0265,-0.6589 0.0234,-'
        '0.6340 0.0140,-0.6153 0.0016,-0.6028 -0.0202,-0.5935 -0.0483,-0.5935 -0.0639,-0.5997 -0.0794,-0.6121'
        ' -0.0919,-0.6371 -0.0919,-0.6682 -0.0826,-0.6869 -0.0607,-0.7056Z'
    ),
    '880/3': (
        'M-0.0047,-0.0078 -0.0857,0.0016 -0.1542,0.0234 -0.2227,0.0607 -0.2944,0.1231 -0.3474,0.1947 -0.3754,'
        '0.2570 -0.3941,0.3318 -0.3972,0.4221 -0.3847,0.4938 -0.3692,0.5405 -0.3474,0.5841 -0.3069,0.6433 -0.'
        '2539,0.6963 -0.1947,0.7368 -0.1137,0.7710 -0.0327,0.7866 0.0296,0.7866 0.1106,0.7710 0.1542,0.7555 0'
        '.1978,0.7336 0.2539,0.6931 0.3006,0.6464 0.3442,0.5841 0.3785,0.5062 0.3941,0.4283 0.3941,0.3505 0.3'
        '785,0.2757 0.3442,0.1947 0.3100,0.1449 0.2664,0.0981 0.2103,0.0545 0.1511,0.0234 0.0826,0.0016ZM-0.0'
        '514,0.0794 0.0234,0.0763 0.0670,0.0826 0.1168,0.0981 0.1791,0.1324 0.2321,0.1791 0.2632,0.2196 0.294'
        '4,0.2819 0.3100,0.3474 0.3131,0.3941 0.3100,0.3972 0.3100,0.4346 0.3006,0.4782 0.2819,0.5280 0.2414,'
        '0.5903 0.1978,0.6340 0.1573,0.6620 0.1044,0.6869 0.0389,0.7025 -0.0421,0.7025 -0.0763,0.6963 -0.1231'
        ',0.6807 -0.1667,0.6589 -0.2009,0.6340 -0.2477,0.5872 -0.2695,0.5561 -0.2944,0.5062 -0.3131,0.4346 -0'
        '.3162,0.3816 -0.3100,0.3255 -0.2913,0.2664 -0.2601,0.2103 -0.2103,0.1542 -0.1636,0.1199 -0.1044,0.09'
        '19Z'
    ),
    '818.5/0': (
        'M-0.4895,-0.6695 -0.4979,-0.6589 -0.5000,-0.6484 -0.5000,0.6463 -0.4958,0.6611 -0.4874,0.6695 -0.476'
        '8,0.6737 0.4747,0.6737 0.4853,0.6695 0.4937,0.6611 0.4979,0.6505 0.4979,-0.6505 0.4937,-0.6632 0.485'
        '3,-0.6716 0.4705,-0.6758 -0.4726,-0.6758Z'
    ),
    '818.5/1': (
        'M-0.0011,-0.1263 -0.0242,-0.0905 -0.1063,0.0547 -0.1126,0.0611 -0.1253,0.0611 -0.1295,0.0653 -0.1295'
        ',0.0947 -0.2242,0.2568 -0.2200,0.2611 0.2179,0.2611 0.2221,0.2568 0.1274,0.0947 0.1253,0.0653 0.1211'
        ',0.0611 0.1105,0.0611 0.1042,0.0547 0.0137,-0.1053ZM-0.0474,-0.0168 -0.0453,-0.0189 0.0432,-0.0189 0'
        '.0453,-0.0147 -0.0011,0.0611ZM-0.0242,-0.1916 -0.0389,-0.1789 -0.2853,0.2463 -0.2916,0.2611 -0.2916,'
        '0.2821 -0.2853,0.2968 -0.2705,0.3116 -0.2474,0.3200 0.2453,0.3200 0.2663,0.3137 0.2832,0.2968 0.2895'
        ',0.2821 0.2895,0.2611 0.2705,0.2232 0.0368,-0.1789 0.0263,-0.1895 0.0137,-0.1958 -0.0053,-0.1979ZM-0'
        '.0200,-0.1832 -0.0074,-0.1874 0.0053,-0.1874 0.0242,-0.1789 0.0347,-0.1663 0.2768,0.2547 0.2811,0.27'
        '16 0.2789,0.2842 0.2747,0.2926 0.2621,0.3053 0.2516,0.3095 -0.2537,0.3095 -0.2663,0.3032 -0.2768,0.2'
        '926 -0.2811,0.2821 -0.2811,0.2611 -0.2768,0.2505 -0.0411,-0.1579Z'
    ),
    '818.5/2': (
        'M-0.0200,-0.1853 -0.0368,-0.1684 -0.2789,0.2505 -0.2832,0.2611 -0.2832,0.2821 -0.2789,0.2926 -0.2663'
        ',0.3053 -0.2537,0.3116 0.2516,0.3116 0.2621,0.3074 0.2768,0.2926 0.2832,0.2716 0.2789,0.2547 0.0368,'
        '-0.1663 0.0179,-0.1853 0.0053,-0.1895 -0.0074,-0.1895ZM-0.0011,-0.1242 0.1021,0.0547 0.1105,0.0632 0'
        '.1232,0.0653 0.1232,0.0905 0.2200,0.2568 0.2179,0.2589 -0.2200,0.2589 -0.2221,0.2568 -0.1274,0.0947 '
        '-0.1274,0.0653 -0.1126,0.0632 -0.1042,0.0547Z'
    ),
    '818.5/3': (
        'M0.0432,-0.0211 -0.0453,-0.0211 -0.0495,-0.0168 -0.0011,0.0632 0.0474,-0.0168Z'
    ),
    '636/0': (
        'M0.4162,-0.4869 0.3874,-0.5026 0.3639,-0.4974 0.3325,-0.5052 0.3115,-0.5052 0.2147,-0.4581 0.1806,-0'
        '.4476 0.1440,-0.4476 0.1283,-0.4529 0.0759,-0.4869 0.0628,-0.4869 0.0445,-0.4738 0.0157,-0.4738 -0.0'
        '445,-0.4581 -0.0681,-0.4634 -0.0969,-0.4791 -0.1230,-0.4791 -0.1623,-0.4712 -0.1963,-0.4529 -0.2120,'
        '-0.4529 -0.2277,-0.4607 -0.2513,-0.4607 -0.2644,-0.4529 -0.3534,-0.4581 -0.3770,-0.4738 -0.4031,-0.4'
        '817 -0.4267,-0.4791 -0.4424,-0.4634 -0.4869,-0.4084 -0.4948,-0.3901 -0.5000,-0.3639 -0.4974,-0.3560 '
        '-0.5000,-0.3482 -0.4974,-0.2644 -0.4921,-0.2225 -0.4921,-0.1466 -0.4712,-0.0733 -0.4712,-0.0524 -0.4'
        '921,0.0314 -0.4921,0.0628 -0.4817,0.1126 -0.4738,0.3089 -0.4817,0.3665 -0.4948,0.4110 -0.4948,0.4581'
        ' -0.4895,0.4712 -0.4817,0.4791 -0.4634,0.4791 -0.4346,0.4476 -0.4136,0.4450 -0.3822,0.4503 -0.2906,0'
        '.4555 -0.2225,0.4895 -0.2016,0.4948 -0.1283,0.4764 -0.0969,0.4764 -0.0524,0.5026 -0.0419,0.5026 -0.0'
        '236,0.4843 0.0236,0.4712 0.0707,0.4634 0.0969,0.4660 0.1492,0.4869 0.1702,0.4869 0.1937,0.4817 0.259'
        '2,0.4581 0.2775,0.4581 0.2984,0.4712 0.3141,0.4555 0.4450,0.4634 0.4660,0.4529 0.4869,0.4319 0.4974,'
        '0.4031 0.4921,0.3429 0.4869,0.3194 0.4738,0.3037 0.4634,0.2827 0.4555,0.2251 0.4555,0.1937 0.4869,0.'
        '1387 0.4921,0.1204 0.4817,0.0105 0.4686,-0.0288 0.4607,-0.0864 0.4686,-0.2225 0.4634,-0.2461 0.4476,'
        '-0.2749 0.4398,-0.3063 0.4293,-0.3953 0.4319,-0.4581 0.4267,-0.4738Z'
    ),
    '636/1': (
        'M0.4084,-0.4843 0.3901,-0.4948 0.3534,-0.4921 0.3220,-0.5000 0.3089,-0.4974 0.3037,-0.4921 0.1990,-0'
        '.4450 0.1623,-0.4398 0.1387,-0.4450 0.1361,-0.4424 0.1152,-0.4529 0.0785,-0.4791 0.0654,-0.4791 0.05'
        '24,-0.4686 0.0209,-0.4686 -0.0419,-0.4529 -0.0576,-0.4555 -0.0602,-0.4529 -0.0942,-0.4712 -0.1152,-0'
        '.4738 -0.1649,-0.4634 -0.1990,-0.4450 -0.2173,-0.4476 -0.2356,-0.4555 -0.2513,-0.4529 -0.2592,-0.445'
        '0 -0.3586,-0.4529 -0.3770,-0.4660 -0.3979,-0.4738 -0.4215,-0.4738 -0.4764,-0.4110 -0.4921,-0.3770 -0'
        '.4921,-0.2749 -0.4895,-0.2723 -0.4895,-0.2330 -0.4843,-0.1885 -0.4843,-0.1387 -0.4660,-0.0785 -0.466'
        '0,-0.0471 -0.4712,-0.0366 -0.4869,0.0393 -0.4869,0.0576 -0.4764,0.1047 -0.4712,0.2565 -0.4686,0.2592'
        ' -0.4712,0.3482 -0.4895,0.4188 -0.4895,0.4503 -0.4791,0.4712 -0.4712,0.4738 -0.4346,0.4398 -0.4058,0'
        '.4398 -0.3455,0.4476 -0.2958,0.4476 -0.2775,0.4529 -0.2094,0.4869 -0.1911,0.4869 -0.1466,0.4738 -0.1'
        '047,0.4686 -0.0916,0.4712 -0.0628,0.4895 -0.0471,0.4948 -0.0340,0.4817 -0.0131,0.4738 0.0654,0.4581 '
        '0.1021,0.4607 0.1361,0.4764 0.1571,0.4817 0.1885,0.4764 0.2277,0.4607 0.2670,0.4503 0.2853,0.4529 0.'
        '2932,0.4581 0.3037,0.4476 0.3063,0.4503 0.3168,0.4476 0.3743,0.4555 0.4372,0.4581 0.4581,0.4503 0.48'
        '17,0.4267 0.4895,0.4084 0.4869,0.3508 0.4817,0.3246 0.4581,0.2880 0.4476,0.1963 0.4843,0.1257 0.4843'
        ',0.0890 0.4764,0.0157 0.4634,-0.0236 0.4555,-0.0785 0.4607,-0.2330 0.4372,-0.2880 0.4241,-0.3874 0.4'
        '241,-0.4607ZM-0.0785,-0.4058 0.0262,-0.4084 0.0759,-0.4005 0.1230,-0.3874 0.1675,-0.3691 0.2277,-0.3'
        '325 0.2906,-0.2775 0.3429,-0.2068 0.3770,-0.1335 0.3953,-0.0602 0.3979,0.0445 0.3901,0.0916 0.3639,0'
        '.1728 0.3246,0.2408 0.2958,0.2775 0.2592,0.3141 0.2147,0.3482 0.1387,0.3874 0.0916,0.4031 0.0550,0.4'
        '110 -0.0236,0.4162 -0.1073,0.4058 -0.1780,0.3822 -0.2487,0.3429 -0.2853,0.3141 -0.3220,0.2775 -0.366'
        '5,0.2173 -0.3979,0.1545 -0.4215,0.0681 -0.4241,-0.0393 -0.4162,-0.0864 -0.3953,-0.1545 -0.3560,-0.22'
        '77 -0.3168,-0.2775 -0.2723,-0.3194 -0.2435,-0.3403 -0.1702,-0.3796 -0.1335,-0.3927Z'
    ),
    '636/2': (
        'M-0.2775,-0.1963 -0.2984,-0.1675 -0.3194,-0.1257 -0.3351,-0.0812 -0.3429,-0.0393 -0.3455,0.0157 -0.3'
        '403,0.0628 -0.3272,0.1126 -0.3037,0.1649 -0.2670,0.2173 -0.2277,0.2565 -0.1806,0.2906 -0.1309,0.3141'
        ' -0.0628,0.3325 0.0157,0.3351 0.0628,0.3272 0.1178,0.3089 0.1780,0.2749 0.1859,0.2670ZM-0.2120,-0.26'
        '18 0.2513,0.2016 0.2801,0.1597 0.3037,0.1047 0.3141,0.0628 0.3194,-0.0052 0.3141,-0.0576 0.3010,-0.1'
        '073 0.2749,-0.1623 0.2356,-0.2173 0.1911,-0.2592 0.1440,-0.2906 0.0707,-0.3194 0.0288,-0.3272 -0.028'
        '8,-0.3298 -0.0969,-0.3194 -0.1492,-0.3010Z'
    ),
    '636/3': (
        'M-0.0681,-0.4084 -0.1387,-0.3927 -0.1911,-0.3717 -0.2251,-0.3534 -0.2827,-0.3115 -0.3272,-0.2670 -0.'
        '3482,-0.2408 -0.3874,-0.1754 -0.4058,-0.1309 -0.4162,-0.0942 -0.4267,-0.0288 -0.4241,0.0576 -0.4110,'
        '0.1204 -0.4005,0.1518 -0.3770,0.2016 -0.3325,0.2670 -0.2749,0.3246 -0.2225,0.3613 -0.1754,0.3848 -0.'
        '1230,0.4031 -0.0497,0.4162 0.0497,0.4136 0.1361,0.3901 0.1963,0.3613 0.2670,0.3089 0.3168,0.2539 0.3'
        '639,0.1754 0.3901,0.0995 0.4005,0.0314 0.4005,-0.0262 0.3953,-0.0681 0.3717,-0.1518 0.3377,-0.2173 0'
        '.3010,-0.2670 0.2565,-0.3115 0.2304,-0.3325 0.1649,-0.3717 0.0838,-0.4005 0.0131,-0.4110ZM-0.2775,-0'
        '.1937 0.1832,0.2670 0.1545,0.2880 0.1178,0.3063 0.0733,0.3220 0.0157,0.3325 -0.0419,0.3325 -0.0995,0'
        '.3220 -0.1440,0.3063 -0.1937,0.2801 -0.2277,0.2539 -0.2644,0.2173 -0.3010,0.1649 -0.3246,0.1126 -0.3'
        '403,0.0471 -0.3429,-0.0079 -0.3325,-0.0812 -0.3168,-0.1257ZM-0.1702,-0.2880 -0.1230,-0.3089 -0.0733,'
        '-0.3220 0.0026,-0.3272 0.0707,-0.3168 0.1230,-0.2984 0.1702,-0.2723 0.2068,-0.2435 0.2461,-0.2016 0.'
        '2723,-0.1623 0.2984,-0.1073 0.3141,-0.0393 0.3168,0.0105 0.3089,0.0759 0.2880,0.1387 0.2565,0.1937 0'
        '.2513,0.1990 -0.2094,-0.2618Z'
    ),
    '640.1/0': (
        'M-0.4392,-0.5273 -0.4581,-0.4769 -0.4623,-0.3532 -0.4665,-0.3218 -0.4476,-0.2589 -0.4476,-0.2421 -0.'
        '4706,-0.1646 -0.4686,-0.1017 -0.4665,-0.0996 -0.4665,-0.0409 -0.4644,-0.0388 -0.4665,-0.0283 -0.4518'
        ',0.0283 -0.4518,0.0409 -0.4790,0.1709 -0.4832,0.2023 -0.4874,0.2128 -0.4874,0.2379 -0.5000,0.3637 -0'
        '.4937,0.3700 -0.4602,0.4287 -0.4308,0.4665 -0.3532,0.5147 -0.3008,0.5189 -0.2631,0.5252 -0.2610,0.52'
        '31 -0.1394,0.5231 -0.1352,0.5252 -0.0828,0.4937 0.0535,0.4832 0.1059,0.4937 0.1583,0.5000 0.2652,0.4'
        '769 0.2883,0.4790 0.4182,0.5168 0.4602,0.4686 0.4769,0.3763 0.4979,0.3449 0.4686,0.2002 0.4057,-0.06'
        '39 0.3574,-0.1960 0.3532,-0.3470 0.3658,-0.3805 0.3658,-0.3931 0.3470,-0.4769 0.3470,-0.4895 0.3113,'
        '-0.5189 0.3071,-0.5168 0.2212,-0.5168 0.2149,-0.5189 0.1205,-0.4979 0.1038,-0.4979 -0.0220,-0.5168 -'
        '0.2233,-0.5189 -0.2820,-0.5126 -0.3679,-0.5084Z'
    ),
    '640.1/1': (
        'M-0.4350,-0.5210 -0.4392,-0.5168 -0.4539,-0.4706 -0.4539,-0.4308 -0.4560,-0.4287 -0.4560,-0.3910 -0.'
        '4602,-0.3491 -0.4602,-0.3176 -0.4413,-0.2484 -0.4644,-0.1688 -0.4602,-0.0199 -0.4455,0.0367 -0.4497,'
        '0.0451 -0.4811,0.2044 -0.4958,0.3595 -0.4623,0.4161 -0.4329,0.4560 -0.4161,0.4706 -0.3491,0.5105 -0.'
        '2799,0.5189 -0.1352,0.5189 -0.0870,0.4895 0.0472,0.4811 0.0493,0.4790 0.1562,0.4958 0.2631,0.4748 0.'
        '2736,0.4706 0.4015,0.5084 0.4161,0.5105 0.4560,0.4644 0.4727,0.3847 0.4727,0.3721 0.4916,0.3470 0.49'
        '16,0.3365 0.4371,0.0807 0.4015,-0.0618 0.3532,-0.1939 0.3491,-0.3470 0.3616,-0.3826 0.3616,-0.3910 0'
        '.3428,-0.4853 0.3113,-0.5126 0.2065,-0.5126 0.1143,-0.4916 0.1017,-0.4958 -0.0325,-0.5126 -0.2233,-0'
        '.5147 -0.2254,-0.5126 -0.3365,-0.5063 -0.3637,-0.5021 -0.3721,-0.5063ZM-0.0514,-0.3826 -0.0094,-0.38'
        '26 0.0115,-0.3784 0.0409,-0.3679 0.0744,-0.3470 0.1017,-0.3197 0.1184,-0.2945 0.1331,-0.2568 0.1373,'
        '-0.2338 0.1373,-0.1939 0.1310,-0.1646 0.1059,-0.1143 0.0807,-0.0870 0.0577,-0.0702 0.0283,-0.0556 -0'
        '.0052,-0.0472 -0.0346,-0.0451 -0.0681,-0.0493 -0.0954,-0.0577 -0.1268,-0.0744 -0.1709,-0.1184 -0.189'
        '7,-0.1541 -0.1981,-0.1876 -0.2002,-0.2170 -0.1960,-0.2505 -0.1834,-0.2883 -0.1667,-0.3155 -0.1415,-0'
        '.3428 -0.1143,-0.3616 -0.0933,-0.3721Z'
    ),
    '640.1/2': (
        'M-0.1394,-0.2945 -0.1562,-0.2694 -0.1667,-0.2338 -0.1667,-0.1960 -0.1625,-0.1771 -0.1394,-0.1310 -0.'
        '1143,-0.1059 -0.1017,-0.0975 -0.0702,-0.0828 -0.0514,-0.0786 0.0010,-0.0807 0.0409,-0.0975 0.0493,-0'
        '.1080ZM-0.1059,-0.3281 -0.1101,-0.3218 0.0786,-0.1352 0.0849,-0.1415 0.0996,-0.1730 0.1059,-0.2086 0'
        '.1017,-0.2484 0.0933,-0.2715 0.0786,-0.2966 0.0514,-0.3239 0.0388,-0.3323 -0.0052,-0.3491 -0.0430,-0'
        '.3512 -0.0660,-0.3470Z'
    ),
    '640.1/3': (
        'M-0.0577,-0.3826 -0.0912,-0.3742 -0.1164,-0.3616 -0.1352,-0.3491 -0.1646,-0.3197 -0.1813,-0.2945 -0.'
        '1960,-0.2568 -0.2002,-0.2358 -0.2002,-0.1939 -0.1897,-0.1520 -0.1771,-0.1268 -0.1625,-0.1059 -0.1310'
        ',-0.0765 -0.0933,-0.0556 -0.0744,-0.0493 -0.0514,-0.0451 -0.0094,-0.0451 0.0262,-0.0535 0.0493,-0.06'
        '39 0.0744,-0.0807 0.1038,-0.1101 0.1164,-0.1289 0.1331,-0.1688 0.1394,-0.2086 0.1373,-0.2400 0.1289,'
        '-0.2736 0.1122,-0.3071 0.0996,-0.3239 0.0681,-0.3532 0.0388,-0.3700 0.0073,-0.3805 -0.0241,-0.3847ZM'
        '-0.1394,-0.2925 0.0472,-0.1080 0.0409,-0.0996 0.0010,-0.0828 -0.0514,-0.0807 -0.0702,-0.0849 -0.1017'
        ',-0.0996 -0.1143,-0.1080 -0.1373,-0.1310 -0.1562,-0.1646 -0.1646,-0.1960 -0.1646,-0.2338 -0.1541,-0.'
        '2694ZM-0.1059,-0.3260 -0.0660,-0.3449 -0.0430,-0.3491 -0.0199,-0.3491 0.0220,-0.3386 0.0514,-0.3218 '
        '0.0765,-0.2966 0.0849,-0.2841 0.0954,-0.2610 0.1017,-0.2379 0.1038,-0.2212 0.1017,-0.1897 0.0975,-0.'
        '1730 0.0828,-0.1415 0.0765,-0.1373 -0.1080,-0.3218Z'
    ),
    '640.5/0': (
        'M-1.0252,-0.4434 -1.0314,-0.4245 -1.0314,0.4214 -1.0126,0.4623 -0.9969,0.4780 -0.9591,0.4969 0.9560,'
        '0.4969 0.9937,0.4780 1.0094,0.4623 1.0220,0.4403 1.0283,0.4214 1.0283,-0.4245 1.0126,-0.4623 0.9748,'
        '-0.4937 0.9560,-0.5000 -0.9591,-0.5000 -0.9937,-0.4843 -1.0126,-0.4654Z'
    ),
    '640.5/1': (
        'M-0.0314,-0.4214 -0.0314,0.4182 -0.0094,0.4434 0.0031,0.4497 0.9465,0.4497 0.9748,0.4277 0.9811,0.41'
        '19 0.9811,-0.4151 0.9748,-0.4308 0.9591,-0.4465 0.9465,-0.4528 0.0031,-0.4528 -0.0094,-0.4465Z'
    ),
    '640.5/2': (
        'M-0.7673,0.2862 -0.9245,0.4434 -0.9182,0.4497 -0.7610,0.2956ZM-0.7893,0.2673 -0.9591,0.4371 -0.9528,'
        '0.4465 -0.7830,0.2767ZM-0.8113,0.2484 -0.9780,0.4151 -0.9717,0.4214 -0.8050,0.2547ZM-0.8302,0.2233 -'
        '0.9843,0.3774 -0.9780,0.3899 -0.8208,0.2327ZM-0.3553,0.2358 -0.5157,0.0755 -0.6918,0.2516 -0.6792,0.'
        '2642 -0.6069,0.2925 -0.5723,0.2987 -0.4937,0.2987 -0.4151,0.2767 -0.3648,0.2484ZM-0.5346,0.0566 -0.7'
        '170,0.2358 -0.7107,0.2421 -0.5283,0.0629ZM-0.5566,0.0346 -0.7390,0.2170 -0.7327,0.2233 -0.5503,0.044'
        '0ZM-0.5786,0.0157 -0.7579,0.1950 -0.7516,0.2013 -0.5723,0.0220ZM-0.6006,-0.0063 -0.7799,0.1730 -0.77'
        '04,0.1824 -0.5912,0.0031ZM-0.2799,-0.1572 -0.4560,0.0157 -0.2956,0.1792 -0.2767,0.1572 -0.2547,0.116'
        '4 -0.2390,0.0660 -0.2327,0.0252 -0.2327,-0.0252 -0.2421,-0.0786 -0.2516,-0.1069ZM-0.7736,-0.1792 -0.'
        '7925,-0.1541 -0.8145,-0.1101 -0.8302,-0.0566 -0.8365,-0.0031 -0.8333,0.0409 -0.8113,0.1195 -0.7987,0'
        '.1447 -0.7893,0.1541 -0.6132,-0.0189ZM-0.2987,-0.1824 -0.4780,-0.0031 -0.4717,0.0031 -0.2925,-0.1730'
        'ZM-0.3145,-0.2044 -0.4969,-0.0252 -0.4906,-0.0157 -0.3082,-0.1981ZM-0.3365,-0.2264 -0.5189,-0.0440 -'
        '0.5126,-0.0377 -0.3302,-0.2201ZM-0.3616,-0.2453 -0.5409,-0.0660 -0.5314,-0.0566 -0.3522,-0.2358ZM-0.'
        '3836,-0.2610 -0.4245,-0.2799 -0.4654,-0.2925 -0.5031,-0.2987 -0.5660,-0.2987 -0.6509,-0.2767 -0.6887'
        ',-0.2579 -0.7138,-0.2390 -0.5535,-0.0786 -0.3774,-0.2547ZM-0.0849,-0.3553 -0.2264,-0.2138 -0.2264,-0'
        '.2075 -0.1950,-0.1572 -0.1698,-0.0881 -0.1635,-0.0535 -0.1604,0.0157 -0.1698,0.0881 -0.1824,0.1289 -'
        '0.2075,0.1824 -0.2547,0.2484 -0.2830,0.2767 -0.3491,0.3239 -0.4025,0.3491 -0.4811,0.3679 -0.5377,0.3'
        '711 -0.6164,0.3616 -0.6698,0.3459 -0.7453,0.3050 -0.8836,0.4434 -0.8774,0.4497 -0.1289,0.4497 -0.100'
        '6,0.4403 -0.0881,0.4277 -0.0786,0.3994 -0.0786,-0.3491ZM-0.0849,-0.3962 -0.2453,-0.2358 -0.2390,-0.2'
        '264 -0.0786,-0.3868ZM-0.0912,-0.4308 -0.2642,-0.2579 -0.2579,-0.2484 -0.0849,-0.4214ZM-0.1132,-0.449'
        '7 -0.2862,-0.2767 -0.2799,-0.2704 -0.1069,-0.4434ZM-0.1478,-0.4528 -0.1541,-0.4528 -0.3082,-0.2987 -'
        '0.3019,-0.2893 -0.1415,-0.4465ZM-0.1918,-0.4528 -0.9403,-0.4528 -0.9591,-0.4465 -0.9780,-0.4277 -0.9'
        '843,-0.4025 -0.9843,0.3396 -0.9780,0.3459 -0.8396,0.2075 -0.8679,0.1604 -0.8899,0.1038 -0.9025,0.034'
        '6 -0.9025,-0.0346 -0.8931,-0.0912 -0.8805,-0.1321 -0.8522,-0.1887 -0.8113,-0.2453 -0.7767,-0.2799 -0'
        '.7138,-0.3239 -0.6258,-0.3585 -0.5786,-0.3679 -0.4874,-0.3679 -0.4371,-0.3585 -0.3616,-0.3302 -0.323'
        '9,-0.3082 -0.1855,-0.4465Z'
    ),
    '640.5/3': (
        'M-0.7138,0.2358 -0.7673,0.2862 -0.7610,0.2956 -0.7075,0.2421ZM-0.7390,0.2138 -0.7925,0.2673 -0.7830,'
        '0.2767 -0.7296,0.2233ZM-0.7579,0.1950 -0.8113,0.2453 -0.8050,0.2547 -0.7516,0.2044ZM-0.7767,0.1730 -'
        '0.8302,0.2233 -0.8239,0.2327 -0.7704,0.1824ZM-0.4748,-0.0031 -0.5377,0.0566 -0.5314,0.0629 -0.4686,0'
        '.0031ZM-0.4969,-0.0252 -0.5597,0.0346 -0.5503,0.0440 -0.4906,-0.0157ZM-0.5189,-0.0472 -0.5786,0.0126'
        ' -0.5723,0.0220 -0.5094,-0.0377ZM-0.5377,-0.0660 -0.6006,-0.0063 -0.5943,0.0031 -0.5314,-0.0566ZM-0.'
        '2170,-0.2013 -0.2296,-0.2107 -0.2830,-0.1572 -0.2547,-0.1069 -0.2453,-0.0786 -0.2358,-0.0252 -0.2358'
        ',0.0252 -0.2421,0.0660 -0.2579,0.1164 -0.2799,0.1572 -0.2956,0.1761 -0.4560,0.0157 -0.5157,0.0755 -0'
        '.3585,0.2358 -0.3648,0.2453 -0.4151,0.2736 -0.4937,0.2956 -0.5723,0.2956 -0.6069,0.2893 -0.6447,0.27'
        '67 -0.6918,0.2516 -0.7453,0.3050 -0.7044,0.3333 -0.6509,0.3553 -0.5818,0.3711 -0.5283,0.3742 -0.5252'
        ',0.3711 -0.4811,0.3711 -0.4025,0.3522 -0.3491,0.3270 -0.2830,0.2799 -0.2516,0.2484 -0.2044,0.1824 -0'
        '.1792,0.1289 -0.1604,0.0535 -0.1572,-0.0157 -0.1667,-0.0881 -0.1792,-0.1289ZM-0.2453,-0.2358 -0.2987'
        ',-0.1824 -0.2925,-0.1761 -0.2390,-0.2264ZM-0.2642,-0.2579 -0.3176,-0.2075 -0.3113,-0.1981 -0.2579,-0'
        '.2484ZM-0.2862,-0.2799 -0.3396,-0.2264 -0.3302,-0.2170 -0.2767,-0.2704ZM-0.3082,-0.2987 -0.3616,-0.2'
        '453 -0.3553,-0.2358 -0.2987,-0.2893ZM-0.3616,-0.3333 -0.4371,-0.3616 -0.4874,-0.3711 -0.5786,-0.3711'
        ' -0.6258,-0.3616 -0.7138,-0.3270 -0.7767,-0.2830 -0.8145,-0.2453 -0.8553,-0.1887 -0.8836,-0.1321 -0.'
        '8962,-0.0912 -0.9057,-0.0346 -0.9057,0.0346 -0.8931,0.1038 -0.8616,0.1792 -0.8396,0.2075 -0.7893,0.1'
        '572 -0.8082,0.1195 -0.8302,0.0409 -0.8333,-0.0031 -0.8302,-0.0063 -0.8302,-0.0409 -0.8113,-0.1101 -0'
        '.7736,-0.1761 -0.6132,-0.0189 -0.5535,-0.0818 -0.7107,-0.2390 -0.6509,-0.2736 -0.5660,-0.2956 -0.503'
        '1,-0.2956 -0.4654,-0.2893 -0.4245,-0.2767 -0.3774,-0.2547 -0.3239,-0.3082Z'
    ),
    '647/0': (
        'M-0.6973,-0.4833 -0.7056,-0.4687 -0.7098,-0.4499 -0.7098,0.4478 -0.7015,0.4749 -0.6868,0.4896 -0.668'
        '1,0.4979 0.6660,0.4979 0.6848,0.4896 0.6994,0.4749 0.7077,0.4478 0.7077,-0.4499 0.6994,-0.4770 0.682'
        '7,-0.4937 0.6681,-0.5000 -0.6701,-0.5000 -0.6848,-0.4937Z'
    ),
    '647/1': (
        'M-0.6806,0.0073 -0.6827,0.0157 -0.6827,0.4499 -0.6785,0.4603 -0.6701,0.4687 -0.6639,0.4708 0.6618,0.'
        '4708 0.6701,0.4666 0.6785,0.4541 0.6785,0.0073 0.6681,-0.0052 0.6576,-0.0094 -0.6597,-0.0094 -0.6701'
        ',-0.0052Z'
    ),
    '647/2': (
        'M-0.6827,-0.4562 -0.6827,-0.0532 -0.6785,-0.0449 -0.6681,-0.0365 -0.6597,-0.0344 0.6576,-0.0344 0.66'
        '81,-0.0386 0.6806,-0.0532 0.6806,-0.4562 0.6660,-0.4729 0.6597,-0.4749 -0.6618,-0.4749 -0.6722,-0.47'
        '08ZM-0.5136,-0.4019 -0.4739,-0.3977 -0.4509,-0.3873 -0.4280,-0.3706 -0.4113,-0.3518 -0.3987,-0.3288 '
        '-0.3904,-0.2891 -0.3925,-0.2599 -0.3987,-0.2390 -0.4196,-0.2056 -0.4405,-0.1868 -0.4676,-0.1722 -0.5'
        '010,-0.1660 -0.5324,-0.1681 -0.5532,-0.1743 -0.5762,-0.1868 -0.5887,-0.1973 -0.6138,-0.2307 -0.6200,'
        '-0.2453 -0.6263,-0.2808 -0.6200,-0.3225 -0.6075,-0.3476 -0.5929,-0.3664 -0.5783,-0.3789 -0.5532,-0.3'
        '935Z'
    ),
    '647/3': (
        'M-0.5282,-0.4019 -0.5553,-0.3935 -0.5741,-0.3831 -0.6075,-0.3497 -0.6159,-0.3351 -0.6242,-0.3100 -0.'
        '6263,-0.2683 -0.6138,-0.2286 -0.6013,-0.2098 -0.5783,-0.1868 -0.5511,-0.1722 -0.5282,-0.1660 -0.4885'
        ',-0.1660 -0.4656,-0.1722 -0.4447,-0.1827 -0.4113,-0.2140 -0.3967,-0.2411 -0.3904,-0.2641 -0.3904,-0.'
        '3038 -0.3967,-0.3267 -0.4113,-0.3539 -0.4426,-0.3831 -0.4781,-0.3998ZM-0.5846,-0.3330 -0.5804,-0.335'
        '1 -0.4551,-0.2098 -0.4739,-0.1994 -0.5010,-0.1931 -0.5282,-0.1952 -0.5616,-0.2098 -0.5846,-0.2349 -0'
        '.5971,-0.2641 -0.5992,-0.2766 -0.5971,-0.3038ZM-0.5574,-0.3601 -0.5282,-0.3727 -0.4990,-0.3747 -0.48'
        '02,-0.3706 -0.4614,-0.3622 -0.4342,-0.3372 -0.4238,-0.3184 -0.4175,-0.2954 -0.4196,-0.2620 -0.4342,-'
        '0.2328 -0.5595,-0.3559Z'
    ),
    '647/4': (
        'M-0.5825,-0.3372 -0.5929,-0.3225 -0.5992,-0.3038 -0.6013,-0.2766 -0.5950,-0.2516 -0.5804,-0.2265 -0.'
        '5616,-0.2077 -0.5282,-0.1931 -0.5157,-0.1910 -0.4864,-0.1931 -0.4572,-0.2056 -0.4530,-0.2098ZM-0.557'
        '4,-0.3622 -0.5616,-0.3559 -0.4342,-0.2307 -0.4217,-0.2495 -0.4154,-0.2724 -0.4175,-0.3058 -0.4322,-0'
        '.3372 -0.4551,-0.3601 -0.4739,-0.3706 -0.4885,-0.3747 -0.5177,-0.3768 -0.5470,-0.3685Z'
    ),
    '667/0': (
        'M-0.4652,-0.8022 -0.4913,-0.7761 -0.5000,-0.7457 -0.5000,0.7413 -0.4913,0.7717 -0.4652,0.7978 -0.439'
        '1,0.8065 0.4391,0.8065 0.4652,0.7978 0.4913,0.7717 0.4957,0.7587 0.4957,-0.7630 0.4913,-0.7761 0.465'
        '2,-0.8022 0.4391,-0.8109 -0.4391,-0.8109Z'
    ),
    '667/1': (
        'M0.1130,0.0848 0.0957,0.0761 0.0652,0.0761 -0.0696,0.1109 -0.2304,0.1457 -0.2609,0.1717 -0.2696,0.18'
        '91 -0.2652,0.3500 -0.2913,0.3804 -0.2913,0.4152 -0.2652,0.5239 -0.2304,0.5630 -0.2130,0.6370 -0.2174'
        ',0.6413 -0.2826,0.6413 -0.2913,0.6500 -0.2913,0.6935 -0.2826,0.7022 0.2696,0.7022 0.2783,0.6935 0.27'
        '83,0.5543 0.2652,0.5413 0.2783,0.5239 0.2565,0.4413 0.2696,0.4239 0.2739,0.3978 0.2435,0.2717 0.2217'
        ',0.2500 0.1957,0.2413 0.1391,0.1109ZM0.1739,0.4761 0.1870,0.5326 0.1826,0.5457 0.0304,0.5457 0.0217,'
        '0.5543 0.0217,0.6370 0.0174,0.6413 -0.1391,0.6413 -0.1435,0.6370 -0.1261,0.6196 -0.1435,0.5457 -0.13'
        '91,0.5370 -0.0870,0.5326 0.0087,0.5065 0.1043,0.4891 0.1609,0.4674ZM0.1435,0.2109 0.1435,0.2239 0.11'
        '74,0.2413 -0.0261,0.2630 -0.1913,0.3109 -0.2217,0.3109 -0.2304,0.3022 -0.2348,0.2413 -0.2217,0.2109 '
        '-0.1783,0.1848 -0.1304,0.1717 -0.0913,0.1674 0.0217,0.1370 0.0826,0.1326 0.1043,0.1413 0.1217,0.1587'
        'ZM0.1870,-0.6978 0.1304,-0.7109 -0.2261,-0.7109 -0.2348,-0.7022 -0.2348,-0.0457 -0.2261,-0.0370 -0.0'
        '913,-0.0370 -0.0826,-0.0457 -0.0826,-0.2935 -0.0783,-0.2978 0.1522,-0.2978 0.2087,-0.3196 0.2522,-0.'
        '3674 0.2696,-0.4065 0.2739,-0.4413 0.2696,-0.5978 0.2565,-0.6326 0.2348,-0.6630ZM-0.0826,-0.5891 -0.'
        '0783,-0.5935 0.0696,-0.5935 0.0957,-0.5848 0.1174,-0.5630 0.1261,-0.5326 0.1174,-0.4457 0.0783,-0.41'
        '52 -0.0783,-0.4152 -0.0826,-0.4196Z'
    ),
    '667/2': (
        'M-0.1478,0.6413 -0.0826,0.6413 -0.1087,0.6370 -0.1261,0.6152ZM0.0217,0.6065 0.0174,0.6196 0.0000,0.6'
        '370 -0.0261,0.6413 0.0217,0.6413ZM-0.2261,0.5804 -0.2261,0.6022 -0.2348,0.6196 -0.2522,0.6370 -0.265'
        '2,0.6413 -0.2087,0.6413 -0.2174,0.6326ZM-0.1043,0.5326 -0.1435,0.5370 -0.1348,0.5848 -0.1348,0.5674 '
        '-0.1261,0.5500ZM0.1913,0.5457 0.1696,0.4674 0.1043,0.4891 -0.0261,0.5152 -0.0261,0.5196 0.0000,0.523'
        '9 0.0174,0.5413 0.0217,0.5543 0.0261,0.5457ZM-0.2304,0.2804 -0.2304,0.3022 -0.2217,0.3109 -0.1870,0.'
        '3065 -0.2130,0.3022ZM0.1348,0.1891 0.1348,0.2065 0.1261,0.2239 0.1043,0.2413 0.1174,0.2413 0.1435,0.'
        '2239ZM-0.0826,-0.2630 -0.0783,-0.2761 -0.0609,-0.2935 -0.0348,-0.2978 -0.0826,-0.2978ZM-0.0826,-0.45'
        '00 -0.0826,-0.4152 -0.0348,-0.4152 -0.0609,-0.4196 -0.0783,-0.4370ZM-0.0826,-0.5587 -0.0783,-0.5717 '
        '-0.0609,-0.5891 -0.0348,-0.5935 -0.0826,-0.5935ZM-0.2174,-0.7935 -0.2000,-0.7674 -0.2000,-0.7413 -0.'
        '2217,-0.7109 0.1304,-0.7109 0.1391,-0.7065 0.1174,-0.7239 0.1087,-0.7413 0.1087,-0.7674 0.1261,-0.79'
        '35Z'
    ),
    '667.1/0': (
        'M-0.6399,-0.4695 -0.6510,-0.4501 -0.6565,-0.4280 -0.6565,0.4224 -0.6427,0.4612 -0.6233,0.4806 -0.598'
        '3,0.4945 -0.5845,0.4972 0.5873,0.4972 0.6150,0.4861 0.6399,0.4640 0.6537,0.4391 0.6537,-0.4418 0.642'
        '7,-0.4640 0.6177,-0.4889 0.5956,-0.5000 -0.5956,-0.5000 -0.6177,-0.4889Z'
    ),
    '667.1/1': (
        'M0.1967,-0.3560 0.1828,-0.3421 0.1468,-0.2618 0.1274,-0.2507 0.1163,-0.2396 0.1108,-0.2258 0.0970,-0'
        '.1648 0.0970,-0.1454 0.1053,-0.1260 0.0942,-0.0873 0.0942,-0.0762 0.1025,-0.0651 0.0942,-0.0568 0.09'
        '42,0.0291 0.0997,0.0346 0.4488,0.0346 0.4543,0.0291 0.4543,0.0014 0.4488,-0.0042 0.4100,-0.0042 0.40'
        '72,-0.0069 0.4155,-0.0512 0.4349,-0.0706 0.4404,-0.0817 0.4571,-0.1565 0.4515,-0.1759 0.4404,-0.1870'
        ' 0.4432,-0.2867 0.4377,-0.2978 0.4211,-0.3144 0.4100,-0.3199 0.2327,-0.3615 0.2078,-0.3615ZM0.1579,-'
        '0.1039 0.1634,-0.1122 0.1717,-0.1122 0.2216,-0.0956 0.3241,-0.0734 0.3546,-0.0706 0.3601,-0.0596 0.3'
        '490,-0.0180 0.3601,-0.0069 0.3573,-0.0042 0.2576,-0.0042 0.2548,-0.0069 0.2548,-0.0568 0.2493,-0.062'
        '3 0.1496,-0.0623 0.1468,-0.0651 0.1524,-0.0706ZM0.1773,-0.2756 0.1939,-0.3116 0.2022,-0.3199 0.2133,'
        '-0.3255 0.2465,-0.3255 0.3795,-0.2950 0.3989,-0.2867 0.4183,-0.2645 0.4183,-0.2230 0.4100,-0.2119 0.'
        '3934,-0.2119 0.2936,-0.2424 0.1856,-0.2618ZM-0.1856,-0.3864 -0.2133,-0.3947 -0.4515,-0.3947 -0.4571,'
        '-0.3892 -0.4571,0.0291 -0.4515,0.0346 -0.3684,0.0346 -0.3629,0.0291 -0.3629,-0.1288 -0.3601,-0.1316 '
        '-0.2133,-0.1316 -0.1994,-0.1343 -0.1690,-0.1510 -0.1468,-0.1759 -0.1385,-0.1925 -0.1330,-0.2175 -0.1'
        '357,-0.3255 -0.1524,-0.3587ZM-0.3629,-0.3172 -0.3601,-0.3199 -0.2576,-0.3199 -0.2493,-0.3172 -0.2327'
        ',-0.3006 -0.2271,-0.2839 -0.2271,-0.2452 -0.2355,-0.2230 -0.2493,-0.2119 -0.2659,-0.2064 -0.3601,-0.'
        '2064 -0.3629,-0.2091ZM-0.6399,-0.4584 -0.6510,-0.4252 -0.6510,0.4224 -0.6371,0.4584 -0.6177,0.4778 -'
        '0.5873,0.4917 0.5873,0.4917 0.6205,0.4751 0.6399,0.4529 0.6510,0.4197 0.6510,-0.4224 0.6427,-0.4529 '
        '0.6150,-0.4834 0.5789,-0.4972 -0.5789,-0.4972 -0.6066,-0.4889ZM-0.6122,0.1620 -0.5956,0.1427 -0.5817'
        ',0.1371 0.5817,0.1371 0.5983,0.1454 0.6122,0.1648 0.6122,0.4252 0.6094,0.4335 0.5928,0.4501 0.5789,0'
        '.4557 -0.5789,0.4557 -0.5983,0.4474 -0.6122,0.4280ZM-0.6122,-0.4335 -0.5956,-0.4529 -0.5734,-0.4612 '
        '0.5734,-0.4612 0.5956,-0.4529 0.6122,-0.4307 0.6122,0.0679 0.6094,0.0762 0.5900,0.0956 0.5762,0.0983'
        ' -0.5789,0.0983 -0.5900,0.0956 -0.6122,0.0734Z'
    ),
    '667.1/2': (
        'M0.0970,0.0983 0.4515,0.0983 0.4349,0.0956 0.4183,0.0734 0.4183,0.0568 0.4349,0.0346 0.4377,0.0346 0'
        '.1108,0.0346 0.1247,0.0457 0.1302,0.0568 0.1302,0.0734 0.1136,0.0956ZM-0.4404,0.0346 -0.4266,0.0457 '
        '-0.4211,0.0568 -0.4211,0.0734 -0.4377,0.0956 -0.4543,0.0983 -0.3657,0.0983 -0.3823,0.0956 -0.3989,0.'
        '0734 -0.3989,0.0568 -0.3934,0.0457 -0.3795,0.0346ZM0.3629,-0.0042 0.3490,-0.0180 0.3518,-0.0263 0.34'
        '90,-0.0180 0.3380,-0.0069 0.3213,-0.0042ZM0.2548,-0.0263 0.2548,-0.0042 0.2853,-0.0042 0.2687,-0.006'
        '9 0.2576,-0.0180ZM0.4127,-0.0374 0.4044,-0.0042 0.4377,-0.0042 0.4294,-0.0069 0.4183,-0.0180ZM0.3435'
        ',-0.0706 0.3518,-0.0623 0.3573,-0.0485 0.3601,-0.0679ZM0.1440,-0.0623 0.2521,-0.0623 0.2548,-0.0596 '
        '0.2576,-0.0679 0.2687,-0.0789 0.2853,-0.0817 0.1994,-0.1011 0.1717,-0.1122 0.1607,-0.1122 0.1524,-0.'
        '0706ZM-0.3629,-0.1094 -0.3601,-0.1177 -0.3490,-0.1288 -0.3324,-0.1316 -0.3629,-0.1316ZM-0.3629,-0.22'
        '85 -0.3601,-0.2064 -0.3324,-0.2064 -0.3490,-0.2091 -0.3601,-0.2202ZM0.4183,-0.2396 0.4155,-0.2313 0.'
        '4044,-0.2202 0.3850,-0.2147 0.4100,-0.2119 0.4183,-0.2230ZM0.1856,-0.2950 0.1773,-0.2729 0.1856,-0.2'
        '618 0.1994,-0.2590 0.1856,-0.2784ZM-0.3629,-0.2978 -0.3601,-0.3061 -0.3490,-0.3172 -0.3324,-0.3199 -'
        '0.3629,-0.3199Z'
    ),
    '667.2/0': (
        'M-0.4694,-0.8035 -0.4913,-0.7817 -0.5000,-0.7555 -0.5000,0.7555 -0.4913,0.7773 -0.4738,0.7948 -0.438'
        '9,0.8079 -0.3734,0.8079 -0.3690,0.8035 -0.3646,0.8079 0.4345,0.8079 0.4651,0.7991 0.4956,0.7598 0.49'
        '56,-0.7642 0.4913,-0.7773 0.4694,-0.8035 0.4476,-0.8122 -0.4476,-0.8122Z'
    ),
    '667.2/1': (
        'M-0.1943,0.1354 -0.2380,0.1485 -0.2686,0.1834 -0.2729,0.2358 -0.2686,0.2620 -0.2598,0.2707 -0.1856,0'
        '.1485ZM0.1114,0.0830 0.0633,0.0742 0.0371,0.0961 0.0197,0.1266 0.0284,0.1354 0.0808,0.1310 0.1026,0.'
        '1397 0.1201,0.1572 0.1376,0.1921 0.1419,0.2227 0.1288,0.2358 -0.0459,0.2664 -0.0677,0.2795 -0.2336,0'
        '.5677 -0.2205,0.6245 -0.2118,0.6376 -0.2162,0.6419 -0.2729,0.6419 -0.2904,0.6638 -0.2904,0.6943 -0.2'
        '817,0.7031 0.2686,0.7031 0.2773,0.6943 0.2773,0.5546 0.2642,0.5415 0.2773,0.5284 0.2773,0.5153 0.259'
        '8,0.4541 0.2729,0.3930 0.2467,0.2795 0.2205,0.2489 0.1943,0.2402 0.1376,0.1092ZM0.1725,0.4716 0.1856'
        ',0.5415 0.1812,0.5459 0.0284,0.5459 0.0197,0.5546 0.0197,0.6376 0.0153,0.6419 -0.1419,0.6419 -0.1463'
        ',0.6376 -0.1288,0.6201 -0.1288,0.5983 -0.1419,0.5546 -0.1376,0.5371 -0.0895,0.5328 0.0066,0.5066 0.1'
        '026,0.4891 0.1594,0.4672ZM0.1812,-0.7031 0.1507,-0.7118 -0.2249,-0.7118 -0.2336,-0.7031 -0.2336,-0.0'
        '480 -0.2249,-0.0393 -0.0939,-0.0393 -0.0852,-0.0480 -0.0852,-0.2926 -0.0808,-0.2969 0.0677,-0.2969 0'
        '.0764,-0.3057 0.2598,-0.6245 0.2467,-0.6507 0.2074,-0.6900ZM-0.0852,-0.5895 -0.0808,-0.5939 0.0808,-'
        '0.5939 0.1026,-0.5808 0.1201,-0.5590 0.1245,-0.5415 0.1245,-0.4716 0.1157,-0.4454 0.0808,-0.4192 -0.'
        '0808,-0.4192 -0.0852,-0.4236Z'
    ),
    '667.2/2': (
        'M0.4607,-0.8122 0.3690,-0.8166 0.3515,-0.7948 -0.5044,0.6900 -0.5044,0.7467 -0.4913,0.7817 -0.4563,0'
        '.8079 -0.3734,0.8079 -0.3559,0.7904 0.5000,-0.6943 0.5000,-0.7642 0.4869,-0.7904Z'
    ),
    '667.2/3': (
        'M-0.2642,0.7031 -0.2424,0.7205 -0.2336,0.7380 -0.2336,0.7642 -0.2511,0.7904 0.2380,0.7904 0.2205,0.7'
        '642 0.2205,0.7380 0.2293,0.7205 0.2511,0.7031ZM0.0197,0.6070 0.0153,0.6201 -0.0022,0.6376 -0.0284,0.'
        '6419 0.0197,0.6419ZM-0.1507,0.6419 -0.0808,0.6419 -0.1070,0.6376 -0.1245,0.6201 -0.1288,0.6070 -0.13'
        '32,0.6288ZM-0.2249,0.5895 -0.2249,0.6070 -0.2336,0.6245 -0.2555,0.6419 -0.2074,0.6419 -0.2162,0.6376'
        'ZM-0.1070,0.5328 -0.1419,0.5371 -0.1376,0.5764 -0.1288,0.5502ZM0.1900,0.5459 0.1681,0.4672 0.1026,0.'
        '4891 -0.0284,0.5153 -0.0284,0.5197 -0.0022,0.5240 0.0153,0.5415 0.0197,0.5546 0.0240,0.5459ZM0.1332,'
        '0.1834 0.1332,0.2052 0.1245,0.2227 0.1026,0.2402 0.1376,0.2314 0.1419,0.2052ZM-0.0852,-0.2620 -0.080'
        '8,-0.2751 -0.0633,-0.2926 -0.0371,-0.2969 -0.0852,-0.2969ZM-0.0852,-0.4541 -0.0852,-0.4192 -0.0371,-'
        '0.4192 -0.0633,-0.4236 -0.0808,-0.4410ZM-0.0852,-0.5590 -0.0808,-0.5721 -0.0633,-0.5895 -0.0371,-0.5'
        '939 -0.0852,-0.5939Z'
    ),
    '668/0': (
        'M-0.4737,-0.8048 -0.5000,-0.7697 -0.5000,0.7610 -0.4956,0.7741 -0.4693,0.8004 -0.4430,0.8092 0.4386,'
        '0.8092 0.4649,0.8004 0.4956,0.7610 0.4956,-0.7697 0.4868,-0.7873 0.4518,-0.8136 -0.4561,-0.8136Z'
    ),
    '668/1': (
        'M-0.4079,0.6513 -0.4079,0.6952 -0.3991,0.7039 0.3860,0.7039 0.3947,0.6952 0.3947,0.5592 0.3860,0.550'
        '4 0.3596,0.5461 0.3684,0.5373 0.3684,0.4496 0.3860,0.4320 0.3947,0.4101 0.3947,0.2873 0.3860,0.2654 '
        '0.3596,0.2478 0.3509,0.2346 0.3289,0.1031 0.3202,0.0855 0.2939,0.0592 0.2675,0.0504 -0.0351,0.0504 -'
        '0.0746,0.0680 -0.0877,0.0811 -0.0965,0.1031 -0.1228,0.2434 -0.1535,0.2654 -0.1623,0.2873 -0.1623,0.4'
        '145 -0.1535,0.4364 -0.1404,0.4496 -0.1404,0.5329 -0.1272,0.5461 -0.1491,0.5504 -0.1579,0.5592 -0.157'
        '9,0.6382 -0.1623,0.6425 -0.3991,0.6425ZM-0.0570,0.5461 -0.0439,0.5329 -0.0439,0.4627 -0.0395,0.4583 '
        '0.0088,0.4583 0.0132,0.4627 0.2719,0.4583 0.2763,0.4627 0.2763,0.5329 0.2895,0.5461 0.2851,0.5504 -0'
        '.0526,0.5504ZM-0.0746,0.1732 -0.0614,0.1294 -0.0482,0.1162 -0.0088,0.1031 0.2412,0.1031 0.2719,0.111'
        '8 0.2982,0.1382 0.3070,0.1776 0.3070,0.2127 0.2895,0.2215 0.1535,0.2171 0.1491,0.2127 -0.0570,0.2215'
        ' -0.0746,0.2127ZM0.1842,-0.7039 0.1579,-0.7127 -0.2281,-0.7127 -0.2368,-0.7039 -0.2368,-0.0504 -0.22'
        '81,-0.0417 -0.0965,-0.0417 -0.0877,-0.0504 -0.0877,-0.2961 -0.0833,-0.3004 0.1491,-0.3004 0.2061,-0.'
        '3224 0.2500,-0.3662 0.2719,-0.4320 0.2719,-0.5943 0.2588,-0.6338 0.2412,-0.6601 0.2193,-0.6820ZM-0.0'
        '877,-0.5943 -0.0833,-0.5987 0.0614,-0.5987 0.0833,-0.5943 0.1053,-0.5811 0.1228,-0.5504 0.1228,-0.46'
        '27 0.1096,-0.4408 0.0877,-0.4232 0.0702,-0.4189 -0.0833,-0.4189 -0.0877,-0.4232Z'
    ),
    '668/2': (
        'M-0.3816,0.7039 -0.3596,0.7215 -0.3509,0.7390 -0.3509,0.7654 -0.3684,0.7917 0.3553,0.7917 0.3377,0.7'
        '654 0.3377,0.7390 0.3465,0.7215 0.3684,0.7039ZM-0.1579,0.6075 -0.1623,0.6206 -0.1798,0.6382 -0.2061,'
        '0.6425 -0.1579,0.6425ZM-0.1491,0.5504 -0.1184,0.5504 -0.1404,0.5329ZM0.3860,0.5504 0.3684,0.5241 0.3'
        '684,0.5373 0.3509,0.5504ZM-0.0658,0.5504 0.2982,0.5504 0.2763,0.5329 0.2763,0.4539 0.2193,0.4627 0.0'
        '132,0.4627 -0.0439,0.4539 -0.0439,0.5329ZM0.3070,0.1776 0.2982,0.1996 0.2807,0.2171 0.2544,0.2215 0.'
        '3026,0.2171ZM-0.0746,0.1732 -0.0702,0.2171 -0.0219,0.2215 -0.0482,0.2171 -0.0658,0.1996ZM-0.0877,-0.'
        '2654 -0.0833,-0.2785 -0.0658,-0.2961 -0.0395,-0.3004 -0.0877,-0.3004ZM-0.0877,-0.4539 -0.0877,-0.418'
        '9 -0.0395,-0.4189 -0.0658,-0.4232 -0.0833,-0.4408ZM-0.0877,-0.5636 -0.0833,-0.5768 -0.0658,-0.5943 -'
        '0.0395,-0.5987 -0.0877,-0.5987Z'
    ),
    '668.1/0': (
        'M-0.6399,-0.4668 -0.6510,-0.4474 -0.6565,-0.4252 -0.6565,0.4252 -0.6454,0.4584 -0.6260,0.4806 -0.595'
        '6,0.4972 0.5956,0.4972 0.6260,0.4806 0.6427,0.4612 0.6537,0.4391 0.6537,-0.4418 0.6454,-0.4584 0.623'
        '3,-0.4834 0.5873,-0.5000 -0.5845,-0.5000 -0.6150,-0.4889Z'
    ),
    '668.1/1': (
        'M-0.4681,0.2091 -0.4903,0.2175 -0.5125,0.2479 -0.5180,0.2673 -0.5180,0.3172 -0.5097,0.3393 -0.4903,0'
        '.3615 -0.4598,0.3698 -0.4432,0.3670 -0.4155,0.3476 -0.4072,0.3310 -0.4072,0.2950 -0.4127,0.2839 -0.4'
        '321,0.2645 -0.4598,0.2590 -0.4820,0.2673 -0.4848,0.2562 -0.4737,0.2424 -0.4654,0.2396 -0.4488,0.2396'
        ' -0.4321,0.2535 -0.4183,0.2507 -0.4072,0.2424 -0.4238,0.2202 -0.4404,0.2119ZM-0.4654,0.2867 -0.4488,'
        '0.2895 -0.4377,0.3033 -0.4377,0.3227 -0.4543,0.3393 -0.4737,0.3366 -0.4848,0.3227 -0.4848,0.3006 -0.'
        '4737,0.2895ZM0.0886,-0.3643 0.0776,-0.3393 0.0637,-0.2590 0.0471,-0.2479 0.0388,-0.2313 0.0388,-0.14'
        '82 0.0526,-0.1260 0.0526,-0.0734 0.0609,-0.0651 0.0443,-0.0623 0.0388,-0.0568 0.0388,0.0319 0.0443,0'
        '.0374 0.5429,0.0374 0.5485,0.0319 0.5485,0.0014 0.5429,-0.0042 0.3906,-0.0042 0.3878,-0.0069 0.3878,'
        '-0.0568 0.3712,-0.0651 0.3767,-0.0706 0.3767,-0.1260 0.3906,-0.1399 0.3934,-0.1510 0.3934,-0.2285 0.'
        '3878,-0.2424 0.3657,-0.2645 0.3518,-0.3421 0.3435,-0.3615 0.3324,-0.3726 0.3102,-0.3809 0.1219,-0.38'
        '09 0.1080,-0.3781ZM0.1108,-0.1205 0.1136,-0.1233 0.1274,-0.1205 0.3047,-0.1205 0.3158,-0.1233 0.3186'
        ',-0.1205 0.3186,-0.0706 0.3241,-0.0651 0.3213,-0.0623 0.1080,-0.0623 0.1053,-0.0651 0.1108,-0.0706ZM'
        '0.0942,-0.3033 0.1025,-0.3283 0.1247,-0.3449 0.1385,-0.3476 0.2909,-0.3476 0.3130,-0.3421 0.3296,-0.'
        '3283 0.3352,-0.3144 0.3380,-0.2784 0.3296,-0.2729 0.2742,-0.2729 0.2715,-0.2756 0.1025,-0.2729 0.094'
        '2,-0.2784ZM-0.1828,-0.3837 -0.2216,-0.3947 -0.4515,-0.3947 -0.4571,-0.3892 -0.4571,0.0319 -0.4515,0.'
        '0374 -0.3684,0.0374 -0.3629,0.0319 -0.3629,-0.1260 -0.3601,-0.1288 -0.2050,-0.1316 -0.1773,-0.1427 -'
        '0.1468,-0.1731 -0.1330,-0.2147 -0.1357,-0.3255 -0.1468,-0.3504 -0.1579,-0.3643ZM-0.3629,-0.3172 -0.3'
        '601,-0.3199 -0.2659,-0.3199 -0.2438,-0.3116 -0.2299,-0.2950 -0.2271,-0.2812 -0.2271,-0.2424 -0.2327,'
        '-0.2258 -0.2465,-0.2119 -0.2604,-0.2064 -0.3601,-0.2064 -0.3629,-0.2091ZM-0.6343,-0.4640 -0.6454,-0.'
        '4446 -0.6510,-0.4252 -0.6510,0.4224 -0.6399,0.4557 -0.6233,0.4751 -0.6066,0.4861 -0.5789,0.4945 0.57'
        '89,0.4945 0.6066,0.4861 0.6371,0.4584 0.6482,0.4363 0.6510,0.4197 0.6510,-0.4224 0.6399,-0.4557 0.61'
        '22,-0.4834 0.5873,-0.4945 -0.5873,-0.4945 -0.6122,-0.4834ZM-0.6122,0.1648 -0.6039,0.1510 -0.5900,0.1'
        '399 0.5873,0.1399 0.6066,0.1565 0.6122,0.1676 0.6122,0.4280 0.5956,0.4501 0.5734,0.4584 -0.5734,0.45'
        '84 -0.5956,0.4501 -0.6122,0.4307ZM-0.6122,-0.4307 -0.6011,-0.4474 -0.5789,-0.4584 0.5789,-0.4584 0.5'
        '873,-0.4557 0.6066,-0.4391 0.6122,-0.4280 0.6122,0.0706 0.6066,0.0817 0.5873,0.0983 -0.5873,0.0983 -'
        '0.6011,0.0900 -0.6122,0.0734Z'
    ),
    '668.1/2': (
        'M-0.4654,0.2867 -0.4737,0.2895 -0.4848,0.3006 -0.4848,0.3227 -0.4737,0.3366 -0.4543,0.3393 -0.4377,0'
        '.3227 -0.4377,0.3033 -0.4488,0.2895ZM-0.4875,0.2673 -0.4515,0.2590 -0.4321,0.2645 -0.4183,0.2784 -0.'
        '4183,0.2590 -0.4127,0.2479 -0.4349,0.2535 -0.4488,0.2396 -0.4654,0.2396 -0.4792,0.2479ZM0.0277,0.098'
        '3 0.5596,0.0983 0.5429,0.0956 0.5263,0.0734 0.5263,0.0568 0.5402,0.0374 0.0471,0.0374 0.0609,0.0568 '
        '0.0609,0.0734 0.0443,0.0956ZM-0.4681,0.0983 -0.3518,0.0983 -0.3684,0.0956 -0.3850,0.0734 -0.3850,0.0'
        '568 -0.3712,0.0374 -0.4488,0.0374 -0.4349,0.0568 -0.4349,0.0734 -0.4515,0.0956ZM0.5485,0.0042 0.5485'
        ',0.0291 0.5568,0.0180ZM0.6122,-0.0014 0.6011,0.0152 0.6122,0.0346ZM0.3878,-0.0263 0.3878,-0.0042 0.4'
        '183,-0.0042 0.4017,-0.0069 0.3906,-0.0180ZM0.3823,-0.0623 0.3767,-0.0734 0.3657,-0.0623ZM0.0443,-0.0'
        '623 0.0637,-0.0623 0.0526,-0.0762ZM0.0997,-0.0623 0.3296,-0.0623 0.3186,-0.0706 0.3186,-0.1233 0.304'
        '7,-0.1205 0.1274,-0.1205 0.1108,-0.1233 0.1108,-0.0706ZM-0.3629,-0.1066 -0.3601,-0.1150 -0.3490,-0.1'
        '260 -0.3324,-0.1288 -0.3629,-0.1288ZM-0.3629,-0.2285 -0.3629,-0.2064 -0.3324,-0.2064 -0.3490,-0.2091'
        ' -0.3601,-0.2202ZM0.3380,-0.2978 0.3213,-0.2756 0.3047,-0.2729 0.3352,-0.2756ZM0.0942,-0.3033 0.0970'
        ',-0.2756 0.1274,-0.2729 0.1108,-0.2756 0.0997,-0.2867ZM-0.3629,-0.2978 -0.3601,-0.3061 -0.3490,-0.31'
        '72 -0.3324,-0.3199 -0.3601,-0.3199ZM-0.4543,-0.4584 -0.4377,-0.4557 -0.4211,-0.4335 -0.4211,-0.4169 '
        '-0.4377,-0.3947 -0.4404,-0.3947 -0.2355,-0.3947 -0.2493,-0.4058 -0.2548,-0.4169 -0.2548,-0.4335 -0.2'
        '382,-0.4557 -0.2216,-0.4584Z'
    ),
    '668.2/0': (
        'M-0.4738,-0.8013 -0.5000,-0.7664 -0.5000,0.7620 -0.4913,0.7795 -0.4563,0.8057 0.4476,0.8057 0.4651,0'
        '.7969 0.4869,0.7751 0.4956,0.7489 0.4956,-0.7533 0.4869,-0.7795 0.4476,-0.8100 -0.4520,-0.8100Z'
    ),
    '668.2/1': (
        'M0.3035,0.0677 0.2729,0.0546 0.0633,0.0546 0.0371,0.0939 0.0459,0.1070 0.2511,0.1070 0.2817,0.1201 0'
        '.2948,0.1332 0.3035,0.1550 0.3079,0.2162 0.2904,0.2249 0.1725,0.2205 0.1681,0.2162 -0.0284,0.2205 -0'
        '.0459,0.2380 -0.1550,0.4301 -0.1376,0.4476 -0.1376,0.5349 -0.1245,0.5480 -0.1463,0.5524 -0.1550,0.56'
        '11 -0.1550,0.6397 -0.1594,0.6441 -0.2729,0.6441 -0.3079,0.6921 -0.2991,0.7052 0.3865,0.7052 0.3952,0'
        '.6965 0.3952,0.5611 0.3865,0.5524 0.3603,0.5480 0.3734,0.5349 0.3734,0.4520 0.3952,0.4170 0.3952,0.2'
        '904 0.3865,0.2686 0.3559,0.2467 0.3297,0.1070 0.3210,0.0852ZM-0.0546,0.5480 -0.0415,0.5349 -0.0415,0'
        '.4607 -0.0371,0.4563 0.0197,0.4651 0.2162,0.4651 0.2729,0.4563 0.2773,0.4607 0.2773,0.5349 0.2904,0.'
        '5480 0.2860,0.5524 -0.0502,0.5524ZM0.1900,-0.6965 0.1507,-0.7096 -0.2293,-0.7096 -0.2380,-0.7009 -0.'
        '2380,-0.0459 -0.2293,-0.0371 -0.0983,-0.0371 -0.0895,-0.0459 -0.0895,-0.2948 -0.0852,-0.2991 0.0677,'
        '-0.2991 0.0764,-0.3079 0.2555,-0.6179 0.2555,-0.6310 0.2424,-0.6528ZM-0.0895,-0.5873 -0.0852,-0.5917'
        ' 0.0808,-0.5917 0.0983,-0.5830 0.1114,-0.5699 0.1245,-0.5306 0.1201,-0.5262 0.1201,-0.4607 0.1114,-0'
        '.4432 0.0764,-0.4170 -0.0852,-0.4170 -0.0895,-0.4214Z'
    ),
    '668.2/2': (
        'M0.4651,-0.8057 0.4432,-0.8144 0.3690,-0.8144 0.3472,-0.7882 -0.5000,0.6790 -0.5044,0.7620 -0.4738,0'
        '.8013 -0.4520,0.8100 -0.3734,0.8100 -0.3559,0.7882 0.4956,-0.6878 0.4956,-0.7707Z'
    ),
    '668.2/3': (
        'M-0.1550,0.6092 -0.1594,0.6223 -0.1769,0.6397 -0.2031,0.6441 -0.1550,0.6441ZM0.3952,0.5655 0.3952,0.'
        '6921 0.4083,0.6790 0.4389,0.6703 0.4607,0.6747 0.4782,0.6878 0.4782,0.5699 0.4607,0.5830 0.4389,0.58'
        '73 0.4170,0.5830ZM-0.1463,0.5524 -0.1157,0.5524 -0.1376,0.5349ZM0.3865,0.5524 0.3734,0.5306 0.3515,0'
        '.5524ZM-0.0633,0.5524 0.2991,0.5524 0.2773,0.5349 0.2773,0.4563 0.2162,0.4651 0.0197,0.4651 -0.0415,'
        '0.4563 -0.0415,0.5393ZM0.3952,0.2948 0.3952,0.4127 0.4083,0.3996 0.4389,0.3908 0.4607,0.3952 0.4782,'
        '0.4083 0.4782,0.2991 0.4607,0.3122 0.4389,0.3166 0.4170,0.3122ZM0.3079,0.1769 0.2991,0.1987 0.2817,0'
        '.2162 0.2555,0.2205 0.2686,0.2249 0.3035,0.2205ZM-0.0895,-0.2642 -0.0852,-0.2773 -0.0677,-0.2948 -0.'
        '0415,-0.2991 -0.0852,-0.2991ZM-0.0895,-0.4520 -0.0895,-0.4170 -0.0415,-0.4170 -0.0677,-0.4214 -0.085'
        '2,-0.4389ZM-0.0895,-0.5568 -0.0852,-0.5699 -0.0677,-0.5873 -0.0415,-0.5917 -0.0895,-0.5917Z'
    ),
    '618.3B/0': (
        'M-0.4633,-1.4226 -0.4796,-1.4145 -0.4898,-1.4043 -0.5000,-1.3758 -0.5000,1.3758 -0.4980,1.3880 -0.49'
        '19,1.4022 -0.4776,1.4165 -0.4654,1.4226 0.4654,1.4226 0.4776,1.4165 0.4898,1.4043 0.4959,1.3921 0.49'
        '80,1.3758 0.4980,-1.3758 0.4959,-1.3900 0.4898,-1.4022 0.4756,-1.4165 0.4633,-1.4226 0.4511,-1.4246 '
        '-0.4532,-1.4246Z'
    ),
    '618.3B/1': (
        'M0.1436,0.9420 0.1334,0.9501 0.1314,0.9664 0.1395,0.9766 0.1538,0.9786 0.1680,0.9664 0.1680,0.9542 0'
        '.1599,0.9440ZM-0.1721,0.9420 -0.1843,0.9521 -0.1864,0.9623 -0.1843,0.9684 -0.1762,0.9766 -0.1619,0.9'
        '786 -0.1497,0.9684 -0.1477,0.9562 -0.1599,0.9420ZM-0.1965,0.8116 -0.2047,0.8238 -0.2088,0.8544 -0.20'
        '47,0.8585 -0.1558,0.8585 -0.1517,0.8544 -0.1517,0.8157 -0.1558,0.8116ZM-0.4715,0.1986 -0.4756,0.2067'
        ' -0.4756,1.0214 -0.4633,1.0377 -0.4532,1.0418 0.4511,1.0418 0.4613,1.0377 0.4735,1.0234 0.4735,0.204'
        '7 0.4613,0.1904 0.4511,0.1864 -0.4532,0.1864 -0.4633,0.1904ZM-0.2413,0.8829 -0.2291,0.8727 -0.2210,0'
        '.8136 -0.2128,0.7994 -0.2026,0.7933 -0.1212,0.7933 -0.1151,0.7994 -0.1151,0.8544 -0.1110,0.8585 -0.0'
        '988,0.8585 -0.0947,0.8544 -0.0947,0.7627 -0.0886,0.7587 0.2352,0.7587 0.2413,0.7668 0.2413,0.9582 0.'
        '2393,0.9603 0.1945,0.9603 0.1904,0.9644 0.1864,0.9807 0.1721,0.9949 0.1578,1.0010 0.1415,1.0010 0.12'
        '73,0.9949 0.1151,0.9827 0.1090,0.9644 0.1049,0.9603 -0.1212,0.9603 -0.1334,0.9847 -0.1477,0.9969 -0.'
        '1578,1.0010 -0.1823,0.9990 -0.1986,0.9868 -0.2047,0.9766 -0.2067,0.9644 -0.2108,0.9603 -0.2291,0.958'
        '2 -0.2413,0.8992ZM0.1945,0.3269 0.1965,0.3289 0.1965,0.3513 0.2026,0.3635 0.2699,0.3635 0.2800,0.388'
        '0 0.2780,0.3900 0.2719,0.3859 0.2576,0.4124 0.2475,0.4206 0.2332,0.4267 0.2128,0.4267 0.1965,0.4206 '
        '0.1802,0.4043 0.1741,0.3880 0.1741,0.3697 0.1823,0.3513 0.1925,0.3391ZM0.1273,0.2332 0.1314,0.2312 0'
        '.2047,0.2312 0.2067,0.2332 0.1986,0.2373 0.1904,0.2495 0.1945,0.3228 0.1925,0.3248 0.1843,0.3187 0.1'
        '640,0.3391 0.1538,0.3615 0.1517,0.3859 0.1558,0.4022 0.1721,0.4287 0.1884,0.4409 0.2128,0.4491 0.233'
        '2,0.4491 0.2556,0.4409 0.2821,0.4165 0.2862,0.4022 0.3004,0.4287 0.3330,0.4165 0.3391,0.4104 0.3310,'
        '0.3961 0.3167,0.4022 0.3086,0.3982 0.2902,0.3513 0.2821,0.3411 0.2210,0.3411 0.2189,0.3391 0.2210,0.'
        '3310 0.2658,0.3310 0.2699,0.3269 0.2699,0.3147 0.2658,0.3106 0.2189,0.3106 0.2169,0.3086 0.2149,0.28'
        '00 0.2271,0.2739 0.2352,0.2617 0.2352,0.2475 0.2271,0.2373 0.2169,0.2332 0.2189,0.2312 0.3350,0.2312'
        ' 0.3432,0.2373 0.3473,0.2475 0.3473,0.4409 0.3411,0.4532 0.3371,0.4552 0.1293,0.4552 0.1212,0.4470 0'
        '.1191,0.4409 0.1191,0.2475ZM-0.0234,-0.9114 -0.0784,-0.9012 -0.1090,-0.8890 -0.1477,-0.8666 -0.1945,'
        '-0.8259 -0.2291,-0.7770 -0.2454,-0.7403 -0.2576,-0.6894 -0.2597,-0.6324 -0.2495,-0.5774 -0.2291,-0.5'
        '305 -0.2006,-0.4878 -0.1701,-0.4572 -0.1232,-0.4246 -0.0906,-0.4104 -0.0601,-0.4002 -0.0356,-0.3961 '
        '0.0132,-0.3941 0.0479,-0.3982 0.0988,-0.4145 0.1436,-0.4389 0.1925,-0.4817 0.2128,-0.5081 0.2413,-0.'
        '5631 0.2536,-0.6059 0.2576,-0.6670 0.2495,-0.7179 0.2352,-0.7587 0.2149,-0.7953 0.1986,-0.8177 0.166'
        '0,-0.8503 0.1191,-0.8829 0.0866,-0.8971 0.0580,-0.9053 0.0193,-0.9114ZM-0.4633,-1.3982 -0.4756,-1.38'
        '19 -0.4756,0.1497 -0.4654,0.1619 -0.4491,0.1680 0.4470,0.1680 0.4633,0.1619 0.4735,0.1477 0.4735,-1.'
        '3819 0.4695,-1.3900 0.4572,-1.4002 -0.4593,-1.4002ZM0.1151,0.0193 0.1171,0.0173 0.1395,0.0173 0.1415'
        ',0.0193 0.1395,0.0214 0.1171,0.0214ZM-0.0255,-0.9745 0.0255,-0.9745 0.0967,-0.9603 0.1334,-0.9460 0.'
        '1680,-0.9277 0.2047,-0.9012 0.2536,-0.8503 0.2882,-0.7953 0.3065,-0.7485 0.3208,-0.6711 0.3187,-0.62'
        '02 0.3147,-0.5916 0.3045,-0.5530 0.2780,-0.4939 0.2597,-0.4654 0.2332,-0.4328 0.2026,-0.4043 0.1782,'
        '-0.3859 0.1273,-0.3574 0.0947,-0.3452 0.0540,-0.3350 0.0356,-0.3350 0.0153,-0.3310 -0.0499,-0.3350 -'
        '0.1029,-0.3473 -0.1293,-0.3574 -0.1680,-0.3778 -0.2006,-0.4002 -0.2189,-0.4165 -0.2576,-0.4593 -0.27'
        '60,-0.4857 -0.2943,-0.5204 -0.3106,-0.5652 -0.3187,-0.5998 -0.3228,-0.6344 -0.3228,-0.6731 -0.3187,-'
        '0.7098 -0.3004,-0.7729 -0.2841,-0.8075 -0.2658,-0.8381 -0.2434,-0.8666 -0.2189,-0.8910 -0.1884,-0.91'
        '55 -0.1640,-0.9318 -0.1314,-0.9481 -0.0927,-0.9623Z'
    ),
    '618.3B/2': (
        'M-0.4776,1.0845 -0.4776,1.3778 -0.4715,1.3921 -0.4593,1.4022 -0.4511,1.4043 0.4491,1.4043 0.4593,1.4'
        '022 0.4715,1.3900 0.4756,1.3819 0.4756,1.0825 0.4715,1.0743 0.4593,1.0621 0.4532,1.0601 -0.4532,1.06'
        '01 -0.4654,1.0662ZM-0.2536,1.1049 -0.2189,1.1090 -0.1945,1.1171 -0.1640,1.1375 -0.1415,1.1619 -0.131'
        '4,1.1802 -0.1232,1.2026 -0.1191,1.2271 -0.1212,1.2536 -0.1293,1.2841 -0.1395,1.3045 -0.1517,1.3208 -'
        '0.1721,1.3391 -0.1884,1.3493 -0.2067,1.3574 -0.2312,1.3635 -0.2800,1.3615 -0.3024,1.3534 -0.3248,1.3'
        '411 -0.3554,1.3106 -0.3758,1.2678 -0.3778,1.2536 -0.3778,1.2169 -0.3737,1.1986 -0.3595,1.1660 -0.347'
        '3,1.1497 -0.3248,1.1293 -0.3086,1.1191 -0.2862,1.1110Z'
    ),
    '618.3B/3': (
        'M-0.2617,1.1049 -0.2841,1.1090 -0.3065,1.1171 -0.3269,1.1293 -0.3534,1.1558 -0.3737,1.1945 -0.3778,1'
        '.2088 -0.3798,1.2454 -0.3758,1.2699 -0.3635,1.2984 -0.3534,1.3147 -0.3289,1.3391 -0.3004,1.3554 -0.2'
        '760,1.3635 -0.2373,1.3656 -0.2149,1.3615 -0.1864,1.3493 -0.1680,1.3371 -0.1395,1.3065 -0.1273,1.2821'
        ' -0.1212,1.2617 -0.1191,1.2210 -0.1293,1.1823 -0.1395,1.1640 -0.1538,1.1456 -0.1721,1.1293 -0.1965,1'
        '.1151 -0.2149,1.1090 -0.2393,1.1049ZM-0.3350,1.1762 -0.3310,1.1741 -0.1884,1.3187 -0.2108,1.3310 -0.'
        '2495,1.3391 -0.2841,1.3330 -0.3065,1.3228 -0.3187,1.3126 -0.3371,1.2902 -0.3513,1.2536 -0.3534,1.235'
        '2 -0.3513,1.2128ZM-0.3086,1.1497 -0.2841,1.1375 -0.2475,1.1314 -0.2149,1.1375 -0.1945,1.1477 -0.1782'
        ',1.1599 -0.1619,1.1802 -0.1517,1.2006 -0.1456,1.2332 -0.1477,1.2536 -0.1538,1.2739 -0.1680,1.2984 -0'
        '.3126,1.1538ZM-0.0255,-0.9766 -0.0764,-0.9684 -0.1314,-0.9501 -0.1640,-0.9338 -0.1884,-0.9175 -0.218'
        '9,-0.8931 -0.2454,-0.8666 -0.2678,-0.8381 -0.2862,-0.8075 -0.3024,-0.7729 -0.3208,-0.7098 -0.3248,-0'
        '.6731 -0.3248,-0.6344 -0.3147,-0.5733 -0.2963,-0.5204 -0.2780,-0.4857 -0.2597,-0.4593 -0.2189,-0.414'
        '5 -0.2006,-0.3982 -0.1680,-0.3758 -0.1293,-0.3554 -0.1029,-0.3452 -0.0499,-0.3330 0.0153,-0.3289 0.0'
        '356,-0.3330 0.0540,-0.3330 0.0947,-0.3432 0.1273,-0.3554 0.1660,-0.3758 0.1925,-0.3941 0.2352,-0.432'
        '8 0.2617,-0.4654 0.2800,-0.4939 0.3065,-0.5530 0.3167,-0.5916 0.3208,-0.6202 0.3228,-0.6711 0.3086,-'
        '0.7485 0.2902,-0.7953 0.2556,-0.8503 0.2047,-0.9033 0.1680,-0.9297 0.1334,-0.9481 0.0967,-0.9623 0.0'
        '255,-0.9766ZM-0.0234,-0.9094 0.0193,-0.9094 0.0580,-0.9033 0.0866,-0.8951 0.1191,-0.8809 0.1660,-0.8'
        '483 0.1965,-0.8177 0.2128,-0.7953 0.2332,-0.7587 0.2475,-0.7179 0.2556,-0.6670 0.2515,-0.6059 0.2393'
        ',-0.5631 0.2230,-0.5285 0.1904,-0.4817 0.1436,-0.4409 0.0988,-0.4165 0.0479,-0.4002 0.0132,-0.3961 -'
        '0.0356,-0.3982 -0.0601,-0.4022 -0.0906,-0.4124 -0.1232,-0.4267 -0.1701,-0.4593 -0.1986,-0.4878 -0.22'
        '71,-0.5305 -0.2475,-0.5774 -0.2576,-0.6324 -0.2556,-0.6894 -0.2434,-0.7403 -0.2271,-0.7770 -0.1925,-'
        '0.8259 -0.1477,-0.8646 -0.1090,-0.8870 -0.0784,-0.8992Z'
    ),
    '618.3B/4': (
        'M-0.3330,1.1721 -0.3493,1.2006 -0.3534,1.2128 -0.3554,1.2352 -0.3473,1.2739 -0.3289,1.3045 -0.3065,1'
        '.3248 -0.2678,1.3391 -0.2495,1.3411 -0.2312,1.3391 -0.2108,1.3330 -0.1904,1.3228 -0.1864,1.3167ZM-0.'
        '3086,1.1477 -0.3147,1.1538 -0.1680,1.3004 -0.1619,1.2943 -0.1517,1.2739 -0.1456,1.2536 -0.1436,1.233'
        '2 -0.1497,1.2006 -0.1599,1.1802 -0.1762,1.1599 -0.1945,1.1456 -0.2149,1.1354 -0.2475,1.1293 -0.2841,'
        '1.1354ZM0.1212,0.2373 0.1171,0.2475 0.1171,0.4409 0.1191,0.4470 0.1293,0.4572 0.3371,0.4572 0.3411,0'
        '.4552 0.3493,0.4409 0.3493,0.2475 0.3452,0.2373 0.3350,0.2291 0.2189,0.2291 0.2149,0.2332 0.2271,0.2'
        '393 0.2332,0.2475 0.2312,0.2678 0.2128,0.2800 0.2149,0.3086 0.2189,0.3126 0.2658,0.3126 0.2678,0.314'
        '7 0.2658,0.3289 0.2210,0.3289 0.2169,0.3330 0.2169,0.3391 0.2210,0.3432 0.2821,0.3432 0.2862,0.3473 '
        '0.3065,0.3982 0.3126,0.4043 0.3310,0.3982 0.3371,0.4084 0.3330,0.4145 0.3004,0.4267 0.2739,0.3656 0.'
        '2699,0.3615 0.2026,0.3615 0.2006,0.3595 0.1986,0.3289 0.1945,0.3248 0.1965,0.3045 0.1925,0.2780 0.19'
        '25,0.2495 0.1965,0.2413 0.2088,0.2332 0.2047,0.2291 0.1314,0.2291ZM0.1843,0.3208 0.1925,0.3269 0.190'
        '4,0.3391 0.1802,0.3513 0.1721,0.3697 0.1721,0.3880 0.1782,0.4043 0.2006,0.4246 0.2128,0.4287 0.2332,'
        '0.4287 0.2556,0.4165 0.2678,0.4002 0.2699,0.3900 0.2739,0.3880 0.2800,0.3982 0.2821,0.4124 0.2556,0.'
        '4389 0.2332,0.4470 0.2047,0.4450 0.1782,0.4328 0.1640,0.4145 0.1538,0.3859 0.1558,0.3615 0.1660,0.33'
        '91Z'
    ),
    '618.3B/5': (
        'M0.1090,0.9644 0.1191,0.9868 0.1375,0.9990 0.1599,0.9990 0.1701,0.9949 0.1823,0.9847 0.1884,0.9725 0'
        '.1884,0.9644 0.1762,0.9623 0.1701,0.9582 0.1680,0.9684 0.1517,0.9807 0.1375,0.9766 0.1314,0.9684 0.1'
        '293,0.9582 0.1232,0.9623ZM-0.2067,0.9644 -0.1986,0.9847 -0.1802,0.9990 -0.1558,0.9990 -0.1395,0.9908'
        ' -0.1273,0.9705 -0.1273,0.9644 -0.1395,0.9623 -0.1477,0.9562 -0.1456,0.9623 -0.1497,0.9705 -0.1558,0'
        '.9766 -0.1680,0.9807 -0.1782,0.9766 -0.1843,0.9705 -0.1864,0.9562 -0.1945,0.9623ZM0.2393,0.9481 0.23'
        '12,0.9582 0.2189,0.9603 0.2393,0.9603ZM-0.2291,0.8686 -0.2210,0.8605 -0.2108,0.8585 -0.2026,0.8136 -'
        '0.1965,0.8096 -0.1538,0.8096 -0.1517,0.8116 -0.1517,0.8544 -0.1436,0.8483 -0.1334,0.8462 -0.1232,0.8'
        '483 -0.1151,0.8544 -0.1151,0.8014 -0.1171,0.7974 -0.1232,0.7933 -0.1965,0.7933 -0.2088,0.7974 -0.218'
        '9,0.8116ZM0.2291,0.7607 0.2393,0.7709 0.2393,0.7648 0.2352,0.7607ZM-0.0825,0.7607 -0.0906,0.7607 -0.'
        '0947,0.7648 -0.0947,0.7749 -0.0927,0.7688ZM-0.4633,0.1640 -0.4593,0.1701 -0.4593,0.1843 -0.4633,0.19'
        '04 -0.4552,0.1864 0.4532,0.1864 0.4613,0.1904 0.4572,0.1843 0.4572,0.1701 0.4613,0.1640 0.4511,0.168'
        '0 -0.4532,0.1680ZM0.1151,0.0214 0.1415,0.0214 0.1415,0.0193 0.1171,0.0193Z'
    ),
    '618.3C/0': (
        'M-0.4776,-1.4071 -0.4939,-1.3908 -0.5000,-1.3765 -0.5000,1.3765 -0.4918,1.3929 -0.4796,1.4051 -0.467'
        '3,1.4112 0.4633,1.4112 0.4755,1.4051 0.4878,1.3929 0.4939,1.3827 0.4980,1.3643 0.4980,-1.3663 0.4959'
        ',-1.3786 0.4878,-1.3949 0.4776,-1.4051 0.4571,-1.4133 -0.4612,-1.4133Z'
    ),
    '618.3C/1': (
        'M0.1449,0.9276 0.1347,0.9337 0.1286,0.9480 0.1408,0.9643 0.1510,0.9663 0.1653,0.9561 0.1673,0.9398 0'
        '.1571,0.9296ZM-0.1735,0.9276 -0.1837,0.9357 -0.1878,0.9500 -0.1755,0.9643 -0.1653,0.9663 -0.1531,0.9'
        '582 -0.1490,0.9520 -0.1490,0.9418 -0.1592,0.9296ZM-0.1980,0.7969 -0.2061,0.8071 -0.2102,0.8398 -0.20'
        '61,0.8439 -0.1571,0.8439 -0.1531,0.8398 -0.1531,0.8010 -0.1571,0.7969ZM-0.4735,0.1827 -0.4776,0.1888'
        ' -0.4776,1.0112 -0.4673,1.0235 -0.4612,1.0276 0.4571,1.0276 0.4694,1.0173 0.4735,1.0112 0.4735,0.188'
        '8 0.4633,0.1765 0.4571,0.1724 -0.4612,0.1724ZM-0.2429,0.8704 -0.2306,0.8561 -0.2224,0.7990 -0.2184,0'
        '.7908 -0.2020,0.7786 -0.1245,0.7786 -0.1163,0.7847 -0.1163,0.8398 -0.1122,0.8439 -0.1020,0.8439 -0.0'
        '980,0.8398 -0.0980,0.7520 -0.0878,0.7439 0.2306,0.7439 0.2408,0.7541 0.2408,0.9459 0.2388,0.9480 0.1'
        '939,0.9480 0.1816,0.9724 0.1694,0.9827 0.1592,0.9867 0.1367,0.9867 0.1224,0.9786 0.1122,0.9663 0.108'
        '2,0.9520 0.1041,0.9480 -0.1224,0.9480 -0.1286,0.9541 -0.1347,0.9704 -0.1469,0.9827 -0.1571,0.9867 -0'
        '.1816,0.9867 -0.1898,0.9827 -0.2061,0.9643 -0.2082,0.9520 -0.2122,0.9480 -0.2306,0.9459 -0.2429,0.88'
        '67ZM0.2796,0.3724 0.2816,0.3745 0.2796,0.3806 0.2776,0.3786ZM0.1939,0.3133 0.1959,0.3153 0.1959,0.33'
        '78 0.2020,0.3500 0.2694,0.3500 0.2796,0.3724 0.2776,0.3745 0.2735,0.3704 0.2673,0.3765 0.2653,0.3867'
        ' 0.2592,0.3949 0.2449,0.4071 0.2347,0.4112 0.2102,0.4112 0.1980,0.4071 0.1816,0.3929 0.1735,0.3724 0'
        '.1735,0.3541 0.1755,0.3459 0.1918,0.3255ZM0.1245,0.2194 0.1327,0.2153 0.2082,0.2153 0.2102,0.2173 0.'
        '2000,0.2214 0.1898,0.2337 0.1939,0.3112 0.1918,0.3133 0.1857,0.3031 0.1633,0.3235 0.1531,0.3459 0.15'
        '10,0.3724 0.1531,0.3847 0.1612,0.4010 0.1796,0.4214 0.2000,0.4316 0.2224,0.4357 0.2531,0.4276 0.2633'
        ',0.4214 0.2816,0.4010 0.2857,0.3867 0.3000,0.4153 0.3327,0.4010 0.3388,0.3949 0.3306,0.3806 0.3122,0'
        '.3888 0.2918,0.3418 0.2816,0.3276 0.2204,0.3276 0.2184,0.3255 0.2204,0.3173 0.2653,0.3173 0.2694,0.3'
        '133 0.2694,0.2990 0.2653,0.2949 0.2184,0.2949 0.2163,0.2929 0.2143,0.2663 0.2327,0.2520 0.2347,0.233'
        '7 0.2245,0.2214 0.2143,0.2173 0.2163,0.2153 0.3327,0.2153 0.3429,0.2214 0.3449,0.2255 0.3449,0.4316 '
        '0.3388,0.4398 0.3347,0.4418 0.1306,0.4418 0.1204,0.4337 0.1204,0.2255ZM-0.0694,-0.3684 -0.0653,-0.36'
        '43 -0.0449,-0.3643 -0.0429,-0.3622 0.0490,-0.3622 0.0592,-0.3643 0.0633,-0.3684 0.0592,-0.3724 -0.06'
        '53,-0.3724ZM-0.0694,-0.3888 -0.0653,-0.3847 0.0592,-0.3847 0.0633,-0.3888 0.0592,-0.3929 -0.0653,-0.'
        '3929ZM-0.0694,-0.4092 -0.0653,-0.4051 0.0592,-0.4051 0.0633,-0.4092 0.0592,-0.4133 -0.0653,-0.4133ZM'
        '0.0898,-0.4296 0.0796,-0.4214 0.0776,-0.4092 0.0898,-0.3949 0.1000,-0.3949 0.1122,-0.4051 0.1143,-0.'
        '4153 0.1061,-0.4276ZM-0.1082,-0.4296 -0.1184,-0.4173 -0.1184,-0.4071 -0.1102,-0.3969 -0.0959,-0.3949'
        ' -0.0857,-0.4031 -0.0837,-0.4194 -0.0939,-0.4296ZM-0.0980,-0.4806 -0.0980,-0.4663 -0.0898,-0.4582 -0'
        '.0408,-0.4582 -0.0388,-0.4602 0.0857,-0.4582 0.0939,-0.4684 0.0898,-0.4949 0.0857,-0.5031 0.0755,-0.'
        '5133 0.0592,-0.5173 -0.0306,-0.5194 -0.0327,-0.5173 -0.0735,-0.5153 -0.0918,-0.5010ZM-0.0694,-0.6133'
        ' -0.0735,-0.6092 -0.0694,-0.6051 -0.0653,-0.6092ZM0.1082,-0.6276 0.1020,-0.6235 0.1204,-0.6051 0.110'
        '2,-0.5867 0.1061,-0.5847 0.0898,-0.5867 0.0816,-0.5969 0.0816,-0.6071 0.0857,-0.6153 0.0816,-0.6194 '
        '0.0735,-0.6051 0.0755,-0.5929 0.0878,-0.5786 0.0939,-0.5765 0.1122,-0.5786 0.1245,-0.5929 0.1265,-0.'
        '6010 0.1224,-0.6071 0.1245,-0.6112ZM-0.0980,-0.6276 -0.1143,-0.6133 -0.1163,-0.5969 -0.1020,-0.5786 '
        '-0.0857,-0.5765 -0.0755,-0.5806 -0.0673,-0.5888 -0.0653,-0.5969 -0.0694,-0.6010 -0.0755,-0.5908 -0.0'
        '837,-0.5847 -0.1000,-0.5867 -0.1082,-0.5969 -0.1082,-0.6092 -0.1020,-0.6173 -0.0898,-0.6235ZM0.0633,'
        '-0.6398 0.0571,-0.6398 0.0531,-0.6357 0.0531,-0.6276 0.0571,-0.6235 0.0673,-0.6357ZM0.0184,-0.6643 0'
        '.0061,-0.6765 -0.0122,-0.6663 -0.0184,-0.6582 -0.0143,-0.6541 0.0061,-0.6480ZM-0.0633,-0.7622 -0.098'
        '0,-0.7520 -0.1204,-0.7418 -0.1551,-0.7194 -0.1939,-0.6847 -0.2224,-0.6480 -0.2449,-0.6031 -0.2531,-0'
        '.5806 -0.2592,-0.5500 -0.2612,-0.4908 -0.2571,-0.4582 -0.2429,-0.4112 -0.2204,-0.3684 -0.2041,-0.345'
        '9 -0.1694,-0.3112 -0.1510,-0.2969 -0.1143,-0.2745 -0.0592,-0.2561 -0.0082,-0.2500 0.0449,-0.2541 0.0'
        '837,-0.2643 0.1367,-0.2908 0.1694,-0.3153 0.2122,-0.3643 0.2327,-0.3990 0.2449,-0.4296 0.2531,-0.464'
        '3 0.2571,-0.4969 0.2571,-0.5255 0.2531,-0.5582 0.2388,-0.6051 0.2163,-0.6500 0.1796,-0.6949 0.1449,-'
        '0.7235 0.1102,-0.7439 0.0531,-0.7643 0.0245,-0.7684 -0.0286,-0.7684ZM-0.0918,-0.5357 -0.0735,-0.5418'
        ' 0.0673,-0.5418 0.0796,-0.5398 0.0959,-0.5255 0.1020,-0.5112 0.1102,-0.4520 0.1306,-0.4316 0.1306,-0'
        '.3602 0.1204,-0.3480 0.1204,-0.3051 0.1122,-0.2969 0.0918,-0.2949 0.0776,-0.3031 0.0776,-0.3418 0.07'
        '35,-0.3459 0.0327,-0.3418 -0.0265,-0.3418 -0.0286,-0.3439 -0.0796,-0.3459 -0.0837,-0.3418 -0.0837,-0'
        '.3031 -0.0959,-0.2949 -0.1122,-0.2949 -0.1265,-0.3051 -0.1265,-0.3480 -0.1327,-0.3541 -0.1367,-0.364'
        '3 -0.1367,-0.4276 -0.1306,-0.4398 -0.1163,-0.4500 -0.1082,-0.5092 -0.1020,-0.5255ZM-0.1367,-0.6071 -'
        '0.1286,-0.6296 -0.1122,-0.6439 -0.0980,-0.6480 -0.0939,-0.6520 -0.0939,-0.6704 -0.0918,-0.6724 -0.07'
        '14,-0.6724 -0.0592,-0.6786 -0.0510,-0.6867 -0.0286,-0.7235 -0.0245,-0.7214 -0.0347,-0.6786 -0.0286,-'
        '0.6745 -0.0204,-0.6806 -0.0041,-0.7031 -0.0122,-0.7153 -0.0163,-0.7378 -0.0102,-0.7480 0.0082,-0.750'
        '0 0.0204,-0.7378 0.0163,-0.7194 0.0408,-0.7071 0.0653,-0.6827 0.0735,-0.6663 0.1143,-0.6663 0.1184,-'
        '0.6643 0.1224,-0.6541 0.1367,-0.6439 0.1469,-0.6316 0.1531,-0.6194 0.1551,-0.6031 0.1449,-0.5969 0.1'
        '449,-0.5888 0.1388,-0.5765 0.1265,-0.5643 0.1082,-0.5561 0.0837,-0.5582 0.0755,-0.5622 0.0592,-0.578'
        '6 -0.0245,-0.5786 -0.0429,-0.5929 -0.0510,-0.5765 -0.0633,-0.5643 -0.0816,-0.5561 -0.1061,-0.5582 -0'
        '.1265,-0.5724 -0.1367,-0.5929ZM-0.4673,-1.3867 -0.4776,-1.3724 -0.4776,0.1337 -0.4633,0.1500 -0.4551'
        ',0.1520 0.4510,0.1520 0.4592,0.1500 0.4735,0.1357 0.4735,-1.3745 0.4633,-1.3867 0.4551,-1.3908 -0.45'
        '92,-1.3908ZM-0.0306,-0.8316 0.0265,-0.8316 0.0898,-0.8194 0.1490,-0.7949 0.1796,-0.7765 0.2061,-0.75'
        '61 0.2551,-0.7051 0.2755,-0.6745 0.2939,-0.6378 0.3061,-0.6051 0.3184,-0.5398 0.3184,-0.4745 0.3082,'
        '-0.4235 0.2959,-0.3867 0.2755,-0.3459 0.2571,-0.3173 0.2163,-0.2724 0.1612,-0.2316 0.1000,-0.2031 0.'
        '0612,-0.1929 0.0327,-0.1888 -0.0327,-0.1888 -0.0898,-0.1990 -0.1633,-0.2296 -0.2143,-0.2663 -0.2551,'
        '-0.3092 -0.2857,-0.3561 -0.3102,-0.4133 -0.3204,-0.4541 -0.3245,-0.4867 -0.3245,-0.5398 -0.3184,-0.5'
        '765 -0.3082,-0.6133 -0.2857,-0.6643 -0.2551,-0.7112 -0.2163,-0.7520 -0.1694,-0.7867 -0.1020,-0.8173 '
        '-0.0796,-0.8214 -0.0714,-0.8255Z'
    ),
    '618.3C/2': (
        'M-0.4796,1.0704 -0.4796,1.3684 -0.4735,1.3806 -0.4592,1.3908 0.4551,1.3908 0.4714,1.3786 0.4755,1.36'
        '84 0.4755,1.0684 0.4735,1.0622 0.4571,1.0480 0.4469,1.0459 -0.4510,1.0459 -0.4673,1.0520 -0.4755,1.0'
        '602ZM-0.2653,1.0929 -0.2388,1.0929 -0.2163,1.0969 -0.1939,1.1051 -0.1755,1.1153 -0.1612,1.1276 -0.14'
        '69,1.1439 -0.1306,1.1724 -0.1245,1.1908 -0.1204,1.2173 -0.1224,1.2439 -0.1306,1.2704 -0.1429,1.2949 '
        '-0.1714,1.3255 -0.1878,1.3357 -0.2122,1.3459 -0.2429,1.3520 -0.2735,1.3500 -0.2980,1.3439 -0.3224,1.'
        '3316 -0.3531,1.3031 -0.3694,1.2786 -0.3776,1.2541 -0.3776,1.2418 -0.3816,1.2276 -0.3796,1.2010 -0.37'
        '35,1.1786 -0.3633,1.1561 -0.3531,1.1418 -0.3286,1.1173 -0.3122,1.1071 -0.2857,1.0969Z'
    ),
    '618.3C/3': (
        'M-0.2571,1.0908 -0.2837,1.0949 -0.3061,1.1031 -0.3306,1.1173 -0.3510,1.1378 -0.3633,1.1541 -0.3776,1'
        '.1888 -0.3816,1.2112 -0.3816,1.2337 -0.3714,1.2765 -0.3592,1.2969 -0.3367,1.3214 -0.3204,1.3337 -0.2'
        '878,1.3480 -0.2673,1.3520 -0.2367,1.3520 -0.2143,1.3480 -0.1857,1.3357 -0.1531,1.3092 -0.1408,1.2929'
        ' -0.1224,1.2500 -0.1204,1.2092 -0.1245,1.1867 -0.1367,1.1582 -0.1510,1.1378 -0.1694,1.1194 -0.1918,1'
        '.1051 -0.2184,1.0949ZM-0.3327,1.1602 -0.1898,1.3031 -0.1939,1.3092 -0.2265,1.3235 -0.2612,1.3255 -0.'
        '2816,1.3214 -0.3061,1.3112 -0.3327,1.2867 -0.3469,1.2622 -0.3551,1.2255 -0.3531,1.2010 -0.3469,1.180'
        '6ZM-0.3122,1.1378 -0.2755,1.1214 -0.2347,1.1194 -0.1980,1.1337 -0.1735,1.1541 -0.1633,1.1663 -0.1490'
        ',1.2031 -0.1490,1.2398 -0.1551,1.2602 -0.1694,1.2847 -0.3143,1.1418ZM-0.0306,-0.8337 -0.0612,-0.8296'
        ' -0.1020,-0.8194 -0.1694,-0.7888 -0.2163,-0.7541 -0.2571,-0.7112 -0.2878,-0.6643 -0.3102,-0.6133 -0.'
        '3204,-0.5765 -0.3265,-0.5398 -0.3265,-0.4867 -0.3224,-0.4541 -0.3122,-0.4133 -0.2878,-0.3561 -0.2571'
        ',-0.3092 -0.2143,-0.2643 -0.1633,-0.2276 -0.0898,-0.1969 -0.0327,-0.1867 0.0327,-0.1867 0.0612,-0.19'
        '08 0.1000,-0.2010 0.1612,-0.2296 0.2163,-0.2704 0.2592,-0.3173 0.2776,-0.3459 0.2980,-0.3867 0.3102,'
        '-0.4235 0.3204,-0.4745 0.3204,-0.5398 0.3082,-0.6051 0.2959,-0.6378 0.2776,-0.6745 0.2571,-0.7051 0.'
        '2061,-0.7582 0.1796,-0.7786 0.1490,-0.7969 0.0898,-0.8214 0.0265,-0.8337ZM-0.0633,-0.7602 -0.0286,-0'
        '.7663 0.0245,-0.7663 0.0531,-0.7622 0.0918,-0.7500 0.1224,-0.7357 0.1449,-0.7214 0.1776,-0.6949 0.21'
        '43,-0.6500 0.2327,-0.6153 0.2510,-0.5582 0.2551,-0.5255 0.2551,-0.4969 0.2510,-0.4643 0.2429,-0.4296'
        ' 0.2306,-0.3990 0.2102,-0.3643 0.1694,-0.3173 0.1367,-0.2929 0.0837,-0.2663 0.0449,-0.2561 -0.0082,-'
        '0.2520 -0.0592,-0.2582 -0.1143,-0.2765 -0.1510,-0.2990 -0.1694,-0.3133 -0.2020,-0.3459 -0.2184,-0.36'
        '84 -0.2408,-0.4112 -0.2551,-0.4582 -0.2592,-0.4908 -0.2571,-0.5500 -0.2490,-0.5867 -0.2388,-0.6133 -'
        '0.2204,-0.6480 -0.1918,-0.6847 -0.1551,-0.7173 -0.1204,-0.7398 -0.0980,-0.7500Z'
    ),
    '618.3C/4': (
        'M-0.3327,1.1582 -0.3490,1.1806 -0.3571,1.2173 -0.3531,1.2500 -0.3347,1.2867 -0.3061,1.3133 -0.2735,1'
        '.3255 -0.2612,1.3276 -0.2265,1.3255 -0.1939,1.3112 -0.1878,1.3031ZM-0.3122,1.1357 -0.3163,1.1418 -0.'
        '1694,1.2867 -0.1612,1.2765 -0.1490,1.2480 -0.1469,1.2031 -0.1592,1.1704 -0.1714,1.1541 -0.1980,1.131'
        '6 -0.2347,1.1173 -0.2755,1.1194ZM0.1245,0.2173 0.1184,0.2255 0.1184,0.4337 0.1306,0.4439 0.3347,0.44'
        '39 0.3388,0.4418 0.3469,0.4316 0.3469,0.2255 0.3449,0.2214 0.3327,0.2133 0.2163,0.2133 0.2122,0.2173'
        ' 0.2082,0.2133 0.1327,0.2133ZM0.1796,0.3092 0.1857,0.3051 0.1898,0.3133 0.1898,0.3255 0.1735,0.3459 '
        '0.1714,0.3541 0.1714,0.3724 0.1796,0.3929 0.2020,0.4112 0.2347,0.4133 0.2510,0.4051 0.2612,0.3949 0.'
        '2735,0.3724 0.2816,0.3888 0.2816,0.3969 0.2633,0.4194 0.2347,0.4316 0.2224,0.4337 0.2061,0.4316 0.17'
        '96,0.4194 0.1673,0.4071 0.1551,0.3847 0.1531,0.3582 0.1592,0.3337ZM0.2000,0.2235 0.2122,0.2173 0.224'
        '5,0.2235 0.2327,0.2337 0.2306,0.2520 0.2122,0.2663 0.2143,0.2929 0.2184,0.2969 0.2653,0.2969 0.2673,'
        '0.2990 0.2653,0.3153 0.2204,0.3153 0.2163,0.3194 0.2163,0.3255 0.2204,0.3296 0.2816,0.3296 0.2898,0.'
        '3418 0.3082,0.3867 0.3122,0.3908 0.3306,0.3827 0.3367,0.3949 0.3327,0.3990 0.3000,0.4133 0.2776,0.36'
        '02 0.2694,0.3480 0.2020,0.3480 0.2000,0.3459 0.1918,0.2643 0.1918,0.2337Z'
    ),
    '618.3C/5': (
        'M-0.2082,0.9520 -0.2061,0.9622 -0.2000,0.9724 -0.1878,0.9827 -0.1755,0.9867 -0.1612,0.9867 -0.1490,0'
        '.9827 -0.1388,0.9745 -0.1286,0.9561 -0.1286,0.9520 -0.1408,0.9500 -0.1490,0.9439 -0.1490,0.9541 -0.1'
        '592,0.9643 -0.1735,0.9663 -0.1857,0.9561 -0.1878,0.9439 -0.1959,0.9500ZM0.1082,0.9500 0.1143,0.9684 '
        '0.1265,0.9806 0.1429,0.9867 0.1551,0.9867 0.1714,0.9806 0.1837,0.9684 0.1878,0.9582 0.1857,0.9500 0.'
        '1776,0.9500 0.1694,0.9439 0.1694,0.9500 0.1612,0.9622 0.1531,0.9663 0.1429,0.9663 0.1327,0.9582 0.12'
        '86,0.9500 0.1306,0.9418 0.1224,0.9480ZM0.2388,0.9357 0.2286,0.9459 0.2388,0.9459ZM0.1510,0.9071 0.15'
        '10,0.9153 0.1408,0.9296 0.1571,0.9276 0.1612,0.9316 0.1592,0.9296 0.1612,0.9092ZM-0.1714,0.9071 -0.1'
        '714,0.9214 -0.1755,0.9276 -0.1612,0.9276 -0.1653,0.9214 -0.1653,0.9071ZM-0.2306,0.8520 -0.2204,0.843'
        '9 -0.2122,0.8439 -0.2061,0.8051 -0.1980,0.7949 -0.1551,0.7949 -0.1531,0.7969 -0.1531,0.8398 -0.1449,'
        '0.8337 -0.1347,0.8316 -0.1245,0.8337 -0.1163,0.8398 -0.1163,0.7888 -0.1224,0.7806 -0.2041,0.7806 -0.'
        '2122,0.7847 -0.2204,0.7969ZM-0.4653,0.1500 -0.4612,0.1561 -0.4612,0.1684 -0.4653,0.1745 -0.4551,0.17'
        '04 0.4510,0.1704 0.4612,0.1745 0.4571,0.1684 0.4571,0.1561 0.4612,0.1500 0.4571,0.1520 -0.4612,0.152'
        '0ZM0.1184,-0.3398 0.1122,-0.3337 0.0980,-0.3296 0.0878,-0.3316 0.0796,-0.3378 0.0796,-0.3031 0.0959,'
        '-0.2949 0.1184,-0.3031ZM-0.1245,-0.3418 -0.1245,-0.3031 -0.1082,-0.2949 -0.0898,-0.2990 -0.0837,-0.3'
        '051 -0.0837,-0.3418 -0.0898,-0.3357 -0.1041,-0.3316 -0.1143,-0.3337ZM-0.0776,-0.3459 -0.0490,-0.3459'
        ' -0.0469,-0.3439 0.0714,-0.3459 0.0653,-0.3520 0.0612,-0.3622 -0.0673,-0.3622 -0.0714,-0.3520ZM-0.10'
        '20,-0.5235 -0.1082,-0.5031 -0.1163,-0.4459 -0.1265,-0.4418 -0.1347,-0.4316 -0.1347,-0.3847 -0.1265,-'
        '0.3949 -0.1143,-0.3969 -0.1204,-0.4112 -0.1163,-0.4235 -0.1061,-0.4316 -0.0918,-0.4296 -0.0816,-0.41'
        '73 -0.0816,-0.4092 -0.0857,-0.4010 -0.0918,-0.3969 -0.0796,-0.3949 -0.0714,-0.3867 -0.0673,-0.3724 0'
        '.0612,-0.3724 0.0653,-0.3867 0.0735,-0.3949 0.0857,-0.3969 0.0776,-0.4071 0.0776,-0.4173 0.0857,-0.4'
        '296 0.0980,-0.4316 0.1041,-0.4296 0.1143,-0.4173 0.1143,-0.4071 0.1082,-0.3969 0.1204,-0.3949 0.1286'
        ',-0.3867 0.1306,-0.3806 0.1306,-0.4276 0.1245,-0.4398 0.1102,-0.4480 0.1000,-0.5153 0.0939,-0.5276 0'
        '.0816,-0.5378 0.0755,-0.5398 -0.0776,-0.5398 -0.0939,-0.5337ZM-0.0714,-0.3908 -0.0673,-0.3949 0.0612'
        ',-0.3949 0.0653,-0.3908 0.0653,-0.3847 0.0633,-0.3827 -0.0673,-0.3827ZM-0.0714,-0.4112 -0.0592,-0.41'
        '53 0.0510,-0.4153 0.0633,-0.4133 0.0653,-0.4051 0.0633,-0.4031 -0.0673,-0.4031ZM-0.1000,-0.4724 -0.0'
        '939,-0.4990 -0.0837,-0.5112 -0.0694,-0.5173 -0.0490,-0.5173 -0.0469,-0.5194 0.0673,-0.5173 0.0857,-0'
        '.5051 0.0939,-0.4786 0.0939,-0.4663 0.0837,-0.4561 0.0020,-0.4582 0.0000,-0.4602 -0.0878,-0.4561 -0.'
        '0980,-0.4643ZM0.0714,-0.6643 0.0714,-0.6561 0.0592,-0.6398 0.0694,-0.6378 0.0571,-0.6194 0.0612,-0.6'
        '092 0.0612,-0.5969 0.0571,-0.5888 0.0469,-0.5806 0.0592,-0.5806 0.0714,-0.5663 0.0878,-0.5582 0.1184'
        ',-0.5602 0.1367,-0.5745 0.1429,-0.5867 0.1449,-0.5990 0.1531,-0.6031 0.1510,-0.6214 0.1449,-0.6337 0'
        '.1204,-0.6541 0.1204,-0.6602 0.1163,-0.6643ZM0.1041,-0.6296 0.1143,-0.6255 0.1224,-0.6173 0.1265,-0.'
        '6092 0.1265,-0.5969 0.1224,-0.5867 0.1102,-0.5765 0.0980,-0.5745 0.0898,-0.5765 0.0796,-0.5847 0.073'
        '5,-0.5969 0.0735,-0.6092 0.0776,-0.6173 0.0837,-0.6214 0.0878,-0.6153 0.0816,-0.6031 0.0857,-0.5908 '
        '0.0959,-0.5847 0.1082,-0.5867 0.1163,-0.5969 0.1163,-0.6092 0.1122,-0.6153 0.1000,-0.6235 0.1000,-0.'
        '6276ZM0.0102,-0.7480 -0.0041,-0.7500 -0.0143,-0.7398 -0.0163,-0.7316 -0.0122,-0.7296 -0.0122,-0.7173'
        ' -0.0020,-0.7051 -0.0163,-0.6827 -0.0286,-0.6745 -0.0347,-0.6765 -0.0245,-0.7214 -0.0286,-0.7235 -0.'
        '0490,-0.6888 -0.0612,-0.6765 -0.0776,-0.6704 -0.0918,-0.6704 -0.0918,-0.6520 -0.0755,-0.6500 -0.0735'
        ',-0.6480 -0.0755,-0.6459 -0.0878,-0.6480 -0.1061,-0.6459 -0.1286,-0.6276 -0.1347,-0.6112 -0.1347,-0.'
        '5908 -0.1306,-0.5806 -0.1184,-0.5663 -0.1000,-0.5582 -0.0776,-0.5582 -0.0592,-0.5684 -0.0490,-0.5827'
        ' -0.0449,-0.5969 -0.0449,-0.6092 -0.0510,-0.6255 -0.0612,-0.6378 -0.0571,-0.6398 -0.0490,-0.6296 -0.'
        '0490,-0.6378 -0.0367,-0.6541 -0.0245,-0.6561 -0.0204,-0.6622 0.0082,-0.6786 0.0143,-0.6704 0.0143,-0'
        '.6786 0.0265,-0.6949 0.0408,-0.6990 0.0490,-0.6969 0.0388,-0.7071 0.0143,-0.7194 0.0184,-0.7276 0.01'
        '84,-0.7378ZM-0.0939,-0.6296 -0.0878,-0.6296 -0.0857,-0.6255 -0.0918,-0.6194 -0.1000,-0.6173 -0.1082,'
        '-0.6051 -0.1061,-0.5949 -0.0980,-0.5867 -0.0878,-0.5847 -0.0755,-0.5929 -0.0735,-0.5969 -0.0755,-0.6'
        '133 -0.0694,-0.6194 -0.0633,-0.6071 -0.0653,-0.5908 -0.0735,-0.5806 -0.0816,-0.5765 -0.1041,-0.5786 '
        '-0.1163,-0.5949 -0.1163,-0.6092 -0.1122,-0.6173Z'
    ),
    '651/0': (
        'M-0.5487,-0.4847 -0.5558,-0.4707 -0.5558,0.4695 -0.5499,0.4824 -0.5393,0.4930 -0.5252,0.4988 0.5241,'
        '0.4988 0.5358,0.4941 0.5487,0.4812 0.5546,0.4660 0.5546,-0.4671 0.5487,-0.4824 0.5370,-0.4941 0.5241'
        ',-0.5000 -0.5252,-0.5000 -0.5393,-0.4941Z'
    ),
    '651/1': (
        'M-0.2928,-0.2711 -0.2975,-0.2676 -0.2987,-0.2617 -0.2952,-0.2570 -0.2893,-0.2559 -0.2846,-0.2594 -0.'
        '2835,-0.2653 -0.2870,-0.2700ZM-0.3785,-0.2711 -0.3832,-0.2664 -0.3844,-0.2629 -0.3797,-0.2570 -0.375'
        '0,-0.2559 -0.3691,-0.2606 -0.3680,-0.2641 -0.3738,-0.2711ZM0.0100,-0.2899 0.0065,-0.2887 0.0018,-0.2'
        '817 0.0029,-0.2770 0.0076,-0.2723 0.0123,-0.2723 0.0194,-0.2782 0.0194,-0.2829 0.0135,-0.2887ZM0.046'
        '4,-0.2969 0.0405,-0.2899 0.0393,-0.2864 0.0417,-0.2840 0.0511,-0.2840 0.0534,-0.2864ZM0.0581,-0.3040'
        ' 0.0558,-0.3016 0.0651,-0.2876 0.0675,-0.2793 0.0651,-0.2770 0.0417,-0.2770 0.0393,-0.2746 0.0440,-0'
        '.2664 0.0522,-0.2594 0.0593,-0.2570 0.0663,-0.2570 0.0734,-0.2594 0.0816,-0.2664 0.0851,-0.2723 0.08'
        '63,-0.2852 0.0827,-0.2934 0.0781,-0.2993 0.0687,-0.3040ZM-0.0710,-0.3040 -0.0781,-0.3005 -0.0839,-0.'
        '2946 -0.0874,-0.2876 -0.0874,-0.2746 -0.0851,-0.2688 -0.0757,-0.2594 -0.0675,-0.2570 -0.0604,-0.2570'
        ' -0.0522,-0.2606 -0.0440,-0.2688 -0.0405,-0.2782 -0.0405,-0.2840 -0.0464,-0.2946 -0.0546,-0.2805 -0.'
        '0616,-0.2770 -0.0663,-0.2770 -0.0687,-0.2817 -0.0593,-0.2911 -0.0558,-0.3016 -0.0581,-0.3040ZM-0.375'
        '0,-0.2911 -0.3750,-0.2876 -0.3703,-0.2829 -0.3609,-0.2840 -0.2975,-0.2829 -0.2928,-0.2876 -0.2928,-0'
        '.2946 -0.2952,-0.3016 -0.2999,-0.3063 -0.3058,-0.3087 -0.3621,-0.3087 -0.3680,-0.3063 -0.3715,-0.302'
        '8ZM0.0323,-0.3228 0.0299,-0.3204 0.0205,-0.2923 0.0264,-0.2852 0.0288,-0.2876 0.0311,-0.2969 0.0405,'
        '-0.3087ZM-0.0393,-0.3239 -0.0358,-0.3192 -0.0088,-0.3005 -0.0006,-0.3063 0.0076,-0.3040 0.0100,-0.30'
        '05 0.0076,-0.2981 0.0100,-0.2958 0.0123,-0.2981 0.0112,-0.2993 0.0135,-0.3016 0.0205,-0.3216 0.0182,'
        '-0.3263 -0.0370,-0.3263ZM-0.3081,-0.3603 -0.3104,-0.3580 -0.3081,-0.3545 -0.3058,-0.3568ZM-0.3398,-0'
        '.3709 -0.3374,-0.3674 -0.3292,-0.3650 -0.3245,-0.3721 -0.3304,-0.3768ZM0.3257,-0.4178 0.3011,-0.4131'
        ' 0.2752,-0.4026 0.2600,-0.3920 0.2435,-0.3756 0.2365,-0.3650 0.2248,-0.3392 0.2201,-0.3157 0.2201,-0'
        '.2981 0.2248,-0.2711 0.2342,-0.2500 0.2435,-0.2359 0.2623,-0.2171 0.2788,-0.2066 0.2987,-0.1984 0.32'
        '22,-0.1937 0.3421,-0.1937 0.3656,-0.1984 0.3832,-0.2054 0.4067,-0.2207 0.4173,-0.2312 0.4313,-0.2512'
        ' 0.4407,-0.2758 0.4442,-0.2981 0.4442,-0.3169 0.4396,-0.3404 0.4290,-0.3638 0.4208,-0.3756 0.4043,-0'
        '.3920 0.3891,-0.4026 0.3597,-0.4143 0.3386,-0.4178ZM0.3398,-0.3873 0.3515,-0.3838 0.3562,-0.3768 0.3'
        '550,-0.3685 0.3480,-0.3592 0.3574,-0.3486 0.3656,-0.3286 0.3785,-0.3169 0.3844,-0.3146 0.3867,-0.315'
        '7 0.3903,-0.3146 0.3891,-0.3040 0.3856,-0.3016 0.3668,-0.3075 0.3597,-0.3122 0.3492,-0.3239 0.3468,-'
        '0.3216 0.3457,-0.3157 0.3492,-0.2946 0.3597,-0.2758 0.3633,-0.2653 0.3668,-0.2418 0.3691,-0.2394 0.3'
        '832,-0.2383 0.3844,-0.2359 0.3586,-0.2242 0.3562,-0.2265 0.3480,-0.2559 0.3386,-0.2746 0.3269,-0.291'
        '1 0.3116,-0.2676 0.2905,-0.2465 0.2917,-0.2383 0.2964,-0.2324 0.2952,-0.2312 0.2846,-0.2324 0.2729,-'
        '0.2500 0.2893,-0.2664 0.2999,-0.2817 0.3093,-0.3016 0.3128,-0.3192 0.3128,-0.3275 0.3104,-0.3298 0.3'
        '022,-0.3134 0.3034,-0.2993 0.2987,-0.2969 0.2928,-0.2993 0.2870,-0.3063 0.2905,-0.3110 0.2952,-0.332'
        '2 0.3058,-0.3498 0.3128,-0.3568 0.3198,-0.3615 0.3292,-0.3627 0.3316,-0.3650 0.3292,-0.3697 0.3304,-'
        '0.3791 0.3363,-0.3862ZM-0.0076,-0.4178 -0.0358,-0.4120 -0.0593,-0.4014 -0.0769,-0.3885 -0.0898,-0.37'
        '44 -0.1027,-0.3533 -0.1097,-0.3333 -0.1121,-0.3204 -0.1121,-0.2923 -0.1086,-0.2746 -0.0992,-0.2512 -'
        '0.0863,-0.2324 -0.0734,-0.2195 -0.0604,-0.2101 -0.0370,-0.1995 -0.0100,-0.1937 0.0088,-0.1937 0.0358'
        ',-0.1995 0.0569,-0.2089 0.0722,-0.2195 0.0863,-0.2336 0.0968,-0.2488 0.1062,-0.2700 0.1109,-0.2911 0'
        '.1109,-0.3181 0.1062,-0.3415 0.0968,-0.3627 0.0886,-0.3744 0.0745,-0.3897 0.0640,-0.3979 0.0417,-0.4'
        '096 0.0147,-0.4167ZM-0.0992,-0.2887 -0.0933,-0.3016 -0.0816,-0.3122 -0.0698,-0.3157 -0.0546,-0.3146 '
        '-0.0522,-0.3169 -0.0452,-0.3427 -0.0511,-0.3486 -0.0499,-0.3580 -0.0464,-0.3615 -0.0417,-0.3627 -0.0'
        '264,-0.3627 -0.0252,-0.3533 -0.0358,-0.3521 -0.0381,-0.3498 -0.0358,-0.3474 -0.0346,-0.3439 -0.0358,'
        '-0.3392 -0.0335,-0.3369 0.0241,-0.3369 0.0276,-0.3404 0.0276,-0.3427 0.0252,-0.3451 0.0158,-0.3462 0'
        '.0135,-0.3486 0.0147,-0.3533 0.0475,-0.3533 0.0487,-0.3521 0.0475,-0.3486 0.0405,-0.3439 0.0370,-0.3'
        '392 0.0370,-0.3357 0.0452,-0.3204 0.0499,-0.3146 0.0710,-0.3157 0.0851,-0.3087 0.0910,-0.3028 0.0957'
        ',-0.2946 0.0980,-0.2864 0.0980,-0.2746 0.0945,-0.2641 0.0827,-0.2512 0.0675,-0.2453 0.0499,-0.2477 0'
        '.0428,-0.2512 0.0323,-0.2617 0.0288,-0.2700 0.0288,-0.2746 0.0264,-0.2770 0.0194,-0.2676 0.0229,-0.2'
        '629 0.0276,-0.2617 0.0276,-0.2582 0.0229,-0.2559 0.0147,-0.2570 0.0135,-0.2582 0.0147,-0.2641 0.0123'
        ',-0.2664 0.0053,-0.2664 -0.0018,-0.2723 -0.0041,-0.2770 -0.0041,-0.2840 -0.0100,-0.2899 -0.0370,-0.3'
        '087 -0.0393,-0.3052 -0.0323,-0.2958 -0.0288,-0.2805 -0.0323,-0.2653 -0.0440,-0.2512 -0.0558,-0.2465 '
        '-0.0687,-0.2453 -0.0781,-0.2477 -0.0839,-0.2512 -0.0945,-0.2617 -0.0992,-0.2723ZM-0.3410,-0.4178 -0.'
        '3609,-0.4143 -0.3762,-0.4096 -0.3926,-0.4014 -0.4114,-0.3873 -0.4219,-0.3756 -0.4313,-0.3615 -0.4419'
        ',-0.3369 -0.4454,-0.3169 -0.4454,-0.2946 -0.4419,-0.2746 -0.4290,-0.2453 -0.4196,-0.2324 -0.4079,-0.'
        '2207 -0.3867,-0.2066 -0.3656,-0.1984 -0.3433,-0.1937 -0.3245,-0.1937 -0.2964,-0.1995 -0.2741,-0.2101'
        ' -0.2612,-0.2195 -0.2471,-0.2336 -0.2377,-0.2465 -0.2295,-0.2629 -0.2224,-0.2899 -0.2212,-0.3075 -0.'
        '2236,-0.3298 -0.2306,-0.3509 -0.2435,-0.3732 -0.2588,-0.3897 -0.2729,-0.4002 -0.2917,-0.4096 -0.3175'
        ',-0.4167ZM-0.3703,-0.3181 -0.3668,-0.3192 -0.3011,-0.3192 -0.2952,-0.3169 -0.2905,-0.3122 -0.2881,-0'
        '.3063 -0.2846,-0.2805 -0.2764,-0.2723 -0.2764,-0.2406 -0.2799,-0.2359 -0.2799,-0.2171 -0.2835,-0.213'
        '6 -0.2928,-0.2124 -0.2987,-0.2160 -0.2987,-0.2324 -0.3011,-0.2347 -0.3363,-0.2336 -0.3374,-0.2324 -0'
        '.3656,-0.2347 -0.3680,-0.2324 -0.3680,-0.2171 -0.3715,-0.2136 -0.3809,-0.2124 -0.3867,-0.2160 -0.386'
        '7,-0.2359 -0.3914,-0.2406 -0.3914,-0.2711 -0.3820,-0.2817 -0.3785,-0.3087ZM-0.3914,-0.3498 -0.3891,-'
        '0.3556 -0.3820,-0.3627 -0.3727,-0.3674 -0.3727,-0.3744 -0.3609,-0.3768 -0.3527,-0.3850 -0.3480,-0.39'
        '44 -0.3445,-0.3979 -0.3433,-0.3932 -0.3468,-0.3803 -0.3433,-0.3779 -0.3363,-0.3850 -0.3339,-0.3897 -'
        '0.3386,-0.3944 -0.3398,-0.4038 -0.3351,-0.4096 -0.3292,-0.4096 -0.3245,-0.4049 -0.3234,-0.4002 -0.32'
        '57,-0.3967 -0.3151,-0.3908 -0.3034,-0.3791 -0.2999,-0.3732 -0.2811,-0.3721 -0.2799,-0.3685 -0.2682,-'
        '0.3568 -0.2658,-0.3462 -0.2694,-0.3427 -0.2729,-0.3333 -0.2799,-0.3275 -0.2858,-0.3251 -0.2964,-0.32'
        '63 -0.3011,-0.3286 -0.3081,-0.3357 -0.3445,-0.3357 -0.3504,-0.3404 -0.3597,-0.3286 -0.3727,-0.3251 -'
        '0.3820,-0.3275 -0.3879,-0.3333 -0.3914,-0.3404ZM-0.5346,-0.4718 -0.5370,-0.4671 -0.5370,0.4660 -0.53'
        '46,0.4707 -0.5276,0.4777 -0.5229,0.4800 0.5217,0.4800 0.5335,0.4695 0.5358,0.4636 0.5358,-0.4648 0.5'
        '335,-0.4707 0.5252,-0.4789 0.5205,-0.4812 -0.5229,-0.4812 -0.5276,-0.4789ZM-0.1121,0.3885 -0.0569,0.'
        '3333 -0.0076,0.3333 -0.0065,0.3345 -0.0405,0.3685 -0.0381,0.3709 0.1097,0.3709 0.1109,0.3721 0.1109,'
        '0.4073 0.1097,0.4085 -0.0370,0.4085 -0.0393,0.4108 -0.0065,0.4437 -0.0076,0.4448 -0.0569,0.4448ZM0.3'
        '198,-0.4448 0.3445,-0.4448 0.3715,-0.4390 0.4020,-0.4261 0.4231,-0.4120 0.4384,-0.3967 0.4525,-0.377'
        '9 0.4654,-0.3474 0.4712,-0.3169 0.4712,-0.2934 0.4665,-0.2676 0.4560,-0.2406 0.4407,-0.2171 0.4208,-'
        '0.1972 0.4055,-0.1866 0.3738,-0.1725 0.3445,-0.1667 0.3187,-0.1667 0.2905,-0.1725 0.2670,-0.1819 0.2'
        '412,-0.1995 0.2271,-0.2136 0.2107,-0.2371 0.2001,-0.2594 0.1931,-0.2911 0.1931,-0.3181 0.1966,-0.340'
        '4 0.2025,-0.3580 0.2107,-0.3744 0.2224,-0.3920 0.2447,-0.4143 0.2658,-0.4284 0.2776,-0.4343 0.2952,-'
        '0.4401ZM-0.0135,-0.4448 0.0123,-0.4448 0.0428,-0.4378 0.0628,-0.4296 0.0886,-0.4131 0.1015,-0.4014 0'
        '.1203,-0.3756 0.1332,-0.3451 0.1379,-0.3216 0.1379,-0.2887 0.1332,-0.2664 0.1227,-0.2394 0.1097,-0.2'
        '195 0.0933,-0.2019 0.0710,-0.1854 0.0405,-0.1725 0.0123,-0.1667 -0.0135,-0.1667 -0.0299,-0.1690 -0.0'
        '464,-0.1737 -0.0698,-0.1843 -0.0898,-0.1984 -0.1074,-0.2160 -0.1238,-0.2394 -0.1356,-0.2700 -0.1403,'
        '-0.2958 -0.1391,-0.3251 -0.1367,-0.3310 -0.1356,-0.3415 -0.1297,-0.3592 -0.1215,-0.3756 -0.1109,-0.3'
        '908 -0.0933,-0.4096 -0.0710,-0.4261 -0.0546,-0.4343 -0.0370,-0.4401ZM-0.3468,-0.4448 -0.3210,-0.4448'
        ' -0.2858,-0.4366 -0.2694,-0.4296 -0.2447,-0.4131 -0.2271,-0.3955 -0.2119,-0.3732 -0.2025,-0.3533 -0.'
        '1978,-0.3380 -0.1942,-0.3134 -0.1954,-0.2852 -0.1989,-0.2700 -0.2107,-0.2394 -0.2224,-0.2207 -0.2471'
        ',-0.1960 -0.2694,-0.1819 -0.2952,-0.1714 -0.3187,-0.1667 -0.3480,-0.1667 -0.3762,-0.1725 -0.4067,-0.'
        '1866 -0.4231,-0.1984 -0.4396,-0.2148 -0.4572,-0.2406 -0.4665,-0.2629 -0.4724,-0.2899 -0.4724,-0.3204'
        ' -0.4677,-0.3451 -0.4536,-0.3768 -0.4442,-0.3908 -0.4184,-0.4167 -0.3973,-0.4296 -0.3703,-0.4401Z'
    ),
    '651/2': (
        'M0.3198,-0.4460 0.2952,-0.4413 0.2776,-0.4354 0.2658,-0.4296 0.2447,-0.4155 0.2212,-0.3920 0.2095,-0'
        '.3744 0.2013,-0.3580 0.1954,-0.3404 0.1919,-0.3181 0.1919,-0.2911 0.1989,-0.2594 0.2095,-0.2371 0.22'
        '59,-0.2136 0.2412,-0.1984 0.2670,-0.1808 0.2905,-0.1714 0.3187,-0.1655 0.3445,-0.1655 0.3738,-0.1714'
        ' 0.4055,-0.1854 0.4208,-0.1960 0.4419,-0.2171 0.4572,-0.2406 0.4677,-0.2676 0.4724,-0.2934 0.4724,-0'
        '.3169 0.4665,-0.3474 0.4536,-0.3779 0.4396,-0.3967 0.4231,-0.4131 0.4020,-0.4272 0.3715,-0.4401 0.34'
        '45,-0.4460ZM0.3257,-0.4167 0.3386,-0.4167 0.3597,-0.4131 0.3797,-0.4061 0.4043,-0.3908 0.4196,-0.375'
        '6 0.4278,-0.3638 0.4384,-0.3404 0.4431,-0.3169 0.4431,-0.2981 0.4396,-0.2758 0.4302,-0.2512 0.4161,-'
        '0.2312 0.4067,-0.2218 0.3832,-0.2066 0.3656,-0.1995 0.3421,-0.1948 0.3222,-0.1948 0.2987,-0.1995 0.2'
        '788,-0.2077 0.2623,-0.2183 0.2447,-0.2359 0.2353,-0.2500 0.2259,-0.2711 0.2212,-0.2981 0.2212,-0.315'
        '7 0.2259,-0.3392 0.2377,-0.3650 0.2447,-0.3756 0.2600,-0.3908 0.2752,-0.4014 0.3011,-0.4120ZM-0.0135'
        ',-0.4460 -0.0370,-0.4413 -0.0546,-0.4354 -0.0710,-0.4272 -0.0933,-0.4108 -0.1121,-0.3908 -0.1227,-0.'
        '3756 -0.1309,-0.3592 -0.1367,-0.3415 -0.1379,-0.3310 -0.1403,-0.3251 -0.1414,-0.2958 -0.1367,-0.2700'
        ' -0.1250,-0.2394 -0.1086,-0.2160 -0.0898,-0.1972 -0.0698,-0.1831 -0.0464,-0.1725 -0.0299,-0.1678 -0.'
        '0135,-0.1655 0.0123,-0.1655 0.0405,-0.1714 0.0710,-0.1843 0.0933,-0.2007 0.1109,-0.2195 0.1238,-0.23'
        '94 0.1344,-0.2664 0.1391,-0.2887 0.1391,-0.3216 0.1344,-0.3451 0.1215,-0.3756 0.1027,-0.4014 0.0886,'
        '-0.4143 0.0628,-0.4308 0.0428,-0.4390 0.0123,-0.4460ZM-0.0076,-0.4167 0.0147,-0.4155 0.0417,-0.4085 '
        '0.0640,-0.3967 0.0745,-0.3885 0.0874,-0.3744 0.0957,-0.3627 0.1050,-0.3415 0.1097,-0.3181 0.1097,-0.'
        '2911 0.1050,-0.2700 0.0957,-0.2488 0.0851,-0.2336 0.0722,-0.2207 0.0569,-0.2101 0.0358,-0.2007 0.008'
        '8,-0.1948 -0.0100,-0.1948 -0.0370,-0.2007 -0.0604,-0.2113 -0.0734,-0.2207 -0.0851,-0.2324 -0.0980,-0'
        '.2512 -0.1074,-0.2746 -0.1109,-0.2923 -0.1109,-0.3204 -0.1086,-0.3333 -0.1015,-0.3533 -0.0886,-0.374'
        '4 -0.0769,-0.3873 -0.0593,-0.4002 -0.0358,-0.4108ZM-0.3468,-0.4460 -0.3703,-0.4413 -0.3973,-0.4308 -'
        '0.4184,-0.4178 -0.4454,-0.3908 -0.4548,-0.3768 -0.4689,-0.3451 -0.4736,-0.3204 -0.4736,-0.2899 -0.46'
        '77,-0.2629 -0.4583,-0.2406 -0.4407,-0.2148 -0.4231,-0.1972 -0.4067,-0.1854 -0.3762,-0.1714 -0.3480,-'
        '0.1655 -0.3187,-0.1655 -0.2952,-0.1702 -0.2694,-0.1808 -0.2471,-0.1948 -0.2212,-0.2207 -0.2095,-0.23'
        '94 -0.1978,-0.2700 -0.1942,-0.2852 -0.1931,-0.3134 -0.1966,-0.3380 -0.2013,-0.3533 -0.2107,-0.3732 -'
        '0.2259,-0.3955 -0.2447,-0.4143 -0.2694,-0.4308 -0.2858,-0.4378 -0.3210,-0.4460ZM-0.3410,-0.4167 -0.3'
        '175,-0.4155 -0.2917,-0.4085 -0.2729,-0.3991 -0.2588,-0.3885 -0.2447,-0.3732 -0.2318,-0.3509 -0.2248,'
        '-0.3298 -0.2224,-0.3075 -0.2236,-0.2899 -0.2306,-0.2629 -0.2353,-0.2523 -0.2482,-0.2336 -0.2612,-0.2'
        '207 -0.2741,-0.2113 -0.2964,-0.2007 -0.3245,-0.1948 -0.3433,-0.1948 -0.3656,-0.1995 -0.3867,-0.2077 '
        '-0.4079,-0.2218 -0.4184,-0.2324 -0.4278,-0.2453 -0.4372,-0.2641 -0.4419,-0.2793 -0.4442,-0.2946 -0.4'
        '442,-0.3169 -0.4407,-0.3369 -0.4302,-0.3615 -0.4208,-0.3756 -0.4114,-0.3862 -0.3926,-0.4002 -0.3762,'
        '-0.4085 -0.3609,-0.4131Z'
    ),
    '651/3': (
        'M-0.5499,0.4695 -0.5487,0.4765 -0.5452,0.4824 -0.5393,0.4883 -0.5299,0.4930 -0.5264,0.4930 -0.5241,0'
        '.4859 -0.5182,0.4812 -0.5264,0.4789 -0.5358,0.4695 -0.5370,0.4624 -0.5428,0.4683ZM0.5358,0.4566 0.53'
        '58,0.4660 0.5335,0.4707 0.5264,0.4777 0.5158,0.4812 0.5217,0.4859 0.5241,0.4941 0.5358,0.4894 0.5440'
        ',0.4812 0.5487,0.4707 0.5487,0.4660 0.5417,0.4648 0.5370,0.4601ZM-0.0381,0.4448 -0.0065,0.4448 -0.02'
        '52,0.4261 -0.0241,0.4343 -0.0264,0.4390 -0.0311,0.4437ZM0.1097,0.4014 0.1039,0.4073 0.1097,0.4073ZM-'
        '0.1050,0.3815 -0.1121,0.3885 -0.1050,0.3967 -0.1074,0.3932 -0.1074,0.3850ZM0.0980,0.3709 0.1050,0.37'
        '21 0.1097,0.3779 0.1097,0.3709ZM-0.0252,0.3521 -0.0076,0.3345 -0.0323,0.3345 -0.0264,0.3392 -0.0241,'
        '0.3439ZM0.3468,-0.3005 0.3457,-0.2969 0.3410,-0.2923 0.3292,-0.2899 0.3386,-0.2758 0.3480,-0.2570 0.'
        '3539,-0.2406 0.3574,-0.2242 0.3750,-0.2324 0.3832,-0.2347 0.3832,-0.2371 0.3727,-0.2383 0.3668,-0.24'
        '06 0.3609,-0.2711ZM0.3093,-0.3028 0.3069,-0.2946 0.2964,-0.2746 0.2741,-0.2500 0.2799,-0.2383 0.2858'
        ',-0.2324 0.2952,-0.2324 0.2952,-0.2347 0.2917,-0.2371 0.2893,-0.2465 0.3058,-0.2617 0.3245,-0.2887 0'
        '.3234,-0.2911 0.3163,-0.2923 0.3116,-0.2969ZM-0.3762,-0.3122 -0.3785,-0.3063 -0.3820,-0.2793 -0.3879'
        ',-0.2758 -0.3903,-0.2723 -0.3903,-0.2406 -0.3867,-0.2359 -0.3867,-0.2171 -0.3820,-0.2136 -0.3703,-0.'
        '2148 -0.3680,-0.2347 -0.3539,-0.2347 -0.3527,-0.2336 -0.2999,-0.2347 -0.2987,-0.2336 -0.2987,-0.2171'
        ' -0.2940,-0.2136 -0.2858,-0.2136 -0.2811,-0.2160 -0.2811,-0.2359 -0.2764,-0.2418 -0.2764,-0.2711 -0.'
        '2811,-0.2770 -0.2846,-0.2782 -0.2905,-0.3110 -0.2987,-0.3181 -0.3691,-0.3181ZM-0.3633,-0.2441 -0.360'
        '9,-0.2465 -0.3058,-0.2465 -0.3046,-0.2453 -0.3058,-0.2418 -0.3609,-0.2418ZM-0.3633,-0.2535 -0.3609,-'
        '0.2559 -0.3058,-0.2559 -0.3046,-0.2547 -0.3058,-0.2512 -0.3621,-0.2512ZM-0.3633,-0.2617 -0.3609,-0.2'
        '641 -0.3058,-0.2641 -0.3046,-0.2629 -0.3058,-0.2594 -0.3609,-0.2594ZM-0.2964,-0.2700 -0.2881,-0.2711'
        ' -0.2846,-0.2688 -0.2835,-0.2606 -0.2858,-0.2570 -0.2940,-0.2559 -0.2987,-0.2606 -0.2987,-0.2664ZM-0'
        '.3844,-0.2653 -0.3797,-0.2711 -0.3727,-0.2711 -0.3680,-0.2664 -0.3680,-0.2606 -0.3738,-0.2559 -0.378'
        '5,-0.2559 -0.3832,-0.2594ZM-0.3750,-0.2946 -0.3727,-0.3016 -0.3668,-0.3075 -0.3633,-0.3087 -0.3198,-'
        '0.3099 -0.3187,-0.3087 -0.3034,-0.3087 -0.2987,-0.3063 -0.2928,-0.2981 -0.2917,-0.2887 -0.2964,-0.28'
        '29 -0.3292,-0.2829 -0.3304,-0.2840 -0.3715,-0.2829 -0.3750,-0.2864ZM0.3492,-0.3251 0.3621,-0.3110 0.'
        '3680,-0.3075 0.3879,-0.3028 0.3903,-0.3134 0.3797,-0.3157 0.3715,-0.3216 0.3621,-0.3333 0.3609,-0.33'
        '80 0.3586,-0.3310 0.3539,-0.3263ZM0.3034,-0.3451 0.2964,-0.3333 0.2917,-0.3181 0.2917,-0.3110 0.2881'
        ',-0.3075 0.2881,-0.3040 0.2964,-0.2981 0.3011,-0.2981 0.3034,-0.3005 0.3022,-0.3157 0.3069,-0.3263 0'
        '.3104,-0.3298 0.3034,-0.3392ZM-0.0992,-0.2852 -0.0980,-0.2700 -0.0921,-0.2594 -0.0792,-0.2488 -0.071'
        '0,-0.2465 -0.0581,-0.2465 -0.0452,-0.2512 -0.0370,-0.2594 -0.0311,-0.2700 -0.0299,-0.2746 -0.0311,-0'
        '.2911 -0.0381,-0.3040 -0.0440,-0.3099 -0.0428,-0.3122 -0.0076,-0.2887 -0.0041,-0.2852 -0.0041,-0.280'
        '5 -0.0006,-0.2711 0.0076,-0.2664 0.0147,-0.2664 0.0158,-0.2629 0.0135,-0.2617 0.0135,-0.2582 0.0194,'
        '-0.2559 0.0276,-0.2582 0.0276,-0.2617 0.0229,-0.2617 0.0194,-0.2664 0.0194,-0.2688 0.0264,-0.2782 0.'
        '0288,-0.2758 0.0323,-0.2629 0.0358,-0.2582 0.0440,-0.2512 0.0569,-0.2465 0.0698,-0.2465 0.0816,-0.25'
        '12 0.0933,-0.2629 0.0968,-0.2723 0.0957,-0.2934 0.0921,-0.3005 0.0839,-0.3087 0.0722,-0.3146 0.0604,'
        '-0.3157 0.0499,-0.3134 0.0358,-0.3357 0.0370,-0.3415 0.0428,-0.3451 0.0487,-0.3521 0.0464,-0.3533 0.'
        '0158,-0.3533 0.0135,-0.3509 0.0147,-0.3474 0.0288,-0.3439 0.0252,-0.3357 -0.0358,-0.3357 -0.0370,-0.'
        '3369 -0.0358,-0.3462 -0.0393,-0.3498 -0.0381,-0.3533 -0.0252,-0.3533 -0.0252,-0.3615 -0.0452,-0.3615'
        ' -0.0499,-0.3568 -0.0499,-0.3474 -0.0452,-0.3439 -0.0452,-0.3380 -0.0534,-0.3134 -0.0734,-0.3146 -0.'
        '0827,-0.3110 -0.0933,-0.3005 -0.0968,-0.2946ZM0.0076,-0.2899 0.0135,-0.2899 0.0205,-0.2817 0.0194,-0'
        '.2770 0.0135,-0.2723 0.0065,-0.2723 0.0018,-0.2782 0.0018,-0.2829ZM0.0464,-0.2981 0.0522,-0.2911 0.0'
        '546,-0.2864 0.0534,-0.2840 0.0405,-0.2840 0.0393,-0.2852 0.0417,-0.2934ZM-0.0053,-0.2981 -0.0006,-0.'
        '2993 0.0018,-0.2946 0.0006,-0.2934ZM0.0593,-0.3052 0.0675,-0.3052 0.0757,-0.3016 0.0827,-0.2946 0.08'
        '63,-0.2876 0.0874,-0.2782 0.0839,-0.2688 0.0745,-0.2594 0.0698,-0.2570 0.0569,-0.2570 0.0511,-0.2594'
        ' 0.0417,-0.2688 0.0393,-0.2735 0.0405,-0.2782 0.0663,-0.2782 0.0675,-0.2793 0.0675,-0.2829 0.0546,-0'
        '.3028ZM-0.0687,-0.3052 -0.0593,-0.3052 -0.0558,-0.3028 -0.0581,-0.2923 -0.0675,-0.2829 -0.0675,-0.27'
        '82 -0.0628,-0.2770 -0.0558,-0.2805 -0.0522,-0.2840 -0.0487,-0.2911 -0.0487,-0.2946 -0.0464,-0.2969 -'
        '0.0405,-0.2864 -0.0405,-0.2758 -0.0440,-0.2676 -0.0499,-0.2617 -0.0593,-0.2570 -0.0698,-0.2570 -0.07'
        '81,-0.2606 -0.0851,-0.2676 -0.0886,-0.2770 -0.0886,-0.2852 -0.0851,-0.2934 -0.0769,-0.3016ZM0.0323,-'
        '0.3239 0.0417,-0.3087 0.0311,-0.2958 0.0288,-0.2852 0.0264,-0.2840 0.0194,-0.2923 0.0299,-0.3216ZM-0'
        '.0405,-0.3251 -0.0381,-0.3275 0.0205,-0.3275 0.0217,-0.3228 0.0123,-0.2969 0.0076,-0.2946 0.0053,-0.'
        '2981 0.0088,-0.2993 0.0088,-0.3040 0.0041,-0.3052 -0.0065,-0.3040 -0.0076,-0.2993 -0.0370,-0.3192 -0'
        '.0405,-0.3228ZM-0.3656,-0.3756 -0.3715,-0.3744 -0.3715,-0.3662 -0.3832,-0.3615 -0.3903,-0.3521 -0.39'
        '14,-0.3474 -0.3903,-0.3392 -0.3879,-0.3345 -0.3809,-0.3275 -0.3656,-0.3263 -0.3609,-0.3286 -0.3527,-'
        '0.3392 -0.3527,-0.3415 -0.3597,-0.3462 -0.3621,-0.3380 -0.3703,-0.3333 -0.3773,-0.3357 -0.3820,-0.34'
        '04 -0.3832,-0.3474 -0.3809,-0.3521 -0.3738,-0.3568 -0.3715,-0.3568 -0.3703,-0.3545 -0.3773,-0.3509 -'
        '0.3785,-0.3486 -0.3773,-0.3404 -0.3738,-0.3380 -0.3691,-0.3380 -0.3644,-0.3415 -0.3644,-0.3509 -0.37'
        '15,-0.3603 -0.3715,-0.3674ZM0.3386,-0.3862 0.3304,-0.3779 0.3292,-0.3732 0.3304,-0.3674 0.3327,-0.36'
        '50 0.3433,-0.3638 0.3480,-0.3615 0.3539,-0.3674 0.3550,-0.3779 0.3504,-0.3838 0.3457,-0.3862ZM-0.336'
        '3,-0.4085 -0.3398,-0.4014 -0.3374,-0.3991 -0.3374,-0.3932 -0.3339,-0.3908 -0.3363,-0.3838 -0.3445,-0'
        '.3768 -0.3468,-0.3779 -0.3433,-0.3955 -0.3445,-0.3979 -0.3527,-0.3838 -0.3586,-0.3779 -0.3562,-0.379'
        '1 -0.3492,-0.3779 -0.3410,-0.3709 -0.3292,-0.3779 -0.3245,-0.3732 -0.3269,-0.3674 -0.3163,-0.3650 -0'
        '.3116,-0.3603 -0.3104,-0.3568 -0.3093,-0.3615 -0.3034,-0.3603 -0.3093,-0.3498 -0.3116,-0.3415 -0.316'
        '3,-0.3369 -0.3234,-0.3357 -0.3069,-0.3357 -0.2999,-0.3286 -0.2952,-0.3263 -0.2835,-0.3263 -0.2788,-0'
        '.3286 -0.2729,-0.3345 -0.2705,-0.3439 -0.2658,-0.3451 -0.2682,-0.3556 -0.2717,-0.3615 -0.2776,-0.365'
        '0 -0.2823,-0.3721 -0.3011,-0.3721 -0.3034,-0.3779 -0.3163,-0.3908 -0.3257,-0.3955 -0.3245,-0.3991 -0'
        '.3257,-0.4061 -0.3281,-0.4085ZM-0.2870,-0.3568 -0.2799,-0.3521 -0.2776,-0.3439 -0.2788,-0.3404 -0.28'
        '35,-0.3357 -0.2905,-0.3333 -0.2940,-0.3345 -0.2987,-0.3392 -0.3011,-0.3474 -0.2999,-0.3509 -0.2964,-'
        '0.3533 -0.2952,-0.3521 -0.2964,-0.3415 -0.2917,-0.3380 -0.2870,-0.3380 -0.2823,-0.3427 -0.2823,-0.34'
        '86 -0.2893,-0.3545ZM-0.5264,-0.4941 -0.5393,-0.4894 -0.5487,-0.4777 -0.5499,-0.4707 -0.5428,-0.4695 '
        '-0.5370,-0.4636 -0.5358,-0.4707 -0.5276,-0.4789 -0.5182,-0.4824 -0.5241,-0.4871ZM0.5241,-0.4953 0.52'
        '17,-0.4871 0.5158,-0.4824 0.5264,-0.4789 0.5335,-0.4718 0.5358,-0.4671 0.5358,-0.4577 0.5370,-0.4613'
        ' 0.5417,-0.4660 0.5487,-0.4671 0.5487,-0.4718 0.5428,-0.4836 0.5335,-0.4918Z'
    ),
    '954/0': (
        'M-0.7388,-0.4375 -0.7567,-0.3884 -0.7567,0.3839 -0.7478,0.4152 -0.7254,0.4509 -0.6853,0.4821 -0.6406'
        ',0.4955 0.6362,0.4955 0.6897,0.4777 0.7344,0.4330 0.7522,0.3884 0.7522,-0.3973 0.7299,-0.4464 0.6853'
        ',-0.4866 0.6451,-0.5000 -0.6540,-0.5000 -0.7031,-0.4777Z'
    ),
    '954/1': (
        'M-0.6897,-0.3929 -0.6897,0.3839 -0.6629,0.4196 -0.6451,0.4286 0.6451,0.4286 0.6763,0.4018 0.6897,0.3'
        '661 0.6897,-0.3705 0.6853,-0.3929 0.6629,-0.4241 0.6362,-0.4375 -0.6362,-0.4375 -0.6585,-0.4286Z'
    ),
    '954.2/0': (
        'M-1.1018,-0.3982 -1.1018,0.3938 -1.0796,0.4425 -1.0487,0.4735 -1.0221,0.4867 -0.9867,0.4956 0.9823,0'
        '.4956 1.0442,0.4735 1.0885,0.4204 1.0973,0.3938 1.0973,-0.3938 1.0664,-0.4558 1.0133,-0.4912 0.9735,'
        '-0.5000 -0.9779,-0.5000 -1.0177,-0.4912 -1.0575,-0.4690 -1.0841,-0.4381Z'
    ),
    '954.2/1': (
        'M-1.0354,-0.3894 -1.0398,-0.3673 -1.0398,0.3628 -1.0265,0.4027 -1.0000,0.4248 -0.9867,0.4292 0.9823,'
        '0.4292 1.0044,0.4204 1.0310,0.3850 1.0354,0.3717 1.0354,-0.3717 1.0221,-0.4071 0.9823,-0.4336 -0.986'
        '7,-0.4336 -1.0088,-0.4248Z'
    ),
    '957/0': (
        'M-0.4174,0.0661 -0.4174,0.1033 -0.4091,0.1240 -0.3884,0.1488 -0.3554,0.1653 -0.3017,0.1612 -0.2645,0'
        '.1281 -0.2521,0.0992 -0.2521,0.0702 -0.2645,0.0455 -0.2603,0.0372 -0.2149,0.0661 -0.2025,0.0785 -0.1'
        '983,0.1033 -0.1860,0.1157 -0.1694,0.1198 -0.1570,0.1405 -0.1405,0.1446 -0.1198,0.1281 -0.0909,0.1570'
        ' -0.0702,0.1653 -0.0248,0.1653 -0.0083,0.1570 0.0165,0.1364 0.0331,0.1033 0.0289,0.0537 0.0207,0.037'
        '2 -0.0041,0.0124 -0.0372,0.0000 -0.0744,0.0041 -0.0868,-0.0083 -0.1033,-0.0372 -0.1033,-0.0496 -0.07'
        '85,-0.0702 -0.0868,-0.0826 -0.1570,-0.0826 -0.1653,-0.0702 -0.1488,-0.0579 -0.1364,-0.0579 -0.1322,-'
        '0.0537 -0.1364,-0.0455 -0.2603,-0.0455 -0.2727,-0.0702 -0.2479,-0.0744 -0.2397,-0.0826 -0.2397,-0.09'
        '50 -0.2479,-0.1033 -0.2975,-0.0992 -0.3099,-0.0826 -0.2975,-0.0579 -0.2975,-0.0372 -0.3140,0.0041 -0'
        '.3430,0.0000 -0.3719,0.0083 -0.4050,0.0372ZM-0.1322,0.1033 -0.1240,0.1157 -0.1281,0.1240 -0.1405,0.1'
        '157ZM-0.1818,0.0785 -0.1736,0.0702 -0.1570,0.0702 -0.1488,0.0868 -0.1570,0.0992 -0.1736,0.0992 -0.18'
        '18,0.0909ZM-0.0950,0.0620 -0.0826,0.0537 -0.0744,0.0661 -0.0909,0.0702ZM-0.0537,0.0331 -0.0207,0.041'
        '3 -0.0041,0.0579 0.0000,0.0702 0.0000,0.0992 -0.0083,0.1157 -0.0331,0.1322 -0.0661,0.1322 -0.0950,0.'
        '1033 -0.0909,0.0950 -0.0413,0.0950 -0.0331,0.0868 -0.0579,0.0413ZM-0.3554,0.0372 -0.3306,0.0331 -0.3'
        '223,0.0413 -0.3306,0.0661 -0.3471,0.0785 -0.3388,0.0950 -0.3182,0.0909 -0.2975,0.0702 -0.2934,0.0579'
        ' -0.2851,0.0744 -0.2893,0.1074 -0.3182,0.1322 -0.3512,0.1322 -0.3678,0.1240 -0.3843,0.0992 -0.3843,0'
        '.0702 -0.3760,0.0537ZM-0.1157,0.0000 -0.1033,0.0207 -0.1157,0.0331 -0.1322,0.0661 -0.1405,0.0537 -0.'
        '1240,0.0083ZM-0.2769,-0.0124 -0.2727,-0.0165 -0.1488,-0.0165 -0.1446,-0.0124 -0.1653,0.0372 -0.1818,'
        '0.0248 -0.1942,0.0248 -0.2107,0.0372ZM0.2273,-0.2521 0.2066,-0.2355 0.2025,-0.2231 0.2149,-0.1901 0.'
        '1818,-0.1736 0.1653,-0.1570 0.1488,-0.0909 0.1488,-0.0289 0.1529,-0.0248 0.1488,-0.0083 0.1612,0.004'
        '1 0.1777,0.0000 0.1860,0.0083 0.1860,0.0579 0.1983,0.1281 0.1942,0.1570 0.2107,0.1653 0.2273,0.1488 '
        '0.2314,0.1198 0.2355,0.1446 0.2521,0.1612 0.2645,0.1653 0.2727,0.1570 0.2686,0.0950 0.2769,0.0455 0.'
        '2769,-0.0702 0.2810,-0.0744 0.3017,-0.0289 0.3017,-0.0083 0.3388,0.0207 0.3223,0.0868 0.3388,0.1198 '
        '0.3430,0.1446 0.3347,0.1570 0.3430,0.1653 0.3554,0.1612 0.3678,0.1364 0.3719,0.1488 0.3926,0.1653 0.'
        '4008,0.1570 0.3967,0.1529 0.3967,0.0909 0.4215,0.0744 0.4174,0.0124 0.3926,-0.0165 0.4008,-0.0372 0.'
        '3884,-0.0537 0.3678,-0.0579 0.3512,-0.0455 0.3471,-0.0331 0.3554,-0.0165 0.3512,-0.0124 0.3306,-0.02'
        '89 0.3017,-0.1612 0.2851,-0.1777 0.2603,-0.1901 0.2727,-0.2149 0.2686,-0.2355 0.2479,-0.2521ZM0.1818'
        ',-0.0620 0.1860,-0.0579 0.1818,-0.0207 0.1777,-0.0248ZM0.0785,-0.4298 0.0702,-0.4215 0.0702,0.4174 0'
        '.0785,0.4256 0.1033,0.4256 0.1116,0.4174 0.1116,-0.4215 0.1033,-0.4298Z'
    ),
    '513.1/0': (
        'M-0.8310,-0.4366 -0.8486,-0.3873 -0.8486,0.3838 -0.8415,0.4120 -0.8275,0.4401 -0.8063,0.4648 -0.7817'
        ',0.4824 -0.7430,0.4965 0.7430,0.4965 0.7887,0.4754 0.8239,0.4401 0.8380,0.4120 0.8451,0.3838 0.8451,'
        '-0.3838 0.8275,-0.4366 0.7887,-0.4789 0.7359,-0.5000 -0.7394,-0.5000 -0.7641,-0.4930 -0.7958,-0.4754'
        'Z'
    ),
    '513.1/1': (
        'M-0.7782,-0.3979 -0.7817,-0.3873 -0.7817,0.3838 -0.7746,0.4014 -0.7535,0.4225 -0.7324,0.4331 0.7289,'
        '0.4331 0.7500,0.4225 0.7711,0.4014 0.7817,0.3732 0.7817,-0.3768 0.7676,-0.4085 0.7430,-0.4296 0.7148'
        ',-0.4366 -0.7183,-0.4366 -0.7465,-0.4296Z'
    ),
    '532.3/0': (
        'M-0.7380,0.1028 -0.7380,0.1563 -0.7493,0.1648 -0.7549,0.1901 -0.5493,0.1901 -0.5099,0.1958 -0.5099,0'
        '.2803 -0.5746,0.3930 -0.5803,0.4183 -0.5746,0.4465 -0.5606,0.4690 -0.5437,0.4831 -0.5099,0.4944 0.54'
        '37,0.4944 0.5465,0.4972 0.6479,0.4972 0.6479,0.4915 0.6282,0.4887 0.6282,0.4268 0.6085,0.4268 0.6000'
        ',0.4211 0.6000,0.1958 0.6085,0.1901 0.7521,0.1901 0.7521,0.1845 0.6085,0.1845 0.6000,0.1789 0.6000,0'
        '.1366 0.5915,0.1394 0.5915,0.1789 0.5831,0.1845 0.4225,0.1845 0.0451,-0.4690 0.0197,-0.4915 -0.0056,'
        '-0.5000 -0.0394,-0.4972 -0.0732,-0.4746 -0.3887,0.0690 -0.7239,0.0690Z'
    ),
    '532.3/1': (
        'M0.6254,0.4408 0.6000,0.4859 0.6056,0.4915 0.6254,0.4915 0.6310,0.4859 0.6310,0.4465ZM0.4282,0.1817 '
        '0.4225,0.1873 0.5324,0.3732 0.5465,0.4070 0.5465,0.4324 0.5380,0.4549 0.5155,0.4803 0.4958,0.4915 0.'
        '5014,0.4972 0.5380,0.4972 0.5437,0.4915 0.5859,0.4915 0.5915,0.4831 0.5634,0.4296 0.5859,0.4268 0.59'
        '15,0.4211 0.5915,0.1958 0.5859,0.1901 0.4423,0.1901 0.4338,0.1817ZM-0.7352,0.1113 -0.7408,0.1169 -0.'
        '7352,0.1282 -0.7296,0.1225ZM-0.3887,0.0718 -0.4000,0.0662 -0.4113,0.0775 -0.7183,0.0775 -0.7296,0.10'
        '00 -0.7211,0.1169 -0.7296,0.1366 -0.7296,0.1592 -0.7437,0.1704 -0.7465,0.1789 -0.7408,0.1845 -0.4761'
        ',0.1845 -0.4732,0.1873 -0.4761,0.1930 -0.5070,0.1930 -0.5127,0.1986 -0.5127,0.2662 -0.5070,0.2718 -0'
        '.4873,0.2437ZM-0.0141,-0.3704 -0.0254,-0.3620 -0.2817,0.0859 -0.2873,0.0915 -0.3042,0.0915 -0.3099,0'
        '.0972 -0.3099,0.1338 -0.4592,0.3901 -0.4535,0.3958 0.4197,0.3958 0.4254,0.3901ZM-0.0648,0.3676 -0.02'
        '54,0.3000 -0.0085,0.3000 -0.0028,0.3056 0.0310,0.3648 0.0282,0.3704 -0.0620,0.3704ZM0.2254,0.1141 0.'
        '2282,0.1169 0.2113,0.1479 0.2056,0.1535 0.1887,0.1535 0.1859,0.1479 0.2000,0.1225 0.2085,0.1141ZM0.1'
        '887,0.1141 0.1915,0.1197 0.1803,0.1366 0.1775,0.1169ZM-0.1408,-0.1225 -0.1380,-0.1254 0.1014,-0.1254'
        ' 0.1042,-0.1197 -0.0113,0.0803 -0.0197,0.0859Z'
    ),
    '532.3/2': (
        'M0.6225,0.4268 0.5944,0.4239 0.5718,0.4268 0.5662,0.4324 0.5944,0.4859 0.5887,0.4915 0.5944,0.4972 0'
        '.6028,0.4915 0.6000,0.4859 0.6282,0.4324ZM-0.0648,0.3676 -0.0592,0.3732 0.0254,0.3732 0.0310,0.3648 '
        '-0.0028,0.3056 -0.0113,0.2972 -0.0197,0.2972 -0.0310,0.3085ZM-0.7493,0.1817 -0.7549,0.1873 -0.7493,0'
        '.1930 -0.7437,0.1873ZM0.5972,0.1789 0.5887,0.1873 0.5944,0.1958 0.6056,0.1873ZM-0.7437,0.1592 -0.749'
        '3,0.1648 -0.7437,0.1704 -0.7380,0.1648ZM0.2197,0.1141 0.2085,0.1141 0.2000,0.1225 0.1859,0.1479 0.19'
        '15,0.1535 0.2056,0.1535 0.2254,0.1225ZM0.1859,0.1141 0.1746,0.1197 0.1746,0.1282 0.1803,0.1338 0.191'
        '5,0.1197ZM-0.7324,0.1028 -0.7380,0.1085 -0.7324,0.1141 -0.7268,0.1085ZM-0.1352,-0.1282 -0.1408,-0.12'
        '25 -0.0338,0.0634 -0.0169,0.0859 0.1042,-0.1225 0.0986,-0.1282Z'
    ),
    '548.1/0': (
        'M-0.8052,-0.4553 -0.8151,-0.4305 -0.8176,-0.4107 -0.8176,0.4082 -0.8127,0.4355 -0.8027,0.4553 -0.782'
        '9,0.4777 -0.7680,0.4876 -0.7357,0.4975 0.7333,0.4975 0.7655,0.4876 0.7804,0.4777 0.8002,0.4553 0.810'
        '2,0.4355 0.8151,0.4107 0.8151,-0.4132 0.8052,-0.4504 0.7978,-0.4628 0.7705,-0.4876 0.7357,-0.5000 -0'
        '.7382,-0.5000 -0.7730,-0.4876Z'
    ),
    '548.1/1': (
        'M-0.7655,-0.4330 -0.7705,-0.4206 -0.7705,0.4181 -0.7630,0.4330 -0.7531,0.4429 -0.7382,0.4504 -0.7233'
        ',0.4529 0.7208,0.4529 0.7457,0.4454 0.7630,0.4280 0.7680,0.4156 0.7680,-0.4181 0.7605,-0.4355 0.7432'
        ',-0.4504 0.7233,-0.4553 -0.7258,-0.4553 -0.7457,-0.4504Z'
    ),
    '553.2/0': (
        'M-1.8007,-0.3311 -1.8007,0.3243 -1.7872,0.3716 -1.7601,0.4189 -1.7061,0.4662 -1.6318,0.4932 1.6250,0'
        '.4932 1.6993,0.4662 1.7466,0.4257 1.7804,0.3649 1.7939,0.3108 1.7939,-0.3176 1.7804,-0.3716 1.7399,-'
        '0.4392 1.6993,-0.4730 1.6318,-0.5000 -1.6453,-0.5000 -1.7061,-0.4730 -1.7534,-0.4324 -1.7872,-0.3784'
        'Z'
    ),
    '553.2/1': (
        'M-1.6993,-0.3243 -1.6993,0.3176 -1.6858,0.3514 -1.6588,0.3784 -1.6047,0.3986 1.5980,0.3986 1.6520,0.'
        '3784 1.6926,0.3176 1.6926,-0.3243 1.6588,-0.3784 1.6250,-0.3986 1.5912,-0.4054 -1.6047,-0.4054 -1.65'
        '88,-0.3851Z'
    ),
    '573/0': (
        'M-0.7718,-0.4353 -0.7848,-0.3964 -0.7848,0.3932 -0.7718,0.4320 -0.7589,0.4515 -0.7298,0.4773 -0.7039'
        ',0.4903 -0.6715,0.4968 0.6650,0.4968 0.7006,0.4903 0.7265,0.4773 0.7621,0.4417 0.7751,0.4159 0.7816,'
        '0.3803 0.7816,-0.3835 0.7751,-0.4191 0.7621,-0.4450 0.7265,-0.4806 0.7006,-0.4935 0.6683,-0.5000 -0.'
        '6715,-0.5000 -0.6942,-0.4968 -0.7298,-0.4806 -0.7621,-0.4515Z'
    ),
    '573/1': (
        'M-0.7201,-0.4061 -0.7265,-0.3803 -0.7265,0.3770 -0.7201,0.4029 -0.7006,0.4256 -0.6780,0.4353 0.6748,'
        '0.4353 0.6909,0.4288 0.7136,0.4061 0.7233,0.3738 0.7233,-0.3770 0.7201,-0.3964 0.7104,-0.4159 0.6974'
        ',-0.4288 0.6748,-0.4385 -0.6812,-0.4385 -0.7006,-0.4288ZM-0.3220,0.1861 -0.1634,0.0275 -0.0146,0.027'
        '5 -0.0113,0.0307 -0.1019,0.1246 -0.0955,0.1311 0.3058,0.1311 0.3091,0.1343 0.3091,0.2346 0.3058,0.23'
        '79 -0.0987,0.2379 -0.1052,0.2443 -0.0113,0.3382 -0.0146,0.3414 -0.1667,0.3414Z'
    ),
    '573/2': (
        'M-0.0631,0.2896 -0.0599,0.3123 -0.0663,0.3252 -0.0825,0.3382 -0.0146,0.3382ZM0.3058,0.2184 0.2896,0.'
        '2346 0.3058,0.2346ZM-0.3091,0.1764 -0.3188,0.1861 -0.3058,0.1990ZM0.2896,0.1343 0.3058,0.1505 0.3058'
        ',0.1343ZM-0.0793,0.0307 -0.0631,0.0437 -0.0566,0.0566 -0.0566,0.0728 -0.0146,0.0307Z'
    ),
    '575/0': (
        'M-0.5790,-0.4709 -0.5894,-0.4543 -0.5956,-0.4314 -0.5956,0.4314 -0.5915,0.4480 -0.5832,0.4647 -0.562'
        '4,0.4854 -0.5312,0.4979 0.5291,0.4979 0.5541,0.4896 0.5748,0.4730 0.5894,0.4480 0.5936,0.4335 0.5936'
        ',-0.4335 0.5832,-0.4626 0.5644,-0.4834 0.5478,-0.4938 0.5187,-0.5000 -0.5208,-0.5000 -0.5437,-0.4958'
        ' -0.5665,-0.4834Z'
    ),
    '575/1': (
        'M-0.5478,-0.4480 -0.5561,-0.4314 -0.5561,0.4314 -0.5520,0.4418 -0.5395,0.4543 -0.5208,0.4605 0.5187,'
        '0.4605 0.5374,0.4543 0.5499,0.4418 0.5561,0.4252 0.5561,-0.4272 0.5520,-0.4397 0.5395,-0.4543 0.5270'
        ',-0.4605 -0.5291,-0.4605Z'
    ),
    '775/0': (
        'M-0.8578,-0.4594 -0.8734,-0.4188 -0.8734,0.4156 -0.8547,0.4625 -0.8234,0.4875 -0.7984,0.4969 0.7953,'
        '0.4969 0.8297,0.4813 0.8578,0.4500 0.8703,0.4062 0.8672,0.4000 0.8672,-0.4031 0.8703,-0.4062 0.8609,'
        '-0.4469 0.8516,-0.4625 0.8234,-0.4875 0.7922,-0.5000 -0.7953,-0.5000 -0.8328,-0.4844Z'
    ),
    '775/1': (
        'M-0.8172,-0.4313 -0.8234,-0.4188 -0.8203,-0.4094 -0.8234,-0.4062 -0.8234,0.4125 -0.8172,0.4281 -0.80'
        '47,0.4406 -0.7766,0.4500 0.7703,0.4500 0.7984,0.4406 0.8109,0.4281 0.8203,0.4031 0.8203,-0.4031 0.81'
        '09,-0.4313 0.7984,-0.4438 0.7703,-0.4531 -0.7766,-0.4531 -0.7984,-0.4469Z'
    ),
    '783/0': (
        'M-1.2004,-0.4681 -1.2004,0.4645 -1.1933,0.4823 -1.1720,0.4965 1.1684,0.4965 1.1826,0.4894 1.1968,0.4'
        '645 1.1968,-0.4681 1.1897,-0.4858 1.1720,-0.5000 -1.1720,-0.5000 -1.1897,-0.4894Z'
    ),
    '786/0': (
        'M-0.7065,-0.4688 -0.7195,-0.4403 -0.7195,0.4377 -0.7065,0.4662 -0.6883,0.4844 -0.6597,0.4974 0.6545,'
        '0.4974 0.6883,0.4818 0.7065,0.4610 0.7169,0.4325 0.7169,-0.4351 0.7065,-0.4636 0.6857,-0.4870 0.6545'
        ',-0.5000 -0.6597,-0.5000 -0.6857,-0.4896Z'
    ),
    '786/1': (
        'M-0.6779,-0.4377 -0.6805,-0.4273 -0.6805,0.4247 -0.6753,0.4403 -0.6649,0.4506 -0.6416,0.4584 0.6390,'
        '0.4584 0.6571,0.4532 0.6727,0.4377 0.6779,0.4195 0.6779,-0.4221 0.6727,-0.4403 0.6519,-0.4584 -0.654'
        '5,-0.4584 -0.6649,-0.4532Z'
    ),
    '787/0': (
        'M-0.5000,-1.0808 -0.5000,1.0758 0.4949,1.0758 0.4949,-1.0808Z'
    ),
    '787/1': (
        'M0.3384,0.7121 0.2778,0.7121 0.2475,0.7222 0.1970,0.7727 0.1919,0.7929 0.1970,0.8333 0.2374,0.8788 0'
        '.3131,0.8939 0.3434,0.9141 0.3434,0.9293 0.3182,0.9495 0.2626,0.9444 0.2172,0.9091 0.1667,0.9545 0.1'
        '970,0.9848 0.2323,1.0051 0.2778,1.0152 0.3586,1.0051 0.3788,0.9949 0.4141,0.9495 0.4192,0.9293 0.414'
        '1,0.8889 0.3788,0.8485 0.3485,0.8333 0.2778,0.8182 0.2677,0.8081 0.2677,0.7929 0.2879,0.7778 0.3232,'
        '0.7778 0.3788,0.8030 0.4242,0.7626 0.3889,0.7323ZM-0.0354,0.7121 -0.0859,0.7374 -0.1263,0.7879 -0.14'
        '14,0.8333 -0.1414,0.8838 -0.1162,0.9545 -0.0758,0.9949 -0.0404,1.0101 0.0101,1.0152 0.0707,0.9949 0.'
        '1111,0.9545 0.1364,0.8889 0.1364,0.8384 0.1313,0.8131 0.1061,0.7626 0.0808,0.7374 0.0253,0.7121ZM-0.'
        '0253,0.7778 0.0303,0.7828 0.0556,0.8081 0.0657,0.8434 0.0657,0.8838 0.0505,0.9242 0.0354,0.9394 0.01'
        '01,0.9495 -0.0152,0.9495 -0.0404,0.9394 -0.0556,0.9242 -0.0707,0.8838 -0.0707,0.8434 -0.0606,0.8081Z'
        'M-0.3232,0.7121 -0.3586,0.7222 -0.3990,0.7576 -0.4091,0.7828 -0.4091,0.8283 -0.3737,0.8737 -0.2677,0'
        '.9040 -0.2626,0.9343 -0.2828,0.9495 -0.3232,0.9495 -0.3889,0.9141 -0.4394,0.9545 -0.4141,0.9798 -0.3'
        '737,1.0051 -0.3232,1.0152 -0.2626,1.0101 -0.2273,0.9949 -0.2020,0.9697 -0.1869,0.9343 -0.1919,0.8889'
        ' -0.2323,0.8434 -0.3283,0.8182 -0.3384,0.7980 -0.3182,0.7778 -0.2778,0.7778 -0.2273,0.8030 -0.1818,0'
        '.7626 -0.2071,0.7374 -0.2475,0.7172ZM-0.0758,-1.0253 -0.2071,-1.0051 -0.2374,-0.9697 -0.2374,-0.9394'
        ' -0.1515,-0.6313 -0.1263,-0.6061 -0.0909,-0.6010 -0.0101,-0.6465 0.0606,-0.6364 0.0859,-0.6061 0.096'
        '0,-0.5556 0.0960,0.0556 0.0707,0.1465 0.0303,0.2222 0.0051,0.2525 -0.0909,0.1869 -0.1212,0.1869 -0.1'
        '465,0.2020 -0.1768,0.1970 -0.2020,0.2273 -0.3030,0.4040 -0.3131,0.4343 -0.2929,0.4596 -0.2879,0.5000'
        ' -0.2626,0.5253 -0.1364,0.5808 -0.0253,0.5859 0.0404,0.5606 0.1061,0.5051 0.1869,0.3586 0.2071,0.298'
        '0 0.2525,0.1061 0.2727,-0.0354 0.2778,-0.3434 0.2576,-0.5253 0.2323,-0.6515 0.1869,-0.8081 0.1414,-0'
        '.9040 0.1162,-0.9444 0.0606,-0.9949 0.0051,-1.0202Z'
    ),
    '787/2': (
        'M-0.3889,0.8586 -0.3838,0.8990 -0.3939,0.9192 -0.3838,0.9091 -0.3737,0.9242 -0.3232,0.9495 -0.2828,0'
        '.9495 -0.2626,0.9343 -0.2677,0.9040 -0.3333,0.8838 -0.3535,0.8838ZM0.2677,0.7929 0.2677,0.8081 0.277'
        '8,0.8182 0.3636,0.8384 0.3889,0.8586 0.3788,0.8434 0.3788,0.8081 0.3889,0.7929 0.3687,0.8030 0.3232,'
        '0.7778 0.2879,0.7778ZM0.1061,0.7677 0.1313,0.8131 0.1364,0.8384 0.1364,0.8889 0.1263,0.9242 0.1061,0'
        '.9596 0.1364,0.9495 0.1717,0.9596 0.1667,0.9495 0.2172,0.9091 0.2525,0.9394 0.2828,0.9495 0.3182,0.9'
        '495 0.3434,0.9293 0.3434,0.9141 0.3283,0.8990 0.2374,0.8788 0.2020,0.8434 0.1919,0.8131 0.2020,0.767'
        '7 0.1818,0.7828 0.1566,0.7879 0.1263,0.7828ZM-0.1162,0.9495 -0.1364,0.9091 -0.1414,0.8333 -0.1263,0.'
        '7879 -0.1010,0.7576 -0.1414,0.7727 -0.1818,0.7626 -0.2273,0.8030 -0.2778,0.7778 -0.3182,0.7778 -0.33'
        '33,0.7879 -0.3384,0.8081 -0.3283,0.8182 -0.2424,0.8384 -0.1970,0.8788 -0.1869,0.9040 -0.1869,0.9343 '
        '-0.2020,0.9646 -0.1869,0.9495 -0.1515,0.9394ZM0.0354,0.2121 0.0152,0.2273 -0.0101,0.2323 -0.0404,0.2'
        '222 0.0051,0.2525Z'
    ),
    '788/0': (
        'M-0.4370,-0.9803 -0.4685,-0.9567 -0.4843,-0.9331 -0.5000,-0.8858 -0.5000,0.8819 -0.4843,0.9291 -0.46'
        '85,0.9528 -0.4370,0.9764 -0.4094,0.9882 -0.3819,0.9921 0.3740,0.9921 0.4331,0.9764 0.4803,0.9291 0.4'
        '961,0.8780 0.4961,-0.8819 0.4843,-0.9252 0.4449,-0.9724 0.4134,-0.9882 0.3819,-0.9961 -0.3898,-0.996'
        '1Z'
    ),
    '788/1': (
        'M-0.0157,0.1969 -0.0276,0.2008 -0.0472,0.2205 -0.0591,0.2520 -0.0591,0.2795 -0.0472,0.3150 -0.0315,0'
        '.3307 -0.0157,0.3386 0.0118,0.3386 0.0433,0.3150 0.0551,0.2874 0.0551,0.2520 0.0433,0.2205 0.0236,0.'
        '2008ZM-0.3937,-0.9370 -0.4094,-0.9291 -0.4331,-0.9055 -0.4409,-0.8898 -0.4409,0.8858 -0.4291,0.9055 '
        '-0.3937,0.9331 0.3898,0.9331 0.4252,0.9055 0.4370,0.8780 0.4370,-0.8819 0.4331,-0.8976 0.4055,-0.929'
        '1 0.3898,-0.9370ZM0.3071,0.6654 0.3071,0.6732 0.1535,0.8268 0.0039,0.8268 0.0000,0.8228 0.0945,0.728'
        '3 0.0866,0.7205 -0.3071,0.7205 -0.3110,0.7165 -0.3110,0.6220 -0.3071,0.6181 0.0827,0.6181 0.0906,0.6'
        '102 0.0000,0.5197 0.0039,0.5157 0.1535,0.5157ZM0.2165,0.1535 0.2756,0.1575 0.3110,0.1732 0.3268,0.18'
        '90 0.2913,0.2205 0.2795,0.2087 0.2480,0.1969 0.2244,0.1969 0.2047,0.2165 0.2047,0.2244 0.2165,0.2362'
        ' 0.2795,0.2520 0.3150,0.2795 0.3189,0.3307 0.3110,0.3504 0.2835,0.3740 0.2480,0.3819 0.1969,0.3780 0'
        '.1654,0.3661 0.1339,0.3386 0.1654,0.3110 0.1732,0.3110 0.1969,0.3307 0.2165,0.3386 0.2598,0.3346 0.2'
        '717,0.3189 0.2717,0.3071 0.2598,0.2953 0.1929,0.2795 0.1772,0.2717 0.1575,0.2441 0.1535,0.2323 0.157'
        '5,0.1969 0.1811,0.1693ZM-0.0236,0.1535 0.0079,0.1535 0.0512,0.1654 0.0827,0.1969 0.1024,0.2441 0.102'
        '4,0.2913 0.0906,0.3268 0.0630,0.3622 0.0197,0.3819 -0.0157,0.3819 -0.0591,0.3661 -0.0866,0.3386 -0.1'
        '024,0.3071 -0.1024,0.2283 -0.0945,0.2087 -0.0551,0.1654ZM-0.2677,0.1575 -0.2520,0.1535 -0.1929,0.157'
        '5 -0.1614,0.1732 -0.1457,0.1890 -0.1772,0.2205 -0.1969,0.2047 -0.2244,0.1969 -0.2441,0.1969 -0.2677,'
        '0.2165 -0.2677,0.2244 -0.2559,0.2362 -0.1890,0.2520 -0.1575,0.2795 -0.1496,0.2992 -0.1496,0.3268 -0.'
        '1575,0.3465 -0.1890,0.3740 -0.2244,0.3819 -0.2756,0.3780 -0.3071,0.3661 -0.3386,0.3386 -0.3031,0.311'
        '0 -0.2559,0.3386 -0.2244,0.3386 -0.2008,0.3228 -0.2008,0.3031 -0.2087,0.2953 -0.2874,0.2756 -0.3150,'
        '0.2402 -0.3150,0.2047 -0.3031,0.1811ZM-0.2283,-0.8110 -0.1850,-0.8268 -0.1378,-0.8228 -0.0906,-0.803'
        '1 -0.0512,-0.7756 0.0394,-0.6890 0.1024,-0.6142 0.1614,-0.5276 0.1969,-0.4646 0.2677,-0.2992 0.2992,'
        '-0.1693 0.2953,-0.0512 0.2717,-0.0118 0.2362,0.0197 0.1811,0.0354 0.1024,0.0394 0.0669,0.0079 0.0669'
        ',-0.1457 0.0787,-0.1496 0.1063,-0.1772 0.1732,-0.1732 0.1811,-0.1811 0.1811,-0.2598 0.1693,-0.2992 0'
        '.0079,-0.5866 -0.0433,-0.6457 -0.0669,-0.6457 -0.0945,-0.6339 -0.1260,-0.5827 -0.1614,-0.5787 -0.303'
        '1,-0.7205 -0.3071,-0.7441 -0.2992,-0.7598Z'
    ),
    '788/2': (
        'M0.1063,0.8268 0.0906,0.8268 0.0669,0.8071 0.0591,0.7913 0.0591,0.7677 0.0669,0.7559 -0.0039,0.8268Z'
        'M-0.3110,0.6890 -0.3110,0.7205 -0.2677,0.7205 -0.2913,0.7165 -0.3071,0.7008ZM0.2835,0.6457 0.2913,0.'
        '6575 0.2913,0.6850 0.2835,0.6969 0.3071,0.6732 0.3071,0.6654ZM-0.3110,0.6496 -0.3071,0.6378 -0.2913,'
        '0.6220 -0.2677,0.6181 -0.3110,0.6181ZM-0.0039,0.5157 0.0669,0.5866 0.0591,0.5748 0.0591,0.5512 0.066'
        '9,0.5354 0.0827,0.5197 0.1063,0.5157ZM0.2165,0.1535 0.1811,0.1693 0.1575,0.1969 0.1535,0.2323 0.1772'
        ',0.2717 0.1929,0.2795 0.2520,0.2913 0.2717,0.3071 0.2717,0.3189 0.2598,0.3346 0.2165,0.3386 0.1969,0'
        '.3307 0.1732,0.3110 0.1654,0.3110 0.1339,0.3386 0.1535,0.3583 0.1811,0.3740 0.2165,0.3819 0.2480,0.3'
        '819 0.2835,0.3740 0.3110,0.3504 0.3189,0.3307 0.3189,0.2874 0.2874,0.2559 0.2165,0.2362 0.2047,0.224'
        '4 0.2047,0.2165 0.2244,0.1969 0.2480,0.1969 0.2795,0.2087 0.2913,0.2205 0.3268,0.1890 0.3110,0.1732 '
        '0.2756,0.1575ZM-0.0236,0.1535 -0.0551,0.1654 -0.0945,0.2087 -0.1024,0.2283 -0.1024,0.3071 -0.0866,0.'
        '3386 -0.0591,0.3661 -0.0354,0.3780 0.0197,0.3819 0.0630,0.3622 0.0906,0.3268 0.1024,0.2913 0.1024,0.'
        '2441 0.0827,0.1969 0.0512,0.1654 0.0079,0.1535ZM-0.0157,0.1969 0.0236,0.2008 0.0433,0.2205 0.0551,0.'
        '2520 0.0512,0.2992 0.0433,0.3150 0.0118,0.3386 -0.0157,0.3386 -0.0315,0.3307 -0.0472,0.3150 -0.0591,'
        '0.2795 -0.0591,0.2520 -0.0472,0.2205 -0.0276,0.2008ZM-0.2520,0.1535 -0.2835,0.1654 -0.3031,0.1811 -0'
        '.3150,0.2047 -0.3150,0.2402 -0.3031,0.2638 -0.2874,0.2756 -0.2087,0.2953 -0.2008,0.3031 -0.2008,0.32'
        '28 -0.2244,0.3386 -0.2559,0.3386 -0.3031,0.3110 -0.3386,0.3386 -0.3189,0.3583 -0.2913,0.3740 -0.2559'
        ',0.3819 -0.2244,0.3819 -0.1890,0.3740 -0.1654,0.3583 -0.1496,0.3268 -0.1496,0.2992 -0.1575,0.2795 -0'
        '.1890,0.2520 -0.2559,0.2362 -0.2677,0.2244 -0.2677,0.2165 -0.2441,0.1969 -0.2244,0.1969 -0.1969,0.20'
        '47 -0.1772,0.2205 -0.1457,0.1890 -0.1614,0.1732 -0.1929,0.1575ZM-0.1142,-0.5984 -0.1299,-0.5866 -0.1'
        '496,-0.5827 -0.1732,-0.5906 -0.1614,-0.5787 -0.1339,-0.5787ZM0.0157,-0.7126 0.0236,-0.7008 0.0236,-0'
        '.6772 0.0157,-0.6614 -0.0079,-0.6417 -0.0354,-0.6378 0.0039,-0.5906 0.0039,-0.6063 0.0276,-0.6378 0.'
        '0551,-0.6457 0.0866,-0.6339ZM-0.2835,-0.7717 -0.2992,-0.7598 -0.3071,-0.7441 -0.3031,-0.7205 -0.2913'
        ',-0.7087 -0.2992,-0.7205 -0.2992,-0.7480Z'
    ),
    '883/0': (
        'M-0.9881,-0.4728 -0.9915,-0.4626 -0.9915,0.4592 -0.9813,0.4796 -0.9575,0.4966 0.9507,0.4966 0.9677,0'
        '.4898 0.9847,0.4660 0.9881,0.4524 0.9881,-0.4592 0.9779,-0.4830 0.9541,-0.5000 -0.9575,-0.5000 -0.97'
        '11,-0.4932Z'
    ),
    '884/0': (
        'M-0.4875,-0.5025 -0.5000,-0.4875 -0.5000,-0.3454 -0.4950,-0.3429 -0.4950,-0.3379 -0.5000,-0.3354 -0.'
        '5000,0.2781 -0.4950,0.2805 -0.4950,0.2855 -0.5000,0.2880 -0.5000,0.4850 -0.4975,0.4900 -0.4825,0.502'
        '5 0.3030,0.5025 0.3055,0.5000 0.3105,0.5025 0.4800,0.5025 0.4850,0.5000 0.4975,0.4850 0.4975,-0.4875'
        ' 0.4950,-0.4925 0.4800,-0.5050 -0.4825,-0.5050Z'
    ),
    '884/1': (
        'M-0.3878,0.2232 -0.3928,0.2182 -0.4875,0.2706 -0.4975,0.2805 -0.4925,0.2855ZM0.4252,0.0586 0.4202,0.'
        '0636 0.4227,0.0835 0.4177,0.0910 0.4202,0.1035 0.4152,0.1085 0.4102,0.1384 0.4127,0.1484 0.4077,0.15'
        '34 0.4102,0.1633 0.4052,0.1683 0.4077,0.1733 0.4027,0.1783 0.3953,0.2107 0.3978,0.2157 0.3928,0.2207'
        ' 0.3953,0.2257 0.3878,0.2382 0.3853,0.2481 0.3878,0.2531 0.3803,0.2656 0.3728,0.2905 0.3753,0.2955 0'
        '.3703,0.3005 0.3603,0.3304 0.3628,0.3354 0.3579,0.3404 0.3603,0.3429 0.3554,0.3479 0.3579,0.3504 0.3'
        '529,0.3554 0.3404,0.3928 0.3429,0.3953 0.3329,0.4152 0.3354,0.4177 0.3254,0.4352 0.3279,0.4377 0.322'
        '9,0.4426 0.3254,0.4451 0.3180,0.4551 0.3130,0.4701 0.3155,0.4726 0.3105,0.4776 0.3130,0.4800 0.3030,'
        '0.4975 0.3080,0.5025 0.3180,0.4850 0.3155,0.4825 0.3204,0.4776 0.3180,0.4751 0.3254,0.4651 0.3304,0.'
        '4501 0.3279,0.4476 0.3329,0.4426 0.3304,0.4401 0.3404,0.4227 0.3379,0.4202 0.3479,0.4002 0.3454,0.39'
        '78 0.3529,0.3878 0.3628,0.3579 0.3603,0.3529 0.3653,0.3479 0.3628,0.3454 0.3678,0.3404 0.3653,0.3379'
        ' 0.3703,0.3329 0.3803,0.3030 0.3778,0.2980 0.3828,0.2930 0.3928,0.2606 0.3903,0.2556 0.3953,0.2506 0'
        '.4002,0.2332 0.3978,0.2282 0.4027,0.2232 0.4002,0.2182 0.4077,0.2057 0.4127,0.1833 0.4102,0.1758 0.4'
        '152,0.1708 0.4127,0.1633 0.4177,0.1584 0.4152,0.1509 0.4202,0.1459 0.4252,0.1185 0.4227,0.1060 0.427'
        '7,0.1010 0.4252,0.0860 0.4302,0.0810 0.4302,0.0636ZM0.2307,0.0536 0.2132,0.0561 0.2007,0.0686 0.1958'
        ',0.0810 0.1983,0.0935 0.2107,0.1160 0.2057,0.1209 0.1858,0.1259 0.1733,0.1334 0.1658,0.1434 0.1359,0'
        '.2805 0.1259,0.2880 0.1234,0.2955 0.1085,0.2955 0.1010,0.2905 0.1085,0.2756 0.1085,0.2631 0.0960,0.2'
        '506 0.0810,0.2506 0.0686,0.2656 0.0686,0.2756 0.0761,0.2830 0.0761,0.2905 0.0511,0.3155 0.0461,0.370'
        '3 0.0561,0.3853 0.0661,0.3803 0.0611,0.3728 0.0611,0.3603 0.0661,0.3379 0.0711,0.3329 0.0761,0.3504 '
        '0.0711,0.3778 0.0736,0.4526 0.0786,0.4576 0.0860,0.4501 0.0935,0.4077 0.0985,0.4027 0.1035,0.4052 0.'
        '1035,0.4501 0.1135,0.4601 0.1185,0.4551 0.1160,0.4451 0.1209,0.4277 0.1209,0.4127 0.1334,0.3978 0.13'
        '34,0.3853 0.1160,0.3180 0.1384,0.3080 0.1584,0.2930 0.1534,0.2830 0.1908,0.1908 0.1933,0.1933 0.1908'
        ',0.3204 0.2032,0.4451 0.1933,0.4601 0.1983,0.4651 0.2232,0.4451 0.2257,0.3579 0.2357,0.3055 0.2431,0'
        '.3703 0.2406,0.4476 0.2581,0.4626 0.2631,0.4576 0.2581,0.4526 0.2731,0.3504 0.2731,0.3130 0.2756,0.3'
        '105 0.2756,0.2756 0.2656,0.1908 0.2681,0.1883 0.2731,0.1933 0.2855,0.2207 0.2905,0.2431 0.2905,0.278'
        '1 0.2855,0.2905 0.2930,0.3005 0.3030,0.3005 0.3105,0.2905 0.3080,0.2855 0.3105,0.2282 0.2955,0.1484 '
        '0.2756,0.1309 0.2606,0.1234 0.2456,0.1209 0.2406,0.1160 0.2531,0.0935 0.2556,0.0810 0.2506,0.0686ZM0'
        '.4277,0.0187 0.4227,0.0237 0.4227,0.0337 0.4277,0.0387 0.4327,0.0337 0.4327,0.0237ZM-0.0287,0.0062 -'
        '0.0362,-0.0012 -0.0461,0.0037 -0.0910,0.0062 -0.1110,0.0162 -0.1484,0.0486 -0.1658,0.0461 -0.1883,0.'
        '0262 -0.1958,-0.0262 -0.2057,-0.0337 -0.2057,-0.0387 -0.1958,-0.0461 -0.1933,-0.0611 -0.1958,-0.0711'
        ' -0.2057,-0.0810 -0.2207,-0.0786 -0.2282,-0.0661 -0.2257,-0.0461 -0.2207,-0.0387 -0.2357,-0.0237 -0.'
        '2481,0.0137 -0.2481,0.0561 -0.2456,0.0586 -0.2481,0.0711 -0.2805,0.0611 -0.3155,0.0636 -0.3379,0.073'
        '6 -0.3529,0.0761 -0.3753,0.0736 -0.3878,0.0786 -0.4002,0.0910 -0.4102,0.1085 -0.4177,0.1584 -0.4327,'
        '0.1733 -0.4227,0.1808 -0.4127,0.1783 -0.3903,0.1534 -0.3853,0.1409 -0.3853,0.1110 -0.3778,0.0935 -0.'
        '3653,0.0835 -0.3554,0.0860 -0.3628,0.1110 -0.3603,0.1409 -0.3529,0.1559 -0.3529,0.1758 -0.3678,0.188'
        '3 -0.3678,0.2456 -0.3753,0.2556 -0.3853,0.2606 -0.3853,0.2756 -0.3803,0.2805 -0.3703,0.2781 -0.3579,'
        '0.2656 -0.3603,0.2556 -0.3554,0.2182 -0.3454,0.2057 -0.3454,0.1983 -0.3105,0.1808 -0.3080,0.1883 -0.'
        '3155,0.2007 -0.3005,0.2307 -0.2955,0.2631 -0.2805,0.2706 -0.2805,0.2805 -0.2731,0.2880 -0.2606,0.288'
        '0 -0.2556,0.2830 -0.2606,0.2731 -0.2855,0.2506 -0.2930,0.2032 -0.2830,0.1808 -0.2855,0.1708 -0.2706,'
        '0.1584 -0.2631,0.1633 -0.2257,0.1733 -0.1733,0.1733 -0.1484,0.1658 -0.1459,0.1683 -0.1459,0.1958 -0.'
        '1584,0.2182 -0.1559,0.2406 -0.1683,0.2631 -0.1608,0.2706 -0.1633,0.2830 -0.1584,0.2880 -0.1484,0.288'
        '0 -0.1384,0.2805 -0.1509,0.2631 -0.1534,0.2431 -0.1309,0.2132 -0.1234,0.1983 -0.1209,0.1808 -0.1135,'
        '0.1708 -0.1085,0.1708 -0.0835,0.1908 -0.0586,0.2182 -0.0461,0.2506 -0.0561,0.2631 -0.0461,0.2781 -0.'
        '0387,0.2706 -0.0312,0.2481 -0.0461,0.2207 -0.0511,0.1983 -0.0885,0.1608 -0.0910,0.1459 -0.0860,0.135'
        '9 -0.0860,0.1160 -0.0711,0.0910 -0.0636,0.0661 -0.0436,0.0786 -0.0436,0.0910 -0.0387,0.0960 -0.0362,'
        '0.0935 -0.0287,0.0985 -0.0187,0.0860 -0.0262,0.0561 -0.0237,0.0312 -0.0312,0.0137ZM-0.1933,0.0461 -0'
        '.1883,0.0436 -0.1658,0.0586 -0.1808,0.0686ZM-0.1633,-0.1933 -0.1683,-0.1883 -0.1633,-0.1833 -0.1608,'
        '-0.1858 -0.1559,-0.1808 -0.1534,-0.1833 -0.1434,-0.1758 -0.1060,-0.1633 -0.0511,-0.1334 -0.0237,-0.1'
        '085 -0.0112,-0.0860 -0.0112,-0.0611 -0.0262,-0.0312 -0.0212,-0.0237 -0.0112,-0.0362 -0.0012,-0.0636 '
        '-0.0012,-0.0835 -0.0112,-0.1060 -0.0411,-0.1359 -0.0636,-0.1509 -0.1085,-0.1733 -0.1484,-0.1883 -0.1'
        '509,-0.1858 -0.1559,-0.1908 -0.1584,-0.1883ZM-0.1808,-0.1983 -0.1858,-0.1933 -0.1808,-0.1883 -0.1758'
        ',-0.1933ZM-0.1983,-0.2032 -0.2032,-0.1983 -0.1983,-0.1933 -0.1933,-0.1983ZM-0.2606,-0.2132 -0.2556,-'
        '0.2082 -0.2506,-0.2107 -0.2456,-0.2057 -0.2406,-0.2082 -0.2257,-0.2007 -0.2207,-0.2057 -0.2257,-0.21'
        '07 -0.2307,-0.2082 -0.2357,-0.2132 -0.2406,-0.2107 -0.2556,-0.2182ZM0.2731,-0.2232 0.2681,-0.2182 0.'
        '2756,-0.2107 0.2880,-0.2057 0.3304,-0.1758 0.3703,-0.1359 0.3878,-0.1110 0.4102,-0.0611 0.4152,-0.03'
        '37 0.4202,-0.0287 0.4177,-0.0162 0.4227,-0.0112 0.4202,0.0012 0.4252,0.0062 0.4302,0.0012 0.4302,-0.'
        '0087 0.4252,-0.0137 0.4277,-0.0237 0.4227,-0.0287 0.4252,-0.0411 0.4127,-0.0810 0.3953,-0.1160 0.377'
        '8,-0.1409 0.3379,-0.1808ZM-0.4327,-0.2431 -0.4277,-0.2382 -0.4202,-0.2382 -0.4152,-0.2431 -0.4077,-0'
        '.2357 -0.4002,-0.2406 -0.4052,-0.2456 -0.4127,-0.2406 -0.4202,-0.2481 -0.4277,-0.2481ZM-0.4726,-0.24'
        '81 -0.4676,-0.2431 -0.4601,-0.2431 -0.4551,-0.2481 -0.4476,-0.2406 -0.4377,-0.2456 -0.4426,-0.2506 -'
        '0.4526,-0.2456 -0.4601,-0.2531 -0.4676,-0.2531ZM-0.4975,-0.2506 -0.4925,-0.2456 -0.4825,-0.2456 -0.4'
        '776,-0.2506 -0.4825,-0.2556 -0.4925,-0.2556ZM0.3204,-0.1160 0.3130,-0.1309 0.3005,-0.1434 0.2830,-0.'
        '1509 0.2556,-0.1484 0.2431,-0.1658 0.2556,-0.1758 0.2581,-0.1808 0.2282,-0.2606 0.2182,-0.2706 0.210'
        '7,-0.2706 0.1234,-0.2157 0.1135,-0.2057 0.1135,-0.2007 0.1259,-0.1908 0.1160,-0.1534 0.1110,-0.1484 '
        '0.0860,-0.1509 0.0636,-0.1384 0.0511,-0.1209 0.0486,-0.0935 0.0586,-0.0736 0.0686,-0.0636 0.0835,-0.'
        '0561 0.1085,-0.0561 0.1234,-0.0636 0.1359,-0.0761 0.1434,-0.0910 0.1409,-0.1209 0.1234,-0.1434 0.128'
        '4,-0.1484 0.1833,-0.1085 0.1883,-0.0935 0.1758,-0.0835 0.1808,-0.0761 0.2082,-0.0860 0.2157,-0.0985 '
        '0.2232,-0.0985 0.2307,-0.0810 0.2506,-0.0611 0.2631,-0.0561 0.2855,-0.0561 0.3005,-0.0636 0.3180,-0.'
        '0835ZM0.2506,-0.1309 0.2631,-0.1110 0.2606,-0.1085 0.2406,-0.1110ZM0.2681,-0.1384 0.2930,-0.1334 0.3'
        '030,-0.1234 0.3080,-0.1110 0.3055,-0.0885 0.2930,-0.0736 0.2805,-0.0686 0.2656,-0.0686 0.2456,-0.081'
        '0 0.2406,-0.0910 0.2431,-0.0985 0.2731,-0.0985 0.2781,-0.1035 0.2631,-0.1309ZM0.0910,-0.1384 0.1010,'
        '-0.1384 0.1110,-0.1334 0.1035,-0.1160 0.0910,-0.1035 0.0960,-0.0985 0.1035,-0.1010 0.1160,-0.1135 0.'
        '1209,-0.1284 0.1309,-0.1110 0.1309,-0.0960 0.1259,-0.0835 0.1160,-0.0736 0.1035,-0.0686 0.0885,-0.06'
        '86 0.0736,-0.0761 0.0611,-0.0985 0.0611,-0.1085 0.0686,-0.1259ZM0.2307,-0.1658 0.2456,-0.1409 0.2307'
        ',-0.1259 0.2282,-0.1135 0.2232,-0.1085 0.2107,-0.1085 0.2082,-0.1110ZM0.2157,-0.1658 0.2182,-0.1633 '
        '0.2032,-0.1259 0.1933,-0.1434 0.1908,-0.1608 0.1983,-0.1658ZM0.1284,-0.1633 0.1334,-0.1683 0.1584,-0'
        '.1683 0.1633,-0.1633 0.1733,-0.1334 0.1708,-0.1309 0.1309,-0.1584ZM0.1883,-0.2357 0.2057,-0.1908 0.1'
        '733,-0.1858 0.1658,-0.1783 0.1359,-0.1783 0.1334,-0.1808 0.1384,-0.1933 0.1359,-0.2007ZM-0.0012,-0.2'
        '980 0.0037,-0.2930 0.0137,-0.2955 0.0187,-0.2905 0.0262,-0.2930 0.0312,-0.2880 0.0387,-0.2905 0.0436'
        ',-0.2855 0.0511,-0.2880 0.0561,-0.2830 0.0611,-0.2855 0.0686,-0.2805 0.0761,-0.2830 0.0910,-0.2756 0'
        '.0985,-0.2781 0.1035,-0.2731 0.1085,-0.2756 0.1135,-0.2706 0.1185,-0.2731 0.1234,-0.2681 0.1284,-0.2'
        '706 0.1409,-0.2631 0.1509,-0.2681 0.1459,-0.2731 0.1359,-0.2756 0.1309,-0.2731 0.1259,-0.2781 0.1209'
        ',-0.2756 0.1160,-0.2805 0.1110,-0.2781 0.0960,-0.2855 0.0885,-0.2830 0.0835,-0.2880 0.0761,-0.2855 0'
        '.0711,-0.2905 0.0636,-0.2880 0.0486,-0.2955 0.0411,-0.2930 0.0362,-0.2980 0.0287,-0.2955 0.0237,-0.3'
        '005 0.0137,-0.2980 0.0037,-0.3030ZM0.1908,-0.3105 0.1783,-0.3055 0.1683,-0.2930 0.1708,-0.2781 0.185'
        '8,-0.2656 0.1983,-0.2681 0.2107,-0.2805 0.2082,-0.2980 0.1983,-0.3080ZM-0.4202,-0.3354 -0.4152,-0.33'
        '04 -0.3978,-0.3304 -0.3928,-0.3354 -0.3978,-0.3404 -0.4152,-0.3404ZM-0.4676,-0.3379 -0.4626,-0.3329 '
        '-0.4426,-0.3329 -0.4377,-0.3379 -0.4426,-0.3429 -0.4626,-0.3429ZM-0.4925,-0.3454 -0.4975,-0.3404 -0.'
        '4900,-0.3354 -0.4850,-0.3404ZM-0.3529,-0.3254 -0.3529,-0.2880 -0.3454,-0.2781 -0.3404,-0.2830 -0.335'
        '4,-0.3005 -0.3229,-0.3105 -0.3155,-0.3080 -0.3329,-0.2930 -0.3354,-0.2706 -0.3229,-0.2556 -0.3105,-0'
        '.2506 -0.2930,-0.2556 -0.2830,-0.2656 -0.2805,-0.2880 -0.2955,-0.3055 -0.3155,-0.3080 -0.3180,-0.310'
        '5 -0.3155,-0.3130 -0.2980,-0.3130 -0.2855,-0.3055 -0.2706,-0.2781 -0.1359,-0.2781 -0.1284,-0.2880 -0'
        '.1234,-0.2681 -0.1085,-0.2531 -0.0985,-0.2506 -0.0860,-0.2531 -0.0711,-0.2681 -0.0686,-0.2855 -0.073'
        '6,-0.2955 -0.0910,-0.3080 -0.1035,-0.3080 -0.1135,-0.3030 -0.1259,-0.2855 -0.1284,-0.2930 -0.1135,-0'
        '.3105 -0.0885,-0.3130 -0.0786,-0.3080 -0.0686,-0.2980 -0.0586,-0.2781 -0.0362,-0.2781 -0.0237,-0.285'
        '5 -0.0237,-0.3279 -0.0486,-0.3404 -0.0935,-0.3878 -0.1234,-0.4027 -0.2107,-0.4027 -0.2307,-0.3853 -0'
        '.2481,-0.3554 -0.2581,-0.3454 -0.3429,-0.3354ZM-0.1035,-0.2955 -0.0910,-0.2955 -0.0810,-0.2855 -0.08'
        '35,-0.2706 -0.0935,-0.2631 -0.1060,-0.2656 -0.1135,-0.2756 -0.1135,-0.2830ZM-0.3130,-0.2955 -0.3030,'
        '-0.2955 -0.2930,-0.2880 -0.2930,-0.2731 -0.3055,-0.2631 -0.3155,-0.2656 -0.3229,-0.2731 -0.3229,-0.2'
        '880ZM-0.2406,-0.3529 -0.2157,-0.3878 -0.1608,-0.3878 -0.1584,-0.3853 -0.1185,-0.3878 -0.0835,-0.3504'
        ' -0.0860,-0.3479 -0.1534,-0.3479 -0.1559,-0.3504 -0.1608,-0.3479 -0.2382,-0.3479Z'
    ),
    '884/2': (
        'M0.3155,0.4651 0.3055,0.4726 0.3080,0.4875ZM0.0985,0.4027 0.0935,0.4077 0.0835,0.4526 0.0935,0.4501 '
        '0.1085,0.4551 0.1035,0.4501 0.1035,0.4027ZM0.0711,0.3304 0.0636,0.3454 0.0611,0.3728 0.0661,0.3803 0'
        '.0611,0.3853 0.0711,0.3953 0.0736,0.4027 0.0711,0.3778 0.0761,0.3504ZM0.1334,0.3080 0.1160,0.3180 0.'
        '1209,0.3404 0.1209,0.3254ZM0.2357,0.2930 0.2257,0.3579 0.2257,0.4227 0.2207,0.4476 0.2307,0.4451 0.2'
        '406,0.4476 0.2431,0.4227 0.2431,0.3703ZM0.0711,0.2781 0.0711,0.2905 0.0661,0.2980 0.0761,0.2905 0.07'
        '61,0.2830ZM0.1434,0.2431 0.1284,0.2581 0.1160,0.2606 0.1035,0.2581 0.1085,0.2631 0.1085,0.2756 0.101'
        '0,0.2855 0.1010,0.2930 0.1085,0.2955 0.1284,0.2930 0.1259,0.2880 0.1359,0.2805ZM0.2656,0.1833 0.2756'
        ',0.2756 0.2731,0.3204 0.2756,0.3130 0.2905,0.3005 0.2855,0.2905 0.2905,0.2781 0.2905,0.2431 0.2805,0'
        '.2082ZM-0.3080,0.1808 -0.3155,0.1808 -0.3454,0.1983 -0.3454,0.2057 -0.3554,0.2182 -0.3579,0.2382 -0.'
        '3554,0.2307 -0.3454,0.2207 -0.3279,0.2157 -0.3105,0.2207 -0.3005,0.2332 -0.3155,0.2007 -0.3080,0.188'
        '3ZM0.1933,0.1783 0.1534,0.2830 0.1584,0.2930 0.1509,0.2980 0.1608,0.2955 0.1733,0.2980 0.1908,0.3155'
        'ZM-0.1234,0.1958 -0.1135,0.1883 -0.1010,0.1858 -0.0885,0.1883 -0.1085,0.1708 -0.1135,0.1708 -0.1209,'
        '0.1808ZM-0.1833,0.1733 -0.1733,0.1733 -0.1584,0.1858 -0.1534,0.1958 -0.1534,0.2082 -0.1459,0.1958 -0'
        '.1459,0.1658ZM-0.2581,0.1633 -0.2756,0.1584 -0.2855,0.1708 -0.2830,0.1733 -0.2855,0.1858 -0.2830,0.1'
        '783 -0.2731,0.1683 -0.2581,0.1658ZM0.2506,0.0960 0.2406,0.1160 0.2456,0.1209 0.2631,0.1259 0.2506,0.'
        '1085ZM0.2007,0.0960 0.2007,0.1085 0.1883,0.1259 0.2057,0.1209 0.2107,0.1160ZM-0.3529,0.0810 -0.3653,'
        '0.0835 -0.3778,0.0935 -0.3853,0.1110 -0.3878,0.1484 -0.3953,0.1608 -0.4127,0.1783 -0.4177,0.1783 -0.'
        '4027,0.2007 -0.4027,0.2157 -0.4127,0.2307 -0.3928,0.2182 -0.3878,0.2232 -0.4277,0.2456 -0.4177,0.243'
        '1 -0.4027,0.2456 -0.3878,0.2581 -0.3853,0.2656 -0.3853,0.2581 -0.3728,0.2556 -0.3678,0.2456 -0.3678,'
        '0.1883 -0.3529,0.1758 -0.3529,0.1559 -0.3579,0.1484 -0.3628,0.1259 -0.3603,0.0985ZM-0.0436,0.0786 -0'
        '.0611,0.0661 -0.0661,0.0661 -0.0686,0.0835 -0.0786,0.1035 -0.0661,0.0935 -0.0536,0.0910 -0.0436,0.09'
        '35ZM-0.1933,0.0461 -0.1833,0.0686 -0.1783,0.0686 -0.1658,0.0586 -0.1883,0.0436ZM-0.2481,0.0436 -0.25'
        '06,0.0511 -0.2606,0.0611 -0.2756,0.0636 -0.2456,0.0711ZM-0.1409,0.0411 -0.1559,0.0461 -0.1683,0.0436'
        ' -0.1484,0.0486ZM-0.0237,-0.0237 -0.0312,-0.0087 -0.0411,0.0012 -0.0561,0.0037 -0.0312,-0.0012 -0.03'
        '12,-0.0112ZM-0.2032,-0.0411 -0.2057,-0.0337 -0.2007,-0.0312 -0.2007,-0.0411ZM0.2032,-0.0860 0.2132,-'
        '0.0885 0.2307,-0.0835 0.2257,-0.0985 0.2107,-0.0985 0.2132,-0.0910ZM0.2506,-0.1309 0.2406,-0.1160 0.'
        '2406,-0.1085 0.2656,-0.1085ZM0.2681,-0.1384 0.2606,-0.1359 0.2781,-0.1010 0.2756,-0.0985 0.2406,-0.0'
        '985 0.2406,-0.0910 0.2456,-0.0810 0.2656,-0.0686 0.2805,-0.0686 0.2930,-0.0736 0.3055,-0.0885 0.3080'
        ',-0.1110 0.3030,-0.1234 0.2930,-0.1334ZM0.0910,-0.1384 0.0686,-0.1259 0.0611,-0.1085 0.0611,-0.0985 '
        '0.0736,-0.0761 0.0885,-0.0686 0.1035,-0.0686 0.1160,-0.0736 0.1259,-0.0835 0.1309,-0.0960 0.1309,-0.'
        '1110 0.1234,-0.1259 0.1185,-0.1284 0.1160,-0.1135 0.1035,-0.1010 0.0960,-0.0985 0.0910,-0.1035 0.101'
        '0,-0.1110 0.1110,-0.1359ZM0.1234,-0.1459 0.1359,-0.1309 0.1434,-0.1135 0.1434,-0.0910 0.1359,-0.0786'
        ' 0.1559,-0.0860 0.1758,-0.0810 0.1808,-0.0885 0.1883,-0.0910 0.1883,-0.0985 0.1783,-0.1135 0.1284,-0'
        '.1484ZM0.2182,-0.1658 0.1983,-0.1658 0.1908,-0.1608 0.1908,-0.1509 0.2032,-0.1234ZM0.1185,-0.1658 0.'
        '1085,-0.1534 0.0985,-0.1509 0.1135,-0.1484ZM0.2307,-0.1683 0.2082,-0.1085 0.2257,-0.1085 0.2307,-0.1'
        '259 0.2456,-0.1409ZM0.1309,-0.1683 0.1284,-0.1633 0.1309,-0.1584 0.1758,-0.1284 0.1608,-0.1683ZM0.23'
        '82,-0.2332 0.2581,-0.1833 0.2556,-0.1758 0.2431,-0.1683 0.2531,-0.1484 0.2631,-0.1509 0.2905,-0.1484'
        ' 0.3130,-0.1309 0.3180,-0.1185 0.3229,-0.1284 0.3379,-0.1409 0.3504,-0.1434 0.3703,-0.1359 0.3454,-0'
        '.1633 0.3180,-0.1858 0.2756,-0.2107 0.2656,-0.2207 0.2506,-0.2232ZM0.1883,-0.2357 0.1384,-0.2032 0.1'
        '334,-0.1783 0.1658,-0.1783 0.1733,-0.1858 0.2082,-0.1883ZM0.2107,-0.2805 0.1983,-0.2681 0.1858,-0.26'
        '56 0.1708,-0.2781 0.1683,-0.2880 0.1584,-0.2756 0.1434,-0.2731 0.1534,-0.2656 0.1509,-0.2606 0.1284,'
        '-0.2681 0.1409,-0.2506 0.1409,-0.2332 0.1309,-0.2182 0.1933,-0.2606 0.2157,-0.2706ZM-0.1035,-0.2955 '
        '-0.1110,-0.2880 -0.1135,-0.2756 -0.1060,-0.2656 -0.0935,-0.2631 -0.0835,-0.2706 -0.0810,-0.2855 -0.0'
        '910,-0.2955ZM-0.3130,-0.2955 -0.3229,-0.2880 -0.3229,-0.2731 -0.3204,-0.2681 -0.3055,-0.2631 -0.2955'
        ',-0.2681 -0.2930,-0.2880 -0.3030,-0.2955ZM-0.1434,-0.2781 -0.1334,-0.2781 -0.1234,-0.2706 -0.1259,-0'
        '.2855 -0.1209,-0.2955 -0.1035,-0.3080 -0.0910,-0.3080 -0.0736,-0.2955 -0.0686,-0.2855 -0.0711,-0.270'
        '6 -0.0611,-0.2781 -0.0511,-0.2781 -0.0611,-0.2781 -0.0686,-0.2980 -0.0885,-0.3130 -0.1135,-0.3105 -0'
        '.1259,-0.2980 -0.1309,-0.2805ZM-0.3753,-0.2406 -0.2731,-0.2207 -0.2855,-0.2307 -0.2905,-0.2406 -0.29'
        '05,-0.2556 -0.2855,-0.2631 -0.2930,-0.2556 -0.3055,-0.2506 -0.3180,-0.2531 -0.3329,-0.2656 -0.3354,-'
        '0.2880 -0.3204,-0.3055 -0.3005,-0.3080 -0.2805,-0.2880 -0.2830,-0.2681 -0.2706,-0.2781 -0.2606,-0.27'
        '81 -0.2731,-0.2781 -0.2781,-0.2955 -0.2930,-0.3105 -0.3155,-0.3130 -0.3279,-0.3080 -0.3354,-0.3005 -'
        '0.3404,-0.2905 -0.3404,-0.2805 -0.3454,-0.2781 -0.3454,-0.2631 -0.3504,-0.2531 -0.3603,-0.2431ZM-0.0'
        '237,-0.3229 -0.0237,-0.2855 -0.0112,-0.2955 -0.0012,-0.2955 -0.0037,-0.3030 -0.0112,-0.3055 -0.0212,'
        '-0.3155ZM-0.3803,-0.3304 -0.3653,-0.3279 -0.3554,-0.3180 -0.3529,-0.3105 -0.3529,-0.3254 -0.3454,-0.'
        '3329 -0.3479,-0.3304 -0.3603,-0.3329ZM-0.1534,-0.3878 -0.1534,-0.3479 -0.0810,-0.3479 -0.1185,-0.387'
        '8ZM-0.2431,-0.3479 -0.1608,-0.3479 -0.1608,-0.3878 -0.2157,-0.3878Z'
    ),
    '551.1/0': (
        'M0.1611,-0.0221 0.1391,-0.0265 0.1214,-0.0221 0.1082,-0.0088 0.0949,-0.0132 0.0861,-0.0088 0.0728,-0'
        '.0177 0.0640,-0.0132 0.0419,-0.0177 0.0199,-0.0044 0.0155,-0.0088 0.0110,-0.0044 -0.0375,-0.0044 -0.'
        '0817,-0.0132 -0.0949,0.0000 -0.1082,0.0000 -0.1655,0.0309 -0.2494,0.1148 -0.2538,0.1324 -0.2362,0.15'
        '89 -0.2362,0.1810 -0.2141,0.2119 -0.2229,0.2163 -0.2494,0.2031 -0.2980,0.1987 -0.3068,0.2075 -0.2494'
        ',0.3223 -0.2097,0.3708 -0.1832,0.3796 -0.1700,0.3620 -0.1611,0.3620 -0.1523,0.3708 -0.0905,0.3796 -0'
        '.0773,0.3664 -0.0949,0.3532 -0.1214,0.3443 -0.1126,0.3311 -0.1346,0.3178 -0.1391,0.3046 -0.1170,0.29'
        '14 -0.1170,0.2605 -0.1258,0.2472 -0.1214,0.2428 -0.0993,0.2516 -0.0419,0.2472 -0.0287,0.2384 0.0419,'
        '0.2958 0.0817,0.2914 0.1126,0.3002 0.1435,0.3002 0.1523,0.2869 0.1302,0.2693 0.1567,0.2560 0.1788,0.'
        '2781 0.1920,0.2693 0.1700,0.2340 0.1700,0.2207 0.2053,0.2163 0.2141,0.2031 0.2053,0.1942 0.1744,0.18'
        '98 0.1391,0.1501 0.2009,0.0883 0.1964,0.0795 0.2053,0.0706 0.2009,0.0397 0.1832,0.0177 0.1788,-0.004'
        '4ZM-0.1744,0.3002 -0.1700,0.2958 -0.1523,0.3002 -0.1567,0.3046ZM0.1258,0.2340 0.1346,0.2296 0.1435,0'
        '.2384 0.1346,0.2428ZM0.0861,0.2251 0.1037,0.2163 0.1214,0.2384 0.0993,0.2428ZM0.0905,0.1810 0.0993,0'
        '.1898 0.0773,0.2075 0.0817,0.2207 0.0684,0.2296 0.0552,0.2163Z'
    ),
    '773/0': (
        'M-0.4770,-0.5766 -0.4904,-0.5613 -0.4981,-0.5441 -0.5000,-0.5307 -0.5000,0.5307 -0.4943,0.5536 -0.48'
        '85,0.5632 -0.4732,0.5785 -0.4521,0.5881 0.4502,0.5881 0.4751,0.5766 0.4904,0.5575 0.4981,0.5326 0.49'
        '81,-0.5345 0.4923,-0.5556 0.4847,-0.5670 0.4674,-0.5824 0.4406,-0.5900 -0.4425,-0.5900 -0.4655,-0.58'
        '43Z'
    ),
    '773/1': (
        'M0.2222,-0.4368 0.1897,-0.4253 0.1762,-0.4157 0.1609,-0.3985 0.1513,-0.3812 0.1456,-0.3621 0.1456,-0'
        '.3333 0.1494,-0.3180 0.1590,-0.2989 0.1801,-0.2759 0.2050,-0.2625 0.2184,-0.2586 0.2318,-0.2605 0.23'
        '75,-0.2567 0.2682,-0.2644 0.2835,-0.2720 0.3008,-0.2874 0.3123,-0.3027 0.3218,-0.3257 0.3238,-0.3602'
        ' 0.3218,-0.3716 0.3142,-0.3889 0.2931,-0.4157 0.2759,-0.4272 0.2548,-0.4349 0.2471,-0.4330 0.2433,-0'
        '.4368ZM0.2471,-0.4310 0.2510,-0.4272 0.2625,-0.4253 0.2778,-0.4176 0.3027,-0.3946 0.3103,-0.3812 0.3'
        '161,-0.3621 0.3161,-0.3333 0.3065,-0.3065 0.2874,-0.2835 0.2586,-0.2682 0.2414,-0.2663 0.2337,-0.262'
        '5 0.2299,-0.2663 0.2107,-0.2682 0.1897,-0.2778 0.1705,-0.2950 0.1571,-0.3180 0.1533,-0.3314 0.1533,-'
        '0.3640 0.1628,-0.3889 0.1724,-0.4023 0.1877,-0.4157 0.2126,-0.4272ZM-0.2471,-0.4368 -0.2778,-0.4272 '
        '-0.2893,-0.4195 -0.3103,-0.3985 -0.3238,-0.3678 -0.3257,-0.3352 -0.3142,-0.3027 -0.2931,-0.2778 -0.2'
        '701,-0.2644 -0.2337,-0.2567 -0.2069,-0.2625 -0.1820,-0.2759 -0.1648,-0.2931 -0.1571,-0.3046 -0.1494,'
        '-0.3238 -0.1475,-0.3410 -0.1513,-0.3448 -0.1552,-0.3410 -0.1609,-0.3123 -0.1705,-0.2969 -0.1916,-0.2'
        '778 -0.2203,-0.2663 -0.2529,-0.2663 -0.2663,-0.2701 -0.2816,-0.2778 -0.2989,-0.2931 -0.3103,-0.3103 '
        '-0.3180,-0.3352 -0.3161,-0.3678 -0.3065,-0.3908 -0.2950,-0.4061 -0.2701,-0.4234 -0.2490,-0.4291 -0.2'
        '261,-0.4291 -0.2241,-0.4310 -0.2203,-0.4272 -0.1954,-0.4195 -0.1724,-0.4004 -0.1609,-0.3812 -0.1552,'
        '-0.3621 -0.1552,-0.3525 -0.1513,-0.3487 -0.1475,-0.3525 -0.1475,-0.3621 -0.1513,-0.3774 -0.1609,-0.3'
        '966 -0.1877,-0.4234 -0.2146,-0.4349 -0.2222,-0.4330 -0.2261,-0.4368ZM-0.4559,-0.5556 -0.4655,-0.5460'
        ' -0.4713,-0.5287 -0.4713,0.5268 -0.4655,0.5460 -0.4579,0.5536 -0.4464,0.5594 0.4444,0.5594 0.4559,0.'
        '5536 0.4636,0.5460 0.4693,0.5287 0.4693,-0.5307 0.4655,-0.5441 0.4540,-0.5556 0.4368,-0.5613 -0.4387'
        ',-0.5613ZM-0.4061,-0.4866 -0.4004,-0.4943 -0.3870,-0.5000 0.3831,-0.5000 0.3985,-0.4943 0.4042,-0.48'
        '85 0.4080,-0.4789 0.4080,-0.0364 0.4023,-0.0230 0.3831,-0.0134 -0.3851,-0.0134 -0.3966,-0.0172 -0.40'
        '61,-0.0268 -0.4100,-0.0364 -0.4100,-0.4770Z'
    ),
    '773/2': (
        'M0.2222,-0.4310 0.2069,-0.4272 0.1877,-0.4176 0.1648,-0.3946 0.1552,-0.3774 0.1513,-0.3640 0.1513,-0'
        '.3314 0.1628,-0.3027 0.1820,-0.2816 0.2050,-0.2682 0.2395,-0.2625 0.2586,-0.2663 0.2759,-0.2739 0.28'
        '74,-0.2816 0.3046,-0.3008 0.3180,-0.3333 0.3180,-0.3621 0.3123,-0.3812 0.3046,-0.3946 0.2835,-0.4157'
        ' 0.2567,-0.4291ZM-0.2490,-0.4310 -0.2701,-0.4253 -0.2835,-0.4176 -0.3046,-0.3966 -0.3180,-0.3678 -0.'
        '3199,-0.3352 -0.3161,-0.3199 -0.3065,-0.3008 -0.2816,-0.2759 -0.2529,-0.2644 -0.2203,-0.2644 -0.1916'
        ',-0.2759 -0.1686,-0.2969 -0.1590,-0.3123 -0.1513,-0.3429 -0.1533,-0.3621 -0.1648,-0.3927 -0.1839,-0.'
        '4138 -0.2146,-0.4291Z'
    ),
    '773/3': (
        'M-0.0096,-0.2414 -0.0402,-0.2318 -0.0632,-0.2126 -0.0785,-0.1839 -0.0824,-0.1686 -0.0824,-0.1533 -0.'
        '0785,-0.1360 -0.0709,-0.1188 -0.0536,-0.0977 -0.0307,-0.0843 0.0019,-0.0785 0.0287,-0.0843 0.0460,-0'
        '.0939 0.0613,-0.1073 0.0728,-0.1245 0.0785,-0.1418 0.0805,-0.1667 0.0785,-0.1801 0.0709,-0.1992 0.04'
        '79,-0.2261 0.0249,-0.2375 0.0077,-0.2414Z'
    ),
    '544.2/0': (
        'M0.1082,-0.1280 0.0684,-0.1324 0.0464,-0.1148 0.0375,-0.0839 0.0022,-0.0618 -0.0464,-0.0132 -0.0728,'
        '0.0309 -0.0861,0.0750 -0.1037,0.0618 -0.1126,0.0309 -0.0993,-0.0088 -0.0596,-0.0353 -0.0508,-0.0530 '
        '-0.0508,-0.0750 -0.0596,-0.0927 -0.0817,-0.1104 -0.1126,-0.1104 -0.1391,-0.0883 -0.1435,-0.0441 -0.1'
        '920,0.0044 -0.2141,0.0353 -0.2450,0.0927 -0.2671,0.1589 -0.2803,0.2384 -0.2803,0.2781 -0.2715,0.2869'
        ' -0.2494,0.2914 -0.2538,0.3752 -0.2450,0.3841 -0.1920,0.3841 -0.1832,0.3752 -0.1964,0.3620 -0.2185,0'
        '.3532 -0.2053,0.3002 -0.1964,0.2869 -0.1832,0.2914 -0.1611,0.3664 -0.1479,0.3841 -0.0155,0.3841 -0.0'
        '066,0.3752 -0.0375,0.3532 -0.0243,0.2825 -0.0066,0.3267 0.0022,0.3752 0.0110,0.3841 0.0728,0.3841 0.'
        '0817,0.3752 0.0684,0.3620 0.0508,0.3576 0.0419,0.3443 0.0243,0.2296 0.0110,0.1810 0.0155,0.1059 0.03'
        '75,0.0530 0.0508,0.0397 0.0728,0.0706 0.1391,0.1368 0.1391,0.1457 0.1479,0.1545 0.1611,0.1501 0.1700'
        ',0.1589 0.1302,0.3752 0.1391,0.3841 0.1523,0.3752 0.1832,0.1766 0.2009,0.1368 0.1435,0.0883 0.1214,0'
        '.0618 0.0905,0.0044 0.0773,-0.0397 0.1082,-0.0486 0.1302,-0.0706 0.1302,-0.1015ZM-0.1346,0.0971 -0.0'
        '905,0.1280 -0.0905,0.1678 -0.0817,0.2031 -0.0817,0.3002 -0.0905,0.3487 -0.0993,0.3620 -0.1258,0.3487'
        ' -0.1391,0.2958 -0.1302,0.2693 -0.1479,0.1898 -0.1479,0.1368Z'
    ),
    '551.2/0': (
        'M0.2671,0.1324 0.2053,0.1015 0.1876,0.0618 0.1611,0.0353 0.1258,0.0309 0.1126,0.0353 0.0861,0.0662 0'
        '.0861,0.1015 0.0949,0.1192 0.0861,0.1280 0.0552,0.1324 -0.0110,0.1280 -0.1611,0.1633 -0.2141,0.1633 '
        '-0.2538,0.1501 -0.2759,0.1501 -0.2847,0.1678 -0.1611,0.2825 -0.1082,0.3046 -0.0464,0.3046 -0.0419,0.'
        '3090 -0.0552,0.3311 -0.0375,0.3487 -0.0375,0.3620 -0.0199,0.3752 0.0199,0.3841 0.0331,0.3752 0.0375,'
        '0.3796 0.0552,0.3532 0.0817,0.3576 0.1082,0.3399 0.0993,0.3223 0.0464,0.3223 0.0331,0.3090 0.0375,0.'
        '3046 0.1435,0.2958 0.1832,0.2605 0.1876,0.2163 0.1567,0.1633 0.1523,0.1413 0.2009,0.1324 0.2582,0.15'
        '01ZM-0.0243,0.3267 -0.0066,0.3090 0.0066,0.3090 0.0287,0.3443 -0.0066,0.3487 -0.0243,0.3355Z'
    ),
    '581/0': (
        'M-0.2450,0.3752 -0.2362,0.3841 -0.2097,0.3841 -0.2009,0.3752 -0.2009,0.0971 -0.1964,0.0927 -0.1346,0'
        '.1324 -0.0905,0.1368 -0.0243,0.1766 0.0243,0.1898 0.1037,0.1898 0.1302,0.1810 0.1788,0.1810 0.2318,0'
        '.2031 0.2406,0.1942 0.2582,0.1236 0.2273,0.1015 0.1700,0.0795 0.0508,0.0750 0.0199,0.0618 -0.0066,0.'
        '0353 -0.0640,0.0177 -0.1258,0.0132 -0.1964,0.0706 -0.2097,0.0530 -0.2362,0.0530 -0.2450,0.0618ZM-0.1'
        '391,0.0441 -0.1346,0.0486 -0.1346,0.1059 -0.1435,0.1104 -0.1788,0.0883 -0.1832,0.0795Z'
    ),
    '582/0': (
        'M-0.3730,0.3487 -0.3510,0.3752 -0.3289,0.3841 0.2406,0.3841 0.2627,0.3752 0.2759,0.3620 0.3201,0.295'
        '8 0.3289,0.2605 0.3201,0.2384 0.2936,0.2163 0.0155,0.2163 0.0110,0.2119 0.0331,0.1810 0.2053,0.1633 '
        '0.2141,0.1545 0.2141,0.1413 0.2053,0.1324 0.0287,0.1413 0.0022,0.1148 -0.2009,0.1148 -0.2229,0.1324 '
        '-0.2229,0.2031 -0.2141,0.2119 -0.2185,0.2163 -0.3024,0.2163 -0.3289,0.2384 -0.3730,0.3090Z'
    ),
    '772/0': (
        'M-0.3207,0.2411 -0.3207,0.3429 -0.3119,0.3517 -0.2721,0.3517 -0.2588,0.3650 -0.2411,0.3650 -0.2146,0'
        '.3871 -0.2013,0.3827 -0.1836,0.3650 -0.1659,0.3650 -0.1526,0.3827 -0.1394,0.3871 -0.1261,0.3827 -0.1'
        '128,0.3650 0.1040,0.3650 0.1305,0.3871 0.1438,0.3827 0.1615,0.3650 0.1792,0.3650 0.1924,0.3827 0.205'
        '7,0.3871 0.2190,0.3827 0.2323,0.3650 0.2544,0.3650 0.2676,0.3517 0.3075,0.3517 0.3163,0.3429 0.3163,'
        '0.2544 0.2986,0.1880 0.2853,0.1703 0.2765,0.1659 0.0686,0.1659 0.0597,0.1570 0.0332,0.1570 0.0288,0.'
        '1526 0.0597,0.1217 0.0155,0.0863 0.0155,0.0730 0.0066,0.0641 -0.0111,0.0641 -0.0199,0.0730 -0.0199,0'
        '.0863 -0.0686,0.1217 -0.0376,0.1526 -0.0420,0.1570 -0.0686,0.1570 -0.0774,0.1659 -0.2853,0.1659 -0.3'
        '075,0.1880ZM0.2544,0.2013 0.2676,0.2013 0.2765,0.2101 0.2853,0.2455 0.2809,0.2499 0.2499,0.2455ZM0.1'
        '924,0.2013 0.2146,0.2013 0.2234,0.2101 0.2234,0.3296 0.2190,0.3340 0.1880,0.3296 0.1880,0.2057ZM0.13'
        '94,0.2013 0.1703,0.2057 0.1703,0.3296 0.1659,0.3340 0.1349,0.3296 0.1349,0.2057ZM0.0509,0.2057 0.055'
        '3,0.2013 0.1040,0.2013 0.1084,0.2455 0.1040,0.2499 0.0553,0.2499ZM-0.0332,0.2057 -0.0288,0.2013 0.01'
        '99,0.2013 0.0243,0.2455 0.0199,0.2499 -0.0288,0.2499ZM-0.1172,0.2057 -0.1128,0.2013 -0.0641,0.2013 -'
        '0.0597,0.2455 -0.0641,0.2499 -0.1128,0.2499ZM-0.1703,0.2013 -0.1438,0.2057 -0.1438,0.3296 -0.1482,0.'
        '3340 -0.1792,0.3296 -0.1792,0.2101ZM-0.2234,0.2013 -0.1969,0.2057 -0.1969,0.3296 -0.2013,0.3340 -0.2'
        '278,0.3296 -0.2278,0.2057ZM-0.2765,0.2013 -0.2632,0.2013 -0.2544,0.2101 -0.2588,0.2499 -0.2898,0.245'
        '5 -0.2853,0.2101ZM-0.0420,0.1217 -0.0022,0.0951 0.0376,0.1261 -0.0066,0.1526 -0.0332,0.1349Z'
    ),
    '782/0': (
        'M0.3510,0.3311 0.3421,0.3223 0.2671,0.3223 0.2229,0.3090 0.1258,0.2516 0.1302,0.2472 0.1788,0.2560 0'
        '.2053,0.2516 0.2141,0.2781 0.2362,0.3002 0.2538,0.3046 0.2803,0.2958 0.3024,0.2649 0.3112,0.2737 0.3'
        '289,0.2737 0.3377,0.2649 0.3289,0.2207 0.3068,0.1942 0.2847,0.1810 0.2406,0.1766 0.2009,0.1987 0.192'
        '0,0.1942 0.2097,0.0795 0.1964,0.0618 0.0375,0.0397 0.0243,0.0530 0.0199,0.1059 0.0110,0.1324 -0.0066'
        ',0.1059 -0.1082,0.0927 -0.1170,0.1015 -0.1214,0.1368 -0.1346,0.1457 -0.1479,0.1324 -0.1744,0.0839 -0'
        '.1920,0.0662 -0.2097,0.0662 -0.2538,0.0927 -0.2715,0.1236 -0.2759,0.2340 -0.2406,0.2869 -0.2229,0.27'
        '81 -0.1964,0.3002 -0.1655,0.3002 -0.1391,0.2737 -0.1435,0.2340 -0.1302,0.2207 -0.0993,0.2428 -0.0596'
        ',0.2384 -0.0419,0.2163 -0.0375,0.1942 -0.0464,0.1766 -0.0331,0.1633 0.0022,0.2340 -0.0993,0.2958 -0.'
        '1479,0.3178 -0.3421,0.3223 -0.3510,0.3311 -0.3510,0.3752 -0.3421,0.3841 0.3421,0.3841 0.3510,0.3752Z'
        'M0.2450,0.2560 0.2538,0.2472 0.2627,0.2516 0.2582,0.2649ZM-0.1920,0.2560 -0.1832,0.2472 -0.1744,0.25'
        '16 -0.1788,0.2649ZM-0.0949,0.1987 -0.0861,0.1898 -0.0773,0.1942 -0.0817,0.2075ZM-0.2053,0.1104 -0.19'
        '20,0.1236 -0.1832,0.1501 -0.2406,0.1854 -0.2450,0.1810 -0.2406,0.1324Z'
    ),
    '513.2/0': (
        'M-1.3571,-0.4034 -1.3613,-0.3782 -1.3613,0.3739 -1.3529,0.4118 -1.3319,0.4496 -1.2815,0.4874 -1.2437'
        ',0.4958 1.2437,0.4958 1.3025,0.4748 1.3361,0.4412 1.3571,0.3950 1.3571,-0.3992 1.3277,-0.4580 1.3109'
        ',-0.4748 1.2731,-0.4958 1.2563,-0.5000 -1.2605,-0.5000 -1.3067,-0.4790 -1.3361,-0.4496Z'
    ),
    '513.2/1': (
        'M0.8193,-0.2185 0.7731,-0.1975 0.7353,-0.1597 0.7269,-0.1429 0.7059,-0.0546 0.7059,0.0588 0.7269,0.1'
        '471 0.7395,0.1723 0.7647,0.1975 0.8151,0.2227 0.8739,0.2227 0.9118,0.2059 0.9496,0.1681 0.9664,0.134'
        '5 0.9832,0.0420 0.9790,-0.0798 0.9664,-0.1303 0.9496,-0.1639 0.9160,-0.1975 0.8655,-0.2185ZM-1.2983,'
        '-0.3908 -1.2983,0.3866 -1.2941,0.3992 -1.2563,0.4328 -1.2353,0.4370 1.2311,0.4370 1.2689,0.4244 1.28'
        '57,0.4076 1.2983,0.3782 1.2983,-0.3824 1.2899,-0.4076 1.2647,-0.4328 1.2437,-0.4412 -1.2437,-0.4412 '
        '-1.2689,-0.4328 -1.2899,-0.4118ZM0.7941,-0.3445 0.8950,-0.3445 0.9538,-0.3277 1.0168,-0.2899 1.0504,'
        '-0.2605 1.0756,-0.2227 1.1008,-0.1681 1.1218,-0.0840 1.1261,0.0546 1.1050,0.1597 1.0756,0.2269 1.054'
        '6,0.2605 1.0042,0.3067 0.9370,0.3403 0.9034,0.3487 0.8613,0.3529 0.7857,0.3487 0.7311,0.3319 0.6681,'
        '0.2941 0.6303,0.2563 0.5924,0.1891 0.5672,0.0882 0.5630,0.0546 0.5672,-0.0882 0.5924,-0.1807 0.6345,'
        '-0.2563 0.6765,-0.2941 0.7227,-0.3235ZM0.1050,-0.3487 0.1933,-0.3529 0.2269,-0.3487 0.2941,-0.3277 0'
        '.3361,-0.3025 0.3782,-0.2605 0.4034,-0.2101 0.4118,-0.1681 0.4034,-0.0840 0.3908,-0.0546 0.3487,-0.0'
        '126 0.3950,0.0252 0.4118,0.0630 0.4202,0.1134 0.4118,0.1933 0.4034,0.2227 0.3739,0.2731 0.3319,0.310'
        '9 0.2899,0.3319 0.2185,0.3445 0.1303,0.3445 0.0462,0.3277 0.0042,0.3067 -0.0336,0.2731 -0.0546,0.243'
        '7 -0.0924,0.1555 -0.0966,0.1345 -0.0924,0.1261 0.0378,0.1050 0.0462,0.1134 0.0672,0.1681 0.0966,0.19'
        '75 0.1345,0.2143 0.1555,0.2185 0.2101,0.2143 0.2521,0.1933 0.2731,0.1681 0.2773,0.1092 0.2689,0.0882'
        ' 0.2437,0.0630 0.2227,0.0546 0.1218,0.0504 0.1134,0.0420 0.1134,-0.0714 0.1471,-0.0798 0.1933,-0.079'
        '8 0.2353,-0.0924 0.2647,-0.1218 0.2731,-0.1471 0.2731,-0.1639 0.2479,-0.2017 0.2143,-0.2227 0.1849,-'
        '0.2269 0.1134,-0.2185 0.0882,-0.2059 0.0546,-0.1723 0.0462,-0.1345 0.0378,-0.1261 -0.0798,-0.1429 -0'
        '.0966,-0.1513 -0.0840,-0.1975 -0.0504,-0.2563 -0.0126,-0.2941 0.0420,-0.3277Z'
    ),
    '513.2/2': (
        'M-0.0630,0.1218 -0.0924,0.1261 -0.0882,0.1639 -0.0798,0.1387ZM0.1176,0.0252 0.1176,0.0462 0.1387,0.0'
        '462ZM0.1387,-0.0756 0.1176,-0.0756 0.1176,-0.0546ZM0.0462,-0.1513 0.0252,-0.1345 0.0084,-0.1345 0.04'
        '20,-0.1303ZM-0.0840,-0.1933 -0.0924,-0.1471 -0.0546,-0.1429 -0.0756,-0.1597 -0.0840,-0.1765Z'
    ),
    '530.1/0': (
        'M-1.2118,-0.4170 -1.2205,-0.3865 -1.2205,0.3821 -1.1987,0.4389 -1.1681,0.4694 -1.1376,0.4869 -1.0983'
        ',0.4956 1.0895,0.4956 1.1419,0.4825 1.1638,0.4694 1.1900,0.4432 1.2118,0.3996 1.2162,0.3734 1.2162,-'
        '0.3777 1.2074,-0.4127 1.1900,-0.4476 1.1419,-0.4869 1.0852,-0.5000 -1.0895,-0.5000 -1.1201,-0.4956 -'
        '1.1681,-0.4738 -1.1943,-0.4476Z'
    ),
    '530.1/1': (
        'M-1.1550,-0.3908 -1.1594,-0.3734 -1.1594,0.3690 -1.1376,0.4127 -1.1114,0.4301 1.1070,0.4301 1.1507,0'
        '.3865 1.1550,0.3603 1.1550,-0.3646 1.1463,-0.3996 1.1201,-0.4258 1.1026,-0.4345 -1.1070,-0.4345 -1.1'
        '245,-0.4258Z'
    ),
    '531.2/0': (
        'M-0.4755,-0.5644 -0.4918,-0.5460 -0.5000,-0.5256 -0.5000,0.5215 -0.4959,0.5358 -0.4877,0.5501 -0.465'
        '2,0.5685 -0.4387,0.5746 0.4366,0.5746 0.4632,0.5685 0.4755,0.5603 0.4898,0.5440 0.4980,0.5215 0.4980'
        ',-0.5256 0.4857,-0.5521 0.4652,-0.5706 0.4387,-0.5767 -0.4407,-0.5767 -0.4611,-0.5726Z'
    ),
    '531.2/1': (
        'M-0.4530,-0.5399 -0.4673,-0.5235 -0.4673,0.5215 -0.4530,0.5378 -0.4407,0.5419 0.4387,0.5419 0.4509,0'
        '.5378 0.4632,0.5256 0.4673,0.5112 0.4673,-0.5153 0.4591,-0.5337 0.4530,-0.5399 0.4427,-0.5440 -0.444'
        '8,-0.5440Z'
    ),
    '572/0': (
        'M-1.0447,-0.3883 -1.0615,-0.3268 -1.0615,0.3212 -1.0503,0.3659 -1.0279,0.4050 -1.0000,0.4385 -0.9385'
        ',0.4777 -0.8659,0.4944 0.8547,0.4944 0.8994,0.4888 0.9665,0.4609 1.0223,0.4050 1.0447,0.3603 1.0559,'
        '0.3101 1.0559,-0.3212 1.0447,-0.3715 1.0223,-0.4162 0.9721,-0.4665 0.9330,-0.4888 0.8994,-0.5000 -0.'
        '9050,-0.5000 -0.9721,-0.4721 -1.0056,-0.4441Z'
    ),
    '572/1': (
        'M-0.9497,-0.3436 -0.9553,-0.3268 -0.9553,0.3156 -0.9385,0.3492 -0.8939,0.3827 -0.8771,0.3883 0.8715,'
        '0.3883 0.9162,0.3659 0.9497,0.3156 0.9497,-0.3212 0.9274,-0.3659 0.8883,-0.3939 0.8659,-0.3994 -0.87'
        '15,-0.3994 -0.9162,-0.3827ZM-0.7374,-0.2318 -0.6816,-0.2263 -0.6816,-0.0028 -0.6704,0.0084 -0.6592,-'
        '0.0028 -0.6536,-0.0307 -0.6201,-0.0642 -0.5922,-0.0754 -0.5531,-0.0810 -0.5251,-0.0754 -0.4916,-0.05'
        '87 -0.4637,-0.0140 -0.4637,0.0475 -0.4804,0.0810 -0.5251,0.1257 -0.5140,0.1369 -0.4637,0.1425 -0.469'
        '3,0.1927 -0.6536,0.1927 -0.6592,0.1872 -0.6592,0.1425 -0.5698,0.0810 -0.5307,0.0419 -0.5251,0.0028 -'
        '0.5475,-0.0196 -0.5754,-0.0196 -0.5978,0.0028 -0.6034,0.0363 -0.6648,0.0363 -0.6760,0.0251 -0.6872,0'
        '.0363 -0.7430,0.0363 -0.7486,0.0307 -0.7486,-0.1369 -0.7821,-0.1536 -0.7821,-0.1872 -0.7654,-0.1927 '
        '-0.7430,-0.2151Z'
    ),
    '572/2': (
        'M-0.6145,-0.0642 -0.6536,-0.0251 -0.6592,0.0307 -0.6034,0.0307 -0.5978,-0.0028 -0.5698,-0.0251 -0.55'
        '31,-0.0251 -0.5251,-0.0028 -0.5251,0.0307 -0.5307,0.0475 -0.5587,0.0754 -0.6536,0.1369 -0.6536,0.192'
        '7 -0.4637,0.1927 -0.4637,0.1425 -0.5363,0.1425 -0.5419,0.1369 -0.4804,0.0754 -0.4693,0.0531 -0.4637,'
        '0.0028 -0.4804,-0.0419 -0.5307,-0.0754 -0.5810,-0.0754ZM-0.7374,-0.2263 -0.7598,-0.1927 -0.7821,-0.1'
        '872 -0.7821,-0.1536 -0.7542,-0.1536 -0.7430,-0.1425 -0.7430,0.0307 -0.6872,0.0307 -0.6872,-0.2263Z'
    ),
    '618/0': (
        'M-0.7524,-0.4710 -0.7645,-0.4444 -0.7645,0.4444 -0.7548,0.4662 -0.7283,0.4903 -0.7089,0.4976 0.7041,'
        '0.4976 0.7283,0.4879 0.7500,0.4662 0.7572,0.4517 0.7621,0.4300 0.7621,-0.4300 0.7597,-0.4469 0.7500,'
        '-0.4686 0.7307,-0.4879 0.6969,-0.5000 -0.7017,-0.5000 -0.7258,-0.4928Z'
    ),
    '618/1': (
        'M-0.7234,-0.4493 -0.7283,-0.4396 -0.7283,0.4372 -0.7234,0.4469 -0.7065,0.4614 -0.6944,0.4638 0.6896,'
        '0.4638 0.7114,0.4565 0.7234,0.4420 0.7258,0.4348 0.7258,-0.4372 0.7089,-0.4589 0.6993,-0.4638 -0.704'
        '1,-0.4638Z'
    ),
    '639/0': (
        'M-0.6877,-0.4693 -0.7031,-0.4349 -0.7031,0.4272 -0.6954,0.4502 -0.6724,0.4770 -0.6533,0.4885 -0.6188'
        ',0.4962 0.6149,0.4962 0.6379,0.4923 0.6609,0.4808 0.6839,0.4579 0.6992,0.4080 0.6992,-0.4157 0.6839,'
        '-0.4655 0.6609,-0.4885 0.6341,-0.5000 -0.6418,-0.5000 -0.6609,-0.4923Z'
    ),
    '639/1': (
        'M-0.6648,-0.4349 -0.6648,0.4272 -0.6456,0.4502 -0.6226,0.4579 0.6188,0.4579 0.6379,0.4502 0.6533,0.4'
        '349 0.6609,0.4157 0.6609,-0.4195 0.6533,-0.4425 0.6341,-0.4617 0.6226,-0.4655 -0.6303,-0.4655 -0.645'
        '6,-0.4579ZM0.2088,0.2663 0.1054,0.3736 0.0134,0.3736 0.0096,0.3697 0.0709,0.3084 0.0632,0.3008 -0.21'
        '65,0.3008 -0.2203,0.2969 -0.2203,0.2395 -0.2165,0.2356 0.0632,0.2356 0.0709,0.2280 0.0096,0.1667 0.0'
        '134,0.1628 0.1054,0.1628ZM-0.0096,-0.3927 0.0402,-0.3851 0.0594,-0.3736 0.0900,-0.3429 0.1054,-0.308'
        '4 0.1054,-0.2548 0.0900,-0.2203 0.0747,-0.2011 0.0479,-0.1820 0.0057,-0.1705 -0.0326,-0.1743 -0.0747'
        ',-0.1973 -0.0977,-0.2241 -0.1130,-0.2663 -0.1092,-0.3123 -0.0862,-0.3544 -0.0594,-0.3774Z'
    ),
    '639/2': (
        'M-0.0747,-0.3352 -0.0939,-0.3008 -0.0939,-0.2625 -0.0709,-0.2203 -0.0479,-0.2011 -0.0134,-0.1897 0.0'
        '096,-0.1897 0.0402,-0.2011 0.0479,-0.2126ZM-0.0479,-0.3621 -0.0556,-0.3506 0.0709,-0.2318 0.0862,-0.'
        '2548 0.0900,-0.2739 0.0862,-0.3084 0.0747,-0.3314 0.0479,-0.3582 0.0249,-0.3697 -0.0172,-0.3736Z'
    ),
    '639/3': (
        'M-0.0096,-0.3927 -0.0441,-0.3851 -0.0862,-0.3544 -0.1092,-0.3161 -0.1130,-0.2625 -0.0977,-0.2241 -0.'
        '0747,-0.1973 -0.0441,-0.1782 0.0057,-0.1705 0.0402,-0.1782 0.0594,-0.1897 0.0900,-0.2203 0.1054,-0.2'
        '548 0.1092,-0.2893 0.0900,-0.3429 0.0594,-0.3736 0.0249,-0.3889ZM-0.0747,-0.3314 0.0441,-0.2088 0.02'
        '49,-0.1973 -0.0134,-0.1935 -0.0402,-0.2011 -0.0632,-0.2165 -0.0785,-0.2356 -0.0900,-0.2625 -0.0900,-'
        '0.3008ZM-0.0517,-0.3544 -0.0172,-0.3697 0.0096,-0.3697 0.0479,-0.3544 0.0709,-0.3314 0.0824,-0.3084 '
        '0.0862,-0.2739 0.0747,-0.2395 0.0670,-0.2356Z'
    ),
    '639/4': (
        'M0.1398,0.3391 0.1169,0.3467 0.0977,0.3429 0.0670,0.3123 0.0057,0.3736 0.1054,0.3736ZM0.1858,0.2433 '
        '0.1935,0.2548 0.1935,0.2816 0.1858,0.2931 0.2088,0.2701ZM-0.2203,0.2356 -0.2203,0.2969 -0.2165,0.300'
        '8 0.0632,0.3008 0.0517,0.2816 0.0517,0.2548 0.0632,0.2356ZM0.0057,0.1628 0.0670,0.2241 0.0977,0.1935'
        ' 0.1169,0.1897 0.1398,0.1973 0.1054,0.1628ZM-0.6111,-0.4655 0.6034,-0.4655 0.5843,-0.4847 -0.5920,-0'
        '.4847Z'
    ),
    '640.3/0': (
        'M-0.5527,-0.4854 -0.5608,-0.4741 -0.5656,-0.4595 -0.5656,0.4579 -0.5592,0.4757 -0.5478,0.4887 -0.526'
        '7,0.4984 0.5219,0.4984 0.5348,0.4951 0.5511,0.4838 0.5608,0.4692 0.5640,0.4546 0.5640,-0.4562 0.5608'
        ',-0.4708 0.5559,-0.4789 0.5429,-0.4919 0.5203,-0.5000 -0.5235,-0.5000 -0.5365,-0.4968Z'
    ),
    '640.3/1': (
        'M-0.5397,-0.4660 -0.5429,-0.4579 -0.5429,0.4562 -0.5397,0.4643 -0.5300,0.4741 -0.5203,0.4773 0.5170,'
        '0.4773 0.5300,0.4724 0.5365,0.4660 0.5413,0.4562 0.5413,-0.4579 0.5316,-0.4724 0.5219,-0.4773 -0.525'
        '1,-0.4773ZM-0.3614,-0.1985 -0.3501,-0.2002 -0.3015,-0.1985 -0.2739,-0.1904 -0.2431,-0.1742 -0.2301,-'
        '0.1645 -0.2010,-0.1321 -0.1880,-0.1094 -0.1767,-0.0754 -0.1734,-0.0446 -0.1767,-0.0105 -0.1864,0.020'
        '3 -0.1994,0.0446 -0.2172,0.0673 -0.2399,0.0867 -0.2723,0.1045 -0.2982,0.1126 -0.3241,0.1159 -0.3647,'
        '0.1126 -0.3906,0.1045 -0.4182,0.0900 -0.4295,0.0818 -0.4538,0.0575 -0.4635,0.0446 -0.4765,0.0203 -0.'
        '4862,-0.0105 -0.4895,-0.0413 -0.4862,-0.0737 -0.4781,-0.1013 -0.4652,-0.1272 -0.4506,-0.1467 -0.4198'
        ',-0.1742 -0.3890,-0.1904Z'
    ),
    '640.3/2': (
        'M-0.4327,-0.1191 -0.4425,-0.1062 -0.4538,-0.0802 -0.4587,-0.0559 -0.4587,-0.0284 -0.4506,0.0041 -0.4'
        '408,0.0235 -0.4279,0.0413 -0.4003,0.0656 -0.3695,0.0802 -0.3468,0.0851 -0.3160,0.0851 -0.2934,0.0802'
        ' -0.2577,0.0624 -0.2545,0.0592ZM-0.4036,-0.1483 -0.4068,-0.1434 -0.2301,0.0332 -0.2237,0.0267 -0.207'
        '5,-0.0105 -0.2042,-0.0267 -0.2042,-0.0575 -0.2139,-0.0932 -0.2253,-0.1143 -0.2399,-0.1321 -0.2609,-0'
        '.1499 -0.2820,-0.1613 -0.2950,-0.1661 -0.3209,-0.1710 -0.3420,-0.1710 -0.3614,-0.1677 -0.3809,-0.161'
        '3Z'
    ),
    '640.3/3': (
        'M-0.3549,-0.2002 -0.3857,-0.1921 -0.4149,-0.1775 -0.4344,-0.1629 -0.4635,-0.1305 -0.4765,-0.1062 -0.'
        '4862,-0.0754 -0.4895,-0.0543 -0.4878,-0.0170 -0.4830,0.0041 -0.4716,0.0316 -0.4554,0.0559 -0.4295,0.'
        '0818 -0.4052,0.0981 -0.3728,0.1110 -0.3485,0.1159 -0.3144,0.1159 -0.2901,0.1110 -0.2545,0.0964 -0.23'
        '50,0.0835 -0.2075,0.0559 -0.1912,0.0316 -0.1799,0.0041 -0.1734,-0.0300 -0.1734,-0.0559 -0.1783,-0.08'
        '35 -0.1848,-0.1029 -0.1945,-0.1224 -0.2091,-0.1434 -0.2318,-0.1661 -0.2528,-0.1807 -0.2869,-0.1953 -'
        '0.3241,-0.2018ZM-0.4344,-0.1159 -0.4311,-0.1175 -0.2561,0.0592 -0.2707,0.0689 -0.2934,0.0786 -0.3160'
        ',0.0835 -0.3468,0.0835 -0.3776,0.0754 -0.4003,0.0640 -0.4149,0.0527 -0.4392,0.0235 -0.4489,0.0041 -0'
        '.4571,-0.0284 -0.4571,-0.0559 -0.4522,-0.0802ZM-0.4036,-0.1467 -0.3809,-0.1596 -0.3614,-0.1661 -0.34'
        '20,-0.1694 -0.3209,-0.1694 -0.3015,-0.1661 -0.2820,-0.1596 -0.2609,-0.1483 -0.2431,-0.1337 -0.2269,-'
        '0.1143 -0.2156,-0.0932 -0.2058,-0.0575 -0.2075,-0.0170 -0.2139,0.0041 -0.2253,0.0267 -0.2301,0.0316 '
        '-0.4052,-0.1434Z'
    ),
    '640.4/0': (
        'M-0.6769,-0.4734 -0.6851,-0.4550 -0.6871,-0.4407 -0.6871,0.4387 -0.6851,0.4530 -0.6769,0.4714 -0.658'
        '5,0.4898 -0.6380,0.4980 0.6360,0.4980 0.6564,0.4898 0.6708,0.4775 0.6789,0.4652 0.6851,0.4427 0.6851'
        ',-0.4448 0.6748,-0.4734 0.6564,-0.4918 0.6360,-0.5000 -0.6360,-0.5000 -0.6605,-0.4898Z'
    ),
    '640.4/1': (
        'M-0.6544,-0.4571 -0.6585,-0.4468 -0.6585,0.4448 -0.6524,0.4571 -0.6421,0.4673 -0.6319,0.4714 0.6299,'
        '0.4714 0.6401,0.4673 0.6524,0.4550 0.6564,0.4448 0.6564,-0.4468 0.6524,-0.4571 0.6421,-0.4673 0.6339'
        ',-0.4714 -0.6339,-0.4714 -0.6462,-0.4652ZM-0.4376,-0.3773 -0.4008,-0.3793 -0.3681,-0.3753 -0.3333,-0'
        '.3650 -0.2924,-0.3425 -0.2515,-0.3037 -0.2413,-0.2894 -0.2229,-0.2546 -0.2106,-0.2096 -0.2086,-0.168'
        '7 -0.2127,-0.1380 -0.2249,-0.0992 -0.2474,-0.0603 -0.2802,-0.0256 -0.3129,-0.0031 -0.3538,0.0133 -0.'
        '3824,0.0194 -0.4335,0.0194 -0.4560,0.0153 -0.4867,0.0051 -0.5317,-0.0215 -0.5644,-0.0542 -0.5849,-0.'
        '0849 -0.6012,-0.1258 -0.6074,-0.1585 -0.6074,-0.1994 -0.5992,-0.2382 -0.5828,-0.2771 -0.5665,-0.3016'
        ' -0.5440,-0.3262 -0.5112,-0.3507 -0.4663,-0.3712Z'
    ),
    '640.4/2': (
        'M-0.5358,-0.2730 -0.5460,-0.2607 -0.5624,-0.2239 -0.5685,-0.1912 -0.5685,-0.1626 -0.5562,-0.1155 -0.'
        '5419,-0.0890 -0.5256,-0.0685 -0.5031,-0.0481 -0.4806,-0.0337 -0.4560,-0.0235 -0.4274,-0.0174 -0.3885'
        ',-0.0174 -0.3661,-0.0215 -0.3476,-0.0276 -0.3149,-0.0460 -0.3108,-0.0501ZM-0.4949,-0.3139 -0.5031,-0'
        '.3057 -0.2822,-0.0828 -0.2781,-0.0828 -0.2699,-0.0930 -0.2556,-0.1217 -0.2474,-0.1524 -0.2454,-0.181'
        '0 -0.2495,-0.2137 -0.2597,-0.2444 -0.2740,-0.2689 -0.2904,-0.2894 -0.3292,-0.3200 -0.3517,-0.3303 -0'
        '.3824,-0.3384 -0.4029,-0.3384 -0.4049,-0.3405 -0.4335,-0.3384 -0.4683,-0.3282Z'
    ),
    '640.4/3': (
        'M-0.4274,-0.3793 -0.4601,-0.3732 -0.5010,-0.3569 -0.5297,-0.3384 -0.5665,-0.3016 -0.5828,-0.2771 -0.'
        '5992,-0.2382 -0.6074,-0.1994 -0.6074,-0.1585 -0.6012,-0.1258 -0.5849,-0.0849 -0.5644,-0.0542 -0.5317'
        ',-0.0215 -0.5112,-0.0072 -0.4826,0.0072 -0.4581,0.0153 -0.4192,0.0215 -0.3988,0.0215 -0.3517,0.0133 '
        '-0.3088,-0.0051 -0.2822,-0.0235 -0.2536,-0.0521 -0.2331,-0.0828 -0.2147,-0.1278 -0.2086,-0.1646 -0.2'
        '086,-0.1933 -0.2147,-0.2301 -0.2229,-0.2546 -0.2352,-0.2791 -0.2515,-0.3037 -0.2822,-0.3344 -0.3047,'
        '-0.3507 -0.3558,-0.3732 -0.3885,-0.3793ZM-0.5399,-0.2669 -0.5337,-0.2710 -0.3129,-0.0501 -0.3272,-0.'
        '0399 -0.3661,-0.0235 -0.3885,-0.0194 -0.4274,-0.0194 -0.4560,-0.0256 -0.4806,-0.0358 -0.5153,-0.0603'
        ' -0.5460,-0.0992 -0.5603,-0.1319 -0.5665,-0.1626 -0.5665,-0.1912 -0.5603,-0.2239ZM-0.4949,-0.3119 -0'
        '.4683,-0.3262 -0.4335,-0.3364 -0.4110,-0.3364 -0.4090,-0.3384 -0.3824,-0.3364 -0.3517,-0.3282 -0.329'
        '2,-0.3180 -0.2924,-0.2894 -0.2761,-0.2689 -0.2618,-0.2444 -0.2515,-0.2137 -0.2474,-0.1810 -0.2536,-0'
        '.1339 -0.2781,-0.0849 -0.2822,-0.0849 -0.5010,-0.3057Z'
    ),
    '661.2A/0': (
        'M-0.6936,-0.4665 -0.7027,-0.4421 -0.7027,0.4390 -0.6905,0.4695 -0.6753,0.4848 -0.6448,0.4970 0.6448,'
        '0.4970 0.6631,0.4909 0.6905,0.4665 0.6997,0.4451 0.6997,-0.4451 0.6936,-0.4634 0.6753,-0.4848 0.6601'
        ',-0.4939 0.6357,-0.5000 -0.6387,-0.5000 -0.6631,-0.4939 -0.6814,-0.4817Z'
    ),
    '661.2A/1': (
        'M-0.2790,-0.2835 -0.2912,-0.2866 -0.4832,-0.2866 -0.4893,-0.2805 -0.4893,0.0488 -0.4832,0.0549 -0.42'
        '23,0.0549 -0.4162,0.0488 -0.4162,-0.0762 -0.4131,-0.0793 -0.2912,-0.0793 -0.2637,-0.0915 -0.2424,-0.'
        '1159 -0.2332,-0.1402 -0.2332,-0.2287 -0.2454,-0.2561ZM-0.4162,-0.2287 -0.4131,-0.2317 -0.3338,-0.231'
        '7 -0.3186,-0.2256 -0.3064,-0.2073 -0.3064,-0.1616 -0.3125,-0.1494 -0.3308,-0.1372 -0.4131,-0.1372 -0'
        '.4162,-0.1402ZM-0.6631,-0.4512 -0.6692,-0.4390 -0.6692,0.4360 -0.6540,0.4573 -0.6387,0.4634 0.6387,0'
        '.4634 0.6479,0.4604 0.6662,0.4390 0.6662,-0.4390 0.6509,-0.4604 0.6448,-0.4634 -0.6479,-0.4634ZM0.43'
        '14,0.0732 0.3430,0.1646 0.2576,0.1646 0.2546,0.1616 0.3064,0.1098 0.3003,0.1037 0.0747,0.1037 0.0716'
        ',0.1006 0.0716,0.0488 0.0747,0.0457 0.3003,0.0457 0.3064,0.0396 0.2546,-0.0122 0.2576,-0.0152 0.3430'
        ',-0.0152ZM-0.5899,-0.3415 -0.5838,-0.3445 -0.1845,-0.3445 -0.1662,-0.3323 -0.1601,-0.3171 -0.1601,0.'
        '0732 -0.1662,0.0884 -0.1753,0.0976 -0.1845,0.1006 -0.5838,0.1006 -0.6021,0.0854 -0.6052,0.0793 -0.60'
        '52,-0.3232Z'
    ),
    '661.2A/2': (
        'M-0.4192,-0.2287 -0.4192,-0.1402 -0.4131,-0.1341 -0.3308,-0.1341 -0.3216,-0.1372 -0.3095,-0.1494 -0.'
        '3034,-0.1616 -0.3034,-0.2073 -0.3186,-0.2287 -0.3338,-0.2348 -0.4131,-0.2348ZM-0.5899,-0.3445 -0.608'
        '2,-0.3232 -0.6082,0.0793 -0.6052,0.0854 -0.5838,0.1037 -0.1845,0.1037 -0.1753,0.1006 -0.1631,0.0884 '
        '-0.1570,0.0732 -0.1570,-0.3171 -0.1631,-0.3323 -0.1753,-0.3445 -0.1845,-0.3476 -0.5838,-0.3476ZM-0.2'
        '790,-0.2805 -0.2485,-0.2561 -0.2363,-0.2287 -0.2363,-0.1402 -0.2454,-0.1159 -0.2637,-0.0945 -0.2912,'
        '-0.0823 -0.4131,-0.0823 -0.4192,-0.0762 -0.4192,0.0488 -0.4223,0.0518 -0.4832,0.0518 -0.4863,0.0488 '
        '-0.4863,-0.2805 -0.4832,-0.2835 -0.2912,-0.2835Z'
    ),
    '661.2A/3': (
        'M0.3552,0.1494 0.3430,0.1524 0.3216,0.1463 0.3095,0.1341 0.3034,0.1189 0.2607,0.1616 0.3430,0.1616ZM'
        '0.4162,0.0610 0.4192,0.0640 0.4162,0.0884 0.4284,0.0762ZM0.0747,0.0488 0.0747,0.1006 0.0777,0.1037 0'
        '.3003,0.1037 0.2881,0.0854 0.2881,0.0671 0.3003,0.0488ZM0.2576,-0.0122 0.3064,0.0366 0.3125,0.0183 0'
        '.3247,0.0061 0.3460,0.0000 0.3582,0.0030 0.3430,-0.0122Z'
    ),
    '639.1B/0': (
        'M-0.4860,-0.5315 -0.4965,-0.5175 -0.5000,-0.5018 -0.5000,0.4930 -0.4965,0.5088 -0.4912,0.5175 -0.484'
        '2,0.5245 -0.4702,0.5315 0.4685,0.5315 0.4807,0.5263 0.4912,0.5158 0.4982,0.4982 0.4982,-0.5070 0.491'
        '2,-0.5245 0.4825,-0.5333 -0.4825,-0.5333Z'
    ),
    '639.1B/1': (
        'M-0.2601,-0.0219 -0.2758,-0.0254 -0.3774,-0.0254 -0.3809,-0.0219 -0.3809,0.1708 -0.3774,0.1743 -0.34'
        '06,0.1743 -0.3371,0.1708 -0.3371,0.1007 -0.3354,0.0989 -0.2653,0.0972 -0.2478,0.0884 -0.2356,0.0744 '
        '-0.2303,0.0622 -0.2320,0.0061 -0.2408,-0.0079ZM-0.3371,0.0114 -0.3354,0.0096 -0.2863,0.0096 -0.2811,'
        '0.0114 -0.2758,0.0166 -0.2723,0.0254 -0.2723,0.0482 -0.2758,0.0569 -0.2863,0.0639 -0.3354,0.0639 -0.'
        '3371,0.0622ZM-0.4772,-0.1182 -0.4807,-0.1095 -0.4807,0.4947 -0.4772,0.5035 -0.4667,0.5123 0.4650,0.5'
        '123 0.4755,0.5035 0.4790,0.4930 0.4790,-0.1077 0.4755,-0.1182 0.4650,-0.1270 -0.4667,-0.1270ZM-0.435'
        '2,-0.0552 -0.2005,-0.0552 -0.1935,-0.0499 -0.1900,-0.0429 -0.1900,0.1900 -0.1988,0.2005 -0.2040,0.20'
        '23 -0.4335,0.2023 -0.4440,0.1953 -0.4475,0.1883 -0.4475,-0.0412 -0.4457,-0.0464Z'
    ),
    '639.1B/2': (
        'M-0.4807,-0.5088 -0.4825,-0.5018 -0.4807,-0.1602 -0.4772,-0.1532 -0.4685,-0.1462 -0.4615,-0.1445 0.4'
        '615,-0.1445 0.4702,-0.1480 0.4807,-0.1620 0.4807,-0.5053 0.4790,-0.5105 0.4685,-0.5210 0.4632,-0.522'
        '8 -0.4650,-0.5228 -0.4702,-0.5210ZM-0.3039,-0.3862 -0.2863,-0.3844 -0.2706,-0.3774 -0.2566,-0.3634 -'
        '0.2513,-0.3529 -0.2478,-0.3371 -0.2513,-0.3144 -0.2601,-0.3004 -0.2723,-0.2898 -0.2916,-0.2828 -0.30'
        '91,-0.2828 -0.3319,-0.2933 -0.3441,-0.3074 -0.3511,-0.3249 -0.3511,-0.3424 -0.3441,-0.3616 -0.3354,-'
        '0.3722 -0.3231,-0.3809Z'
    ),
    '639.1B/3': (
        'M-0.3389,0.0114 -0.3389,0.0622 -0.3354,0.0657 -0.2863,0.0657 -0.2741,0.0569 -0.2706,0.0482 -0.2706,0'
        '.0254 -0.2741,0.0166 -0.2811,0.0096 -0.2863,0.0079 -0.3354,0.0079ZM-0.4475,-0.0464 -0.4492,-0.0412 -'
        '0.4492,0.1883 -0.4457,0.1953 -0.4335,0.2040 -0.2040,0.2040 -0.1988,0.2023 -0.1883,0.1900 -0.1883,-0.'
        '0429 -0.1918,-0.0499 -0.2005,-0.0569 -0.4352,-0.0569ZM-0.2601,-0.0201 -0.2426,-0.0079 -0.2320,0.0131'
        ' -0.2320,0.0622 -0.2373,0.0744 -0.2478,0.0867 -0.2653,0.0954 -0.3354,0.0972 -0.3389,0.1007 -0.3389,0'
        '.1708 -0.3406,0.1725 -0.3774,0.1725 -0.3792,0.1708 -0.3792,-0.0219 -0.3774,-0.0236 -0.2758,-0.0236ZM'
        '-0.3319,-0.3599 -0.3389,-0.3529 -0.3424,-0.3424 -0.3424,-0.3249 -0.3336,-0.3074 -0.3214,-0.2968 -0.3'
        '091,-0.2916 -0.2916,-0.2916 -0.2776,-0.2968 -0.2723,-0.3021ZM-0.3231,-0.3704 -0.3266,-0.3669 -0.2671'
        ',-0.3074 -0.2566,-0.3284 -0.2583,-0.3459 -0.2653,-0.3599 -0.2793,-0.3722 -0.2933,-0.3774 -0.3056,-0.'
        '3774Z'
    ),
    '639.1B/4': (
        'M-0.3091,-0.3862 -0.3266,-0.3792 -0.3441,-0.3616 -0.3511,-0.3459 -0.3511,-0.3231 -0.3406,-0.3021 -0.'
        '3214,-0.2863 -0.3109,-0.2828 -0.2881,-0.2828 -0.2723,-0.2898 -0.2583,-0.3021 -0.2478,-0.3249 -0.2478'
        ',-0.3424 -0.2548,-0.3616 -0.2706,-0.3774 -0.2898,-0.3862ZM-0.3371,-0.3529 -0.3319,-0.3581 -0.2741,-0'
        '.3021 -0.2916,-0.2933 -0.3091,-0.2933 -0.3266,-0.3021 -0.3354,-0.3126 -0.3406,-0.3249 -0.3406,-0.342'
        '4ZM-0.3056,-0.3757 -0.2933,-0.3757 -0.2793,-0.3704 -0.2671,-0.3599 -0.2583,-0.3389 -0.2601,-0.3214 -'
        '0.2671,-0.3091 -0.3249,-0.3669Z'
    ),
    '642.3/0': (
        'M-0.6350,-0.4700 -0.6425,-0.4550 -0.6475,-0.4325 -0.6475,0.4325 -0.6350,0.4675 -0.6175,0.4850 -0.590'
        '0,0.4975 0.5900,0.4975 0.6175,0.4850 0.6325,0.4700 0.6450,0.4425 0.6450,-0.4450 0.6375,-0.4650 0.617'
        '5,-0.4875 0.5875,-0.5000 -0.5900,-0.5000 -0.6150,-0.4900Z'
    ),
    '642.3/1': (
        'M-0.6100,-0.4475 -0.6150,-0.4350 -0.6150,0.4350 -0.6075,0.4500 -0.5975,0.4600 -0.5750,0.4675 0.5750,'
        '0.4675 0.5925,0.4625 0.6075,0.4475 0.6125,0.4350 0.6125,-0.4400 0.5950,-0.4625 0.5825,-0.4675 -0.582'
        '5,-0.4675 -0.5950,-0.4625ZM-0.0775,-0.3675 -0.0475,-0.3950 -0.0075,-0.4075 0.0225,-0.4050 0.0525,-0.'
        '3900 0.1075,-0.3900 0.1100,-0.3875 0.1100,-0.2375 0.1075,-0.2350 0.0525,-0.2350 0.0200,-0.2200 -0.02'
        '00,-0.2200 -0.0575,-0.2375 -0.0850,-0.2700 -0.0925,-0.2925 -0.0925,-0.3325Z'
    ),
    '642.3/2': (
        'M-0.0775,-0.3675 -0.0925,-0.3350 -0.0950,-0.3175 -0.0925,-0.2900 -0.0750,-0.2550 -0.0550,-0.2350 -0.'
        '0225,-0.2200 0.0100,-0.2175 0.0375,-0.2250 0.0500,-0.2325 0.1075,-0.2325 0.1125,-0.2375 0.1125,-0.38'
        '75 0.1075,-0.3925 0.0500,-0.3925 0.0250,-0.4050 -0.0125,-0.4075 -0.0475,-0.3950ZM-0.0225,-0.2725 -0.'
        '0200,-0.2700 -0.0200,-0.2450 -0.0275,-0.2425 -0.0425,-0.2525ZM-0.0600,-0.3550 -0.0200,-0.3150 -0.020'
        '0,-0.3100 -0.0600,-0.2700 -0.0675,-0.2775 -0.0750,-0.3000 -0.0725,-0.3350 -0.0675,-0.3475ZM-0.0225,-'
        '0.3850 -0.0200,-0.3825 -0.0200,-0.3550 -0.0225,-0.3525 -0.0425,-0.3725 -0.0350,-0.3800Z'
    ),
    '642.3/3': (
        'M-0.0225,-0.2750 -0.0450,-0.2525 -0.0275,-0.2400 -0.0175,-0.2450 -0.0175,-0.2700ZM-0.0600,-0.3575 -0'
        '.0700,-0.3475 -0.0775,-0.3250 -0.0750,-0.2900 -0.0700,-0.2775 -0.0600,-0.2675 -0.0175,-0.3100 -0.017'
        '5,-0.3150ZM-0.0225,-0.3875 -0.0350,-0.3825 -0.0450,-0.3725 -0.0225,-0.3500 -0.0175,-0.3550 -0.0175,-'
        '0.3825Z'
    ),
    '660.4/0': (
        'M-1.0894,-0.4130 -1.0894,0.4130 -1.0749,0.4469 -1.0411,0.4807 -1.0072,0.4952 1.0024,0.4952 1.0507,0.'
        '4710 1.0797,0.4324 1.0845,0.4179 1.0845,-0.4179 1.0797,-0.4372 1.0556,-0.4710 1.0266,-0.4903 0.9976,'
        '-0.5000 -1.0024,-0.5000 -1.0459,-0.4807 -1.0700,-0.4565Z'
    ),
    '660.4/1': (
        'M-0.7271,0.0072 -0.7464,0.0169 -0.8237,0.1135 -0.7657,0.1715 -0.7367,0.1473 -0.6691,0.0604ZM-0.5386,'
        '-0.2826 -0.5580,-0.2729 -0.5773,-0.2440 -0.5676,-0.2101 -0.5435,-0.1908 -0.5531,-0.1667 -0.5386,-0.0'
        '894 -0.5386,-0.0507 -0.5483,-0.0169 -0.5676,0.0024 -0.6111,0.0217 -0.7609,0.1957 -0.8333,0.1329 -0.8'
        '527,0.1473 -0.8623,0.1667 -0.7560,0.2585 -0.7464,0.2585 -0.7077,0.2150 -0.7029,0.2536 -0.6739,0.2778'
        ' -0.6498,0.2778 -0.6256,0.2585 -0.6208,0.2246 -0.6449,0.1957 -0.6594,0.1908 -0.6836,0.1957 -0.6884,0'
        '.1908 -0.5773,0.0556 -0.5338,0.0362 -0.5097,0.0169 -0.5000,0.0314 -0.5000,0.1522 -0.4855,0.2391 -0.5'
        '290,0.2681 -0.5193,0.2778 -0.4469,0.2778 -0.4372,0.2681 -0.4372,0.0990 -0.4324,0.0942 -0.4082,0.1570'
        ' -0.3647,0.2391 -0.4034,0.2681 -0.3937,0.2778 -0.3261,0.2778 -0.3164,0.2681 -0.3164,0.2343 -0.3792,-'
        '0.0169 -0.4324,-0.1522 -0.4710,-0.1908 -0.4952,-0.2053 -0.4855,-0.2246 -0.4903,-0.2585 -0.5097,-0.27'
        '78ZM-1.0314,-0.4179 -1.0362,-0.4034 -1.0362,0.4034 -1.0266,0.4227 -0.9928,0.4469 0.9879,0.4469 1.002'
        '4,0.4420 1.0314,0.4082 1.0314,-0.4082 1.0217,-0.4275 0.9976,-0.4469 -0.9976,-0.4469ZM-0.9300,-0.3454'
        ' -0.9106,-0.3551 -0.2681,-0.3551 -0.2488,-0.3454 -0.2343,-0.3213 -0.2343,0.3213 -0.2391,0.3309 -0.27'
        '29,0.3551 -0.9058,0.3551 -0.9251,0.3454 -0.9444,0.3213 -0.9444,-0.3213Z'
    ),
    '660.4/2': (
        'M-0.9300,-0.3502 -0.9493,-0.3213 -0.9493,0.3213 -0.9444,0.3309 -0.9058,0.3599 -0.2729,0.3599 -0.2536'
        ',0.3502 -0.2295,0.3213 -0.2295,-0.3213 -0.2391,-0.3406 -0.2681,-0.3599 -0.9106,-0.3599ZM-0.6836,0.20'
        '05 -0.6594,0.1957 -0.6304,0.2150 -0.6256,0.2488 -0.6401,0.2681 -0.6739,0.2729 -0.6981,0.2536 -0.7029'
        ',0.2343ZM-0.7271,0.0121 -0.6739,0.0604 -0.7415,0.1473 -0.7657,0.1667 -0.8188,0.1135 -0.7415,0.0169ZM'
        '-0.5386,-0.2778 -0.5097,-0.2729 -0.4952,-0.2585 -0.4903,-0.2246 -0.5000,-0.2053 -0.4372,-0.1522 -0.3'
        '841,-0.0169 -0.3213,0.2343 -0.3261,0.2729 -0.3937,0.2729 -0.3986,0.2681 -0.3599,0.2391 -0.4034,0.157'
        '0 -0.4227,0.0990 -0.4324,0.0894 -0.4420,0.0990 -0.4420,0.2681 -0.4469,0.2729 -0.5193,0.2729 -0.5242,'
        '0.2681 -0.4807,0.2391 -0.4952,0.1522 -0.4952,0.0314 -0.5097,0.0121 -0.5918,0.0652 -0.7464,0.2536 -0.'
        '7754,0.2391 -0.8575,0.1667 -0.8478,0.1473 -0.8333,0.1377 -0.7609,0.2005 -0.6111,0.0266 -0.5676,0.007'
        '2 -0.5435,-0.0169 -0.5338,-0.0507 -0.5338,-0.0894 -0.5483,-0.1667 -0.5386,-0.1908 -0.5628,-0.2101 -0'
        '.5725,-0.2440 -0.5628,-0.2633Z'
    ),
    '640/0': (
        'M-0.4812,-0.6600 -0.4937,-0.6454 -0.5000,-0.6245 -0.4979,0.6308 -0.4916,0.6454 -0.4791,0.6579 -0.460'
        '3,0.6663 0.4603,0.6663 0.4770,0.6600 0.4916,0.6454 0.4979,0.6308 0.4979,-0.6328 0.4916,-0.6475 0.477'
        '0,-0.6621 0.4623,-0.6684 -0.4623,-0.6684Z'
    ),
    '640/1': (
        'M-0.4707,-0.1077 -0.4749,-0.0994 -0.4749,0.6266 -0.4623,0.6412 -0.4561,0.6433 0.4561,0.6433 0.4665,0'
        '.6391 0.4728,0.6328 0.4770,0.6203 0.4770,-0.0910 0.4749,-0.1015 0.4665,-0.1119 0.4582,-0.1161 -0.458'
        '2,-0.1161ZM0.1213,0.5408 0.1213,0.5450 0.0607,0.6056 0.0042,0.6056 0.0021,0.6036 0.0377,0.5680 0.033'
        '5,0.5638 -0.1213,0.5638 -0.1234,0.5617 -0.1234,0.5262 -0.1213,0.5241 0.0335,0.5241 0.0377,0.5199 0.0'
        '021,0.4843 0.0042,0.4822 0.0628,0.4822Z'
    ),
    '640/2': (
        'M-0.4770,-0.6328 -0.4791,-0.6266 -0.4791,-0.1600 -0.4770,-0.1517 -0.4644,-0.1391 -0.4582,-0.1370 0.4'
        '582,-0.1370 0.4728,-0.1475 0.4770,-0.1559 0.4770,-0.6308 0.4644,-0.6454 0.4582,-0.6475 -0.4603,-0.64'
        '75 -0.4686,-0.6433ZM0.1192,-0.2395 0.0586,-0.1789 0.0084,-0.1789 0.0063,-0.1810 0.0418,-0.2165 0.037'
        '7,-0.2207 -0.1192,-0.2207 -0.1213,-0.2228 -0.1213,-0.2542 -0.1192,-0.2563 0.0356,-0.2563 0.0397,-0.2'
        '626 0.0063,-0.2960 0.0084,-0.2981 0.0607,-0.2981ZM0.3556,-0.6077 0.3766,-0.6056 0.3975,-0.5952 0.414'
        '2,-0.5764 0.4226,-0.5471 0.4184,-0.5241 0.4100,-0.5094 0.3912,-0.4927 0.3619,-0.4843 0.3389,-0.4885 '
        '0.3201,-0.4990 0.3075,-0.5136 0.2992,-0.5345 0.3013,-0.5659 0.3138,-0.5868 0.3326,-0.6015Z'
    ),
    '640/3': (
        'M0.3201,-0.5743 0.3138,-0.5680 0.3096,-0.5575 0.3096,-0.5345 0.3159,-0.5199 0.3326,-0.5031 0.3452,-0'
        '.4969 0.3640,-0.4948 0.3849,-0.5010 0.3891,-0.5073ZM0.3347,-0.5910 0.3305,-0.5847 0.3996,-0.5178 0.4'
        '079,-0.5262 0.4100,-0.5324 0.4100,-0.5596 0.4017,-0.5764 0.3849,-0.5910 0.3661,-0.5973 0.3536,-0.597'
        '3Z'
    ),
    '640/4': (
        'M0.3494,-0.6077 0.3285,-0.5994 0.3117,-0.5847 0.2992,-0.5596 0.2992,-0.5324 0.3117,-0.5073 0.3285,-0'
        '.4927 0.3515,-0.4843 0.3703,-0.4843 0.3954,-0.4948 0.4100,-0.5094 0.4205,-0.5303 0.4226,-0.5533 0.41'
        '42,-0.5764 0.3954,-0.5973 0.3703,-0.6077ZM0.3159,-0.5680 0.3222,-0.5722 0.3870,-0.5052 0.3640,-0.496'
        '9 0.3452,-0.4990 0.3326,-0.5052 0.3180,-0.5199 0.3117,-0.5345 0.3117,-0.5575ZM0.3347,-0.5889 0.3536,'
        '-0.5952 0.3661,-0.5952 0.3912,-0.5847 0.3996,-0.5764 0.4079,-0.5596 0.4059,-0.5262 0.3996,-0.5199 0.'
        '3326,-0.5847Z'
    ),
    '640/5': (
        'M0.0711,0.5931 0.0628,0.5952 0.0481,0.5910 0.0397,0.5826 0.0356,0.5722 0.0042,0.6036 0.0607,0.6036ZM'
        '0.1151,0.5387 0.1130,0.5513 0.1192,0.5450ZM-0.1213,0.5262 -0.1213,0.5617 0.0314,0.5617 0.0230,0.5492'
        ' 0.0230,0.5366 0.0314,0.5241 -0.1192,0.5241ZM0.0042,0.4843 0.0356,0.5157 0.0397,0.5031 0.0481,0.4948'
        ' 0.0628,0.4906 0.0690,0.4927 0.0607,0.4843Z'
    ),
    '650.2/0': (
        'M-0.5994,-0.4789 -0.6114,-0.4608 -0.6175,-0.4337 -0.6175,0.4277 -0.6145,0.4488 -0.6054,0.4669 -0.587'
        '3,0.4849 -0.5542,0.4970 0.5542,0.4970 0.5813,0.4880 0.6024,0.4699 0.6145,0.4428 0.6145,-0.4458 0.605'
        '4,-0.4699 0.5873,-0.4880 0.5602,-0.5000 -0.5602,-0.5000 -0.5843,-0.4910Z'
    ),
    '650.2/1': (
        'M-0.5813,-0.4518 -0.5843,-0.4458 -0.5843,0.4428 -0.5693,0.4608 -0.5512,0.4669 0.5512,0.4669 0.5663,0'
        '.4608 0.5843,0.4398 0.5843,-0.4428 0.5693,-0.4639 0.5542,-0.4699 -0.5572,-0.4699ZM-0.0030,-0.4127 0.'
        '0301,-0.4066 0.0602,-0.3886 0.0753,-0.3705 0.0873,-0.3404 0.0873,-0.3012 0.0663,-0.2620 0.0301,-0.23'
        '80 0.0000,-0.2319 -0.0331,-0.2380 -0.0512,-0.2470 -0.0753,-0.2711 -0.0904,-0.3072 -0.0904,-0.3373 -0'
        '.0753,-0.3735 -0.0512,-0.3976 -0.0331,-0.4066Z'
    ),
    '650.2/2': (
        'M-0.0602,-0.3645 -0.0753,-0.3343 -0.0753,-0.3102 -0.0572,-0.2741 -0.0211,-0.2500 0.0000,-0.2470 0.03'
        '31,-0.2560 0.0422,-0.2651ZM-0.0361,-0.3886 -0.0452,-0.3795 0.0572,-0.2801 0.0663,-0.2892 0.0723,-0.3'
        '042 0.0723,-0.3404 0.0633,-0.3614 0.0392,-0.3855 0.0211,-0.3946 -0.0090,-0.3976Z'
    ),
    '650.2/3': (
        'M-0.0151,-0.4127 -0.0512,-0.3976 -0.0753,-0.3735 -0.0904,-0.3404 -0.0904,-0.3042 -0.0753,-0.2711 -0.'
        '0512,-0.2470 -0.0151,-0.2319 0.0120,-0.2319 0.0452,-0.2440 0.0753,-0.2741 0.0873,-0.3012 0.0873,-0.3'
        '434 0.0753,-0.3705 0.0452,-0.4006 0.0120,-0.4127ZM-0.0633,-0.3584 -0.0572,-0.3614 0.0392,-0.2651 0.0'
        '271,-0.2560 -0.0030,-0.2500 -0.0211,-0.2530 -0.0482,-0.2681 -0.0633,-0.2861 -0.0723,-0.3102 -0.0723,'
        '-0.3343ZM-0.0361,-0.3855 -0.0090,-0.3946 0.0211,-0.3916 0.0392,-0.3825 0.0602,-0.3614 0.0693,-0.3404'
        ' 0.0693,-0.3042 0.0572,-0.2831 -0.0422,-0.3795Z'
    ),
    '618.3/0': (
        'M-0.4720,-1.2690 -0.4920,-1.2530 -0.5000,-1.2350 -0.5000,1.2310 -0.4980,1.2390 -0.4860,1.2570 -0.474'
        '0,1.2650 -0.4600,1.2690 0.4580,1.2690 0.4720,1.2650 0.4880,1.2530 0.4960,1.2390 0.4980,1.2290 0.4980'
        ',-1.2330 0.4900,-1.2530 0.4800,-1.2630 0.4620,-1.2710 -0.4640,-1.2710Z'
    ),
    '618.3/1': (
        'M-0.4680,-0.0610 -0.4740,-0.0550 -0.4780,-0.0450 -0.4780,0.8930 -0.4740,0.9030 -0.4660,0.9110 -0.460'
        '0,0.9130 0.4580,0.9130 0.4640,0.9110 0.4740,0.9010 0.4760,0.8950 0.4760,-0.0470 0.4720,-0.0550 0.466'
        '0,-0.0610 0.4560,-0.0650 -0.4580,-0.0650ZM-0.0180,-0.7990 -0.0640,-0.7910 -0.0920,-0.7810 -0.1200,-0'
        '.7670 -0.1560,-0.7410 -0.1820,-0.7150 -0.2060,-0.6810 -0.2260,-0.6370 -0.2380,-0.5810 -0.2380,-0.543'
        '0 -0.2320,-0.5050 -0.2200,-0.4690 -0.1940,-0.4230 -0.1580,-0.3830 -0.1260,-0.3590 -0.0860,-0.3390 -0'
        '.0460,-0.3270 0.0080,-0.3230 0.0520,-0.3290 0.0900,-0.3410 0.1220,-0.3570 0.1420,-0.3710 0.1820,-0.4'
        '090 0.2060,-0.4430 0.2280,-0.4950 0.2360,-0.5350 0.2360,-0.5850 0.2280,-0.6270 0.2100,-0.6710 0.1800'
        ',-0.7150 0.1520,-0.7430 0.1180,-0.7670 0.0680,-0.7890 0.0340,-0.7970ZM-0.4740,-1.2390 -0.4780,-1.229'
        '0 -0.4780,-0.1050 -0.4740,-0.0970 -0.4660,-0.0890 -0.4600,-0.0870 0.4600,-0.0870 0.4740,-0.0990 0.47'
        '60,-0.1050 0.4760,-1.2310 0.4740,-1.2370 0.4600,-1.2490 -0.4620,-1.2490ZM-0.0280,-0.8570 0.0420,-0.8'
        '550 0.0920,-0.8430 0.1380,-0.8230 0.1860,-0.7910 0.2300,-0.7470 0.2560,-0.7090 0.2800,-0.6550 0.2940'
        ',-0.5870 0.2940,-0.5330 0.2900,-0.5050 0.2800,-0.4670 0.2620,-0.4250 0.2280,-0.3730 0.1880,-0.3330 0'
        '.1440,-0.3030 0.0900,-0.2790 0.0480,-0.2690 0.0140,-0.2650 -0.0380,-0.2670 -0.0980,-0.2810 -0.1600,-'
        '0.3110 -0.2040,-0.3450 -0.2380,-0.3830 -0.2720,-0.4410 -0.2860,-0.4790 -0.2960,-0.5350 -0.2960,-0.58'
        '90 -0.2860,-0.6430 -0.2780,-0.6670 -0.2580,-0.7090 -0.2320,-0.7470 -0.1960,-0.7850 -0.1480,-0.8190 -'
        '0.1200,-0.8330 -0.0820,-0.8470Z'
    ),
    '618.3/2': (
        'M-0.4800,0.9530 -0.4800,1.2290 -0.4780,1.2350 -0.4680,1.2450 -0.4580,1.2490 0.4560,1.2490 0.4660,1.2'
        '450 0.4740,1.2370 0.4780,1.2270 0.4780,0.9550 0.4740,0.9450 0.4640,0.9350 0.4580,0.9330 -0.4600,0.93'
        '30 -0.4660,0.9350 -0.4780,0.9470ZM-0.2620,0.9730 -0.2260,0.9730 -0.1980,0.9810 -0.1740,0.9950 -0.160'
        '0,1.0070 -0.1420,1.0310 -0.1300,1.0590 -0.1260,1.0810 -0.1260,1.1010 -0.1300,1.1230 -0.1400,1.1470 -'
        '0.1520,1.1650 -0.1720,1.1850 -0.2000,1.2010 -0.2300,1.2090 -0.2600,1.2090 -0.2780,1.2050 -0.3020,1.1'
        '950 -0.3200,1.1830 -0.3380,1.1650 -0.3460,1.1530 -0.3600,1.1210 -0.3640,1.0970 -0.3620,1.0690 -0.358'
        '0,1.0530 -0.3380,1.0170 -0.3180,0.9970 -0.3000,0.9850Z'
    ),
    '618.3/3': (
        'M-0.2460,0.9710 -0.2740,0.9750 -0.2920,0.9810 -0.3180,0.9970 -0.3380,1.0170 -0.3480,1.0310 -0.3600,1'
        '.0590 -0.3640,1.0990 -0.3580,1.1290 -0.3500,1.1470 -0.3380,1.1650 -0.3200,1.1830 -0.3060,1.1930 -0.2'
        '780,1.2050 -0.2600,1.2090 -0.2300,1.2090 -0.2100,1.2050 -0.1840,1.1930 -0.1720,1.1850 -0.1500,1.1630'
        ' -0.1300,1.1250 -0.1260,1.1050 -0.1260,1.0770 -0.1320,1.0510 -0.1440,1.0270 -0.1620,1.0050 -0.1980,0'
        '.9810 -0.2160,0.9750ZM-0.3200,1.0350 -0.1900,1.1650 -0.2080,1.1770 -0.2280,1.1830 -0.2620,1.1830 -0.'
        '2820,1.1770 -0.3020,1.1650 -0.3240,1.1410 -0.3320,1.1250 -0.3380,1.1030 -0.3360,1.0670ZM-0.2680,0.99'
        '90 -0.2320,0.9970 -0.2100,1.0030 -0.1860,1.0170 -0.1660,1.0390 -0.1520,1.0730 -0.1520,1.1090 -0.1640'
        ',1.1390 -0.1700,1.1450 -0.3000,1.0150ZM-0.0280,-0.8590 -0.0820,-0.8490 -0.1200,-0.8350 -0.1480,-0.82'
        '10 -0.1840,-0.7970 -0.2240,-0.7590 -0.2600,-0.7090 -0.2800,-0.6670 -0.2880,-0.6430 -0.2980,-0.5890 -'
        '0.2980,-0.5350 -0.2880,-0.4790 -0.2740,-0.4410 -0.2400,-0.3830 -0.2040,-0.3430 -0.1600,-0.3090 -0.09'
        '80,-0.2790 -0.0380,-0.2650 0.0140,-0.2630 0.0480,-0.2670 0.0900,-0.2770 0.1440,-0.3010 0.1880,-0.331'
        '0 0.2300,-0.3730 0.2640,-0.4250 0.2820,-0.4670 0.2920,-0.5050 0.2960,-0.5330 0.2960,-0.5870 0.2820,-'
        '0.6550 0.2580,-0.7090 0.2320,-0.7470 0.1860,-0.7930 0.1380,-0.8250 0.0920,-0.8450 0.0420,-0.8570ZM-0'
        '.0180,-0.7970 0.0340,-0.7950 0.0680,-0.7870 0.1180,-0.7650 0.1520,-0.7410 0.1780,-0.7150 0.2080,-0.6'
        '710 0.2260,-0.6270 0.2340,-0.5850 0.2340,-0.5350 0.2260,-0.4950 0.2040,-0.4430 0.1800,-0.4090 0.1420'
        ',-0.3730 0.1220,-0.3590 0.0900,-0.3430 0.0520,-0.3310 0.0080,-0.3250 -0.0460,-0.3290 -0.0860,-0.3410'
        ' -0.1260,-0.3610 -0.1580,-0.3850 -0.1920,-0.4230 -0.2180,-0.4690 -0.2300,-0.5050 -0.2360,-0.5430 -0.'
        '2360,-0.5810 -0.2240,-0.6370 -0.2040,-0.6810 -0.1800,-0.7150 -0.1560,-0.7390 -0.1200,-0.7650 -0.0920'
        ',-0.7790 -0.0640,-0.7890Z'
    ),
    '618.3/4': (
        'M-0.3200,1.0330 -0.3340,1.0550 -0.3400,1.0770 -0.3380,1.1130 -0.3220,1.1470 -0.3020,1.1670 -0.2900,1'
        '.1750 -0.2620,1.1850 -0.2280,1.1850 -0.2080,1.1790 -0.1940,1.1710 -0.1880,1.1650ZM-0.2980,1.0110 -0.'
        '3020,1.0150 -0.1700,1.1470 -0.1620,1.1390 -0.1500,1.1090 -0.1500,1.0730 -0.1580,1.0490 -0.1680,1.033'
        '0 -0.1860,1.0150 -0.1980,1.0070 -0.2320,0.9950 -0.2680,0.9970Z'
    ),
    '618.3/5': (
        'M-0.4660,-0.0630 -0.4640,-0.0650 0.4620,-0.0650 0.4640,-0.0630 0.4600,-0.0690 0.4620,-0.0870 0.4580,'
        '-0.0850 -0.4600,-0.0850 -0.4640,-0.0870 -0.4620,-0.0690Z'
    ),
    '660.6/0': (
        'M-0.4838,-0.5162 -0.4946,-0.5054 -0.5000,-0.4928 -0.5000,0.4910 -0.4928,0.5054 -0.4784,0.5180 -0.467'
        '6,0.5216 0.4658,0.5216 0.4802,0.5162 0.4928,0.5036 0.4982,0.4910 0.4982,-0.4928 0.4874,-0.5126 0.465'
        '8,-0.5234 -0.4676,-0.5234Z'
    ),
    '660.6/1': (
        'M-0.2351,-0.4279 -0.2495,-0.4315 -0.3541,-0.4315 -0.3577,-0.4279 -0.3577,-0.2297 -0.3541,-0.2261 -0.'
        '3180,-0.2261 -0.3144,-0.2297 -0.3144,-0.3054 -0.3126,-0.3072 -0.2459,-0.3054 -0.2243,-0.3144 -0.2099'
        ',-0.3306 -0.2045,-0.3450 -0.2063,-0.3973 -0.2153,-0.4135ZM-0.2514,-0.3883 -0.2495,-0.3523 -0.2568,-0'
        '.3432 -0.2640,-0.3396 -0.3126,-0.3396 -0.3144,-0.3414 -0.3144,-0.3937 -0.3126,-0.3955 -0.2676,-0.395'
        '5 -0.2658,-0.3973 -0.2568,-0.3937ZM-0.4694,-0.5018 -0.4784,-0.4928 -0.4802,-0.4874 -0.4802,0.4856 -0'
        '.4784,0.4910 -0.4712,0.4982 -0.4622,0.5018 0.4604,0.5018 0.4676,0.5000 0.4784,0.4874 0.4784,-0.4892 '
        '0.4676,-0.5018 0.4622,-0.5036 -0.4640,-0.5036ZM0.3270,-0.1721 0.4586,-0.1721 0.4604,-0.1703 0.4604,-'
        '0.0261 0.4586,-0.0243 0.3270,-0.0243 0.3252,-0.0261 0.3252,-0.1703ZM-0.4207,-0.4604 -0.4135,-0.4640 '
        '-0.1793,-0.4640 -0.1667,-0.4568 -0.1613,-0.4423 -0.1613,-0.2189 -0.1703,-0.2009 -0.1793,-0.1973 -0.1'
        '829,-0.1991 -0.4081,-0.1991 -0.4135,-0.1973 -0.4261,-0.2063 -0.4279,-0.2099 -0.4279,-0.4514Z'
    ),
    '660.6/2': (
        'M-0.2495,-0.3883 -0.2568,-0.3955 -0.2658,-0.3991 -0.2676,-0.3973 -0.3126,-0.3973 -0.3162,-0.3937 -0.'
        '3162,-0.3414 -0.3126,-0.3378 -0.2640,-0.3378 -0.2568,-0.3414 -0.2477,-0.3523ZM-0.4207,-0.4622 -0.429'
        '7,-0.4514 -0.4297,-0.2099 -0.4279,-0.2063 -0.4135,-0.1955 -0.4081,-0.1973 -0.1829,-0.1973 -0.1793,-0'
        '.1955 -0.1703,-0.1991 -0.1649,-0.2045 -0.1595,-0.2189 -0.1595,-0.4423 -0.1649,-0.4568 -0.1703,-0.462'
        '2 -0.1793,-0.4658 -0.4135,-0.4658ZM-0.2351,-0.4261 -0.2171,-0.4135 -0.2063,-0.3901 -0.2063,-0.3450 -'
        '0.2117,-0.3306 -0.2243,-0.3162 -0.2459,-0.3072 -0.3126,-0.3090 -0.3162,-0.3054 -0.3162,-0.2297 -0.31'
        '80,-0.2279 -0.3541,-0.2279 -0.3559,-0.2297 -0.3559,-0.4279 -0.3541,-0.4297 -0.2495,-0.4297Z'
    ),
    '660.6/3': (
        'M0.4604,-0.0387 0.4586,-0.0333 0.4514,-0.0261 0.4405,-0.0243 0.4604,-0.0243ZM0.3252,-0.0387 0.3252,-'
        '0.0243 0.3450,-0.0243 0.3342,-0.0261 0.3270,-0.0333ZM0.4405,-0.1721 0.4514,-0.1703 0.4586,-0.1631 0.'
        '4604,-0.1577 0.4604,-0.1721ZM0.3252,-0.1577 0.3270,-0.1631 0.3342,-0.1703 0.3450,-0.1721 0.3252,-0.1'
        '721Z'
    ),
    '660.7/0': (
        'M-0.4766,-1.1169 -0.4874,-1.1097 -0.4946,-1.1007 -0.5000,-1.0845 -0.5000,1.0827 -0.4964,1.0953 -0.47'
        '66,1.1151 -0.4604,1.1187 0.4586,1.1187 0.4694,1.1169 0.4802,1.1115 0.4910,1.1007 0.4982,1.0809 0.498'
        '2,-1.0827 0.4964,-1.0917 0.4910,-1.1025 0.4802,-1.1133 0.4604,-1.1205 -0.4622,-1.1205Z'
    ),
    '660.7/1': (
        'M-0.4802,0.7086 -0.4802,1.0809 -0.4784,1.0863 -0.4658,1.0971 0.4640,1.0971 0.4766,1.0845 0.4766,0.70'
        '50 0.4658,0.6942 0.4604,0.6924 -0.4622,0.6924 -0.4712,0.6960ZM0.3273,0.8381 0.4568,0.8381 0.4586,0.8'
        '399 0.4586,0.9838 0.4568,0.9856 0.3273,0.9856 0.3255,0.9838 0.3255,0.8399ZM-0.4712,-0.3201 -0.4802,-'
        '0.3076 -0.4802,0.6565 -0.4784,0.6619 -0.4694,0.6709 -0.4640,0.6727 0.4622,0.6727 0.4694,0.6691 0.476'
        '6,0.6601 0.4766,-0.3094 0.4658,-0.3219 0.4568,-0.3237 -0.4604,-0.3237ZM0.1061,0.3076 0.0522,0.3615 0'
        '.0072,0.3615 0.0054,0.3597 0.0360,0.3291 0.0324,0.3255 -0.1043,0.3255 -0.1061,0.3237 -0.1061,0.2914 '
        '-0.1043,0.2896 0.0324,0.2896 0.0360,0.2860 0.0054,0.2572 0.0072,0.2554 0.0540,0.2554ZM0.3255,-0.1781'
        ' 0.4568,-0.1781 0.4586,-0.1763 0.4586,-0.0324 0.4568,-0.0306 0.3255,-0.0306 0.3237,-0.0324 0.3237,-0'
        '.1763ZM-0.4802,-0.7320 -0.4802,-0.3597 -0.4784,-0.3543 -0.4658,-0.3435 0.4640,-0.3435 0.4766,-0.3561'
        ' 0.4766,-0.7356 0.4694,-0.7446 0.4622,-0.7482 -0.4640,-0.7482 -0.4694,-0.7464ZM0.3273,-0.6025 0.4568'
        ',-0.6025 0.4586,-0.6007 0.4586,-0.4586 0.4568,-0.4568 0.3273,-0.4568 0.3255,-0.4586 0.3255,-0.6007ZM'
        '-0.2050,-1.0342 -0.3183,-1.0342 -0.3219,-1.0306 -0.3219,-0.8345 -0.3183,-0.8309 -0.2824,-0.8309 -0.2'
        '788,-0.8345 -0.2788,-0.9065 -0.2770,-0.9083 -0.2050,-0.9101 -0.1906,-0.9155 -0.1745,-0.9317 -0.1673,'
        '-0.9550 -0.1691,-0.9982 -0.1763,-1.0144 -0.1888,-1.0270ZM-0.2788,-0.9982 -0.2770,-1.0000 -0.2266,-1.'
        '0000 -0.2212,-0.9982 -0.2122,-0.9874 -0.2140,-0.9532 -0.2248,-0.9442 -0.2770,-0.9442 -0.2788,-0.9460'
        'ZM-0.4802,-1.0845 -0.4802,-0.7842 -0.4766,-0.7770 -0.4640,-0.7680 0.4622,-0.7680 0.4694,-0.7716 0.47'
        '66,-0.7806 0.4766,-1.0863 0.4658,-1.0989 0.4604,-1.1007 -0.4622,-1.1007 -0.4712,-1.0971ZM0.2536,-0.8'
        '723 0.2014,-0.8183 0.1583,-0.8183 0.1565,-0.8201 0.1853,-0.8507 0.1817,-0.8543 0.0432,-0.8543 0.0414'
        ',-0.8561 0.0414,-0.8867 0.0432,-0.8885 0.1817,-0.8885 0.1853,-0.8921 0.1565,-0.9227 0.1583,-0.9245 0'
        '.2014,-0.9245ZM-0.3849,-1.0629 -0.3777,-1.0665 -0.1385,-1.0665 -0.1295,-1.0594 -0.1259,-1.0522 -0.12'
        '59,-0.8165 -0.1331,-0.8058 -0.1403,-0.8022 -0.3777,-0.8022 -0.3867,-0.8076 -0.3921,-0.8201 -0.3921,-'
        '1.0486Z'
    ),
    '660.7/2': (
        'M-0.2806,-0.9982 -0.2806,-0.9460 -0.2770,-0.9424 -0.2248,-0.9424 -0.2122,-0.9532 -0.2104,-0.9874 -0.'
        '2212,-1.0000 -0.2266,-1.0018 -0.2770,-1.0018ZM-0.3849,-1.0647 -0.3921,-1.0558 -0.3939,-1.0486 -0.393'
        '9,-0.8201 -0.3885,-0.8076 -0.3777,-0.8004 -0.1403,-0.8004 -0.1331,-0.8040 -0.1241,-0.8165 -0.1241,-1'
        '.0522 -0.1277,-1.0594 -0.1385,-1.0683 -0.3777,-1.0683ZM-0.1888,-1.0252 -0.1781,-1.0144 -0.1709,-0.99'
        '82 -0.1691,-0.9550 -0.1763,-0.9317 -0.1906,-0.9173 -0.2050,-0.9119 -0.2770,-0.9101 -0.2806,-0.9065 -'
        '0.2806,-0.8345 -0.2824,-0.8327 -0.3183,-0.8327 -0.3201,-0.8345 -0.3201,-1.0306 -0.3183,-1.0324 -0.20'
        '50,-1.0324Z'
    ),
    '660.7/3': (
        'M0.4586,0.9712 0.4568,0.9766 0.4496,0.9838 0.4388,0.9856 0.4586,0.9856ZM0.3255,0.9712 0.3255,0.9856 '
        '0.3453,0.9856 0.3345,0.9838 0.3273,0.9766ZM0.4388,0.8381 0.4496,0.8399 0.4568,0.8471 0.4586,0.8525 0'
        '.4586,0.8381ZM0.3255,0.8525 0.3273,0.8471 0.3345,0.8399 0.3453,0.8381 0.3255,0.8381ZM-0.4694,0.6942 '
        '-0.4622,0.6906 0.4604,0.6906 0.4676,0.6942 0.4640,0.6888 0.4658,0.6727 0.4622,0.6745 -0.4640,0.6745 '
        '-0.4676,0.6727 -0.4658,0.6888ZM0.0665,0.3453 0.0594,0.3471 0.0504,0.3453 0.0360,0.3309 0.0072,0.3597'
        ' 0.0522,0.3597ZM0.0971,0.3004 0.0989,0.3022 0.0971,0.3147 0.1043,0.3076ZM-0.1061,0.2914 -0.1061,0.32'
        '37 0.0306,0.3237 0.0234,0.3129 0.0234,0.3022 0.0306,0.2914ZM0.0072,0.2572 0.0342,0.2824 0.0486,0.268'
        '0 0.0576,0.2662 0.0647,0.2680 0.0540,0.2572ZM0.4586,-0.0450 0.4568,-0.0396 0.4496,-0.0324 0.4388,-0.'
        '0306 0.4586,-0.0306ZM0.3237,-0.0450 0.3237,-0.0306 0.3435,-0.0306 0.3327,-0.0324 0.3255,-0.0396ZM0.4'
        '388,-0.1781 0.4496,-0.1763 0.4568,-0.1691 0.4586,-0.1637 0.4586,-0.1781ZM0.3237,-0.1637 0.3255,-0.16'
        '91 0.3327,-0.1763 0.3435,-0.1781 0.3237,-0.1781ZM-0.4694,-0.3219 -0.4676,-0.3237 0.4640,-0.3237 0.46'
        '58,-0.3219 0.4622,-0.3273 0.4622,-0.3381 0.4658,-0.3435 0.4622,-0.3417 -0.4658,-0.3417 -0.4676,-0.34'
        '35 -0.4658,-0.3273ZM0.4586,-0.4712 0.4568,-0.4658 0.4496,-0.4586 0.4388,-0.4568 0.4586,-0.4568ZM0.32'
        '55,-0.4712 0.3255,-0.4568 0.3453,-0.4568 0.3345,-0.4586 0.3273,-0.4658ZM0.4388,-0.6025 0.4496,-0.600'
        '7 0.4568,-0.5935 0.4586,-0.5881 0.4586,-0.6025ZM0.3255,-0.5881 0.3273,-0.5935 0.3345,-0.6007 0.3453,'
        '-0.6025 0.3255,-0.6025ZM-0.4694,-0.7698 -0.4658,-0.7644 -0.4658,-0.7518 -0.4694,-0.7464 -0.4640,-0.7'
        '500 0.4622,-0.7500 0.4676,-0.7464 0.4640,-0.7518 0.4640,-0.7644 0.4676,-0.7698 0.4586,-0.7662 -0.460'
        '4,-0.7662ZM0.2158,-0.8345 0.2086,-0.8327 0.1996,-0.8345 0.1853,-0.8489 0.1583,-0.8201 0.2014,-0.8201'
        'ZM0.2446,-0.8795 0.2464,-0.8777 0.2446,-0.8633 0.2518,-0.8705ZM0.0432,-0.8867 0.0432,-0.8561 0.1817,'
        '-0.8561 0.1763,-0.8651 0.1763,-0.8777 0.1817,-0.8867ZM0.1583,-0.9227 0.1853,-0.8939 0.1996,-0.9083 0'
        '.2086,-0.9101 0.2158,-0.9083 0.2014,-0.9227Z'
    ),
    '638/0': (
        'M-1.0901,-0.4244 -1.1017,-0.3895 -1.1017,0.3837 -1.0727,0.4477 -1.0262,0.4826 -0.9855,0.4942 0.9738,'
        '0.4942 1.0378,0.4709 1.0727,0.4360 1.0843,0.4128 1.0959,0.3605 1.0959,-0.3663 1.0727,-0.4419 1.0378,'
        '-0.4767 1.0145,-0.4884 0.9622,-0.5000 -0.9680,-0.5000 -1.0262,-0.4884 -1.0669,-0.4593Z'
    ),
    '638/1': (
        'M-1.0320,-0.3953 -1.0378,-0.3779 -1.0378,0.3721 -1.0262,0.4012 -0.9855,0.4302 0.9738,0.4302 0.9913,0'
        '.4244 1.0262,0.3895 1.0320,0.3663 1.0320,-0.3721 1.0203,-0.4012 0.9855,-0.4302 0.9680,-0.4360 -0.973'
        '8,-0.4360 -0.9971,-0.4302Z'
    ),
}

# Plates: w, h, rx (face units), plate colour, traced layers (colour, PATHS key),
# legend lines (text, cx, cy of cap band, cap height, narrow, colour, Schedule 17 part) measured
# from the same diagram, and legend fields (validator S2).
PLATES: dict[str, dict] = {
    '2701': {
        'w': 3.1579,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '2701/0'), ('yellow', '2701/1')],
        'text': [('Oak Farm', 0.1155, -0.1901, 0.2515, 0.819, 'black', 2), ('Estate', 0.1272, 0.1608, 0.2515, 0.812, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.5063, -0.43, 1.5063, 0.427)],
    },
    '531.1A': {
        'w': 1.1976,
        'h': 1.058,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '531.1A/0')],
        'text': [('12\'-6"', 0.0063, 0.2729, 0.1438, 0.724, 'black', 2)],
        'over': [],
        'fields': [],
    },
    '675A': {
        'w': 1.0,
        'h': 1.4246,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '675A/0'), ('white', '675A/1'), ('red', '675A/2'), ('grey', '675A/3')],
        'text': [('20', -0.2591, 0.4791, 0.1474, 0.902, 'grey', 2), ('30', 0.0044, -0.2101, 0.3245, 0.979, 'black', 2), ('Zone', 0.1821, 0.3994, 0.0979, 0.796, 'black', 2), ('ENDS', 0.1859, 0.56, 0.1221, 1.002, 'black', 2)],
        'over': [('black', '675A/4')],
        'fields': [('rect', -0.46, -0.6696, 0.46, 0.2279), ('rect', -0.46, 0.2849, 0.46, 0.6696)],
    },
    '827.1': {
        'w': 1.0,
        'h': 1.0198,
        'rx': 0.0665,
        'plate': 'blue',
        'layers': [('white', '827.1/0')],
        'text': [('No A & E', 0.0036, 0.33, 0.1367, 0.847, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.48, -0.4895, 0.48, 0.4895)],
    },
    '958': {
        'w': 1.0,
        'h': 1.9011,
        'rx': 0.0482,
        'plate': 'blue',
        'layers': [('white', '958/0')],
        'text': [('authorised', -0.1103, -0.5906, 0.0887, 0.767, 'white', 1), ('vehicles', -0.1096, -0.4709, 0.0875, 0.765, 'white', 1), ('taxi', -0.3042, -0.1178, 0.0887, 0.735, 'white', 1), ('Mon - Fri', 0.0025, 0.5742, 0.0862, 0.709, 'white', 1), ('7 - 10 am', -0.0051, 0.7085, 0.0887, 0.667, 'white', 1), ('4.00 - 6.30 pm', -0.0038, 0.8295, 0.09, 0.753, 'white', 1), ('local', -0.0678, -0.8086, 0.0887, 0.808, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.472, -0.9221, 0.472, 0.4658), ('rect', -0.472, 0.4905, 0.472, 0.9221)],
    },
    '959B': {
        'w': 1.0,
        'h': 1.4055,
        'rx': 0.048,
        'plate': 'blue',
        'layers': [('white', '959B/0')],
        'text': [('authorised', -0.1098, -0.3381, 0.0878, 0.777, 'white', 1), ('vehicles', -0.1093, -0.2176, 0.0878, 0.764, 'white', 1), ('taxi', -0.3044, 0.1358, 0.0878, 0.743, 'white', 1), ('Mon - Fri', 0.0031, 0.3396, 0.0868, 0.707, 'white', 1), ('7 - 10 am', -0.0036, 0.4596, 0.0878, 0.676, 'white', 1), ('4.00 - 6.30 pm', -0.0036, 0.5807, 0.0909, 0.748, 'white', 1), ('local', -0.0674, -0.5577, 0.0878, 0.816, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.473, -0.6761, 0.263, 0.2305), ('rect', -0.473, 0.2558, 0.474, 0.6761)],
    },
    '960': {
        'w': 2.2086,
        'h': 1.0,
        'rx': 0.0708,
        'plate': 'blue',
        'layers': [('white', '960/0')],
        'text': [],
        'over': [],
        'fields': [],
    },
    'MARKER': {
        'w': 1.0,
        'h': 8.2635,
        'rx': 0,
        'plate': 'white',
        'layers': [('black', 'MARKER/0')],
        'text': [('A', 0.003, -1.1258, 0.6946, 0.845, 'white', 1), ('3', -0.015, -0.0359, 0.7186, 0.747, 'white', 1), ('0', 0.003, 0.8503, 0.7186, 0.913, 'white', 1), ('3', -0.015, 1.7425, 0.7066, 0.759, 'white', 1), ('W', 0.021, 3.0299, 0.6946, 0.912, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.5, -1.7305, 0.5, 3.6287)],
    },
    '618': {
        'w': 1.529,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '618/0'), ('white', '618/1')],
        'text': [('Play', -0.3152, -0.3305, 0.1264, 0.8469, 'black', 2), ('Street', 0.2307, -0.3273, 0.1377, 0.8149, 'black', 2), ('to sunset', 0.2464, -0.087, 0.1353, 0.7924, 'black', 2), ('am', -0.372, -0.0905, 0.1375, 0.7865, 'black', 2), ('except for', -0.0012, 0.1188, 0.1264, 0.8414, 'black', 2), ('access', 0.0, 0.3143, 0.1443, 0.7335, 'black', 2), ('8', -0.6014, -0.0894, 0.1353, 0.8269, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.7645, -0.5, 0.7645, 0.5)],
        'kind': 'plate',
    },
    '618.1': {
        'w': 1.3019,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '618.1/0'), ('white', '618.1/1')],
        'text': [('No vehicles', 0.006, -0.3249, 0.1377, 0.8008, 'black', 2), ('10 am - 4 pm', -0.0048, -0.0947, 0.1245, 0.7963, 'black', 2), ('except for', -0.0024, 0.1188, 0.1264, 0.8439, 'black', 2), ('access', -0.0024, 0.3136, 0.1409, 0.7528, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.651, -0.5, 0.651, 0.5)],
        'kind': 'plate',
    },
    '618.2': {
        'w': 0.951,
        'h': 1.0543,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '618.2/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'proh',
    },
    '618.3': {
        'w': 1.0,
        'h': 2.542,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '618.3/0'), ('white', '618.3/1'), ('yellow', '618.3/2'), ('red', '618.3/3'), ('blue', '618.3/4'), ('black', '618.3/5')],
        'text': [('PEDESTRIAN', 0.0, -1.164, 0.086, 0.9618, 'black', 2), ('ZONE', -0.004, -0.999, 0.14, 0.9818, 'black', 2), ('No vehicles', 0.005, -0.178, 0.086, 0.7956, 'black', 2), ('Except for', 0.005, 0.0181, 0.0781, 0.8657, 'black', 2), ('loading', -0.001, 0.1388, 0.0797, 0.8413, 'black', 2), ('Mon - Sat', 0.005, 0.288, 0.086, 0.7244, 'black', 2), ('Midnight - 11 am', 0.004, 0.4201, 0.0781, 0.7991, 'black', 2), ('4 pm - Midnight', 0.0, 0.5388, 0.0797, 0.8159, 'black', 2), ('Sunday', 0.002, 0.6848, 0.0797, 0.8884, 'black', 2), ('At any', -0.141, 0.8201, 0.0781, 0.859, 'black', 2), ('time', 0.169, 0.822, 0.082, 1.0861, 'black', 2), ('At', 0.055, 1.029, 0.084, 0.8486, 'black', 2), ('any', 0.259, 1.0262, 0.078, 0.8434, 'black', 2), ('time', 0.173, 1.148, 0.082, 0.8394, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -1.271, 0.5, 1.271)],
        'kind': 'plate',
    },
    '618.3A': {
        'w': 1.0,
        'h': 2.2437,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '618.3A/0'), ('white', '618.3A/1'), ('yellow', '618.3A/2'), ('red', '618.3A/3'), ('blue', '618.3A/4'), ('black', '618.3A/5')],
        'text': [('PEDESTRIAN', 0.0, -1.0073, 0.0917, 0.9858, 'black', 2), ('ZONE', -0.0052, -0.8344, 0.15, 0.9936, 'black', 2), ('No vehicles', 0.0052, 0.0396, 0.0896, 0.8399, 'black', 2), ('Except for', 0.0042, 0.3717, 0.083, 0.8894, 'black', 2), ('access', 0.0, 0.5012, 0.0955, 0.7507, 'black', 2), ('At', 0.0479, 0.8635, 0.0875, 0.8929, 'black', 2), ('any', 0.2698, 0.861, 0.0833, 0.858, 'black', 2), ('time', 0.176, 0.9906, 0.0875, 0.8627, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -1.1219, 0.5, 1.1219)],
        'kind': 'plate',
    },
    '618.4': {
        'w': 1.0,
        'h': 1.7167,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '618.4/0'), ('white', '618.4/1'), ('grey', '618.4/2'), ('black', '618.4/3')],
        'text': [('Pedestrian', 0.0137, 0.259, 0.1205, 0.7736, 'black', 2), ('Zone', 0.0106, 0.426, 0.1205, 0.7859, 'black', 2), ('ENDS', 0.0159, 0.6649, 0.1797, 1.012, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.8583, 0.5, 0.8583)],
        'kind': 'plate',
    },
    '622.9': {
        'w': 2.0594,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '622.9/0'), ('white', '622.9/1')],
        'text': [('No', 0.0068, -0.1826, 0.2511, 0.9073, 'black', 2), ('explosives', -0.0023, 0.153, 0.2283, 0.8514, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.0297, -0.5, 1.0297, 0.5)],
        'kind': 'plate',
    },
    '627.1': {
        'w': 2.6255,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('grey', '627.1/0'), ('white', '627.1/1'), ('black', '627.1/2')],
        'text': [('Except', -0.5532, -0.1818, 0.2194, 0.8979, 'black', 2), ('empty', 0.6, -0.1759, 0.2227, 0.8781, 'black', 2), ('vehicles', -0.0149, 0.166, 0.2426, 0.7801, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.3128, -0.5, 1.3128, 0.5)],
        'kind': 'plate',
    },
    '637.1': {
        'w': 1.047,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '637.1/0'), ('yellow', '637.1/1'), ('blue', '637.1/2'), ('red', '637.1/3'), ('black', '637.1/4')],
        'text': [('At', 0.2652, -0.3494, 0.1133, 0.8706, 'black', 2), ('any', 0.2652, -0.1896, 0.105, 0.8477, 'black', 2), ('time', 0.2652, -0.0235, 0.1133, 0.8394, 'black', 2), ('on', -0.2459, 0.1781, 0.1189, 0.7442, 'black', 2), ('verge', 0.1188, 0.1756, 0.1077, 0.8352, 'black', 2), ('footway', 0.1077, 0.3385, 0.1079, 0.8788, 'black', 2), ('or', -0.3425, 0.3411, 0.1189, 0.7444, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5235, -0.5, 0.5235, 0.5)],
        'kind': 'plate',
    },
    '637.2': {
        'w': 1.0,
        'h': 1.3077,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '637.2/0'), ('yellow', '637.2/1'), ('blue', '637.2/2'), ('red', '637.2/3')],
        'text': [('Pedestrian', 0.0014, -0.5041, 0.1126, 0.8104, 'black', 2), ('Zone', -0.0014, -0.3407, 0.1154, 0.7995, 'black', 2), ('At', -0.1621, 0.3283, 0.1126, 0.8857, 'black', 2), ('any', 0.1168, 0.3252, 0.1044, 0.8477, 'black', 2), ('time', -0.0027, 0.4904, 0.1126, 0.8317, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.6539, 0.5, 0.6539)],
        'kind': 'plate',
    },
    '637.3': {
        'w': 1.9231,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '637.3/0'), ('yellow', '637.3/1'), ('blue', '637.3/2'), ('red', '637.3/3'), ('black', '637.3/4')],
        'text': [('At', -0.4981, 0.0019, 0.1577, 0.8706, 'black', 2), ('any', -0.1135, -0.0025, 0.1462, 0.8477, 'black', 2), ('time', 0.3808, 0.0019, 0.1577, 0.8317, 'black', 2), ('1 May - 30 Sept', -0.0019, 0.2766, 0.1532, 0.8279, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.9616, -0.5, 0.9616, 0.5)],
        'kind': 'plate',
    },
    '638': {
        'w': 2.2035,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '638/0'), ('white', '638/1')],
        'text': [('No', -0.6424, -0.1802, 0.2442, 0.9368, 'black', 2), ('loading', 0.2936, -0.1638, 0.2771, 0.6929, 'black', 2), ('at', -0.7587, 0.1628, 0.2442, 0.7668, 'black', 2), ('time', 0.564, 0.1628, 0.2442, 0.8176, 'black', 2), ('any', -0.1192, 0.1558, 0.2326, 1.0531, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.1018, -0.5, 1.1018, 0.5)],
        'kind': 'plate',
    },
    '638.1': {
        'w': 1.2383,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '638.1/0'), ('white', '638.1/1'), ('black', '638.1/2')],
        'text': [('No loading', -0.0013, -0.3639, 0.1012, 0.8857, 'black', 2), ('Mon - Fri', 0.0, -0.171, 0.1088, 0.6981, 'black', 2), ('8.00 - 9.30', -0.1244, 0.0, 0.1088, 0.8228, 'black', 2), ('4.30 - 6.30pm', -0.0078, 0.1454, 0.0992, 0.9475, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.6191, -0.5, 0.6191, 0.5)],
        'kind': 'plate',
    },
    '639': {
        'w': 1.4061,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '639/0'), ('yellow', '639/1'), ('blue', '639/2'), ('red', '639/3'), ('black', '639/4')],
        'text': [('am-6', -0.0939, -0.0134, 0.1533, 0.904, 'black', 2), ('pm', 0.4195, -0.0167, 0.1418, 0.917, 'black', 2), ('8', -0.5153, -0.0134, 0.1533, 0.8077, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.703, -0.5, 0.703, 0.5)],
        'kind': 'plate',
    },
    '639.1B': {
        'w': 1.0,
        'h': 1.0665,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '639.1B/0'), ('white', '639.1B/1'), ('yellow', '639.1B/2'), ('blue', '639.1B/3'), ('red', '639.1B/4')],
        'text': [('Mon - Sat', 0.12, -0.4475, 0.0736, 0.7405, 'black', 2), ('8 -10', 0.035, -0.331, 0.0753, 0.7739, 'black', 2), ('am', 0.2566, -0.3316, 0.073, 0.8099, 'black', 2), ('4 - 6 pm', 0.113, -0.2301, 0.067, 0.7582, 'black', 2), ('Mon - Sat', 0.1489, -0.0525, 0.0753, 0.7244, 'black', 2), ('10', -0.0744, 0.063, 0.0753, 1.3691, 'black', 2), ('am - 4 pm', 0.2128, 0.0624, 0.067, 0.783, 'black', 2), ('1 hour', 0.1445, 0.1935, 0.0736, 0.7875, 'black', 2), ('No return', 0.0018, 0.3301, 0.0736, 0.8274, 'black', 2), ('within 2 hours', -0.0009, 0.4326, 0.0753, 0.7949, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.5333, 0.5, 0.5333)],
        'kind': 'plate',
    },
    '640': {
        'w': 1.0,
        'h': 1.3368,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '640/0'), ('white', '640/1'), ('yellow', '640/2'), ('blue', '640/3'), ('red', '640/4'), ('black', '640/5')],
        'text': [('Mon - Sat', -0.1444, -0.5335, 0.09, 0.7151, 'black', 2), ('am - 6.30 pm', 0.0544, -0.3995, 0.0817, 0.8244, 'black', 2), ('No loading', 0.0, -0.0292, 0.0817, 0.8891, 'black', 2), ('Mon - Fri', 0.001, 0.1266, 0.0879, 0.7015, 'black', 2), ('8.00 - 9.30', -0.0983, 0.2646, 0.0879, 0.8228, 'black', 2), ('am', 0.3431, 0.2635, 0.0901, 0.7825, 'black', 2), ('4.30 - 6.30', -0.1056, 0.387, 0.09, 0.7972, 'black', 2), ('pm', 0.3169, 0.3814, 0.0837, 1.1365, 'black', 2), ('8', -0.386, -0.3964, 0.0879, 0.7949, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.6684, 0.5, 0.6684)],
        'kind': 'plate',
    },
    '640.2A': {
        'w': 1.0,
        'h': 1.252,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '640.2A/0'), ('yellow', '640.2A/1'), ('blue', '640.2A/2'), ('red', '640.2A/3'), ('white', '640.2A/4'), ('black', '640.2A/5')],
        'text': [('5T', -0.127, -0.4385, 0.1331, 0.6469, 'white', 1), ('Mon -Fri', 0.002, -0.1804, 0.0847, 0.7772, 'black', 2), ('Midnight - 7', -0.0907, -0.0503, 0.0788, 0.7891, 'black', 2), ('am', 0.3387, -0.0491, 0.084, 0.8099, 'black', 2), ('8 pm - Midnight', 0.002, 0.0674, 0.0803, 0.8033, 'black', 2), ('Sat & Sun', -0.001, 0.2188, 0.0847, 0.84, 'black', 2), ('At', -0.2631, 0.3528, 0.0827, 0.8706, 'black', 2), ('any', -0.0585, 0.351, 0.0786, 0.8339, 'black', 2), ('time', 0.2046, 0.3528, 0.0827, 0.8394, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.626, 0.5, 0.626)],
        'kind': 'plate',
    },
    '640.3': {
        'w': 1.1313,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '640.3/0'), ('yellow', '640.3/1'), ('blue', '640.3/2'), ('red', '640.3/3')],
        'text': [('Loading', -0.1848, -0.3567, 0.1051, 0.8519, 'black', 2), ('area', 0.3217, -0.3548, 0.1148, 0.75, 'black', 2), ('Except by', 0.188, -0.1794, 0.0836, 0.8657, 'black', 2), ('permitted', 0.1831, -0.0537, 0.0823, 0.8914, 'black', 2), ('vehicles', 0.1823, 0.0762, 0.0891, 0.7967, 'black', 2), ('Mon - Fri', 0.0016, 0.2358, 0.0908, 0.6964, 'black', 2), ('am-6pm', 0.0519, 0.3732, 0.0836, 0.9939, 'black', 2), ('8', -0.2917, 0.376, 0.0891, 0.8224, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5656, -0.5, 0.5656, 0.5)],
        'kind': 'plate',
    },
    '640.4': {
        'w': 1.3742,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '640.4/0'), ('yellow', '640.4/1'), ('blue', '640.4/2'), ('red', '640.4/3')],
        'text': [('Except by', 0.2311, -0.3573, 0.1054, 0.8657, 'black', 2), ('permitted', 0.2239, -0.1986, 0.1038, 0.8941, 'black', 2), ('vehicles', 0.2229, -0.0337, 0.1145, 0.7779, 'black', 2), ('Mon - Fri', 0.0061, 0.1667, 0.1145, 0.6964, 'black', 2), ('am-6pm', 0.0675, 0.34, 0.1054, 0.9939, 'black', 2), ('8', -0.365, 0.3446, 0.1145, 0.7885, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.6871, -0.5, 0.6871, 0.5)],
        'kind': 'plate',
    },
    '642.3': {
        'w': 1.295,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '642.3/0'), ('yellow', '642.3/1'), ('red', '642.3/2'), ('blue', '642.3/3')],
        'text': [('No stopping', 0.0025, -0.085, 0.125, 0.8909, 'black', 2), ('except in', -0.0025, 0.124, 0.123, 0.85, 'black', 2), ('emergency', 0.0013, 0.315, 0.125, 0.8616, 'black', 2), ('4', 0.03, -0.3113, 0.1525, 0.6709, 'blue', 2)],
        'over': [],
        'fields': [('rect', -0.6475, -0.5, 0.6475, 0.5)],
        'kind': 'plate',
    },
    '650.1': {
        'w': 1.2342,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '650.1/0'), ('yellow', '650.1/1'), ('red', '650.1/2'), ('blue', '650.1/3')],
        'text': [('No stopping', 0.0015, -0.1038, 0.1197, 0.8867, 'black', 2), ('11 pm - 5 am', -0.003, 0.1172, 0.1173, 0.7646, 'black', 2), ('except taxis', 0.0, 0.3202, 0.115, 0.8773, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.6171, -0.5, 0.6171, 0.5)],
        'kind': 'plate',
    },
    '650.2': {
        'w': 1.2349,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '650.2/0'), ('yellow', '650.2/1'), ('blue', '650.2/2'), ('red', '650.2/3')],
        'text': [('No', -0.3328, -0.1009, 0.1295, 0.9009, 'black', 2), ('waiting', 0.1506, -0.1057, 0.12, 0.8518, 'black', 2), ('11 pm- 5', -0.113, 0.1179, 0.1153, 0.9216, 'black', 2), ('am', 0.3599, 0.1219, 0.1297, 0.7933, 'black', 2), ('except taxis', 0.0015, 0.3197, 0.1153, 0.8773, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.6175, -0.5, 0.6175, 0.5)],
        'kind': 'plate',
    },
    '650.3': {
        'w': 1.2934,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '650.3/0'), ('yellow', '650.3/1'), ('blue', '650.3/2'), ('red', '650.3/3')],
        'text': [('At', -0.4132, -0.0804, 0.1325, 0.8634, 'black', 2), ('any', -0.0915, -0.0849, 0.123, 0.8339, 'black', 2), ('time', 0.3218, -0.0804, 0.1325, 0.8251, 'black', 2), ('except taxis', 0.0032, 0.125, 0.1208, 0.8745, 'black', 2), ('11', -0.4416, 0.3155, 0.1293, 0.6917, 'black', 2), ('pm-5', -0.0521, 0.3124, 0.1232, 0.994, 'black', 2), ('am', 0.377, 0.3154, 0.1358, 0.7933, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.6467, -0.5, 0.6467, 0.5)],
        'kind': 'plate',
    },
    '660.3': {
        'w': 1.7337,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '660.3/0'), ('white', '660.3/1'), ('blue', '660.3/2'), ('black', '660.3/3')],
        'text': [('Resident', 0.144, -0.3297, 0.13, 0.8274, 'black', 2), ('permit', 0.1378, -0.1206, 0.1209, 0.8958, 'black', 2), ('holders', 0.1393, 0.0991, 0.1331, 0.7911, 'black', 2), ('only', 0.1362, 0.3078, 0.1234, 0.8617, 'black', 2), ('C', 0.6796, 0.2879, 0.1517, 0.8367, 'white', 1), ('A', 0.6827, -0.2879, 0.257, 0.9036, 'white', 1), ('B', 0.6858, 0.0, 0.257, 0.9581, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.8669, -0.5, 0.8669, 0.5)],
        'kind': 'plate',
    },
    '660.4': {
        'w': 2.1787,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '660.4/0'), ('white', '660.4/1'), ('blue', '660.4/2')],
        'text': [('Loading', 0.413, -0.1385, 0.2302, 0.6892, 'black', 2), ('only', 0.4082, 0.1306, 0.1887, 0.864, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.0894, -0.5, 1.0894, 0.5)],
        'kind': 'plate',
    },
    '660.5': {
        'w': 1.0,
        'h': 1.4927,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '660.5/0'), ('white', '660.5/1'), ('blue', '660.5/2'), ('black', '660.5/3')],
        'text': [('Mon- Sat', 0.1533, -0.6487, 0.0785, 0.7763, 'black', 2), ('9am -6pm', 0.1496, -0.5326, 0.0699, 0.9459, 'black', 2), ('Voucher', 0.1487, -0.3686, 0.0766, 0.777, 'black', 2), ('parking', 0.1478, -0.2636, 0.0713, 0.8497, 'black', 2), ('only', 0.1496, -0.1578, 0.0713, 0.8474, 'black', 2), ('2 hour limit', -0.0009, 0.0036, 0.0766, 0.8031, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.7463, 0.5, 0.7463)],
        'kind': 'plate',
    },
    '660.6': {
        'w': 1.0,
        'h': 1.0468,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '660.6/0'), ('white', '660.6/1'), ('blue', '660.6/2'), ('black', '660.6/3')],
        'text': [('Mon - Sat', 0.1631, -0.3937, 0.0757, 0.7469, 'black', 2), ('7am-7pm', 0.1568, -0.2745, 0.069, 1.0325, 'black', 2), ('Permit holders', -0.0658, -0.0964, 0.0757, 0.8086, 'black', 2), ('or', -0.0027, 0.0396, 0.0776, 0.7294, 'black', 2), ('20 mins', -0.0009, 0.1784, 0.0775, 0.8155, 'black', 2), ('No return', 0.0027, 0.3135, 0.0739, 0.8463, 'black', 2), ('within 40 mins', 0.0, 0.4189, 0.0757, 0.8353, 'black', 2), ('A', 0.3937, -0.0973, 0.1495, 0.9157, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.5, -0.5234, 0.5, 0.5234)],
        'kind': 'plate',
    },
    '660.7': {
        'w': 1.0,
        'h': 2.241,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '660.7/0'), ('white', '660.7/1'), ('blue', '660.7/2'), ('black', '660.7/3')],
        'text': [('Mon- Sat', 0.1538, -1.0063, 0.0773, 0.7931, 'black', 2), ('7-8am', -0.0045, -0.6718, 0.0773, 0.9152, 'black', 2), ('Permit holders', -0.0665, -0.5288, 0.0755, 0.8086, 'black', 2), ('only', 0.0, -0.4271, 0.0703, 0.864, 'black', 2), ('8am-7pm', 0.0009, -0.2483, 0.0717, 0.9934, 'black', 2), ('Permit holders', -0.0665, -0.1025, 0.0755, 0.8086, 'black', 2), ('or', -0.0018, 0.0332, 0.0774, 0.7294, 'black', 2), ('Pay at machine', 0.0027, 0.1707, 0.0717, 0.8395, 'black', 2), ('Display ticket', 0.0027, 0.4549, 0.0717, 0.8451, 'black', 2), ('Max stay 2 hours', 0.0036, 0.588, 0.0717, 0.8369, 'black', 2), ('7-9pm', -0.0045, 0.7664, 0.0689, 1.0364, 'black', 2), ('Permit holders', -0.0665, 0.9083, 0.0755, 0.8086, 'black', 2), ('only', 0.0, 1.0135, 0.0703, 0.864, 'black', 2), ('A', 0.393, -0.5288, 0.1475, 0.9146, 'white', 1), ('A', 0.3921, -0.1034, 0.1493, 0.9157, 'white', 1), ('A', 0.393, 0.9128, 0.1493, 0.9036, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.5, -1.1205, 0.5, 1.1205)],
        'kind': 'plate',
    },
    '661.1': {
        'w': 1.3773,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '661.1/0'), ('white', '661.1/1'), ('blue', '661.1/2')],
        'text': [('Mon - Sat', 0.2209, -0.3618, 0.1111, 0.7213, 'black', 2), ('8am-7pm', 0.2145, -0.1963, 0.1009, 1.0147, 'black', 2), ('20 mins', 0.2145, 0.0, 0.1111, 0.8196, 'black', 2), ('No return', 0.0, 0.2016, 0.1111, 0.7993, 'black', 2), ('within 40 mins', -0.0013, 0.3527, 0.1085, 0.833, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.6886, -0.5, 0.6886, 0.5)],
        'kind': 'plate',
    },
    '661.2A': {
        'w': 1.4055,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '661.2A/0'), ('white', '661.2A/1'), ('blue', '661.2A/2'), ('black', '661.2A/3')],
        'text': [('Pay at', 0.2622, -0.3368, 0.1191, 0.8246, 'black', 2), ('machine', 0.2561, -0.1524, 0.128, 0.8082, 'black', 2), ('Display', -0.2683, 0.3248, 0.1191, 0.8696, 'black', 2), ('ticket', 0.3476, 0.3308, 0.1311, 0.7806, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.7027, -0.5, 0.7027, 0.5)],
        'kind': 'plate',
    },
    '661.3A': {
        'w': 1.9386,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '661.3A/0'), ('white', '661.3A/1'), ('blue', '661.3A/2')],
        'text': [('Pay', 0.0487, -0.249, 0.141, 0.8325, 'black', 2), ('here', 0.5217, -0.2437, 0.1516, 0.7669, 'black', 2), ('at machine', 0.2996, -0.0307, 0.1516, 0.8021, 'black', 2), ('Display', -0.3195, 0.2889, 0.141, 0.8648, 'black', 2), ('ticket', 0.4079, 0.2942, 0.1516, 0.8014, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.9693, -0.5, 0.9693, 0.5)],
        'kind': 'plate',
    },
    '661.4': {
        'w': 2.3319,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '661.4/0'), ('white', '661.4/1'), ('blue', '661.4/2')],
        'text': [('Have', 0.1106, -0.2677, 0.1814, 0.8207, 'black', 2), ('you', 0.7124, -0.2718, 0.1726, 0.8244, 'black', 2), ('paid', 0.0973, -0.0171, 0.1694, 0.8579, 'black', 2), ('and', 0.6593, -0.0088, 0.1858, 0.7789, 'black', 2), ('displayed', 0.3606, 0.2413, 0.1728, 0.8082, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.166, -0.5, 1.166, 0.5)],
        'kind': 'plate',
    },
    '662': {
        'w': 1.0653,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '662/0'), ('white', '662/1'), ('blue', '662/2')],
        'text': [('Disc', -0.2257, -0.3505, 0.1248, 0.8012, 'black', 2), ('Zone', 0.203, -0.3505, 0.1248, 0.8017, 'black', 2), ('Mon- Sat', 0.1673, -0.1723, 0.0851, 0.7864, 'black', 2), ('8am-6pm', 0.1634, -0.0455, 0.0774, 1.0262, 'black', 2), ('30 mins', 0.1634, 0.104, 0.0832, 0.8412, 'black', 2), ('No return', 0.001, 0.2564, 0.0832, 0.8205, 'black', 2), ('within 1 hour', -0.002, 0.3733, 0.0832, 0.802, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5326, -0.5, 0.5326, 0.5)],
        'kind': 'plate',
    },
    '675B': {
        'w': 1.0,
        'h': 1.4232,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '675B/0'), ('white', '675B/1'), ('grey', '675B/2'), ('black', '675B/3')],
        'text': [('Zone', 0.1809, 0.3991, 0.0987, 0.7664, 'black', 2), ('ENDS', 0.1853, 0.5603, 0.1228, 0.99, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.7116, 0.5, 0.7116)],
        'kind': 'plate',
    },
    '878': {
        'w': 1.0,
        'h': 1.2791,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '878/0'), ('white', '878/1'), ('black', '878/2')],
        'text': [('Traffic', 0.0, 0.0439, 0.1473, 0.7599, 'black', 2), ('signal', 0.0, 0.2379, 0.1373, 0.8575, 'black', 2), ('cameras', 0.0, 0.4383, 0.1543, 0.742, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.6395, 0.5, 0.6395)],
        'kind': 'plate',
    },
    '880': {
        'w': 1.0,
        'h': 1.785,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '880/0'), ('white', '880/1'), ('black', '880/2'), ('red', '880/3')],
        'text': [('30', 0.0047, 0.3941, 0.3053, 0.9837, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.8925, 0.5, 0.8925)],
        'kind': 'plate',
    },
    '818.5': {
        'w': 1.0,
        'h': 1.3516,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '818.5/0'), ('white', '818.5/1'), ('red', '818.5/2'), ('black', '818.5/3')],
        'text': [('Low', -0.2116, -0.5779, 0.0989, 0.7523, 'white', 1), ('bridge', 0.1463, -0.5805, 0.0938, 0.7922, 'white', 1), ('south of', 0.0, -0.4453, 0.0989, 0.7583, 'white', 1), ('Maplebeck', 0.0074, -0.3169, 0.0905, 0.8481, 'white', 1), ('4.4m', -0.0032, 0.1084, 0.0737, 0.8063, 'black', 2), ('14-6"', 0.0021, 0.2095, 0.0653, 0.7663, 'black', 2), ('Alternative', 0.0011, 0.4389, 0.0989, 0.7383, 'white', 1), ('route via A123', 0.0, 0.5705, 0.1011, 0.7312, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.5, -0.6758, 0.5, 0.6758)],
        'kind': 'plate',
    },
    '636': {
        'w': 1.0,
        'h': 1.0105,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '636/0'), ('yellow', '636/1'), ('blue', '636/2'), ('red', '636/3')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'plate',
    },
    '640.1': {
        'w': 1.0,
        'h': 1.0545,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '640.1/0'), ('yellow', '640.1/1'), ('blue', '640.1/2'), ('red', '640.1/3')],
        'text': [('No', -0.0356, 0.0797, 0.1237, 0.9089, 'black', 2), ('loading', -0.0304, 0.2429, 0.1146, 0.8331, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.5272, 0.5, 0.5272)],
        'kind': 'plate',
    },
    '622.4': {
        'w': 1.0,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [],
        'text': [('No', 0.0042, -0.2437, 0.1008, 0.8836, 'black', 2), ('track', 0.0021, -0.1113, 0.0966, 0.8071, 'black', 2), ('laying', -0.0021, 0.0248, 0.1083, 0.6759, 'black', 2), ('vehicles', -0.0021, 0.1513, 0.1008, 0.7435, 'black', 2)],
        'over': [],
        'fields': [('circle', 0.0, 0.0, 0.4)],
        'kind': 'proh',
    },
    '640.5': {
        'w': 2.0629,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '640.5/0'), ('yellow', '640.5/1'), ('white', '640.5/2'), ('grey', '640.5/3')],
        'text': [('End of', 0.4969, -0.25, 0.1855, 0.7881, 'black', 2), ('loading', 0.4827, -0.0096, 0.1695, 0.836, 'black', 2), ('area', 0.4858, 0.2394, 0.1878, 0.7329, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.0314, -0.5, 1.0314, 0.5)],
        'kind': 'plate',
    },
    '647': {
        'w': 1.4196,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '647/0'), ('white', '647/1'), ('yellow', '647/2'), ('red', '647/3'), ('blue', '647/4')],
        'text': [('URBAN', 0.1482, -0.357, 0.119, 0.9961, 'black', 2), ('CLEARWAY', 0.1524, -0.1681, 0.1211, 0.9342, 'black', 2), ('End', 0.0104, 0.2276, 0.2443, 0.8175, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.7098, -0.5, 0.7098, 0.5)],
        'kind': 'plate',
    },
    '667': {
        'w': 1.0,
        'h': 1.6217,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '667/0'), ('white', '667/1'), ('blue', '667/2')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'plate',
    },
    '667.1': {
        'w': 1.313,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '667.1/0'), ('white', '667.1/1'), ('blue', '667.1/2')],
        'text': [('6pm-8', -0.1662, 0.2855, 0.1472, 0.9506, 'white', 1), ('am', 0.3975, 0.289, 0.1616, 0.7349, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.6565, -0.5, 0.6565, 0.5)],
        'kind': 'plate',
    },
    '667.2': {
        'w': 1.0,
        'h': 1.6245,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '667.2/0'), ('white', '667.2/1'), ('red', '667.2/2'), ('blue', '667.2/3')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'plate',
    },
    '668': {
        'w': 1.0,
        'h': 1.6272,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '668/0'), ('white', '668/1'), ('blue', '668/2')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'plate',
    },
    '668.1': {
        'w': 1.313,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '668.1/0'), ('white', '668.1/1'), ('blue', '668.1/2')],
        'text': [('pm - 8', -0.0693, 0.2855, 0.1472, 0.6474, 'white', 1), ('am', 0.3975, 0.289, 0.1616, 0.7349, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.6565, -0.5, 0.6565, 0.5)],
        'kind': 'plate',
    },
    '668.2': {
        'w': 1.0,
        'h': 1.6201,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '668.2/0'), ('white', '668.2/1'), ('red', '668.2/2'), ('blue', '668.2/3')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'plate',
    },
    '618.3B': {
        'w': 1.0,
        'h': 2.8493,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '618.3B/0'), ('white', '618.3B/1'), ('yellow', '618.3B/2'), ('red', '618.3B/3'), ('blue', '618.3B/4'), ('black', '618.3B/5')],
        'text': [('PEDESTRIAN', 0.0, -1.3065, 0.0937, 1.0183, 'black', 2), ('ZONE', -0.0051, -1.1273, 0.1548, 0.9695, 'black', 2), ('No', -0.2637, -0.2383, 0.0957, 0.9034, 'black', 2), ('vehicles', 0.111, -0.2383, 0.0957, 0.7612, 'black', 2), ('Mon- Sat', 0.0051, -0.0784, 0.0978, 0.7354, 'black', 2), ('10', -0.3004, 0.0662, 0.0937, 0.9421, 'black', 2), ('am-4', -0.0224, 0.0682, 0.0896, 0.9246, 'black', 2), ('pm', 0.2454, 0.0499, 0.1018, 0.7066, 'black', 2), ('Except', -0.1263, 0.336, 0.0875, 0.869, 'black', 2), ('and for', -0.001, 0.5397, 0.0957, 0.7496, 'black', 2), ('loading', -0.0937, 0.6647, 0.0891, 0.8271, 'black', 2), ('by', 0.2077, 0.666, 0.0875, 1.3179, 'black', 2), ('At', 0.0489, 1.168, 0.0937, 0.8782, 'black', 2), ('any', 0.2699, 1.1633, 0.0896, 0.7997, 'black', 2), ('time', 0.1752, 1.2963, 0.0937, 0.8085, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -1.4246, 0.5, 1.4246)],
        'kind': 'plate',
    },
    '618.3C': {
        'w': 1.0,
        'h': 2.8265,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '618.3C/0'), ('white', '618.3C/1'), ('yellow', '618.3C/2'), ('red', '618.3C/3'), ('blue', '618.3C/4'), ('black', '618.3C/5')],
        'text': [('PEDESTRIAN', -0.002, -1.2959, 0.0959, 0.9372, 'black', 2), ('and', -0.2429, -1.1663, 0.0939, 0.7785, 'black', 2), ('CYCLE', 0.0908, -1.1673, 0.0959, 1.0619, 'black', 2), ('ZONE', -0.0061, -0.9847, 0.1592, 0.943, 'black', 2), ('Mon- Sat', 0.0041, -0.0949, 0.098, 0.7354, 'black', 2), ('10', -0.302, 0.05, 0.0939, 0.9421, 'black', 2), ('am - 4', -0.0245, 0.05, 0.0939, 0.6656, 'black', 2), ('pm', 0.251, 0.0353, 0.1, 1.0059, 'black', 2), ('Except', -0.1286, 0.3204, 0.0877, 0.8643, 'black', 2), ('and for', -0.002, 0.5255, 0.0939, 0.7678, 'black', 2), ('loading', -0.0959, 0.6518, 0.0893, 0.8228, 'black', 2), ('by', 0.2102, 0.6518, 0.0893, 1.2551, 'black', 2), ('At', 0.049, 1.1541, 0.0939, 0.8647, 'black', 2), ('any', 0.2694, 1.1514, 0.0898, 0.7997, 'black', 2), ('time', 0.1745, 1.2827, 0.0939, 0.8085, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -1.4132, 0.5, 1.4132)],
        'kind': 'plate',
    },
    '651': {
        'w': 1.1115,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '651/0'), ('white', '651/1'), ('red', '651/2'), ('black', '651/3')],
        'text': [('No motor vehicles', -0.0018, -0.0827, 0.0857, 0.7132, 'black', 2), ('cycles animals', -0.0065, 0.0228, 0.0761, 0.7539, 'black', 2), ('pedestrians', 0.0006, 0.1334, 0.0743, 0.8523, 'black', 2), ('on mown', -0.1667, 0.2463, 0.0848, 0.7692, 'black', 2), ('verge', 0.2547, 0.2445, 0.0763, 0.811, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5557, -0.5, 0.5557, 0.5)],
        'kind': 'plate',
    },
    '954': {
        'w': 1.5134,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '954/0'), ('white', '954/1')],
        'text': [('Except', 0.0134, -0.1598, 0.2965, 0.6673, 'black', 2), ('buses', 0.0089, 0.1629, 0.2455, 0.803, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.7567, -0.5, 0.7567, 0.5)],
        'kind': 'plate',
    },
    '954.2': {
        'w': 2.2035,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '954.2/0'), ('white', '954.2/1')],
        'text': [('Except', 0.0111, -0.1584, 0.2938, 0.6673, 'black', 2), ('local buses', 0.0022, 0.1659, 0.2522, 0.7752, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.1018, -0.5, 1.1018, 0.5)],
        'kind': 'plate',
    },
    '957': {
        'w': 1.0,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('white', '957/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'mand',
    },
    '513.1': {
        'w': 1.6972,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '513.1/0'), ('white', '513.1/1')],
        'text': [('Adverse', -0.0035, -0.1813, 0.25, 0.7857, 'black', 2), ('camber', -0.0053, 0.1673, 0.25, 0.804, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.8486, -0.5, 0.8486, 0.5)],
        'kind': 'plate',
    },
    '532.3': {
        'w': 1.5099,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('red', '532.3/0'), ('white', '532.3/1'), ('black', '532.3/2')],
        'text': [('14-6', -0.0507, 0.2085, 0.1831, 0.6652, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.755, -0.5, 0.755, 0.5)],
        'kind': 'plate',
    },
    '548.1': {
        'w': 1.6352,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '548.1/0'), ('white', '548.1/1')],
        'text': [('When', -0.3685, -0.2779, 0.1712, 0.8544, 'black', 2), ('lights', 0.3722, -0.2831, 0.1609, 0.8807, 'black', 2), ('show', -0.0012, -0.036, 0.1737, 0.8364, 'black', 2), ('200 yds', 0.0, 0.2548, 0.1648, 0.9013, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.8176, -0.5, 0.8176, 0.5)],
        'kind': 'plate',
    },
    '553.2': {
        'w': 3.6014,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '553.2/0'), ('white', '553.2/1')],
        'text': [('Farm', -0.875, -0.0135, 0.3784, 0.7982, 'black', 2), ('traffic', 0.7365, -0.0135, 0.3919, 0.7693, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.8007, -0.5, 1.8007, 0.5)],
        'kind': 'plate',
    },
    '573': {
        'w': 1.5696,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '573/0'), ('white', '573/1'), ('black', '573/2')],
        'text': [('250', -0.3155, -0.212, 0.233, 0.9121, 'black', 2), ('yds', 0.3592, -0.2171, 0.2099, 0.8489, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.7848, -0.5, 0.7848, 0.5)],
        'kind': 'plate',
    },
    '575': {
        'w': 1.1913,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '575/0'), ('white', '575/1')],
        'text': [('Oncoming', -0.0021, -0.3179, 0.1397, 0.8657, 'black', 2), ('vehicles', -0.001, -0.1081, 0.1476, 0.7855, 'black', 2), ('in middle', 0.001, 0.0967, 0.1455, 0.8109, 'black', 2), ('of', -0.2505, 0.3025, 0.1497, 0.7935, 'black', 2), ('road', 0.131, 0.3035, 0.1476, 0.7649, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5957, -0.5, 0.5957, 0.5)],
        'kind': 'plate',
    },
    '775': {
        'w': 1.7469,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '775/0'), ('white', '775/1')],
        'text': [('KEEP', -0.0031, -0.2469, 0.175, 1.0, 'black', 2), ('CROSSING', -0.0078, 0.0, 0.1813, 1.009, 'black', 2), ('CLEAR', -0.0031, 0.2438, 0.1813, 0.9516, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.8734, -0.5, 0.8734, 0.5)],
        'kind': 'plate',
    },
    '783': {
        'w': 2.4007,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '783/0')],
        'text': [('DRIVERS', -0.594, -0.3422, 0.1667, 0.8992, 'white', 1), ('OF LARGE', 0.5408, -0.344, 0.1702, 0.9218, 'white', 1), ('OR SLOW VEHICLES', 0.0, -0.1206, 0.1702, 0.8591, 'white', 1), ('phone', 0.0, 0.101, 0.1524, 0.823, 'white', 1), ('before crossing', -0.0018, 0.292, 0.1939, 0.6099, 'white', 1)],
        'over': [],
        'fields': [('rect', -1.2004, -0.5, 1.2004, 0.5)],
        'kind': 'plate',
    },
    '786': {
        'w': 1.439,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '786/0'), ('white', '786/1')],
        'text': [('PARK HERE', 0.0026, -0.3143, 0.1481, 0.9495, 'black', 2), ('AND USE', -0.0065, -0.1104, 0.1506, 0.9599, 'black', 2), ('PHONE AT', 0.0091, 0.0948, 0.1506, 0.9287, 'black', 2), ('CROSSING', -0.0039, 0.2987, 0.1532, 0.9737, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.7195, -0.5, 0.7195, 0.5)],
        'kind': 'plate',
    },
    '787': {
        'w': 1.0,
        'h': 2.1616,
        'rx': 0.0,
        'plate': None,
        'layers': [('yellow', '787/0'), ('black', '787/1'), ('yellow', '787/2')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'plate',
    },
    '788': {
        'w': 1.0,
        'h': 1.9921,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '788/0'), ('yellow', '788/1'), ('black', '788/2')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'plate',
    },
    '883': {
        'w': 1.983,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('blue', '883/0')],
        'text': [("Turner's", -0.4252, -0.3129, 0.2041, 0.6858, 'white', 1), ('Green', 0.5289, -0.3129, 0.2041, 0.737, 'white', 1), ('Traffic calmed', -0.0102, 0.0238, 0.1973, 0.7409, 'white', 1), ('area', -0.0034, 0.2896, 0.2031, 0.703, 'white', 1)],
        'over': [],
        'fields': [('rect', -0.9915, -0.5, 0.9915, 0.5)],
        'kind': 'plate',
    },
    '884': {
        'w': 1.0,
        'h': 1.01,
        'rx': 0.0,
        'plate': None,
        'layers': [('primary', '884/0'), ('white', '884/1'), ('primary', '884/2')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'plate',
    },
    '551.1': {
        'w': 1.1875,
        'h': 1.0507,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '551.1/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'warn',
    },
    '773': {
        'w': 1.0,
        'h': 1.1801,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '773/0'), ('white', '773/1'), ('red', '773/2'), ('yellow', '773/3')],
        'text': [('STOP', 0.001, 0.1188, 0.1341, 0.9081, 'black', 2), ('when', -0.0038, 0.2883, 0.1092, 0.8215, 'black', 2), ('lights show', 0.0019, 0.4355, 0.1048, 0.837, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.59, 0.5, 0.59)],
        'kind': 'plate',
    },
    '544.2': {
        'w': 1.1875,
        'h': 1.0507,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '544.2/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'warn',
    },
    '551.2': {
        'w': 1.1875,
        'h': 1.0507,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '551.2/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'warn',
    },
    '581': {
        'w': 1.1875,
        'h': 1.0507,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '581/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'warn',
    },
    '582': {
        'w': 1.1875,
        'h': 1.0507,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '582/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'warn',
    },
    '772': {
        'w': 1.19,
        'h': 1.0485,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '772/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'warn',
    },
    '782': {
        'w': 1.1875,
        'h': 1.0507,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '782/0')],
        'text': [],
        'over': [],
        'fields': [],
        'kind': 'warn',
    },
    '513.2': {
        'w': 2.7227,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '513.2/0'), ('white', '513.2/1'), ('black', '513.2/2')],
        'text': [('Max', -0.7143, -0.1744, 0.2395, 0.8088, 'black', 2), ('speed', -0.7374, 0.1452, 0.2232, 0.8479, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.3614, -0.5, 1.3614, 0.5)],
        'kind': 'plate',
    },
    '530.1': {
        'w': 2.441,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '530.1/0'), ('white', '530.1/1')],
        'text': [('Overhanging', -0.0044, -0.1621, 0.3002, 0.6394, 'black', 2), ('building', -0.0044, 0.1016, 0.3036, 0.6362, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.2205, -0.5, 1.2205, 0.5)],
        'kind': 'plate',
    },
    '531.2': {
        'w': 1.0,
        'h': 1.1534,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '531.2/0'), ('white', '531.2/1')],
        'text': [('ARCH', -0.0072, -0.4305, 0.1166, 0.9767, 'black', 2), ('BRIDGE', 0.002, -0.2699, 0.1186, 0.9559, 'black', 2), ('High', 0.0031, -0.0629, 0.1278, 0.7484, 'black', 2), ('vehicles', -0.001, 0.0951, 0.1207, 0.7562, 'black', 2), ('middle', 0.1626, 0.2556, 0.1186, 0.7995, 'black', 2), ('use', -0.2822, 0.2539, 0.1221, 0.72, 'black', 2), ('of', -0.1994, 0.4162, 0.1207, 0.7964, 'black', 2), ('road', 0.1053, 0.4172, 0.1186, 0.762, 'black', 2)],
        'over': [],
        'fields': [('rect', -0.5, -0.5767, 0.5, 0.5767)],
        'kind': 'plate',
    },
    '572': {
        'w': 2.1229,
        'h': 1.0,
        'rx': 0.0,
        'plate': None,
        'layers': [('black', '572/0'), ('white', '572/1'), ('black', '572/2')],
        'text': [('mile', 0.2682, -0.0196, 0.3799, 0.814, 'black', 2)],
        'over': [],
        'fields': [('rect', -1.0615, -0.5, 1.0615, 0.5)],
        'kind': 'plate',
    },
}

def path(key: str, fill: str, transform: str = "") -> str:
    t = f' transform="{transform}"' if transform else ""
    return f'<path d="{PATHS[key]}" fill="{fill}" fill-rule="evenodd"{t}/>'
