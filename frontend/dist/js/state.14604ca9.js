"use strict";(self["webpackChunkkinderabholung"]=self["webpackChunkkinderabholung"]||[]).push([[522],{8384:function(e,t,s){s.r(t),s.d(t,{default:function(){return v}});var a=s(6768),i=s(5130),n=s(4232);const r={class:"message-create"},l={key:0,class:"status-online"},o={key:1,class:"status-offline"},c=["disabled"],d={key:2,class:"success"},h={key:3,class:"error"};function u(e,t,s,u,g,p){return(0,a.uX)(),(0,a.CE)("div",r,[t[5]||(t[5]=(0,a.Lk)("h2",{class:"message-title"},"Notfall - Hilfe anfordern",-1)),g.isRaspberryOnline?((0,a.uX)(),(0,a.CE)("p",l)):((0,a.uX)(),(0,a.CE)("p",o," ❌ System funktioniert aktuell nicht - AV kann nicht benachrichtigt werden!! ")),(0,a.Lk)("form",{onSubmit:t[2]||(t[2]=(0,i.D$)(((...e)=>p.createMessage&&p.createMessage(...e)),["prevent"]))},[t[3]||(t[3]=(0,a.Lk)("p",{class:"label"},"NOTFALL",-1)),(0,a.Lk)("div",null,[(0,a.bo)((0,a.Lk)("input",{type:"text",id:"content","onUpdate:modelValue":t[0]||(t[0]=e=>g.message.content=e),placeholder:"Wer wird benötigt?",onInput:t[1]||(t[1]=(...e)=>p.validateInput&&p.validateInput(...e)),required:""},null,544),[[i.Jo,g.message.content]])]),(0,a.Lk)("button",{type:"submit",disabled:!g.isValid||g.isSubmitting||!g.isRaspberryOnline}," Nachricht senden ",8,c)],32),g.successMessage?((0,a.uX)(),(0,a.CE)("div",d,t[4]||(t[4]=[(0,a.Lk)("p",null,"Nachricht erfolgreich gesendet!",-1)]))):(0,a.Q3)("",!0),g.errorMessage?((0,a.uX)(),(0,a.CE)("div",h,[(0,a.Lk)("p",null,(0,n.v_)(g.errorMessage),1)])):(0,a.Q3)("",!0)])}s(4114);var g={data(){return{message:{content:"",status:"sent"},successMessage:null,errorMessage:null,isValid:!1,isSubmitting:!1,isRaspberryOnline:!1}},methods:{async checkRaspberryStatus(){try{console.log("Prüfe Raspberry Pi Status...");const e=await fetch("http://192.168.104.45/api/live/",{method:"GET"});this.isRaspberryOnline=e.ok,console.log("Raspberry Online Status:",this.isRaspberryOnline)}catch(e){this.isRaspberryOnline=!1,console.log("Fehler beim Abrufen des Status:",e)}},validateInput(){const e=35,t=this.message.content.length<=e;t||(this.errorMessage=`Die Eingabe darf maximal ${e} Zeichen lang sein.`,this.isValid=!1,this.isValid=t)},async createMessage(){if(this.isValid&&!this.isSubmitting&&this.isRaspberryOnline){this.isSubmitting=!0;try{const e=await fetch("http://192.168.104.45/api/emergency/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(this.message)});if(!e.ok)throw new Error(`HTTP-Fehler! Status: ${e.status}`);this.successMessage="Nachricht erfolgreich gesendet!",this.errorMessage=null,setTimeout((()=>this.$router.push("/state")),1500),this.message.content="",this.message.status="sent",this.isValid=!1}catch(e){this.errorMessage=`Fehler beim Senden der Nachricht: ${e.message}`,this.successMessage=null}finally{this.isSubmitting=!1}}}},mounted(){this.checkRaspberryStatus()}},p=s(1241);const m=(0,p.A)(g,[["render",u],["__scopeId","data-v-6458b7ae"]]);var v=m},5869:function(e,t,s){s.r(t),s.d(t,{default:function(){return L}});var a=s(6768);const i={class:"messages-container"},n={key:0,class:"loading"},r={key:1};function l(e,t,s,l,o,c){const d=(0,a.g2)("MessageItem");return(0,a.uX)(),(0,a.CE)("div",i,[t[0]||(t[0]=(0,a.Lk)("h2",{class:"messages-title"},"Gesendete Nachrichten",-1)),o.loading?((0,a.uX)(),(0,a.CE)("div",n,"⏳ Lade Nachrichten...")):((0,a.uX)(),(0,a.CE)("div",r,[((0,a.uX)(!0),(0,a.CE)(a.FK,null,(0,a.pI)(o.messages,(e=>((0,a.uX)(),(0,a.Wv)(d,{key:e.id,text:e.content,date:e.created_at,state:e.status},null,8,["text","date","state"])))),128))]))])}var o=s(4232);const c={class:"message-item"},d={class:"message-text"},h={class:"message-meta"},u={class:"message-date"},g={class:"message-state"},p={key:0,class:"tooltip"};function m(e,t,s,i,n,r){return(0,a.uX)(),(0,a.CE)("div",c,[(0,a.Lk)("div",d,[t[1]||(t[1]=(0,a.eW)(" Die Eltern von ")),(0,a.Lk)("strong",null,(0,o.v_)(s.text),1),t[2]||(t[2]=(0,a.eW)(" bitte zum Check-in kommen "))]),(0,a.Lk)("div",h,[(0,a.Lk)("span",u,(0,o.v_)(r.formattedDate),1),(0,a.Lk)("div",g,[(0,a.Lk)("span",{class:(0,o.C4)(r.statusClass)},(0,o.v_)(r.translatedState),3),(0,a.Lk)("span",{class:"info-icon",onClick:t[0]||(t[0]=(...e)=>r.toggleTooltip&&r.toggleTooltip(...e))},"❓"),n.showTooltip?((0,a.uX)(),(0,a.CE)("div",p,(0,o.v_)(r.statusExplanation),1)):(0,a.Q3)("",!0)])])])}var v={name:"MessageItem",props:{text:String,date:String,state:String},data(){return{showTooltip:!1}},computed:{formattedDate(){return new Date(this.date).toLocaleString()},translatedState(){const e={received:"Wartet auf Freigabe",approved:"Wird angezeigt",rejected:"Wurde abgelehnt",sent:"An AV Gesendet",displayed:"Wurde angezeigt"};return e[this.state]||this.state},statusExplanation(){const e={received:"Das AV-Team hat deine Nachricht erhalten. Es entscheidet jetzt wann und ob es deine Nachricht auf der LED-Wall anzeigt. Du wirst hier informiert, sobald es eine Entscheidung trifft",approved:"Das AV-Team zeigt deine Nachricht gerade auf der LED-Wall an.",rejected:"Das AV-Team hat entschieden deine Nachricht nicht auf der LED-Wall anzuzeigen.",sent:"Deine Nachricht wird gerade an das AV-Team gesendet, ist aber noch nicht dort angekommen.",displayed:"Deine Nachricht ist jetzt nicht mehr auf der LED-Wall zu sehen. Sie wurde aber angezeigt."};return e[this.state]||""}},methods:{toggleTooltip(){this.showTooltip=!this.showTooltip},statusClass(){return{"status-pending":"received"===this.state,"status-success":"approved"===this.state,"status-error":"rejected"===this.state,"status-sent":"sent"===this.state,"status-displayed":"displayed"===this.state}}}},b=s(1241);const f=(0,b.A)(v,[["render",m],["__scopeId","data-v-386e3252"]]);var k=f,y={components:{MessageItem:k},data(){return{messages:[],loading:!0,intervalId:null}},async created(){await this.getMessages(),this.startPolling()},beforeUnmount(){this.stopPolling()},methods:{async getMessages(){try{let e=await fetch("http://192.168.104.45/api/messages/",{method:"GET"});if(!e.ok)throw new Error(`HTTP-Fehler! Status: ${e.status}`);this.messages=await e.json(),this.loading=!1}catch(e){console.error("Fehler beim Abrufen der Nachrichten:",e),this.loading=!1}},startPolling(){this.intervalId=setInterval(this.getMessages,4e3)},stopPolling(){this.intervalId&&clearInterval(this.intervalId)}}};const E=(0,b.A)(y,[["render",l],["__scopeId","data-v-4e32ca43"]]);var L=E}}]);
//# sourceMappingURL=state.14604ca9.js.map