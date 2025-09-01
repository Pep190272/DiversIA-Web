const nodemailer = require('nodemailer');

async function testGmail() {
  console.log('🔧 Iniciando test de Gmail...');
  
  // Verificar variables de entorno
  const gmailUser = process.env.GMAIL_USER;
  const gmailPassword = process.env.GMAIL_APP_PASSWORD;
  
  console.log('📧 GMAIL_USER:', gmailUser ? '✅ Configurado' : '❌ No configurado');
  console.log('🔑 GMAIL_APP_PASSWORD:', gmailPassword ? '✅ Configurado' : '❌ No configurado');
  
  if (!gmailUser || !gmailPassword) {
    console.error('❌ Credenciales de Gmail no configuradas');
    return false;
  }
  
  try {
    // Crear transporter de Gmail
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: gmailUser,
        pass: gmailPassword,
      },
    });
    
    console.log('🔌 Verificando conexión con Gmail...');
    
    // Verificar conexión
    await transporter.verify();
    console.log('✅ Conexión con Gmail exitosa');
    
    // Enviar email de prueba
    console.log('📤 Enviando email de prueba...');
    
    const mailOptions = {
      from: gmailUser,
      to: 'diversiaeternals@gmail.com',
      subject: '🧪 Test de configuración Gmail - DiversIA',
      text: 'Este es un email de prueba para verificar que Gmail está funcionando correctamente en DiversIA.',
      html: `
        <h2>🧪 Test de Gmail - DiversIA</h2>
        <p>Este email confirma que Gmail está configurado correctamente para DiversIA.</p>
        <ul>
          <li>✅ Configuración de Gmail: OK</li>
          <li>✅ Autenticación: OK</li>
          <li>✅ Envío de emails: OK</li>
        </ul>
        <p>Fecha del test: ${new Date().toLocaleString('es-ES')}</p>
      `
    };
    
    const result = await transporter.sendMail(mailOptions);
    console.log('✅ Email enviado exitosamente:', result.messageId);
    console.log('📬 Email enviado a: diversiaeternals@gmail.com');
    
    return true;
    
  } catch (error) {
    console.error('❌ Error con Gmail:', error.message);
    return false;
  }
}

// Ejecutar test
testGmail()
  .then(success => {
    if (success) {
      console.log('\n🎉 ¡Gmail configurado correctamente para DiversIA!');
      console.log('✅ El sistema de emails automáticos está listo');
    } else {
      console.log('\n❌ Hay problemas con la configuración de Gmail');
    }
    process.exit(success ? 0 : 1);
  })
  .catch(error => {
    console.error('💥 Error ejecutando test:', error);
    process.exit(1);
  });