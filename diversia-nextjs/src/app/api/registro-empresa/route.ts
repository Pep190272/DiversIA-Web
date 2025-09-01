import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { z } from 'zod';
import { emailService } from '@/lib/email';

const empresaSchema = z.object({
  nombre_empresa: z.string().min(1, 'El nombre de la empresa es requerido'),
  email_contacto: z.string().email('Email inválido'),
  telefono: z.string().optional(),
  ciudad: z.string().min(1, 'La ciudad es requerida'),
  sector: z.string().min(1, 'El sector es requerido'),
  tamano_empresa: z.string().min(1, 'El tamaño de empresa es requerido'),
  sitio_web: z.string().optional(),
  descripcion_empresa: z.string().optional(),
  politicas_inclusion: z.string().optional(),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validatedData = empresaSchema.parse(body);

    // Verificar si la empresa ya existe
    const existingCompany = await prisma.company.findFirst({
      where: { email_contacto: validatedData.email_contacto }
    });

    if (existingCompany) {
      // Actualizar empresa existente
      const updatedCompany = await prisma.company.update({
        where: { id: existingCompany.id },
        data: {
          nombre_empresa: validatedData.nombre_empresa,
          telefono: validatedData.telefono,
          ciudad: validatedData.ciudad,
          sector: validatedData.sector,
          tamano_empresa: validatedData.tamano_empresa,
          sitio_web: validatedData.sitio_web,
          descripcion_empresa: validatedData.descripcion_empresa,
          politicas_inclusion: validatedData.politicas_inclusion,
          updated_at: new Date(),
        }
      });

      return NextResponse.json({
        success: true,
        message: `¡Información de ${validatedData.nombre_empresa} actualizada exitosamente!`,
        data: updatedCompany
      });
    }

    // Crear nueva empresa
    const newCompany = await prisma.company.create({
      data: {
        nombre_empresa: validatedData.nombre_empresa,
        email_contacto: validatedData.email_contacto,
        telefono: validatedData.telefono,
        ciudad: validatedData.ciudad,
        sector: validatedData.sector,
        tamano_empresa: validatedData.tamano_empresa,
        sitio_web: validatedData.sitio_web,
        descripcion_empresa: validatedData.descripcion_empresa,
        politicas_inclusion: validatedData.politicas_inclusion,
      }
    });

    // Enviar emails de forma asíncrona
    Promise.all([
      // Email de bienvenida a la empresa
      emailService.sendCompanyWelcomeEmail({
        nombre_empresa: validatedData.nombre_empresa,
        email: validatedData.email_contacto,
        sector: validatedData.sector,
        tamano: validatedData.tamano_empresa,
      }),
      // Email de notificación a DiversIA
      emailService.sendCompanyNotificationEmail({
        nombre_empresa: validatedData.nombre_empresa,
        email: validatedData.email_contacto,
        telefono: validatedData.telefono || undefined,
        ciudad: validatedData.ciudad,
        sector: validatedData.sector,
        tamano_empresa: validatedData.tamano_empresa,
        fecha_registro: new Date().toLocaleString('es-ES', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        }),
      }),
    ]).catch(error => {
      console.error('❌ Error enviando emails de empresa:', error);
    });

    return NextResponse.json({
      success: true,
      message: `¡${validatedData.nombre_empresa} se ha registrado exitosamente! Nos pondremos en contacto pronto para discutir oportunidades de inclusión laboral.`,
      data: newCompany
    });

  } catch (error) {
    console.error('Error processing company registration:', error);
    
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { success: false, error: 'Datos de formulario inválidos', details: error.issues },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { success: false, error: 'Error al procesar el registro de empresa' },
      { status: 500 }
    );
  }
}