// Fanplayr Platform Loader v1.273
!function(a,b){function c(){try{a.console.log.apply(a.console,arguments)}catch(a){}}function d(){var a=m._i&&m._i.length&&m._i[0],b=a&&(a.accountKey||a.ak);return b||(b=m.adaptor&&m.adaptor.config&&m.adaptor.config.accountKey),b||(b=m.zanox&&m.zanox.config&&m.zanox.config.accountKey),!b&&m.custom&&(b=m.custom.accountKey),b||null}function e(){var a=m.adaptor&&m.adaptor.config||{};return m.allowInFrame||a.allowInFrame}function f(a){var c=b.createElement("script");if(c.async=!0,c.src=a,c.src){var d=b.getElementsByTagName("script")[0];d.parentNode.insertBefore(c,d)}}function g(){if(k[p])return!0;for(var b=a.location.hostname,c=0,d=l.length;c<d;c++)if(-1!==b.indexOf(l[c]))return!0}function h(){return/(GoogleBot|Catchpoint|KTXN|KHTE|GomezAgent|Evidon|Baiduspider|YandexBot|YandexMobileBot)/i.test(a.navigator&&a.navigator.userAgent)}var i={platform:"1.107.0","services/offers":"1.18.0","services/offers-legacy":"1.8.5","services/intent":"1.4.5","services/widget":"1.17.0","services/runtime":"1.132.0","services/debug":"1.5.0"},j={f72a2b03f99f4a86a9b9804585383771:1},k={"2926e141811521da8a53d0f7cc2cba65":1,dafa184bfe313e08b63f8ae6f9110479:1,"59594f7fc30901a2e235afb8a9b91277":1,e03b4aac8d78a14a32fbd62330c9b98d:1,"9fd0910edec0a9a6d10123c37ddea857":1,b67c42d72f581d5d24103746aa98902c:1,"4cbbcf8dfb09c2398a9af6eb5825a5b3":1,"490ffda63e1b37c31f335ff5361151db":1},l=["dekbed-discounter.nl","efarma.com","efarma.it"],m=a.fanplayr=a.fanplayr||{},n=m.loader=m.loader||{},o=n.params={},p=d(),q="_loadState";if(a.top!==a&&!e())return void c("Fanplayr prevent in frame: "+(a.frameElement&&a.frameElement.src));if(!(m[q]||g()||h())){if(m[q]=1,p&&j[p])return void f("//d1q7pknmpq2wkm.cloudfront.net/js/my.fanplayr.com/fp_smart.embed.js");for(var r=/(?:d38nbbai6u794i|fanplayr|fpc).*?loader\.js(.*)/i,s=b.getElementsByTagName("script"),t=0;t<s.length;t++){var u=s[t].src;if(r.test(u)){u.replace(/([^?&=]+)=([^?&=]+)/g,function(a,b,c){o[b]=decodeURIComponent(c),/^cdn|debug|adaptor|cache$/.test(b)&&(n[b]=o[b])});break}}var v=".min.js";!1===n.min&&(v=".js"),void 0===n.cache||n.cache||(v+="?_="+ +new Date),n.uri=function(a){var b=n.cdn=n.cdn||o.cdn||"//cdn.fanplayr.com/client/production",c=i[a],d=a.split("/").pop()+v;return/\.js$/.test(a)?b+"/"+a:n.debug?b+"/"+a+"/"+d:c?b+"/"+a+"/releases/"+c+"/"+d:void 0},n.base=function(a){var b=n.uri(a).split("/");return b.pop(),b.join("/")},f(n.uri("platform"))}}(window,document);
//# sourceMappingURL=loader.js.map