/* 原聲帶四首。file 是完整版（遊戲裡用的是切好的循環版），cover 是曲目封面，slides 是播放時依序換上的背景（照劇情順序）。
   line 取自信裡的原句。路徑都相對於 assets/。dur 是完整版的秒數。 */
window.TRACKS = [
  { n: 1, file: "audio/full/theme.mp3", title: "A Letter at the Dresser", scene: "主題曲：信的開頭，三條線共用", dur: 165,
    line: "他叫程徹，是一個話很少的人。有一天，他把一副新鑰匙放在我手心，只說了一句：「多打的。」",
    cover: "art/cg/C01_v1.webp", pos: "50% 50%", slides: ["art/cg/C01_v1.webp", "art/cg/C02_v1.webp", "art/cg/C10_v1.webp", "art/cg/C20_v1.webp", "art/cg/C22_v1.webp", "art/cg/C26_v1.webp", "art/cg/C28_v1.webp"] },
  { n: 2, file: "audio/full/normal.mp3", title: "Keys on the Hook", scene: "客廳線：房門外的客廳，和十一年後", dur: 144,
    line: "接力賽裡，交棒以後，跑完的人會停在跑道旁邊，看著下一棒越跑越遠。媽媽現在就站在那裡。",
    cover: "art/cg/N01_v1.webp", pos: "50% 50%", slides: ["art/cg/N01_v1.webp", "art/cg/N02_v1.webp", "art/cg/N04_v1.webp", "art/cg/NS01_v1.webp", "art/cg/NS05_v1.webp"] },
  { n: 3, file: "audio/full/tragic.mp3", title: "After the Finish Line", scene: "照片線：牆上的照片，和回家的那一天", dur: 174,
    line: "接力賽裡，有時候也要靠隊友替妳多跑一段。這幾年，是外婆替我跑完了那一段。現在，媽媽把棒子接回來了。",
    cover: "art/cg/T01_v1.webp", pos: "50% 50%", slides: ["art/cg/T01_v1.webp", "art/cg/T04_v1.webp", "art/cg/T07_v1.webp", "art/cg/TS00_v1.webp", "art/cg/TS03_v1.webp", "art/cg/TS06_v1.webp"] },
  { n: 4, file: "audio/full/fantasy.mp3", title: "Still on the Blocks", scene: "鏡子線：化妝台上的鏡子，和第一個月", dur: 179,
    line: "接力賽要有下一棒，棒子才交得出去。媽媽跑了好久好久，終於等到妳了。",
    cover: "art/cg/F01_v1.webp", pos: "50% 50%", slides: ["art/cg/F01_v1.webp", "art/cg/F07_v1.webp", "art/cg/F12_v1.webp", "art/cg/FS01_v1.webp", "art/cg/FS03_v1.webp", "art/cg/FS04_v1.webp"] }
];
