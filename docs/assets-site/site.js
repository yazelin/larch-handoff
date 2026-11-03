/* 共用：素材網址、遊玩按鈕、導覽列、進場動畫。
   圖片與音樂一律走 jsDelivr；site.json 的 assetBase 可以改，網址後面加 ?local 會改用 repo 裡的 ../assets/（本機驗收用）。 */
(function () {
  "use strict";
  var DEFAULT_BASE = "https://cdn.jsdelivr.net/gh/yazelin/larch-handoff@main/assets/";
  var me = document.currentScript && document.currentScript.src;
  var siteJson = new URL("../site.json", me || location.href).href;
  var local = /[?&]local\b/.test(location.search);
  var base = local ? new URL("../assets/", siteJson).href : DEFAULT_BASE;

  var S = window.SITE = { base: base, playUrl: "", ready: null };
  S.asset = function (p) { return S.base + p; };

  function apply(root) {
    (root || document).querySelectorAll("[data-a]").forEach(function (el) {
      var u = S.asset(el.getAttribute("data-a"));
      if (el.tagName === "A") el.href = u; else if (el.getAttribute("src") !== u) el.src = u;
    });
    (root || document).querySelectorAll("[data-bg]").forEach(function (el) {
      el.style.backgroundImage = "url(\"" + S.asset(el.getAttribute("data-bg")) + "\")";
    });
  }
  S.apply = apply;

  function playButtons() {
    document.querySelectorAll("[data-play]").forEach(function (a) {
      if (S.playUrl) {
        a.href = S.playUrl; a.removeAttribute("aria-disabled"); a.target = "_blank"; a.rel = "noopener";
        a.querySelector("span").textContent = "在 Larch 上遊玩";
      } else {
        a.removeAttribute("href"); a.setAttribute("aria-disabled", "true");
        a.querySelector("span").textContent = "即將上架";
      }
    });
  }

  S.ready = fetch(siteJson, { cache: "no-cache" }).then(function (r) { return r.json(); }).catch(function () { return {}; }).then(function (j) {
    S.playUrl = (j.playUrl || "").trim();
    if (!local && j.assetBase) {
      var b = new URL(j.assetBase, siteJson).href;
      if (b !== S.base) { S.base = b; apply(); }
    }
    playButtons();
    return S;
  });

  /* 主題：程徹版（預設）／林向晚版，記在 localStorage */
  function skin(name, animate) {
    var root = document.documentElement;
    if (animate) { root.classList.add("skinning"); clearTimeout(skin.t); skin.t = setTimeout(function () { root.classList.remove("skinning"); }, 700); }
    root.setAttribute("data-skin", name);
    try { localStorage.setItem("ho-skin", name); } catch (e) {}
    document.querySelectorAll("[data-skin-set]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-skin-set") === name)); });
  }
  S.skin = skin;

  /* 林向晚版的花瓣：一次放好，顯示與否交給 CSS */
  function petals() {
    if (document.querySelector(".petals")) return;
    var box = document.createElement("div"); box.className = "petals"; box.setAttribute("aria-hidden", "true");
    for (var i = 0; i < 11; i++) {
      var p = document.createElement("i"), r = Math.random;
      p.style.cssText = "--x:" + (r() * 100).toFixed(1) + "vw;--s:" + (9 + r() * 9).toFixed(1) + "px;--d:" + (14 + r() * 12).toFixed(1) + "s;--dl:" + (-r() * 26).toFixed(1) + "s;--dx:" + (r() * 30 - 10).toFixed(1) + "vw";
      box.appendChild(p);
    }
    document.body.appendChild(box);
  }

  function boot() {
    apply(); playButtons();
    var cur = document.documentElement.getAttribute("data-skin") === "lin" ? "lin" : "cheng";
    document.querySelectorAll("[data-skin-set]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-skin-set") === cur));
      b.addEventListener("click", function (e) { e.stopPropagation(); skin(b.getAttribute("data-skin-set"), true); });
    });
    var top = document.querySelector(".top");
    if (top && !top.hasAttribute("data-solid")) {
      var onScroll = function () { top.classList.toggle("solid", scrollY > 40); };
      addEventListener("scroll", onScroll, { passive: true }); onScroll();
    }
    var els = document.querySelectorAll(".rise");
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
      }, { rootMargin: "0px 0px -8% 0px" });
      els.forEach(function (el) { io.observe(el); });
    } else els.forEach(function (el) { el.classList.add("in"); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();

  /* 跨網域檔案的下載：<a download> 對 jsDelivr 無效，先抓成 blob 再存；失敗就開原檔 */
  S.download = function (url, name, btn) {
    if (btn) btn.disabled = true;
    return fetch(url).then(function (r) { if (!r.ok) throw 0; return r.blob(); }).then(function (b) {
      var a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = name;
      document.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 3000);
    }).catch(function () { window.open(url, "_blank"); }).then(function () { if (btn) btn.disabled = false; });
  };
})();
