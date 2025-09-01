import { NextRequest, NextResponse } from 'next/server';
import { emailService } from '@/lib/email';

export async function POST(request: NextRequest) {
  try {
    const { type = 'test' } = await request.json();

    if (type === 'configuration') {
      // Probar la configuración de Gmail
      const testResult = await emailService.testGmailConfiguration();
      return NextResponse.json({
        success: testResult,
        service: 'Gmail',
        message: testResult ? 'Gmail configurado correctamente' : 'Gmail no configurado'
      });
    }

    if (type === 'welcome') {
      // Probar email de bienvenida
      const success = await emailService.sendWelcomeEmail({
        nombre: 'Usuario Test',
        email: 'diversiaeternals@gmail.com',
        tipo_neurodivergencia: 'TDAH'
      });

      return NextResponse.json({
        success,
        message: success ? 'Email de bienvenida enviado con Gmail' : 'Error enviando email de bienvenida'
      });
    }

    if (type === 'notification') {
      // Probar email de notificación
      const success = await emailService.sendNotificationEmail({
        nombre: 'Usuario Test Gmail',
        email: 'test@diversia.com',
        telefono: '+34 600 000 000',
        ciudad: 'Madrid',
        tipo_neurodivergencia: 'TDAH',
        fecha_registro: new Date().toLocaleString('es-ES')
      });

      return NextResponse.json({
        success,
        message: success ? 'Email de notificación enviado con Gmail' : 'Error enviando email de notificación'
      });
    }

    return NextResponse.json({
      success: false,
      error: 'Tipo de test no válido. Usa: configuration, welcome, o notification'
    }, { status: 400 });

  } catch (error) {
    console.error('Error en test de email:', error);
    return NextResponse.json({
      success: false,
      error: 'Error ejecutando test de email'
    }, { status: 500 });
  }
}