using System;
using System.Collections.Generic;

namespace GridForge
{
    /// <summary>
    /// Frozen KYTS catalogue (spec 015 Appendix A). N = 412 = G 38 glyph + F 374 fallback.
    /// Tokenizer is longest-code match; unlisted OSM numbers use FallbackFamily, never a cube.
    /// </summary>
    public enum TsrgdFamily
    {
        WarnTriangle, GiveWay, Stop, Prohibitory, National, Mandatory,
        InfoBlue, DirPrimary, DirLocal, DirMotorway, TouristBrown, WorksRed,
        SignalHead, PedHead, MatrixMS4, Countdown, Marker
    }

    public enum TsrgdMount
    {
        Post, TwoPost, Cantilever, PortalGantry, Belisha, SignalHead, Refuge610, MarkerPost, StreetName
    }

    public struct TsrgdRow
    {
        public string Code;
        public int Chapter;
        public TsrgdFamily Family;
        public TsrgdMount Mount;
        public string SitingId;
        public string V1;
        public TsrgdRow(string code, int chapter, TsrgdFamily family, TsrgdMount mount, string sitingId, string v1)
        {
            Code = code; Chapter = chapter; Family = family; Mount = mount; SitingId = sitingId; V1 = v1;
        }
    }

    public static class UkTsrgdCatalogue
    {
        public const int GlyphCount = 38;
        public const int FallbackCount = 374;
        public const int N = 412;

        static readonly Dictionary<string, TsrgdRow> ByCode;
        static readonly string[] CodesLongestFirst;
        static readonly TsrgdRow[] AllRows;

        static UkTsrgdCatalogue()
        {
            var rows = new TsrgdRow[]
            {
                new TsrgdRow("670", 5, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("671", 5, TsrgdFamily.National, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("602", 4, TsrgdFamily.GiveWay, TsrgdMount.Post, "gw_stop", "glyph"),
                new TsrgdRow("601.1", 4, TsrgdFamily.Stop, TsrgdMount.Post, "gw_stop", "glyph"),
                new TsrgdRow("611.1", 4, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("616", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "both_kerbs", "glyph"),
                new TsrgdRow("610", 4, TsrgdFamily.Mandatory, TsrgdMount.Refuge610, "refuge", "glyph"),
                new TsrgdRow("543", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("544", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("545", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("510", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("3000", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "glyph"),
                new TsrgdRow("4003", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "glyph"),
                new TsrgdRow("BELISHA", 20, TsrgdFamily.PedHead, TsrgdMount.Belisha, "crossing", "glyph"),
                new TsrgdRow("801", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("2025", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "glyph"),
                new TsrgdRow("2101", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "glyph"),
                new TsrgdRow("2701", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "glyph"),
                new TsrgdRow("2202", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "glyph"),
                new TsrgdRow("GANTRY_ADS", 14, TsrgdFamily.DirMotorway, TsrgdMount.PortalGantry, "portal", "glyph"),
                new TsrgdRow("530", 6, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "stack", "glyph"),
                new TsrgdRow("532.2", 6, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "stack", "glyph"),
                new TsrgdRow("629.2A", 6, TsrgdFamily.Prohibitory, TsrgdMount.Post, "stack", "glyph"),
                new TsrgdRow("611", 4, TsrgdFamily.Mandatory, TsrgdMount.Refuge610, "refuge", "glyph"),
                new TsrgdRow("674", 5, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("675", 5, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("823", 14, TsrgdFamily.Countdown, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("824", 14, TsrgdFamily.Countdown, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("825", 14, TsrgdFamily.Countdown, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("3014", 7, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "wigwag", "glyph"),
                new TsrgdRow("953", 9, TsrgdFamily.Mandatory, TsrgdMount.Post, "both_kerbs", "glyph"),
                new TsrgdRow("2911", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "glyph"),
                new TsrgdRow("2901", 14, TsrgdFamily.DirMotorway, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("2931", 14, TsrgdFamily.DirMotorway, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("640.2A", 22, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "glyph"),
                new TsrgdRow("MS4", 14, TsrgdFamily.MatrixMS4, TsrgdMount.PortalGantry, "portal", "glyph"),
                new TsrgdRow("MARKER", 14, TsrgdFamily.Marker, TsrgdMount.MarkerPost, "marker", "glyph"),
                new TsrgdRow("XING_PAR", 20, TsrgdFamily.PedHead, TsrgdMount.Belisha, "crossing", "glyph"),
                new TsrgdRow("504.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("504.2", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("505.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("506.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("507.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("508.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("509.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("512", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("512.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("512.2", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("513", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("513.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("513.2", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("516", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("517", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("521", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("522", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("523.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("524.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("526", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("528", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("529.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("531.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("544.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("544.2", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("546", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("547", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("548", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("548.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("549", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("550", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("550.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("550.2", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("551", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("551.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("551.2", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("552", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("553.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("553.2", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("554", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("554.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("554.2", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("555", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("556", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("556.1", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("557", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("558", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("559", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("562", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("572", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("573", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("574", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("575", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("581", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("582", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("583", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("584", 3, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("606", 4, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("607", 4, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("608", 4, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("609", 4, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("612", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("613", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("614", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("615", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("617", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("618", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("619", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("619.1", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("619.2", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("622.1A", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("622.2", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("622.4", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("622.5", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("622.6", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("622.7", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("622.8", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("622.9", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("625.1", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("626.2A", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("627.1", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("629", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("629.1", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("629.2", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("632", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("636", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("637.1", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("638", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("638.1", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("639", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("639.1B", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("640", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("642", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("642.2", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("642.3", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("646", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("647", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("649.1", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("649.2", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("650.1", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("650.2", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("650.3", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("651", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("652", 4, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("811", 4, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("811.1", 4, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("672", 5, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("673", 5, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("675A", 5, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("530.1", 6, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "stack", "fallback"),
                new TsrgdRow("531.2", 6, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "stack", "fallback"),
                new TsrgdRow("532.3", 6, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "stack", "fallback"),
                new TsrgdRow("533", 6, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "stack", "fallback"),
                new TsrgdRow("534", 6, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "stack", "fallback"),
                new TsrgdRow("770", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("771", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("772", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("773", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("774", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("775", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("776", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("777", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("778", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("779", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("780.1", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("780.2", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("781", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("782", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("783", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("784", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("785", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("786", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("787", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("788", 7, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("953.1", 8, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("953.2", 8, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("954", 8, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("954.2", 8, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("978", 8, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("979", 8, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("952", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("954.5", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("955", 9, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("956", 9, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("957", 9, TsrgdFamily.Mandatory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("958", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("958.1", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("959", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("959.1", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("960", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("960.1", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("962", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("962.1", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("962.2", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("963", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("964", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("965", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("967", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("968", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("968.1", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("969", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("974", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("975", 9, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("618.1", 10, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("618.2", 10, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("618.3", 10, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("618.3A", 10, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("618.3B", 10, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("618.3C", 10, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("618.4", 10, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("637.2", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("637.3", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("640.1", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("640.3", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("640.4", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("640.5", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("660", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("660.3", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("660.4", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("660.5", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("660.6", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("660.7", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("661.1", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("661.2A", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("661.3A", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("661.4", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("662", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("667", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("667.1", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("667.2", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("668", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("668.1", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("668.2", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("669", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("669.1", 11, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("883", 13, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("884", 13, TsrgdFamily.WarnTriangle, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("2702", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2703", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2704", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2705", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2706", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2707", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2708", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2710", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2711", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2712", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2713", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2713.1", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2714", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2715", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2716", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2717", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2720", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2721", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2722", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2723", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2724", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2725", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2726", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2727", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2728", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2729", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2730", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2731", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2732", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2733", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2734", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2735", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2736", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2737", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2738", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2740", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2902", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2902.1", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2903", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2904", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2904.1", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2905", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2908", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2908.1", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2910", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2913", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2913.1", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2914", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2915", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2920", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2921", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2922", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2924", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2925", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2926", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2927", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2928", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2929", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2930", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2932", 14, TsrgdFamily.DirMotorway, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2026", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2027", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2028", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2029", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2030", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2031", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2032", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2033", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2034", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2035", 15, TsrgdFamily.DirPrimary, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2102", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2103", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2104", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2111", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2112", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2113", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2114", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2115", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2116", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2117", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2118", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2120", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2121", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2122", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2123", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2124", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2125", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2126", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2127", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2128", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2130", 15, TsrgdFamily.DirLocal, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2201", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2203", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2204", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2205", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2206", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2207", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2208", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2209", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2210", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2301", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2302", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2303", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2304", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2305", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2306", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2307", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2308", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2310", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2311", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2313", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2314", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2315", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2316", 15, TsrgdFamily.TouristBrown, TsrgdMount.TwoPost, "verge_std", "fallback"),
                new TsrgdRow("2601", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2601.1", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2602", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2602.1", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2603", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2604", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2605", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2606", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2607", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2608", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2609", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2610", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2610.1", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2610.2", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("2611", 16, TsrgdFamily.DirLocal, TsrgdMount.Post, "footway_dir", "fallback"),
                new TsrgdRow("802", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("803.1", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("804.1", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("814", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("816", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("816.1", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("818.1", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("818.2", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("818.3", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("818.4", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("820", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("821", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("822", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("829.1", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("832", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("833", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("834", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("835", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("836", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("837", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("857", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("872", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("873", 17, TsrgdFamily.InfoBlue, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("3000.2", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3000.7", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3001", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3001.2", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3011", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3013", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3013.1", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3013.2", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3013.3", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3013.4", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("3013.5", 18, TsrgdFamily.SignalHead, TsrgdMount.SignalHead, "signals", "fallback"),
                new TsrgdRow("4002", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("4002.1", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("4003.1", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("4003.2", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("4003.3", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("4003.4", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("4003.5", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("4003.6", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("4003.7", 20, TsrgdFamily.PedHead, TsrgdMount.SignalHead, "crossing", "fallback"),
                new TsrgdRow("878", 22, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("880", 22, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("951", 22, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("640.2B", 22, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
                new TsrgdRow("818.5", 22, TsrgdFamily.Prohibitory, TsrgdMount.Post, "verge_std", "fallback"),
            };
            AllRows = rows;
            ByCode = new Dictionary<string, TsrgdRow>(rows.Length, StringComparer.OrdinalIgnoreCase);
            for (var i = 0; i < rows.Length; i++)
                ByCode[rows[i].Code] = rows[i];
            var keys = new string[rows.Length];
            for (var i = 0; i < rows.Length; i++) keys[i] = rows[i].Code;
            Array.Sort(keys, (a, b) => b.Length != a.Length ? b.Length.CompareTo(a.Length) : string.Compare(a, b, StringComparison.OrdinalIgnoreCase));
            CodesLongestFirst = keys;
        }

        public static IReadOnlyList<TsrgdRow> All => AllRows;

        public static bool TryGet(string token, out TsrgdRow row, out int param)
        {
            row = default;
            param = 0;
            if (string.IsNullOrWhiteSpace(token)) return false;
            SplitToken(token, out var code, out param);
            if (code.Length == 0) return false;
            if (ByCode.TryGetValue(code, out row)) return true;
            for (var i = 0; i < CodesLongestFirst.Length; i++)
            {
                var k = CodesLongestFirst[i];
                if (code.StartsWith(k, StringComparison.OrdinalIgnoreCase) &&
                    (code.Length == k.Length || !char.IsDigit(code[k.Length])))
                {
                    row = ByCode[k];
                    return true;
                }
            }
            return false;
        }

        public static TsrgdFamily FallbackFamily(string token)
        {
            SplitToken(token, out var code, out _);
            if (code.Length == 0) return TsrgdFamily.InfoBlue;
            var u = code.ToUpperInvariant();
            if (u == "BELISHA" || u == "XING_PAR") return TsrgdFamily.PedHead;
            if (u == "GANTRY_ADS") return TsrgdFamily.DirMotorway;
            if (u == "MS4") return TsrgdFamily.MatrixMS4;
            if (u == "MARKER") return TsrgdFamily.Marker;
            var n = LeadingInt(code);
            if (n >= 500 && n <= 599) return TsrgdFamily.WarnTriangle;
            if (u == "601" || u.StartsWith("601.")) return TsrgdFamily.Stop;
            if (u == "602") return TsrgdFamily.GiveWay;
            if (u == "610" || u == "611") return TsrgdFamily.Mandatory;
            if (u == "611.1") return TsrgdFamily.Mandatory;
            if (n >= 606 && n <= 611) return TsrgdFamily.Mandatory;
            if (u == "616") return TsrgdFamily.Prohibitory;
            if (n >= 612 && n <= 669) return TsrgdFamily.Prohibitory;
            if (n >= 670 && n <= 679) return TsrgdFamily.Prohibitory;
            if (u == "823" || u == "824" || u == "825") return TsrgdFamily.Countdown;
            if (n >= 800 && n <= 899) return TsrgdFamily.InfoBlue;
            if (n >= 2000 && n <= 2099) return TsrgdFamily.DirPrimary;
            if (n >= 2100 && n <= 2199) return TsrgdFamily.DirLocal;
            if (n >= 2200 && n <= 2399) return TsrgdFamily.TouristBrown;
            if (n >= 2600 && n <= 2699) return TsrgdFamily.DirLocal;
            if (n >= 2700 && n <= 2799) return TsrgdFamily.DirMotorway;
            if (n >= 2900 && n <= 2999) return TsrgdFamily.DirMotorway;
            if (u == "3014") return TsrgdFamily.SignalHead;
            if (n >= 3000 && n <= 3999) return TsrgdFamily.SignalHead;
            if (n >= 4000 && n <= 4999) return TsrgdFamily.PedHead;
            if (n >= 7000 && n <= 7999) return TsrgdFamily.WorksRed;
            return TsrgdFamily.InfoBlue;
        }

        public static TsrgdMount FallbackMount(TsrgdFamily f)
        {
            switch (f)
            {
                case TsrgdFamily.DirPrimary:
                case TsrgdFamily.DirLocal:
                case TsrgdFamily.DirMotorway:
                case TsrgdFamily.TouristBrown: return TsrgdMount.TwoPost;
                case TsrgdFamily.MatrixMS4: return TsrgdMount.PortalGantry;
                case TsrgdFamily.SignalHead:
                case TsrgdFamily.PedHead: return TsrgdMount.SignalHead;
                case TsrgdFamily.Marker: return TsrgdMount.MarkerPost;
                case TsrgdFamily.Countdown: return TsrgdMount.Post;
                default: return TsrgdMount.Post;
            }
        }

        public static List<(TsrgdRow row, int param)> ParseAll(string trafficSign, int max = 4)
        {
            var list = new List<(TsrgdRow, int)>(4);
            if (string.IsNullOrWhiteSpace(trafficSign)) return list;
            if (max < 1) max = 1;
            if (max > 4) max = 4;
            var parts = trafficSign.Split(new[] { ';', '|' }, StringSplitOptions.RemoveEmptyEntries);
            foreach (var part in parts)
            {
                if (list.Count >= max) break;
                var raw = StripNs(part.Trim());
                if (raw.Length == 0) continue;
                TsrgdRow row;
                int param;
                if (TryGet(raw, out row, out param))
                {
                    list.Add((row, param));
                    continue;
                }
                SplitToken(raw, out var code, out param);
                if (code.Length == 0) continue;
                var fam = FallbackFamily(code);
                row = new TsrgdRow(code, 0, fam, FallbackMount(fam), "verge_std", "fallback");
                list.Add((row, param));
            }
            return list;
        }

        public static string SelfTest()
        {
            if (AllRows.Length != N) return "N rows " + AllRows.Length + " != " + N;
            var g = 0; var f = 0;
            var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            for (var i = 0; i < AllRows.Length; i++)
            {
                var r = AllRows[i];
                if (!seen.Add(r.Code)) return "dup " + r.Code;
                if (r.V1 == "glyph") g++;
                else if (r.V1 == "fallback") f++;
                else return "bad v1 " + r.Code;
            }
            if (g != GlyphCount) return "G " + g + " != " + GlyphCount;
            if (f != FallbackCount) return "F " + f + " != " + FallbackCount;
            TsrgdRow row; int p;
            if (!TryGet("611", out row, out p) || row.Code != "611" || row.V1 != "glyph") return "611 not glyph";
            if (!TryGet("611.1", out row, out p) || row.Code != "611.1") return "611.1 miss";
            if (!TryGet("629.2A", out row, out p) || row.Code != "629.2A") return "629.2A miss";
            if (!TryGet("823", out row, out p) || row.Family != TsrgdFamily.Countdown) return "823 not countdown";
            if (FallbackFamily("9999") != TsrgdFamily.InfoBlue) return "9999 not InfoBlue";
            if (FallbackFamily("512.9") != TsrgdFamily.WarnTriangle) return "512.9 not warn";
            if (FallbackFamily("7001") != TsrgdFamily.WorksRed) return "7001 crash/family";
            var stacked = ParseAll("GB:543;GB:573");
            if (stacked.Count != 2) return "stack count " + stacked.Count;
            return null;
        }

        public static string StripNs(string s)
        {
            if (string.IsNullOrEmpty(s)) return "";
            var colon = s.IndexOf(':');
            if (colon > 0 && colon < 4) return s.Substring(colon + 1).Trim();
            return s.Trim();
        }

        static void SplitToken(string token, out string code, out int param)
        {
            param = 0;
            code = "";
            if (string.IsNullOrWhiteSpace(token)) return;
            var s = StripNs(token).Trim();
            s = s.Replace("_", "");
            var lb = s.IndexOf('[');
            if (lb >= 0)
            {
                var rb = s.IndexOf(']', lb + 1);
                var inside = rb > lb ? s.Substring(lb + 1, rb - lb - 1) : s.Substring(lb + 1);
                var digits = "";
                for (var i = 0; i < inside.Length; i++)
                    if (char.IsDigit(inside[i])) digits += inside[i];
                int.TryParse(digits, out param);
                s = s.Substring(0, lb);
            }
            code = s.Trim();
        }

        static int LeadingInt(string code)
        {
            var n = 0;
            var any = false;
            for (var i = 0; i < code.Length; i++)
            {
                if (!char.IsDigit(code[i])) break;
                any = true;
                n = n * 10 + (code[i] - '0');
            }
            return any ? n : -1;
        }
    }
}

