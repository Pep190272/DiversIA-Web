import nodemailer from 'nodemailer';

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

export interface CompanyWelcomeEmailData {
  nombre_empresa: string;
  email: string;
  sector: string;
  tamano: string;
}

export interface CompanyNotificationEmailData {
  nombre_empresa: string;
  email: string;
  telefono?: string;
  ciudad: string;
  sector: string;
  tamano_empresa: string;
  fecha_registro: string;
}

export interface AssociationWelcomeEmailData {
  nombre_asociacion: string;
  email: string;
  contacto_nombre: string;
  pais: string;
  neurodivergencias: string[];
}

export interface AssociationNotificationEmailData {
  nombre_asociacion: string;
  email: string;
  telefono?: string;
  ciudad: string;
  pais: string;
  contacto_nombre: string;
  fecha_registro: string;
}

// Clase principal para manejo de emails - SOLO GMAIL
export class EmailService {
  private transporter: nodemailer.Transporter | null = null;
  private isConfigured: boolean = false;

  constructor() {
    this.initializeGmail();
  }

  private initializeGmail() {
    // Solo Gmail - nada más
    const gmailUser = process.env.GMAIL_USER;
    const gmailPassword = process.env.GMAIL_APP_PASSWORD;

    if (gmailUser && gmailPassword) {
      this.setupGmail(gmailUser, gmailPassword);
      this.isConfigured = true;
      console.log('✅ Gmail configurado correctamente');
    } else {
      console.error('❌ Gmail no configurado - se requieren GMAIL_USER y GMAIL_APP_PASSWORD');
      this.isConfigured = false;
    }
  }

  private setupGmail(user: string, password: string) {
    this.transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: user,
        pass: password, // App Password de Google
      },
    });
  }

  // Método principal para enviar emails - SOLO GMAIL
  async sendEmail(config: EmailConfig): Promise<boolean> {
    if (!this.isConfigured || !this.transporter) {
      console.error('❌ Gmail no configurado. Configure GMAIL_USER y GMAIL_APP_PASSWORD');
      return false;
    }

    try {
      console.log('📧 Enviando email con Gmail...');
      
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
      console.error('❌ Error enviando email con Gmail:', error);
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
    const diversiaEmail = 'diversiaeternals@gmail.com';
    const notificationHtml = this.generateNotificationEmail(data);
    const notificationText = this.generateNotificationEmailText(data);

    return await this.sendEmail({
      to: diversiaEmail,
      subject: `🔔 Nuevo registro en DiversIA - ${data.nombre}`,
      html: notificationHtml,
      text: notificationText,
    });
  }

  // Email de bienvenida para empresas
  async sendCompanyWelcomeEmail(data: CompanyWelcomeEmailData): Promise<boolean> {
    const welcomeHtml = this.generateCompanyWelcomeEmail(data);
    const welcomeText = this.generateCompanyWelcomeEmailText(data);

    return await this.sendEmail({
      to: data.email,
      subject: `🤝 ¡Bienvenida ${data.nombre_empresa} a DiversIA!`,
      html: welcomeHtml,
      text: welcomeText,
    });
  }

  // Email de notificación de empresa para DiversIA
  async sendCompanyNotificationEmail(data: CompanyNotificationEmailData): Promise<boolean> {
    const diversiaEmail = 'diversiaeternals@gmail.com';
    const notificationHtml = this.generateCompanyNotificationEmail(data);
    const notificationText = this.generateCompanyNotificationEmailText(data);

    return await this.sendEmail({
      to: diversiaEmail,
      subject: `🏢 Nueva empresa registrada - ${data.nombre_empresa}`,
      html: notificationHtml,
      text: notificationText,
    });
  }

  // Email de bienvenida para asociaciones
  async sendAssociationWelcomeEmail(data: AssociationWelcomeEmailData): Promise<boolean> {
    const welcomeHtml = this.generateAssociationWelcomeEmail(data);
    const welcomeText = this.generateAssociationWelcomeEmailText(data);

    return await this.sendEmail({
      to: data.email,
      subject: `🤝 ¡Bienvenida ${data.nombre_asociacion} a DiversIA!`,
      html: welcomeHtml,
      text: welcomeText,
    });
  }

  // Email de notificación de asociación para DiversIA
  async sendAssociationNotificationEmail(data: AssociationNotificationEmailData): Promise<boolean> {
    const diversiaEmail = 'diversiaeternals@gmail.com';
    const notificationHtml = this.generateAssociationNotificationEmail(data);
    const notificationText = this.generateAssociationNotificationEmailText(data);

    return await this.sendEmail({
      to: diversiaEmail,
      subject: `🏛️ Nueva asociación registrada - ${data.nombre_asociacion}`,
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

Si tienes preguntas, responde a este email o escríbenos a diversiaeternals@gmail.com

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

  // PLANTILLAS PARA EMPRESAS
  private generateCompanyWelcomeEmail(data: CompanyWelcomeEmailData): string {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .highlight { background: #eff6ff; padding: 20px; border-radius: 8px; border-left: 4px solid #2563eb; margin: 20px 0; }
            .button { background: #2563eb; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
            .footer { text-align: center; color: #666; font-size: 14px; margin-top: 30px; }
            ul { margin: 15px 0; padding-left: 20px; }
            li { margin: 8px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤝 ¡Bienvenida a DiversIA!</h1>
                <p>Juntos construiremos un futuro laboral más inclusivo</p>
            </div>
            <div class="content">
                <h2>Estimado equipo de ${data.nombre_empresa},</h2>
                <p>¡Nos emociona que hayan decidido unirse a DiversIA! Su compromiso con la inclusión laboral marca la diferencia en la vida de personas con neurodivergencia.</p>
                
                <div class="highlight">
                    <h3>💼 ¿Qué viene ahora?</h3>
                    <ul>
                        <li>Nuestro equipo revisará su perfil empresarial</li>
                        <li>Identificaremos candidatos que encajen perfectamente con su cultura</li>
                        <li>Les presentaremos talento neurodivergente excepcional</li>
                        <li>Les apoyaremos en todo el proceso de inclusión</li>
                    </ul>
                </div>

                <h3>🎯 Beneficios de contratar talento neurodivergente:</h3>
                <ul>
                    <li>✅ Diversidad de pensamiento e innovación</li>
                    <li>✅ Habilidades únicas y especializadas</li>
                    <li>✅ Alta atención al detalle y precisión</li>
                    <li>✅ Lealtad y compromiso excepcional</li>
                    <li>✅ Perspectivas frescas para resolver problemas</li>
                </ul>

                <p><strong>Sector:</strong> ${data.sector}<br>
                <strong>Tamaño de empresa:</strong> ${data.tamano}</p>

                <p>Nos pondremos en contacto pronto para discutir cómo podemos ayudarles a encontrar el talento perfecto para ${data.nombre_empresa}.</p>

                <a href="mailto:diversiaeternals@gmail.com" class="button">Contáctanos para más información</a>

                <p><strong>¡Gracias por apostar por la inclusión!</strong></p>
            </div>
            <div class="footer">
                <p>DiversIA - Conectando empresas comprometidas con talento excepcional</p>
            </div>
        </div>
    </body>
    </html>
    `;
  }

  private generateCompanyWelcomeEmailText(data: CompanyWelcomeEmailData): string {
    return `
¡Bienvenida ${data.nombre_empresa} a DiversIA!

Nos emociona que hayan decidido unirse a DiversIA. Su compromiso con la inclusión laboral marca la diferencia.

¿Qué viene ahora?
- Nuestro equipo revisará su perfil empresarial
- Identificaremos candidatos que encajen perfectamente con su cultura  
- Les presentaremos talento neurodivergente excepcional
- Les apoyaremos en todo el proceso de inclusión

Beneficios de contratar talento neurodivergente:
✅ Diversidad de pensamiento e innovación
✅ Habilidades únicas y especializadas
✅ Alta atención al detalle y precisión
✅ Lealtad y compromiso excepcional
✅ Perspectivas frescas para resolver problemas

Sector: ${data.sector}
Tamaño de empresa: ${data.tamano}

Nos pondremos en contacto pronto para discutir cómo podemos ayudarles a encontrar el talento perfecto.

¡Gracias por apostar por la inclusión!

DiversIA - Conectando empresas comprometidas con talento excepcional
    `;
  }

  private generateCompanyNotificationEmail(data: CompanyNotificationEmailData): string {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #1e40af; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
            .content { background: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .urgent { background: #dbeafe; border-left: 4px solid #2563eb; padding: 15px; margin: 15px 0; }
            .data-section { background: #f8fafc; padding: 15px; border-radius: 6px; margin: 15px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏢 Nueva Empresa Registrada</h1>
                <p>Se ha registrado una nueva empresa en DiversIA</p>
            </div>
            <div class="content">
                <div class="urgent">
                    <h3>⚡ Empresa Interesada en Inclusión</h3>
                    <p>Una nueva empresa quiere formar parte de nuestra red de empleadores inclusivos.</p>
                </div>

                <div class="data-section">
                    <h3>🏢 Información de la Empresa</h3>
                    <p><strong>Nombre:</strong> ${data.nombre_empresa}</p>
                    <p><strong>Email:</strong> ${data.email}</p>
                    ${data.telefono ? `<p><strong>Teléfono:</strong> ${data.telefono}</p>` : ''}
                    <p><strong>Ciudad:</strong> ${data.ciudad}</p>
                    <p><strong>Sector:</strong> ${data.sector}</p>
                    <p><strong>Tamaño:</strong> ${data.tamano_empresa}</p>
                    <p><strong>Fecha de Registro:</strong> ${data.fecha_registro}</p>
                </div>

                <div class="data-section">
                    <h3>📝 Próximos Pasos</h3>
                    <ul>
                        <li>Contactar a la empresa para agendar reunión inicial</li>
                        <li>Evaluar necesidades específicas de contratación</li>
                        <li>Presentar perfiles de candidatos adecuados</li>
                        <li>Facilitar el proceso de matching</li>
                    </ul>
                </div>

                <p><strong>¡Oportunidad para generar impacto laboral!</strong></p>
            </div>
        </div>
    </body>
    </html>
    `;
  }

  private generateCompanyNotificationEmailText(data: CompanyNotificationEmailData): string {
    return `
🏢 NUEVA EMPRESA REGISTRADA EN DIVERSIA

Una nueva empresa quiere formar parte de nuestra red de empleadores inclusivos:

🏢 INFORMACIÓN DE LA EMPRESA:
- Nombre: ${data.nombre_empresa}
- Email: ${data.email}
${data.telefono ? `- Teléfono: ${data.telefono}` : ''}
- Ciudad: ${data.ciudad}
- Sector: ${data.sector}
- Tamaño: ${data.tamano_empresa}
- Fecha de Registro: ${data.fecha_registro}

📝 PRÓXIMOS PASOS:
- Contactar a la empresa para agendar reunión inicial
- Evaluar necesidades específicas de contratación
- Presentar perfiles de candidatos adecuados
- Facilitar el proceso de matching

¡Oportunidad para generar impacto laboral!
    `;
  }

  // PLANTILLAS PARA ASOCIACIONES
  private generateAssociationWelcomeEmail(data: AssociationWelcomeEmailData): string {
    const neurodivergenciasText = data.neurodivergencias.length > 0 
      ? data.neurodivergencias.join(', ') 
      : 'Diversas neurodivergencias';

    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #ffffff; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .highlight { background: #ecfdf5; padding: 20px; border-radius: 8px; border-left: 4px solid #059669; margin: 20px 0; }
            .button { background: #059669; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
            .footer { text-align: center; color: #666; font-size: 14px; margin-top: 30px; }
            ul { margin: 15px 0; padding-left: 20px; }
            li { margin: 8px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤝 ¡Bienvenida a DiversIA!</h1>
                <p>Juntos amplificaremos el impacto de la inclusión</p>
            </div>
            <div class="content">
                <h2>Estimado/a ${data.contacto_nombre} de ${data.nombre_asociacion},</h2>
                <p>¡Es un honor que se unan a nuestra red de organizaciones comprometidas con la neurodiversidad! Su experiencia y conocimiento serán fundamentales para crear más oportunidades.</p>
                
                <div class="highlight">
                    <h3>🌟 Oportunidades de Colaboración</h3>
                    <ul>
                        <li>Referir candidatos de su organización a oportunidades laborales</li>
                        <li>Colaborar en programas de capacitación empresarial</li>
                        <li>Participar en eventos y talleres de sensibilización</li>
                        <li>Compartir mejores prácticas de apoyo e inclusión</li>
                    </ul>
                </div>

                <h3>🎯 Su Especialización:</h3>
                <p><strong>Neurodivergencias atendidas:</strong> ${neurodivergenciasText}</p>
                <p><strong>Ubicación:</strong> ${data.pais}</p>

                <h3>💡 Cómo podemos trabajar juntos:</h3>
                <ul>
                    <li>✅ Identificar miembros listos para oportunidades laborales</li>
                    <li>✅ Proporcionar recursos de empleabilidad</li>
                    <li>✅ Capacitar empresas sobre neurodiversidad</li>
                    <li>✅ Crear programas de mentorías laborales</li>
                </ul>

                <p>Nos pondremos en contacto pronto para explorar cómo ${data.nombre_asociacion} puede ser parte activa de nuestra misión.</p>

                <a href="mailto:diversiaeternals@gmail.com" class="button">Conversemos sobre colaboraciones</a>

                <p><strong>¡Gracias por su dedicación a la comunidad neurodivergente!</strong></p>
            </div>
            <div class="footer">
                <p>DiversIA - Uniendo fuerzas por la inclusión laboral neurodivergente</p>
            </div>
        </div>
    </body>
    </html>
    `;
  }

  private generateAssociationWelcomeEmailText(data: AssociationWelcomeEmailData): string {
    const neurodivergenciasText = data.neurodivergencias.length > 0 
      ? data.neurodivergencias.join(', ') 
      : 'Diversas neurodivergencias';

    return `
¡Bienvenida ${data.nombre_asociacion} a DiversIA!

Estimado/a ${data.contacto_nombre},

Es un honor que se unan a nuestra red de organizaciones comprometidas con la neurodiversidad.

Oportunidades de Colaboración:
- Referir candidatos de su organización a oportunidades laborales
- Colaborar en programas de capacitación empresarial  
- Participar en eventos y talleres de sensibilización
- Compartir mejores prácticas de apoyo e inclusión

Su Especialización:
- Neurodivergencias atendidas: ${neurodivergenciasText}
- Ubicación: ${data.pais}

Cómo podemos trabajar juntos:
✅ Identificar miembros listos para oportunidades laborales
✅ Proporcionar recursos de empleabilidad
✅ Capacitar empresas sobre neurodiversidad
✅ Crear programas de mentorías laborales

Nos pondremos en contacto pronto para explorar cómo pueden ser parte activa de nuestra misión.

¡Gracias por su dedicación a la comunidad neurodivergente!

DiversIA - Uniendo fuerzas por la inclusión laboral neurodivergente
    `;
  }

  private generateAssociationNotificationEmail(data: AssociationNotificationEmailData): string {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #047857; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
            .content { background: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .urgent { background: #ecfdf5; border-left: 4px solid #059669; padding: 15px; margin: 15px 0; }
            .data-section { background: #f8fafc; padding: 15px; border-radius: 6px; margin: 15px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏛️ Nueva Asociación Registrada</h1>
                <p>Se ha registrado una nueva asociación en DiversIA</p>
            </div>
            <div class="content">
                <div class="urgent">
                    <h3>⚡ Oportunidad de Alianza</h3>
                    <p>Una nueva asociación quiere colaborar en la misión de inclusión laboral.</p>
                </div>

                <div class="data-section">
                    <h3>🏛️ Información de la Asociación</h3>
                    <p><strong>Nombre:</strong> ${data.nombre_asociacion}</p>
                    <p><strong>Contacto:</strong> ${data.contacto_nombre}</p>
                    <p><strong>Email:</strong> ${data.email}</p>
                    ${data.telefono ? `<p><strong>Teléfono:</strong> ${data.telefono}</p>` : ''}
                    <p><strong>País:</strong> ${data.pais}</p>
                    <p><strong>Ciudad:</strong> ${data.ciudad}</p>
                    <p><strong>Fecha de Registro:</strong> ${data.fecha_registro}</p>
                </div>

                <div class="data-section">
                    <h3>📝 Próximos Pasos</h3>
                    <ul>
                        <li>Contactar para agendar reunión de colaboración</li>
                        <li>Explorar oportunidades de referencia de candidatos</li>
                        <li>Discutir programas conjuntos de capacitación</li>
                        <li>Establecer canales de comunicación regulares</li>
                    </ul>
                </div>

                <p><strong>¡Oportunidad para expandir nuestra red de apoyo!</strong></p>
            </div>
        </div>
    </body>
    </html>
    `;
  }

  private generateAssociationNotificationEmailText(data: AssociationNotificationEmailData): string {
    return `
🏛️ NUEVA ASOCIACIÓN REGISTRADA EN DIVERSIA

Una nueva asociación quiere colaborar en la misión de inclusión laboral:

🏛️ INFORMACIÓN DE LA ASOCIACIÓN:
- Nombre: ${data.nombre_asociacion}
- Contacto: ${data.contacto_nombre}
- Email: ${data.email}
${data.telefono ? `- Teléfono: ${data.telefono}` : ''}
- País: ${data.pais}
- Ciudad: ${data.ciudad}
- Fecha de Registro: ${data.fecha_registro}

📝 PRÓXIMOS PASOS:
- Contactar para agendar reunión de colaboración
- Explorar oportunidades de referencia de candidatos
- Discutir programas conjuntos de capacitación
- Establecer canales de comunicación regulares

¡Oportunidad para expandir nuestra red de apoyo!
    `;
  }

  // Método para probar la configuración
  async testGmailConfiguration(): Promise<boolean> {
    if (!this.isConfigured || !this.transporter) {
      console.log('❌ Gmail no configurado');
      return false;
    }

    try {
      const testEmail = process.env.GMAIL_USER || 'test@diversia.com';
      
      return await this.sendEmail({
        to: testEmail,
        subject: 'Test de configuración Gmail - DiversIA',
        text: 'Este es un email de prueba para verificar que Gmail está funcionando correctamente.',
        html: '<p>Este es un email de prueba para verificar que Gmail está funcionando correctamente.</p>'
      });
    } catch (error) {
      console.error('❌ Error en test de Gmail:', error);
      return false;
    }
  }
}

// Instancia singleton del servicio
export const emailService = new EmailService();