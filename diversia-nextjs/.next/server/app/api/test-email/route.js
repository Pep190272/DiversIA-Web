(()=>{var a={};a.id=573,a.ids=[573],a.modules={261:a=>{"use strict";a.exports=require("next/dist/shared/lib/router/utils/app-paths")},3295:a=>{"use strict";a.exports=require("next/dist/server/app-render/after-task-async-storage.external.js")},10846:a=>{"use strict";a.exports=require("next/dist/compiled/next-server/app-page.runtime.prod.js")},12412:a=>{"use strict";a.exports=require("assert")},14985:a=>{"use strict";a.exports=require("dns")},19121:a=>{"use strict";a.exports=require("next/dist/server/app-render/action-async-storage.external.js")},21820:a=>{"use strict";a.exports=require("os")},24429:()=>{},27910:a=>{"use strict";a.exports=require("stream")},28354:a=>{"use strict";a.exports=require("util")},28635:()=>{},29021:a=>{"use strict";a.exports=require("fs")},29294:a=>{"use strict";a.exports=require("next/dist/server/app-render/work-async-storage.external.js")},33873:a=>{"use strict";a.exports=require("path")},34631:a=>{"use strict";a.exports=require("tls")},44870:a=>{"use strict";a.exports=require("next/dist/compiled/next-server/app-route.runtime.prod.js")},55511:a=>{"use strict";a.exports=require("crypto")},55591:a=>{"use strict";a.exports=require("https")},60016:(a,b,c)=>{"use strict";c.d(b,{g:()=>h});var d=c(72275),e=c(26739),f=c.n(e);class g{constructor(){this.transporter=null,this.useGmail=!1,this.useSendGrid=!1,this.initializeServices()}initializeServices(){let a=process.env.GMAIL_USER,b=process.env.GMAIL_APP_PASSWORD||process.env.GMAIL_PASSWORD;a&&b&&(this.setupGmail(a,b),this.useGmail=!0,console.log("✅ Gmail configurado como servicio de email"));let c=process.env.SENDGRID_API_KEY;c&&(f().setApiKey(c),this.useSendGrid=!0,console.log("✅ SendGrid configurado como backup")),this.useGmail||this.useSendGrid||console.warn("⚠️ No se encontraron credenciales de email configuradas")}setupGmail(a,b){this.transporter=d.createTransport({service:"gmail",auth:{user:a,pass:b}})}async sendEmail(a){try{if(this.useGmail&&this.transporter)return await this.sendWithGmail(a);if(this.useSendGrid)return await this.sendWithSendGrid(a);return console.error("❌ No hay servicios de email configurados"),!1}catch(a){return console.error("❌ Error enviando email:",a),!1}}async sendWithGmail(a){try{if(!this.transporter)return!1;let b={from:process.env.GMAIL_USER,to:a.to,subject:a.subject,text:a.text,html:a.html},c=await this.transporter.sendMail(b);return console.log("✅ Email enviado con Gmail:",c.messageId),!0}catch(b){if(console.error("❌ Error con Gmail:",b),this.useSendGrid)return console.log("\uD83D\uDD04 Intentando con SendGrid como backup..."),await this.sendWithSendGrid(a);return!1}}async sendWithSendGrid(a){try{let b={to:a.to,from:"noreply@diversia.com",subject:a.subject,content:[{type:"text/plain",value:a.text||""},{type:"text/html",value:a.html||""}]};return await f().send(b),console.log("✅ Email enviado con SendGrid"),!0}catch(a){return console.error("❌ Error con SendGrid:",a),!1}}async sendWelcomeEmail(a){let b=this.generateWelcomeEmail(a),c=this.generateWelcomeEmailText(a);return await this.sendEmail({to:a.email,subject:"\uD83C\uDF89 \xa1Bienvenido/a a DiversIA! Tu perfil ha sido creado",html:b,text:c})}async sendNotificationEmail(a){let b=process.env.DIVERSIA_EMAIL||"diversiaeternals@gmail.com",c=this.generateNotificationEmail(a),d=this.generateNotificationEmailText(a);return await this.sendEmail({to:b,subject:`🔔 Nuevo registro en DiversIA - ${a.nombre}`,html:c,text:d})}generateWelcomeEmail(a){return`
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .highlight { background: #f8f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin: 20px 0; }
            .button { background: #667eea; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
            .footer { text-align: center; color: #666; font-size: 14px; margin-top: 30px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 \xa1Bienvenido/a a DiversIA!</h1>
                <p>Tu perfil ha sido creado exitosamente</p>
            </div>
            <div class="content">
                <h2>Hola ${a.nombre},</h2>
                <p>\xa1Qu\xe9 emocionante tenerte en nuestra comunidad! Tu registro en DiversIA ha sido completado con \xe9xito.</p>
                
                <div class="highlight">
                    <h3>🧠 \xbfQu\xe9 pasa ahora?</h3>
                    <ul>
                        <li>Estamos revisando tu perfil para crear las mejores oportunidades</li>
                        <li>Nuestro equipo identificar\xe1 empresas que valoren tu talento \xfanico</li>
                        <li>Te contactaremos con oportunidades laborales que realmente encajen contigo</li>
                        ${a.tipo_neurodivergencia?`<li>Tu perfil especializado en <strong>${a.tipo_neurodivergencia}</strong> nos ayudar\xe1 a encontrar el match perfecto</li>`:""}
                    </ul>
                </div>

                <h3>💼 Tu Proceso de Empleabilidad</h3>
                <p>En DiversIA entendemos que tu neurodivergencia es una fortaleza, no una limitaci\xf3n. Trabajamos con empresas que:</p>
                <ul>
                    <li>✅ Valoran la diversidad de pensamiento</li>
                    <li>✅ Ofrecen adaptaciones del entorno laboral</li>
                    <li>✅ Buscan activamente talento neurodivergente</li>
                    <li>✅ Entienden el potencial \xfanico que aportas</li>
                </ul>

                <p>Mientras tanto, mantente atento/a a tu correo. Te contactaremos pronto con oportunidades emocionantes.</p>

                <a href="mailto:contacto@diversia.com" class="button">Cont\xe1ctanos si tienes preguntas</a>

                <p><strong>\xa1Gracias por confiar en DiversIA para tu futuro laboral!</strong></p>
            </div>
            <div class="footer">
                <p>DiversIA - Conectando talento neurodivergente con oportunidades excepcionales</p>
                <p>Si no solicitaste este registro, puedes ignorar este email.</p>
            </div>
        </div>
    </body>
    </html>
    `}generateWelcomeEmailText(a){return`
\xa1Bienvenido/a a DiversIA, ${a.nombre}!

Tu perfil ha sido creado exitosamente en nuestra plataforma.

\xbfQu\xe9 pasa ahora?
- Estamos revisando tu perfil para crear las mejores oportunidades
- Nuestro equipo identificar\xe1 empresas que valoren tu talento \xfanico
- Te contactaremos con oportunidades laborales que realmente encajen contigo
${a.tipo_neurodivergencia?`- Tu perfil especializado en ${a.tipo_neurodivergencia} nos ayudar\xe1 a encontrar el match perfecto`:""}

En DiversIA entendemos que tu neurodivergencia es una fortaleza, no una limitaci\xf3n.

Trabajamos con empresas que:
✅ Valoran la diversidad de pensamiento
✅ Ofrecen adaptaciones del entorno laboral  
✅ Buscan activamente talento neurodivergente
✅ Entienden el potencial \xfanico que aportas

Mantente atento/a a tu correo. Te contactaremos pronto con oportunidades emocionantes.

Si tienes preguntas, responde a este email o escr\xedbenos a contacto@diversia.com

\xa1Gracias por confiar en DiversIA para tu futuro laboral!

DiversIA - Conectando talento neurodivergente con oportunidades excepcionales
    `}generateNotificationEmail(a){return`
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
            .content { background: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .data-section { background: #f8fafc; padding: 15px; border-radius: 6px; margin: 15px 0; }
            .urgent { background: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin: 15px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔔 Nuevo Registro en DiversIA</h1>
                <p>Se ha registrado un nuevo usuario en la plataforma</p>
            </div>
            <div class="content">
                <div class="urgent">
                    <h3>⚡ Acci\xf3n Requerida</h3>
                    <p>Un nuevo usuario se ha registrado y est\xe1 esperando seguimiento del equipo de DiversIA.</p>
                </div>

                <div class="data-section">
                    <h3>📋 Informaci\xf3n del Usuario</h3>
                    <p><strong>Nombre:</strong> ${a.nombre}</p>
                    <p><strong>Email:</strong> ${a.email}</p>
                    ${a.telefono?`<p><strong>Tel\xe9fono:</strong> ${a.telefono}</p>`:""}
                    ${a.ciudad?`<p><strong>Ciudad:</strong> ${a.ciudad}</p>`:""}
                    ${a.tipo_neurodivergencia?`<p><strong>Tipo de Neurodivergencia:</strong> ${a.tipo_neurodivergencia}</p>`:""}
                    <p><strong>Fecha de Registro:</strong> ${a.fecha_registro}</p>
                </div>

                <div class="data-section">
                    <h3>📝 Pr\xf3ximos Pasos</h3>
                    <ul>
                        <li>Revisar el perfil completo en el panel administrativo</li>
                        <li>Validar la informaci\xf3n proporcionada</li>
                        <li>Comenzar el proceso de matching con empresas</li>
                        <li>Contactar al usuario para seguimiento personalizado</li>
                    </ul>
                </div>

                <p><strong>Accede al panel administrativo para ver todos los detalles del perfil.</strong></p>
            </div>
        </div>
    </body>
    </html>
    `}generateNotificationEmailText(a){return`
🔔 NUEVO REGISTRO EN DIVERSIA

Se ha registrado un nuevo usuario en la plataforma:

📋 INFORMACI\xd3N DEL USUARIO:
- Nombre: ${a.nombre}
- Email: ${a.email}
${a.telefono?`- Tel\xe9fono: ${a.telefono}`:""}
${a.ciudad?`- Ciudad: ${a.ciudad}`:""}
${a.tipo_neurodivergencia?`- Tipo de Neurodivergencia: ${a.tipo_neurodivergencia}`:""}
- Fecha de Registro: ${a.fecha_registro}

📝 PR\xd3XIMOS PASOS:
- Revisar el perfil completo en el panel administrativo
- Validar la informaci\xf3n proporcionada  
- Comenzar el proceso de matching con empresas
- Contactar al usuario para seguimiento personalizado

Accede al panel administrativo para ver todos los detalles del perfil.
    `}async testConfiguration(){let a=process.env.GMAIL_USER||"test@diversia.com";return{gmail:!!this.useGmail&&await this.sendEmail({to:a,subject:"Test de configuraci\xf3n Gmail - DiversIA",text:"Este es un email de prueba para verificar la configuraci\xf3n de Gmail.",html:"<p>Este es un email de prueba para verificar la configuraci\xf3n de Gmail.</p>"}),sendgrid:!!this.useSendGrid&&await this.sendEmail({to:a,subject:"Test de configuraci\xf3n SendGrid - DiversIA",text:"Este es un email de prueba para verificar la configuraci\xf3n de SendGrid.",html:"<p>Este es un email de prueba para verificar la configuraci\xf3n de SendGrid.</p>"})}}}let h=new g},63033:a=>{"use strict";a.exports=require("next/dist/server/app-render/work-unit-async-storage.external.js")},64749:()=>{},67601:(a,b,c)=>{"use strict";c.r(b),c.d(b,{handler:()=>C,patchFetch:()=>B,routeModule:()=>x,serverHooks:()=>A,workAsyncStorage:()=>y,workUnitAsyncStorage:()=>z});var d={};c.r(d),c.d(d,{POST:()=>w});var e=c(44112),f=c(73125),g=c(53588),h=c(79510),i=c(11932),j=c(261),k=c(11290),l=c(42600),m=c(49704),n=c(57451),o=c(67845),p=c(74951),q=c(95017),r=c(47102),s=c(86439),t=c(8916),u=c(79113),v=c(60016);async function w(a){try{let{type:b="test"}=await a.json();if("configuration"===b){let a=await v.g.testConfiguration();return u.NextResponse.json({success:!0,results:a,message:"Test de configuraci\xf3n completado"})}if("welcome"===b){let a=await v.g.sendWelcomeEmail({nombre:"Usuario Test",email:process.env.GMAIL_USER||"test@diversia.com",tipo_neurodivergencia:"TDAH"});return u.NextResponse.json({success:a,message:a?"Email de bienvenida enviado":"Error enviando email de bienvenida"})}if("notification"===b){let a=await v.g.sendNotificationEmail({nombre:"Usuario Test",email:"test@diversia.com",telefono:"+34 600 000 000",ciudad:"Madrid",tipo_neurodivergencia:"TDAH",fecha_registro:new Date().toLocaleString("es-ES")});return u.NextResponse.json({success:a,message:a?"Email de notificaci\xf3n enviado":"Error enviando email de notificaci\xf3n"})}return u.NextResponse.json({success:!1,error:"Tipo de test no v\xe1lido. Usa: configuration, welcome, o notification"},{status:400})}catch(a){return console.error("Error en test de email:",a),u.NextResponse.json({success:!1,error:"Error ejecutando test de email"},{status:500})}}let x=new e.AppRouteRouteModule({definition:{kind:f.RouteKind.APP_ROUTE,page:"/api/test-email/route",pathname:"/api/test-email",filename:"route",bundlePath:"app/api/test-email/route"},distDir:".next",relativeProjectDir:"",resolvedPagePath:"/home/runner/workspace/diversia-nextjs/src/app/api/test-email/route.ts",nextConfigOutput:"",userland:d}),{workAsyncStorage:y,workUnitAsyncStorage:z,serverHooks:A}=x;function B(){return(0,g.patchFetch)({workAsyncStorage:y,workUnitAsyncStorage:z})}async function C(a,b,c){var d;let e="/api/test-email/route";"/index"===e&&(e="/");let g=await x.prepare(a,b,{srcPage:e,multiZoneDraftMode:!1});if(!g)return b.statusCode=400,b.end("Bad Request"),null==c.waitUntil||c.waitUntil.call(c,Promise.resolve()),null;let{buildId:u,params:v,nextConfig:w,isDraftMode:y,prerenderManifest:z,routerServerContext:A,isOnDemandRevalidate:B,revalidateOnlyGenerated:C,resolvedPathname:D}=g,E=(0,j.normalizeAppPath)(e),F=!!(z.dynamicRoutes[E]||z.routes[D]);if(F&&!y){let a=!!z.routes[D],b=z.dynamicRoutes[E];if(b&&!1===b.fallback&&!a)throw new s.NoFallbackError}let G=null;!F||x.isDev||y||(G="/index"===(G=D)?"/":G);let H=!0===x.isDev||!F,I=F&&!H,J=a.method||"GET",K=(0,i.getTracer)(),L=K.getActiveScopeSpan(),M={params:v,prerenderManifest:z,renderOpts:{experimental:{cacheComponents:!!w.experimental.cacheComponents,authInterrupts:!!w.experimental.authInterrupts},supportsDynamicResponse:H,incrementalCache:(0,h.getRequestMeta)(a,"incrementalCache"),cacheLifeProfiles:null==(d=w.experimental)?void 0:d.cacheLife,isRevalidate:I,waitUntil:c.waitUntil,onClose:a=>{b.on("close",a)},onAfterTaskError:void 0,onInstrumentationRequestError:(b,c,d)=>x.onRequestError(a,b,d,A)},sharedContext:{buildId:u}},N=new k.NodeNextRequest(a),O=new k.NodeNextResponse(b),P=l.NextRequestAdapter.fromNodeNextRequest(N,(0,l.signalFromNodeResponse)(b));try{let d=async c=>x.handle(P,M).finally(()=>{if(!c)return;c.setAttributes({"http.status_code":b.statusCode,"next.rsc":!1});let d=K.getRootSpanAttributes();if(!d)return;if(d.get("next.span_type")!==m.BaseServerSpan.handleRequest)return void console.warn(`Unexpected root span type '${d.get("next.span_type")}'. Please report this Next.js issue https://github.com/vercel/next.js`);let e=d.get("next.route");if(e){let a=`${J} ${e}`;c.setAttributes({"next.route":e,"http.route":e,"next.span_name":a}),c.updateName(a)}else c.updateName(`${J} ${a.url}`)}),g=async g=>{var i,j;let k=async({previousCacheEntry:f})=>{try{if(!(0,h.getRequestMeta)(a,"minimalMode")&&B&&C&&!f)return b.statusCode=404,b.setHeader("x-nextjs-cache","REVALIDATED"),b.end("This page could not be found"),null;let e=await d(g);a.fetchMetrics=M.renderOpts.fetchMetrics;let i=M.renderOpts.pendingWaitUntil;i&&c.waitUntil&&(c.waitUntil(i),i=void 0);let j=M.renderOpts.collectedTags;if(!F)return await (0,o.I)(N,O,e,M.renderOpts.pendingWaitUntil),null;{let a=await e.blob(),b=(0,p.toNodeOutgoingHttpHeaders)(e.headers);j&&(b[r.NEXT_CACHE_TAGS_HEADER]=j),!b["content-type"]&&a.type&&(b["content-type"]=a.type);let c=void 0!==M.renderOpts.collectedRevalidate&&!(M.renderOpts.collectedRevalidate>=r.INFINITE_CACHE)&&M.renderOpts.collectedRevalidate,d=void 0===M.renderOpts.collectedExpire||M.renderOpts.collectedExpire>=r.INFINITE_CACHE?void 0:M.renderOpts.collectedExpire;return{value:{kind:t.CachedRouteKind.APP_ROUTE,status:e.status,body:Buffer.from(await a.arrayBuffer()),headers:b},cacheControl:{revalidate:c,expire:d}}}}catch(b){throw(null==f?void 0:f.isStale)&&await x.onRequestError(a,b,{routerKind:"App Router",routePath:e,routeType:"route",revalidateReason:(0,n.c)({isRevalidate:I,isOnDemandRevalidate:B})},A),b}},l=await x.handleResponse({req:a,nextConfig:w,cacheKey:G,routeKind:f.RouteKind.APP_ROUTE,isFallback:!1,prerenderManifest:z,isRoutePPREnabled:!1,isOnDemandRevalidate:B,revalidateOnlyGenerated:C,responseGenerator:k,waitUntil:c.waitUntil});if(!F)return null;if((null==l||null==(i=l.value)?void 0:i.kind)!==t.CachedRouteKind.APP_ROUTE)throw Object.defineProperty(Error(`Invariant: app-route received invalid cache entry ${null==l||null==(j=l.value)?void 0:j.kind}`),"__NEXT_ERROR_CODE",{value:"E701",enumerable:!1,configurable:!0});(0,h.getRequestMeta)(a,"minimalMode")||b.setHeader("x-nextjs-cache",B?"REVALIDATED":l.isMiss?"MISS":l.isStale?"STALE":"HIT"),y&&b.setHeader("Cache-Control","private, no-cache, no-store, max-age=0, must-revalidate");let m=(0,p.fromNodeOutgoingHttpHeaders)(l.value.headers);return(0,h.getRequestMeta)(a,"minimalMode")&&F||m.delete(r.NEXT_CACHE_TAGS_HEADER),!l.cacheControl||b.getHeader("Cache-Control")||m.get("Cache-Control")||m.set("Cache-Control",(0,q.getCacheControlHeader)(l.cacheControl)),await (0,o.I)(N,O,new Response(l.value.body,{headers:m,status:l.value.status||200})),null};L?await g(L):await K.withPropagatedContext(a.headers,()=>K.trace(m.BaseServerSpan.handleRequest,{spanName:`${J} ${a.url}`,kind:i.SpanKind.SERVER,attributes:{"http.method":J,"http.target":a.url}},g))}catch(b){if(L||b instanceof s.NoFallbackError||await x.onRequestError(a,b,{routerKind:"App Router",routePath:E,routeType:"route",revalidateReason:(0,n.c)({isRevalidate:I,isOnDemandRevalidate:B})}),F)throw b;return await (0,o.I)(N,O,new Response(null,{status:500})),null}}},74075:a=>{"use strict";a.exports=require("zlib")},79551:a=>{"use strict";a.exports=require("url")},79646:a=>{"use strict";a.exports=require("child_process")},81630:a=>{"use strict";a.exports=require("http")},86439:a=>{"use strict";a.exports=require("next/dist/shared/lib/no-fallback-error.external")},91645:a=>{"use strict";a.exports=require("net")},94735:a=>{"use strict";a.exports=require("events")}};var b=require("../../../webpack-runtime.js");b.C(a);var c=b.X(0,[958,314,1],()=>b(b.s=67601));module.exports=c})();