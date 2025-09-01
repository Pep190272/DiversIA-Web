import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { z } from 'zod';
import { emailService } from '@/lib/email';

const asociacionSchema = z.object({
  nombre_asociacion: z.string().min(1, 'El nombre de la asociación es requerido'),
  acronimo: z.string().optional(),
  pais: z.string().min(1, 'El país es requerido'),
  ciudad: z.string().min(1, 'La ciudad es requerida'),
  email: z.string().email('Email inválido'),
  telefono: z.string().optional(),
  sitio_web: z.string().optional(),
  descripcion: z.string().optional(),
  contacto_nombre: z.string().min(1, 'El nombre de contacto es requerido'),
  contacto_cargo: z.string().optional(),
  neurodivergencias_atendidas: z.array(z.string()).optional(),
  servicios: z.array(z.string()).optional(),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validatedData = asociacionSchema.parse(body);

    // Verificar si la asociación ya existe
    const existingAssociation = await prisma.asociacion.findFirst({
      where: { email: validatedData.email }
    });

    if (existingAssociation) {
      // Actualizar asociación existente
      const updatedAssociation = await prisma.asociacion.update({
        where: { id: existingAssociation.id },
        data: {
          nombre_asociacion: validatedData.nombre_asociacion,
          acronimo: validatedData.acronimo,
          pais: validatedData.pais,
          ciudad: validatedData.ciudad,
          telefono: validatedData.telefono,
          sitio_web: validatedData.sitio_web,
          descripcion: validatedData.descripcion,
          contacto_nombre: validatedData.contacto_nombre,
          contacto_cargo: validatedData.contacto_cargo,
          neurodivergencias_atendidas: validatedData.neurodivergencias_atendidas?.join(','),
          servicios: validatedData.servicios?.join(','),
          updated_at: new Date(),
        }
      });

      return NextResponse.json({
        success: true,
        message: `¡Información de ${validatedData.nombre_asociacion} actualizada exitosamente!`,
        data: updatedAssociation
      });
    }

    // Crear nueva asociación
    const newAssociation = await prisma.asociacion.create({
      data: {
        nombre_asociacion: validatedData.nombre_asociacion,
        acronimo: validatedData.acronimo,
        pais: validatedData.pais,
        ciudad: validatedData.ciudad,
        email: validatedData.email,
        telefono: validatedData.telefono,
        sitio_web: validatedData.sitio_web,
        descripcion: validatedData.descripcion,
        contacto_nombre: validatedData.contacto_nombre,
        contacto_cargo: validatedData.contacto_cargo,
        neurodivergencias_atendidas: validatedData.neurodivergencias_atendidas?.join(','),
        servicios: validatedData.servicios?.join(','),
      }
    });

    // Enviar emails de forma asíncrona
    Promise.all([
      // Email de bienvenida a la asociación
      emailService.sendAssociationWelcomeEmail({
        nombre_asociacion: validatedData.nombre_asociacion,
        email: validatedData.email,
        contacto_nombre: validatedData.contacto_nombre,
        pais: validatedData.pais,
        neurodivergencias: validatedData.neurodivergencias_atendidas || [],
      }),
      // Email de notificación a DiversIA
      emailService.sendAssociationNotificationEmail({
        nombre_asociacion: validatedData.nombre_asociacion,
        email: validatedData.email,
        telefono: validatedData.telefono || undefined,
        ciudad: validatedData.ciudad,
        pais: validatedData.pais,
        contacto_nombre: validatedData.contacto_nombre,
        fecha_registro: new Date().toLocaleString('es-ES', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        }),
      }),
    ]).catch(error => {
      console.error('❌ Error enviando emails de asociación:', error);
    });

    return NextResponse.json({
      success: true,
      message: `¡${validatedData.nombre_asociacion} se ha registrado exitosamente! Nos pondremos en contacto pronto para explorar colaboraciones.`,
      data: newAssociation
    });

  } catch (error) {
    console.error('Error processing association registration:', error);
    
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { success: false, error: 'Datos de formulario inválidos', details: error.issues },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { success: false, error: 'Error al procesar el registro de asociación' },
      { status: 500 }
    );
  }
}