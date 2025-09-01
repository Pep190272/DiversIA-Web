import nodemailer from 'nodemailer';
import sgMail from '@sendgrid/mail';

// Configuración de tipos
export interface EmailConfig {
  to: string;
  subject: string;
  text?: string;
  html?: string;
}

export interface WelcomeEmailData {
  nombre: string;
  email: string;
  tipo_neurodivergencia?: string;
}

export interface NotificationEmailData {
  nombre: string;
  email: string;
  telefono?: string;
  ciudad?: string;
  tipo_neurodivergencia?: string;
  fecha_registro: string;
}

// Clase principal para manejo de emails
export class EmailService {
  private transporter: nodemailer.Transporter | null = null;
  private useGmail: boolean = false;
  private useSendGrid: boolean = false;

  constructor() {
    this.initializeServices();
  }

  private initializeServices() {
    // Verificar si tenemos credenciales de Gmail (PRIORIDAD)
    const gmailUser = process.env.GMAIL_USER;
    const gmailPassword = process.env.GMAIL_APP_PASSWORD || process.env.GMAIL_PASSWORD;

    if (gmailUser && gmailPassword) {
      this.setupGmail(gmailUser, gmailPassword);
      this.useGmail = true;
      console.log('✅ Gmail configurado como servicio principal de email');
    } else {
      console.warn('⚠️ Gmail no configurado - se requieren GMAIL_USER y GMAIL_APP_PASSWORD');
    }
    
    // SendGrid como backup solamente
    const sendGridKey = process.env.SENDGRID_API_KEY;
    if (sendGridKey) {
      sgMail.setApiKey(sendGridKey);
      this.useSendGrid = true;
      console.log('📧 SendGrid disponible como backup');
    }

    if (!this.useGmail && !this.useSendGrid) {
      console.error('❌ No se encontraron credenciales de email configuradas');
    }
  }

  private setupGmail(user: string, password: string) {
    this.transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: user,
        pass: password, // Debe ser una App Password, no la contraseña normal
      },
    });
  }

  // Método principal para enviar emails (GMAIL PRIMERO)
  async sendEmail(config: EmailConfig): Promise<boolean> {
    try {
      // PRIORIDAD 1: Intentar con Gmail
      if (this.useGmail && this.transporter) {
        console.log('📧 Enviando email con Gmail...');
        return await this.sendWithGmail(config);
      }
      
      // FALLBACK: Si Gmail no está disponible, usar SendGrid
      else if (this.useSendGrid) {
        console.log('📧 Gmail no disponible, usando SendGrid como fallback...');
        return await this.sendWithSendGrid(config);
      } 
      
      // ERROR: Ningún servicio disponible
      else {
        console.error('❌ No hay servicios de email configurados. Configure Gmail (GMAIL_USER + GMAIL_APP_PASSWORD)');
        return false;
      }
    } catch (error) {
      console.error('❌ Error enviando email:', error);
      return false;
    }
  }

  private async sendWithGmail(config: EmailConfig): Promise<boolean> {
    try {
      if (!this.transporter) return false;

      const mailOptions = {
        from: process.env.GMAIL_USER,
        to: config.to,
        subject: config.subject,
        text: config.text,
        html: config.html,
      };

      const result = await this.transporter.sendMail(mailOptions);
      console.log('✅ Email enviado con Gmail:', result.messageId);
      return true;
    } catch (error) {
      console.error('❌ Error con Gmail:', error);
      
      // Si falla Gmail, intentar con SendGrid como backup
      if (this.useSendGrid) {
        console.log('🔄 Intentando con SendGrid como backup...');
        return await this.sendWithSendGrid(config);
      }
      return false;
    }
  }

  private async sendWithSendGrid(config: EmailConfig): Promise<boolean> {
    try {
      const msg = {
        to: config.to,
        from: 'noreply@diversia.com',
        subject: config.subject,
        text: config.text,
        html: config.html
      };

      await sgMail.send(msg);
      console.log('✅ Email enviado con SendGrid');
      return true;
    } catch (error) {
      console.error('❌ Error con SendGrid:', error);
      return false;
    }
  }

  // Email de bienvenida para usuarios
  async sendWelcomeEmail(data: WelcomeEmailData): Promise<boolean> {
    const welcomeHtml = this.generateWelcomeEmail(data);
    const welcomeText = this.generateWelcomeEmailText(data);

    return await this.sendEmail({
      to: data.email,
      subject: '🎉 ¡Bienvenido/a a DiversIA! Tu perfil ha sido creado',
      html: welcomeHtml,
      text: welcomeText,
    });
  }

  // Email de notificación para DiversIA
  async sendNotificationEmail(data: NotificationEmailData): Promise<boolean> {
    const diversiaEmail = process.env.DIVERSIA_EMAIL || 'diversiaeternals@gmail.com';
    const notificationHtml = this.generateNotificationEmail(data);
    const notificationText = this.generateNotificationEmailText(data);

    return await this.sendEmail({
      to: diversiaEmail,
      subject: `🔔 Nuevo registro en DiversIA - ${data.nombre}`,
      html: notificationHtml,
      text: notificationText,
    });
  }

  // Generadores de plantillas HTML
  private generateWelcomeEmail(data: WelcomeEmailData): string {
    return `
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
                <h1>🎉 ¡Bienvenido/a a DiversIA!</h1>
                <p>Tu perfil ha sido creado exitosamente</p>
            </div>
            <div class="content">
                <h2>Hola ${data.nombre},</h2>
                <p>¡Qué emocionante tenerte en nuestra comunidad! Tu registro en DiversIA ha sido completado con éxito.</p>
                
                <div class="highlight">
                    <h3>🧠 ¿Qué pasa ahora?</h3>
                    <ul>
                        <li>Estamos revisando tu perfil para crear las mejores oportunidades</li>
                        <li>Nuestro equipo identificará empresas que valoren tu talento único</li>
                        <li>Te contactaremos con oportunidades laborales que realmente encajen contigo</li>
                        ${data.tipo_neurodivergencia ? `<li>Tu perfil especializado en <strong>${data.tipo_neurodivergencia}</strong> nos ayudará a encontrar el match perfecto</li>` : ''}
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

                <a href="mailto:contacto@diversia.com" class="button">Contáctanos si tienes preguntas</a>

                <p><strong>¡Gracias por confiar en DiversIA para tu futuro laboral!</strong></p>
            </div>
            <div class="footer">
                <p>DiversIA - Conectando talento neurodivergente con oportunidades excepcionales</p>
                <p>Si no solicitaste este registro, puedes ignorar este email.</p>
            </div>
        </div>
    </body>
    </html>
    `;
  }

  private generateWelcomeEmailText(data: WelcomeEmailData): string {
    return `
¡Bienvenido/a a DiversIA, ${data.nombre}!

Tu perfil ha sido creado exitosamente en nuestra plataforma.

¿Qué pasa ahora?
- Estamos revisando tu perfil para crear las mejores oportunidades
- Nuestro equipo identificará empresas que valoren tu talento único
- Te contactaremos con oportunidades laborales que realmente encajen contigo
${data.tipo_neurodivergencia ? `- Tu perfil especializado en ${data.tipo_neurodivergencia} nos ayudará a encontrar el match perfecto` : ''}

En DiversIA entendemos que tu neurodivergencia es una fortaleza, no una limitación.

Trabajamos con empresas que:
✅ Valoran la diversidad de pensamiento
✅ Ofrecen adaptaciones del entorno laboral  
✅ Buscan activamente talento neurodivergente
✅ Entienden el potencial único que aportas

Mantente atento/a a tu correo. Te contactaremos pronto con oportunidades emocionantes.

Si tienes preguntas, responde a este email o escríbenos a contacto@diversia.com

¡Gracias por confiar en DiversIA para tu futuro laboral!

DiversIA - Conectando talento neurodivergente con oportunidades excepcionales
    `;
  }

  private generateNotificationEmail(data: NotificationEmailData): string {
    return `
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
                    <h3>⚡ Acción Requerida</h3>
                    <p>Un nuevo usuario se ha registrado y está esperando seguimiento del equipo de DiversIA.</p>
                </div>

                <div class="data-section">
                    <h3>📋 Información del Usuario</h3>
                    <p><strong>Nombre:</strong> ${data.nombre}</p>
                    <p><strong>Email:</strong> ${data.email}</p>
                    ${data.telefono ? `<p><strong>Teléfono:</strong> ${data.telefono}</p>` : ''}
                    ${data.ciudad ? `<p><strong>Ciudad:</strong> ${data.ciudad}</p>` : ''}
                    ${data.tipo_neurodivergencia ? `<p><strong>Tipo de Neurodivergencia:</strong> ${data.tipo_neurodivergencia}</p>` : ''}
                    <p><strong>Fecha de Registro:</strong> ${data.fecha_registro}</p>
                </div>

                <div class="data-section">
                    <h3>📝 Próximos Pasos</h3>
                    <ul>
                        <li>Revisar el perfil completo en el panel administrativo</li>
                        <li>Validar la información proporcionada</li>
                        <li>Comenzar el proceso de matching con empresas</li>
                        <li>Contactar al usuario para seguimiento personalizado</li>
                    </ul>
                </div>

                <p><strong>Accede al panel administrativo para ver todos los detalles del perfil.</strong></p>
            </div>
        </div>
    </body>
    </html>
    `;
  }

  private generateNotificationEmailText(data: NotificationEmailData): string {
    return `
🔔 NUEVO REGISTRO EN DIVERSIA

Se ha registrado un nuevo usuario en la plataforma:

📋 INFORMACIÓN DEL USUARIO:
- Nombre: ${data.nombre}
- Email: ${data.email}
${data.telefono ? `- Teléfono: ${data.telefono}` : ''}
${data.ciudad ? `- Ciudad: ${data.ciudad}` : ''}
${data.tipo_neurodivergencia ? `- Tipo de Neurodivergencia: ${data.tipo_neurodivergencia}` : ''}
- Fecha de Registro: ${data.fecha_registro}

📝 PRÓXIMOS PASOS:
- Revisar el perfil completo en el panel administrativo
- Validar la información proporcionada  
- Comenzar el proceso de matching con empresas
- Contactar al usuario para seguimiento personalizado

Accede al panel administrativo para ver todos los detalles del perfil.
    `;
  }

  // Método para probar la configuración
  async testConfiguration(): Promise<{ gmail: boolean; sendgrid: boolean }> {
    const testEmail = process.env.GMAIL_USER || 'test@diversia.com';
    
    const gmailTest = this.useGmail ? await this.sendEmail({
      to: testEmail,
      subject: 'Test de configuración Gmail - DiversIA',
      text: 'Este es un email de prueba para verificar la configuración de Gmail.',
      html: '<p>Este es un email de prueba para verificar la configuración de Gmail.</p>'
    }) : false;

    const sendgridTest = this.useSendGrid ? await this.sendEmail({
      to: testEmail,
      subject: 'Test de configuración SendGrid - DiversIA',
      text: 'Este es un email de prueba para verificar la configuración de SendGrid.',
      html: '<p>Este es un email de prueba para verificar la configuración de SendGrid.</p>'
    }) : false;

    return {
      gmail: gmailTest,
      sendgrid: sendgridTest
    };
  }
}

// Instancia singleton del servicio
export const emailService = new EmailService();