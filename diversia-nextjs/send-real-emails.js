const nodemailer = require('nodemailer');

async function sendRealEmails() {
  console.log('📧 Enviando emails reales con Gmail...');
  
  // Verificar credenciales
  const gmailUser = process.env.GMAIL_USER;
  const gmailPassword = process.env.GMAIL_APP_PASSWORD;
  
  if (!gmailUser || !gmailPassword) {
    console.error('❌ Credenciales de Gmail no configuradas');
    return false;
  }
  
  try {
    // Configurar Gmail
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: gmailUser,
        pass: gmailPassword,
      },
    });
    
    console.log('✅ Gmail configurado, verificando conexión...');
    await transporter.verify();
    console.log('✅ Conexión con Gmail exitosa');
    
    // 1. EMAIL DE BIENVENIDA para jose190272@gmail.com
    console.log('\n📤 Enviando email de bienvenida a jose190272@gmail.com...');
    
    const welcomeEmail = {
      from: gmailUser,
      to: 'jose190272@gmail.com',
      subject: '🎉 ¡Bienvenido a DiversIA! Tu perfil ha sido creado',
      text: `¡Hola José!

Tu perfil ha sido creado exitosamente en DiversIA.

¿Qué pasa ahora?
- Estamos revisando tu perfil para crear las mejores oportunidades
- Nuestro equipo identificará empresas que valoren tu talento único
- Te contactaremos con oportunidades laborales que realmente encajen contigo

En DiversIA entendemos que tu neurodivergencia es una fortaleza, no una limitación.

Trabajamos con empresas que:
✅ Valoran la diversidad de pensamiento
✅ Ofrecen adaptaciones del entorno laboral  
✅ Buscan activamente talento neurodivergente
✅ Entienden el potencial único que aportas

Mantente atento/a a tu correo. Te contactaremos pronto con oportunidades emocionantes.

Si tienes preguntas, responde a este email o escríbenos a diversiaeternals@gmail.com

¡Gracias por confiar en DiversIA para tu futuro laboral!

DiversIA - Conectando talento neurodivergente con oportunidades excepcionales`,
      html: `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .highlight { background: #f8f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin: 20px 0; }
            .button { background: #667eea; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
            .footer { text-align: center; color: #666; font-size: 14px; margin-top: 30px; }
            ul { margin: 15px 0; padding-left: 20px; }
            li { margin: 8px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 ¡Bienvenido a DiversIA!</h1>
                <p>Tu perfil ha sido creado exitosamente</p>
            </div>
            <div class="content">
                <h2>¡Hola José!</h2>
                <p>¡Qué emocionante tenerte en nuestra comunidad! Tu registro en DiversIA ha sido completado con éxito.</p>
                
                <div class="highlight">
                    <h3>🧠 ¿Qué pasa ahora?</h3>
                    <ul>
                        <li>Estamos revisando tu perfil para crear las mejores oportunidades</li>
                        <li>Nuestro equipo identificará empresas que valoren tu talento único</li>
                        <li>Te contactaremos con oportunidades laborales que realmente encajen contigo</li>
                    </ul>
                </div>

                <h3>💼 Tu Proceso de Empleabilidad</h3>
                <p>En DiversIA entendemos que tu neurodivergencia es una fortaleza, no una limitación. Trabajamos con empresas que:</p>
                <ul>
                    <li>✅ Valoran la diversidad de pensamiento</li>
                    <li>✅ Ofrecen adaptaciones del entorno laboral</li>
                    <li>✅ Buscan activamente talento neurodivergente</li>
                    <li>✅ Entienden el potencial único que aportas</li>
                </ul>

                <p>Mientras tanto, mantente atento/a a tu correo. Te contactaremos pronto con oportunidades emocionantes.</p>

                <a href="mailto:diversiaeternals@gmail.com" class="button">Contáctanos si tienes preguntas</a>

                <p><strong>¡Gracias por confiar en DiversIA para tu futuro laboral!</strong></p>
            </div>
            <div class="footer">
                <p>DiversIA - Conectando talento neurodivergente con oportunidades excepcionales</p>
                <p>Si no solicitaste este registro, puedes ignorar este email.</p>
            </div>
        </div>
    </body>
    </html>
      `
    };
    
    const welcomeResult = await transporter.sendMail(welcomeEmail);
    console.log('✅ Email de bienvenida enviado:', welcomeResult.messageId);
    
    // 2. EMAIL DE NOTIFICACIÓN para DiversIA
    console.log('\n📤 Enviando email de notificación a DiversIA...');
    
    const notificationEmail = {
      from: gmailUser,
      to: 'diversiaeternals@gmail.com',
      subject: '🔔 Confirmación: Email enviado a usuario registrado - José',
      text: `🔔 CONFIRMACIÓN DE ENVÍO - DIVERSIA

Se ha enviado un email de bienvenida a un usuario registrado:

📋 INFORMACIÓN DEL ENVÍO:
- Destinatario: jose190272@gmail.com
- Nombre: José
- Tipo de Email: Bienvenida para usuario registrado
- Fecha/Hora: ${new Date().toLocaleString('es-ES')}
- ID del Email: ${welcomeResult.messageId}

✅ EMAIL ENVIADO EXITOSAMENTE

📝 ESTADO DEL SISTEMA:
- Gmail configurado correctamente
- Sistema de emails automáticos funcionando
- Sin uso de SendGrid (eliminado completamente)

Este email confirma que el sistema de notificaciones de DiversIA está operativo.`,
      html: `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
            .content { background: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .success-section { background: #f0f9f0; padding: 15px; border-radius: 6px; border-left: 4px solid #10b981; margin: 15px 0; }
            .data-section { background: #f8fafc; padding: 15px; border-radius: 6px; margin: 15px 0; }
            .status-section { background: #fef3f2; padding: 15px; border-radius: 6px; border-left: 4px solid #22c55e; margin: 15px 0; }
            ul { margin: 10px 0; padding-left: 20px; }
            li { margin: 5px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔔 Confirmación de Envío</h1>
                <p>Email enviado exitosamente a usuario registrado</p>
            </div>
            <div class="content">
                <div class="success-section">
                    <h3>✅ Email Enviado Exitosamente</h3>
                    <p>Se ha enviado un email de bienvenida a un usuario registrado de DiversIA.</p>
                </div>

                <div class="data-section">
                    <h3>📋 Información del Envío</h3>
                    <ul>
                        <li><strong>Destinatario:</strong> jose190272@gmail.com</li>
                        <li><strong>Nombre:</strong> José</li>
                        <li><strong>Tipo de Email:</strong> Bienvenida para usuario registrado</li>
                        <li><strong>Fecha/Hora:</strong> ${new Date().toLocaleString('es-ES')}</li>
                        <li><strong>ID del Email:</strong> ${welcomeResult.messageId}</li>
                    </ul>
                </div>

                <div class="status-section">
                    <h3>📊 Estado del Sistema</h3>
                    <ul>
                        <li>✅ Gmail configurado correctamente</li>
                        <li>✅ Sistema de emails automáticos funcionando</li>
                        <li>✅ Sin uso de SendGrid (eliminado completamente)</li>
                        <li>✅ Emails exclusivamente con Gmail</li>
                    </ul>
                </div>

                <p><strong>El sistema de notificaciones de DiversIA está completamente operativo.</strong></p>
            </div>
        </div>
    </body>
    </html>
      `
    };
    
    const notificationResult = await transporter.sendMail(notificationEmail);
    console.log('✅ Email de notificación enviado:', notificationResult.messageId);
    
    console.log('\n🎉 ¡EMAILS ENVIADOS EXITOSAMENTE!');
    console.log('📧 Email de bienvenida → jose190272@gmail.com');
    console.log('🔔 Email de confirmación → diversiaeternals@gmail.com');
    
    return true;
    
  } catch (error) {
    console.error('❌ Error enviando emails:', error.message);
    return false;
  }
}

// Ejecutar envío de emails
sendRealEmails()
  .then(success => {
    if (success) {
      console.log('\n✅ MISIÓN COMPLETADA - Gmail funcionando perfectamente');
    } else {
      console.log('\n❌ Error en el envío de emails');
    }
    process.exit(success ? 0 : 1);
  })
  .catch(error => {
    console.error('💥 Error ejecutando envío:', error);
    process.exit(1);
  });