(function(){"use strict";var e={5814:function(e,t,n){var r=n(5130),s=n(6768);function i(e,t,n,r,i,a){const o=(0,s.g2)("Header"),u=(0,s.g2)("router-link"),c=(0,s.g2)("router-view");return(0,s.uX)(),(0,s.CE)(s.FK,null,[(0,s.bF)(o),(0,s.Lk)("nav",null,[(0,s.bF)(u,{to:"/"},{default:(0,s.k6)((()=>t[0]||(t[0]=[(0,s.eW)("Nachricht senden")]))),_:1}),t[2]||(t[2]=(0,s.eW)(" | ")),(0,s.bF)(u,{to:"/state"},{default:(0,s.k6)((()=>t[1]||(t[1]=[(0,s.eW)("Status")]))),_:1})]),(0,s.bF)(c)],64)}var a=n.p+"img/icf-kids-logo_v2_black.d0f200d8.png";function o(e,t,n,r,i,o){return(0,s.uX)(),(0,s.CE)("header",null,t[0]||(t[0]=[(0,s.Lk)("img",{alt:"icf",src:a,class:"logo"},null,-1)]))}var u={name:"Header"},c=n(1241);const l=(0,c.A)(u,[["render",o],["__scopeId","data-v-4bf9d33e"]]);var d=l,f={components:{Header:d}};const h=(0,c.A)(f,[["render",i]]);var p=h,g=n(1387),m=n(4232);const b={class:"message-create"},v={key:0,class:"status-online"},y={key:1,class:"status-offline"},k=["disabled"],S={key:2,class:"success"},E={key:3,class:"error"};function O(e,t,n,i,a,o){return(0,s.uX)(),(0,s.CE)("div",b,[t[6]||(t[6]=(0,s.Lk)("h2",{class:"message-title"},"Nachricht an AV senden",-1)),a.isRaspberryOnline?((0,s.uX)(),(0,s.CE)("p",v)):((0,s.uX)(),(0,s.CE)("p",y," ❌ System funktioniert aktuell nicht - AV kann nicht benachrichtigt werden!! ")),(0,s.Lk)("form",{onSubmit:t[2]||(t[2]=(0,r.D$)(((...e)=>o.createMessage&&o.createMessage(...e)),["prevent"]))},[t[3]||(t[3]=(0,s.Lk)("p",{class:"label"},"Die Eltern von",-1)),(0,s.Lk)("div",null,[(0,s.bo)((0,s.Lk)("input",{type:"text",id:"content","onUpdate:modelValue":t[0]||(t[0]=e=>a.message.content=e),placeholder:"Vorname N.",onInput:t[1]||(t[1]=(...e)=>o.validateInput&&o.validateInput(...e)),required:""},null,544),[[r.Jo,a.message.content]])]),t[4]||(t[4]=(0,s.Lk)("p",{class:"label2"},"bitte zum Check-in kommen",-1)),(0,s.Lk)("button",{type:"submit",disabled:!a.isValid||a.isSubmitting||!a.isRaspberryOnline}," Nachricht senden ",8,k)],32),a.successMessage?((0,s.uX)(),(0,s.CE)("div",S,t[5]||(t[5]=[(0,s.Lk)("p",null,"Nachricht erfolgreich gesendet!",-1)]))):(0,s.Q3)("",!0),a.errorMessage?((0,s.uX)(),(0,s.CE)("div",E,[(0,s.Lk)("p",null,(0,m.v_)(a.errorMessage),1)])):(0,s.Q3)("",!0)])}n(4114);var C={data(){return{message:{content:"",status:"sent"},successMessage:null,errorMessage:null,isValid:!1,isSubmitting:!1,isRaspberryOnline:!1}},methods:{async checkRaspberryStatus(){try{console.log("Prüfe Raspberry Pi Status...");const e=await fetch("http://192.168.104.45/api/live/",{method:"GET"});this.isRaspberryOnline=e.ok,console.log("Raspberry Online Status:",this.isRaspberryOnline)}catch(e){this.isRaspberryOnline=!1,console.log("Fehler beim Abrufen des Status:",e)}},validateInput(){const e=25,t=/^[A-Za-zÄÖÜäöüß]+\s[A-Za-z]\.$/,n=t.test(this.message.content),r=this.message.content.length<=e;r?(this.errorMessage=n?null:"Bitte das Format 'Vorname N.' verwenden. Datenschutz!!!",this.isValid=n&&r):(this.errorMessage=`Die Eingabe darf maximal ${e} Zeichen lang sein.`,this.isValid=!1)},async createMessage(){if(this.isValid&&!this.isSubmitting&&this.isRaspberryOnline){this.isSubmitting=!0;try{const e=await fetch("http://192.168.104.45/api/messages/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(this.message)});if(!e.ok)throw new Error(`HTTP-Fehler! Status: ${e.status}`);this.successMessage="Nachricht erfolgreich gesendet!",this.errorMessage=null,setTimeout((()=>this.$router.push("/state")),1500),this.message.content="",this.message.status="sent",this.isValid=!1}catch(e){this.errorMessage=`Fehler beim Senden der Nachricht: ${e.message}`,this.successMessage=null}finally{this.isSubmitting=!1}}}},mounted(){this.checkRaspberryStatus()}};const w=(0,c.A)(C,[["render",O],["__scopeId","data-v-3c80350d"]]);var A=w;const L=[{path:"/",name:"home",component:A},{path:"/state",name:"state",component:()=>n.e(522).then(n.bind(n,5869))}],N=(0,g.aE)({history:(0,g.LA)("/"),routes:L});var M=N;(0,r.Ef)(p).use(M).mount("#app")}},t={};function n(r){var s=t[r];if(void 0!==s)return s.exports;var i=t[r]={exports:{}};return e[r].call(i.exports,i,i.exports,n),i.exports}n.m=e,function(){var e=[];n.O=function(t,r,s,i){if(!r){var a=1/0;for(l=0;l<e.length;l++){r=e[l][0],s=e[l][1],i=e[l][2];for(var o=!0,u=0;u<r.length;u++)(!1&i||a>=i)&&Object.keys(n.O).every((function(e){return n.O[e](r[u])}))?r.splice(u--,1):(o=!1,i<a&&(a=i));if(o){e.splice(l--,1);var c=s();void 0!==c&&(t=c)}}return t}i=i||0;for(var l=e.length;l>0&&e[l-1][2]>i;l--)e[l]=e[l-1];e[l]=[r,s,i]}}(),function(){n.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(t,{a:t}),t}}(),function(){n.d=function(e,t){for(var r in t)n.o(t,r)&&!n.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})}}(),function(){n.f={},n.e=function(e){return Promise.all(Object.keys(n.f).reduce((function(t,r){return n.f[r](e,t),t}),[]))}}(),function(){n.u=function(e){return"js/state.a5fbad32.js"}}(),function(){n.miniCssF=function(e){return"css/state.c756d4fa.css"}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={},t="kinderabholung:";n.l=function(r,s,i,a){if(e[r])e[r].push(s);else{var o,u;if(void 0!==i)for(var c=document.getElementsByTagName("script"),l=0;l<c.length;l++){var d=c[l];if(d.getAttribute("src")==r||d.getAttribute("data-webpack")==t+i){o=d;break}}o||(u=!0,o=document.createElement("script"),o.charset="utf-8",o.timeout=120,n.nc&&o.setAttribute("nonce",n.nc),o.setAttribute("data-webpack",t+i),o.src=r),e[r]=[s];var f=function(t,n){o.onerror=o.onload=null,clearTimeout(h);var s=e[r];if(delete e[r],o.parentNode&&o.parentNode.removeChild(o),s&&s.forEach((function(e){return e(n)})),t)return t(n)},h=setTimeout(f.bind(null,void 0,{type:"timeout",target:o}),12e4);o.onerror=f.bind(null,o.onerror),o.onload=f.bind(null,o.onload),u&&document.head.appendChild(o)}}}(),function(){n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){n.p="/"}(),function(){if("undefined"!==typeof document){var e=function(e,t,r,s,i){var a=document.createElement("link");a.rel="stylesheet",a.type="text/css",n.nc&&(a.nonce=n.nc);var o=function(n){if(a.onerror=a.onload=null,"load"===n.type)s();else{var r=n&&n.type,o=n&&n.target&&n.target.href||t,u=new Error("Loading CSS chunk "+e+" failed.\n("+r+": "+o+")");u.name="ChunkLoadError",u.code="CSS_CHUNK_LOAD_FAILED",u.type=r,u.request=o,a.parentNode&&a.parentNode.removeChild(a),i(u)}};return a.onerror=a.onload=o,a.href=t,r?r.parentNode.insertBefore(a,r.nextSibling):document.head.appendChild(a),a},t=function(e,t){for(var n=document.getElementsByTagName("link"),r=0;r<n.length;r++){var s=n[r],i=s.getAttribute("data-href")||s.getAttribute("href");if("stylesheet"===s.rel&&(i===e||i===t))return s}var a=document.getElementsByTagName("style");for(r=0;r<a.length;r++){s=a[r],i=s.getAttribute("data-href");if(i===e||i===t)return s}},r=function(r){return new Promise((function(s,i){var a=n.miniCssF(r),o=n.p+a;if(t(a,o))return s();e(r,o,null,s,i)}))},s={524:0};n.f.miniCss=function(e,t){var n={522:1};s[e]?t.push(s[e]):0!==s[e]&&n[e]&&t.push(s[e]=r(e).then((function(){s[e]=0}),(function(t){throw delete s[e],t})))}}}(),function(){var e={524:0};n.f.j=function(t,r){var s=n.o(e,t)?e[t]:void 0;if(0!==s)if(s)r.push(s[2]);else{var i=new Promise((function(n,r){s=e[t]=[n,r]}));r.push(s[2]=i);var a=n.p+n.u(t),o=new Error,u=function(r){if(n.o(e,t)&&(s=e[t],0!==s&&(e[t]=void 0),s)){var i=r&&("load"===r.type?"missing":r.type),a=r&&r.target&&r.target.src;o.message="Loading chunk "+t+" failed.\n("+i+": "+a+")",o.name="ChunkLoadError",o.type=i,o.request=a,s[1](o)}};n.l(a,u,"chunk-"+t,t)}},n.O.j=function(t){return 0===e[t]};var t=function(t,r){var s,i,a=r[0],o=r[1],u=r[2],c=0;if(a.some((function(t){return 0!==e[t]}))){for(s in o)n.o(o,s)&&(n.m[s]=o[s]);if(u)var l=u(n)}for(t&&t(r);c<a.length;c++)i=a[c],n.o(e,i)&&e[i]&&e[i][0](),e[i]=0;return n.O(l)},r=self["webpackChunkkinderabholung"]=self["webpackChunkkinderabholung"]||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))}();var r=n.O(void 0,[504],(function(){return n(5814)}));r=n.O(r)})();
//# sourceMappingURL=app.ec61206b.js.map